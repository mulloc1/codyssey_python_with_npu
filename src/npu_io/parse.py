"""한 줄·다줄 행렬 파싱(콘솔 입력 검증용 순수 함수)."""

from __future__ import annotations

# subject.md 4-2 예시 문구
ROW_FORMAT_ERROR_3 = (
    "입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요."
)


def parse_row(line: str, expected_count: int = 3) -> list[float]:
    """
    공백으로 구분된 숫자 한 줄을 파싱한다.

    Raises:
        ValueError: 토큰 개수 불일치 또는 숫자 파싱 실패 시
    """
    parts = line.strip().split()
    if len(parts) != expected_count:
        msg = ROW_FORMAT_ERROR_3 if expected_count == 3 else _generic_row_error(expected_count)
        raise ValueError(msg)

    try:
        return [float(p) for p in parts]
    except ValueError as e:
        msg = ROW_FORMAT_ERROR_3 if expected_count == 3 else _generic_row_error(expected_count)
        raise ValueError(msg) from e


def _generic_row_error(expected_count: int) -> str:
    return f"입력 형식 오류: 각 줄에 {expected_count}개의 숫자를 공백으로 구분해 입력하세요."


def read_square_matrix_lines(lines: list[str], size: int = 3) -> list[list[float]]:
    """
    정확히 size줄의 문자열을 정사각 행렬로 파싱한다.

    Raises:
        ValueError: 줄 개수 불일치 또는 행 파싱 실패
    """
    if len(lines) != size:
        raise ValueError(
            f"입력 형식 오류: {size}줄이 필요합니다. (현재 {len(lines)}줄)"
        )
    return [parse_row(line, expected_count=size) for line in lines]
