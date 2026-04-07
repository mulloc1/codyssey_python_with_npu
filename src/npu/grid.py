"""2차원 배열(그리드) 형상 검증 유틸."""

from __future__ import annotations

from typing import Any, Sequence


def validate_matrix(matrix: Any, expected_size: int | None = None) -> int:
    """
    유효한 N×N 정사각형인지 검증하고 N을 반환한다.

    - 최소 1행 이상
    - 모든 행이 리스트이며 길이가 행 개수(N)와 같음
    - expected_size가 주어지면 N이 expected_size와 같아야 함

    Raises:
        ValueError: 형상이 올바르지 않거나, expected_size와 크기가 다를 때
        TypeError: expected_size가 int가 아닐 때
    """
    if not isinstance(matrix, list):
        raise ValueError("matrix must be a list of rows")

    n = len(matrix)
    if n == 0:
        raise ValueError("matrix must not be empty")

    for i, row in enumerate(matrix):
        if not isinstance(row, list):
            raise ValueError(f"row {i} must be a list")
        if len(row) != n:
            raise ValueError(
                "matrix must be square: each row length must equal the number of rows"
            )

    if expected_size is not None:
        if not isinstance(expected_size, int):
            raise TypeError("expected_size must be an int")
        if expected_size < 1:
            raise ValueError("expected_size must be at least 1")
        if n != expected_size:
            raise ValueError(f"expected {expected_size}x{expected_size} matrix, got {n}x{n}")

    return n


def same_shape(a: Sequence[Any], b: Sequence[Any]) -> bool:
    """두 그리드가 동일한 N×N 형상이면 True."""
    try:
        a_size = validate_matrix(a)
        b_size = validate_matrix(b)
    except ValueError:
        return False
    except TypeError:
        return False
    return a_size == b_size
