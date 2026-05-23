<!-- INTEGRATED_PLAN.md -->

# Integrated Plan — 영상 R&D Sub-Project

> 4 reference (R0+R1 / baseline_unit01 / current_plan_C / R6 quality_essence) 통합 plan.
> compact 직후 (2026-05-23) 작성. VISION/GOALS 의 상위 통합 view.
> 본 문서 = sub-project 의 "지금 어디에 있는가 + 어디로 가는가" 단일 진입점.

---

## §0. TL;DR

- 본 sub-project = **영상 quality R&D**. SSOT·산출물은 외부 (10_system / 50_channel) — 본 폴더는 R&D 워크플로우·실험·평가만.
- scope: **시즌1 5편** (D-004 β 후보) 이지만 R6 통찰로 **옵션 δ 등장** — 5편 = Cornerstone 3 + 표준 2.
- 즉시 가능 sprint: **NCC 자율 4건** (R1.9) — D-004~019 결정 기다리지 않고 진행.
- 핵심 결정 1건: **D-004 (scope) — β vs δ**. 나머지 모든 결정이 여기 의존.
- 시간 모델: β = 3~5주 (표준만). **δ = ~235h = 4개월 주당 15h 현실적**.

---

## §1. 4 Reference 통합 — 한 표

| 자료 | 무엇을 추가했나 | 본 plan 에 반영된 결과 |
|---|---|---|
| **01_R0_R1_summary** | unit-01 v1.5 baseline 정밀 (SSML/이미지/config) + 13단원 격차 5축 D1-D5 + R1 zoom out (시즌1=5편 비전 / 7 갭 / 진화 메커니즘) + NCC 자율 4건 | scope = β 시즌1 5편. D-001~013 결정 체계. NCC 자율 sprint 0 |
| **02_baseline_unit01** | 9 산출물 인벤토리 + SSML 패턴 + 6 장면 / 캐릭터 시트 / motion / 메트릭 후보 | `30_pipeline/*/README.md` 표준. v1.6 시드의 출발점 |
| **03_current_plan_C** | math-story-telling 전체 큰 그림에서의 sub-project 위치 (Phase 0-A 중) | 큰 그림 entry point. 시즌1 5편 = "옛 비전 + 옛 트랙 정렬" |
| **04_R6_quality_essence** ⭐ | **Cornerstone 차등 전략 + 영상 5 quality 레버 [A]~[E] + 7 원칙 P1~P7 + 시간 모델 380h** | scope 옵션 δ 신설. D-014~019 신설. 운영 원칙 7개. v1.6 시드에 quality 절 추가 |

R6 가 sub-project plan 골격을 본질적으로 바꿈:
- **이전**: "13편 또는 5편을 v1.5 표준으로 평준화 빌드 + 도구 도입 (ElevenLabs·MJ)"
- **이후**: "5편 안에서도 Cornerstone 3 + 표준 2 차등. Cornerstone 에 quality 레버 5종 + Polish Loop 운영"

→ "표준화" 라는 단어가 **두 층**으로 분리됨: ① 표준 단원의 평균선 (v1.5 → v1.6 표준) / ② Cornerstone 단원의 피크 (quality 레버).

---

## §2. math-story-telling 큰 그림에서의 위치

```
[~05-20] 13단원 앱 완성 + 영상 v1.5 unit-01 완성
[05-21~22] repo 통합 + 마이그 + 수학 챕터 표준 정의
[05-23 ← 현재] C R0+R1+R6 = 영상 R&D 본격 시작 / 영상 1/5 완성
```

본 sub-project 가 책임지는 4축 매핑:
- **축 B (흥미·서사)** ← 영상의 직접 책임 영역
- **축 A (개념)** 와 cross-link — Set-piece [A] 가 개념 시각화의 정점
- **축 C (수학언어)** 무관 (외부 트랙)
- **축 D (문제)** 무관

