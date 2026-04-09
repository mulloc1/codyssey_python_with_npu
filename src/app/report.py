"""결과 요약/리포트 포맷 유틸."""

from __future__ import annotations


def summarize_results(
    total: int,
    passed: int,
    failed: int,
    failures_detail: list[tuple[str, str]],
) -> str:
    """JSON 모드 최종 요약 문자열을 반환한다."""
    lines = [
        "--- data.json 결과 요약 ---",
        f"전체 테스트 수: {total}",
        f"통과 수: {passed}",
        f"실패 수: {failed}",
    ]
    if failures_detail:
        lines.append("실패 케이스:")
        for key, reason in failures_detail:
            lines.append(f"  - {key}: {reason}")
    return "\n".join(lines)
