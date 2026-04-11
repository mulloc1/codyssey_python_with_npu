"""2차원 배열(그리드) 형상 검증 유틸."""

from __future__ import annotations

from typing import Any


def validate_matrix(lMatrix: list[list[int]], iExpectedSize: int | None = None) -> int:
    """
    유효한 N×N 정사각형인지 검증하고 N을 반환한다.

    - 최소 1행 이상
    - 모든 행이 리스트이며 길이가 행 개수(N)와 같음
    - expected_size가 주어지면 N이 expected_size와 같아야 함

    Raises:
        ValueError: 형상이 올바르지 않거나, expected_size와 크기가 다를 때
        TypeError: expected_size가 int가 아닐 때
    """
    if not isinstance(lMatrix, list):
        raise ValueError("matrix must be a list of rows")

    iSize = len(lMatrix)
    if iSize == 0:
        raise ValueError("matrix must not be empty")

    for iRow, lRow in enumerate(lMatrix):
        if not isinstance(lRow, list):
            raise ValueError(f"row {iRow} must be a list")
        if len(lRow) != iSize:
            raise ValueError(
                "matrix must be square: each row length must equal the number of rows"
            )

    if iExpectedSize is not None:
        if not isinstance(iExpectedSize, int):
            raise TypeError("expected_size must be an int")
        if iExpectedSize < 1:
            raise ValueError("expected_size must be at least 1")
        if iSize != iExpectedSize:
            raise ValueError(f"expected {iExpectedSize}x{iExpectedSize} matrix, got {iSize}x{iSize}")

    return iSize
