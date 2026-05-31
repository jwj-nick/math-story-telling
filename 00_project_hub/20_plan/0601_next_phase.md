<!-- 0601_next_phase.md -->

# 0601 Next Phase — 마스터 플랜 (할일 전수 + 실행 디렉터리 + 스킬/에이전트 정리)

> **작성**: 2026-05-31 (NCC, Round 0) · **방식**: chatlog 라운드 기반으로 이 파일에서 다듬는다.
> **이 파일 = 단일 정리본.** 흩어진 TODO(`TODO_video_enhancements`·`TODO_skill_architecture`·`TODO_video_deploy_encoding`)·current-plan §4·Nick_TODO·retro 시드를 한 곳에 모음.
> **전제**: 13편 영상 완주 + 1차 배포(jwj-nick.github.io/mid1, 폰 시청) + git push 완료.
> **비범위(고정)**: 수학 문제 제작(축 D) = Nick 완성 간주 → 본 플랜 제외.

---

## 0. Nick 방향 (raw, Round 0 입력 — 보존)

> "거의 새 프로젝트. 영상 더 완벽하게, 인물 더 추가… **구분법이 중요치 않음. 연관된 것 최대한 많이 배우고 연결성도 명확히 보이도록**… 인물이야기를 **감싼 설명이 앱에 보이도록**… **navigation app** 같은…"
> "기존 수학앱 사람이야기 ↔ 현재 영상 차이 정리 필요(예: u12 카발리에리→아르키메데스). 단원별 인물 2~3명 정리한 적 있음 — 제대로 확인."
> "예전 스킬(underbar)을 최신(agentskills) 스타일로 정리 필요. 최근 것과 겹치는 것/독립적인 것 구분해 수정 계획."

---

## 1. ⭐ 인물 배정 정합성 (검증 완료)

3계층: **① meta.json(정본, 2~3명/단원)** · **② 현재 영상** · **③ 옛 수학앱 story(v1)**.
**결론: 현재 영상 = meta 정본 100% 일치. 옛 수학앱만 4건 어긋남.**

| U | 단원 | meta 주연 / 조연 | ② 영상 | ③ 옛 앱 | 정합 |
|---|---|---|---|---|---|
| 01 | 소인수분해 | eratosthenes | 에라토스테네스 | 에라토스테네스 | ✅ |
| 02 | 정수와 유리수 | brahmagupta / al-khwarizmi | 브라마굽타 | 브라마굽타 | ✅ |
| 03 | 문자와 식 | al-khwarizmi / viete | 알콰리즈미 | 알콰리즈미 | ✅ |
| 04 | 일차방정식 | diophantus / al-khwarizmi | 디오판토스 | 디오판토스 | ✅ |
| 05 | 좌표와 그래프 | descartes / fermat | 데카르트 | 데카르트 | ✅ |
| 06 | 정비례와 반비례 | **kepler** / boyle | **케플러** | **데카르트** | ❌ |
| 07 | 기본도형 | euclid / thales | 유클리드 | 유클리드 | ✅ |
| 08 | 작도와 합동 | euclid / gauss | 유클리드 | 유클리드 | ✅ |
| 09 | 다각형 | **pythagoras** / kepler | **피타고라스** | **가우스** | ❌ |
| 10 | 원과 부채꼴 | archimedes / liu-hui | 아르키메데스 | 아르키메데스 | ✅ |
| 11 | 다면체와 회전체 | **plato** / kepler | **플라톤** | **케플러** | ❌ |
| 12 | 겉넓이와 부피 | **archimedes** / cavalieri | **아르키메데스** | **카발리에리** | ❌ |
| 13 | 자료의 정리·해석 | nightingale / playfair | 나이팅게일 | 나이팅게일 | ✅ |

- 옛 주연 강등/이동: u06 데카르트→(u05 단독) / u09 가우스→u08 조연 / u11 케플러→u11 조연 / u12 카발리에리→u12 조연.
- **인물 다단원 출연(연결망 뼈대)**: kepler ×3(06주·09조·11조), al-khwarizmi ×3(02조·03주·04조), archimedes ×2(10·12주), euclid ×2(07·08주).
- 기회: 1차 배포로 옛 애니가 `anim.html` 보존 → u06·09·11·12는 이미 "단원당 2인" 콘텐츠.

