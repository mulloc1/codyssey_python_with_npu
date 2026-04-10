"""app.report 단위 테스트."""

from __future__ import annotations

import unittest

from src.app.report import summarize_results


class TestSummarizeResults(unittest.TestCase):
    def test_formats_counts(self) -> None:
        sText = summarize_results(
            iTotal=8,
            iPassed=7,
            iFailed=1,
            lFailuresDetail=[],
        )
        self.assertIn("전체 테스트 수: 8", sText)
        self.assertIn("통과 수: 7", sText)
        self.assertIn("실패 수: 1", sText)

    def test_formats_failure_details(self) -> None:
        sText = summarize_results(
            iTotal=3,
            iPassed=2,
            iFailed=1,
            lFailuresDetail=[("size_5_099", "expected 5x5 matrix, got 4x4")],
        )
        self.assertIn("실패 케이스:", sText)
        self.assertIn("size_5_099: expected 5x5 matrix, got 4x4", sText)

    def test_omits_failure_section_when_no_failures(self) -> None:
        sText = summarize_results(
            iTotal=2,
            iPassed=2,
            iFailed=0,
            lFailuresDetail=[],
        )
        self.assertNotIn("실패 케이스:", sText)


if __name__ == "__main__":
    unittest.main()
