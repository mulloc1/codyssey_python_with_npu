"""MAC 성능 측정(분할 A/B + 총합) 유틸."""

from __future__ import annotations

import time
from typing import Any

from src.npu.mac import compute_mac


def benchmark_mac_once(lPattern: Any, lFilter: Any) -> float:
    """MAC 1회 실행 시간을 ms 단위로 반환한다."""
    fStart = time.perf_counter()
    compute_mac(lPattern, lFilter)
    fEnd = time.perf_counter()
    return (fEnd - fStart) * 1000.0


def benchmark_mac_average(lPattern: Any, lFilter: Any, iRepeats: int = 10) -> float:
    """MAC 반복 실행 평균 시간을 ms 단위로 반환한다."""
    if iRepeats <= 0:
        raise ValueError("repeats must be greater than 0")
    fTotalMs = 0.0
    for _ in range(iRepeats):
        fTotalMs += benchmark_mac_once(lPattern, lFilter)
    return fTotalMs / iRepeats


def benchmark_pair(
    lPattern: Any,
    lFilterA: Any,
    lFilterB: Any,
    iRepeats: int = 10,
) -> dict[str, float | int]:
    """
    동일 패턴에 대한 A/B 분할 평균과 총합 평균을 반환한다.

    반환 키:
    - size
    - avg_a_ms
    - avg_b_ms
    - avg_total_ms
    - ops_n2
    """
    iSize = len(lPattern)
    fAvgAMs = benchmark_mac_average(lPattern, lFilterA, iRepeats=iRepeats)
    fAvgBMs = benchmark_mac_average(lPattern, lFilterB, iRepeats=iRepeats)
    return {
        "size": iSize,
        "avg_a_ms": fAvgAMs,
        "avg_b_ms": fAvgBMs,
        "avg_total_ms": fAvgAMs + fAvgBMs,
        "ops_n2": iSize * iSize,
    }


def build_benchmark_rows(
    lCases: list[tuple[int, Any, Any, Any]],
    iRepeats: int = 10,
) -> list[dict[str, float | int]]:
    """(size, pattern, filter_a, filter_b) 목록을 성능 행 목록으로 변환한다."""
    lRows: list[dict[str, float | int]] = []
    for iSize, lPattern, lFilterA, lFilterB in lCases:
        dRow = benchmark_pair(lPattern, lFilterA, lFilterB, iRepeats=iRepeats)
        dRow["size"] = iSize
        lRows.append(dRow)
    return lRows


def format_benchmark_table(lRows: list[dict[str, float | int]]) -> str:
    """성능 행 목록을 콘솔 표 문자열로 변환한다."""
    lColumns = ("크기(N×N)", "A 평균(ms)", "B 평균(ms)", "합계 평균(ms)", "연산 횟수(N²)")
    sRowLeftPad = " "
    lWidths = [8, 10, 10, 12, 11]
    lFormattedRows: list[tuple[str, str, str, str, str]] = []
    for dRow in lRows:
        iSize = int(dRow["size"])
        fAvgA = float(dRow["avg_a_ms"])
        fAvgB = float(dRow["avg_b_ms"])
        fAvgTotal = float(dRow["avg_total_ms"])
        iOpsN2 = int(dRow["ops_n2"])
        lFormattedRows.append(
            (
                f"{iSize}x{iSize}",
                f"{fAvgA:.6f}",
                f"{fAvgB:.6f}",
                f"{fAvgTotal:.6f}",
                str(iOpsN2),
            ),
        )

    for iIdx, sColumn in enumerate(lColumns):
        lWidths[iIdx] = max(lWidths[iIdx], len(sColumn))
    for tRow in lFormattedRows:
        for iIdx, sValue in enumerate(tRow):
            lWidths[iIdx] = max(lWidths[iIdx], len(sValue))

    sHeader = " | ".join(lColumns)
    sSeparator = "-" * (len(sHeader) + 14)
    lLines = [sHeader, sSeparator]
    for sSize, sAvgA, sAvgB, sAvgTotal, sOpsN2 in lFormattedRows:
        lLines.append(
            sRowLeftPad
            + " | ".join(
                [
                    sSize.ljust(lWidths[0]),
                    sAvgA.rjust(lWidths[1]),
                    sAvgB.rjust(lWidths[2]),
                    sAvgTotal.rjust(lWidths[3]),
                    sOpsN2.rjust(lWidths[4]),
                ]
            )
        )
    return "\n".join(lLines)


def build_cross_pattern(iSize: int) -> list[list[float]]:
    """Cross 패턴 생성."""
    iCenter = iSize // 2
    return [
        [1.0 if (i == iCenter or j == iCenter) else 0.0 for j in range(iSize)]
        for i in range(iSize)
    ]


def build_x_pattern(iSize: int) -> list[list[float]]:
    """X 패턴 생성."""
    return [
        [1.0 if (i == j or i + j == iSize - 1) else 0.0 for j in range(iSize)]
        for i in range(iSize)
    ]
