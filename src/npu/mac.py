"""MAC(Multiply-Accumulate) 연산 코어."""

from __future__ import annotations

from typing import Any

from src.npu.grid import validate_matrix


def validate_mac_inputs(lPattern: Any, lFilter: Any) -> int:
    """MAC 입력을 검증하고 공통 한 변 크기를 반환한다."""
    iPatternSize = validate_matrix(lPattern)
    iFilterSize = validate_matrix(lFilter)
    if iPatternSize != iFilterSize:
        raise ValueError("pattern and filter must have the same shape")
    return iPatternSize


def compute_mac(lPattern: Any, lFilter: Any, iSize: int) -> float:
    """
    검증된 pattern/filter의 위치별 곱을 누적한 MAC 점수를 반환한다.

    이 함수는 입력 검증을 수행하지 않는다.
    호출 전 validate_mac_inputs로 shape/type 검증을 완료해야 한다.
    """
    fAcc = 0.0
    for iRow in range(iSize):
        for iCol in range(iSize):
            fAcc += lPattern[iRow][iCol] * lFilter[iRow][iCol]
    return float(fAcc)
