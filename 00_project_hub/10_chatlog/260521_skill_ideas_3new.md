<!-- 260521_skill_ideas_3new.md -->

# 신규 Skill 3종 아이디어 정리

> Nick 요청 (2026-05-21):
> "처음 시나리오 작성(사실검증), 아이들 관심있도록 업그레이드, 고급 그림 프롬프트 생성 에 대한 스킬도 생각해보고 아이디어 구체적으로 정리하기"
>
> Round 1 — NCC 정리·권고. 결정은 Nick. 확정 항목은 추후 `mathtelling/system/proposals/<skill>.md`로 승격.

---

## Round 1 — 큰 그림 + 3개 skill 명세

### 1. v1.5 파이프라인 확장 위치

```
[0] scenario_research.md      ← /se_scenario_research  (NEW, 사실 검증)
       ↓
[1] storyboard_v1_5.md         (기존)
       ↓
[2] narration_v1_5.txt 초안    (기존)
       ↓
[2a] narration_v1_5.txt 강화   ← /se_narration_engage  (NEW, 후처리)
       ↓
[3] image_prompts.md           ← /se_image_prompts_pro (UPGRADE)
       ↓
[4]~[9] (기존)
```

기존 `/se_story_write`, `/se_story_video_v1_5`는 그대로. 새 skill 3개가 그 사이/위에 끼워짐.

---

## 2. `/se_scenario_research` — 시나리오 사실 검증

### 목적
- 인물·시대·일화의 **역사적 사실성** 확보
- 수학적 주장의 정확성 (예: 7.2도, 1% 오차)

### 인자
```
/se_scenario_research unit-01 에라토스테네스
/se_scenario_research unit-02 브라마굽타 --depth deep
```

### Phase 절차

| Phase | 동작 | 도구 |
|---|---|---|
| A. 1차 소스 | Wikipedia (한/영), Britannica, 학술 사이트 | WebFetch, WebSearch |
| B. 사실 분류 | ✅ 확정 / 🟡 강한 정설 / 🟠 약한 정설 / ⚠️ 전설 | NCC 판단 |
| C. Timeline | 인물 생애·작품·시대 사건 정렬 | MD 표 |
| D. 수학 정밀 | 수치·증명·당시 표기법 검증 | Wolfram Alpha MCP |
| E. Citation | 각 주장 옆 출처 링크 | URL 포함 .md |

### 산출물
```
channel/season-X/unit-NN/scenario_research.md
├── ## 인물 사실 (✅/🟡/🟠/⚠️ 태그)
├── ## Timeline
├── ## 수학적 사실 검증
├── ## 시대 디테일 (의상·도시·도구)
└── ## 출처
```

### `/se_story_write`와의 연계
- 현재: `se_story_write`가 곧장 스토리 작성 → 사실/픽션 혼재 위험
- 신규: `se_scenario_research` → `se_story_write`가 이걸 읽고 작성. "✅"만 사실로 쓰고 "⚠️"은 명시적 픽션화.

### audit
- `/se_ncc_audit_story`에 "각 주장이 scenario_research.md에 출처 있나" 체크 추가

### 위치
- SSOT: `mathtelling/system/skills/se_scenario_research/`
- 참조: `system/principles/STORY_VIDEO_v1_5.md`, `system/context/PERSON_CAST.md` (예정)

---

## 3. `/se_narration_engage` — 흥미 후크 강화

### 목적
- narration이 "이야기 톤"은 좋지만 **흥미 hook이 약함**
- 아이가 "왜 이걸 들어야 해?"라는 질문에 첫 10초에 답해야 함
- 후처리 skill — 이미 작성된 narration을 받아 강화

### 인자
```
/se_narration_engage unit-01
/se_narration_engage unit-01 --hook-strength high
```

### Engagement Toolkit (7기법)

| 기법 | 무엇 | 예시 |
|---|---|---|
| Hook (첫 5s) | 청자를 끌어들이는 질문/긴장/충격 | "막대기 하나로 지구를 잴 수 있을까?" |
| Curiosity gap | 결론을 미루고 호기심 유발 | "그가 왜 '베타'라 불렸는지, 이상하게도..." |
| Personal connection | 청자와 인물을 연결 | "여러분이 만약 그 자리에 있었다면..." |
| Reversal | 의외성·반전 | "근데 말이에요. 진짜 놀라운 건 그게 아니에요." |
| Concrete > abstract | 추상어를 구체 이미지로 | "큰 도시" → "별이 박힌 항구" |
| Stakes | 인물이 무엇을 잃을 수 있었나 | "실패하면 평생 '베타'로 남을 운명" |
| Emotional arc | 잔잔→긴장→해소 곡선 | S3 잔잔 / S4 긴장 / S5 해소 |

### Phase 절차

| Phase | 동작 |
|---|---|
| A. 진단 | 현재 narration을 7기법으로 채점 (각 0~3점). 약한 곳 표시 |
| B. 후보 생성 | 약한 곳마다 3개 대안 제시 |
| C. Nick 선택 | 채팅으로 A/B/C 또는 자유 수정 |
| D. 통합 + 길이 dry run | 적용 + edge-tts로 길이 재확인 (95~120s 유지) |
| E. diff 보고 | 변경 전/후 비교 |

### 산출물
- `narration_v1_5.txt` 갱신 (원본은 `.v0.txt`로 백업)
- `narration_engage_report.md` — 점수표 + 변경 이유

### 갈래: Hook 강도

| 모드 | 톤 | 권장 |
|---|---|---|
| `subtle` (기본) | 잔잔한 호기심 자극 | 학습 영상 — 톤 깨지지 않음 |
| `medium` | 명확한 hook 문장 | 신규 단원 도입 |
| `high` | 강한 충격·반전 | TikTok 식. 우리는 X |

