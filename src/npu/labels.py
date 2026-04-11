"""라벨 정규화 유틸리티."""

from __future__ import annotations

from src.npu.constants import LABEL_CROSS, LABEL_X

_LABEL_MAP: dict[str, str] = {
    "cross": LABEL_CROSS,
    "x": LABEL_X,
    "+": LABEL_CROSS,
    LABEL_CROSS: LABEL_CROSS,
    LABEL_X: LABEL_X,
}


def normalize_label(sValue: str) -> str:
    """라벨 문자열을 표준 라벨(Cross/X)로 변환한다."""
    s = sValue.strip()
    if s in _LABEL_MAP:
        return _LABEL_MAP[s]
    sl = s.lower()
    if sl in _LABEL_MAP:
        return _LABEL_MAP[sl]
    raise ValueError(f"unsupported label: {sValue}")


def normalize_filter_score_keys(dScoresByFilterKey: dict[str, float]) -> dict[str, float]:
    """
    필터 키를 표준 라벨로 변환한 점수 맵을 반환한다.

    입력: {"cross": 1.2, "x": 0.9}
    반환: {"Cross": 1.2, "X": 0.9}
    """
    dNormalized: dict[str, float] = {}
    for sKey, fScore in dScoresByFilterKey.items():
        sNormalizedKey = normalize_label(sKey)
        if sNormalizedKey in dNormalized:
            raise ValueError(f"duplicate normalized filter label: {sNormalizedKey}")
        dNormalized[sNormalizedKey] = fScore
    return dNormalized
