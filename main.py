"""Mini NPU 시뮬레이터 진입점."""

from __future__ import annotations

import sys
from pathlib import Path

# 저장소 루트에서 `python main.py` 실행 시 패키지 경로 보장
_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from app.console_flow import main  # noqa: E402

if __name__ == "__main__":
    main()
