<!-- 0602_skill_cleanup_retro_and_open.md -->

# 0602 — 스킬 정리 회고 + 열린 항목 정리

> NCC 자율 종료 기록. 직전 작업 = `0601_skill_cleanup_checklist.md` 실행(완료·push). 본 파일은 그 회고 + 앞으로 더 논의/불확실/개선/궁금/추가작업할 항목을 한곳에 모은 것.
> 후속 결정은 이 파일에 `# Round N` 누적. 마스터 플랜 = `00_project_hub/20_plan/0601_next_phase.md`.

---

## 0. 직전 라운드 결과 (스킬·에이전트 정리 — 완료)

- **최종 인벤토리:** 23 skill + 2 agent, 전부 kebab.
  - 영상 9 (se-people-pick·se-people-narrate·se-video-story·se-video-storyboard·se-video-narration·se-video-image·se-video-motion·se-video-render·se-video-compose)
  - math/audit/meta 13 (se-unit-plan·se-concept-review·se-math-figure·se-math-practice·se-math-error-note·se-type-explorer·se-unit-review·se-audit-{app,math,concept,problem,story}·se-distill-principles)
  - story 1 (se-story-write — 보존 결정)
  - agent 2 (se-unit-orchestrator·se-video-orchestrator)
- **폐기:** se_story_video_v1_5 → `90_archive/skills_legacy/` (8-STEP 완전 대체).
- **검증:** SSOT·미러 underscore 0 / forward 참조 잔존 0 / `name:` 전부 kebab / available-skills 등록 확인.
- **커밋:** `f811346` push 완료. 1차 배포(jwj-nick.github.io/mid1)도 라이브.

---

## 1. 🟡 더 논의할 것 (Nick 결정 대기)

1. **se-story-write 흡수 여부** — 현재 보존. 영상 파이프라인의 `se-people-narrate`와 역할 겹침(인물 산문). story.html(축B 앱) 입력으로 실사용 중이라 즉시 삭제 위험 → 보류. *추후: 두 스킬 입력/출력 스펙 비교 후 통합 or 분리 확정.*
(Nick) 두 skill 중 하나만 남기기. 최근 workflow setup 때 se-people-narrate 를 주력으로 했고 se-story-write 가 이전에 만든거였던 것 같은데, agent, 다른 major skill 들, orchestrator 가 어떤걸 major 로 쓰는 지 확인하고 지금 정리하기.

2. **audit 접두 "ncc" 제거 수용 확인** — `se_ncc_audit_*` → `se-audit-*`로 줄임(TODO 선례). 호칭 NCC는 chatlog에서 유지, 스킬명에서만 탈락. 문제없으면 확정.
(Nick) se_ncc_audit_* 는 이미 사라진 것 같은데?? 문제 없음

3. **nav app 위치** — `mid1/` 통합 vs 새 앱/새 배포. (0601 §5-2)
(Nick) nav app 위치는 mid1/ 통합이 적절할 것 같음. (일단은 그렇게)

4. **연결망(connection-graph) 범위** — 중1 13단원만 vs 중2~고1 골격까지. (0601 §5-3) → 데이터 모델 SSOT 위치(`30_content/` graph)와 직결.
(Nick) 나중에는 계속 연결됨. 중1에 한정하지 않음.

5. **감싼 설명(wrapping) 톤** — 딸용 짧은 감성 vs 참고형, 빈칸 남길지(절대원칙 5). (0601 §5-4)
(Nick) '0601 §5-4'?? 어느파일?  당신이 합리적인 방법으로 정리 바람. 지금 어느정도 셋업 완료 된걸로 아는데...
---

## 2. ❓ 불확실한 것

- **sync-skills.sh 비-mirror 위험** — 삭제 동기화 안 됨. rename·폐기마다 `.claude/` 옛 디렉터리 수동 삭제 필요. → *개선안 §3-1.*
(Nick) 당신이 합리적인 방법으로 정리 바람.
- **70_meta/ outdated 3종**(VISION·MASTER_PLAN·ROADMAP) — 옛 00_LearningSystem 시절 표기 잔존. 이번 정리에서 의도적으로 skip. 폐기 vs 갱신 미정.
(Nick) 폐기
- **.claude/settings.local.json 추적 상태** — git status에 계속 M으로 뜸. untrack(.gitignore) 할지 (0601 G1).
(Nick) Git 에 나중에 push 하길 
- **se-story-write 실제 호출 경로** — 축B 앱 제작이 현재 수동인지 스킬 경유인지 재확인 필요(흡수 결정의 전제).
(Nick) se-people-narrate 만 남기는게 좋지 않을까?
---

