"""data.json 로드/패턴 반복 유틸."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(sPath: str | Path) -> dict[str, Any]:
    """JSON 파일을 읽어 dict로 반환한다."""
    pFilePath = Path(sPath)
    try:
        with pFilePath.open("r", encoding="utf-8") as f:
            dData = json.load(f)
    except FileNotFoundError as exc:
        raise ValueError(f"json file not found: {pFilePath}") from exc
    except PermissionError as exc:
        raise ValueError(f"json file is not readable: {pFilePath}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid json format: {pFilePath}") from exc
    except OSError as exc:
        raise ValueError(f"failed to read json file: {pFilePath} ({exc})") from exc

    if not isinstance(dData, dict):
        raise ValueError("json root must be an object")
    return dData


def iter_pattern_cases(dData: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """
    patterns 섹션을 (pattern_key, pattern_case) 리스트로 반환한다.

    pattern_case는 최소한 input/expected 키를 가져야 한다.
    """
    dPatterns = dData.get("patterns")
    if not isinstance(dPatterns, dict):
        raise ValueError("missing or invalid 'patterns' section")

    lCases: list[tuple[str, dict[str, Any]]] = []
    for sKey, dValue in dPatterns.items():
        if not isinstance(sKey, str):
            raise ValueError("pattern key must be a string")
        if not isinstance(dValue, dict):
            raise ValueError(f"pattern '{sKey}' must be an object")
        lCases.append((sKey, dValue))
    return lCases
