"""npu.judgement 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu.constants import LABEL_CROSS, LABEL_UNDECIDED, LABEL_X
from src.npu.judgement import judge


class TestJudgeCrossVsX(unittest.TestCase):
    def test_returns_undecided_when_diff_is_less_than_epsilon(self) -> None:
        self.assertEqual(
            judge(1.0, 1.0 + 1e-10, LABEL_CROSS, LABEL_X, fEpsilon=1e-9),
            LABEL_UNDECIDED,
        )

    def test_returns_cross_when_cross_score_is_higher(self) -> None:
        self.assertEqual(judge(5.0, 1.0, LABEL_CROSS, LABEL_X, fEpsilon=1e-9), LABEL_CROSS)

    def test_returns_x_when_x_score_is_higher(self) -> None:
        self.assertEqual(judge(1.0, 5.0, LABEL_CROSS, LABEL_X, fEpsilon=1e-9), LABEL_X)

    def test_boundary_equal_to_epsilon_is_not_undecided(self) -> None:
        self.assertEqual(judge(1.0, 1.0 + 1e-9, LABEL_CROSS, LABEL_X, fEpsilon=1e-9), LABEL_X)

    def test_raises_when_epsilon_is_zero_or_negative(self) -> None:
        with self.assertRaises(ValueError):
            judge(1.0, 1.0, LABEL_CROSS, LABEL_X, fEpsilon=0.0)
        with self.assertRaises(ValueError):
            judge(1.0, 1.0, LABEL_CROSS, LABEL_X, fEpsilon=-1e-9)


class TestJudgeAb(unittest.TestCase):
    def test_returns_a_when_score_a_is_higher(self) -> None:
        self.assertEqual(judge(5.0, 1.0, "A", "B", fEpsilon=1e-9), "A")

    def test_returns_b_when_score_b_is_higher(self) -> None:
        self.assertEqual(judge(1.0, 5.0, "A", "B", fEpsilon=1e-9), "B")

    def test_returns_undecided_when_within_epsilon(self) -> None:
        self.assertEqual(judge(1.0, 1.0 + 1e-10, "A", "B", fEpsilon=1e-9), LABEL_UNDECIDED)


if __name__ == "__main__":
    unittest.main()
