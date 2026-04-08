"""data.json 로드/패턴 반복 유틸."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    """JSON 파일을 읽어 dict로 반환한다."""
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as exc:
        raise ValueError(f"json file not found: {file_path}") from exc
    except PermissionError as exc:
        raise ValueError(f"json file is not readable: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid json format: {file_path}") from exc
    except OSError as exc:
        raise ValueError(f"failed to read json file: {file_path} ({exc})") from exc

    if not isinstance(data, dict):
        raise ValueError("json root must be an object")
    return data


def iter_pattern_cases(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """
    patterns 섹션을 (pattern_key, pattern_case) 리스트로 반환한다.

    pattern_case는 최소한 input/expected 키를 가져야 한다.
    """
    patterns = data.get("patterns")
    if not isinstance(patterns, dict):
        raise ValueError("missing or invalid 'patterns' section")

    cases: list[tuple[str, dict[str, Any]]] = []
    for key, value in patterns.items():
        if not isinstance(key, str):
            raise ValueError("pattern key must be a string")
        if not isinstance(value, dict):
            raise ValueError(f"pattern '{key}' must be an object")
        cases.append((key, value))
    return cases
