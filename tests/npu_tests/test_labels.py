"""npu.labels 단위 테스트."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from npu.constants import LABEL_CROSS, LABEL_X  # noqa: E402
from npu.labels import normalize_expected, normalize_filter_key  # noqa: E402


class TestNormalizeExpected(unittest.TestCase):
    def test_maps_plus_to_cross(self) -> None:
        self.assertEqual(normalize_expected("+"), LABEL_CROSS)

    def test_maps_x_to_x(self) -> None:
        self.assertEqual(normalize_expected("x"), LABEL_X)

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

    def test_accepts_already_standard_labels(self) -> None:
        self.assertEqual(normalize_filter_key(LABEL_CROSS), LABEL_CROSS)
        self.assertEqual(normalize_filter_key(LABEL_X), LABEL_X)

    def test_raises_for_unsupported_value(self) -> None:
        with self.assertRaises(ValueError):
            normalize_filter_key("plus")


if __name__ == "__main__":
    unittest.main()
