"""npu.grid 검증 함수 단위 테스트.

`tests/npu/`는 unittest discover 시 모듈명 `npu.*`와 소스 패키지 `npu`가 충돌하므로
`tests/npu_tests/`에 둔다(src/npu 구조는 tests/npu_tests로 미러링).
"""

from __future__ import annotations

import unittest

from src.npu.constants import DEFAULT_EPSILON
from src.npu.grid import same_shape, validate_matrix


def _zeros(n: int) -> list[list[int]]:
    return [[0 for _ in range(n)] for _ in range(n)]


class TestValidateMatrix(unittest.TestCase):
    # 지원 대상 크기(3, 5, 13, 25)의 정사각형 입력은 정상 통과해야 한다.
    def test_accepts_square_sizes_3_5_13_25(self) -> None:
        for n in (3, 5, 13, 25):
            with self.subTest(n=n):
                m = _zeros(n)
                self.assertEqual(validate_matrix(m), n)

    # 빈 배열은 유효한 정사각형이 아니므로 예외가 나야 한다.
    def test_rejects_empty_matrix(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix([])

    # matrix 자체가 리스트가 아니면 예외가 나야 한다.
    def test_rejects_non_list_matrix(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix("not a list")  # type: ignore[arg-type]

    # 각 행은 리스트여야 하며, 다른 타입이 섞이면 예외가 나야 한다.
    def test_rejects_row_that_is_not_list(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix([[0, 0, 0], "bad", [0, 0, 0]])  # type: ignore[list-item]

    # 행 길이가 들쭉날쭉한 ragged 배열은 거부해야 한다.
    def test_rejects_ragged_rows(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix([[0, 0], [0, 0, 0]])


class TestSameShape(unittest.TestCase):
    # 동일한 크기의 두 정사각형은 same_shape가 True여야 한다.
    def test_true_when_both_same_n(self) -> None:
        a = _zeros(3)
        b = _zeros(3)
        self.assertTrue(same_shape(a, b))

    # 크기가 다르면 same_shape가 False여야 한다.
    def test_false_when_different_n(self) -> None:
        a = _zeros(3)
        b = _zeros(5)
        self.assertFalse(same_shape(a, b))

    # 둘 중 하나라도 유효하지 않은 행렬이면 False여야 한다.
    def test_false_when_either_invalid(self) -> None:
        self.assertFalse(same_shape([], _zeros(3)))
        self.assertFalse(same_shape(_zeros(3), []))


class TestValidateMatrixWithExpectedSize(unittest.TestCase):
    # expected_size와 실제 크기가 같으면 통과해야 한다.
    def test_accepts_when_expected_size_matches(self) -> None:
        for n in (3, 5, 13, 25):
            with self.subTest(n=n):
                self.assertEqual(validate_matrix(_zeros(n), expected_size=n), n)

    # expected_size와 실제 크기가 다르면 예외가 나야 한다.
    def test_rejects_when_expected_size_mismatches(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            validate_matrix(_zeros(3), expected_size=5)
        self.assertIn("expected 5x5", str(ctx.exception))

    # expected_size는 1 이상이어야 한다.
    def test_rejects_expected_size_less_than_one(self) -> None:
        with self.assertRaises(ValueError):
            validate_matrix(_zeros(1), expected_size=0)

    # expected_size 타입이 int가 아니면 예외가 나야 한다.
    def test_rejects_non_int_expected_size(self) -> None:
        with self.assertRaises(TypeError):
            validate_matrix(_zeros(3), expected_size="3")  # type: ignore[arg-type]


class TestConstantsImported(unittest.TestCase):
    """constants.py가 기대값을 노출하는지 스모크."""

    # 기본 epsilon 상수가 문서 기준값(1e-9)인지 확인한다.
    def test_default_epsilon(self) -> None:
        self.assertEqual(DEFAULT_EPSILON, 1e-9)


if __name__ == "__main__":
    unittest.main()
