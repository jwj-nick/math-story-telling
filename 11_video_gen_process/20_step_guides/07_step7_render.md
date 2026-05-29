<!-- 20_step_guides/07_step7_render.md / STEP 7 [영상 5 렌더] 심화 가이드 -->

# STEP 7 — [영상 5] 렌더 (Render) 심화 가이드

> **상위 frame**: [`../00_charter/PURPOSE.md`](../00_charter/PURPOSE.md) · [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) · 템플릿 [`./00_index.md`](./00_index.md)
> **이 STEP의 skill**: `se-video-render` (⚠️ SKILL.md **미작성** — 시범 단계. §3에 설계 제안)
> **실제 산출물 (exp-002)**: `40_experiments/exp-002-build-unit01/clips/S1.mp4` (1280×720, 18.24s, 검증 성공)
> **상태**: 🟡 시범 — FFmpeg zoompan+fade로 S1 클립 1개 렌더 검증 완료, 나머지 5장면·concat 자동화 대기

---

## 1. Step 개요

### 1.1 이 step이 무엇을 하는가

STEP 7 [렌더]는 **정지 이미지(STEP 5)에 카메라 모션을 입히고 한글 자막을 새겨, 음성이 없는 영상(raw mp4)으로 굳히는 단계**다. 입력은 세 가지가 모인다 — 이미지 4~6장(`5-images/`), 자막·전환 명세(`3-storyboard.md`), 그리고 이 둘을 시간 축에 정렬한 모션 config(`6-motion-config.json`). 출력은 음성을 *아직 입히지 않은* 영상이다. 음성 합성은 다음 STEP 8 [합성]에서 별도로 mux한다.

핵심 도구는 **FFmpeg** 단 하나다. GSAP·HyperFrames·브라우저 렌더 없이, 정지 이미지를 `-loop 1`로 늘려놓고 `zoompan`(Ken Burns 줌/팬), `drawtext`(한글 자막), `fade`(장면 in/out)를 필터 그래프로 쌓아 장면별 클립을 만든 뒤 `concat`으로 이어붙인다.

### 1.2 4축 중 어디에 기여하는가

| 축 | 기여도 | 설명 |
|---|---|---|
| **B. 흥미** | ★★★ 직접 | 렌더가 곧 "보이는 영상". 정지 그림에 모션·자막이 붙어야 비로소 영상이 된다. 약속 3겹(시대 감각 / 인물 정서 / 발견의 필연성)을 시청자 눈에 전달하는 마지막 시각 관문 |
| A·C·D | 간접 | 영상은 앱·문제 트랙의 *흥미 보조*(INTEGRATED_PLAN §1.3). 렌더 자체는 개념·언어·문제를 직접 만들지 않음 |

### 1.3 8단계 파이프라인에서의 위치

```
… STEP 5 이미지 ──┐
   STEP 3 스토리보드(자막·전환) ──┼──▶  [STEP 7 렌더]  ──▶  STEP 8 합성(음성 mux + BGM/SFX)
   STEP 6 모션 config ────────────┘        raw mp4              final mp4
```

- **선행**: STEP 6 [모션] — `6-motion-config.json`이 렌더의 *직접 입력*. scene별 start/end·zoom·motion·captions가 모두 여기 들어 있다. STEP 5 [이미지]는 픽셀 원천, STEP 3 [스토리보드]는 자막 텍스트·전환 종류의 권위 명세.
- **후행**: STEP 8 [합성] — raw mp4에 `4-narration.mp3`(음성)을 mux하고 BGM·SFX를 mix한다. **렌더 단계의 가장 큰 책임은 "음성과 시간이 어긋나지 않는 raw mp4"를 내놓는 것**이다.

### 1.4 본질적 난제 2개

1. **음성 sync 보존** — 영상은 음성과 길이가 0.1초만 어긋나도 시청자가 알아챈다. 그런데 음성은 STEP 8에서 붙는다. 따라서 STEP 7은 **각 scene 클립의 길이를 모션 config의 `end - start`에 정확히 일치시켜야** 한다. zoompan은 프레임 수(`d=`) 단위로 길이를 정하므로 "초 × fps" 반올림 오차가 누적되면 마지막에 수십 ms가 밀린다. (exp-002에서 검증된 S1: 18.23초 명세 → 실제 18.24초. 0.01초 오차는 25fps 양자화의 1프레임에 해당.)
2. **한글 자막 렌더** — FFmpeg `drawtext`는 한글을 *직접 인자로 주면* 깨지기 쉽다(쉘 인코딩 + 폰트 fallback). NotoSerifCJKkr 폰트 파일을 명시(`fontfile`)하고, 텍스트는 UTF-8 textfile로 분리(`textfile=`)해야 안정적으로 박힌다. 이것이 STEP 7의 두 번째 핵심 노하우다.

