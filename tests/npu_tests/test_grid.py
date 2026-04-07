"""npu.grid 검증 함수 단위 테스트.

`tests/npu/`는 unittest discover 시 모듈명 `npu.*`와 소스 패키지 `npu`가 충돌하므로
`tests/npu_tests/`에 둔다(src/npu 구조는 tests/npu_tests로 미러링).
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# 프로젝트 루트의 src를 import 경로에 추가 (unittest discover 시 PYTHONPATH 없이 동작)
_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from npu.constants import DEFAULT_EPSILON  # noqa: E402
from npu.grid import same_shape, validate_matrix  # noqa: E402


def _zeros(n: int) -> list[list[int]]:
    return [[0 for _ in range(n)] for _ in range(n)]


class TestValidateMatrix(unittest.TestCase):
    def test_accepts_square_sizes_3_5_13_25(self) -> None:
        for n in (3, 5, 13, 25):
            with self.subTest(n=n):
                m = _zeros(n)
                self.assertEqual(validate_matrix(m), n)

    def test_rejects_empty_matrix(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix([])

    def test_rejects_non_list_matrix(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix("not a list")  # type: ignore[arg-type]

    def test_rejects_row_that_is_not_list(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix([[0, 0, 0], "bad", [0, 0, 0]])  # type: ignore[list-item]

    def test_rejects_ragged_rows(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix([[0, 0], [0, 0, 0]])


class TestSameShape(unittest.TestCase):
    def test_true_when_both_same_n(self) -> None:
        a = _zeros(3)
        b = _zeros(3)
        self.assertTrue(same_shape(a, b))

    def test_false_when_different_n(self) -> None:
        a = _zeros(3)
        b = _zeros(5)
        self.assertFalse(same_shape(a, b))

    def test_false_when_either_invalid(self) -> None:
        self.assertFalse(same_shape([], _zeros(3)))
        self.assertFalse(same_shape(_zeros(3), []))


class TestValidateMatrixWithExpectedSize(unittest.TestCase):
    def test_accepts_when_expected_size_matches(self) -> None:
        for n in (3, 5, 13, 25):
            with self.subTest(n=n):
                self.assertEqual(validate_matrix(_zeros(n), expected_size=n), n)

    def test_rejects_when_expected_size_mismatches(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            validate_matrix(_zeros(3), expected_size=5)
        self.assertIn("expected 5x5", str(ctx.exception))

    def test_rejects_expected_size_less_than_one(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix(_zeros(1), expected_size=0)

    def test_rejects_non_int_expected_size(self) -> None:
        with self.assertRaises(TypeError):
            validate_matrix(_zeros(3), expected_size="3")  # type: ignore[arg-type]


class TestConstantsImported(unittest.TestCase):
    """constants.py가 기대값을 노출하는지 스모크."""

    def test_default_epsilon(self) -> None:
        self.assertEqual(DEFAULT_EPSILON, 1e-9)


if __name__ == "__main__":
    unittest.main()