## 3. 🔧 개선할 것

1. **sync-skills.sh를 mirror 모드로** — `--delete` 옵션 또는 rsync식 미러로 바꿔 옛 디렉터리 자동 청소. (수동 rm 실수 방지)
2. **영상 web 재인코딩** — 현 mp4 NO faststart → 폰 스트리밍 시 전체 다운로드 후 재생. `-movflags +faststart` + AAC mono 112k 재인코딩(option1, ~110MB). (0601 B4)
3. **lower-third(인물명 자막)·지도(maps)** — 영상 품질 개선 백로그. (0601 B1·B2)
4. **13편 전수 리뷰** — 일관성·길이·이미지 품질 최종 점검 1회. (0601 B3)
5. **70_meta 정리** — outdated 3종 폐기/갱신 결정 후 처리.

(Nick) 모두 정리 및 확인 필요. 검토 의견 파일에 잘 정리해두기.

---

## 4. 🤔 궁금한 것 (0601 §5 Open Decisions 재게시)

1. **시작 작업** — A1(인물 배정 정본통일·즉효) / C(스킬 정리=완료) / A3(nav app·비전검증) 중 다음 첫 타?
2. **인물 추가 우선** — 옛 애니 4인 승격 vs meta 조연(thales·viete·fermat·boyle·liu-hui·playfair)?
3. **스킬 정리 시점 철학** — (이번엔 일괄 청소로 진행함) 앞으로 새 스킬은 새 콘텐츠 작업과 묶어 점진 도입할지.

---

## 5. ➕ 추가로 할 것 (백로그, 우선순위 미정)

| ID | 작업 | 디렉터리 | 스킬/에이전트 |
|---|---|---|---|
| A1 | 인물 배정 정본 통일(앱↔영상↔meta 불일치 4건: u06·u09·u11·u12) | `mid1/`, `30_content/units/` | — |
| A2 | 연결망 데이터 모델 | `30_content/` (graph SSOT) | 신규 스킬 후보 |
| A3 | navigation app | `20_packages/navigator/` + `mid1/`(or 신규) | 신규 |
| A4 | 인물이야기 감싼 설명 레이어 | story 앱/페이지 | se-story-write? |
| A5 | 단원당 인물 2~3인 풀 확장 | `30_content/people/` | se-people-pick |
| B4 | web 재인코딩(faststart) | `70_tools/`, `mid1/story/_video/` | — |
| F1 | Concept/Manim 영상 트랙(별개) | 신규 | 신규 |
| G1 | settings.local.json untrack | repo root | — |

> 불일치 4건 메모: u06 데카르트→케플러, u09 가우스→피타고라스, u11 케플러→플라톤, u12 카발리에리→아르키메데스. (영상·meta.json 기준이 정본, 옛 앱 애니는 `anim.html`로 보존 = 단원당 2인 보너스 콘텐츠.)

(Nick) 
G1 수행
A3, A2 는 이번에 수행 해보면 좋겠음.
F1 은 어떤 일인가?
A4+A1+A5+B4 한번에 처리하기. 그때 계획 정교하게 세워서 진행해야 함. 단 다른 작업 모두 완료후 시작... 새로운 영상들 제작및 app 형태 달리지는 큰 단위의 일이다.


---

## 6. 다음 액션

- Nick이 §1·§4의 결정(특히 "다음 첫 타")을 정하면 해당 Round 착수.
- 기본 추천: **A1(정본 통일)** = 즉효·저위험, 6월 학습 시작 전 정합성 확보.

---

# Round 1 — Nick 결정 반영 + 즉시 정리 실행 (2026-06-01, NCC)

## R1.1 이번 라운드에 실제 처리한 것 (commit `26cbd3c`)

