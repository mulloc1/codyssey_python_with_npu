"""JSON 로드 단계에서 라벨 정규화를 적용하는 I/O 유틸."""

from __future__ import annotations

from src.npu.labels import normalize_expected, normalize_filter_key


def normalize_expected_and_filter_key(expected: str, filter_key: str) -> tuple[str, str]:
    """
    JSON 케이스에서 expected/필터 키를 즉시 표준 라벨(Cross/X)로 정규화한다.

    반환 순서: (normalized_expected, normalized_filter_key)

    예시:
        입력: "+", "cross"
        반환: ("Cross", "Cross")
        입력: "x", "x"
        반환: ("X", "X")
    """
    return normalize_expected(expected), normalize_filter_key(filter_key)


def normalize_filter_score_keys(scores_by_filter_key: dict[str, float]) -> dict[str, float]:
    """
    필터 키를 표준 라벨로 변환한 점수 맵을 반환한다.

    입력: {"cross": 1.2, "x": 0.9}
    반환: {"Cross": 1.2, "X": 0.9}
    입력: {"Cross": 5.0, "x": 1.0}
    반환: {"Cross": 5.0, "X": 1.0}
    """
    normalized: dict[str, float] = {}
    for key, score in scores_by_filter_key.items():
        normalized_key = normalize_filter_key(key)
        if normalized_key in normalized:
            raise ValueError(f"duplicate normalized filter label: {normalized_key}")
        normalized[normalized_key] = score
    return normalized
