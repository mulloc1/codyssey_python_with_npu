"""app.report 단위 테스트."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from app.report import summarize_results  # noqa: E402


class TestSummarizeResults(unittest.TestCase):
    def test_formats_counts(self) -> None:
        text = summarize_results(
            total=8,
            passed=7,
            failed=1,
            failures_detail=[],
        )
        self.assertIn("전체 테스트 수: 8", text)
        self.assertIn("통과 수: 7", text)
        self.assertIn("실패 수: 1", text)

    def test_formats_failure_details(self) -> None:
        text = summarize_results(
            total=3,
            passed=2,
            failed=1,
            failures_detail=[("size_5_099", "expected 5x5 matrix, got 4x4")],
        )
        self.assertIn("실패 케이스:", text)
        self.assertIn("size_5_099: expected 5x5 matrix, got 4x4", text)

    def test_omits_failure_section_when_no_failures(self) -> None:
        text = summarize_results(
            total=2,
            passed=2,
            failed=0,
            failures_detail=[],
        )
        self.assertNotIn("실패 케이스:", text)


if __name__ == "__main__":
    unittest.main()