| 항목 | Nick 결정 | 처리 |
|---|---|---|
| §1.1 story-write/people-narrate | 하나만 남기기 (people-narrate 주력) | ✅ **se-story-write 폐기**→`90_archive/skills_legacy/`. 인물 서사는 se-people-narrate 일원화. orchestrator·plan·review·principles·INTEGRATED_PLAN 참조 모두 갱신. |
| §1.2 audit "ncc" | 문제없음 | ✅ (이미 se-audit-*로 정리됨, 확인) |
| §2 sync-skills 비-mirror | 합리적으로 정리 | ✅ **mirror 모드(prune)**로 재작성 — SSOT에서 사라진 항목 자동 삭제. dry/real 검증(22/22). |
| §2 70_meta 3종 | 폐기 | ✅ VISION/MASTER_PLAN/ROADMAP→`90_archive/70_meta_legacy/`. (concept.md·LEARNERS·BLUEPRINTS 등은 유지.) |
| §5 G1 settings.local.json | G1 수행 + git push | ✅ `git rm --cached` + `.gitignore` 등록. 변경 push 완료. |

→ 결과 인벤토리: **22 skill + 2 agent**, 전부 kebab. SSOT↔미러 일치.

## R1.2 §1·§2 나머지 결정 (기록만, 후속 라운드에서 사용)

- **nav app 위치** = `mid1/` 통합 (확정, 일단).
- **연결망 범위** = 중1 한정 X. 중2~고1·과목 간까지 계속 연결되는 그래프 전제로 데이터 모델 설계 (확장 가능 스키마).

## R1.3 §3 개선항목 — 검토 의견 (Nick: "모두 정리·확인, 검토 의견 정리")

> 결론: §3-1(sync mirror)은 이번에 **완료**. 나머지 4개는 모두 **B-track(영상 폴리시)** 으로, Nick이 "A4+A1+A5+B4 한번에, 다른 작업 완료 후"라 한 큰 batch에 속함 → **지금은 평가만, 실행은 batch 때.**

1. **sync-skills mirror화** — ✅ 완료(R1.1).
2. **web 재인코딩(faststart)** — *검토:* 현 13편 mp4는 `+faststart` 없음 → 폰에서 "전체 다운로드 후 재생" 체감. 단 GitHub Pages + `preload="metadata"`라 실사용엔 큰 문제 아님(파일 100~200MB라면 체감 큼). **권고:** B4 batch 때 13편 일괄 `-movflags +faststart` 재mux(재인코딩 불필요, `-c copy`로 무손실·수초). 우선순위 中.
3. **lower-third(인물명 자막)·지도** — *검토:* 영상 본편은 완주됨. lower-third·지도는 "품질 향상"이지 "결손 보정"이 아님. 새 영상 재제작(A 큰 batch)과 묶을 때만 의미. **권고:** 단독 진행 X, A-batch에서 신규 영상 표준에 반영. 우선순위 下.
4. **13편 전수 리뷰** — *검토:* 일관성·길이(145~188s 편차)·이미지 품질 1회 점검은 가치 있음. 단 딸과 6월 시청 시작엔 현 상태로 충분. **권고:** A-batch 직전 1회 수행(재제작 대상 선별 목적). 우선순위 中.
5. **70_meta 정리** — ✅ outdated 3종 폐기 완료(R1.1). 잔여(SYSTEM_GUIDE.md=옛 underscore 스킬명 다수)도 outdated → 다음 청소 때 폐기 후보. 우선순위 下.

## R1.4 F1 이 뭔가? (Nick 질문)

**F1 = "Manim 개념 시각화 영상" 트랙.** 지금까지 만든 13편은 전부 **인물 스토리 영상**(수학자 이야기 + 약속 3겹). F1은 그것과 **별개 트랙**으로, *개념 자체*를 움직이는 그림으로 설명하는 영상이다 — 예: 소수의 분포가 수직선 위에 찍히는 애니, 함수 y=a/x에서 a를 바꿀 때 그래프가 변형되는 애니 (3Blue1Brown 스타일). 도구는 **Manim**(파이썬 수학 애니 라이브러리). Nick_TODO T4와 동일 항목.
- **현재 상태:** 미착수(⚪). 스킬도 없음(`se-concept-video` 후보).
- **NCC 의견:** 인물 영상과 제작 파이프라인이 완전히 다르고(나레이션·캐릭터 일관성 대신 수식·좌표 애니), 학습 효과도 별개. **지금 큰 batch(A2/A3/A4...)와 섞지 말고, 별도 시점에 단독 트랙으로 여는 것을 권고.** 우선순위 下(딸 반응 보고 결정).