---

## 2. Workflow (절차)

### 2.1 입력 align → 처리 → 출력 흐름

```
[입력 align]
  6-motion-config.json   ← fps, resolution, scenes[], transition, font, palette
  5-images/*.png         ← scene별 img 경로
  3-storyboard.md        ← 자막 텍스트·전환 종류의 권위(검증용)
        │
        ▼
[scene 루프]  for each scene in config.scenes:
  1) 길이 계산     dur = end - start,  frames = round(dur * fps)
  2) 베이스 변환   scale(상위 커버) → crop(1280×720 정렬) → setsar=1
  3) zoompan       motion → z 표현식 매핑 (push_in/zoom_out/ken_burns/pan_right/slow_zoom)
  4) drawtext      captions[] → caption별 textfile(UTF-8) + enable=between(t,s,e)
  5) fade          fade=in:0:N + fade=out:(frames-N):N  (transition.in/out)
  6) encode        libx264 + yuv420p + 25fps, clips/<id>.mp4
        │
        ▼
[concat]  clips/S1.mp4 … S6.mp4  →  concat demuxer  →  7-render-raw.mp4 (음성 없음)
        │
        ▼
[검증]  ffprobe 길이 == config.total_duration ± 1프레임 ?  해상도·fps·pix_fmt ?
```

### 2.2 실제 동작 순서 (skill의 RD/CL/CC 액션 — §3 설계 제안과 1:1)

| 약칭 | 액션 | 내용 |
|---|---|---|
| **RD** (read) | config 로드 | `6-motion-config.json` 파싱. fps·resolution·scenes·transition·font 확보 |
| **CL** (clip) | scene별 클립 렌더 | scene 루프. 위 6단계(scale/crop → zoompan → drawtext → fade → encode) |
| **CC** (concat) | 이어붙이기 | `concat.txt` 작성 → `-f concat -c copy`로 무손실 결합 |
| **VF** (verify) | 검증 | ffprobe로 길이·해상도·fps·프레임 수 확인. config와 대조 |

### 2.3 의사결정 포인트 (분기)

| 분기 | 선택지 | exp-002 결정 |
|---|---|---|
| 클립 단위 | (a) scene별 따로 렌더 후 concat / (b) 한 필터그래프에 전부 | **(a) scene별**. concat이 음성 sync 보존·디버깅·증분 렌더에 유리 |
| 전환 구현 | (a) 각 클립 fade in/out (concat) / (b) `xfade`로 클립끼리 겹침 | exp-002 = **(a) fade**. xfade는 겹치는 시간만큼 *총 길이가 줄어* 음성 sync가 틀어짐(§7.4) |
| cut vs fade | scene 명세별 | storyboard: S2→S3 = cut(겹침 0), S1→S2·S4→S5·S5→S6 = fade |
| 자막 textfile | (a) UTF-8 파일 분리 / (b) 인자 직접 | **(a)**. 한글 안전 (§1.4 난제 2) |
| 줌 기준점 | center / 인물 얼굴 / 명세 | exp-002 = center 고정(`x=iw/2-...`). 향후 saliency 기반(§8) |

---

## 3. Skill / Agent / Tools / Context

### 3.1 사용하는 skill — `se-video-render` (SKILL.md 미작성, 설계 제안)

