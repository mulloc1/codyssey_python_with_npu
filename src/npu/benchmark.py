"""MAC 성능 측정(분할 A/B + 총합) 유틸."""

from __future__ import annotations

import time
from typing import Any

from src.npu.mac import compute_mac


def benchmark_mac_once(pattern: Any, filter_: Any) -> float:
    """MAC 1회 실행 시간을 ms 단위로 반환한다."""
    t0 = time.perf_counter()
    compute_mac(pattern, filter_)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0


def benchmark_mac_average(pattern: Any, filter_: Any, repeats: int = 10) -> float:
    """MAC 반복 실행 평균 시간을 ms 단위로 반환한다."""
    if repeats <= 0:
        raise ValueError("repeats must be greater than 0")
    total_ms = 0.0
    for _ in range(repeats):
        total_ms += benchmark_mac_once(pattern, filter_)
    return total_ms / repeats


def benchmark_pair(
    pattern: Any,
    filter_a: Any,
    filter_b: Any,
    repeats: int = 10,
) -> dict[str, float | int]:
    """
    동일 패턴에 대한 A/B 분할 평균과 총합 평균을 반환한다.

    반환 키:
    - size
    - avg_a_ms
    - avg_b_ms
    - avg_total_ms
    - ops_n2
    """
    size = len(pattern)
    avg_a_ms = benchmark_mac_average(pattern, filter_a, repeats=repeats)
    avg_b_ms = benchmark_mac_average(pattern, filter_b, repeats=repeats)
    return {
        "size": size,
        "avg_a_ms": avg_a_ms,
        "avg_b_ms": avg_b_ms,
        "avg_total_ms": avg_a_ms + avg_b_ms,
        "ops_n2": size * size,
    }


def build_benchmark_rows(
    cases: list[tuple[int, Any, Any, Any]],
    repeats: int = 10,
) -> list[dict[str, float | int]]:
    """(size, pattern, filter_a, filter_b) 목록을 성능 행 목록으로 변환한다."""
    rows: list[dict[str, float | int]] = []
    for size, pattern, filter_a, filter_b in cases:
        row = benchmark_pair(pattern, filter_a, filter_b, repeats=repeats)
        row["size"] = size
        rows.append(row)
    return rows


def format_benchmark_table(rows: list[dict[str, float | int]]) -> str:
    """성능 행 목록을 콘솔 표 문자열로 변환한다."""
    header = "크기(N×N) | A 평균(ms) | B 평균(ms) | 합계 평균(ms) | 연산 횟수(N²)"
    sep = "-" * len(header)
    lines = [header, sep]
    for row in rows:
        size = int(row["size"])
        avg_a = float(row["avg_a_ms"])
        avg_b = float(row["avg_b_ms"])
        avg_total = float(row["avg_total_ms"])
        ops_n2 = int(row["ops_n2"])
        lines.append(
            f"{size}x{size} | {avg_a:.6f} | {avg_b:.6f} | {avg_total:.6f} | {ops_n2}",
        )
    return "\n".join(lines)


def build_cross_pattern(size: int) -> list[list[float]]:
    """Cross 패턴 생성."""
    c = size // 2
    return [
        [1.0 if (i == c or j == c) else 0.0 for j in range(size)]
        for i in range(size)
    ]


def build_x_pattern(size: int) -> list[list[float]]:
    """X 패턴 생성."""
    return [
        [1.0 if (i == j or i + j == size - 1) else 0.0 for j in range(size)]
        for i in range(size)
    ]
