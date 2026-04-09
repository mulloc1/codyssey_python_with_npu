"""npu_io.json_loader 단위 테스트."""

from __future__ import annotations

import json
import tempfile
import unittest

from src.npu_io.json_loader import iter_pattern_cases, load_json


class TestLoadJson(unittest.TestCase):
    def test_loads_valid_json_object(self) -> None:
        payload = {"filters": {}, "patterns": {}}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump(payload, tf)
            path = tf.name
        loaded = load_json(path)
        self.assertEqual(loaded, payload)

    def test_raises_when_json_root_is_not_object(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump([1, 2, 3], tf)
            path = tf.name
        with self.assertRaises(ValueError):
            load_json(path)


class TestIterPatternCases(unittest.TestCase):
    def test_returns_key_case_list(self) -> None:
        data = {
            "patterns": {
                "size_5_001": {"input": [[0]], "expected": "+"},
                "size_5_002": {"input": [[1]], "expected": "x"},
            },
        }
        cases = iter_pattern_cases(data)
        self.assertEqual(len(cases), 2)
        self.assertEqual(cases[0][0], "size_5_001")

    def test_raises_when_patterns_section_missing(self) -> None:
        with self.assertRaises(ValueError):
            iter_pattern_cases({})


if __name__ == "__main__":
    unittest.main()
