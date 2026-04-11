"""라벨 정규화 유틸리티."""

from __future__ import annotations

from src.npu.constants import LABEL_CROSS, LABEL_X

_EXPECTED_LABEL_MAP: dict[str, str] = {
    "+": LABEL_CROSS,
    "x": LABEL_X,
    LABEL_CROSS: LABEL_CROSS,
    LABEL_X: LABEL_X,
}

# primary에 없는 expected 별칭(소문자만). "x"/"X"는 primary, "+"는 보조에 넣지 않음.
_EXPECTED_LABEL_LOWER_ALIASES: dict[str, str] = {
    "cross": LABEL_CROSS,
}

_FILTER_KEY_LABEL_MAP: dict[str, str] = {
    "cross": LABEL_CROSS,
    "x": LABEL_X,
    LABEL_CROSS: LABEL_CROSS,
    LABEL_X: LABEL_X,
}


def normalize_expected(sValue: str) -> str:
    """expected 라벨 입력을 표준 라벨(Cross/X)로 변환한다."""
    s = sValue.strip()
    if s in _EXPECTED_LABEL_MAP:
        return _EXPECTED_LABEL_MAP[s]
    sl = s.lower()
    if sl in _EXPECTED_LABEL_LOWER_ALIASES:
        return _EXPECTED_LABEL_LOWER_ALIASES[sl]
    raise ValueError(f"unsupported expected label: {sValue}")


def normalize_filter_key(sValue: str) -> str:
    """필터 키 입력을 표준 라벨(Cross/X)로 변환한다."""
    s = sValue.strip()
    if s in _FILTER_KEY_LABEL_MAP:
        return _FILTER_KEY_LABEL_MAP[s]
    sl = s.lower()
    try:
        return _FILTER_KEY_LABEL_MAP[sl]
    except KeyError as exc:
        raise ValueError(f"unsupported filter key label: {sValue}") from exc
