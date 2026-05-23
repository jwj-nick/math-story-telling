<!-- 260523_video_v1_5_standardize.md -->

# 영상 v1.5 표준화 + 13단원 일괄 재제작 계획

> Nick 메시지 요지 (2026-05-23): unit-01 v1.5 영상에서 narration 톤·pause·몰입에 꽤 공들였음. 예전 v1 영상 13개는 모두 버리고, v1.5 기반으로 13단원 제대로 다시 만든다. 그 **계획**부터 짠다.
>
> Plan reference: `00_project_hub/20_plan/260522_plan_video_flow.md`
> 표준 원본: `10_system/10_principles/STORY_VIDEO_v1_5.md`

---

# Round 0 — NCC 진단 (Nick 메시지 받은 직후)

## 0.1 현 baseline 정밀 분석 — unit-01 v1.5

`50_channel/season-1-ancient/unit-01/` 산출물 15파일 보유. 그 중 SSOT 텍스트 자료:

| 파일 | 역할 | 분량 |
|---|---|---|
| `storyboard_v1_5.md` | 6장면 마스터 (시간·시각·이미지·모션·텍스트·나레이션) | 5.8KB |
| `narration_v1_5.txt` | edge-tts 입력 (단문+빈줄로 pause) | 549자 / 1.4KB |
| `narration_v1_5.xml` | **SSML 풀스펙** (break·prosody·pitch) — ElevenLabs/Azure 전환 대비 | 2.7KB |
| `image_prompts.md` | AI 이미지 5장 영문 프롬프트 + **공통 캐릭터 시트** | 6.6KB |
| `config_v1_5.json` | HyperFrames 렌더 데이터 (장면 textbox·image path·motion·scene_times) | 2.5KB |
| `index_v1_5.html` | v1.5 마스터 템플릿 + 단원 데이터 | 15KB |
| `final_v1_5.mp4` | 완성본 | 21MB |
| `poster_v1_5.jpg` | 썸네일 (S1 화면) | 85KB |
| `_assets/` | AI 이미지 5장 (gitignored) | — |
| `README.md` | ⚠️ 옛 v1 기준 — `apps/math1/unit-01/` 참조 (이미 폐기된 경로) | 0.9KB |

### narration baseline 정밀 (Nick 강조 부분)

`narration_v1_5.xml` SSML 패턴 분석:
- **break**: 단문 사이 200~800ms, 장면 전환 1500ms — 6장면 약 **40회** 사용
- **prosody rate="-5%"**: 전체 느린 톤 (5자/초 표준 대비 약간 더)
- **prosody pitch="+5%"**: "오차는, 단 일 퍼센트." 한 곳 — 극적 강조
- **prosody pitch="+3%"**: "소인수분해" 단어 — 키워드 강조
- **호흡 단위**: 한 문장 = 12~20자, "는요/이에요/거예요" 어미로 다정함

→ 이게 unit-01 narration "톤·pause·몰입"의 정체. **13단원 모두 이 패턴으로 SSML 작성** 표준화 필요.

### image_prompts baseline 정밀

`image_prompts.md`의 핵심 발견 — "**공통 캐릭터 시트**" 블록:
```
An elderly Hellenistic Greek scholar around 70, gentle weathered face,
short grey curly hair, light beard, wearing a simple white linen chiton
with a worn ochre wool mantle. Calm, observing eyes. Sun-bronzed skin.
```
→ S3·S4 인물 일관성을 위해 5장 중 인물 등장 2장에 동일 시트 삽입.
→ **19인 인물 모두 캐릭터 시트 필요** (`30_content/people/<ref>.md` 안 or 별도).

각 프롬프트는 **영문 + Negative + Style notes** 3블록 표준화됨. 새 단원 동일 패턴 답습 가능.

### config 구조 정밀

`config_v1_5.json` 의 motion 키:
- `scale_from / scale_to`: ken burns zoom (1.0 → 1.04~1.06)
- `pan_x`: 좌우 이동 (-3 ~ +2 %)
- `scene_times`: s1_in=0 / s2_in=5 / ... / s4_spike=65 / end=115

→ 새 단원: 같은 schema 따르되 시간·텍스트만 교체. **자동 시드 생성 가능**.

---

## 0.2 현 v1 (폐기 대상) 분석

`50_channel/_archive/v1/unit02~unit13/` 12개 단원 (unit01도 v1 있음, v1.5로 갱신):

각 단원 보유 파일:
- `storyboard.md` · `narration.txt` (250자, 50초) · `config.json` · `index.html` · `feedback_hitl.md`
- `narration.mp3` · `raw.mp4` · `final.mp4` (gitignored 산출물)

**Nick "다 버린다" 결정의 의미**: v1 산출물(mp4/mp3/index)은 폐기. 텍스트 시드(storyboard/narration/feedback_hitl)는 **v1.5 재작성의 reference** 로 살릴 가치 있음. 특히 `feedback_hitl.md` 는 옛 검수 의견 누적분 — 참고가 됨.

