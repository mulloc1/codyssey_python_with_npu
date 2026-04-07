"""npu.mac 단위 테스트."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from npu.mac import compute_mac  # noqa: E402


class TestComputeMac(unittest.TestCase):
    def test_subject_example_cross_cross_scores_five(self) -> None:
        cross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        self.assertEqual(compute_mac(cross, cross), 5.0)

    def test_subject_example_cross_x_scores_one(self) -> None:
        cross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        x_filter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        self.assertEqual(compute_mac(cross, x_filter), 1.0)

    def test_cross_filter_score_higher_than_x_filter(self) -> None:
        cross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        x_filter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        score_cross = compute_mac(cross, cross)
        score_x = compute_mac(cross, x_filter)
        self.assertGreater(score_cross, score_x)

    def test_float_inputs_are_accumulated_correctly(self) -> None:
        pattern = [
            [0.1, 0.2],
            [0.3, 0.4],
        ]
        filt = [
            [1.5, -1.0],
            [0.5, 2.0],
        ]
        # 0.1*1.5 + 0.2*(-1.0) + 0.3*0.5 + 0.4*2.0 = 0.9
        self.assertAlmostEqual(compute_mac(pattern, filt), 0.9, places=12)

    def test_raises_on_shape_mismatch(self) -> None:
        pattern = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        filt = [
            [1, 0],
            [0, 1],
        ]
        with self.assertRaises(ValueError) as ctx:
            compute_mac(pattern, filt)
        self.assertIn("same shape", str(ctx.exception))

    def test_raises_on_invalid_ragged_matrix(self) -> None:
        pattern = [
            [1, 0, 1],
            [0, 1],
            [1, 0, 1],
        ]
        filt = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        with self.assertRaises(ValueError):
            compute_mac(pattern, filt)


if __name__ == "__main__":
    unittest.main()
