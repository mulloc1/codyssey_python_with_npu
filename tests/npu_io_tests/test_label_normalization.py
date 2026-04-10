"""npu_io.label_normalization 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu.constants import LABEL_CROSS, LABEL_X
from src.npu_io.label_normalization import (
    normalize_expected_and_filter_key,
    normalize_filter_score_keys,
)


class TestNormalizeExpectedAndFilterKey(unittest.TestCase):
    def test_normalizes_expected_and_filter_key_for_json_case(self) -> None:
        sNormalizedExpected, sNormalizedFilter = normalize_expected_and_filter_key("+", "cross")
        self.assertEqual(sNormalizedExpected, LABEL_CROSS)
        self.assertEqual(sNormalizedFilter, LABEL_CROSS)


class TestNormalizeFilterScoreKeys(unittest.TestCase):
    def test_normalizes_score_map_keys_to_standard_labels(self) -> None:
        dNormalized = normalize_filter_score_keys({"cross": 5.0, "x": 1.0})
        self.assertEqual(dNormalized, {LABEL_CROSS: 5.0, LABEL_X: 1.0})

    def test_raises_when_normalized_keys_collide(self) -> None:
        with self.assertRaises(ValueError):
            normalize_filter_score_keys({"cross": 5.0, LABEL_CROSS: 4.0})


if __name__ == "__main__":
    unittest.main()
