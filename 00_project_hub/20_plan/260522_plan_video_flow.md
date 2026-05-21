<!-- 260522_plan_video_flow.md -->

# Plan — 영상 Flow 정교화 + 13단원 일괄 적용

> 출발점. 다음 라운드에서 넓혀나갈 이슈 메모.
> 작성: 2026-05-22

---

## 1. 비전 한 줄

`https://jwj-nick.github.io/mid1/story/index.html`의 모든 단원 story 페이지를
**`50_channel/season-1-ancient/unit-NN/`의 final mp4 style 영상**으로 교체.

---

## 2. 현재 자산 (Reference)

`50_channel/season-1-ancient/unit-01/` (유일하게 v1.5 완성됨):
- `final_v1_5.mp4` — 완성 영상
- `narration_v1_5.mp3` / `.xml` / `.txt` — TTS 산출물
- `storyboard_v1_5.md` / `index_v1_5.html` / `config_v1_5.json` — 소스
- `image_prompts.md` / `poster_v1_5.jpg`

**unit-02~13은 `50_channel/_archive/v1/unit02~13/` 에 v1 (구버전)만 존재.**

---

## 3. 다음 라운드 토론 이슈

### 3.1 v1.5 표준화
- 현재 v1.5 (unit-01) 구조를 13단원 적용 가능 표준으로 정제
- `10_system/10_principles/STORY_VIDEO_v1_5.md` 와 `se_story_video_v1_5` skill 점검 — 무엇이 모자란가?
- 인물별 시그니처 (signature-color, era-palette, signature-object) 일관 적용 (`30_content/units/NN/meta.json` 활용)

### 3.2 품질 게이트
- TTS 자연스러움 (edge-tts 한국어 voice 후보·세팅)
- 영상 길이·페이스 기준 (단원당 X분, 챕터당 Y초)
- 가독성 (텍스트 크기·노출 시간, 그림 컷 vs 텍스트 컷 비율)
- 음악·SFX 사용 정책

### 3.3 workflow 다듬기
- HyperFrames(GSAP) → FFmpeg → edge-tts 파이프라인 자동화 정도
- 1단원 1세션 vs 1단원 N세션
- 산출물 검수 audit skill 필요 여부 (`se_ncc_audit_video` 같은 신설?)
- chatlog 기반 진행 (Round N 기록)

### 3.4 13단원 일괄 확장 전략
- unit-01 표준 확정 → unit-02~13 순차 vs 병렬
- 시즌1 (Ancient): 에라토스테네스 → 브라마굽타 → 알콰리즈미 → 디오판토스 → 데카르트 → ...
- 인물별 영상 톤 차별화 정도

### 3.5 배포 hookup (수학 챕터 plan과 연계)
- `50_channel/season-1-ancient/unit-NN/final_v1_5.mp4` 를
  현 `mid1/story/unitNN/index.html` 위치로 배포 매핑
- 60_deploy/channel/ 빌드 출력 정의
- 인물 페이지(math1)와 영상 페이지(story) 양방향 link → **수학 챕터 plan 참조**

---

## 4. 연관 문서

- `10_system/10_principles/STORY_VIDEO_v1_5.md` — 영상 v1.5 원칙
- `.claude/skills/se_story_video_v1_5/` — 현 skill
- `50_channel/_archive/v1/` — v1 (구버전) 13단원
- `260522_plan_math_chapter.md` — 수학 챕터 plan (인물 ↔ 영상 link 구조)
