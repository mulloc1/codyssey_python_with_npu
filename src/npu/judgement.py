"""점수 비교/판정 정책."""

from __future__ import annotations

from npu.constants import DEFAULT_EPSILON, LABEL_CROSS, LABEL_UNDECIDED, LABEL_X


def judge_cross_vs_x(
    score_cross: int | float,
    score_x: int | float,
    epsilon: float = DEFAULT_EPSILON,
) -> str:
    """
    Cross/X 점수를 비교해 표준 라벨(Cross, X, UNDECIDED) 중 하나를 반환한다.

    동점 규칙:
    - abs(score_cross - score_x) < epsilon 이면 UNDECIDED
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be greater than 0")

    if abs(score_cross - score_x) < epsilon:
        return LABEL_UNDECIDED
    if score_cross > score_x:
        return LABEL_CROSS
    return LABEL_X