→ 결정: `_archive/v1/` 그대로 유지(이미 archive 폴더). 새 작업은 `season-1-ancient/` (또는 이중 트리) 에서 신규 작성. v1 텍스트는 input으로 열어보되 복붙은 지양 (스타일 v1.5와 다름).

---

## 0.3 13단원 표준화 격차 5축

### D1. **TTS 도구 결정** ⭐ 가장 시급

| 옵션 | 장점 | 단점 |
|---|---|---|
| edge-tts (현재) | 무료, 자동화 검증됨 | SSML 미동작(단문+빈줄로만 pause), 톤·voice 한정, 자연스러움 한계 |
| ElevenLabs | SSML 완전 동작, voice 다양, 톤·감정·pause 정교, 한국어 우수 | 유료 (월 $5~$22), API 키 관리 |
| Azure Cognitive | SSML 동작, 무료 티어 5만자/월 | 가입 절차, 한국어 voice 적음 |

**NCC 권장**: ElevenLabs 전환. 이유 — Nick이 강조한 "narration 톤·pause·몰입"의 baseline이 SSML 풀스펙(narration_v1_5.xml). edge-tts로는 그 정밀도 재현 불가. 13단원 일관 톤을 위해 **지금 결정** 필요. Nick_TODO T1과 직결.

### D2. **AI 이미지 도구 결정** ⭐ 두 번째 시급

| 옵션 | 장점 | 단점 |
|---|---|---|
| ChatGPT (DALL-E 3) | 자연어 프롬프트 친화, Plus 구독 시 무제한 | 인물 일관성 약함 (캐릭터 reference 미지원) |
| Claude.ai 이미지 | 같은 워크플로우 안에서 가능 | 같은 한계 (reference 약함) |
| Midjourney | 인물 일관성 강함(`--cref`), 화풍 우수 | $10~$30/월, Discord 인터페이스 |
| Stable Diffusion 로컬 | 무료, ControlNet으로 캐릭터 고정 | 셋업·VRAM 부담, Nick 손에 익혀야 |

단원당 5장 × 12 = **60장 추가**. 인물 등장 장면(S3·S4)은 동일 캐릭터 일관성 필수.

**NCC 권장**: Midjourney + `--cref` (캐릭터 reference). 이유 — 19인 캐릭터 시트를 한 번 이미지로 만들어두면 모든 단원에서 일관성. Stable Diffusion 로컬은 학습 비용 큼. Nick_TODO T2와 직결.

### D3. **이중 트리 이동 시점**

B 라운드에서 합의: 원본 `50_channel/people/<ref>/<ep>/` + view `50_channel/seasons/season-N/unit-NN/`.

현 unit-01: `season-1-ancient/unit-01/` 에 있음. 옮길 위치는 `people/eratosthenes/sieve-of-eratosthenes/` (또는 단원-인물 매핑별 episode-key).

| 옵션 | 장점 | 단점 |
|---|---|---|
| 지금 옮긴다 | 13단원 신규 작업이 새 트리 기준 | unit-01 검증된 산출물 이동 리스크 |
| 13단원 후 일괄 | unit-01 안정 유지 | 새 단원 13개가 모두 옛 트리에 쌓임 → 나중 이동 비용 큼 |

**NCC 권장**: **지금** 옮긴다. 이유 — 새 12단원 작업 시작 전에 표준 트리 확정해두면 일관 적용. unit-01 git history 보존된 채로 `git mv` 가능. 검증된 final_v1_5.mp4 그대로 옮기면 됨.

### D4. **시드 자동 생성 vs 단원별 순차 작성**

`30_content/units/NN/meta.json` (schema v2)의 다음 필드들로 시드 가능:
- `persons[].story-hook` → S3 인물 등장 / S4 결정적 순간 시드
- `persons[].signature-object` → S4 시각 요소
- `persons[].era-palette` + `signature-color` → 팔레트
- `key-concepts[]` → S5 수학 연결
- `persons[].videos[]` (episode-key) → 파일명 시드

`30_content/people/<ref>.md` (19인)에서 "핵심 일화" 섹션 → 일화 narrative 시드.

| 옵션 | 장점 | 단점 |
|---|---|---|
| 12단원 시드 일괄 (1라운드) | 빠름, 일관 톤, 격차 한눈에 | 시드 품질 검증 후 일괄 수정 부담 |
| 단원별 순차 (12라운드) | 단원당 깊이, 품질 보장 | 시간 길어짐, 일관성 표류 위험 |

**NCC 권장**: 시드 일괄 + 파일럿 1단원(unit-02 브라마굽타). 시드 12개를 NCC가 자동 생성 → unit-02 풀빌드(이미지·TTS·렌더) 검증 → quality gate 통과하면 나머지 11단원 동일 패턴.

### D5. **빌드 자동화 / audit skill 신설**

`se_story_video_v1_5` skill 점검 필요 (다음 라운드에서 확인).

신설 후보 `se_ncc_audit_video`:
- 길이 95~120s 확인
- narration 자수 480~620
- SSML break 횟수 30+ (pause 충분)
- 이미지 4~6장 + 16:9
- final.mp4 < 25MB / sync ±0.3s

