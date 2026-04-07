"""MAC(Multiply-Accumulate) 연산 코어."""

from __future__ import annotations

from typing import Any

from npu.grid import validate_matrix


def compute_mac(pattern: Any, filter_: Any) -> float:
    """
    pattern과 filter_의 위치별 곱을 누적한 MAC 점수를 반환한다.

    Raises:
        ValueError: pattern/filter_ 형상이 유효하지 않거나 크기가 다를 때
        TypeError: validate_matrix의 타입 제약을 위반할 때
    """
    pattern_size = validate_matrix(pattern)
    filter_size = validate_matrix(filter_)

    if pattern_size != filter_size:
        raise ValueError("pattern and filter must have the same shape")

    acc = 0.0
    for i in range(pattern_size):
        for j in range(pattern_size):
            acc += pattern[i][j] * filter_[i][j]
    return float(acc)
