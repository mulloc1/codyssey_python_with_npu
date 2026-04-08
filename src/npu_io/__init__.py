"""입력 파싱 등 I/O 유틸(stdlib `io` 패키지명과 충돌 방지로 npu_io 사용)."""

from npu_io.parse import ROW_FORMAT_ERROR_3, parse_row, read_square_matrix_lines

__all__ = [
    "ROW_FORMAT_ERROR_3",
    "parse_row",
    "read_square_matrix_lines",
]
