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
| `main.py` | `console_flow.run()`을 호출하는 진입점 |
| `src/app/console_flow.py` | 메인 메뉴·모드 라우팅(`run`) |
| `src/app/user_input_3x3.py` | 3×3 수동 입력 모드(MAC·판정·소형 성능 표) |
| `src/app/data_json_mode.py` | `data.json` 분석 모드(케이스별 출력·요약·성능 표) |
| `src/app/report.py` | JSON 모드 종료 시 통과·실패 요약 문자열 생성 |
| `src/app/constants.py` | 메뉴 선택값 등 앱 상수 |
| `src/npu/mac.py` | MAC 누적 연산: `validate_mac_inputs`, 순수 `compute_mac(pattern, filter, size)` |
| `src/npu/grid.py` | 2차원 리스트가 정사각형 `N×N`인지 검증 (`validate_matrix` 등) |
| `src/npu/judgement.py` | MAC 점수 비교로 A/B 또는 Cross vs X 판정 (epsilon 반영) |
| `src/npu/labels.py` | 기대 라벨·필터 키 문자열을 내부 `Cross` / `X` 등으로 정규화 |
| `src/npu/constants.py` | 라벨 문자열, `DEFAULT_EPSILON` 등 |
| `src/npu/benchmark.py` | MAC 반복 측정, 표 포맷, Cross/X 패턴 생성 헬퍼 |
| `src/npu/__init__.py` | 패키지 공개 API 재노출 |
| `src/npu_io/json_loader.py` | `data.json` 로드, `patterns` 섹션 순회 |
| `src/npu_io/schema.py` | 패턴 키에서 `N` 추출, 크기별 필터 선택, 패턴·필터 형상 일괄 검증 |
| `src/npu_io/parse.py` | 콘솔 한 줄·행 단위 입력 파싱 |
| `src/npu_io/label_normalization.py` | 필터 키 집합을 표준 라벨로 변환·중복 검증 (`normalize_filter_score_keys`) |
| `tests/` | 위 모듈별 단위 테스트 |
| `docs/` | 구현 체크리스트, 네이밍, [함수 작성 가이드](docs/function_conventions.md) 등 |

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

## 결과 리포트(실패 원인 + 복잡도)

JSON 분석 모드(`data.json`)가 끝나면 콘솔에 요약 블록이 출력됩니다. `src/app/report.py`의 `summarize_results`가 전체 테스트 수·통과 수·실패 수를 내고, 실패가 있으면 패턴 키별로 한 줄 요약을 이어 붙입니다. 같은 정보를 바탕으로 “왜 실패했는지”와 “연산 비용이 어떻게 스케일하는지”를 아래 축으로 나누어 보면 보고서 해석이 수월합니다.

### 콘솔에 나오는 것

- 각 패턴 케이스 한 줄: Cross/X MAC 점수, 판정 라벨, 기대 라벨, PASS 또는 FAIL, 측정 시간(ms).
- 마지막 요약: 전체·통과·실패 건수와 실패 케이스 목록(키와 짧은 사유).

### 실패 원인을 나누는 기준

실패 한 건이 항상 “모델이 틀렸다”는 뜻은 아닙니다. 원인은 대략 세 갈래로 묶을 수 있습니다.

1. 데이터·스키마: 패턴 키가 `size_<N>_<idx>` 규칙을 벗어남, `filters.size_<N>` 누락, `input`과 `N` 또는 필터 행렬의 행·열 수 불일치, JSON 필드 타입 오류 등. 이 경우는 MAC 이전 단계에서 예외로 잡히며 요약에 메시지가 남습니다.
2. 라벨·표기: 파일에는 `+`, `x`, `cross`, 대소문자·공백 혼용이 올 수 있습니다. 내부에서는 `Cross` / `X`로 정규화한 뒤 기대값과 판정을 비교합니다. 정규화 규칙과 맞지 않는 문자열은 지원되지 않은 라벨로 실패합니다.
3. 수치·판정: 두 점수 차이가 매우 작을 때 부동소수점만으로는 “동점인지 승자인지”가 흔들릴 수 있습니다. 그래서 `abs(a - b) < ε`(기본 `ε = 1e-9`)이면 동률로 보고 JSON 모드에서는 `UNDECIDED`로 표시하며, 기대가 Cross 또는 X일 때는 일치하지 않으므로 FAIL로 집계됩니다.

### 복잡도와 성능 표의 읽는 법

- MAC 한 번은 패턴과 필터의 같은 위치끼리 곱해 합하므로, 한 변 길이를 `N`이라 하면 위치 수는 `N²`이고 시간 복잡도는 `Θ(N²)`입니다.
- 벤치마크 표는 크기별로 MAC를 여러 번 돌린 뒤 평균 시간(ms)을 냅니다. Cross 대 X 판정에 가깝게, 필터 A·B(또는 크기별 `cross`/`x`)에 대한 시간을 나누어 보여 주고 합계 열로 한 판정 루프에 가까운 비용을 볼 수 있습니다.
- `3×3 → 5×5 → 13×13 → 25×25`처럼 `N`이 커질수록 평균 시간과 표의 `연산 횟수(N²)`가 함께 커지는 경향이 나오면, 구현이 이론적 스케일과 크게 어긋나지 않는다고 보면 됩니다.

### 실패 0건일 때

통과만 있어도 리포트 관점에서는 “스키마·라벨·epsilon 정책이 전제를 만족했는지”를 한 번 점검했다는 뜻입니다. 반대로 실패가 많다면 위 세 축 중 어디에서 깨졌는지부터 나누어 보는 것이 디버깅 순서를 정리하는 데 도움이 됩니다.