## R1.5 §5-4 "어느 파일?" + wrapping 톤 결정

- **파일 위치 답:** `00_project_hub/20_plan/0601_next_phase.md` 의 §5(Open Decisions) 4번 항목. (이 0602 파일 §1.5에도 재게시돼 있음.)
- **현재 셋업 확인:** 1차 배포로 각 단원 story 페이지(`mid1/story/unitNN/index.html`)는 이미 **[뒤로]·[한 단어 chip]·[인물명]·[단원]·[영상 플레이어]** 구성 완료. 옛 애니는 `anim.html`로 보존. → Nick 말대로 "어느정도 셋업 완료" 맞음.
- **wrapping(감싼 설명) NCC 결정(합리적 기본):** A4는 이 story 페이지에 **영상 위/아래로 "맥락 설명 레이어"** 를 얇게 추가하는 일. 톤은 **딸용 짧은 감성 + 1개의 빈칸(절대원칙 5)** 혼합:
  - 영상 위: 한 줄 후킹("왜 2200년 전 사람이 소수를 셌을까?")
  - 영상 아래: ① 이 인물이 푼 문제 = 우리 단원의 무엇인지 1~2문장 ② **연결 링크**(앞/뒤 단원, 같은 인물 다른 단원 = A2 그래프) ③ 보너스: `anim.html`(2번째 인물) 링크 ④ 빈칸 1개("너라면 이 방법을 어디에 쓸까?" → 딸이 적는 자리)
  - → 단, A4는 Nick이 "A1+A5+B4와 한 batch, 다른 작업 완료 후"로 묶었으므로 **이 결정은 그 batch의 설계 입력으로만 보관**.

## R1.6 A2 + A3 — "이번에 수행" 요청 건 (설계 제안 → Nick 확인 요청)

Nick: "A3, A2 는 이번에 수행 해보면 좋겠음." 두 작업은 outward-facing(앱 구조 변경)이라, **만들기 전에 모양을 맞추는 게** 맞다(작업 방식: Q&A 우선). 아래 제안에 답 주시면 바로 빌드 착수.

**A2 = 연결망 데이터 모델 (그래프 SSOT)**
- 위치 제안: `30_content/graph/connections.json` (단일 SSOT). 빌드시 mid1로 복사.
- 스키마 제안(확장 가능 — 중1 한정 X):
  ```json
  {
    "nodes": [
      {"id":"u01","grade":"middle1","unit":1,"concept":"소인수분해","person":["에라토스테네스"],"word":"정리"},
      ...
    ],
    "edges": [
      {"from":"u01","to":"u03","type":"concept-prereq","label":"수→식 확장"},
      {"from":"u05","to":"u06","type":"same-person","label":"데카르트"},
      {"from":"u01","to":"future:중2-소수","type":"forward","label":"중2에서 다시"}
    ]
  }
  ```
  - edge type: `concept-prereq`(개념 선후), `same-person`(같은 인물), `same-era`(같은 시대), `forward`(상위 학년 예고).
- **확인 Q1:** 노드 단위는 "단원"이면 충분? 아니면 "개념"까지 잘게(예: u01 안에 소수/합성수/지수)?

**A3 = navigation app (mid1 통합)**
- 위치 제안: `mid1/map/index.html` (story/math1 와 형제). 13개 노드를 **시대 타임라인 + 개념 연결선**으로 한 화면에 보여주고, 노드 탭 → 해당 단원 앱/영상으로 이동.
- 형태 후보(택1):
  - **(가) 타임라인 띠** — 가로 시대축(고대→근대)에 인물 카드, 아래 개념 연결선. 폰 가로 스크롤. *직관적, 구현 가벼움.*
  - **(나) 노드 그래프** — 힘-방향 그래프(노드=단원, 선=연결). *연결 강조, 폰에선 복잡할 수 있음.*
  - **(다) 하이브리드** — 기본 타임라인 + "연결 보기" 토글 시 선 표시.
