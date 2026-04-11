"""npu.mac 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu.mac import compute_mac, validate_mac_inputs


def _mac(lPattern: list, lFilter: list) -> float:
    """테스트 헬퍼: 검증 후 MAC 계산."""
    iSize = validate_mac_inputs(lPattern, lFilter)
    return compute_mac(lPattern, lFilter, iSize)


class TestComputeMac(unittest.TestCase):
    def test_subject_example_cross_cross_scores_five(self) -> None:
        lCross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        self.assertEqual(_mac(lCross, lCross), 5.0)

    def test_subject_example_cross_x_scores_one(self) -> None:
        lCross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        lXFilter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        self.assertEqual(_mac(lCross, lXFilter), 1.0)

    def test_cross_filter_score_higher_than_x_filter(self) -> None:
        lCross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        lXFilter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        fScoreCross = _mac(lCross, lCross)
        fScoreX = _mac(lCross, lXFilter)
        self.assertGreater(fScoreCross, fScoreX)

    def test_float_inputs_are_accumulated_correctly(self) -> None:
        lPattern = [
            [0.1, 0.2],
            [0.3, 0.4],
        ]
        lFilter = [
            [1.5, -1.0],
            [0.5, 2.0],
        ]
        self.assertAlmostEqual(_mac(lPattern, lFilter), 0.9, places=12)

    def test_raises_on_shape_mismatch(self) -> None:
        lPattern = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        lFilter = [
            [1, 0],
            [0, 1],
        ]
        with self.assertRaises(ValueError) as oCtx:
            _mac(lPattern, lFilter)
        self.assertIn("same shape", str(oCtx.exception))

    def test_raises_on_invalid_ragged_matrix(self) -> None:
        lPattern = [
            [1, 0, 1],
            [0, 1],
            [1, 0, 1],
        ]
        lFilter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        with self.assertRaises(ValueError):
            _mac(lPattern, lFilter)


if __name__ == "__main__":
    unittest.main()