---

## 2. 전체 할일 마스터 인덱스 (✅완료 / 🟡부분 / ⚪미착수 / 🔒보류)

### A. 다음 단계 새 프로젝트
- ⚪ A1 인물 배정 정본 통일 (수학앱 story 표기·링크 → meta 정본; u06·09·11·12)
- ⚪ A2 연결망 데이터 모델 (인물·개념·시대·한단어 노드+엣지)
- ⚪ A3 navigation app 프로토타입 (4축 탐색 + 영상·이야기 점프)
- ⚪ A4 "감싼 설명" 레이어 (왜 이 인물·시대·개념연결·다음다리 → 앱 노출)
- ⚪ A5 인물 풀 확장 2~3인/단원 (옛 애니 4인 승격 + meta 조연 제작)

### B. 영상 개선
- ⚪ B1 로워서드 자막 (인물명·시대/나라·생몰연대)
- ⚪ B2 나라/도시 지도 + 시대상 인트로 비트
- ⚪ B3 13편 전수 재검토 (음성/자막/수학/고증/일관성/길이)
- ⚪ B4 웹 재인코딩 (H.264 High crf23 + faststart + AAC mono, ~110MB) — `TODO_video_deploy_encoding`
- ⚪ B5 YouTube 비공개+임베드 (출판/채널화 단계)
- 🔒 B6 디렉토리 재정리 season-1-ancient→season-1-algebra (Windows 잠금)

### C. 스킬·에이전트 정리  → §4 상세
- ⚪ C1 옛(underbar) 15스킬+1에이전트를 최신 kebab/spec으로
- ⚪ C2 겹치는 것 폐기/흡수 · 독립적인 것 rename
- ✅ C0 영상 9스킬 + orchestrator = 이미 kebab 졸업

### D. 배포 인프라
- ✅ D0 영상 1차 라이브 배포 (mid1/story)
- ⚪ D1 `60_deploy/` 빌드 출력 구조 + 한글→slug-en URL 변환 스크립트
- ⚪ D2 design-system 경로 dev↔deploy 매핑

### E. math 4축 잔여 (문제 제외)
- 🟡 E1 `30_content/concepts/` 13단원 개념 검수·보완
- ⚪ E2 13단원 `index/story/concepts.html` ↔ UNIT_PAGE_STANDARD audit + 옛 경로 갱신
- ⚪ E3 episode md 분리(선택) · era-palette CSS 토큰화

### F. Concept 영상 트랙 (별개)
- ⚪ F1 Manim 개념 시각화 영상 (소수 분포·함수 등) — Story 영상과 별개 (Nick_TODO T4)

### G. git/repo 정리
- ⚪ G1 `.claude/settings.local.json` 추적 해제
- 🔒 G2 season-1 rename (= B6)
- ⚪ G3 (선택·비권장) `.git` 296MB 이력 다이어트
- ⚪ G4 mid_eun 옛 repo "moved to" README (Nick 판단)

### H. 메타·진화
- ⚪ H1 옛 `10_system/70_meta/{VISION,MASTER_PLAN,ROADMAP}` 정리
- ⚪ H2 Distill 사이클: 13편 retro → principles 승격 (`se-distill-principles`)
- ✅ H0 영상 retro R1~R50 누적 (대부분 SSOT 반영)

### I. Nick 외부 의존 (Nick_TODO)
- ✅ T1 ElevenLabs / ⚪ T2 SD·MJ(Nano Banana로 대체중) / ⚪ T3 Motion Canvas / ⚪ T4 Manim(=F1) / ⚪ T5 출판채널 / ⚪ T6 ElevenLabs 유료

---

## 3. 작업별 실행 맵 (디렉터리 + 스킬/에이전트)