상위 우선순위 ("앱=백본 / 영상=보조" — 260516 meta planning):
- 앱 트랙이 큰 그림의 백본. 영상은 *몰입·흥미*의 보조 강화.
- 본 sub-project 시간 배분 = math-story-telling 전체 시간의 30~50% 정도가 한계 (다른 트랙·study 5개 고려).

---

## §3. Cornerstone 모델 — R6 핵심 신 frame

### 3.1 Cornerstone 단원 후보 (R6 §1)

시즌1 5편 안에서:

| Ep | 단원 | 인물 | 분류 후보 | 사유 |
|---|---|---|---|---|
| Ep1 | 01 소인수분해 | 에라토스테네스 | **Cornerstone** | 첫 단원 = 시리즈 첫인상. 이미 v1.5 baseline 완성 → 5 레버 적용 실험 최적 |
| Ep2 | 02 정수와 유리수 | 브라마굽타 | 표준 | 시즌1 두 번째. v1.6 표준 검증 파일럿 적합 |
| Ep3 | 03 문자와 식 | 알콰리즈미 | **Cornerstone (후보 1)** | 추상화 첫 도약. 대수의 어원 |
| Ep4 | 04 일차방정식 | 디오판토스 | **Cornerstone (후보 2)** | 미지수의 첫 등장. 후보 1 과 택일 |
| Ep5 | 05 좌표와 그래프 | 데카르트 | **Cornerstone** | 딸 결정적 약점 지점 (y=a/x 변환). 가장 추상적 |

→ **결정 필요**: 03 vs 04 (D-014 의 하위 결정).
→ **NCC 추천**: 04 디오판토스 = Cornerstone (방정식 = 중1 시험 가장 큰 비중).

### 3.2 Cornerstone 5 레버 적용 매트릭스

| 레버 | Cornerstone (3편) | 표준 (2편) | 외부 영향 |
|---|---|---|---|
| **[A] Set-piece 30s** | ✅ 각 단원 1개 (S4 결정적 순간) | ❌ | `30_pipeline/4_motion/` + `40_experiments/exp-006-set-piece-01/` |
| **[B] ElevenLabs** | ✅ 5 voice 매핑 | edge-tts 유지 | `30_pipeline/2_narration/` + `40_experiments/exp-001-elevenlabs/`. Nick_TODO T1 |
| **[C] BGM + SFX** | ✅ era-팔레트 ambient + sting | ✅ ambient 만 | `30_pipeline/4_motion/` + `40_experiments/exp-007-bgm-sfx/` |
| **[D] 일러스트 (외주)** | ✅ 인물 한 장 외주 | ❌ AI 만 | `30_pipeline/3_image/` + Nick_TODO 신규 |
| **[E] Sub-3min 보조** | ✅ 단원당 1~3개 | △ 단원당 0~1개 | `30_pipeline/` 신 stage 또는 별도. R6 §2.2 [E] |

### 3.3 표준 단원의 책무 (피크 X / 평균선 ↑)

- v1.6 standard (v1.5 → 캐릭터 시트 분리 + length dry run + 5인 voice 매핑 + 디렉토리 이중 트리) 만 적용
- [C] BGM ambient 만 (sting 없음) — 전 단원 베이스라인 ↑
- [E] Sub-3min 1개 (단원 결론 30s) — 인스타·공유용
- 외주·set-piece·ElevenLabs 없음

---

## §4. 결정 흐름 (D-001 ~ D-019)

