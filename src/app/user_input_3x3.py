"""콘솔 모드: 3×3 필터 A/B·패턴 수동 입력 및 MAC·판정 출력."""

from __future__ import annotations

import time

from src.npu.benchmark import build_benchmark_rows, format_benchmark_table
from src.npu.constants import DEFAULT_EPSILON, LABEL_UNDECIDED
from src.npu.judgement import judge_ab
from src.npu.mac import compute_mac, validate_mac_inputs
from src.npu_io.parse import parse_row


def _read_3x3_matrix_lines(sLabel: str) -> list[list[float]]:
    print(f"\n{sLabel}")
    print("각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
    lMatrix: list[list[float]] = []
    for i in range(3):
        while True:
            sLine = input(f"  줄 {i + 1}/3: ")
            try:
                lMatrix.append(parse_row(sLine, iExpectedCount=3))
                break
            except ValueError as exc:
                print(exc)
    return lMatrix


def run_user_input_mode_3x3() -> None:
    """3×3 필터 A/B + 패턴 입력 후 MAC·판정·시간 출력."""
    while True:
        try:
            lFilterA = _read_3x3_matrix_lines("필터 A (3×3)")
            lFilterB = _read_3x3_matrix_lines("필터 B (3×3)")

            print("\n[저장 확인] 필터 A, B가 올바르게 입력되었습니다. 패턴을 이어서 입력합니다.")

            lPattern = _read_3x3_matrix_lines("패턴 (3×3)")
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
