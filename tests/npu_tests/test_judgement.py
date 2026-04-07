"""npu.judgement 단위 테스트."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from npu.constants import LABEL_CROSS, LABEL_UNDECIDED, LABEL_X  # noqa: E402
from npu.judgement import judge_cross_vs_x  # noqa: E402


class TestJudgeCrossVsX(unittest.TestCase):
    # 점수 차이가 epsilon보다 작으면 UNDECIDED여야 한다.
    def test_returns_undecided_when_diff_is_less_than_epsilon(self) -> None:
        self.assertEqual(
            judge_cross_vs_x(1.0, 1.0 + 1e-10, epsilon=1e-9),
            LABEL_UNDECIDED,
        )

    # Cross 점수가 더 크면 Cross 라벨을 반환해야 한다.
    def test_returns_cross_when_cross_score_is_higher(self) -> None:
        self.assertEqual(judge_cross_vs_x(5.0, 1.0, epsilon=1e-9), LABEL_CROSS)

    # X 점수가 더 크면 X 라벨을 반환해야 한다.
    def test_returns_x_when_x_score_is_higher(self) -> None:
        self.assertEqual(judge_cross_vs_x(1.0, 5.0, epsilon=1e-9), LABEL_X)

    # 경계값(|diff| == epsilon)은 동점이 아니라 큰 쪽으로 판정해야 한다.
    def test_boundary_equal_to_epsilon_is_not_undecided(self) -> None:
        self.assertEqual(judge_cross_vs_x(1.0, 1.0 + 1e-9, epsilon=1e-9), LABEL_X)

    # epsilon이 0 이하면 정책 위반으로 예외가 발생해야 한다.
    def test_raises_when_epsilon_is_zero_or_negative(self) -> None:
        with self.assertRaises(ValueError):
            judge_cross_vs_x(1.0, 1.0, epsilon=0.0)
        with self.assertRaises(ValueError):
            judge_cross_vs_x(1.0, 1.0, epsilon=-1e-9)


if __name__ == "__main__":
    unittest.main()
