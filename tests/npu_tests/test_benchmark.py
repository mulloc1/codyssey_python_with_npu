"""npu.benchmark 단위 테스트."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from src.npu.benchmark import (
    benchmark_mac_average,
    benchmark_mac_once,
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
    def test_benchmark_mac_once_uses_perf_counter_delta(self) -> None:
        with patch("src.npu.benchmark.time.perf_counter", side_effect=[1.0, 1.002]):
            elapsed_ms = benchmark_mac_once(_cross_3(), _cross_3())
        self.assertAlmostEqual(elapsed_ms, 2.0, places=9)

    def test_benchmark_mac_average_returns_repeat_mean(self) -> None:
        # repeats=2, 각 반복에서 (1ms, 3ms) 구간
        with patch(
            "src.npu.benchmark.time.perf_counter",
            side_effect=[0.0, 0.001, 1.0, 1.003],
        ):
            avg_ms = benchmark_mac_average(_cross_3(), _x_3(), repeats=2)
        self.assertAlmostEqual(avg_ms, 2.0, places=9)

    def test_benchmark_mac_average_raises_when_repeats_invalid(self) -> None:
        with self.assertRaises(ValueError):
            benchmark_mac_average(_cross_3(), _x_3(), repeats=0)

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
            row = benchmark_pair(_cross_3(), _cross_3(), _x_3(), repeats=2)

        self.assertEqual(row["size"], 3)
        self.assertEqual(row["ops_n2"], 9)
        self.assertAlmostEqual(float(row["avg_a_ms"]), 1.0, places=9)
        self.assertAlmostEqual(float(row["avg_b_ms"]), 2.0, places=9)
        self.assertAlmostEqual(float(row["avg_total_ms"]), 3.0, places=9)

    def test_format_table_includes_required_headers(self) -> None:
        table = format_benchmark_table(
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
        self.assertIn("크기(N×N)", table)
        self.assertIn("A 평균(ms)", table)
        self.assertIn("B 평균(ms)", table)
        self.assertIn("합계 평균(ms)", table)
        self.assertIn("연산 횟수(N²)", table)


if __name__ == "__main__":
    unittest.main()
