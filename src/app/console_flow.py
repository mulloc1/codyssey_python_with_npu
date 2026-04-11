"""콘솔 메인 메뉴 및 모드 라우팅."""

from __future__ import annotations

from src.app.data_json_mode import run_data_json_mode
from src.app.user_input_3x3 import run_user_input_mode_3x3

_MENU_USER_INPUT_3X3 = "1"
_MENU_JSON_ANALYSIS = "2"


def run() -> None:
    """시작 메뉴 루프."""
    while True:
        try:
            print("\n입력 방식을 선택하세요.")
            print("  1) 사용자 입력(3×3)")
            print("  2) data.json 분석")
            sChoice = input("선택 (1-2): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n입력이 중단되어 종료합니다.")
            return
        if sChoice == _MENU_USER_INPUT_3X3:
            run_user_input_mode_3x3()
            continue
        if sChoice == _MENU_JSON_ANALYSIS:
            run_data_json_mode()
            continue
        print(f"\n{_MENU_USER_INPUT_3X3}, {_MENU_JSON_ANALYSIS} 중에서 입력해 주세요.")
