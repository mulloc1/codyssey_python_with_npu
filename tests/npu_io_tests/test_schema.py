"""npu_io.schema 단위 테스트."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from npu_io.schema import (  # noqa: E402
    extract_size_from_pattern_key,
    select_filters_for_size,
    validate_pattern_and_filters,
)


def _cross(n: int) -> list[list[float]]:
    c = n // 2
    return [[1.0 if (i == c or j == c) else 0.0 for j in range(n)] for i in range(n)]


class TestExtractSizeFromPatternKey(unittest.TestCase):
    def test_extracts_size_from_valid_key(self) -> None:
        self.assertEqual(extract_size_from_pattern_key("size_13_002"), 13)

    def test_raises_for_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            extract_size_from_pattern_key("pattern_13_002")


class TestSelectFiltersForSize(unittest.TestCase):
    def test_selects_filters_by_size(self) -> None:
        filters = {"size_5": {"cross": _cross(5), "x": _cross(5)}}
        selected = select_filters_for_size(filters, 5)
        self.assertIn("cross", selected)
        self.assertIn("x", selected)

    def test_raises_when_size_key_missing(self) -> None:
        with self.assertRaises(ValueError):
            select_filters_for_size({"size_13": {}}, 5)


class TestValidatePatternAndFilters(unittest.TestCase):
    def test_accepts_valid_shapes(self) -> None:
        pattern = _cross(5)
        filters = {"Cross": _cross(5), "X": _cross(5)}
        validate_pattern_and_filters(pattern, filters, expected_size=5)

    def test_raises_on_shape_mismatch(self) -> None:
        pattern = _cross(5)
        bad_filter = [[1.0, 0.0], [0.0, 1.0]]
        filters = {"Cross": _cross(5), "X": bad_filter}
        with self.assertRaises(ValueError):
            validate_pattern_and_filters(pattern, filters, expected_size=5)


if __name__ == "__main__":
    unittest.main()