| 작업 | 진행 디렉터리 | 관여 스킬/에이전트 |
|---|---|---|
| A1 인물 정본 통일 | 라이브 `C:/Nick/30_Apps/jwj-nick.github.io/mid1/` (+ 소스 `30_content/units/*/meta.json`) | (수작업·스크립트) — `70_tools/` 헬퍼 |
| A2 연결망 모델 | `30_content/` 신규 `graph/` 또는 `units/*/meta.json` 확장 | 신규 `se-knowledge-graph`(후보) |
| A3 nav app | **신규 앱** — 후보: `20_packages/navigator/`(재사용 모듈) → 배포 `mid1/` 또는 별 경로 | 바닐라 HTML/JS (빌드 없음, APP_PRINCIPLES) |
| A4 감싼 설명 | `30_content/people/` + `50_channel/*/unit-*/`(1-narrative 부록) → 앱 노출 | `se-people-narrate`(확장) |
| A5 인물 추가 | `50_channel/`(영상) + `30_content/people/` | `se-people-pick` → 8-STEP(`se-video-*`) + `se-video-orchestrator` |
| B1·B2 로워서드·지도 | `50_channel/*/unit-*/` (6-motion-config·5-images) | `se-video-motion`·`se-video-image`·`se-video-render` 표준 확장 |
| B3 전수 재검토 | `50_channel/` 전체 | `se-video-*` + (영상 audit은 orchestrator 게이트) |
| B4 재인코딩 | `50_channel/*/unit-*/` → `60_deploy/channel/` 또는 mid1 | `70_tools/` ffmpeg 스크립트 (+ `se-video-compose` 표준화) |
| C 스킬 정리 | `10_system/30_skills/`·`35_agents/` → `.claude/`(sync) | `70_tools/sync-skills.sh` |
| D 배포 인프라 | `60_deploy/`·`70_tools/` | 빌드 스크립트 |
| E math 4축 | `40_grades/middle/math1/`·`30_content/concepts/` | `se-concept-review`·`se-audit-*`(kebab화 후) |
| F Concept 영상 | **신규 트랙** `11_video_gen_process/`(또는 신규) | 신규 `se-concept-video`(Manim) 후보 |
| H2 Distill | `10_system/50_insights/`·`10_principles/` | `se-distill-principles`(kebab화) |

> **새 프로젝트(nav app·연결망) 디렉터리 제안**: 재사용성 고려 `20_packages/navigator/`(엔진) + 콘텐츠는 `30_content/`(SSOT graph). 배포는 기존 `mid1/`에 통합 vs 새 경로 — **Round 결정**.

---

## 4. ⭐ 스킬·에이전트 정리 계획 (Nick flag)

### 4.1 현 인벤토리 (24 skills + 2 agents)
**🟢 kebab 최신 (영상, 유지) — 9 skills + 1 agent**
`se-people-pick` `se-people-narrate` `se-video-story` `se-video-storyboard` `se-video-narration` `se-video-image` `se-video-motion` `se-video-render` `se-video-compose` + agent `se-video-orchestrator`

**🟡 underbar 옛 (정리 대상) — 15 skills + 1 agent**
`se_story_video_v1_5` `se_story_write` `se_unit_plan` `se_concept_review` `se_math_figure` `se_math_practice` `se_math_error_note` `se_type_explorer` `se_unit_review` `se_ncc_audit_app` `se_ncc_audit_math` `se_ncc_audit_concept` `se_ncc_audit_problem` `se_ncc_audit_story` `se_distill_principles` + agent `se_agent_unit_orchestrator`

### 4.2 분류 — 최신 것과 ① 겹침 vs ② 독립

**① 겹침 (영상 kebab 파이프라인과 역할 중복 → 폐기/흡수)**
| 옛 스킬 | 겹치는 최신 | 처리 |
|---|---|---|
| `se_story_video_v1_5` | 영상 8-STEP 전체 | 🔴 **폐기 → 90_archive** (완전 대체, 무위험) |
| `se_story_write` | `se-people-narrate` (인물 서사) | 🟡 **점검 후 폐기 or 흡수** — 단원 앱 story.html 입력이 1-narrative.md로 대체 가능하면 폐기, 톤/용도 다르면 `se-story-write`(kebab)로 흡수 |
| `se_ncc_audit_story` | 영상=orchestrator 게이트가 커버 | 🟢 **유지하되 kebab화** — 앱 story.html 검수엔 독립 가치. `se-audit-story` |

