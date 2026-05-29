<!-- final-retrospective.md / exp-002 unit01 vertical slice 종합 회고 -->

# exp-002 unit01 — Vertical Slice 종합 회고

> **무엇**: 단원 1 (소인수분해 / 에라토스테네스) 영상 1편을 본 sub-project 안에서 끝까지 빌드하며 8 STEP 스킬 전부를 시범·정형화.
> **결과**: `8-final.mp4` (140.27s, 11.2MB) — 영상 1편 완성. 8 STEP 스킬 v0.1~v0.5.2.
> **본질**: 영상 *양산*이 아니라 *시스템 구축*. 이 한 편을 만드는 과정에서 겪은 시행착오가 시스템 자산.
> **기간**: 2026-05-25 ~ 2026-05-29.

---

## 1. STEP별 결과 + 핵심 교훈

| STEP | 산출물 | 스킬 | 핵심 교훈 |
|---|---|---|---|
| 1 서사 | 1-narrative.md | se-people-narrate v0.1 | 추상 설계 6라운드 → 비효율. **reverse-engineering**(시범 먼저→정형화)로 전환 |
| 2 스토리 | 2-story-seed.md | se-video-story v0.1 | 약속 3겹을 6장면에 직조. S4(아르키메데스)가 발견 필연성의 절정 |
| 3 스토리보드 | 3-storyboard.md | se-video-storyboard v0.1 | 부록 A/B/C가 후속 4단계(나레이션·이미지·모션·렌더)의 단일 소스 |
| 4 나레이션 | 4-narration.mp3 (140s) | se-video-narration v0.5.2 | **도구·voice 선정은 반복 탐색** (아래 §2) |
| 5 이미지 | 5-images/ 8장 | se-video-image v0.1 | 캐릭터 일관성 2단계 + Nano Banana. billing 장벽 → web 수동 |
| 6 모션 | 6-motion-config.json | se-video-motion v0.1 | scene별 시간 = 음성 sync 기준. 자막은 나레이션 turn에 종속 |
| 7 렌더 | 7-raw.mp4 | se-video-render v0.1 | FFmpeg zoompan+drawtext, concat으로 sync 보존 (xfade 금지) |
| 8 합성 | 8-final.mp4 | se-video-compose v0.1 | 영상+음성 mux, -shortest로 sync |

---

## 2. 가장 큰 교훈 — 도구·소재 결정은 1-shot이 아니다

### TTS 변천 (STEP 4)
edge-tts(한국어 3 voice, 청소년 X) → ElevenLabs Free(library voice **HTTP 402** 차단) → Google Cloud TTS(결제 SMS 막힘 보류) → **ElevenLabs API $10 충전**(확정).

### voice 폐기 연쇄
Jessica/Will(미국식) → Mono Beige(음량 과대) → Annie/Onyu(느림) → Yura(청취 후 별로) → **Kanna/Kyle 확정** (단원1) + Mina(대안).

### 기술 발견 (시스템 자산)
- **`speed` 파라미터** (voice_settings, 0.7~1.2) → ffmpeg atempo 후처리 폐기
- **음량 balance**: voice마다 default 다름 → volumedetect 측정 → +dB 보정 (Mike +8, Kyle +3.8)
- **pause 설계**: Q/A 300ms + scene 1000ms silence concat
- **노이즈 대응**: 특정 turn 합성 아티팩트 → 그 turn만 재합성

### 이미지 (STEP 5)
- 도구 비교: GPT Image / **Nano Banana(1차)** / Midjourney(API X) / Flux. DALL-E 3는 2026-05-12 제거.
- **캐릭터 일관성 2단계**: CHAR 묘사 블록 + reference 우선 생성 (에라토 ref→S2·S4)
- **Gemini 이미지 free tier 0** → billing 필수 (Cloud TTS와 동일 장벽). web 수동 우회.
- **S3 '소수의 체' 이중 메타포** (Nick 아이디어): 진짜 체 + 숫자의 체. 손(분류)→체(소수) 전환.

