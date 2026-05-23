<!-- 04_R6_quality_essence.md -->

# 발췌 — `260523_R6_quality_essence.md` (Quality / Essence)

- **원본**: `C:/Kids/00_LearningSystem/00_chatlog/260523_R6_quality_essence.md`
  - ⚠️ math-story-telling 외부 위치 (옛 00_LearningSystem 잔존). 본 sub-project 갱신 시 그쪽도 갱신 검토 (D-012 와 함께).
- **발췌 일자**: 2026-05-23 (compact 직후)
- **발췌 범위**: 영상 R&D 직접 관련 §1, §2, §4.3, §5 전체 / §3, §4.2, §6 요약 (앱·콘텐츠 영역 — 외부 트랙)

---

## 1. 자동화 vs 깊이 — Cornerstone 단원 전략 ⭐ 신 frame

핵심 명제:
- **자동화**: 13단원 × 4축 = 52 산출물의 **평균선**을 끌어올림
- **깊이**: 일부 산출물의 **피크**를 끌어올림 — "와 이거 진짜다"
- 둘을 같은 단원에 똑같이 부으면 둘 다 못 함

→ **Cornerstone 단원 전략**: 13개 중 2~3개에 10배 투자. 나머지는 v1.5 표준으로 빠르게.

### Cornerstone 후보 (시즌1 안에서)

| 단원 | 인물 | Cornerstone 사유 |
|---|---|---|
| **01** 소인수분해 | 에라토스테네스 | 첫 단원 = 시리즈 첫인상 (이미 v1.5 완성) |
| **03 or 04** 문자·식 / 일차방정식 | 알콰리즈미 / 디오판토스 | 중1 수학의 추상화 첫 도약 |
| **05** 좌표·그래프 | 데카르트 | 가장 추상적, 딸 결정적 약점 지점 (LEARNER_PROFILE: y=a/x 변환) |

→ 시즌1 5편 = **Cornerstone 3편 + 표준 2편** (02 브라마굽타, 04 디오판토스 or 03 알콰리즈미 중 비 Cornerstone).

**본 sub-project 영향**: D-004 scope 옵션 δ 신설 — β + Cornerstone 차등.

---

## 2. 영상 Quality — v1.5 천장과 그 너머

### 2.1 v1.5 현재 한계 (정직 진단)

- **AI 이미지 5장** = 고품질 stock 사진 느낌. 13편 누적 시 "또 비슷한 풍경/인물 톤" 위험
- **edge-tts 다정한 어조 = 90%** 라고 했지만 — S4(결정적 순간) 감정 곡선 평이
- **BGM·SFX 무음** → "영상이라기보단 슬라이드 + 나레이션"
- **모션 = ken burns + fade**가 거의 전부. 화면이 결국 정적

### 2.2 5 quality 레버 [A]~[E] (effort 큰 순) ⭐

| 레버 | 무엇 | 적용 | Effort | sub-project 배치 |
|---|---|---|---|---|
| **[A] Set-piece 30s** | 단원당 "꼭 봐야 하는 30초" 동적 다이어그램 (JSXGraph/D3.js). 에라토스테네스 → S4 30초: 막대기+그림자+시에네+곡률+7.2°=1/50바퀴+둘레 풀려나옴 | Cornerstone 단원만 | 큼 | `30_pipeline/4_motion/` + `40_experiments/exp-006-set-piece-01/` |
| **[B] ElevenLabs (감정 곡선)** | "비용/품질" 이 아니라 "결정적 순간 떨림·여운". S3 calm / S4 hushed-excited / S6 gentle-decay | Cornerstone 3편만. 표준 단원은 edge-tts | 중 | `30_pipeline/2_narration/` + `40_experiments/exp-001-elevenlabs/` |
| **[C] BGM + SFX** | era-ancient 팔레트마다 1곡 ambient (4시대=4곡, CC0). SFX 결정적 순간 1회 sting (chime/drum). 단원당 1~2회. 효과: "강의"→"다큐멘터리" | 전 단원 (자동화 가능 영역) | 중 | `30_pipeline/4_motion/` + `40_experiments/exp-007-bgm-sfx/` |
| **[D] 인물 일러스트 (손그림 보완)** | 캐릭터 시트 SSOT 는 *일관성* 해결, *quality* 안 됨. Cornerstone 3단원 인물 한 장만 외주 (5~10만원). AI = 풍경·도구·환경. 사람 = 인물 | Cornerstone 3편만 | 중 (외주) | `30_pipeline/3_image/` + Nick_TODO |
| **[E] Sub-3min Series** | 본 영상 115s 외에 30~60s "한 컷 영상". "7.2°가 1/50바퀴인 이유 30초", "지구 둘레 4만km 풀려나가는 30초". 단원당 1~3개. 인스타/쇼츠. **딸이 "다시 보고 싶은 부분"만 끊어서** | 전 단원 (본 영상보다 *쉬움*) | 작음~중 | `30_pipeline/` 신 stage 또는 별도 산출물 종류 |

