"""콘솔 메뉴 및 모드 1(3×3) 사용자 입력 흐름."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

from npu.benchmark import (
    build_benchmark_rows,
    build_cross_pattern,
    build_x_pattern,
    format_benchmark_table,
)
from npu.constants import DEFAULT_EPSILON, LABEL_CROSS, LABEL_UNDECIDED, LABEL_X
from npu.judgement import judge_ab, judge_cross_vs_x
from npu.labels import normalize_expected
from npu.mac import compute_mac
from npu.pattern_generator import generate_cross_pattern, generate_x_pattern, validate_size
from npu_io.json_loader import iter_pattern_cases, load_json
from npu_io.label_normalization import normalize_expected_and_filter_key
from npu_io.parse import parse_row, read_square_matrix_lines
from npu_io.schema import (
    extract_size_from_pattern_key,
    select_filters_for_size,
    validate_pattern_and_filters,
)


from app.constants import (
    MENU_JSON_ANALYSIS,
    MENU_PATTERN_GENERATOR,
    MENU_USER_INPUT_3X3,
)
from app.report import summarize_results


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
            print("\n입력이 중단되어 종료합니다.")
            return
        except KeyboardInterrupt:
            print("\n입력이 중단되어 종료합니다.")
            return
        if choice == MENU_USER_INPUT_3X3:
            run_user_input_mode_3x3(reader)
            continue
        if choice == MENU_JSON_ANALYSIS:
            run_data_json_mode()
            continue
        if choice == MENU_PATTERN_GENERATOR:
            run_pattern_generator_mode(reader)
            continue
        print(
            f"\n{MENU_USER_INPUT_3X3}, {MENU_JSON_ANALYSIS}, {MENU_PATTERN_GENERATOR} 중에서 입력해 주세요.",
        )


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

    try:
        filter_a = _read_3x3_matrix_lines("필터 A (3×3)", read)
        filter_b = _read_3x3_matrix_lines("필터 B (3×3)", read)

        print("\n[저장 확인] 필터 A, B가 올바르게 입력되었습니다. 패턴을 이어서 입력합니다.")

        pattern = _read_3x3_matrix_lines("패턴 (3×3)", read)
    except KeyboardInterrupt:
        print("\n\n입력이 중단되어 메인 메뉴로 돌아갑니다.")
        return

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
    benchmark_rows = build_benchmark_rows(
        [(3, pattern, filter_a, filter_b)],
        repeats=10,
    )
    print("\n--- 성능 분석 (3×3) ---")
    print(format_benchmark_table(benchmark_rows))


def run_data_json_mode(data_path: str | Path | None = None) -> None:
    """data.json을 로드해 케이스별 판정/PASS-FAIL/요약을 출력한다."""
    target_path = Path(data_path) if data_path is not None else Path(__file__).resolve().parents[2] / "data.json"

    try:
        data = load_json(target_path)
    except Exception as e:  # noqa: BLE001
        print(f"\n[data.json 로드 실패] {e}")
        return

    filters_section = data.get("filters")
    if not isinstance(filters_section, dict):
        print("\n[data.json 스키마 오류] 'filters' 섹션이 없거나 형식이 올바르지 않습니다.")
        return

    try:
        pattern_cases = iter_pattern_cases(data)
    except Exception as e:  # noqa: BLE001
        print(f"\n[data.json 스키마 오류] {e}")
        return

    total = 0
    passed = 0
    failed = 0
    failures: list[tuple[str, str]] = []
    benchmark_rows: list[dict[str, float | int]] = []

    print(f"\n[data.json 분석 시작] path={target_path}")

    for pattern_key, pattern_case in pattern_cases:
        total += 1
        try:
            size = extract_size_from_pattern_key(pattern_key)
            pattern_input = pattern_case["input"]
            expected_raw = pattern_case["expected"]
            if not isinstance(expected_raw, str):
                raise ValueError("expected must be a string")

            raw_filters = select_filters_for_size(filters_section, size=size)
            normalized_filters: dict[str, list[list[float]]] = {}
            for raw_filter_key, filter_matrix in raw_filters.items():
                if not isinstance(raw_filter_key, str):
                    raise ValueError("filter key must be a string")
                _, normalized_filter_key = normalize_expected_and_filter_key(expected_raw, raw_filter_key)
                if normalized_filter_key in normalized_filters:
                    raise ValueError(
                        f"duplicate normalized filter label: {normalized_filter_key}",
                    )
                normalized_filters[normalized_filter_key] = filter_matrix

            normalized_expected = normalize_expected(expected_raw)
            validate_pattern_and_filters(
                pattern_input=pattern_input,
                filters_by_label=normalized_filters,
                expected_size=size,
            )

            if LABEL_CROSS not in normalized_filters or LABEL_X not in normalized_filters:
                raise ValueError("both Cross and X filters are required for each size")

            t0 = time.perf_counter()
            score_cross = compute_mac(pattern_input, normalized_filters[LABEL_CROSS])
            score_x = compute_mac(pattern_input, normalized_filters[LABEL_X])
            t1 = time.perf_counter()
            elapsed_ms = (t1 - t0) * 1000.0

            verdict = judge_cross_vs_x(score_cross, score_x, epsilon=DEFAULT_EPSILON)
            pass_fail = "PASS" if verdict == normalized_expected else "FAIL"
            if pass_fail == "PASS":
                passed += 1
            else:
                failed += 1
                failures.append(
                    (pattern_key, f"expected={normalized_expected}, verdict={verdict}"),
                )

            print(
                f"- {pattern_key}: Cross={score_cross}, X={score_x}, verdict={verdict}, expected={normalized_expected} -> {pass_fail} ({elapsed_ms:.6f} ms)",
            )
        except Exception as e:  # noqa: BLE001
            failed += 1
            failures.append((pattern_key, str(e)))
            print(f"- {pattern_key}: FAIL ({e})")

    print()
    print(
        summarize_results(
            total=total,
            passed=passed,
            failed=failed,
            failures_detail=failures,
        ),
    )

    benchmark_cases: list[tuple[int, list[list[float]], list[list[float]], list[list[float]]]] = []
    benchmark_cases.append((3, build_cross_pattern(3), build_cross_pattern(3), build_x_pattern(3)))
    for size in (5, 13, 25):
        try:
            size_filters = select_filters_for_size(filters_section, size=size)
            benchmark_cases.append(
                (
                    size,
                    build_cross_pattern(size),
                    size_filters["cross"],
                    size_filters["x"],
                ),
            )
        except Exception as e:  # noqa: BLE001
            print(f"[성능 분석 제외] size_{size}: {e}")

    if benchmark_cases:
        benchmark_rows = build_benchmark_rows(benchmark_cases, repeats=10)
        print("\n--- 성능 분석 (3×3, 5×5, 13×13, 25×25) ---")
        print(format_benchmark_table(benchmark_rows))


def _format_pattern_lines(pattern: list[list[float]]) -> str:
    return "\n".join(" ".join(str(int(v)) for v in row) for row in pattern)


def run_pattern_generator_mode(
    reader: Callable[[str], str] | None = None,
) -> None:
    """크기 N 입력으로 Cross/X 패턴을 생성해 출력한다."""
    read = reader or input
    try:
        raw = read("\n생성할 패턴 크기 N(3 이상)을 입력하세요: ").strip()
        size = int(raw)
        validate_size(size)
    except ValueError:
        print("입력 형식 오류: 3 이상의 정수를 입력하세요.")
        return
    except KeyboardInterrupt:
        print("\n\n입력이 중단되어 메인 메뉴로 돌아갑니다.")
        return
    except EOFError:
        print("\n입력이 중단되어 메인 메뉴로 돌아갑니다.")
        return

    cross = generate_cross_pattern(size)
    x_pattern = generate_x_pattern(size)

    print(f"\n--- 생성 결과 ({size}x{size}) ---")
    print("[Cross]")
    print(_format_pattern_lines(cross))
    print("\n[X]")
    print(_format_pattern_lines(x_pattern))


def main() -> None:
    run_main_menu()