---

## 3. 8 스킬 상태

| 스킬 | version | SSOT 위치 |
|---|---|---|
| se-people-narrate | v0.1 | 70_tools/se-people-narrate/ |
| se-video-story | v0.1 | 70_tools/se-video-story/ |
| se-video-storyboard | v0.1 | 70_tools/se-video-storyboard/ |
| se-video-narration | v0.5.2 | 70_tools/se-video-narration/ (+ voice-pool §0 합성 config SSOT) |
| se-video-image | v0.1 | 70_tools/se-video-image/ (+ image-tools-guide.md) |
| se-video-motion | v0.1 | 70_tools/se-video-motion/ |
| se-video-render | v0.1 | 70_tools/se-video-render/ |
| se-video-compose | v0.1 | 70_tools/se-video-compose/ |

부속 자산: `20_step_guides/` 8개 심화 가이드, `voice-pool.md §0`(재현 config), `tts-tools-guide.md`, `image-tools-guide.md`, `google-cloud-tts-guide.md`.

---

## 4. 결정 누적 (INTEGRATED_PLAN §8 반영 대상)

- **TONE_STRUCTURE v3.5**: 2화자 dialog(Q 청소년 존댓말 + A 대학원생 친절 반말), 의문/감탄/평문 다양화, ElevenLabs 1차
- **voice 확정**: Kanna(Q)+Kyle(A) 단원1 / Mina 대안. speed 1.15, +dB balance, pause 300/1000
- **이미지**: Nano Banana 1차(billing 필요), 캐릭터 일관성 2단계, 16:9/no-text/era-palette
- **렌더**: FFmpeg 1280x720/25fps, zoompan+drawtext(NotoSerifCJKkr), concat sync
- **길이**: ~140s (목표 150~180 하한 근처)

---

## 5. 시간·효율 — 단원1은 탐색, 단원2는 가속

단원1 = 스킬 정의 + 도구 탐색 + 반복(voice 6회, 이미지 billing, S3 보강)으로 **시간 多**. 단원2부터는:
- 스킬 8개 정형화됨 → 시범 단계 생략, 바로 실행
- voice-pool §0 config 재사용 (단원별 randomize)
- FFmpeg 렌더 파이프라인 재사용 (config만 교체)
- 이미지 billing 해결 시 NCC 완전 자율 (web 수동 불요)

→ **목표: 단원당 사람 개입 최소, NCC 자율 진행.**

---

## 6. 단원2 일반화 항목 (열린 과제)

- [ ] 이미지 billing 활성화 → NCC API 자동 생성 (현재 web 수동)
- [ ] se-video-motion/render/compose SKILL.md 시드 → 단원2에서 일반화 검증
- [ ] voice 단원별 randomize (단원2 = Q 남 + A 여, voice-pool §3.1)
- [ ] 인물별 voice 고정 옵션 (시리즈 정체성)
- [ ] 렌더 파이프라인 = 재사용 스크립트화 (config→mp4 자동)
- [ ] 1~30 격자 SVG (S3 보강 — se-math-figure 연계)
- [ ] BGM/효과음 레이어 (STEP 8 고급)
- [ ] 단원당 사람 시간 측정 (단원1 대비 단축률)

---

## 7. 단계 [이전] 준비 (vertical slice 종료 후)

- 8 스킬 SSOT(70_tools/) → 안정화 후 외부 통합 검토
- 표준 문서(TONE_STRUCTURE, voice-pool, 8 step guides) → 시스템 자산
- 영상 1편 → 채널/배포 (A7 시리즈 정체성 확정 후)

---

## 8. 한 줄 결론

**8 STEP 파이프라인이 실제로 영상 1편을 끝까지 만들어냈다.** 도구·소재 선정의 시행착오가 컸지만, 그 과정이 voice-pool §0·image-tools-guide·8 step guides 같은 재사용 자산으로 남았다. 단원2부터는 이 자산 위에서 가속한다.
