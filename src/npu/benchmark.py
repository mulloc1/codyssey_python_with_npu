"""MAC 성능 측정(분할 A/B + 총합) 유틸."""

from __future__ import annotations

import time
from typing import Any

from src.npu.mac import compute_mac, validate_mac_inputs


def benchmark_mac_average(lPattern: Any, lFilter: Any, iRepeats: int = 10) -> float:
    """MAC 반복 실행 평균 시간을 ms 단위로 반환한다."""
    if iRepeats <= 0:
        raise ValueError("repeats must be greater than 0")

    iSize = validate_mac_inputs(lPattern, lFilter)
    fTotalMs = 0.0
    for _ in range(iRepeats):
        fStart = time.perf_counter()
        compute_mac(lPattern, lFilter, iSize)
        fEnd = time.perf_counter()
        fTotalMs += (fEnd - fStart) * 1000.0
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
    return [
        benchmark_pair(lPattern, lFilterA, lFilterB, iRepeats=iRepeats)
        for _, lPattern, lFilterA, lFilterB in lCases
    ]


def format_benchmark_table(lRows: list[dict[str, float | int]]) -> str:
    """성능 행 목록을 콘솔 표 문자열로 변환한다."""
    lColumns = ("크기(N×N)", "A 평균(ms)", "B 평균(ms)", "합계 평균(ms)", "연산 횟수(N²)")
    lFormattedRows = [
        (
            f"{int(d['size'])}x{int(d['size'])}",
            f"{d['avg_a_ms']:.6f}",
            f"{d['avg_b_ms']:.6f}",
            f"{d['avg_total_ms']:.6f}",
            str(int(d["ops_n2"])),
        )
        for d in lRows
    ]

    lAllRows = [lColumns, *lFormattedRows]
    lWidths = [max(len(row[i]) for row in lAllRows) for i in range(len(lColumns))]

    sHeader = " | ".join(lColumns)
    sSeparator = "-" * (len(sHeader) + 14)
    lLines = [sHeader, sSeparator]
    for tRow in lFormattedRows:
        lLines.append(
            " "
            + " | ".join(
                sVal.ljust(lWidths[i]) if i == 0 else sVal.rjust(lWidths[i])
                for i, sVal in enumerate(tRow)
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
