<!-- 0525_step4_skill_draft.md -->

# exp-002 / STEP 4 / Issue — `se-video-narration` SKILL.md draft + 통검토

> **issue**: STEP 1·2·3 frame 단축 적용 — frontmatter 통째 draft + Nick 통검토 → 즉시 시범.
> **step**: STEP 4 (CHECKLIST.md §4)
> **선행**: STEP 3 종료 ([`retro-3-storyboard.md`](../40_experiments/exp-002-build-unit01/retro-3-storyboard.md))
> **선행 양식**: [`../70_tools/se-video-storyboard/SKILL.md`](../70_tools/se-video-storyboard/SKILL.md)
> **STEP 4 특이점**: *외부 도구 호출 필요* (TTS 엔진) — 본 단계가 처음
> **시작**: 2026-05-25

---

## STEP 4 특이점 — 외부 도구 호출

본 단계 = **실제 오디오 source 생성**. 외부 TTS 도구 필요.

CHECKLIST.md §4.4 도구 결정 시점 명시:
- **edge-tts** (옛 1편 사용, 무료, Python 패키지, SSML 일부 지원)
- **ElevenLabs** (감정 표현 우수, API key 필요, 무료 quota ~10000자)

### 시범 환경 (NCC 직접 호출 가능성)

| 도구 | NCC 직접 호출 가능? | 비고 |
|---|---|---|
| edge-tts | ✅ Python CLI (`pip install edge-tts`), Bash tool 로 호출 가능 | 무료, sandbox 외부 통신 필요 |
| ElevenLabs | ⚠️ API key 환경 변수 필요 | Nick 확인 필요 |

NCC 추천 시범 시퀀스:
- **1차** = edge-tts (NCC 직접 시범 가능)
- **2차 (옵션)** = ElevenLabs (Nick API key 가능 시)
- **비교 표** = `70_tools/se-video-narration/comparison.md`

---

## Draft — `se-video-narration` frontmatter (NCC 작성)

```yaml
---
name: se-video-narration
description: 영상 제작 시스템의 단계 [영상 2] 나레이션 스킬. 단계 [영상 1] 스토리보드의 나레이션 시드를 받아 실제 발화용 텍스트 + SSML 풀스펙 + 음성 합성 (mp3) 을 작성한다. 입력 (스토리보드 / 정체성 = 시청자·약속·톤 / TTS 도구 선택 / (옵션) 음성 매핑 / (옵션) 옛 baseline SSML) 을 받아 동작 (입력 align → Q&A → 나레이션 정련 → SSML 마크업 → TTS 합성 → 길이 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 영상 나레이션 작성, SSML 마크업, TTS 합성 + 길이 사전 검증, 인물별 음성 매핑 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/3-storyboard.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/narration_v1_5.xml` baseline) 를 참조만 함. 외부 도구 호출: edge-tts (Python CLI) 또는 ElevenLabs API.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 2 나레이션 (NR1~NR7)
  ssot: 11_video_gen_process/70_tools/se-video-narration/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---
```

---

## 잠정 입력 (3 필수 + 2 옵션)

| # | 입력 | 형식 | 예시 |
|---|---|---|---|
| 1 | 스토리보드 | `3-storyboard.md` (필수) | `40_experiments/exp-002-build-unit01/3-storyboard.md` (부록 A) |
| 2 | 정체성 | 시청자 + 약속 + 톤 (A5) (필수) | INTEGRATED_PLAN §8 + A5 |
| 3 | TTS 도구 | edge-tts / ElevenLabs / 양쪽 (필수) | 본 시범 = edge-tts (NCC 추천) |
| 4 (옵션) | 음성 매핑 | 인물별 음성 (성별·나이·음역) | 본 시범 = 1명 (NCC 가 한국어 여성/남성 voice 추천) |
| 5 (옵션) | 옛 baseline SSML | 경로 | `50_channel/season-1-ancient/unit-01/narration_v1_5.xml` (미참조) |

---

## NCC 추천 결정

| 항목 | 결정 |
|---|---|
| name | `se-video-narration` |
| stage | `영상 2 나레이션 (NR1~NR7)` |
| 동작 수 잠정 | 7 |
| 입력 수 | 3 필수 + 2 옵션 |
| **1차 시범 도구** | **edge-tts** (무료, Python, NCC 직접 호출) |
| 2차 시범 도구 (옵션) | ElevenLabs (Nick API key 가능 시) |
| 양식 통일 | ✅ se-video-storyboard 와 동일 패턴 |
| prefix | NR (Nick 합의 옵션 A) |

---

## Nick 통검토 요청 (3 항목)

1. **frontmatter + 입력 5 + stage NR** — 모두 OK?
2. **1차 시범 도구 = edge-tts** — OK? (또는 다른 선택?)
3. **ElevenLabs API key 환경** — 가능? (2차 시범 옵션, 없으면 1차만 진행)

OK 받으면 즉시 진행:
1. `70_tools/se-video-narration/` 신설 + SKILL.md (frontmatter + body placeholder)
2. 시범 = `3-storyboard.md` 부록 A → `4-narration.txt` (550자) → `4-narration.xml` (SSML) → edge-tts CLI 호출 → `4-narration.mp3` 생성 → 길이 측정 (~110s ±10%)
3. body reverse-engineering
4. 검증 + retro + STEP 5 진입

## Nick 답변

1. frontmatter + 입력 + stage NR — **모두 OK**
2. 1차 시범 도구 — **양쪽 동시 시범 + 비교** 원함
3. ElevenLabs API key — *아직 모름*

## NCC 환경 확인 결과 (2026-05-25)

| 도구 | 상태 |
|---|---|
| edge-tts | ✅ 설치됨 (Python 3.14.2) |
| **ElevenLabs API key** | ❌ 환경 변수 없음 |
| ffmpeg + ffprobe | ✅ 설치됨 |

## 진행 방식 결정 (Nick OK 채택)

- **1차 = edge-tts 즉시 진행** (NCC 직접 호출, 무료)
- **2차 = ElevenLabs 후속** (Nick key 설정 후 별도 시범 — 동일 입력 재사용 가능)

## 부가 작업 (Nick 요청)

→ `70_tools/se-video-narration/tts-tools-guide.md` 신설:
- 무료/유료 옵션 비교
- 금액 상세
- ElevenLabs setup 가이드 (Nick 용)
- 한국어 voice 비교
- SSML 지원 비교

---

# 본 turn 작업

1. ✅ `70_tools/se-video-narration/` + SKILL.md (frontmatter + body placeholder)
2. ✅ `70_tools/se-video-narration/tts-tools-guide.md` 신설
3. ➡️ 다음 turn = edge-tts 시범 실행 (4-narration.txt + xml + mp3 + 길이 검증)
