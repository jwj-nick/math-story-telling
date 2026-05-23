<!-- 02_baseline_unit01.md -->

> ⚠️ **이 발췌는 옛 표기 (v1.5, R0 등) 를 그대로 포함한다.**
> 자연어로 풀이된 본 프로젝트의 현재 계획은 [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) §3 (1편 출발점) 에 있다.
> 본 발췌는 1편 (에라토스테네스) 의 정밀 사실 자료 보존용. 일반 사용 시 INTEGRATED_PLAN §3.1 이 충분하다.

# 발췌 — unit-01 v1.5 baseline 데이터

- **원본**: `../../50_channel/season-1-ancient/unit-01/` 안 6개 텍스트 소스
- **발췌 일자**: 2026-05-23
- **목적**: 본 sub-project 의 모든 비교·실험·표준화의 기준선 (golden reference)

---

## 1. 산출물 인벤토리

| 파일 | 크기 | 역할 |
|---|---|---|
| `storyboard_v1_5.md` | 5.8KB | 6장면 마스터 (시간·시각·이미지·모션·텍스트·나레이션) |
| `narration_v1_5.txt` | 1.4KB / 549자 | edge-tts 입력 — 단문+빈줄 호흡 |
| `narration_v1_5.xml` | 2.7KB | **SSML 풀스펙** (ElevenLabs/Azure 전환 input) |
| `image_prompts.md` | 6.6KB | 5장 영문 프롬프트 + Negative + Style notes + **공통 캐릭터 시트** |
| `config_v1_5.json` | 2.5KB | HyperFrames 렌더 데이터 |
| `index_v1_5.html` | 15KB | v1.5 마스터 템플릿 (HTML + GSAP) |
| `final_v1_5.mp4` | 21MB | 완성본 107.4s |
| `poster_v1_5.jpg` | 85KB | 썸네일 (S1 화면) |
| `narration_v1_5.mp3` | 644KB | TTS 산출물 |
| `_assets/` | — | AI 이미지 5장 (gitignored) |
| `README.md` | 0.9KB | ⚠️ 옛 v1 시절. 갱신 필요 (`apps/math1/unit-01/` 참조는 폐기 경로) |

---

## 2. narration_v1_5.xml SSML 패턴 (Nick "톤·pause·몰입" 의 정체)

### 2.1 break 사용 (~40회)

| 위치 | 길이 | 용도 |
|---|---|---|
| 단문 사이 | 200~800ms | 호흡 |
| 강조구 안 | 200~400ms | 미세 강조 |
| 장면 전환 | 1500ms | 큰 호흡 |

### 2.2 prosody 패턴

| 위치 | 효과 |
|---|---|
| 전체 wrap | `rate="-5%"` (느린 톤) |
| "오차는, 단 일 퍼센트." | `pitch="+5%"` (극적 강조 1회) |
| "소인수분해" | `pitch="+3%"` (키워드 강조 1회) |

### 2.3 호흡 단위

- 한 문장 = 12~20자
- 어미: "는요 / 이에요 / 거예요 / 답니다" — 다정한 어조
- 빈 줄로 장면 전환 분리

→ **13단원 모두 이 패턴으로 SSML 작성** 표준화 필요. ElevenLabs 도입의 직접 입력.

---

## 3. storyboard_v1_5.md 6장면 구조

| Scene | 시간 | 길이 | 글자수 | 목적 | 시각 주체 |
|---|---|---|---|---|---|
| S1 | 0~5s | 5s | 24 | 타이틀 | 정적 배경 + 텍스트 |
| S2 | 5~25s | 20s | 88 | **시대·장소 풍경** (v1.5 NEW) | AI 이미지 wide |
| S3 | 25~50s | 25s | 120 | 인물 등장 | AI 이미지 medium |
| S4 | 50~80s | 30s | 148 | 결정적 순간 | AI 이미지 + 강조 spike |
| S5 | 80~105s | 25s | 130 | 수학 연결 | AI 이미지 + SVG 다이어그램 |
| S6 | 105~115s | 10s | 38 | 마무리 | 최소 시각 + 텍스트 |

→ 합계 **115s / 548자** (목표 95~120s, 480~620자 범위 ✅).

---

## 4. image_prompts.md 핵심 패턴

### 4.1 공통 캐릭터 시트 (영문)

```
An elderly Hellenistic Greek scholar around 70,
gentle weathered face, short grey curly hair, light beard,
wearing a simple white linen chiton with a worn ochre wool mantle.
Calm, observing eyes. Sun-bronzed skin.
```

