# Mini NPU 시뮬레이터

`python_with_npu`는 MAC(Multiply-Accumulate) 연산 원리를 코드로 구현하고,  
입력 패턴이 Cross/X 필터 중 어느 쪽에 가까운지 판정하는 콘솔 프로젝트입니다.

## 프로젝트 구조

```text
python_with_npu/
├── main.py                 # 애플리케이션 진입점
├── data.json               # JSON 분석 모드용 필터·패턴 데이터
├── README.md
├── src/
│   ├── app/                # 콘솔 UI·흐름
│   ├── npu/                # MAC·판정·벤치마크 코어
│   └── npu_io/             # JSON/입력 파싱·스키마
├── tests/                  # 단위 테스트 (npu, npu_io, app)
└── docs/                   # 과제·커밋·인사이트 문서
```

## 주요 파일 역할

| 경로 | 역할 |
|------|------|
| `main.py` | `console_flow.main()`을 호출하는 진입점 |
| `src/app/console_flow.py` | 메뉴(3×3 수동 입력 / `data.json` 분석), MAC·판정·벤치 출력 흐름 |
| `src/app/report.py` | JSON 모드 종료 시 통과·실패 요약 문자열 생성 |
| `src/app/constants.py` | 메뉴 선택값 등 앱 상수 |
| `src/npu/mac.py` | MAC 누적 연산: `validate_mac_inputs`, 순수 `compute_mac(pattern, filter, size)`, 검증 포함 `compute_mac_checked` |
| `src/npu/grid.py` | 2차원 리스트가 정사각형 `N×N`인지 검증 (`validate_matrix` 등) |
| `src/npu/judgement.py` | MAC 점수 비교로 A/B 또는 Cross vs X 판정 (epsilon 반영) |
| `src/npu/labels.py` | 기대 라벨·필터 키 문자열을 내부 `Cross` / `X` 등으로 정규화 |
| `src/npu/constants.py` | 라벨 문자열, `DEFAULT_EPSILON` 등 |
| `src/npu/benchmark.py` | MAC 반복 측정, 표 포맷, Cross/X 패턴 생성 헬퍼 |
| `src/npu/__init__.py` | 패키지 공개 API 재노출 |
| `src/npu_io/json_loader.py` | `data.json` 로드, `patterns` 섹션 순회 |
| `src/npu_io/schema.py` | 패턴 키에서 `N` 추출, 크기별 필터 선택, 패턴·필터 형상 일괄 검증 |
| `src/npu_io/parse.py` | 콘솔 한 줄·행 단위 입력 파싱 |
| `src/npu_io/label_normalization.py` | JSON 쪽 raw 필터 키·expected와의 정규화 조합 |
| `tests/` | 위 모듈별 단위 테스트 |
| `docs/` | 구현 체크리스트, 네이밍, 과제 설명 등 참고 문서 |

## `data.json` 구조

루트는 객체이며, 최소한 **`filters`**와 **`patterns`** 두 섹션을 둡니다.

### `filters`

- 키: `"size_<N>"` 형식 (예: `"size_5"`, `"size_13"`). `<N>`은 정사각 행렬의 한 변 길이입니다.
- 값: 객체. 보통 **`cross`**, **`x`** 키에 각각 `N×N` 실수(또는 정수) 이차원 배열을 둡니다.  
  JSON 분석 모드에서는 이 행렬들이 내부 라벨 `Cross` / `X`에 대응하도록 정규화된 뒤 MAC에 사용됩니다.

### `patterns`

- 키: **`size_<N>_<idx>`** 형식만 허용됩니다 (예: `size_5_001`, `size_13_002`).  
  코드는 정규식으로 여기서 **`<N>`을 추출**해 `filters.size_<N>`을 고릅니다. 키 형식이 맞지 않으면 오류입니다.
- 값: 객체. 필수 필드:
  - **`input`**: `N×N` 이차원 배열. 위에서 추출한 `N`과 행·열 수가 일치해야 합니다.
  - **`expected`**: 문자열. 예: `"+"`, `"x"` 등. 로더는 이를 내부 기대 라벨(`Cross` / `X` 등)로 정규화한 뒤, MAC 판정 결과와 비교해 PASS/FAIL을 냅니다.

패턴 키의 `N`과 `input` 실제 크기, 그리고 선택된 필터 행렬 크기가 어긋나면 스키마 검증 단계에서 실패합니다.

## 결과 리포트

이번 구현에서 JSON 모드 종료 시 전체 테스트 수/통과 수/실패 수와 실패 상세를 함께 출력하도록 구성했습니다.  
실패 원인은 단일 원인이 아니라, 크게 세 부류로 나누어 분석할 수 있습니다.  
첫째, **데이터/스키마 문제**입니다. 예를 들어 `size_{N}_{idx}` 키 형식 오류, `filters.size_N` 누락, 패턴/필터 크기 불일치가 여기에 해당합니다.  
둘째, **라벨 해석 문제**입니다. 외부 데이터는 `+`, `x`, `cross`처럼 표기가 섞일 수 있으므로, 내부에서는 `Cross/X`로 정규화하지 않으면 PASS/FAIL 비교가 흔들립니다.  
셋째, **수치 비교 문제**입니다. 점수 비교에서 부동소수점 오차를 고려하지 않으면 동점 판정이 불안정해지고 오판정이 발생할 수 있습니다.  
이를 방지하기 위해 epsilon 기반 정책(`abs(a-b) < 1e-9`)을 사용해 `UNDECIDED` 경계를 명확히 했습니다.  
시간 복잡도 관점에서 MAC 코어는 `N×N` 배열을 한 번 순회하므로 기본적으로 `O(N²)`입니다.  
실제 성능 표에서도 `3x3 -> 5x5 -> 13x13 -> 25x25`로 갈수록 평균 시간이 증가하며, 연산 횟수(`N²`) 증가 경향과 일치합니다.  
또한 성능 지표는 판정 실사용 흐름을 반영하기 위해 A/B 분할 시간과 합계 시간(A+B)을 함께 출력했습니다.  
실패가 0건인 실행이라도 “왜 0건인지”를 라벨 정규화와 epsilon 비교 정책으로 설명할 수 있어야 결과 해석이 완성됩니다.