**② 독립 / 상관없음 (영상과 무관, math 4축·meta → 단순 최신화: rename + spec 점검)**
| 옛 스킬 | → kebab | 비고 |
|---|---|---|
| `se_unit_plan` | `se-unit-plan` | 단원 초기화 |
| `se_concept_review` | `se-concept-review` | 개념 검수 (E1) |
| `se_math_figure` | `se-math-figure` | 그래프 렌더 (영상 X, 앱·문제용) |
| `se_math_practice` | `se-math-practice` | 문제(=완성간주, 스킬은 보존) |
| `se_math_error_note` | `se-math-error-note` | 오답노트 |
| `se_type_explorer` | `se-type-explorer` | 유형 심화 |
| `se_unit_review` | `se-unit-review` | 단원 검토 |
| `se_ncc_audit_app` | `se-audit-app` | 앱 품질 |
| `se_ncc_audit_math` | `se-audit-math` | 수학 정확성 |
| `se_ncc_audit_concept` | `se-audit-concept` | 개념 수준 |
| `se_ncc_audit_problem` | `se-audit-problem` | 문제 커버리지 |
| `se_distill_principles` | `se-distill-principles` | 회고→원칙 (H2) |
| agent `se_agent_unit_orchestrator` | `se-unit-orchestrator` | 4축 파이프라인. 내부 스킬 참조도 kebab 갱신 |

### 4.3 "최신 스타일"의 정의 (rename만이 아님)
1. 디렉터리·`name:` = kebab-case (agentskills.io spec, [[reference-agentskills-spec]])
2. frontmatter: `description`에 트리거 문구 + 입력/동작 요약 (영상 스킬 포맷 기준)
3. body: 입력→동작(단계)→출력→평가기준→QnA시드 구조 통일 (영상 스킬이 레퍼런스)
4. cross-link `[[...]]`·경로 `../se_x`→`../se-x` 갱신
5. `sync-skills.sh` 미러 + 호출 등록 확인

### 4.4 마이그레이션 절차 (스킬 1개당) · 순서
절차: ① dir rename → ② frontmatter kebab+spec → ③ 내부 링크/경로 → ④ 참조처(agent·CLAUDE.md·workflow) → ⑤ sync-skills.sh → ⑥ 호출 테스트.
권장 순서:
1. `se_story_video_v1_5` → 아카이브 (즉시·무위험)
2. 결정 A: `se_story_write` 점검 후 폐기/흡수
3. audit 5종 일괄 kebab (`se-audit-*`) — 형태 동일, 기계적
4. math 6종 kebab (`se-unit-plan`·`se-concept-review`·`se-math-*`·`se-type-explorer`·`se-unit-review`)
5. `se-distill-principles`
6. agent `se_agent_unit_orchestrator`→`se-unit-orchestrator` (내부 스킬 참조 일괄 kebab)
7. CLAUDE.md 스킬표·agent표 전면 갱신 + sync

> ⚠️ 옛 스킬명을 참조하는 곳: CLAUDE.md(스킬표), `se_agent_unit_orchestrator`(내부), chatlog(역사=보존). rename 시 전향적 참조만 갱신.

---

## 5. Open Decisions (Round 1)
1. **시작 작업**: A1(정본통일·즉효) / C(스킬 정리·기반청소) / A3(nav app·비전검증) 중 첫 타?
2. **nav app 위치**: `mid1/` 통합 vs 새 앱/새 배포?
3. **연결망 범위**: 중1 13단원만 vs 중2~고1 골격까지?
4. **감싼 설명 톤**: 딸용 짧은 감성 vs 참고형? (빈칸 남길지 — 절대원칙 5)
5. **인물 추가 우선**: 옛 애니 4인 승격 vs meta 조연(thales·viete·fermat·boyle·liu-hui·playfair)?
6. **스킬 정리 시점**: 새 콘텐츠 작업과 묶어 점진 vs 지금 일괄 청소?

---

## 6. 비범위 / 고정
- 수학 문제(축 D) = 완성 간주, 손대지 않음.
- 1차 배포물(mid1/story) 라이브 — 변경 시 폰 시청 가능 유지.
- 기록: 본 파일 `# Round N` 누적 (CLAUDE.md chatlog 관행).
- 흡수된 옛 TODO: `TODO_video_enhancements`(→B1·2·3·6), `TODO_skill_architecture`(→C/§4), `TODO_video_deploy_encoding`(→B4·5), current-plan §4(→D·E·H), Nick_TODO(→I).