### 위치
- SSOT: `mathtelling/system/skills/se_narration_engage/`
- 참조: `system/context/TONE_GUIDE.md`, `system/principles/STORY_VIDEO_v1_5.md`
- 신규 context: `system/context/ENGAGEMENT_TOOLKIT.md` (7기법 카탈로그)

---

## 4. `/se_image_prompts_pro` — 고급 이미지 프롬프트

### 목적
- 캐릭터 일관성·시대 정확성·도구별 변환 자동화
- Unit 01에서 본 문제 해결:
  - 5장 프롬프트에 캐릭터 묘사 5번 반복 → **캐릭터 시트** 1회만
  - 시대 키워드 매번 떠올림 → ERA_PALETTES + 시대 toolkit 자동
  - 도구마다 문법 다름 → multi-target 출력

### 인자
```
/se_image_prompts_pro unit-01
/se_image_prompts_pro unit-01 --target midjourney
/se_image_prompts_pro unit-01 --target sd-flux
/se_image_prompts_pro unit-01 --target claude-image  (기본)
```

### Phase 절차

| Phase | 동작 |
|---|---|
| A. Character Sheet | 인물 외모 invariants 1회 작성 (얼굴·나이·복장·머리·자세) |
| B. Era Toolkit 로드 | `system/context/ERA_PALETTES.md`에서 시각 키워드 |
| C. Shot List | 6장면 → 컷 명세 (medium/wide/close-up, 카메라 각도, 라이트) |
| D. Prompt 합성 | (character sheet + era toolkit + shot 명세 + 부정 프롬프트) |
| E. Tool-specific 변환 | DALL-E (자연어) / MJ (키워드+파라미터) / SD (positive/negative + LoRA) |
| F. Audit | 시대 anachronism · 글자 포함 · 인물 invariants 일치 자동 체크 |

### 새 image_prompts.md 양식

```markdown
## 캐릭터 시트 (인물: 에라토스테네스)
- 나이: ~70세 elderly
- 외모: kind weathered face, white-grey beard
- 복장: Hellenistic chiton + himation, off-white linen
- (이하 invariants...)

## Shot 1 — S2 알렉산드리아 풍경
- Type: wide establishing shot
- Time: golden hour
- Mood: 장엄함 + 따뜻함
- Negative space: 좌측 하단 (자막용)

### Target: claude-image
> {full English prompt — character sheet 없음, 풍경 only}

### Target: midjourney
> {prompt} --ar 16:9 --style raw --v 6

### Target: sd-flux
positive: {...}
negative: {text, watermark, modern clothing, ...}
LoRA: ancient-architecture-v2 (weight 0.7)
```

### 갈래: 이미지 도구

| Target | 상황 | 비고 |
|---|---|---|
| `claude-image` (기본) | 현재 Nick 워크플로우 | Claude/ChatGPT 채팅에 복붙 |
| `midjourney` | Nick MJ 유료화 후 (Nick_TODO T2-B) | 더 시네마틱 |
| `sd-flux` | Nick SD 로컬 셋업 후 (T2-A) | 무한 생성 + LoRA |

### 위치
- SSOT: `mathtelling/system/skills/se_image_prompts_pro/`
- 참조: `system/context/ERA_PALETTES.md`, `system/principles/STORY_VIDEO_v1_5.md §2`
- 신규 context: `system/context/CHARACTER_SHEETS.md` (단원별 캐릭터 invariants 누적)

---

## 5. 3개 skill 의존 그래프

```
ERA_PALETTES.md ─────────────────┐
                                  ├─→ se_image_prompts_pro
CHARACTER_SHEETS.md ─────────────┤
TONE_GUIDE.md ──→ se_narration_engage
ENGAGEMENT_TOOLKIT.md ──→ se_narration_engage
PERSON_CAST.md ──→ se_scenario_research
```

신규 system/ 파일 3개 필요:
- `context/PERSON_CAST.md` — 13단원 인물 캐스팅·기본 사실
- `context/CHARACTER_SHEETS.md` — 단원별 캐릭터 invariants 누적
- `context/ENGAGEMENT_TOOLKIT.md` — 7기법 카탈로그 + 예시

---

## 6. 작업 우선순위 추천

| 순서 | Skill | 이유 |
|---|---|---|
| **1** | `/se_image_prompts_pro` | Unit 01 회고에서 가장 명확한 통증. 즉시 효과 큼. |
| **2** | `/se_narration_engage` | 톤은 있지만 hook 약함. 다음 영상 품질 도약. |
| **3** | `/se_scenario_research` | 깊지만 가장 무거운 작업. Unit 02 시작 전 한 번 만들면 됨. |

---

## Nick 결정 대기

- [ ] **D1**: 3개 모두 만들기 vs 1개씩? 만들면 어느 순서? (NCC 추천: 1→2→3)
- [ ] **D2**: `/se_image_prompts_pro`가 기존 (있다면) 대체 vs 신규?
- [ ] **D3**: `se_narration_engage`는 별도 skill vs `se_story_video_v1_5` Phase B에 흡수?
- [ ] **D4**: `se_scenario_research`는 `se_story_write` 앞단 vs `se_story_write` 자체를 강화?

각 D에 답하면 Round 2 — 그 skill부터 1차 명세 (`system/proposals/<name>.md`)로 incubation.

---

## 변경 이력
- R1 (2026-05-21): NCC 3개 skill 명세 + 의존 그래프 + 우선순위. proposals/ 공간 신설 제안.
