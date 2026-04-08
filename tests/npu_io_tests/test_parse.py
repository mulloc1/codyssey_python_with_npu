"""npu_io.parse 단위 테스트."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from npu_io.parse import ROW_FORMAT_ERROR_3, parse_row, read_square_matrix_lines  # noqa: E402


class TestParseRow(unittest.TestCase):
    # 정상 한 줄은 3개 실수 리스트로 파싱되어야 한다.
    def test_parses_three_numbers(self) -> None:
        self.assertEqual(parse_row("1 0 1"), [1.0, 0.0, 1.0])

    # 연속 공백이 있어도 토큰은 3개로 인식되어야 한다.
    def test_handles_multiple_spaces(self) -> None:
        self.assertEqual(parse_row("  -1.5   2   0 "), [-1.5, 2.0, 0.0])

    # 토큰이 3개가 아니면 안내 문구 기준 ValueError여야 한다.
    def test_rejects_wrong_token_count(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_row("1 2")
        self.assertEqual(str(ctx.exception), ROW_FORMAT_ERROR_3)

    # 숫자가 아니면 파싱 실패로 동일 안내 메시지를 써야 한다.
    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_row("1 a 0")
        self.assertEqual(str(ctx.exception), ROW_FORMAT_ERROR_3)


class TestReadSquareMatrixLines(unittest.TestCase):
    # 3줄이면 정사각 행렬로 파싱되어야 한다.
    def test_reads_three_lines(self) -> None:
        lines = ["0 1 0", "1 1 1", "0 1 0"]
        m = read_square_matrix_lines(lines, size=3)
        self.assertEqual(len(m), 3)
        self.assertEqual(m[0], [0.0, 1.0, 0.0])

    # 줄 수가 size와 다르면 예외여야 한다.
    def test_rejects_wrong_line_count(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            read_square_matrix_lines(["0 1 0", "1 1 1"], size=3)
        self.assertIn("3줄이 필요", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