> ⚠️ 본 STEP은 **SKILL.md가 아직 없다.** exp-002에서 S1 클립 1개를 손으로 렌더해 FFmpeg 파이프라인이 동작함을 검증한 시범 단계다. 아래는 그 검증 결과를 토대로 한 **`se-video-render` skill 설계 제안**이다. (작성 시 [agentskills.io spec](https://agentskills.io/specification) 준수 — INTEGRATED_PLAN 결정 7. name kebab-case, body < 500줄, 상세는 references/로 분리.)

#### 3.1.1 frontmatter 제안

```yaml
---
name: se-video-render
description: 모션 config(JSON)·이미지·스토리보드를 입력받아 FFmpeg로 장면별 클립(zoompan+drawtext+fade)을 렌더하고 concat으로 음성 없는 raw mp4를 만든다. 호출 예시 — "/se-video-render exp-002", "/se-video-render unit01 S3만".
allowed-tools: [Bash, Read, Write]
metadata:
  step: 7
  pipeline: video
  tool: ffmpeg
  resolution: "1280x720"
  fps: 25
---
```

#### 3.1.2 핵심 동작 4 (RD → CL → CC → VF)

| 동작 | 입력 | 출력 | 비고 |
|---|---|---|---|
| RD config 로드 | `6-motion-config.json` | scene 배열 메모리 | fps/res/font/palette 추출 |
| CL scene 렌더 | scene + 이미지 | `clips/<id>.mp4` | 6단계 필터 그래프 (§2.1). 증분(이미 있고 입력 변경 없으면 skip) |
| CC concat | `clips/*.mp4` | `7-render-raw.mp4` | concat demuxer, `-c copy` 무손실 |
| VF 검증 | raw mp4 + config | 검증 리포트 | 길이 ±1프레임 / 해상도 / fps / pix_fmt |

#### 3.1.3 QnA / 리서치 패턴 (skill 내재화 시드)

- **QnA**: "scene 길이 합 == total_duration 인가" / "한글 자막이 모두 박혔는가(빈 글리프 □ 없는가)" / "cut인데 fade가 들어간 곳 없는가" / "줌이 명세 zoom 범위 안에서 끝나는가"
- **리서치**: 렌더 도구 비교(FFmpeg vs Remotion vs HyperFrames+GSAP, §8) → 안정성·속도·재현성 기록 → references/render-tools-compare.md 누적

### 3.2 사용하는 외부 도구 — FFmpeg (선택 근거)

| 도구 | 역할 | 선택 근거 |
|---|---|---|
| **FFmpeg** | 전체 렌더 엔진 | 외부 의존 0·설치 1개·재현성 100%. 브라우저/Node 런타임 불필요. zoompan·drawtext·fade·concat이 모두 내장. CLI라 skill(Bash)로 곧장 호출·자동화 가능 |
| libx264 | 인코더 | 호환성 최강(모든 플레이어·YouTube). CRF로 품질 제어 |
| NotoSerifCJKkr-Regular.otf | 한글 자막 폰트 | storyboard 명세 = serif + gold. CJK 한글 글리프 완비. `C:/Windows/Fonts/`에 존재 |

INTEGRATED_PLAN §5.5.5는 렌더 도구로 "HyperFrames + GSAP"을 *잠정* 명시했으나, exp-002 시범에서 **FFmpeg 단독으로 zoompan+drawtext+fade가 충분히 동작함을 검증**했다. GSAP은 코드 기반 정밀 모션이 필요해질 때(§8.3) 전환 후보로 남긴다.

### 3.3 참조 context (SSOT)

| 파일 | 역할 |
|---|---|
| `6-motion-config.json` | **직접 입력**. scene 시간·zoom·motion·captions·font·palette·transition |
| `3-storyboard.md` | 자막 텍스트·전환 종류(cut/fade)의 권위 명세 (검증 대조) |
| `5-images/*.png` | 픽셀 원천 |
| `4-narration.mp3` (140.27s) | 직접 사용 X. 그러나 **total_duration의 진실 기준** — 렌더 길이가 여기 맞아야 STEP 8 sync 성립 |

### 3.4 agent 활용

렌더는 결정론적 변환(입력→출력 1:1)이라 Q&A가 거의 없다. **skill(Bash 실행) 단독이 자연스럽다.** 단, scene 수가 많거나 여러 음성안(exp-002의 turns_norm_* 5종)을 병렬 렌더할 때는 scene별/안별 background agent 병렬화가 가능(§8.5).

---

## 4. User Input (Nick 입력)

### 4.1 무엇을 / 언제 / 어떤 형식으로

| 입력 | 시점 | 형식 | 필수/선택 |
|---|---|---|---|
| 렌더 트리거 | STEP 6 완료 후 | "렌더 돌려" / `/se-video-render exp-002` | 필수 |
| 폰트 경로 | 최초 1회 | config의 `font` 필드 | 필수 (기본 NotoSerifCJKkr) |
| 품질 프로파일 | 선택 | draft(빠른 미리보기) / final(CRF 18) | 선택 (기본 final) |
| 부분 렌더 | 선택 | "S3만 다시" | 선택 (증분 렌더) |

### 4.2 HITL (사람 개입) 지점

렌더는 자동 단계다. HITL은 **출력 검수 1회** — Nick이 raw mp4를 보고 "모션 속도/자막 위치/줌 방향"이 의도와 맞는지 판단. 어긋나면 STEP 6 모션 config을 고쳐 재렌더(렌더 단계 자체는 config을 신뢰).

---

## 5. Step Output (산출물)

### 5.1 산출 파일 형식 + 위치 규약

```
exp-002-build-unit01/
├── clips/                 ← scene별 중간 산출 (증분 렌더 캐시)
│   ├── S1.mp4   (18.24s)  ← exp-002 검증 완료 ✅
│   ├── S2.mp4 … S6.mp4    ← (대기)
├── captxt/                ← 자막 UTF-8 textfile (caption별)
│   ├── S2-cap1.txt  "β"
│   ├── S2-cap2.txt  "베타 — 모든 분야 2등"
│   └── …
├── concat.txt             ← clips 결합 목록 (이미 음성용으로 존재 → 영상용 별도)
└── 7-render-raw.mp4       ← 최종 산출 (음성 없음, 1280×720, 25fps, ~140.27s)
```

- 클립: `clips/<scene-id>.mp4`. scene-id는 config의 `id`(S1~S6).
- 자막 텍스트: `captxt/<scene-id>-cap<N>.txt` (UTF-8, BOM 없음).
- raw 영상: `7-render-raw.mp4` (STEP 번호 prefix 규약).

### 5.2 다음 step 입력 연결

STEP 8 [합성]이 `7-render-raw.mp4` + `4-narration.mp3`를 mux한다:

```bash
ffmpeg -i 7-render-raw.mp4 -i 4-narration.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest 8-final.mp4
```

`-c:v copy`로 영상은 **재인코딩 없이 그대로** 가져간다 → 렌더 품질 손실 0. 따라서 STEP 7의 인코딩 품질이 곧 최종 품질이다.

### 5.3 품질 검증 기준

| 기준 | 자동 (ffprobe) | Nick 검수 |
|---|---|---|
| 길이 | total == 140.27 ± 1프레임(0.04s) | — |
| 해상도 | 1280×720 | — |
| fps | 25, CFR (가변 X) | — |
| pix_fmt | yuv420p (호환성) | — |
| 자막 | 빈 글리프(□) 0개 | 위치·타이밍 의도 일치 |
| 모션 | zoom 범위 명세 내 | 속도·방향 자연스러움 |
| 전환 | cut/fade 명세 일치 | 끊김 없음 |

---

## 6. 현재 구현 (exp-002 실제 사례)

### 6.1 unit01 (에라토스테네스) 에서 실제로 한 것

검증 성공한 **S1 클립 1개**의 실제 파이프라인. config의 S1 = `push_in`, zoom [1.0→1.08], 18.23초, 자막 없음.

#### 6.1.1 베이스 변환 (scale → crop → setsar)

원본 PNG를 1280×720 캔버스에 맞추되, zoompan이 줌인할 *여유 픽셀*을 위해 상위 해상도로 키워 둔다. 좌표 떨림(jitter) 방지를 위해 zoompan은 큰 입력에서 동작시키는 것이 정석이다.

```
scale=2560:-1,crop=2560:1440          # 2배 캔버스 (줌 시 선명도 확보)
```

#### 6.1.2 zoompan — push_in (z 표현식)

```
zoompan=
  z='min(zoom+0.0011,1.08)'           # 매 프레임 +0.0011, 1.08에서 멈춤
  :d=456                              # 18.23s × 25fps ≈ 456 프레임
  :x='iw/2-(iw/zoom/2)'               # 줌 기준점 = 가로 중앙
  :y='ih/2-(ih/zoom/2)'               # 세로 중앙
  :s=1280x720                         # 출력 해상도 (다운스케일)
  :fps=25
```

`z` 증분은 (목표줌 − 시작줌) / 프레임수로 계산: (1.08−1.0)/456 ≈ 0.000175... 를 부드럽게 보이도록 약간 키운 값으로 잡고 `min()`으로 상한을 건다. **이 한 줄이 Ken Burns 효과의 심장**이다.

#### 6.1.3 fade in/out (transition.in/out = 0.6s)

```
fade=t=in:st=0:d=0.6 , fade=t=out:st=17.63:d=0.6
```

`st=17.63` = (18.23 − 0.6). 클립 끝 0.6초 동안 페이드아웃. **concat 시 클립 길이는 그대로 보존**되므로 음성 sync가 깨지지 않는다(§1.4 난제 1).

#### 6.1.4 인코딩 (검증된 출력)

```
-c:v libx264 -pix_fmt yuv420p -r 25 -crf 18 clips/S1.mp4
```

→ **검증 결과: 1280×720, 18.24초, libx264, yuv420p, 25fps. ✅**

#### 6.1.5 S1 전체 명령 (재구성)

```bash
ffmpeg -loop 1 -i 5-images/4-S1-Museion.png -t 18.23 \
  -vf "scale=2560:-1,crop=2560:1440,\
zoompan=z='min(zoom+0.0011,1.08)':d=456:\
x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=25,\
fade=t=in:st=0:d=0.6,fade=t=out:st=17.63:d=0.6,\
format=yuv420p" \
  -c:v libx264 -crf 18 -r 25 clips/S1.mp4
```

#### 6.1.6 한글 자막이 있는 scene (S2~S6) drawtext 패턴

S1은 자막이 없지만, S2부터는 한글 자막이 들어간다. 검증된 안전 패턴:

```bash
# 1) 자막 텍스트를 UTF-8 파일로 분리 (한글 안전)
#    captxt/S2-cap1.txt = "β"
#    captxt/S2-cap2.txt = "베타 — 모든 분야 2등"

# 2) drawtext를 zoompan 뒤에 체인
... ,zoompan=...:s=1280x720:fps=25,
drawtext=fontfile='C\:/Windows/Fonts/NotoSerifCJKkr-Regular.otf':
  textfile='captxt/S2-cap1.txt':
  fontcolor=0xE89B4F:fontsize=130:
  x=(w-text_w)/2:y=h*0.30-text_h/2:
  shadowcolor=0x000000:shadowx=2:shadowy=2:
  enable='between(t,23.5,30.0)',
drawtext=fontfile='C\:/Windows/Fonts/NotoSerifCJKkr-Regular.otf':
  textfile='captxt/S2-cap2.txt':
  fontcolor=0xFFFFFF:fontsize=40:
  x=(w-text_w)/2:y=h*0.82-text_h/2:
  shadowcolor=0x000000:shadowx=2:shadowy=2:
  enable='between(t,26.0,33.0)'
```

핵심 4가지:
1. **fontfile 명시** — 시스템 폰트 이름 의존 X. Windows 경로의 콜론은 `C\:`로 이스케이프.
2. **textfile로 한글 분리** — 쉘·필터 파싱이 한글을 건드리지 않음 (□ 깨짐 방지).
3. **config의 좌표 매핑** — `x:"center"` → `x=(w-text_w)/2`, `y:"0.30"` → `y=h*0.30-text_h/2`. color는 palette(`gold`=0xE89B4F, `white`=0xFFFFFF) 사용.
4. **enable=between(t,start,end)** — caption의 start/end(영상 절대 시각). 단, drawtext의 `t`는 *클립 로컬 시간*이므로 scene start를 빼야 함: 실제로는 `between(t, 23.5−18.23, 30.0−18.23)`. **이 좌표 변환이 자막 타이밍의 함정**(§7.2).

### 6.2 시행착오·결정

| 항목 | 발견 | 대응 |
|---|---|---|
| 렌더 도구 | INTEGRATED_PLAN은 HyperFrames+GSAP 잠정. 그러나 외부 런타임 무거움 | **FFmpeg 단독 검증 성공** → 1차 표준 채택 |
| 한글 자막 | drawtext 인자 직접 입력 시 깨짐 위험 | **textfile UTF-8 + fontfile 명시** 패턴 |
| 음성 sync | xfade는 총 길이를 줄여 sync 붕괴 | **scene별 fade + concat(`-c copy`)** 으로 길이 보존 |
| 줌 jitter | zoompan을 작은 입력에서 돌리면 떨림 | scale 2배 → zoompan → 1280×720 다운스케일 |
| 자막 t 기준 | drawtext `t`는 클립 로컬 시간 | scene.start 만큼 offset 빼기 |
| 음성안 다중 | turns_norm_* 5종(kanna/mina/onyu/yura + EL) | 영상은 음성 무관 1회 렌더 → STEP 8에서 음성안만 교체 (렌더 재사용) |

### 6.3 강점과 한계

**강점**: 외부 의존 0 · 100% 재현성 · scene별 증분 렌더 · 음성과 분리되어 음성안 교체 시 재렌더 불필요 · S1 검증으로 파이프라인 신뢰.

**한계**:
1. zoompan은 *정수 프레임 양자화* — 0.01초 미세 오차 누적(S1 18.23→18.24).
2. zoompan의 미세 떨림(서브픽셀)은 scale-up으로 완화하나 완전 제거 X.
3. S3 격자 애니메이션(2·3·5 배수 gray out, storyboard 명세)은 FFmpeg zoompan으로 **표현 불가** — 정적 이미지 줌만 가능. SVG/코드 모션 필요(§8.3).
4. drawtext는 텍스트 *애니메이션*(fade-in 자막, 자간, 곡선 배치) 불가 — alpha 표현식으로 제한적 페이드만.
5. SKILL.md 미작성 → 현재는 수동 명령. 자동화 미완(§7.1).

---

## 7. 개선 방향 탐색 / 아이디어

### 7.1 단기 개선 — SKILL.md 작성 + config→FFmpeg 컴파일러

가장 시급한 것은 **`6-motion-config.json`을 읽어 FFmpeg 명령을 자동 생성하는 컴파일러**다. scene별로 §6의 명령을 손으로 쓰는 대신, config을 순회하며:

```python
# render_compile.py (의사코드)
for scene in config["scenes"]:
    dur = scene["end"] - scene["start"]
    frames = round(dur * config["fps"])
    z_inc = (scene["zoom"][1] - scene["zoom"][0]) / frames
    vf = [
        "scale=2560:-1,crop=2560:1440",
        zoompan_expr(scene["motion"], scene["zoom"], frames),  # motion→z/x/y
    ]
    for i, cap in enumerate(scene["captions"]):
        write_utf8(f"captxt/{scene['id']}-cap{i+1}.txt", cap["text"])
        vf.append(drawtext_expr(cap, scene["start"], config))   # t offset 반영
    vf += [fade_in(config), fade_out(config, dur), "format=yuv420p"]
    ffmpeg_render(scene["img"], dur, ",".join(vf), f"clips/{scene['id']}.mp4")
concat_clips(config["scenes"], "7-render-raw.mp4")
verify(config)
```

이 컴파일러가 `se-video-render` SKILL.md의 references/render_compile.py가 된다. motion 5종(push_in/zoom_out/ken_burns/pan_right/slow_zoom)을 z·x·y 표현식 테이블로 매핑(§9.1).

### 7.2 자막 타이밍 오류 자동 방지

§6.1.6의 함정 — drawtext `t`가 클립 로컬 시간인 점. 컴파일러가 `enable='between(t, {cap.start - scene.start}, {cap.end - scene.start})'`로 **자동 offset**하면 사람이 틀릴 여지가 사라진다. + 검증 단계에서 "caption.start ≥ scene.start AND caption.end ≤ scene.end" assert.

### 7.3 효율 — draft/final 2-pass + 증분 렌더

| 프로파일 | 설정 | 용도 |
|---|---|---|
| draft | scale 1배, `-preset ultrafast`, CRF 28 | 모션·자막 위치 빠른 확인 |
| final | scale 2배, `-preset slow`, CRF 18 | 배포 품질 |

증분: clips/<id>.mp4가 이미 있고 그 scene의 config·이미지 mtime이 더 오래됐으면 skip. scene 1개만 고쳤을 때 1개만 재렌더 → 분 단위가 초 단위로.

### 7.4 리스크와 대응

| 리스크 | 영향 | 대응 |
|---|---|---|
| 음성 sync 붕괴 | 치명 (시청자 즉시 인지) | scene별 length == config 검증 자동화. **xfade 금지**(총 길이 변동) — fade+concat 고수. 정 xfade 쓰면 `offset` 보정으로 총 길이 복원 |
| 한글 □ 깨짐 | 자막 무용 | fontfile 명시 + textfile + 렌더 후 자막 프레임 OCR/픽셀 검사 |
| 프레임 반올림 누적 | 마지막 수십 ms 밀림 | 마지막 scene 길이를 `total_duration − 누적합`으로 역산 보정 |
| zoompan jitter | 화질 거슬림 | scale 2~4배 입력 + `-flags +bitexact` 비활성, 충분한 입력 해상도 |

---

## 8. 고급 Workflow (상상력·창의력)

### 8.1 코드 기반 모션 vs FFmpeg — 정직한 비교

| 차원 | FFmpeg (현재) | GSAP/HyperFrames (브라우저 렌더) | Remotion (React 프로그래matic) |
|---|---|---|---|
| 모션 표현력 | zoom/pan/fade만. 키프레임 곡선 제한 | 무제한 (easing, 경로, SVG morph, 격자 애니메이션) | 무제한 (React 컴포넌트 = 프레임) |
| 자막 타이포 | drawtext 정적 + alpha | CSS/SVG 완전 (가변 폰트·자간·곡선·마스크) | CSS/SVG 완전 + 컴포넌트 재사용 |
| 재현성 | ★★★ (CLI 1개) | ★★ (브라우저 버전 의존) | ★★ (Node+Chromium) |
| 속도 | ★★★ (네이티브) | ★ (브라우저 페인트 후 캡처) | ★★ (병렬 프레임) |
| 외부 의존 | 0 | 무거움 (Puppeteer/Chromium) | 무거움 (Node 생태계) |
| **적합 영역** | 정지 이미지 Ken Burns + 정적 자막 | **S3 격자 애니메이션 등 동적 다이어그램** | 시리즈 템플릿화·데이터 주도 영상 |

**전략: 하이브리드.** 정지 이미지 scene(S1·S2·S4·S5·S6)은 FFmpeg, 동적 다이어그램 scene(S3 소수의 체 격자)은 Remotion/GSAP로 mp4 클립을 따로 렌더 → 같은 concat에 합류. **렌더 단계가 "여러 엔진의 클립을 표준 규격(1280×720/25fps/yuv420p)으로 통일해 concat하는 오케스트레이터"가 된다.** §7.1성 핵심 시각화 30초(INTEGRATED_PLAN §7.1)가 바로 이 자리에 들어온다.

### 8.2 프로그래matic 비디오 — Remotion 도입 시나리오

Remotion은 React 컴포넌트의 매 프레임을 렌더한다. `<Scene start={18.23} end={33.87} motion="zoom_out">`처럼 **모션 config을 그대로 props로** 받는 컴포넌트를 만들면, config 1개가 FFmpeg와 Remotion 양쪽의 단일 입력이 된다. 자막은 `<Caption>` React 컴포넌트로 — fade-in, 글자별 stagger, 가변 폰트 weight 애니메이션이 CSS로 자유. 시리즈 정체성(폰트·색·로워서드)을 컴포넌트 라이브러리로 박아 **모든 인물 영상이 같은 디자인 언어**를 갖게 된다.

### 8.3 S3 격자 애니메이션 — "소수의 체" 동적 시각화

storyboard S3는 1~30 격자에서 2→4·6·8 gray out, 3→9·15 gray out, 5→25 gray out, 남은 소수 gold 강조를 **시간에 따라** 보여준다. FFmpeg로 불가. 해법:
- SVG + SMIL/CSS 애니메이션 → headless Chromium 프레임 캡처 → mp4
- 또는 JSXGraph(이미 프로젝트 기술 스택)로 인터랙티브 보드를 렌더 후 화면 캡처
- 산출 mp4를 S3 클립으로 concat 합류

이 30초가 INTEGRATED_PLAN §7.1 "핵심 시각화 30초" 능력의 첫 실현이며, 약속 3겹 중 "발견의 필연성 서사"를 *시각적으로* 운반하는 결정타다.

### 8.4 영화 후반작업·방송 그래픽스 차용

| 기법 | 출처 | 적용 |
|---|---|---|
| **로워서드(lower-third)** | 방송 자막 | 인물 이름·연대 자막을 박스+선 그래픽으로 (S4 "BCE 250", S5 "유클리드 BCE 300") |
| **컬러 그레이딩** | 영화 DI | 시대 팔레트(era-ancient 테라코타/황토/청동)를 `curves`·`colorbalance` 필터로 전 scene 일관 적용 → 시대 감각 몰입(약속 1) |
| **모션 블러** | 3D 렌더 | 줌·팬에 `tblend`/`minterpolate`로 미세 블러 → 시네마틱(§9.3) |
| **비네팅·필름 그레인** | 필름 룩 | `vignette` + `noise` 필터로 고대 사료 질감 |
| **오디오 덕킹 cue** | 방송 믹싱 | STEP 8 대비 — 자막·결정적 순간 시각 cue에 맞춰 BGM 덕킹 마커를 config에 함께 기록 |

### 8.5 자동 렌더 파이프라인 — 캐싱·증분·병렬

이상적 파이프라인:
```
config 변경 감지(mtime/hash)
   → 영향받은 scene만 dirty 표시
   → dirty scene 병렬 렌더 (background agent N개 / GNU parallel)
   → 콘텐츠 해시 기반 clip 캐시 (같은 입력 = 같은 출력 재사용)
   → concat → verify → raw mp4
   → 길이/해상도/자막 자동 검증 통과 시에만 STEP 8 트리거
```
콘텐츠 주소 지정 캐시(입력 해시 = 클립 키)로 "두 번 같은 렌더 안 함"(INTEGRATED_PLAN 진화 원칙 1과 정신 일치). 음성안 5종(turns_norm_*)이 있어도 **영상 렌더는 1회** — 음성 무관이므로 클립 캐시 100% 재사용.

### 8.6 "이상적이라면" 비전

config 하나를 고치면(예: S3를 25초→30초) → 컴파일러가 영향 scene 자동 식별 → 그 scene만 재렌더 → 음성 sync 자동 재검증 → 통과 시 STEP 8 자동 mux → Nick에게 "S3 30초 버전 raw 완성, sync OK" 1줄 보고. 사람 손은 **모션의 의도(어떤 줌·어떤 자막 타이밍)** 결정에만. 이것이 PURPOSE 3단계 진화의 "자동화" 단계에서 STEP 7이 도달할 모습이다.

---

## 9. 고급 Contents 생성 방법 (품질 도약)

### 9.1 모션 어휘를 "감정 문법"으로 — motion 5종의 의미화

exp-002 config의 motion 5종은 단순 카메라 움직임이 아니라 **감정 전달 도구**다. 이를 표현식 테이블로 표준화하면 시리즈 일관성이 생긴다:

| motion | z·x·y 표현식 | 감정·서사 의미 | exp-002 scene |
|---|---|---|---|
| `push_in` | z↑, xy center | 빨려듦·도입·집중 (시대 안으로) | S1 도서관 |
| `zoom_out` | z↓, xy center | 드러남·전모·인물 공개 | S2 에라토 |
| `ken_burns` | z 미세↑, xy 미세 drift | 사색·관조·시간의 흐름 | S3 분류 |
| `pan_right` | z 고정, x→ | 이동·여정·먼 곳(시러큐스) | S4 편지 |
| `slow_zoom` | z 아주 천천히↑ | 정중·권위·여운 | S5 유클리드·류후이 |

**원칙: 결정적 순간(S5 "인류, 같은 답 두 번")은 모션을 *멈춰* 정적으로** — 움직임의 부재가 강조다(영화 freeze 기법). 모션 속도(z 증분)를 scene의 정서 무게에 반비례시킨다.

### 9.2 자막 타이포그래피 고급화

storyboard 명세 = serif(NotoSerifCJKkr) + gold(0xE89B4F). 한 단계 위로:

| 기법 | 구현 | 효과 |
|---|---|---|
| **fade-in 자막** | drawtext `alpha='if(lt(t,s+0.4),(t-s)/0.4,1)'` | 자막이 슥 떠오름 (cut 느낌 제거) |
| **그림자·아웃라인 2겹** | `shadowx/y` + `borderw=2:bordercolor` | 어떤 배경에서도 가독성 (시대 사진 위) |
| **위계 색** | 핵심어 gold(β·정리·소수의 체) / 부가 white(연대·부제) | 시청자 눈이 닻 단어로 (진화 원칙 5 "한 단어") |
| **가변 폰트 weight** | (Remotion 시) 등장 시 weight 300→700 | 단어의 무게감 |
| **로워서드 박스** | `drawbox` + `drawtext` 조합 | 인물/연대 자막을 방송 그래픽으로 |

핵심어(인물의 "한 단어" — 에라토스테네스 = "정리")는 **항상 gold·화면 중앙·큰 폰트**로 표준화 → 시청자가 시리즈를 가로질러 "닻 단어"를 학습(진화 원칙 5).

### 9.3 렌더 품질 도약 — 고해상도·HDR·시네마틱

| 도약 | 방법 | 트레이드오프 |
|---|---|---|
| **고해상도** | 1280×720 → 1920×1080 또는 4K 마스터. 입력 이미지가 충분히 크면 zoompan scale-up 여유 ↑ | 렌더 시간·용량 ↑. YouTube는 1080p 권장 |
| **컬러 그레이딩** | `curves`/`colorbalance`로 era-ancient 팔레트 전 scene 통일 | 시대 감각(약속 1) ↑↑ |
| **모션 블러** | `minterpolate=fps=50:mi_mode=mci` 후 `tblend` → 25fps 다운 | 시네마틱하나 연산 비쌈·아티팩트 위험 |
| **HDR** | libx265 + bt2020 + smpte2084 | 플랫폼 호환성 낮음. 현 단계 과함 — 미래 옵션 |
| **필름 룩** | `vignette` + 미세 `noise` + 그레인 | 고대 사료 질감·정서 |
| **고품질 인코딩** | `-preset slow -crf 18 -profile:v high -tune film` | 시간↑, 화질↑ |

**현 단계 권장**: 1080p + era-ancient 컬러 그레이딩 + 가벼운 비네팅 + CRF 18. HDR·모션블러는 §10.2 가설 검증(능력 흡수 가치) 후 점진 도입(진화 원칙 4 "한꺼번에 X").

### 9.4 시리즈 정체성·일관성·확장성

- **렌더 프리셋을 SSOT화** — 해상도/fps/pix_fmt/CRF/팔레트/폰트/로워서드 스타일을 `render-profile.json` 하나로. 모든 인물 영상이 같은 시각 언어 → 채널 정체성(INTEGRATED_PLAN A7).
- **확장성** — config 스키마가 안정되면 새 인물 영상은 "이미지 + config" 입력만으로 같은 품질로 자동 렌더. 단원당 시간 단축(가설 4)의 가장 큰 수혜 단계가 렌더다(결정론적이라 자동화 이득이 가장 큼).
- **"양보하지 않은 것" 기록**(진화 원칙 6) — 매 렌더에서 타협한 것(예: "S3 격자는 정적 줌으로 임시 처리, 동적 시각화는 다음 단원에서")을 한 줄 남겨 시리즈의 품질 부채를 추적.

### 9.5 이 step에서만 가능한 차별화 포인트

렌더는 **여러 매체(AI 이미지 + 코드 다이어그램 + 손그림 외주 §7.4)를 하나의 시각 언어로 통일하는 유일한 지점**이다. 컬러 그레이딩·모션 어휘·자막 타이포가 여기서 한 번에 적용되므로, "출처가 제각각인 소재들이 한 편의 일관된 영상으로 보이게 하는 것"이 STEP 7만의 책임이자 차별화다. 정지 이미지 한 장이 18초 동안 *살아 있게* 만드는 Ken Burns + 자막의 호흡 — 그 미세한 타이밍 감각이 "잘 만든 영상"과 "슬라이드쇼"를 가른다.

---

## 변경 이력

- **2026-05-29**: 신규. STEP 7 [영상 5 렌더] 심화 가이드 9섹션 작성. exp-002 S1 클립 검증(1280×720/18.24s) 기반 FFmpeg zoompan+drawtext+fade 파이프라인 문서화 + `se-video-render` SKILL.md 설계 제안 + 코드 모션 비교·프로그래matic 비디오·자동 파이프라인·시네마틱 품질 도약 아이디어.
