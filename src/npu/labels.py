"""라벨 정규화 유틸리티."""

from __future__ import annotations

from src.npu.constants import LABEL_CROSS, LABEL_X

_EXPECTED_LABEL_MAP: dict[str, str] = {
    "+": LABEL_CROSS,
    "x": LABEL_X,
    LABEL_CROSS: LABEL_CROSS,
    LABEL_X: LABEL_X,
}

_FILTER_KEY_LABEL_MAP: dict[str, str] = {
    "cross": LABEL_CROSS,
    "x": LABEL_X,
    LABEL_CROSS: LABEL_CROSS,
    LABEL_X: LABEL_X,
}


def normalize_expected(sValue: str) -> str:
    """expected 라벨 입력을 표준 라벨(Cross/X)로 변환한다."""
    try:
        return _EXPECTED_LABEL_MAP[sValue]
    except KeyError as exc:
        raise ValueError(f"unsupported expected label: {sValue}") from exc


def normalize_filter_key(sValue: str) -> str:
    """필터 키 입력을 표준 라벨(Cross/X)로 변환한다."""
    try:
        return _FILTER_KEY_LABEL_MAP[sValue]
    except KeyError as exc:
        raise ValueError(f"unsupported filter key label: {sValue}") from exc
