"""콘솔 메뉴 및 모드 1(3×3) 사용자 입력 흐름."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

from src.npu.benchmark import (
    build_benchmark_rows,
    build_cross_pattern,
    build_x_pattern,
    format_benchmark_table,
)
from src.npu.constants import DEFAULT_EPSILON, LABEL_CROSS, LABEL_UNDECIDED, LABEL_X
from src.npu.judgement import judge_ab, judge_cross_vs_x
from src.npu.labels import normalize_expected
from src.npu.mac import compute_mac, validate_mac_inputs
from src.npu_io.json_loader import iter_pattern_cases, load_json
from src.npu_io.label_normalization import normalize_expected_and_filter_key
from src.npu_io.parse import parse_row, read_square_matrix_lines
from src.npu_io.schema import (
    extract_size_from_pattern_key,
    select_filters_for_size,
    validate_pattern_and_filters,
)


from src.app.constants import (
    MENU_JSON_ANALYSIS,
    MENU_USER_INPUT_3X3,
)
from src.app.report import summarize_results


def _prompt_choice(input_fn: Callable[[str], str]) -> str:
    print("\n입력 방식을 선택하세요.")
    print("  1) 사용자 입력(3×3)")
    print("  2) data.json 분석")
    return input_fn("선택 (1-2): ").strip()


def run_main_menu(
    input_fn: Callable[[str], str] | None = None,
) -> None:
    """시작 메뉴 루프. 기본값은 내장 input()."""
    fnReader = input_fn or input
    while True:
        try:
            sChoice = _prompt_choice(fnReader)
        except (EOFError, KeyboardInterrupt):
            print("\n입력이 중단되어 종료합니다.")
            return
        if sChoice == MENU_USER_INPUT_3X3:
            run_user_input_mode_3x3(fnReader)
            continue
        if sChoice == MENU_JSON_ANALYSIS:
            run_data_json_mode()
            continue
        print(
            f"\n{MENU_USER_INPUT_3X3}, {MENU_JSON_ANALYSIS} 중에서 입력해 주세요.",
        )


def _read_3x3_matrix_lines(sLabel: str, fnReader: Callable[[str], str]) -> list[list[float]]:
    print(f"\n{sLabel}")
    print("각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
    lLines: list[str] = []
    for i in range(3):
        while True:
            sLine = fnReader(f"  줄 {i + 1}/3: ")
            try:
                parse_row(sLine, iExpectedCount=3)
                lLines.append(sLine)
                break
            except ValueError as exc:
                print(exc)
    return read_square_matrix_lines(lLines, iSize=3)


def run_user_input_mode_3x3(reader: Callable[[str], str] | None = None) -> None:
    """3×3 필터 A/B + 패턴 입력 후 MAC·판정·시간 출력."""
    fnRead = reader or input

    while True:
        try:
            lFilterA = _read_3x3_matrix_lines("필터 A (3×3)", fnRead)
            lFilterB = _read_3x3_matrix_lines("필터 B (3×3)", fnRead)

            print("\n[저장 확인] 필터 A, B가 올바르게 입력되었습니다. 패턴을 이어서 입력합니다.")

            lPattern = _read_3x3_matrix_lines("패턴 (3×3)", fnRead)
        except (EOFError, KeyboardInterrupt):
            print("\n\n입력이 중단되어 메인 메뉴로 돌아갑니다.")
            return

        try:
            # 필터마다 패턴과의 형상을 검증한 뒤, 반환된 N이 서로 같은지 한 번 더 본다.
            iSizeA = validate_mac_inputs(lPattern, lFilterA)
            iSizeB = validate_mac_inputs(lPattern, lFilterB)
            if iSizeA != iSizeB:
                raise ValueError(
                    "MAC square size mismatch across filters after validation",
                )
        except ValueError as exc:
            print(f"\n[입력 검증 오류] {exc}")
            print(
                "패턴과 필터의 행·열 크기가 서로 같은지 확인한 뒤, 처음부터 다시 입력해 주세요.",
            )
            continue

        iSize = iSizeA
        fStart = time.perf_counter()
        fScoreA = compute_mac(lPattern, lFilterA, iSize)
        fScoreB = compute_mac(lPattern, lFilterB, iSize)
        fEnd = time.perf_counter()
        fElapsedMs = (fEnd - fStart) * 1000.0

        sVerdict = judge_ab(fScoreA, fScoreB, fEpsilon=DEFAULT_EPSILON)
        sVerdictDisplay = "판정 불가" if sVerdict == LABEL_UNDECIDED else sVerdict

        print("\n--- 결과 ---")
        print(f"MAC 점수 (필터 A): {fScoreA}")
        print(f"MAC 점수 (필터 B): {fScoreB}")
        print(f"판정 결과: {sVerdictDisplay}")
        print(f"연산 시간: {fElapsedMs:.6f} ms (MAC 2회)")
        lBenchmarkRows = build_benchmark_rows(
            [(3, lPattern, lFilterA, lFilterB)],
            iRepeats=10,
        )
        print("\n--- 성능 분석 (3×3) ---")
        print(format_benchmark_table(lBenchmarkRows))
        break


def run_data_json_mode(sDataPath: str | Path | None = None) -> None:
    """data.json을 로드해 케이스별 판정/PASS-FAIL/요약을 출력한다."""
    pTargetPath = Path(sDataPath) if sDataPath is not None else Path(__file__).resolve().parents[2] / "data.json"

    try:
        dData = load_json(pTargetPath)
    except Exception as exc:  # noqa: BLE001
        print(f"\n[data.json 로드 실패] {exc}")
        return

    dFiltersSection = dData.get("filters")
    if not isinstance(dFiltersSection, dict):
        print("\n[data.json 스키마 오류] 'filters' 섹션이 없거나 형식이 올바르지 않습니다.")
        return

    try:
        lPatternCases = iter_pattern_cases(dData)
    except Exception as exc:  # noqa: BLE001
        print(f"\n[data.json 스키마 오류] {exc}")
        return

    iTotal = 0
    iPassed = 0
    iFailed = 0
    lFailures: list[tuple[str, str]] = []

    print(f"\n[data.json 분석 시작] path={pTargetPath}")

    for sPatternKey, dPatternCase in lPatternCases:
        iTotal += 1
        try:
            iSize = extract_size_from_pattern_key(sPatternKey)
            lPatternInput = dPatternCase["input"]
            sExpectedRaw = dPatternCase["expected"]
            if not isinstance(sExpectedRaw, str):
                raise ValueError("expected must be a string")

            dRawFilters = select_filters_for_size(dFiltersSection, iSize=iSize)
            dNormalizedFilters: dict[str, list[list[float]]] = {}
            for sRawFilterKey, lFilterMatrix in dRawFilters.items():
                if not isinstance(sRawFilterKey, str):
                    raise ValueError("filter key must be a string")
                # 입력: raw_filter_key="cross"
                # 반환: normalized_filter_key="Cross"
                _, sNormalizedFilterKey = normalize_expected_and_filter_key(sExpectedRaw, sRawFilterKey)
                if sNormalizedFilterKey in dNormalizedFilters:
                    raise ValueError(
                        f"duplicate normalized filter label: {sNormalizedFilterKey}",
                    )
                dNormalizedFilters[sNormalizedFilterKey] = lFilterMatrix

            # 입력: expected_raw="+"
            # 반환: normalized_expected="Cross"
            sNormalizedExpected = normalize_expected(sExpectedRaw)
            validate_pattern_and_filters(
                lPatternInput=lPatternInput,
                dFiltersByLabel=dNormalizedFilters,
                iExpectedSize=iSize,
            )

            if LABEL_CROSS not in dNormalizedFilters or LABEL_X not in dNormalizedFilters:
                raise ValueError("both Cross and X filters are required for each size")

            iMacCross = validate_mac_inputs(lPatternInput, dNormalizedFilters[LABEL_CROSS])
            iMacX = validate_mac_inputs(lPatternInput, dNormalizedFilters[LABEL_X])
            if iMacCross != iMacX:
                raise ValueError("MAC square size mismatch across filters after validation")
            iMacSize = iMacCross
            fStart = time.perf_counter()
            fScoreCross = compute_mac(lPatternInput, dNormalizedFilters[LABEL_CROSS], iMacSize)
            fScoreX = compute_mac(lPatternInput, dNormalizedFilters[LABEL_X], iMacSize)
            fEnd = time.perf_counter()
            fElapsedMs = (fEnd - fStart) * 1000.0

            sVerdict = judge_cross_vs_x(fScoreCross, fScoreX, fEpsilon=DEFAULT_EPSILON)
            # 입력: verdict="Cross", normalized_expected="Cross"
            # 반환: pass_fail="PASS"
            sPassFail = "PASS" if sVerdict == sNormalizedExpected else "FAIL"
            if sPassFail == "PASS":
                iPassed += 1
            else:
                iFailed += 1
                lFailures.append(
                    (sPatternKey, f"expected={sNormalizedExpected}, verdict={sVerdict}"),
                )

            print(
                f"- {sPatternKey}: Cross={fScoreCross}, X={fScoreX}, verdict={sVerdict}, expected={sNormalizedExpected} -> {sPassFail} ({fElapsedMs:.6f} ms)",
            )
        except Exception as exc:  # noqa: BLE001
            iFailed += 1
            lFailures.append((sPatternKey, str(exc)))
            print(f"- {sPatternKey}: FAIL ({exc})")

    print()
    print(
        summarize_results(
            iTotal=iTotal,
            iPassed=iPassed,
            iFailed=iFailed,
            lFailuresDetail=lFailures,
        ),
    )

    lBenchmarkCases: list[tuple[int, list[list[float]], list[list[float]], list[list[float]]]] = []
    lBenchmarkCases.append((3, build_cross_pattern(3), build_cross_pattern(3), build_x_pattern(3)))
    for iSize in (5, 13, 25):
        try:
            dSizeFilters = select_filters_for_size(dFiltersSection, iSize=iSize)
            lBenchmarkCases.append(
                (
                    iSize,
                    build_cross_pattern(iSize),
                    dSizeFilters["cross"],
                    dSizeFilters["x"],
                ),
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[성능 분석 제외] size_{iSize}: {exc}")

    if lBenchmarkCases:
        lBenchmarkRows = build_benchmark_rows(lBenchmarkCases, iRepeats=10)
        print("\n--- 성능 분석 (3×3, 5×5, 13×13, 25×25) ---")
        print(format_benchmark_table(lBenchmarkRows))


def main() -> None:
    run_main_menu()
