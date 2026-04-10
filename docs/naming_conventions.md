# 네이밍 규칙 가이드 (`python_with_npu`)

이 문서는 `python_with_npu` 저장소에서 변수명을 정할 때 사용할 **타입 접두사 규칙**과
클래스 멤버 변수 규칙(`m_`)을 정의한다.

목표는 다음 2가지다.

- 변수명만 보고 데이터 형태를 빠르게 추론할 수 있게 한다.
- 운영 코드(`src`, `main.py`)와 테스트(`tests`)의 네이밍 기준을 통일한다.

---

## 1) 기본 원칙

- 변수명은 **접두사 + 의미 이름** 형식으로 작성한다.
- 접두사는 타입 힌트를 주고, 뒤 이름은 역할을 설명한다.
- 의미 이름은 가능한 명사/명사구로 작성한다.
- 상수(`UPPER_SNAKE_CASE`)는 기존 규칙을 유지한다.

예:

- `iSize`, `fElapsedMs`, `sPatternKey`, `bIsPass`, `lRows`, `dFiltersSection`

---

## 2) 타입 접두사 매핑

| 타입 | 접두사 | 예시 |
|------|--------|------|
| `int` | `i` | `iSize`, `iTotal` |
| `float` | `f` | `fScoreCross`, `fElapsedMs` |
| `str` | `s` | `sExpectedRaw`, `sSizeKey` |
| `pathlib.Path` | `p` | `pFilePath`, `pTargetPath` |
| `Callable` (function) | `fn` | `fnReader`, `fnInput` |
| `bool` | `b` | `bIsValid`, `bHasFailure` |
| `list` | `l` | `lPatternCases`, `lFailureDetails` |
| `dict` | `d` | `dData`, `dNormalizedFilters` |

권장:

- 복합 타입은 바깥 타입 기준으로 시작한다.
  - `list[dict[str, float]]` -> `lScoreRows`
  - `dict[str, list[list[float]]]` -> `dFiltersByLabel`
- 파일 경로를 `Path` 객체로 다룰 때는 `p` 접두사를 사용한다.
  - 예: `pFilePath = Path(sPath)`
- 함수(콜러블) 참조를 담는 변수는 `fn` 접두사를 사용한다.
  - 예: `fnReader = input_fn or input`

---

## 3) 적용 범위

- 함수 인자
- 함수 내부 지역 변수
- 테스트 코드 내 입력/기대값/중간값 변수
- 클래스 멤버 변수(`self.m_<name>`)

---

## 4) 멤버 변수 규칙

클래스 속성은 `m_` 접두사를 먼저 사용한다.

- 형식: `self.m_<name>`
- 필요 시 `<name>` 안에 타입 접두사를 함께 사용한다.
  - 예: `self.m_iRetryCount`, `self.m_sMode`

현재 저장소는 클래스 멤버 상태가 많지 않으므로, 신규 클래스 추가 시 이 규칙을 우선 적용한다.

---

## 5) 예외/허용 규칙

다음은 가독성 또는 관용을 위해 허용한다.

- `_` (의도적 미사용 변수)
- 예외 객체 `exc` (또는 매우 제한적으로 `e`)
- 루프 인덱스도 접두사 규칙을 기본 적용한다.
  - 권장: `iRow`, `iCol`, `iIdx`
  - 예외: 1~2줄짜리 매우 단순 반복에서만 `i`, `j`를 허용
- 타입이 불명확하거나 추론이 어려운 경우에는 타입 힌트(annotation)로 보완

주의:

- 내장 이름(`list`, `dict`, `str`, `id` 등)을 변수명으로 사용하지 않는다.
- 의미 없는 축약(`tmp`, `val`, `data2`)은 지양한다.

---

## 6) Before / After 예시

### 예시 A: JSON 처리 흐름

```python
# Before
data = load_json(path)
filters_section = data.get("filters")
pattern_cases = iter_pattern_cases(data)

# After
dData = load_json(sPath)
dFiltersSection = dData.get("filters")
lPatternCases = iter_pattern_cases(dData)
```

### 예시 B: 점수 판정

```python
# Before
score_cross = compute_mac(pattern_input, normalized_filters["Cross"])
score_x = compute_mac(pattern_input, normalized_filters["X"])
pass_fail = "PASS" if verdict == normalized_expected else "FAIL"

# After
fScoreCross = compute_mac(lPatternInput, dNormalizedFilters["Cross"])
fScoreX = compute_mac(lPatternInput, dNormalizedFilters["X"])
sPassFail = "PASS" if sVerdict == sNormalizedExpected else "FAIL"
```

---

## 7) 리팩터링 시 체크리스트

- 변수명 변경은 선언/사용 지점을 한 번에 바꾼다.
- 이름만 바꾸고 동작은 바꾸지 않는다.
- 모듈 단위로 변경 후 테스트를 즉시 실행한다.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

---

## 8) 관련 문서

- [`docs/commit_guidelines.md`](commit_guidelines.md)
- [`docs/testing_guidelines.md`](testing_guidelines.md)
