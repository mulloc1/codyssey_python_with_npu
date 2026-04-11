"""npu.benchmark 단위 테스트."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from src.npu.benchmark import (
    benchmark_mac_average,
    benchmark_pair,
    format_benchmark_table,
)


def _cross_3() -> list[list[float]]:
    return [
        [0.0, 1.0, 0.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 0.0],
    ]


def _x_3() -> list[list[float]]:
    return [
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
    ]


class TestBenchmarkCore(unittest.TestCase):
    def test_benchmark_mac_average_returns_repeat_mean(self) -> None:
        # repeats=2, 각 반복에서 (1ms, 3ms) 구간
        with patch(
            "src.npu.benchmark.time.perf_counter",
            side_effect=[0.0, 0.001, 1.0, 1.003],
        ):
            fAvgMs = benchmark_mac_average(_cross_3(), _x_3(), iRepeats=2)
        self.assertAlmostEqual(fAvgMs, 2.0, places=9)

    def test_benchmark_mac_average_raises_when_repeats_invalid(self) -> None:
        with self.assertRaises(ValueError):
            benchmark_mac_average(_cross_3(), _x_3(), iRepeats=0)

    def test_benchmark_pair_contains_split_and_total_columns(self) -> None:
        # A 평균: (1ms + 1ms)/2 = 1ms
        # B 평균: (2ms + 2ms)/2 = 2ms
        # 총합: 3ms
        with patch(
            "src.npu.benchmark.time.perf_counter",
            side_effect=[
                0.0, 0.001, 1.0, 1.001,  # A repeats=2
                2.0, 2.002, 3.0, 3.002,  # B repeats=2
            ],
        ):
            dRow = benchmark_pair(_cross_3(), _cross_3(), _x_3(), iRepeats=2)

        self.assertEqual(dRow["size"], 3)
        self.assertEqual(dRow["ops_n2"], 9)
        self.assertAlmostEqual(float(dRow["avg_a_ms"]), 1.0, places=9)
        self.assertAlmostEqual(float(dRow["avg_b_ms"]), 2.0, places=9)
        self.assertAlmostEqual(float(dRow["avg_total_ms"]), 3.0, places=9)

    def test_format_table_includes_required_headers(self) -> None:
        sTable = format_benchmark_table(
            [
                {
                    "size": 3,
                    "avg_a_ms": 1.0,
                    "avg_b_ms": 2.0,
                    "avg_total_ms": 3.0,
                    "ops_n2": 9,
                },
            ],
        )
        self.assertIn("크기(N×N)", sTable)
        self.assertIn("A 평균(ms)", sTable)
        self.assertIn("B 평균(ms)", sTable)
        self.assertIn("합계 평균(ms)", sTable)
        self.assertIn("연산 횟수(N²)", sTable)


if __name__ == "__main__":
    unittest.main()
