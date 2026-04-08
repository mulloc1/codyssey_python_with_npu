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


def judge_ab(
    score_a: int | float,
    score_b: int | float,
    epsilon: float = DEFAULT_EPSILON,
) -> str:
    """
    모드 1(사용자 입력)용: 필터 A/B 점수를 비교해 A, B, UNDECIDED 중 하나를 반환한다.

    동점 규칙은 judge_cross_vs_x와 동일(abs(diff) < epsilon).
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be greater than 0")

    if abs(score_a - score_b) < epsilon:
        return LABEL_UNDECIDED
    if score_a > score_b:
        return "A"
    return "B"
