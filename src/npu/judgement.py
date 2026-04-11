"""점수 비교/판정 정책."""

from __future__ import annotations

from src.npu.constants import DEFAULT_EPSILON, LABEL_UNDECIDED


def judge(
    fScoreFirst: int | float,
    fScoreSecond: int | float,
    sLabelFirst: str,
    sLabelSecond: str,
    fEpsilon: float = DEFAULT_EPSILON,
) -> str:
    """
    두 점수를 비교해 sLabelFirst, sLabelSecond, UNDECIDED 중 하나를 반환한다.

    동점 규칙:
    - abs(first - second) < epsilon 이면 UNDECIDED
    """
    if fEpsilon <= 0:
        raise ValueError("epsilon must be greater than 0")
    if abs(fScoreFirst - fScoreSecond) < fEpsilon:
        return LABEL_UNDECIDED
    if fScoreFirst > fScoreSecond:
        return sLabelFirst
    return sLabelSecond