→ S3·S4 의 인물 등장 장면에서 동일 시트 삽입. 인물 일관성 유지.

### 4.2 각 프롬프트 3블록 표준

```
### Prompt (영문)
[Scene 묘사 + 공통 캐릭터 시트 인용 + 16:9 + style + composition]

### Negative
[no modern items, no text, no anachronism, ...]

### Style notes
[톤·구도·여백 의도 + 학습자가 받는 감각]
```

### 4.3 5장 슬롯

| 슬롯 | 파일 | 장면 | 핵심 |
|---|---|---|---|
| 1 | `s2-alexandria-vista.png` | S2 | 항구·등대·도서관 wide, 황금시간대 |
| 2 | `s3-library-scholar.png` | S3 | 도서관 안 두루마리 + 학자 medium |
| 3 | `s4-shadow-experiment.png` | S4 | 막대기·그림자·각도 측정 흔적 |
| 4 | `s5-numbers-bridge.png` | S5 | 양피지 숫자표 close-up (옛↔현재 다리) |
| 5 | `s6-closing-light.png` | S6 | 등잔불 + 두루마리 (선택, 검정 여백) |

---

## 5. config_v1_5.json 구조

### 5.1 메타

```json
{
  "version": "1.5",
  "duration_target": 115,
  "duration_range": [95, 120],
  "palette": "era-ancient",
  "narration_voice": "ko-KR-SunHiNeural"
}
```

### 5.2 각 장면 motion

| 장면 | scale_from→to | pan_x | 효과 |
|---|---|---|---|
| s2 | 1.0 → 1.06 | -3 | wide ken burns |
| s3 | 1.0 → 1.04 | 0 | 미세 zoom in |
| s4 | 1.0 → 1.05 | +2 | pan + zoom |
| s5 | 1.05 → 1.0 | 0 | zoom out (옛→현재) |
| s6 | 1.0 → 1.03 | 0 | 천천히 zoom in (여운) |

### 5.3 scene_times

```
s1_in=0 / s2_in=5 / s3_in=25 / s4_in=50 / s4_spike=65 / s5_in=80 / s6_in=105 / end=115
```

→ 새 단원: 같은 schema, 시간·텍스트만 교체. **자동 시드 생성 가능**.

---

## 6. 빌드 파이프라인 (현 검증된 흐름)

```
[1] storyboard_v1_5.md       (수동 작성)
[2] narration_v1_5.txt       (수동, 480~620자 목표)
[3] image_prompts.md         (수동 + 캐릭터 시트)
    ↓ (3a) Nick → Claude/ChatGPT 이미지 생성 → _assets/ 저장
[4] config_v1_5.json         (수동, 시드 자동 생성 후보)
[5] index_v1_5.html          (템플릿 + 단원 데이터)
    ↓ edge-tts --rate=-5%
[6] narration_v1_5.mp3
    ↓ ffprobe → AUDIO_DURATION
    ↓ index.html data-duration 자동 갱신
    ↓ hyperframes render
[7] raw_v1_5.mp4             (영상만)
    ↓ ffmpeg -map 0:v -map 1:a -c:v copy -c:a aac -shortest
[8] final_v1_5.mp4 ⭐
    ↓ retrospective 자동 작성 (현재 미구현, skill Phase E 추가 필요)
[9] insight md
```

---

## 7. NCC 추가 분석 — 본 sub-project 가 추적할 baseline 메트릭

| 메트릭 | unit-01 값 | 단원별 표준 후보 |
|---|---|---|
| 길이 | 107.4s | 95~120s |
| narration 글자수 | 549자 | 480~620자 |
| narration 속도 (글/초) | 5.1 | 4.5~5.5 |
| break 횟수 (SSML) | ~40 | 30+ |
| prosody 강조 (SSML) | 2회 (pitch+5%, +3%) | 1~3회 |
| AI 이미지 수 | 5장 | 4~6장 |
| final.mp4 크기 | 21MB | < 25MB |
| 이미지 1장 작업 시간 (Nick) | ~10분 | (목표 결정) |
| 빌드 시간 (TTS + render + ffmpeg) | ? | (측정) |
| 작업 총 시간 (소스 + 빌드 + 회고) | 약 3시간 | (목표 결정) |

→ `60_evaluation/baseline.md` 에 정식 등록 후 후속 단원 비교 기준.

---

## 변경 이력

- 2026-05-23: 발췌. unit-01 v1.5 6개 산출물 + SSML 패턴 정밀 + 빌드 파이프라인 + 메트릭 후보.