**NCC 권장**: skill 점검 결과(Round 2)에 따라 결정. 자동화 신뢰도 낮으면 NCC가 매 단원 audit.

---

## 0.4 STORY_VIDEO_v1_5.md 갱신 필요 사항 (Round 2에서)

현 문서(237줄, v1.5.1) 잘 작성됨. 갱신 필요:

1. **§3.1 edge-tts → ElevenLabs 전환** (D1 결정 후)
2. **§2 캐릭터 시트 표준** 추가 — 19인 모두 캐릭터 시트 (.md 또는 image)
3. **§7 디렉토리 구조** — 이중 트리 반영 (D3 결정 후)
4. **§5.3 narration SSML 검수 항목** — break 30회+ / 강조 prosody 1~3회
5. **§6 Skill 호출** — `se_ncc_audit_video` 추가 (D5 결정 후)

---

## 0.5 로드맵 제안 (Round 단위)

| Round | 일감 | 산출물 | 외부 의존 |
|---|---|---|---|
| **R0** (지금) | NCC 진단 | 본 chatlog | — |
| **R1** | Nick 5축 결정 (D1~D5) | 결정 기록 | Nick 응답 |
| **R2** | STORY_VIDEO_v1_5.md 갱신 + se_story_video_v1_5 skill 점검·갱신 | 문서·skill 업데이트 | — |
| **R3** | 19인 캐릭터 시트 일괄 작성 (`30_content/people/` 보강 또는 별도) | 19개 시트 | (선택) Nick MJ 이미지 생성 |
| **R4** | (D3 결정 시) unit-01 → 이중 트리 이동 | `git mv` 결과 | — |
| **R5** | 12단원 시드 일괄 생성 (storyboard/narration/image_prompts/config) | 12 × 4 파일 = 48 파일 | — |
| **R6** | unit-02 파일럿 풀빌드 (이미지 5장 + TTS + render + final.mp4) | unit-02 v1.5 산출물 | Nick 이미지 생성 / TTS 키 |
| **R7~R17** | 남은 11단원 단원별 진입 (각 1세션) | 11 × v1.5 산출물 | Nick 이미지 + TTS |
| **R18** | 13단원 일괄 quality gate + E 배포 매핑 hookup | audit log + 배포 build | — |

소요 추정: R1~R5는 빠르게 (1~2주). R6~R17이 Nick 이미지 생성에 좌우 — 단원당 1~2시간 Nick 작업 + 빌드 30분.

---

## 0.6 Nick에게 요청하는 결정 (R1에서 답 부탁)

다음 라운드(R1)에 Nick이 결정해줘야 할 것:

- **Q1 (D1)**: TTS — edge-tts 유지 / ElevenLabs 전환 / 다른 옵션?
- **Q2 (D2)**: AI 이미지 — ChatGPT / Claude / Midjourney / Stable Diffusion 로컬 / 미정(R3에서 결정)?
- **Q3 (D3)**: 이중 트리 이동 — 지금 / 13단원 후 / 다른 시점?
- **Q4 (D4)**: 시드 자동 생성 vs 단원별 순차 — NCC 권장(일괄+파일럿) OK?
- **Q5 (D5)**: audit skill 신설 — Round 2 점검 결과 보고 결정 / 지금 결정?
- **Q6 (확장)**: 시즌 1(Ancient) 외 추가 시즌은 13단원 후 검토? 또는 13단원 작업 중 병행?

---

## 0.7 잠재적 리스크 / 미확정

- ElevenLabs 한국어 voice 후보: SunHi(다정) 대체 voice 찾기 — R2에서 sample 청취 필요
- Midjourney `--cref` 캐릭터 일관성 실제 검증 필요 — R3에서 19인 중 한두 명으로 테스트
- final.mp4 13개 합 ~250MB → GitHub Releases 분할 vs YouTube 업로드 정책 결정 (E와 연계)
- 라이센스: AI 이미지 상업적 사용 / 음성 voice 라이센스 (ElevenLabs Terms)
- Rate limit: ElevenLabs 무료 1만자/월 → 13단원 약 7000자 → 무료로 가능. 단 재생성 여유 필요 시 유료.

---

> **다음 액션**: Nick이 (Q1~Q6) 답하면 R1 시작. 답 안 한 Q는 NCC 권장 그대로 진행.

---

# Round 1 — NCC zoom out 재진단 (Nick "이 시점에 생각을 많이 해보자" 받음)

> Nick 메시지 (2026-05-23): "지금부터 앞으로 계획을 다시 재정리하면 어떨지... 현재 전체 마스터 플랜 리스트에서 어느 단계인지 확인 필요함. 이제부터 진짜 중요할 것 같다."
>
> R0 완성 직후 zoom out 요청. NCC가 R0를 무비판으로 추진하지 말고, **마이그 전 결정·비전 문서들과 정합 점검** + **scope·우선순위 재진단** 후 R0를 보정한다.

