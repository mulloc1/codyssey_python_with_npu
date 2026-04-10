"""결과 요약/리포트 포맷 유틸."""

from __future__ import annotations


def summarize_results(
    iTotal: int,
    iPassed: int,
    iFailed: int,
    lFailuresDetail: list[tuple[str, str]],
) -> str:
    """JSON 모드 최종 요약 문자열을 반환한다."""
    lLines = [
        "--- data.json 결과 요약 ---",
        f"전체 테스트 수: {iTotal}",
        f"통과 수: {iPassed}",
        f"실패 수: {iFailed}",
    ]
    if lFailuresDetail:
        lLines.append("실패 케이스:")
        for sKey, sReason in lFailuresDetail:
            lLines.append(f"  - {sKey}: {sReason}")
    return "\n".join(lLines)