**Cornerstone 01 (이미 v1.5 존재) 즉시 시도 권장**: [A] Set-piece 30s + [C] BGM/SFX.

### 2.3 STORY_VIDEO_v1_5 → v1.6 시드에 추가될 절

- §3.2 [E] Sub-3min series 정의 + 산출물 종류 +1
- §4.7 BGM/SFX 표준 (era-팔레트별 ambient 1곡 + sting 위치)
- §2.3 Set-piece 30s 권장 (Cornerstone 단원만)

---

## 3. App Quality + Content Quality — 외부 트랙 (요약)

### 3.1 App Quality (외부 트랙 — 본 sub-project 영역 아님)

`40_grades/middle/math1/NN_*/{index,story,concepts}.html` 영역.

가장 큰 ROI 3가지:
1. **Typography + Spacing 토큰화** (Pretendard / 본문 16~18px / 행간 1.7) — 1일
2. **200ms Motion 통합 라이브러리** (`.enter` `.exit` `.appear`) — 0.5일
3. **Cinematic Intro 1화면** (Cornerstone 단원만) — 단원당 2시간

→ math-story-telling 큰 그림의 **앱 트랙**으로 진행. 본 sub-project 와 cross-link.
→ `10_system/10_principles/APP_PRINCIPLES.md` 갱신 트랙으로 별도.

### 3.2 Content Quality — Deep-dive 8종 (외부 트랙)

| 자료 | 형식 | Effort |
|---|---|---|
| 인물 비하인드 | 1500자 + 1~2 이미지 | 중 |
| 모순·논쟁·실수 | 800자 + 다이어그램 | 중 |
| 현대 응용 1개 깊이 (GPS·암호·CPU) | 1000자 + 시각화 1 | 중 |
| 계보 트리 (1500년 흐름) | 인터랙티브 timeline | 큼 |
| 도전 문제 1개 | 1문제 | 작음 |
| 인물의 한 단어 | 단어 1개 + 30s 영상 ⭐ (Sub-3min 연동) | 작음 |
| 다른 과목 연결 한 줄 | 한 단락 | 작음 |
| **Nick 5분 에세이** | 800자, 인물의 무엇이 인상 깊었나 | 큼 (시간≠분량) |

→ **본 sub-project 와 직접 교차**: "인물의 한 단어 + 30s 영상" = [E] Sub-3min 의 한 종.

### 3.3 "한 권의 책" 메타포 (큰 그림)

13단원 = 카드 13장 병렬 → "한 권의 책" 만들기:
- 인접 단원 인물 그림자 (디오판토스 → 알콰리즈미 인용)
- 단원 끝 "다음 단원의 ?" teaser
- 13단원 후 "인물 13인 가계도" 통합 인포그래픽 1장
- **Interlude 1~2분 영상** ← 본 sub-project 산출물 종류 +1 (시즌1→시즌2 다리)

---

## 4. 자동화 너머 — 7 원칙 P1~P7 ⭐

본 sub-project 의 운영 원칙으로 채택 권장.

| # | 원칙 | 본 sub-project 운영 |
|---|---|---|
| **P1** | **Polish Loop** — 한 장면을 30번 다듬는다. 매 단원 "이 부분 톤이 진짜 좋다" 한 곳 → 다음 단원 standard 승격 | `60_evaluation/retrospectives/` 양식에 "Polish 1건" 필드. promote 흐름의 트리거 |
| **P2** | **학습자 한 줄이 재가공한다** — 딸 "7.2°가 부담" → **수정**이 아니라 **재가공** (별도 30초 영상 추가). 짐 더하기 아닌 깊이 더하기 | `.private/feedback/` → chatlog → 새 산출물 (Sub-3min [E] 1편) |
| **P3** | **Nick 손 1편 = 시리즈 무게** — 모든 산출물 AI = "AI 시리즈". 단원당 1편만 Nick = "사람 시리즈". 권장: 단원당 Nick 5분 에세이 1편 (800자) | 외부 트랙 (Content Quality §3.2) 와 연동. 본 sub-project 는 영상 차원 추적만 |
| **P4** | **Cornerstone 3단원 10배 시간** — 13단원 평준화 X | D-004 옵션 δ 의 운영 원칙. §6 시간 모델로 정량화 |
| **P5** | **"한 단어" 압축** — 인물 1인 = 1단어. 단원 모든 콘텐츠가 그 단어를 향함. "에라토스테네스 = 측정" | `30_content/units/NN/meta.json` schema v2 에 `signature_word` 필드 신설 후보 |
| **P6** | **"양보하지 않은 것" 기록** — 매 단원 완성 시 Nick "이 단원에서 양보하지 않은 것" 한 줄. 모이면 시리즈 영혼 문서 | `math-story-telling/10_system/50_insights/manifesto.md` (누적 1줄씩) 신설 |
| **P7** | **빈칸 5개 의도** — CLAUDE.md 원칙의 운영화. 단원당 think-box 5개. 딸 답은 `.private/feedback/`. **NCC 절대 채우지 않음** | 영상 영역 외 (앱·deep-dive 자료 영역). 본 sub-project 와 약 교차 |