---

## 1.1 검토 input — 마이그 전 작성된 비전·플랜 5건 재독

| 파일 | 핵심 자산 |
|---|---|
| `10_system/50_insights/260520_unit01_story_video_v1_5.md` | unit-01 v1.5 회고. 5 원칙 후보 중 **2개 미반영** (length dry run + 캐릭터 시트 분리) |
| `00_project_hub/10_chatlog/260516_channel_vision_review.md` | 5개 외부 비전 문서 검토 + NCC 종합. **시즌1=Ancient 5단원 우선**, ElevenLabs 5인 voice 매핑, 4편 분할 구조, 창의 제안 8개 |
| `00_project_hub/10_chatlog/260520_system_architecture.md` | **진화 메커니즘 4단계 사이클** (Build → Retrospect → Distill → Apply). Option B + sync script + insight 파일 누적·반영 표시 — Nick 확정 |
| `00_project_hub/10_chatlog/260516_meta_planning.md` | R3 신규 monorepo 결정 (mathtelling + design-system) + 5년 후 가설. **앱=백본 / 영상=보조** 원칙 명문화 |
| `00_project_hub/30_history/Nick_TODO.md` | T1 ElevenLabs (무료 10000자/월 = 13단원 7800자 1회 가능), T2 SD vs MJ 미결정 |
| `10_system/70_meta/{VISION, MASTER_PLAN, ROADMAP}.md` | ⚠️ **옛 00_LearningSystem 시절** 마스터 플랜. 마이그 후 단일 repo 현실 미반영. **outdated** |

---

## 1.2 마스터 플랜 위치 매핑 — 현재 어디인가

### 옛 비전 문서들 기준 timeline

```
[2026-05-09~11] 13단원 앱 일괄 (mid_eun 50_units/)              ✅ 완료
[2026-05-14]   영상 v1 13편 + STORY_VIDEO_GUIDE                ✅ 완료 (현재는 _archive/v1)
[2026-05-16]   채널 비전 5문서 + NCC 12 결정 + 메타 플래닝 R1   ✅ 완료
[2026-05-16]   메타 플래닝 R2~R3 → 신규 monorepo 결정          ✅ 완료
[2026-05-19~20] R3 Step 1·2 — mathtelling + design-system 초기화 ✅ 완료
[2026-05-20]   영상 v1.5 unit-01 완성                          ✅ 완료
[2026-05-20]   진화 메커니즘 (Build/Retrospect/Distill/Apply)  ✅ 합의 → 1차 작동
[2026-05-21]   repo 통합 결정 + 마이그 실행                    ✅ 완료
[2026-05-22~23] 수학 챕터 표준 (B) + walk_01 (F) + repo 정리   ✅ 완료
[2026-05-23]   ← 현재
```

### 채널 비전 리뷰 (`260516_channel_vision_review.md`) Phase 0-A 명세

| 항목 | 명세 (시즌1 한정) | 현 상태 |
|---|---|---|
| 인물 수 | **5인** (Ancient: 에라토스테네스/브라마굽타/알콰리즈미/디오판토스/데카르트) | meta·인물 자료는 19인 모두 준비됨. 영상 5인은 unit-01만 완성 (1/5) |
| 시즌1 영상 편수 | **5편** (단원 01·02·03·04·05) | 1편 (unit-01) |
| 길이 | 60~90s → 95~120s (v1.5 표준) | unit-01 = 107s ✅ |
| TTS | ElevenLabs **5인 voice 매핑** | edge-tts SunHi 단일 voice |
| AI 이미지 | SD 로컬 또는 MJ | unit-01만 Claude/ChatGPT 수동 5장 |

→ **현 위치 = Phase 0-A 진행 중 (1/5 영상 완성)**. 남은 영상 = **시즌1 4편 (unit-02·03·04·05)**. 단원 06~13 은 **시즌2~3 으로 후순위**.

### 어제 R0 가정의 문제

R0는 **"13단원 일괄 재제작"** 을 전제로 D1~D5 + 로드맵 R1~R18을 짰음.
→ 채널 비전(시즌1=5인)과 어긋남. 13편 전부는 **시즌1~3 합산** 분량으로 1년+ 작업.

---

## 1.3 어제 R0 진단의 갭 7개

