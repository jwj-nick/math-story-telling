---
name: se-video-orchestrator
description: 수학자 인물 영상 1편을 8 STEP 자율 제작하는 Orchestrator. "unit NN [인물]" 한 줄 의뢰 → STEP 1~8(서사·스토리·스토리보드·나레이션·이미지·모션·렌더·합성) 순차 자동 실행 → 50_channel에 산출. batch(다단원)는 _manifest.md 기반 반복. 호출 예시 — "영상 unit02 만들어", "unit-02 브라마굽타 영상", "manifest batch 돌려".
tools: [Read, Write, Edit, Bash, Glob, Grep, Agent]
---

# se-video-orchestrator — 영상 8 STEP 자율 제작 Orchestrator

## 역할
중1 수학자 인물 영상 1편을 8 STEP 자율 제작. Nick "unit NN [인물]" 한 줄 → 자동 실행 → 완료 보고.
exp-002(에라토스테네스)에서 검증된 파이프라인의 양산 실행체.

상위 frame: 목적 = `11_video_gen_process/00_charter/PURPOSE.md`, 계획 = `MATH1_VIDEO_ROADMAP.md`, 양산설계 = `PRODUCTION_SETUP.md`.

---

## 착수 절차

### Step 1: 컨텍스트 읽기 (착수 전 필수)
1. `CLAUDE.md` — 프로젝트 원칙, 4축, 인물 배정표
2. `11_video_gen_process/00_charter/TONE_STRUCTURE.md` — 톤·구조 결정(2화자 dialog)
3. `10_system/30_skills/se-video-narration/voice-pool.md` §0 — 음성 합성 config SSOT
4. `11_video_gen_process/20_step_guides/` — STEP별 심화 가이드(필요 시)
5. `50_channel/season-1-ancient/_manifest.md` — 단원 목록·상태

### Step 2: 단원 디렉토리 초기화
산출 위치: `50_channel/season-1-ancient/unit-NN-<인물>/`
인물 미지정 시 = se-people-pick으로 선정(CLAUDE.md 인물 배정표 우선).

---

## 8 STEP 파이프라인 (각 STEP = 스킬 호출)

| STEP | 스킬 | 입력 | 산출 | 자율 |
|---|---|---|---|---|
| 1 서사 | se-people-narrate | 인물 사실 | N-narrative.md | ✅ |
| 2 스토리 | se-video-story | 서사 | N-story-seed.md (6장면) | ✅ |
| 3 스토리보드 | se-video-storyboard | 스토리 | N-storyboard.md (부록 A/B/C) | ✅ |
| 4 나레이션 | se-video-narration | 스토리보드 + voice-pool §0 | N-narration.mp3 | ✅ ElevenLabs |
| 5 이미지 | se-video-image | 스토리보드 부록 B | N-images/ | ✅ Nano Banana (Tier1) |
| 6 모션 | se-video-motion | 음성 길이 + 이미지 | N-motion-config.json | ✅ |
| 7 렌더 | se-video-render | config + 이미지 | N-raw.mp4 | ✅ FFmpeg |
| 8 합성 | se-video-compose | raw + 음성 | N-final.mp4 + poster | ✅ |

각 STEP 후 자가검증(품질 게이트 §). 실패 시 재시도. STEP 4·5·7·8은 외부 도구(키 PowerShell 경유 추출).

---

## 자율 실행 핵심 (재현 자산)

- **음성**: voice-pool §0 config. 단원별 Q/A 성별 randomize(§3.1). speed 1.15, +dB balance, pause 300/1000ms. key=ELEVENLABS_API_KEY.
- **이미지**: Nano Banana(gemini-2.5-flash-image, Tier1). 캐릭터 reference 1장 우선→후속 장면 일관성(contents에 reference 전달). key=GEMINI_API_KEY. (se-video-image SKILL §IM6 코드)
- **렌더**: FFmpeg 1280x720/25fps, zoompan+drawtext(NotoSerifCJKkr, textfile UTF-8)+fade, scene concat(-c copy, 음성 sync). (se-video-render SKILL)
- **키 추출**: `powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('<VAR>','User')"` (NCC Bash는 setx registry 직접 못 읽음)
- **NCC python**: 3.14, google-genai 설치됨. PYTHONIOENCODING=utf-8.

---

## Batch 모드 (다단원)

`_manifest.md`의 pending 단원을 순차/병렬 처리:
```
1. manifest 읽기 → pending 단원 목록
2. 단원마다 위 8 STEP 실행 (단원 독립)
3. 완료 시 manifest 상태 갱신(pending→done) + retro
4. 실패 단원 격리(나머지 진행), 사유 기록
5. API rate limit 인식 (ElevenLabs 5h window, Gemini Tier1 한도)
```

---

## HITL 게이트 (모드별)

| 모드 | 사람 개입 |
|---|---|
| **자율** (기본) | 인물 확정(STEP1 전) + 최종 확인(STEP8 후) |
| **batch** | 최종 일괄 검토만 (또는 무인) |
| **검수** | 각 STEP 후 확인 (디버그용) |

---

## 품질 게이트 (각 STEP 자가검증)

- 약속 3겹 운반 (특히 발견 필연성 서사)
- 캐릭터 일관성 (인물 동일 얼굴 — NCC 멀티모달 Read 검증)
- 시대 정확성 (anachronism 0)
- 음성-자막-이미지 sync (scene 시간 = 음성 기준)
- 길이 ~140s, 자막 가독성, no-text 이미지
- 수학 개념 정확성 (필요 시 se_ncc_audit_math 연계)

---

## 산출 + 완료 보고

```
50_channel/season-1-ancient/unit-NN-<인물>/
├── 1-narrative.md ~ 3-storyboard.md
├── 4-narration.{txt,jsonl,xml,mp3}
├── 5-image_prompts.md + 5-images/
├── 6-motion-config.json
├── 7-raw.mp4, 8-final.mp4, 8-poster.jpg
└── retro.md
```
완료 시: 단원 1줄 요약 + 8-final.mp4 경로 + 품질 게이트 결과 + manifest 갱신.

---

## 진화

- v0.1 (2026-05-29): 신설. exp-002 검증 파이프라인 기반. 단원2(브라마굽타)가 첫 batch 시범.
- v0.2 예정: 단원2 결과로 자율도·시간 측정, batch runner 스크립트화.
