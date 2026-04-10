"""npu_io.schema 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu_io.schema import (
    extract_size_from_pattern_key,
    select_filters_for_size,
    validate_pattern_and_filters,
)


def _cross(iSize: int) -> list[list[float]]:
    iCenter = iSize // 2
    return [[1.0 if (i == iCenter or j == iCenter) else 0.0 for j in range(iSize)] for i in range(iSize)]


class TestExtractSizeFromPatternKey(unittest.TestCase):
    def test_extracts_size_from_valid_key(self) -> None:
        self.assertEqual(extract_size_from_pattern_key("size_13_002"), 13)

    def test_raises_for_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            extract_size_from_pattern_key("pattern_13_002")


class TestSelectFiltersForSize(unittest.TestCase):
    def test_selects_filters_by_size(self) -> None:
        dFilters = {"size_5": {"cross": _cross(5), "x": _cross(5)}}
        dSelected = select_filters_for_size(dFilters, 5)
        self.assertIn("cross", dSelected)
        self.assertIn("x", dSelected)

    def test_raises_when_size_key_missing(self) -> None:
        with self.assertRaises(ValueError):
            select_filters_for_size({"size_13": {}}, 5)


class TestValidatePatternAndFilters(unittest.TestCase):
    def test_accepts_valid_shapes(self) -> None:
        lPattern = _cross(5)
        dFilters = {"Cross": _cross(5), "X": _cross(5)}
        validate_pattern_and_filters(lPattern, dFilters, iExpectedSize=5)

    def test_raises_on_shape_mismatch(self) -> None:
        lPattern = _cross(5)
        lBadFilter = [[1.0, 0.0], [0.0, 1.0]]
        dFilters = {"Cross": _cross(5), "X": lBadFilter}
        with self.assertRaises(ValueError):
            validate_pattern_and_filters(lPattern, dFilters, iExpectedSize=5)


if __name__ == "__main__":
    unittest.main()
