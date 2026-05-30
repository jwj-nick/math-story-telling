---
name: se-video-render
description: 영상 제작 시스템의 단계 [영상 5] 렌더 스킬. 단계 [영상 4] 모션의 모션 config(JSON) + 단계 [영상 3] 이미지 + 한글 폰트를 받아 FFmpeg로 장면별 클립(zoompan 카메라 모션 + drawtext 한글 자막 + fade 전환)을 렌더하고 concat으로 음성 없는 raw mp4(NN-raw.mp4)를 만든다. 입력(6-motion-config.json / 5-images/*.png / NotoSerifCJKkr 폰트 / (옵션) 품질 프로파일 / (옵션) 부분 렌더 scene)을 받아 동작(RD config 로드 → CL scene별 클립 렌더 → CC concat → VF 검증)을 진행. math-story-telling 영상의 FFmpeg 렌더, Ken Burns 모션, 한글 자막 새기기, 음성 sync 보존 raw mp4 제작 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료(40_experiments/exp-NNN/6-motion-config.json, 5-images/*.png, 3-storyboard.md, C:/Windows/Fonts/NotoSerifCJKkr-Regular.otf)를 참조만 함. 외부 도구: FFmpeg + ffprobe (CLI, 외부 런타임 의존 0).
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 5 렌더 (RD1~VF)
  ssot: 11_video_gen_process/70_tools/se-video-render/SKILL.md
  version: "0.1"
  status: 시드 (exp-002 STEP 7 시범 실행 후 reverse-engineering 정형화)
  tool: ffmpeg
  resolution: "1280x720"
  fps: 25
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-video-render — 영상 5 렌더 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 5]. 단계 [영상 4] 모션의 `6-motion-config.json`과 단계 [영상 3] 이미지를 받아, **정지 이미지에 카메라 모션(zoompan)을 입히고 한글 자막(drawtext)을 새겨, 음성이 없는 영상(raw mp4)으로 굳힌다.** 핵심 도구는 FFmpeg 단 하나. 출력은 다음 단계 [영상 6] 합성(`se-video-compose`)의 직접 입력 — 거기서 `4-narration.mp3`(음성)을 `-c:v copy`로 mux한다.

상위 frame: [INTEGRATED_PLAN](../../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md) §5.0 skill chain. 심화 가이드: [`../../20_step_guides/07_step7_render.md`](../../20_step_guides/07_step7_render.md).

원칙:
- 본 스킬은 외부 자료를 **참조**만 한다. 외부를 변경 X.
- **렌더 = 결정론적 변환** (config → mp4 1:1). Q&A 거의 없음 → skill(Bash) 단독이 자연스럽다.
- **렌더의 최대 책임 = "음성과 시간이 어긋나지 않는 raw mp4"**. 각 scene 클립 길이 == config의 `end - start`. xfade 금지(총 길이 변동 → sync 붕괴).
- **음성 무관** — 영상 렌더는 1회. 음성안 여러 종(turns_norm_*)이 있어도 STEP 8에서 음성만 교체(렌더 재사용).
- **1차 도구 = FFmpeg 단독** (v0.1 현행). 외부 의존 0·재현성 100%. GSAP/Remotion은 S3 격자 등 동적 다이어그램 필요 시 후보(진화 §).

---

본 v0.1 body 는 **exp-002 STEP 7 시범** 으로 작성됨 (2026-05-29). 시범 결과: 검증 성공한 S1 클립(1280×720, 18.24s) 기반 FFmpeg zoompan+drawtext+fade 파이프라인. 클립: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/clips/`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/clips/), 자막 textfile: `captxt/`.

---

## 입력 (3 필수 + 2 옵션)

| # | 입력 | 형식 | 출처 |
|---|---|---|---|
| 1 | 모션 config | `6-motion-config.json` (fps·resolution·total_duration·scenes[]·transition·font·palette) | 40_experiments/exp-NNN/ (STEP 6 산출) |
| 2 | 이미지 | `5-images/*.png` (scene별 `img` 경로) | STEP 5 산출 |
| 3 | 한글 폰트 | `C:/Windows/Fonts/NotoSerifCJKkr-Regular.otf` | config의 `font` 필드 |
| 4 (옵션) | 품질 프로파일 | draft(미리보기) / final(CRF 18, 기본) | 기본 final |
| 5 (옵션) | 부분 렌더 scene | "S3만" 등 (증분 렌더) | 기본 전체 |

검증 대조용(직접 입력 아님): `3-storyboard.md`(자막 텍스트·전환 종류 cut/fade 권위), `4-narration.mp3`(total_duration 진실 기준).

---

## 동작 (RD1 → CL → CC → VF)

### RD1. config 로드
- `6-motion-config.json` 파싱. `fps`(25) / `resolution`([1280,720]) / `total_duration`(140.27) / `font` / `palette`(gold·white·shadow) / `scenes[]` / `transition`(fade in/out 0.6) 확보.
- scene별: `id` / `img` / `start` / `end` / `motion`(push_in·zoom_out·ken_burns·slow_zoom·pan_right·zoom_in) / `zoom`([z0,z1]) / `captions[]`(text·x·y·size·color·start·end).

### CL. scene별 클립 렌더 (6단계 필터 그래프)
scene 루프. 각 scene → `clips/<id>.mp4`. (split 장면은 S3a/S3b, S5a/S5b로 분리 클립.)

1. **길이 계산** — `dur = end - start`, `frames = round(dur * fps)`. (마지막 scene은 `total_duration - 누적합`으로 역산 보정해 프레임 반올림 누적 방지.)
2. **베이스 변환** — `scale=2560:-1,crop=2560:1440` (2배 캔버스 — 줌 시 선명도 확보 + zoompan 서브픽셀 jitter 완화. zoompan은 큰 입력에서 동작시키는 것이 정석).
3. **zoompan** — `motion → z/x/y 표현식` 매핑. z 증분 = `(z1 - z0)/frames`, `min()`으로 상한. x/y = 중앙(`iw/2-(iw/zoom/2)` · `ih/2-(ih/zoom/2)`). `:s=1280x720:fps=25`로 다운스케일 출력.
4. **drawtext** — caption별. 한글은 **UTF-8 textfile로 분리**(`captxt/<id>_<N>.txt`) — 커맨드라인 한글 회피. `fontfile` 명시(Windows 경로 콜론 `C\:`로 이스케이프). `enable=between(t, cap.start-scene.start, cap.end-scene.start)` — **drawtext의 `t`는 클립 로컬 시간이라 scene.start만큼 offset 필수** (이 좌표 변환이 자막 타이밍의 함정). color는 palette(gold=0xE89B4F·white=0xFFFFFF), shadow 2px.
5. **fade** — `fade=t=in:st=0:d=0.6`, `fade=t=out:st=(dur-0.6):d=0.6`. **클립 길이는 그대로 보존**(음성 sync). cut 장면(storyboard S2→S3)은 fade out 생략 가능.
6. **encode** — `-c:v libx264 -pix_fmt yuv420p -r 25 -crf 18 -an` (음성 없음).

증분: `clips/<id>.mp4`가 이미 있고 그 scene의 config·이미지 mtime이 더 오래됐으면 skip.

### CC. concat (이어붙이기)
- `clips/list.txt`(`file 'S1.mp4'` …) 작성 → concat demuxer로 무손실 결합.
- `ffmpeg -f concat -safe 0 -i clips/list.txt -c copy <NN>-raw.mp4`.
- **`-c copy` 무손실** — 클립 인코딩 품질이 곧 최종 품질. **xfade 절대 금지**(겹침만큼 총 길이 줄어 음성 sync 붕괴).

### VF. 검증 (ffprobe)
- 길이 `total == total_duration ± 1프레임(0.04s)` / 해상도 `1280×720` / fps `25 CFR` / `pix_fmt=yuv420p` / 자막 빈 글리프(□) 0개.
- config와 대조. 통과 시에만 STEP 8 트리거.

---

## 검증된 FFmpeg 명령 (exp-002 실측)

**S1 — 자막 없는 push_in 클립 (1280×720, 18.24s 검증 ✅)**:

```bash
ffmpeg -loop 1 -i 5-images/4-S1-Museion.png -t 18.23 -r 25 \
  -vf "scale=2560:-1,crop=2560:1440,\
zoompan=z='min(zoom+0.0011,1.08)':d=456:\
x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=25,\
fade=t=in:st=0:d=0.6,fade=t=out:st=17.63:d=0.6,\
format=yuv420p" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -r 25 -an clips/S1.mp4
```

- `d=456` = `18.23s × 25fps ≈ 456` 프레임. z 증분 `0.0011`은 `(1.08-1.0)/456`을 부드럽게 키운 값 + `min(...,1.08)` 상한.
- `st=17.63` = `18.23 - 0.6` (끝 0.6초 fade out). concat 시 길이 보존 → 음성 sync 유지.

**S2 — 한글 자막(drawtext) 있는 zoom_out 클립**:

```bash
# 1) 자막을 UTF-8 textfile로 분리 (한글 안전)
#    captxt/S2_0.txt = "β"
#    captxt/S2_1.txt = "베타 — 모든 분야 2등"

# 2) zoompan 뒤에 drawtext 체인. enable의 t는 클립 로컬 → scene.start(18.23) offset
ffmpeg -loop 1 -i 5-images/2-S2-Close-up.png -t 15.64 -r 25 \
  -vf "scale=2560:-1,crop=2560:1440,\
zoompan=z='if(eq(on,0),1.08,max(zoom-0.0005,1.0))':d=391:\
x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=25,\
drawtext=fontfile='C\:/Windows/Fonts/NotoSerifCJKkr-Regular.otf':\
textfile='captxt/S2_0.txt':fontcolor=0xE89B4F:fontsize=130:\
x=(w-text_w)/2:y=h*0.30-text_h/2:\
shadowcolor=0x000000:shadowx=2:shadowy=2:\
enable='between(t,5.27,11.77)',\
drawtext=fontfile='C\:/Windows/Fonts/NotoSerifCJKkr-Regular.otf':\
textfile='captxt/S2_1.txt':fontcolor=0xFFFFFF:fontsize=40:\
x=(w-text_w)/2:y=h*0.82-text_h/2:\
shadowcolor=0x000000:shadowx=2:shadowy=2:\
enable='between(t,7.77,14.77)',\
fade=t=in:st=0:d=0.6,fade=t=out:st=15.04:d=0.6,\
format=yuv420p" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -r 25 -an clips/S2.mp4
```

- dur = `33.87 - 18.23 = 15.64`, frames = `15.64×25 ≈ 391`.
- 자막 1 (β): config 절대 시각 `23.5~30.0` → 로컬 `23.5-18.23=5.27` ~ `30.0-18.23=11.77`.
- 자막 2 (부제): config `26.0~33.0` → 로컬 `7.77` ~ `14.77`.
- color: gold=0xE89B4F (핵심어 β), white=0xFFFFFF (부제). x=중앙, y=`h*비율`.

**concat (무손실 결합 → raw mp4)**:

```bash
# clips/list.txt:
#   file 'S1.mp4'
#   file 'S2.mp4'
#   file 'S3a.mp4'
#   ...  file 'S6.mp4'
ffmpeg -y -f concat -safe 0 -i clips/list.txt -c copy 7-render-raw.mp4
```

**검증 (ffprobe)**:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration -of default=nw=1 7-render-raw.mp4
# 기대: width=1280 height=720 r_frame_rate=25/1 pix_fmt=yuv420p duration≈140.27
```

**drawtext 핵심 4 (한글 자막 노하우)**:
1. `fontfile` 명시 — 시스템 폰트 이름 의존 X. Windows 경로 콜론은 `C\:`로 이스케이프.
2. `textfile`로 한글 분리 — 쉘·필터 파싱이 한글을 건드리지 않음(□ 깨짐 방지). UTF-8, BOM 없음.
3. config 좌표 매핑 — `x:"center"`→`x=(w-text_w)/2`, `y:"0.30"`→`y=h*0.30-text_h/2`.
4. `enable=between(t, start, end)` — **반드시 scene.start offset** (drawtext t = 클립 로컬 시간).

---

## 출력

```text
<exp>/
├── clips/                ← scene별 중간 클립 (증분 렌더 캐시, gitignore)
│   ├── S1.mp4  S2.mp4  S3a.mp4  S3b.mp4  S4.mp4  S5a.mp4  S5b.mp4  S6.mp4
│   └── list.txt          ← concat 결합 목록
├── captxt/               ← 자막 UTF-8 textfile (caption별, BOM 없음)
│   ├── S2_0.txt  S2_1.txt  S3b_0.txt  ...
└── <NN>-raw.mp4          ← 최종 산출: 음성 없음, 1280×720, 25fps, yuv420p, ≈total_duration
```

- 클립: `clips/<scene-id>.mp4` (id = config의 `id`, split은 S3a/S3b).
- raw 영상: `<NN>-raw.mp4` (STEP 번호 prefix, 예: `7-render-raw.mp4`). gitignore.

다음 단계 [영상 6] 합성: `ffmpeg -i <NN>-raw.mp4 -i 4-narration.mp3 -c:v copy -c:a aac -b:a 192k -shortest 8-final.mp4` (영상 재인코딩 0).

---

## 평가 기준

| 항목 | 합격 (자동 ffprobe) | Nick 검수 |
|---|---|---|
| 해상도 | 1280×720 | — |
| fps | 25, CFR (가변 X) | — |
| pix_fmt | yuv420p (호환성) | — |
| **길이 = 음성 sync** | total == total_duration ± 1프레임(0.04s) | — |
| **자막 가독** | 빈 글리프(□) 0개 | 위치·타이밍 의도 일치 |
| 모션 | zoom 범위 명세 내 | 속도·방향 자연스러움 |
| **전환** | cut/fade 명세 일치(storyboard) | 끊김 없음 |
| 음성 sync 위험 | xfade 미사용(fade+concat) | — |

---

## QnA 패턴 시드

- *"scene 길이 합 == total_duration 인가? (음성 sync 1순위)"*
- *"한글 자막이 모두 박혔는가(□ 없는가)? enable t offset 맞는가?"*
- *"cut인데 fade 들어간 곳 없는가? (storyboard 대조)"*
- *"줌이 명세 zoom 범위 안에서 끝나는가?"*
- *"품질 = draft(빠른 미리보기) / final(CRF 18)?"*
- *"부분 렌더 = 전체 / 특정 scene만(증분)?"*

## 리서치 패턴 시드

렌더는 결정론적이라 외부 리서치 거의 불필요. 다음 경우만:

1. 렌더 도구 비교 — FFmpeg vs Remotion vs HyperFrames+GSAP (S3 격자 등 동적 다이어그램 필요 시) → references/render-tools-compare.md 누적.
2. FFmpeg 필터 문법 — zoompan/drawtext/fade/xfade 공식 docs.
3. 한글 폰트 글리프 완비성 — NotoSerifCJKkr 외 대안 검증.

---

## 진화 메커니즘

- **v0.1** (2026-05-29) — exp-002 STEP 7 시범. FFmpeg 단독 zoompan+drawtext+fade 파이프라인 검증(S1 1280×720/18.24s). scene별 클립 → concat(`-c copy`) → raw mp4. 한글 자막 = textfile UTF-8 + fontfile 명시 + enable t offset. xfade 금지(음성 sync). 현행.
- **v0.2** (예정 — 전체 6장면 렌더 + 검증 후):
  - `6-motion-config.json` → FFmpeg 명령 자동 생성 컴파일러 (references/render_compile.py). motion 5종 → z/x/y 표현식 테이블.
  - 자막 t offset 자동화 + "cap.start ≥ scene.start AND cap.end ≤ scene.end" assert.
  - **자막 x-fraction 지원** (unit-06): `x:"center"`→중앙 / `x:"0.27"`→`w*0.27-text_w/2` (좌/우 대비 자막 = 정비례좌·반비례우 라벨). y와 동일 패턴.
  - draft/final 2-pass + 콘텐츠 해시 기반 증분·병렬 렌더.
  - 마지막 scene 길이 역산 보정으로 프레임 반올림 누적 제거.
- **v0.3+** = 하이브리드 렌더 오케스트레이터(정지 이미지=FFmpeg + S3 격자=Remotion/GSAP 클립, 같은 1280×720/25fps/yuv420p로 통일해 concat). 컬러 그레이딩(era 팔레트)·로워서드·1080p 도약. 인물 영상 시리즈 정체성을 `render-profile.json` SSOT화.

---

## 호출 방법

```yaml
스킬: se-video-render
입력:
  1. 모션 config: 40_experiments/exp-NNN/6-motion-config.json
  2. 이미지: 40_experiments/exp-NNN/5-images/*.png
  3. 한글 폰트: C:/Windows/Fonts/NotoSerifCJKkr-Regular.otf (config의 font)
  4. (옵션) 품질 프로파일: draft / final(기본)
  5. (옵션) 부분 렌더: "S3만" 등 (증분)
출력:
  - 40_experiments/exp-NNN/clips/*.mp4 (scene별, gitignore)
  - 40_experiments/exp-NNN/captxt/*.txt (자막 UTF-8)
  - 40_experiments/exp-NNN/<NN>-raw.mp4 (음성 없는 raw, 1280×720/25fps, gitignore)
다음 단계: se-video-compose (STEP 8) — raw mp4 + 4-narration.mp3 mux
```

본 시범 호출 예시: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/clips/`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/clips/) (S1 검증 1280×720/18.24s).
