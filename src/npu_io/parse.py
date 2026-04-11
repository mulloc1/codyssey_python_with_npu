"""한 줄·다줄 행렬 파싱(콘솔 입력 검증용 순수 함수)."""

from __future__ import annotations

# subject.md 4-2 예시 문구
ROW_FORMAT_ERROR_3 = (
    "입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요."
)


def parse_row(sLine: str, iExpectedCount: int = 3) -> list[float]:
    """
    공백으로 구분된 숫자 한 줄을 파싱한다.

    예시:
        입력: "0 1 0"
        반환: [0.0, 1.0, 0.0]
        입력: "  -1.5   2   0 "
        반환: [-1.5, 2.0, 0.0]

    Raises:
        ValueError: 토큰 개수 불일치 또는 숫자 파싱 실패 시
    """
    lParts = sLine.strip().split()
    if len(lParts) != iExpectedCount:
        sMsg = ROW_FORMAT_ERROR_3 if iExpectedCount == 3 else _generic_row_error(iExpectedCount)
        raise ValueError(sMsg)

    try:
        return [float(sPart) for sPart in lParts]
    except ValueError as exc:
        sMsg = ROW_FORMAT_ERROR_3 if iExpectedCount == 3 else _generic_row_error(iExpectedCount)
        raise ValueError(sMsg) from exc


def _generic_row_error(iExpectedCount: int) -> str:
    return f"입력 형식 오류: 각 줄에 {iExpectedCount}개의 숫자를 공백으로 구분해 입력하세요."
