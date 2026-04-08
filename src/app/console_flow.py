"""콘솔 메뉴 및 모드 1(3×3) 사용자 입력 흐름."""

from __future__ import annotations

import time
from collections.abc import Callable

from npu.constants import DEFAULT_EPSILON, LABEL_UNDECIDED
from npu.judgement import judge_ab
from npu.mac import compute_mac
from npu_io.parse import parse_row, read_square_matrix_lines


from app.constants import MENU_USER_INPUT_3X3, MENU_JSON_ANALYSIS, MENU_PATTERN_GENERATOR


def _prompt_choice(input_fn: Callable[[str], str]) -> str:
    print("\n입력 방식을 선택하세요.")
    print("  1) 사용자 입력(3×3)")
    print("  2) data.json 분석")
    print("  3) 패턴 자동 생성기(보너스 연계)")
    return input_fn("선택 (1-3): ").strip()


def run_main_menu(
    input_fn: Callable[[str], str] | None = None,
) -> None:
    """시작 메뉴 루프. 기본값은 내장 input()."""
    reader = input_fn or input
    while True:
        try:
            choice = _prompt_choice(reader)
        except EOFError:
            print("\n종료합니다.")
            return
        if choice == MENU_USER_INPUT_3X3:
            run_user_input_mode_3x3(reader)
            continue
        if choice == MENU_JSON_ANALYSIS:
            print("\n아직 구현되지 않았습니다. (data.json 분석 모드)")
            continue
        if choice == MENU_PATTERN_GENERATOR:
            print("\n아직 구현되지 않았습니다. (패턴 자동 생성기)")
            continue
        print(f"\n{MENU_USER_INPUT_3X3}, {MENU_JSON_ANALYSIS}, {MENU_PATTERN_GENERATOR} 중에서 입력해 주세요.")


def _read_3x3_matrix_lines(label: str, reader: Callable[[str], str]) -> list[list[float]]:
    print(f"\n{label}")
    print("각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
    lines: list[str] = []
    for i in range(3):
        while True:
            line = reader(f"  줄 {i + 1}/3: ")
            try:
                parse_row(line, expected_count=3)
                lines.append(line)
                break
            except ValueError as e:
                print(e)
    return read_square_matrix_lines(lines, size=3)


def run_user_input_mode_3x3(reader: Callable[[str], str] | None = None) -> None:
    """3×3 필터 A/B + 패턴 입력 후 MAC·판정·시간 출력."""
    read = reader or input

    filter_a = _read_3x3_matrix_lines("필터 A (3×3)", read)
    filter_b = _read_3x3_matrix_lines("필터 B (3×3)", read)

    print("\n[저장 확인] 필터 A, B가 올바르게 입력되었습니다. 패턴을 이어서 입력합니다.")

    pattern = _read_3x3_matrix_lines("패턴 (3×3)", read)

    t0 = time.perf_counter()
    score_a = compute_mac(pattern, filter_a)
    score_b = compute_mac(pattern, filter_b)
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0

    verdict = judge_ab(score_a, score_b, epsilon=DEFAULT_EPSILON)
    verdict_display = "판정 불가" if verdict == LABEL_UNDECIDED else verdict

    print("\n--- 결과 ---")
    print(f"MAC 점수 (필터 A): {score_a}")
    print(f"MAC 점수 (필터 B): {score_b}")
    print(f"판정 결과: {verdict_display}")
    print(f"연산 시간: {elapsed_ms:.6f} ms (MAC 2회)")


def main() -> None:
    run_main_menu()
