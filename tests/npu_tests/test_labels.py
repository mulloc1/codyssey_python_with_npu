"""npu.labels 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu.constants import LABEL_CROSS, LABEL_X
from src.npu.labels import normalize_filter_score_keys, normalize_label


class TestNormalizeLabel(unittest.TestCase):
    def test_maps_plus_to_cross(self) -> None:
        self.assertEqual(normalize_label("+"), LABEL_CROSS)

    def test_maps_x_to_x(self) -> None:
        self.assertEqual(normalize_label("x"), LABEL_X)

    def test_maps_uppercase_x_and_whitespace(self) -> None:
        self.assertEqual(normalize_label("X"), LABEL_X)
        self.assertEqual(normalize_label("  x  "), LABEL_X)

    def test_maps_cross_aliases_case_insensitive(self) -> None:
        self.assertEqual(normalize_label("cross"), LABEL_CROSS)
        self.assertEqual(normalize_label("CROSS"), LABEL_CROSS)
        self.assertEqual(normalize_label("  CrOsS  "), LABEL_CROSS)

    def test_accepts_already_standard_labels(self) -> None:
        self.assertEqual(normalize_label(LABEL_CROSS), LABEL_CROSS)
        self.assertEqual(normalize_label(LABEL_X), LABEL_X)

    def test_raises_for_unsupported_value(self) -> None:
        with self.assertRaises(ValueError):
            normalize_label("triangle")


class TestNormalizeFilterScoreKeys(unittest.TestCase):
    def test_normalizes_score_map_keys_to_standard_labels(self) -> None:
        dNormalized = normalize_filter_score_keys({"cross": 5.0, "x": 1.0})
        self.assertEqual(dNormalized, {LABEL_CROSS: 5.0, LABEL_X: 1.0})

    def test_raises_when_normalized_keys_collide(self) -> None:
        with self.assertRaises(ValueError):
            normalize_filter_score_keys({"cross": 5.0, LABEL_CROSS: 4.0})


if __name__ == "__main__":
    unittest.main()
