"""data.json 키 파싱/필터 선택/형상 검증."""

from __future__ import annotations

import re
from typing import Any

from src.npu.grid import validate_matrix

_PATTERN_KEY_RE = re.compile(r"^size_(\d+)_(\d+)$")


def extract_size_from_pattern_key(pattern_key: str) -> int:
    """
    pattern key(`size_{N}_{idx}`)에서 N을 추출한다.

    예시:
        입력: "size_13_002"
        반환: 13
        입력: "size_5_001"
        반환: 5
    """
    match = _PATTERN_KEY_RE.match(pattern_key)
    if match is None:
        raise ValueError(f"invalid pattern key format: {pattern_key}")
    return int(match.group(1))


def select_filters_for_size(filters_section: dict[str, Any], size: int) -> dict[str, Any]:
    f"""
    filters 섹션에서 size에 대응하는 필터 맵을 반환한다.

    예시:
        입력: filters_section = {
            "size_5": {...},
            "size_13": {...},
        }, size = 5
        반환: {...} => n * n 의 filter matrix
    """
    size_key = f"size_{size}"
    filters_for_size = filters_section.get(size_key)
    if not isinstance(filters_for_size, dict):
        raise ValueError(f"missing or invalid filters for '{size_key}'")
    return filters_for_size


def validate_pattern_and_filters(
    pattern_input: Any,
    filters_by_label: dict[str, Any],
    expected_size: int,
) -> None:
    """패턴과 필터들의 N×N 형상을 검증한다."""
    validate_matrix(pattern_input, expected_size=expected_size)
    for filter_label, filter_matrix in filters_by_label.items():
        try:
            validate_matrix(filter_matrix, expected_size=expected_size)
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"invalid filter matrix for '{filter_label}': {exc}",
            ) from exc
