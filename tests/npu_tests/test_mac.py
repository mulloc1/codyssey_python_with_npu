"""npu.mac 단위 테스트."""

from __future__ import annotations

import unittest

from src.npu.mac import compute_mac


class TestComputeMac(unittest.TestCase):
    # 문서 예시 기준으로 Cross x Cross MAC 점수는 5여야 한다.
    def test_subject_example_cross_cross_scores_five(self) -> None:
        cross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        self.assertEqual(compute_mac(cross, cross), 5.0)

    # 문서 예시 기준으로 Cross x X MAC 점수는 1이어야 한다.
    def test_subject_example_cross_x_scores_one(self) -> None:
        cross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        x_filter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        self.assertEqual(compute_mac(cross, x_filter), 1.0)

    # 동일 입력에서는 Cross 필터 점수가 X 필터 점수보다 커야 한다.
    def test_cross_filter_score_higher_than_x_filter(self) -> None:
        cross = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
        x_filter = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        score_cross = compute_mac(cross, cross)
        score_x = compute_mac(cross, x_filter)
        self.assertGreater(score_cross, score_x)

    # 실수 입력이 섞여도 MAC 누적 결과가 기대값(0.9)에 근접해야 한다.
    def test_float_inputs_are_accumulated_correctly(self) -> None:
        pattern = [
            [0.1, 0.2],
            [0.3, 0.4],
        ]
        filt = [
            [1.5, -1.0],
            [0.5, 2.0],
        ]
        # 0.1*1.5 + 0.2*(-1.0) + 0.3*0.5 + 0.4*2.0 = 0.9
        self.assertAlmostEqual(compute_mac(pattern, filt), 0.9, places=12)

    # pattern/filter 크기가 다르면 명시적 예외를 발생시켜야 한다.
    def test_raises_on_shape_mismatch(self) -> None:
        pattern = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        filt = [
            [1, 0],
            [0, 1],
        ]
        with self.assertRaises(ValueError) as ctx:
            compute_mac(pattern, filt)
        self.assertIn("same shape", str(ctx.exception))

    # ragged matrix처럼 형상이 깨진 입력은 예외로 거부해야 한다.
    def test_raises_on_invalid_ragged_matrix(self) -> None:
        pattern = [
            [1, 0, 1],
            [0, 1],
            [1, 0, 1],
        ]
        filt = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        with self.assertRaises(ValueError):
            compute_mac(pattern, filt)


if __name__ == "__main__":
    unittest.main()
