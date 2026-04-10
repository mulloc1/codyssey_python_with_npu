"""data.json 키 파싱/필터 선택/형상 검증."""

from __future__ import annotations

import re
from typing import Any

from src.npu.grid import validate_matrix

_PATTERN_KEY_RE = re.compile(r"^size_(\d+)_(\d+)$")


def extract_size_from_pattern_key(sPatternKey: str) -> int:
    """
    pattern key(`size_{N}_{idx}`)에서 N을 추출한다.

    예시:
        입력: "size_13_002"
        반환: 13
        입력: "size_5_001"
        반환: 5
    """
    oMatch = _PATTERN_KEY_RE.match(sPatternKey)
    if oMatch is None:
        raise ValueError(f"invalid pattern key format: {sPatternKey}")
    return int(oMatch.group(1))


def select_filters_for_size(dFiltersSection: dict[str, Any], iSize: int) -> dict[str, Any]:
    """
    filters 섹션에서 size에 대응하는 필터 맵을 반환한다.

    예시:
        입력: filters_section = {
            "size_5": {...},
            "size_13": {...},
        }, size = 5
        반환: {...} => n * n 의 filter matrix
    """
    sSizeKey = f"size_{iSize}"
    dFiltersForSize = dFiltersSection.get(sSizeKey)
    if not isinstance(dFiltersForSize, dict):
        raise ValueError(f"missing or invalid filters for '{sSizeKey}'")
    return dFiltersForSize


def validate_pattern_and_filters(
    lPatternInput: Any,
    dFiltersByLabel: dict[str, Any],
    iExpectedSize: int,
) -> None:
    """패턴과 필터들의 N×N 형상을 검증한다."""
    validate_matrix(lPatternInput, iExpectedSize=iExpectedSize)
    for sFilterLabel, lFilterMatrix in dFiltersByLabel.items():
        try:
            validate_matrix(lFilterMatrix, iExpectedSize=iExpectedSize)
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"invalid filter matrix for '{sFilterLabel}': {exc}",
            ) from exc