| # | 갭 | 출처 | 영향 |
|---|---|---|---|
| **G1** | **scope: 13편 vs 시즌1 5편** | 260516 채널 비전 D1 | 작업량 60장 이미지 → 25장. 8주 → 3주. **가장 큰 갭** |
| **G2** | "4편 분할 구조" (D3) — 1단원 1편 vs 분할 | 260516 D3 | 단원당 110s 단편 vs 더 긴 다편 시리즈 선택 미답 |
| **G3** | ElevenLabs **5인 voice 매핑** | 260516 D4 | R0는 voice 1개만 가정. 실제는 인물별 다른 voice 권장 |
| **G4** | 인물 캐릭터 시트 분리 **미반영** (insight 후보 4번) | 260520 insight 미반영 | R0는 19인 캐릭터 시트 작성을 R3 작업으로 잡음 — 이미 합의된 미완 작업 |
| **G5** | narration length dry run **미반영** (insight 후보 2번) | 260520 insight 미반영 | R0 표준 갱신 항목에 없음. **STORY_VIDEO_v1_5.md §4 절차 갱신 필요** |
| **G6** | "앱 = 백본 / 영상 = 보조" 우선순위 | 260516 meta planning | R0는 영상에 R1~R18 (17 라운드) 할당. 앱 D 트랙 보강이나 축 C 진도는? |
| **G7** | 창의 제안 8개 (편지함·딸 #001·Lab Notes·그림책·시그니처 사물·캡슐·Audio Story·문해력 노트) | 260516 channel vision §5 | R0는 표준 6장면 v1.5만 가정. **편지함 framing device** 같은 메타 장치 채택 여부 미검토 |

---

## 1.4 권장 — scope 재정리

### scope 옵션

| 옵션 | 작업량 | 기간 | 비고 |
|---|---|---|---|
| α. 어제 R0 — 13편 일괄 | 65장 이미지 + 13편 TTS·렌더 | 8~12주 (Nick 이미지 작업 좌우) | 비전 문서와 불일치. 영상 비중 과다 |
| **β. 시즌1 5편 우선 (NCC 권장)** | **25장 이미지 + 5편 TTS·렌더** | **3~5주** | 260516 비전과 정합. 무료 quota 가능 (ElevenLabs 10000자) |
| γ. 시즌1 + 시즌2(3편) 점진 | 40장 + 8편 | 6~9주 | 후속 시즌 시작 시 다시 결정 |

**NCC 권장: β**.

이유:
1. **비전 정합**: 260516 채널 비전 D1 (시즌1=5단원) 그대로 따름
2. **Nick 외부 의존 최소**: ElevenLabs 무료 + MJ basic $10 1개월로 시즌1 충당
3. **품질 게이트 검증**: 5편 완성 후 회고 → 6~13편 결정 (필요/불필요/축소 등)
4. **앱 D 트랙 병행 여력**: 5편 작업이 짧아서 동시에 단원별 concepts/problems 보강 가능
5. **이북·창의 제안 검토 시간 확보**: 5편 끝나면 zoom out 1회 더

### 시즌1 5편 명세

| Ep | 단원 | 인물 (primary) | episode-key | era-palette |
|---|---|---|---|---|
| Ep1 | 01 소인수분해 | 에라토스테네스 | sieve-of-eratosthenes | era-ancient |
| Ep2 | 02 정수와 유리수 | 브라마굽타 | zero-and-negatives | era-medieval (India 시드 색) |
| Ep3 | 03 문자와 식 | 알콰리즈미 | birth-of-algebra | era-medieval (Islamic) |
| Ep4 | 04 일차방정식 | 디오판토스 | arithmetica-puzzles | era-ancient (Late antiquity) |
| Ep5 | 05 좌표와 그래프 | 데카르트 | coordinate-revolution | era-modern (Early) |

각 110s × 5 = 약 9분. narration 약 600자 × 5 = 3000자. ElevenLabs 무료 10000자 충분.

---

## 1.5 진화 메커니즘 본격화 — 지금 즉시 처리 가능한 sub-tasks

`10_system/50_insights/_index.md` 의 미반영 1건 (5 후보 중 2개) 즉시 처리.

### 1.5.1 STORY_VIDEO_v1_5.md 갱신 — 4개 항목 추가

1. **§2.2 캐릭터 시트 분리 원칙** 추가 — `image_prompts.md` 최상단에 인물 공통 묘사 1회 작성, 각 장면 프롬프트는 "use the common character" 참조
2. **§4 [6.5] 길이 dry run 분기** 추가 — narration.txt 작성 직후 TTS 1회 합성으로 95~120s 검증 → 벗어나면 narration 재조정
3. **§3.1 인물별 voice 매핑 표** 추가 — (ElevenLabs 전환 후) 시즌1 5인 voice 매핑
4. **§7 디렉토리 구조** — 이중 트리 반영 (R0 D3 결정 후)

### 1.5.2 se_story_video_v1_5 skill Phase E 추가

`.claude/skills/se_story_video_v1_5/` 의 SKILL.md 에 **Phase E — 자동 retrospective** 추가:
- 빌드 완료 직후 `10_system/50_insights/{YYMMDD}_unitNN_story_video_v1_5.md` 자동 작성
- `_index.md` 에 새 entry 자동 append
- 5 원칙 후보 도출 templating

### 1.5.3 insight 처리

`260520_unit01_story_video_v1_5.md` 의 2번/4번 후보를 STORY_VIDEO_v1_5.md 에 반영 → `_index.md` 의 미반영 entry를 `[x]` 로 변경.

→ 이 3개 (STORY_VIDEO_v1_5 갱신 + skill Phase E + insight 반영 표시)는 NCC가 자율 진행 가능. R2의 첫 작업.

---

## 1.6 `10_system/70_meta/` 옛 마스터 플랜 처리

`VISION.md` / `MASTER_PLAN.md` / `ROADMAP.md` 는 옛 00_LearningSystem 시절 작성된 **여러 자식 프로젝트 (mid_eun + HS2604) 통합 메타** 문서.

마이그 후 현재 math-story-telling 은:
- 단일 repo (mid_eun + mathtelling + design-system + 00_LearningSystem 합산)
- HS2604 는 별개 (`C:/Nick/...` 등)

→ 옛 마스터 플랜은 **이력 자료**로는 가치 있으나 **현 작업 가이드**로는 부적합.

### 처리 옵션

| 옵션 | 비고 |
|---|---|
| A. 옛 마스터 플랜 그대로 유지 | 혼동 위험 |
| B. **`10_system/70_meta/` 의 3건을 `90_archive/`로 이동** + **신규 `10_system/70_meta/VISION.md` 작성** (math-story-telling 단일 비전) | 권장 |
| C. 옛 문서 안에 "outdated, math-story-telling 단일 repo 마이그 후" 헤더 한 줄만 추가 | 가볍지만 모호 |

**NCC 권장: B**. 신규 VISION/MASTER_PLAN/ROADMAP 은 본 chatlog R1.4 의 scope 결정 후 작성.

→ R2 또는 별도 chatlog `260523_meta_realignment.md` 에서 처리.

---

## 1.7 R0 결정의 변경

R0의 D1~D5 결정은 **scope β 채택 시** 다음과 같이 조정:

| R0 결정 | R0 권장 | R1 조정 (β scope 가정) |
|---|---|---|
| D1 TTS | ElevenLabs 전환 | **유지** — 단 시즌1 5편 voice 매핑 (5인 다른 voice) |
| D2 AI 이미지 | Midjourney + `--cref` | **유지** — 25장만, MJ basic $10 1개월 |
| D3 이중 트리 이동 시점 | 지금 | **유지** — unit-01만 일단 이동 |
| D4 시드 자동 생성 | 12단원 일괄 + unit-02 파일럿 | **시즌1 4단원 (02·03·04·05) 시드 + unit-02 파일럿** |
| D5 audit skill 신설 | R2 후 결정 | **유지** |

신규 결정:
| 결정 | 옵션 | NCC 권장 |
|---|---|---|
| **D6 scope** | α 13편 / **β 5편** / γ 8편 | **β** |
| D7 단원 → 영상 분할 | 1단원 1편 / 분할 | 1단원 1편 (110s) — 시즌1에선 유지. 시즌2+ 에서 분할 검토 |
| D8 창의 제안 채택 | "수학자의 편지함" framing 외 7개 | 시즌1 5편 끝나고 회고 시 검토. **지금은 0개 채택** |
| D9 옛 70_meta 처리 | A/B/C | **B** (별도 chatlog) |
| D10 진화 메커니즘 본격화 | 지금 / 시즌1 후 | **지금** — R2에서 STORY_VIDEO_v1_5 갱신 + skill Phase E + insight 반영 |

---

## 1.8 Nick 결정 요청 (R1 응답)

가장 중요한 결정 1개 + 보조 결정 4개:

### 🔴 핵심
- **D6 (scope)**: α 13편 일괄 / **β 시즌1 5편 우선** / γ 시즌1 + 시즌2 일부?

### 🟡 보조 (NCC 권장 기본값으로 진행 가능)
- D7 단원→영상 분할 (1단원 1편 vs 분할)
- D8 창의 제안 (지금 0개 vs 일부 채택)
- D9 옛 70_meta 처리 (A/B/C)
- D10 진화 메커니즘 본격화 시점 (지금 vs 시즌1 후)

### 🟢 R0 결정 유지
- R0 Q1~Q5 (TTS·이미지·이중 트리·시드·audit skill) — Nick "권장 따름" 시 NCC 자율 진행

---

## 1.9 Nick 결정 없이도 NCC 자율 진행 가능한 작업 (R2 후보)

D6~D10 답 없어도 **무관하게 추진 가능한 인프라**:

1. **`10_system/50_insights/_index.md` 의 미반영 2건을 STORY_VIDEO_v1_5.md 에 반영** + `[x]` 표시 — 진화 메커니즘 본격화 첫 단계
2. **`se_story_video_v1_5` skill 점검** — SKILL.md 읽고 v1.5 표준과 격차 audit
3. **STORY_VIDEO_v1_5.md 4개 항목 갱신** (§2.2 캐릭터 시트 / §4 length dry run / §3.1 voice 매핑 / §7 디렉토리)
4. **`10_system/70_meta/` 옛 3건의 비전 정합성 audit 보고서** — 작성·이동은 D9 결정 후

→ 이 4건은 D6~D10 어떤 답이 와도 가치 있음. **Nick 응답 대기 중 자율 진행**.

---

## 1.10 R0→R1 의 의미

R0는 "13단원 영상 만들기" 에 집중. R1은 **"왜 영상을 만드는가, 얼마나 만드는가, 비전 5건과 정합한가"** 를 zoom out 해서 점검.

핵심 발견: 어제 R0 = "방법론적 완전성" / R1 = "전략적 정합성".

13편 전부 만드는 것이 *옳다* 가 아니라 *증명되지 않은 가정*. 시즌1 5편으로 좁히고 후속 zoom out을 한 번 더 하는 것이 학습 시스템 비전 (앱=백본 / 영상=보조) 과 맞음.

> **다음 액션**: Nick이 D6 (scope) 만이라도 답하면 R2 시작. 동시에 NCC는 1.9의 4건 자율 진행.


---

# Round 2 — R6 (Quality / Essence) 통합 + sub-project plan 재정립

> 2026-05-23 compact 후. Nick 지시: "C:/Kids/00_LearningSystem/00_chatlog/260523_R6_quality_essence.md 도 여기 갖고와서 11_video_gen_process plan을 원래 있던 파일들과 함께 생각해서 세워보기"
>
> 본 라운드 본문은 sub-project 내부 (`11_video_gen_process/00_charter/INTEGRATED_PLAN.md`) 에 정리. 여기는 메타 + 변경 요지만.

## 2.1 R6 를 sub-project 로 가져온 방식

- 원본: `C:/Kids/00_LearningSystem/00_chatlog/260523_R6_quality_essence.md` (외부 위치 — 옛 00_LearningSystem 잔존)
- 발췌: `11_video_gen_process/10_reference/04_R6_quality_essence.md` (영상 R&D 직접 관련 §1·§2·§4.3·§5 + 외부 트랙 §3·§4.2·§6 요약)
- 인덱스: `10_reference/_origin.md` 에 entry 추가
- 외부 위치 D-012 옛 70_meta 처리 와 함께 검토 필요로 표시

## 2.2 R6 가 sub-project plan 골격을 바꾼 부분

| 이전 (R0+R1) | 이후 (R6 통합) |
|---|---|
| scope = β 시즌1 5편 평준화 | **scope = δ 시즌1 5편 + Cornerstone 차등 (3+2)** |
| 표준화 = v1.5 → v1.6 단일 층 | 표준화 **2 층**: ① 표준 단원 v1.6 평균선 + ② Cornerstone 단원 peak (5 quality 레버) |
| 시간 = 3~5주 (β) | **시간 = 235h / 4개월 (주당 15h)** |
| 결정 항목 D-004~D-013 | + **D-014~D-019 신설** (Cornerstone / Set-piece / BGM·SFX / 일러스트 / Sub-3min / Polish Loop) |
| NCC 자율 4건 (R1.9) | + **자율 5건째** 추가 (R6 7 원칙 운영화 시드) |

## 2.3 핵심 신 frame — Cornerstone 차등

R6 §1 "자동화 vs 깊이는 충돌" 명제. 같은 단원에 둘 다 부으면 둘 다 못 함.

→ **5편 안에서도 3 Cornerstone + 2 표준**:
- Cornerstone 추천: 01 에라토스테네스 + 04 디오판토스 + 05 데카르트 (방정식 = 중1 시험 최대 비중)
- 표준: 02 브라마굽타 (시즌1 두 번째 = v1.6 표준 검증 파일럿) + 03 알콰리즈미

5 quality 레버 [A]~[E] 적용 매트릭스:
| 레버 | Cornerstone | 표준 |
|---|---|---|
| [A] Set-piece 30s | ✅ | ❌ |
| [B] ElevenLabs | ✅ 5 voice | edge-tts |
| [C] BGM | ✅ ambient + sting | ✅ ambient 만 |
| [D] 일러스트 외주 | ✅ 한 장 | ❌ AI |
| [E] Sub-3min 보조 | ✅ 1~3개 | △ 0~1개 |

## 2.4 산출물

- ⭐ `11_video_gen_process/00_charter/INTEGRATED_PLAN.md` 신설 — 4 reference 통합 plan (메인 산출물)
- `10_reference/04_R6_quality_essence.md` 발췌
- `10_reference/_origin.md` 갱신
- `00_charter/DECISIONS.md` 갱신 — D-004 옵션 δ + D-014~D-019 신설
- `00_charter/VISION.md` 갱신 — §4 Cornerstone / §5 한 단어·manifesto 신호
- `00_charter/GOALS.md` 갱신 — δ 시간 모델 + 우선순위 8 후보 + 마일스톤 M1~M4 (16주)

## 2.5 다음 액션 분기 (sub-project INTEGRATED_PLAN §7)

- **분기 A** Nick 결정 우선: D-013 → D-004 → D-014 → 즉시 sprint
- **분기 B** NCC 자율 우선 (권장): D-013 만 결정 → 자율 5건 진행 → Nick 결정은 R3 라운드로 평행
- **분기 C** 단원 빌드 즉시: 지양 (v1.5 → v1.6 갱신 전 빌드 = polish 기회 손실)

→ NCC 추천 = **분기 B**. compact 후 첫 세션 = "NCC 자율 sprint 0 + R3 안건 상정".

## 2.6 R6 의 Q1~Q6 중 본 sub-project 영역 (Nick 응답 대기)

- **Q1** Cornerstone 3단원 후보 — 01 + 04 + 05 (NCC 추천) or 01 + 03 + 05 → D-014
- **Q2** Cornerstone 01 즉시 시도 1~2개 — [A] Set-piece + [C] BGM/SFX (NCC 추천) → D-015 + D-016
- **Q4** Deep-dive 8종 중 영상 영역 — "인물의 한 단어 + 30s 영상" 만 (= Sub-3min [E])
- **Q5** Polish Loop 운영 — 단원 완료 후 retrospective + manifesto 한 줄 (NCC 추천) → D-019
- Q3·Q6 = 외부 트랙 (앱·ops-studio-app)


---

# Round 3 — 본질 재정의 (2026-05-24)

> Nick 지시: "시즌1 5편 잊어라. 이 디렉토리는 영상 제작 시스템 (프로세스 + 자동화) 을 구축하는 곳. 디렉토리 이름이 그렇게 지어졌다."

## 3.1 본질의 명시화

영상 트랙의 본질이 다음으로 재정의됨:

- **이 디렉토리는 영상을 양산하는 곳이 아니다.**
- 한 단원을 깊이 있게 만들면서 시스템의 모든 단계를 손으로 경험한다.
- 그렇게 만든 시스템으로 다음 영상은 *훨씬 쉽게* 만든다.
- 시스템이 안정되면 거의 **자동화** 한다.
- 결과적으로 각 챕터당 1~2개 영상이 만들어진다 — 부산물이지 목표가 아니다.

## 3.2 신설 산출물

⭐ **`11_video_gen_process/00_charter/PURPOSE.md`** — 절대 변하지 않는 목적을 박은 단일 문서. 변경 시 본 파일이 가장 먼저 갱신되고 그 후 INTEGRATED_PLAN 이 따른다.

## 3.3 폐기된 frame

- "시즌1 5편 완성" — X
- "16주 안에 N편" — X
- "Cornerstone N편 + 표준 N편" — X
- "집중 단원" / "기본 단원" / "차등" / "평균선" — X
- "1단원당 N시간" — X
- "13단원 영상 일괄 확장" 트랙 — X (큰 그림 current-plan 의 옛 D 트랙)
- 영상 산출물 수를 목표로 표현하는 모든 것 — X

## 3.4 새 frame — 3단계 진화

| 단계 | 무엇 | 신호 |
|---|---|---|
| 1. 수동 깊이 | 한 단원 손으로 깊이. 6단계 모두 직접 경험. 표준 추출 | 표준 문서 단계별 명시 |
| 2. 반복 적용 | 시스템으로 다음 단원 빌드. 부족 발견·보강 | 단원당 시간 ↓, 동일 격차 재발견 X |
| 3. 자동화 | 시스템 안정. 자동화 도구 누적 | 1편 빌드 시 사람 시간 < 5h |

단계 간 시간은 자연스럽게. 일정 박지 않음.

## 3.5 결정 항목 재정렬 (2차)

산출물 양산 frame 폐기로 결정 5개가 사라짐. 남은 결정 11개로 재번호.

- 폐기: 옛 결정 ② (평균선 vs 차등) / ③ (집중 단원 3편 선정) / ⑨ (동시 시드 vs 순차) / ⑧ (단원 분할)
- 유지+재번호: ② 음성 도구 / ③ 이미지 도구 / ④ 디렉토리 / ⑤ 자동 검증 / ⑥ 다듬기 사이클 / ⑦ 일러스트 외주 / ⑧ 짧은 보조 영상 / ⑨ 핵심 시각화 30초 / ⑩ 배경음·효과음 / ⑪ 옛 비전 문서

매핑 표: `11_video_gen_process/00_charter/DECISIONS.md`

## 3.6 변경된 산출물 인벤토리

- ⭐ `00_charter/PURPOSE.md` 신설
- `00_charter/INTEGRATED_PLAN.md` 전면 재작성 (3단계 진화 frame)
- `00_charter/DECISIONS.md` 매핑 표 2차 재정렬
- `00_charter/VISION.md` 변경 이력만 (deprecated 유지)
- 9개 README + 2개 _index 잔여 표현 ("시즌1 5인", "집중 단원만") 정리
- 큰 그림: `CLAUDE.md`, `00_project_hub/20_plan/current-plan.md` — 5편/16주/D 트랙 표현 제거. PURPOSE.md 진입 안내 추가
- TaskList 정리: 옛 frame 작업 12건 delete. #17 subject 갱신 ("영상 제작 시스템 구축")

## 3.7 이 시점부터 절대 원칙

- 본 프로젝트의 어떤 문서에도 "N편 완성" 같은 산출물 양산 목표가 등장하지 않는다.
- 영상 수는 결과이지 목표가 아니다.
- 시스템 진화의 신호는 *시간 ↓·표준 안정·동일 격차 재발견 없음* 으로 측정한다.

