"""콘솔 모드: data.json 로드·패턴별 MAC 판정·요약·벤치마크 출력."""

from __future__ import annotations

import time
from pathlib import Path

from src.npu.benchmark import (
    build_benchmark_rows,
    build_cross_pattern,
    build_x_pattern,
    format_benchmark_table,
)
from src.npu.constants import DEFAULT_EPSILON, LABEL_CROSS, LABEL_X
from src.npu.judgement import judge
from src.npu.labels import normalize_label
from src.npu.mac import compute_mac
from src.npu_io.json_loader import iter_pattern_cases, load_json
from src.npu_io.schema import (
    extract_size_from_pattern_key,
    select_filters_for_size,
    validate_pattern_and_filters,
)

from src.app.report import summarize_results


def run_data_json_mode(sDataPath: str | Path | None = None) -> None:
    """data.json을 로드해 케이스별 판정/PASS-FAIL/요약을 출력한다.

    인자가 없으면 이 파일 기준 프로젝트 루트의 data.json을 사용한다
    (`Path(__file__).resolve().parents[2] / "data.json"`).
    """
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
            dNormalizedFilters = {
                normalize_label(k): v for k, v in dRawFilters.items()
            }

            sNormalizedExpected = normalize_label(sExpectedRaw)
            validate_pattern_and_filters(
                lPatternInput=lPatternInput,
                dFiltersByLabel=dNormalizedFilters,
                iExpectedSize=iSize,
            )

            if LABEL_CROSS not in dNormalizedFilters or LABEL_X not in dNormalizedFilters:
                raise ValueError("both Cross and X filters are required for each size")

            fStart = time.perf_counter()
            fScoreCross = compute_mac(lPatternInput, dNormalizedFilters[LABEL_CROSS], iSize)
            fScoreX = compute_mac(lPatternInput, dNormalizedFilters[LABEL_X], iSize)
            fEnd = time.perf_counter()
            fElapsedMs = (fEnd - fStart) * 1000.0

            sVerdict = judge(fScoreCross, fScoreX, LABEL_CROSS, LABEL_X, fEpsilon=DEFAULT_EPSILON)
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
