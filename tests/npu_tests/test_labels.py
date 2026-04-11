"""npu.labels 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu.constants import LABEL_CROSS, LABEL_X
from src.npu.labels import normalize_expected, normalize_filter_key


class TestNormalizeExpected(unittest.TestCase):
    def test_maps_plus_to_cross(self) -> None:
        self.assertEqual(normalize_expected("+"), LABEL_CROSS)

    def test_maps_x_to_x(self) -> None:
        self.assertEqual(normalize_expected("x"), LABEL_X)

    def test_maps_uppercase_x_and_whitespace(self) -> None:
        self.assertEqual(normalize_expected("X"), LABEL_X)
        self.assertEqual(normalize_expected("  x  "), LABEL_X)

    def test_maps_cross_aliases_case_insensitive(self) -> None:
        self.assertEqual(normalize_expected("cross"), LABEL_CROSS)
        self.assertEqual(normalize_expected("CROSS"), LABEL_CROSS)
        self.assertEqual(normalize_expected("  CrOsS  "), LABEL_CROSS)

    def test_accepts_already_standard_labels(self) -> None:
        self.assertEqual(normalize_expected(LABEL_CROSS), LABEL_CROSS)
        self.assertEqual(normalize_expected(LABEL_X), LABEL_X)

    def test_raises_for_unsupported_value(self) -> None:
        with self.assertRaises(ValueError):
            normalize_expected("triangle")


class TestNormalizeFilterKey(unittest.TestCase):
    def test_maps_cross_to_cross(self) -> None:
        self.assertEqual(normalize_filter_key("cross"), LABEL_CROSS)

    def test_maps_x_to_x(self) -> None:
        self.assertEqual(normalize_filter_key("x"), LABEL_X)

    def test_maps_cross_uppercase_and_whitespace(self) -> None:
        self.assertEqual(normalize_filter_key("CROSS"), LABEL_CROSS)
        self.assertEqual(normalize_filter_key(" X "), LABEL_X)

    def test_accepts_already_standard_labels(self) -> None:
        self.assertEqual(normalize_filter_key(LABEL_CROSS), LABEL_CROSS)
        self.assertEqual(normalize_filter_key(LABEL_X), LABEL_X)

    def test_raises_for_unsupported_value(self) -> None:
        with self.assertRaises(ValueError):
            normalize_filter_key("plus")


if __name__ == "__main__":
    unittest.main()