→ **P1·P2·P4·P6 = 본 sub-project 직접 채택**. P3·P5·P7 = cross-link.

---

## 5. 시간 배분 모델 ⭐

| 작업 종류 | 13단원 총 비율 | 1단원당 |
|---|---|---|
| 표준 v1.5 (10단원) | 60% | ~15h |
| **Cornerstone (3단원)** | 30% | ~60h |
| Polish & 재가공 (전체 누적) | 10% | 지속 |

표준 15h × 10 = 150h.
Cornerstone 60h × 3 = 180h.
Polish 누적 ≈ 50h.
**총 ≈ 380h** = 1년 평균 주당 7~8h. 무리 없음.

### 시즌1 5편 한정 시 (D-004 δ 옵션)

| 작업 종류 | 시즌1 5편 비율 | 1단원당 |
|---|---|---|
| 표준 v1.5 (2단원: 02·04 후보) | 40% | ~15h × 2 = 30h |
| **Cornerstone (3단원: 01·03·05 후보)** | 50% | ~60h × 3 = 180h |
| Polish & 진화 메커니즘 (전체 누적) | 10% | ~25h |

**시즌1 총 ≈ 235h** = 3~5주 (주당 50~80h) 또는 8주 (주당 30h) 또는 4개월 (주당 15h).

→ Nick 본업·다른 트랙 (5개 study) 고려 시 **주당 15h × 16주 = 4개월** 현실적.

→ **β 5편 "3~5주" 가정 (R0+R1) 은 표준 단원 기준**. Cornerstone 도입 시 4개월 가정 필요.

---

## 6. 본 sub-project 가 채택할 내용 — 정리

### 채택 (반영 작업 필요)

1. **D-004 scope 에 옵션 δ 신설** — β (5편 평준화) vs **δ (5편 Cornerstone 차등 3+2)**
2. **D-014 ~ D-019 신설** — 5 quality 레버 [A]~[E] 각각 채택 여부 + Polish Loop manifesto
3. **20_principles/ 시드 추가** — Cornerstone 단원 정의 + 7 원칙 운영화 (`STORY_VIDEO_v1_6_seed.md` 에 §2.3 추가)
4. **40_experiments/ 후보 +2** — exp-006-set-piece-01, exp-007-bgm-sfx
5. **30_pipeline/4_motion/** 에 BGM/SFX/Set-piece 시드 항목 추가
6. **60_evaluation/RETROSPECTIVE_TEMPLATE.md** 에 "Polish 1건" 필드
7. **시간 모델 (GOALS.md)** — Cornerstone 도입 시 4개월 가정 명시

### Cross-link (외부 트랙)

- 앱 Polish (`APP_PRINCIPLES.md`) — 본 sub-project 와 동기화 시점 명시 (Cornerstone 단원의 cinematic intro = 영상 poster 사용)
- Content Deep-dive 8종 (`30_content/concepts/`) — 본 sub-project [E] Sub-3min 과 "인물의 한 단어" 연동
- Nick 에세이 (P3) — 외부, 본 sub-project 는 영상 차원 추적만
- manifesto.md (P6) — `10_system/50_insights/manifesto.md` 신설 (외부 SSOT)

---

## 7. R6 의 Nick 응답 대기 Q1~Q6 (외부 chatlog 에서 Nick 응답 대기)

R6 원본 §7. 본 sub-project 영역 응답만 정리:

- **Q1** Cornerstone 3단원 — 01·03 or 04·05 → **본 sub-project D-004 δ 의 입력**
- **Q2** 영상 quality 레버 [A]~[E] 중 Cornerstone 01 즉시 시도 1~2개 → **NCC 추천: [A] + [C]. 본 sub-project D-015 + D-016**
- Q3 App polish (외부 트랙)
- **Q4** Deep-dive 8종 중 Cornerstone 01 추가 3개 → **NCC 추천: 인물 비하인드 / 모순·논쟁 / Nick 5분 에세이**. 본 sub-project 는 "인물의 한 단어 + 30s 영상" 만 (= Sub-3min [E])
- **Q5** Polish Loop 운영 방식 → **NCC 추천: 단원 완료 후 retrospective + manifesto 한 줄**. 본 sub-project D-019
- Q6 ops-studio-app 페이지 4 추가 시점 (외부)

→ 본 sub-project 영역 = Q1, Q2, Q4(부분), Q5.

---

## 변경 이력

- 2026-05-23: 발췌. R6 본문에서 영상 R&D 직접 관련 부분 중심 + 외부 트랙 cross-link 메타.