- **확인 Q2:** (가)/(나)/(다) 중 선호? (NCC 추천 = **(다)** — 폰 친화 + 연결성 둘 다.)
- **확인 Q3:** A2 데이터부터 만들고(반나절) → A3 앱(반나절) 순차 진행 OK? 아니면 A3 목업 먼저 보고 A2 스키마 확정?

---

# Round 2 — A2 + A3 빌드 완료 (2026-06-01, NCC 자율)

## R2.0 Nick 결정 (AskUserQuestion)
- **A3 형태 = (다) 하이브리드** (타임라인 + 연결 보기 토글)
- **A2 노드 단위 = 개념 단위** → 단원 노드 + 그 아래 개념 노드 2-레벨로 구현

## R2.1 A2 — 연결망 SSOT (commit `26cbd3c` 다음, SSOT repo push 완료)
- **파일:** `30_content/graph/connections.json` (SSOT) + 생성기 `70_tools/build_connections.py` (meta.json 13개 기반, 재현 가능).
- **107 노드:** 단원 13 + 개념 89 + 상위학년(future) 5.
- **24 엣지:** `same-person` 6(persons 교차 자동 도출) + `concept-prereq` 13(학습 선후 큐레이션) + `forward` 5(중2~중3 예고 stub).
- **링크:** 배포 mid1 기준 상대경로. 13단원 video+app 링크 26개 **전부 실파일 존재 검증 완료** (mid1 디렉터리명이 meta slug-en과 8건 불일치 → 검증본 `MID1_DIR` 고정).
- **확장성:** 중2~고1·과목 간 노드를 같은 스키마로 추가 가능. future 노드를 실단원으로 승격하면 끝.

## R2.2 A3 — 수학 지도 nav app (mid1 repo commit `2e6dfc5`, push 완료 → **live**)
- **위치:** `mid1/map/index.html` (+ `mid1/index.html`에 "🗺️ 수학 지도" 카드 추가). **live: https://jwj-nick.github.io/mid1/map/**
- **형태:** 폰 우선 **세로 타임라인** (1→13단원, era 색 점). story 페이지와 같은 다크 팔레트.
- **하이브리드 토글 3종:** [개념 흐름]🔵 / [같은 인물]🟡 / [상위 학년 →]🟣 — 켜면 각 카드에 연결 chip 표시, chip 탭 → 해당 단원으로 스크롤.
- **카드 탭:** 펼치면 그 단원 개념 목록 + [📺 인물 영상] [📱 수학 앱] 버튼.
- **검증:** JS 문법 OK(node --check) + 데이터 contract OK + 링크 26개 실존.

## R2.3 배포 메모 (중요)
- connections.json은 **SSOT=`30_content/graph/`**, **배포본=`mid1/map/connections.json`** (수동 복사). 그래프 수정 시:
  ```
  PYTHONIOENCODING=utf-8 python 70_tools/build_connections.py
  cp 30_content/graph/connections.json <mid1>/map/connections.json
  ```
  → 추후 deploy 스크립트(E.배포 hookup, #19)에 이 복사 단계 포함 권고.

## R2.4 남은 것 / Nick 확인 요청
- **폰에서 실제 시청 확인 바람** (live 링크). 타임라인 가독성·연결 chip·영상/앱 이동 잘 되는지.
- 개선 여지(차후): 시대순 정렬 토글, SVG 곡선 연결선(데스크톱), 개념 노드 간 직접 연결 시각화.
- **다음 큰 batch (A1+A4+A5+B4)** = Nick이 "다른 작업 모두 완료 후 시작"이라 한 영상 재제작·앱 형태 변경 대단위. 착수 시 별도 정교한 플랜 필요.

> 이 Round의 §R1.6 답이 오면 A2→A3 착수. (A1·A4·A5·B4 큰 batch는 그 뒤.)
