"""NPU 시뮬레이터 코어 패키지."""

from npu.constants import (
    DEFAULT_EPSILON,
    LABEL_CROSS,
    LABEL_UNDECIDED,
    LABEL_X,
)
from npu.benchmark import (
    benchmark_mac_average,
    benchmark_mac_once,
    benchmark_pair,
    build_benchmark_rows,
    build_cross_pattern,
    build_x_pattern,
    format_benchmark_table,
)
from npu.judgement import judge_ab, judge_cross_vs_x
from npu.labels import normalize_expected, normalize_filter_key
from npu.mac import compute_mac
from npu.pattern_generator import (
    generate_cross_pattern,
    generate_x_pattern,
    validate_size,
)

__all__ = [
    "DEFAULT_EPSILON",
    "LABEL_CROSS",
    "LABEL_UNDECIDED",
    "LABEL_X",
    "benchmark_mac_average",
    "benchmark_mac_once",
    "benchmark_pair",
    "build_benchmark_rows",
    "build_cross_pattern",
    "build_x_pattern",
    "format_benchmark_table",
    "generate_cross_pattern",
    "generate_x_pattern",
    "judge_ab",
    "judge_cross_vs_x",
    "normalize_expected",
    "normalize_filter_key",
    "compute_mac",
    "validate_size",
]
