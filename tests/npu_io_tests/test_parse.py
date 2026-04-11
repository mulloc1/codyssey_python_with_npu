"""npu_io.parse 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu_io.parse import ROW_FORMAT_ERROR_3, parse_row


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


class TestParseRowMatrixIdiom(unittest.TestCase):
    """다줄 행렬은 호출부에서 줄 수를 맞춘 뒤 행마다 parse_row를 쓴다."""

    def test_three_lines_via_parse_row(self) -> None:
        lLines = ["0 1 0", "1 1 1", "0 1 0"]
        lMatrix = [parse_row(sLine, iExpectedCount=3) for sLine in lLines]
        self.assertEqual(len(lMatrix), 3)
        self.assertEqual(lMatrix[0], [0.0, 1.0, 0.0])


if __name__ == "__main__":
    unittest.main()