```
D-001 ✅ sub-project 분리 (top-level 11_)
D-002 ✅ 풀세팅 9
D-003 ✅ 발췌 방식
─────────────────── (위 3건 확정)
D-004 ⏳ scope — β (평준화 5편) vs δ (Cornerstone 차등 3+2) ⭐ 모든 후속 결정 의존
D-013 ⏳ 진화 메커니즘 본격화 시점 (NCC 권장 = 지금)
─────────────────── (위 2건 = compact 후 첫 결정)
D-014 ⏳ Cornerstone 단원 확정 (01 / 03 or 04 / 05)
D-005 ⏳ TTS 도구 — ElevenLabs (Cornerstone 3편만 NCC 권장)
D-015 ⏳ Set-piece [A] 채택 시점 (Cornerstone 01 즉시 NCC 권장)
D-016 ⏳ BGM·SFX [C] 채택 시점 (Cornerstone 01 즉시 NCC 권장)
─────────────────── (위 4건 = δ 선택 시 즉시 결정)
D-006 ⏳ AI 이미지 도구 — Midjourney --cref (Nick_TODO T2)
D-017 ⏳ 일러스트 외주 [D] 채택 (Cornerstone 3편만 시즌1 후반)
D-018 ⏳ Sub-3min [E] 도입 (전 단원 권장)
D-007 ⏳ 이중 트리 이동 시점 (지금 권장)
D-008 ⏳ 시드 자동 생성 vs 단원별 (시즌1 4편 시드 + unit-02 파일럿)
D-009 ⏳ se_ncc_audit_video 신설 (R2 후 결정)
D-010 ⏳ 4편 분할 구조 (1단원 1편)
D-011 ⏳ 창의 제안 8개 (시즌1 후 검토 = 지금 0개)
D-012 ⏳ 옛 70_meta 처리 (B = 90_archive 이동 + 신규)
D-019 ⏳ Polish Loop + manifesto.md 운영 (R6 P1·P6)
```

→ **결정 의존 그래프**:
- D-004 → D-014 → (D-005, D-015, D-016, D-017, D-018)
- D-013 → (D-019, NCC 자율 4건)
- 나머지 = D-004 와 독립

---

## §5. NCC 자율 sprint 0 (Nick 응답 없이 가능)

R1.9 자율 4건 + R6 통합 후 +1.

### 5.1 자율 진행 5건

1. **insights 미반영 2건** → `STORY_VIDEO_v1_5.md` 반영 + `[x]` 표시
   - 캐릭터 시트 분리 (image_prompts.md 공통 묘사)
   - length dry run 분기 (TTS 1회 합성 → 95~120s 검증)
   - 위치: `../../10_system/10_principles/STORY_VIDEO_v1_5.md` + `../../10_system/50_insights/_index.md`
2. **`se_story_video_v1_5` skill 점검** (현 SKILL.md 격차 audit)
   - 위치: `../../.claude/skills/se_story_video_v1_5/SKILL.md` + SSOT 비교
3. **`STORY_VIDEO_v1_5.md` 4개 항목 갱신**
   - §2.2 캐릭터 시트 분리 / §4 length dry run / §3.1 voice 매핑 / §7 디렉토리 이중 트리
4. **옛 `10_system/70_meta/` 정합성 audit 보고서** (이동은 D-012 후)
5. ⭐ **R6 7 원칙 (P1~P7) 운영화 시드 작성** — `20_principles/POLISH_LOOP_OPERATING.md` (P1·P2·P4·P6 본 sub-project 채택 부분만)

→ Anthropic API rate limit (5h sliding window) 고려해 한 세션에 2~3건 처리. compact 직후 첫 세션 = R0 charter writing 에 통합.

### 5.2 자율 진행 의 안전 한계

- SSOT (`10_system/10_principles/`) 수정 = 외부 영향 큼. 변경 전 chatlog 또는 본 plan 에 한 줄 기록 후 진행.
- skill SSOT 수정 = `70_tools/sync-skills.sh` mirror 갱신 필수.
- **Cornerstone 단원 확정 (D-014) 은 Nick 결정 영역** — NCC 자율 X.

---

## §6. 시간 모델

R6 §6 + 시즌1 5편 한정.

### 6.1 옵션별 총 시간

| 옵션 | 구성 | 단원당 | 총 시간 |
|---|---|---|---|
| **β** (평준화) | v1.5 표준 × 5 | ~15h | **~75h** |
| **δ** (Cornerstone 차등) | 표준 × 2 (30h) + Cornerstone × 3 (180h) + Polish (25h) | 15h / 60h | **~235h** |
| α 참고 (13편) | — | — | ~380h |

