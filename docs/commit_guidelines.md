# Git 커밋 규칙 (`python_with_npu`)

이 문서는 **이 저장소(`python_with_npu`)** 에서 Mini NPU 과제를 진행할 때 **커밋 단위**와 **커밋 메시지**를 맞추기 위한 가이드이다.

---

## 1) 커밋 단위

- **한 커밋에는 하나의 논리적 변경**만 담는 것을 권장한다.
  - 예: MAC 연산 구현, `data.json` 로더 추가, 라벨 정규화, epsilon 판정, 성능 측정, 테스트 보강, README 리포트 섹션 각각을 분리.
- 서로 무관한 수정을 한 커밋에 섞으면 **되돌리기·리뷰·이력 추적**이 어려워진다.

---

## 2) 커밋 메시지 컨벤션

- **첫 줄**: 무엇을 했는지 **한 문장**(대략 **50자 내외** 권장).
- **본문**(선택): 이유·주의사항·스키마/epsilon 같은 판단 근거를 필요할 때만 추가한다.
- **타입 접두어**(권장): [Conventional Commits](https://www.conventionalcommits.org/) 스타일을 쓸 수 있다.

| 접두어 | 용도 |
|--------|------|
| `feat:` | 새 기능(모드, 판정, CLI 흐름 등) |
| `fix:` | 버그 수정·예외·잘못된 판정/파싱 수정 |
| `docs:` | `docs/*.md`, README만 변경 |
| `test:` | 테스트 추가·수정 |
| `refactor:` | 동작 유지 리팩터링 |
| `chore:` | 디렉터리 정리, 병합, 설정 등(기능 변경이 주가 아닐 때) |

---

## 3) 커밋 개수 목표

- 과제를 단계별로 진행할수록 커밋이 쌓이도록 하고, **이 저장소 기준 총 10개 이상**의 커밋을 유지하는 것을 목표로 한다.
- 현재 로컬 브랜치의 커밋 개수 확인:

```bash
git rev-list --count HEAD
```

---

## 4) 메시지 예시 (이 과제에 맞춘 패턴)

아래는 **Mini NPU 시뮬레이터** 범위에서 쓰기 좋은 첫 줄 예시이다. 해시는 실제 커밋 후 자동으로 붙는 값이므로 메시지만 참고하면 된다.

```text
feat: MAC 연산 및 동일 크기 검증 구현
feat: 3×3 콘솔 입력 모드(필터 A/B, 패턴)
feat: data.json 로드 및 패턴 키에서 N 추출
feat: 라벨 정규화(Cross/X) 및 expected 매핑
feat: epsilon 기반 동점 처리 및 UNDECIDED 판정
feat: JSON 모드 PASS/FAIL 및 실패 케이스 수집
feat: 크기별 MAC 반복 측정 및 결과 표 출력
fix: 부동소수점 비교 시 오판정 나는 케이스 수정
test: MAC 및 판정 로직 유닛 테스트 추가
docs: README에 결과 리포트·시간 복잡도 섹션 추가
refactor: 입출력과 도메인 로직 분리
chore: 프로젝트 초기 디렉터리 및 실행 진입점 정리
```

브랜치 작업 시:

```bash
git log --oneline --decorate -20
git log --oneline --graph --all -30
```

---

## 5) 과제 요구사항과 커밋 나누기

`docs/subject.md` 기준으로 나누기 쉬운 경계는 대략 다음과 같다.

- MAC 코어(외부 라이브러리 없이 이중 루프)
- 콘솔 3×3 모드 vs `data.json` 모드 분기
- 스키마·크기 검증(실패 시 FAIL, 비정상 종료 없음)
- 성능 측정(반복 횟수, I/O 제외 권장 구간)
- README의 결과 리포트·복잡도 서술

한 PR/제출물 안에서도 **히스토리가 읽히도록** 위 단위에 가깝게 커밋을 쌓는 것이 좋다.

---

## 6) 관련 문서 (이 저장소)

- [`docs/subject.md`](subject.md) — 기능·실행 흐름·제출 요구사항
- [`docs/testing_guidelines.md`](testing_guidelines.md) — 테스트 배치·작성 규칙(테스트 커밋 시 참고)
- [Conventional Commits](https://www.conventionalcommits.org/) — 접두어·본문 작성 참고
