# 00_LearningSystem — Kids 학습 도우미 메타 시스템

> 작성: 2026-05-11 | 위치: `C:/Kids/00_LearningSystem/`
> 작성자: Nick + NCC (Claude)

## 한 줄 비전

> **들이는 시간·노력은 거의 같지만, 아이가 얻는 흥미·생각의 깊이·지식 수준이 훨씬 높아지는 학습 환경을 만든다.**
> 결국 **아이 스스로** 필요한 자료·앱·도구를 손쉽게 만들어내는 단계까지 간다.

---

## 왜 이 디렉토리가 있는가

- `C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/` — 딸(중1, 수학)을 위한 **성숙한** 시스템 (4축·orchestrator·audit 5종·chatlog 라운드 기반)
- `C:/Kids/70_HighSchool/2604_고1_중간고사/` — 아들(고1)을 위한 **시험·수행평가** 작업 공간 (수학 오답노트 4스킬 정착, 그 외 ad-hoc)
- 두 프로젝트에서 **반복되는 패턴**과 **다음 단계로 일반화 가능한 자산**들이 누적되고 있다.

> 이 디렉토리는 **개별 프로젝트의 산출물이 아니라**, 그 산출물에서 추출한 **패턴·원칙·청사진·미해결 질문**을 모아두는 메타 레이어다.

---

## 디렉토리 구조

| 폴더/파일 | 역할 |
|---|---|
| `README.md` | (이 파일) 진입점 |
| `CLAUDE.md` | 새 Claude 세션 시작 규칙 |
| `SYSTEM_GUIDE.md` | ⭐ **전체 skill/agent 운영 가이드** — 상황별 명령어·흐름 예시·배포 구조 |
| `00_chatlog/` | **모든 라운드 기록** — NCC가 의사결정·진행 누적 (Q03 확정) |
| `10_VISION.md` | 비전·우선순위·3대 원칙 |
| `20_PATTERNS/` | **자산 카탈로그** — 발견된 도우미 패턴 (P01~P06) |
| `30_COMPONENTS.md` | UI 공통 컴포넌트 모음 (HTML 앱 부품) |
| `40_PRINCIPLES/` | 절대 원칙 — common + 영역별 (math, perf_eval, writing, deploy, communication) |
| `50_BLUEPRINTS.md` | Skill / Agent 개별 청사진 명세 |
| `51_MASTER_PLAN.md` | **전체 시스템 그림 + 링크 다이어그램 + 빌드 순서 (Phase A~F)** ⭐ |
| `60_LEARNERS.md` | 학습자 프로필 (아들·딸, 현재 자율도 L0) |
| `70_OPEN_QUESTIONS/` | Nick에게 묻는 의사결정 질문 |
| `80_ROADMAP.md` | 진화 로드맵 (now → 3개월 → 1년) |

---

## 작업 순서 추천 (이 디렉토리 활용법)

### 새 과목·새 학년·새 과제를 만나면

1. `20_PATTERNS/`에서 비슷한 패턴이 있는지 본다 (있으면 재사용)
2. 없으면 ad-hoc로 작업한 후, **끝나면** `20_PATTERNS/P99_새_패턴_제안_템플릿.md`를 채워서 자산화
3. 새 UI 컴포넌트가 나오면 `30_COMPONENTS.md`에 추가

### 의사결정이 필요할 때

- `70_OPEN_QUESTIONS/` 에서 관련 질문 찾기
- 답이 결정되면 해당 질문 파일에 `(Nick)`로 결정 기록 → `40_PRINCIPLES.md` 또는 `50_BLUEPRINTS.md`에 반영

### 다음에 만들 skill / agent 결정

- `50_BLUEPRINTS.md` 의 우선순위 표 참고
- `80_ROADMAP.md` 의 현재 단계 확인

---

## 두 자식 프로젝트 (단순 링크)

- 🟣 **MathTelling (딸)**: `../30_MiddleSchool/260426_MathTelling_Idea/`
- 🟢 **HighSchool 1학년 (아들)**: `../70_HighSchool/2604_고1_중간고사/`