### 6.2 δ 의 일정 시나리오

| 주당 | 기간 |
|---|---|
| 50h | 5주 (집중) |
| 30h | 8주 (2개월) |
| **15h** | **16주 (4개월) ← 현실적** |

Nick 본업·다른 5 study (UVM·NVDLA·MIT·앱 등) 고려 시 **주당 15h × 16주 = 4개월** 권장.
→ 시즌1 완성 목표 = **2026-09** (2026-05 시작 가정).

### 6.3 마일스톤

- **M1 (~2026-06-15, 3주)**: NCC 자율 5건 완료 + STORY_VIDEO_v1_6 확정 + unit-02 파일럿 (표준)
- **M2 (~2026-07-15, 7주)**: Cornerstone 01 재빌드 ([A]+[C] 적용) + Cornerstone 결정 확정
- **M3 (~2026-08-15, 12주)**: Cornerstone 04 or 03 빌드 + 표준 unit-04 빌드
- **M4 (~2026-09-15, 16주)**: Cornerstone 05 빌드 + 시즌1 종합 회고 + 시즌2 진입 결정

---

## §7. 다음 행동 분기 (compact 후 첫 세션)

### 7.1 분기 A — Nick 결정 우선 (최단)

순서: D-013 → D-004 → D-014.

1. D-013 진화 메커니즘 본격화 → **지금** (NCC 권장)
2. D-004 scope → **δ** (Cornerstone 차등, NCC 권장) or β (평준화)
3. D-014 Cornerstone 단원 확정 (δ 선택 시) → 01 + 04 + 05 (NCC 추천) or 01 + 03 + 05

이후 D-005·D-015·D-016 즉시 결정 가능. NCC 자율 sprint 시작.

### 7.2 분기 B — NCC 자율 우선 (현재 권장)

D-013 만 결정 (지금 권장 = ✅) → 자율 5건 (§5.1) 진행 → Nick 결정 항목은 chatlog R3 로 따로.

이유: D-004·D-014 는 본질 결정이라 Nick 의 충분한 숙고 필요. NCC 가 평행 진행해 토대 만듦.

→ **NCC 추천 = B**. compact 후 첫 세션 = "NCC 자율 sprint 0" + "Nick 결정 R3 라운드 안건 상정".

### 7.3 분기 C — 단원 빌드 즉시 진행 (지양)

unit-02 파일럿 즉시 빌드. 표준 검증.
→ **지양**: 진화 메커니즘 (v1.5 → v1.6) 갱신 전 빌드 = polish 기회 손실.

---

## §8. 본 plan 의 변경 조건

다음이 발생하면 본 plan 재정렬:
- D-004 결정 (β vs δ)
- D-014 결정 (Cornerstone 단원)
- R6 의 Q1~Q6 Nick 응답 (외부 chatlog `260523_R6_quality_essence.md`)
- 새로운 reference 발견 (예: 폐기 50_channel/_archive/v1/ 회고 자료, 옛 70_meta 정밀 검토 후)

---

## §9. 참조

- `../10_reference/_origin.md` — 외부 자료 path 인덱스
- `../10_reference/01_R0_R1_summary.md`
- `../10_reference/02_baseline_unit01.md`
- `../10_reference/03_current_plan_C.md`
- `../10_reference/04_R6_quality_essence.md` ⭐
- `./VISION.md` / `./GOALS.md` / `./DECISIONS.md`
- 외부 chatlog: `../../00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` (R0·R1 / 향후 R2 통합 / R3 결정 라운드)
- 외부 chatlog: `C:/Kids/00_LearningSystem/00_chatlog/260523_R6_quality_essence.md` ⚠️ 외부

---

## 변경 이력

- 2026-05-23 (compact 후): 신설. 4 reference 통합. R6 통찰 통합 plan 골격 확정.
