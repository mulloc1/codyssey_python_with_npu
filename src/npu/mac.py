"""MAC(Multiply-Accumulate) 연산 코어."""

from __future__ import annotations

from typing import Any

from src.npu.grid import validate_matrix


def compute_mac(lPattern: Any, lFilter: Any) -> float:
    """
    pattern과 filter_의 위치별 곱을 누적한 MAC 점수를 반환한다.

    Raises:
        ValueError: pattern/filter_ 형상이 유효하지 않거나 크기가 다를 때
        TypeError: validate_matrix의 타입 제약을 위반할 때
    """
    iPatternSize = validate_matrix(lPattern)
    iFilterSize = validate_matrix(lFilter)

    if iPatternSize != iFilterSize:
        raise ValueError("pattern and filter must have the same shape")

    fAcc = 0.0
    for iRow in range(iPatternSize):
        for iCol in range(iPatternSize):
            fAcc += lPattern[iRow][iCol] * lFilter[iRow][iCol]
    return float(fAcc)
