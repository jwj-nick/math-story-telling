# 0501 · Unit01 시각화 개발 일지

> 작업 디렉토리: `80_tools/unit01_소인수분해/` (웹) · `90_video/unit01_소인수분해/` (영상)
> 목적: 기술을 배우면서 결과물을 만드는 과정을 기록

---

## 목차 (TOC)

| 세션 | 날짜 | 주제 | 상태 |
|---|---|---|---|
| [Session 1](#session-1--2026-04-29--웹-인터랙티브-5종-세트) | 2026-04-29 | 웹 인터랙티브 5종 세트 | ✅ 완료 |
| [Session 2](#session-2--2026-05-02--hyperframes--gsap-동영상) | 2026-05-02 | HyperFrames + GSAP 동영상 | ✅ 완료 |
| [Session 3](#session-3--2026-05-02--tts-한국어-음성-추가) | 2026-05-02 | TTS 한국어 음성 추가 | ✅ 완료 |
| [Session 4](#session-4--계획--remotion으로-다시-만들기) | 그다음 | Remotion으로 다시 만들기 | 🔜 계획 |
| [기술 용어 메모](#기술-용어-메모) | — | 누적 용어 사전 | — |

---

## Session 1 · 2026-04-29 — 웹 인터랙티브 5종 세트

### 작업 순서 및 근거

```
shared.css        ← 공통 스타일 변수 정의 (모든 파일이 이걸 import)
sieve.html        ← 소수의 체 인터랙티브 (가장 임팩트 큰 결과물 먼저)
index.html        ← 스토리 허브 (이야기 텍스트 + 섹션 링크)
concepts.html     ← 개념 카드 + 빈칸 채우기
problems.html     ← 문제 세트 (힌트 토글, 답 확인)
```

---

### [완료] shared.css

**배우는 개념**: CSS Custom Properties (변수)

```css
:root {
  --prime: #ef4444;   /* 이렇게 정의하면 */
}
.cell.prime {
  background: var(--prime);   /* 이렇게 재사용 */
}
```

- `:root`는 HTML 전체의 최상위 요소. 여기에 `--변수명: 값` 형태로 변수를 정의하면
  어느 파일에서든 `var(--변수명)`으로 불러올 수 있음.
- 나중에 색상 테마를 바꿀 때 `:root` 한 곳만 수정하면 전체 반영됨.
- `link rel="stylesheet" href="shared.css"`로 각 HTML에서 불러옴.

---

### [완료] sieve.html

**배우는 개념 1**: CSS Grid로 숫자 배열

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(44px, 1fr));
  gap: 6px;
}
```

- `auto-fill`: 컨테이너 너비에 맞춰 열 수 자동 결정
- `minmax(44px, 1fr)`: 최소 44px, 최대 균등 분배
- 화면이 좁아지면 자동으로 열이 줄어듦 (반응형)

**배우는 개념 2**: CSS Transition으로 부드러운 상태 변화

```css
.cell {
  transition: all 0.25s ease;
}
.cell.crossed {
  opacity: 0.3;
  text-decoration: line-through;
}
```

- JS로 클래스를 추가/제거하면 CSS가 자동으로 애니메이션 처리
- `transition: all 0.25s`는 "모든 CSS 속성 변화를 0.25초에 걸쳐 부드럽게"

**배우는 개념 3**: async/await + Promise로 딜레이 있는 애니메이션

```javascript
// 이렇게 하면 setTimeout의 콜백 지옥을 피할 수 있음
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runSieve() {
  for (let p = 2; ...) {
    highlight(p);
    await delay(700);    // 0.7초 기다린 후 다음 줄 실행
    crossOutMultiples(p);
    await delay(400);
  }
}
```

- `Promise`: "나중에 완료될 작업"을 표현하는 객체
- `async function`: 내부에서 `await` 사용 가능한 함수
- `await delay(700)`: 700ms 동안 멈췄다가 계속 실행

**배우는 개념 4**: DOM 조작 (JS로 HTML 요소 제어)

```javascript
// data-num 속성으로 숫자에 해당하는 셀을 빠르게 찾음
function getCell(n) {
  return document.querySelector(`[data-num="${n}"]`);
}
// classList로 CSS 클래스 추가/제거
getCell(4).classList.add('crossed');
getCell(2).classList.add('prime');
```

---

### [완료] index.html — 스토리 허브

**배우는 개념**: CSS hover transition + 링크 카드 패턴

```css
.link-card {
  transition: border-color 0.15s, transform 0.12s;
}
.link-card:hover {
  transform: translateY(-2px);  /* hover 시 2px 위로 뜨는 효과 */
}
```

- `transition`을 여러 속성에 콤마로 구분해서 각각 타이밍 지정 가능
- `transform: translateY(-2px)`: 실제 위치는 안 바뀌고, 시각적으로만 올라감 (레이아웃 영향 없음)

---

### [완료] concepts.html — 플래시카드 + 빈칸 채우기

**배우는 개념 1**: CSS 3D 카드 뒤집기

```css
.flashcard { perspective: 800px; }         /* 원근감 */
.card-inner { transform-style: preserve-3d; transition: transform 0.45s; }
.flashcard.flipped .card-inner { transform: rotateY(180deg); }
.card-back { transform: rotateY(180deg); backface-visibility: hidden; }
```

- `perspective`: 관찰자 거리. 작을수록 강한 3D 효과.
- `preserve-3d`: 자식 요소들이 부모의 3D 공간을 공유함.
- `backface-visibility: hidden`: 반대편 바라볼 때 그 면이 안 보임.
- JS는 딱 한 줄: `card.classList.toggle('flipped')`

**배우는 개념 2**: Event Delegation (이벤트 위임)

```javascript
// ❌ 나쁜 방법: 카드마다 리스너 6개
cards.forEach(c => c.addEventListener('click', ...));

// ✅ 좋은 방법: 부모 하나에 리스너 1개
document.getElementById('cardGrid').addEventListener('click', e => {
  const card = e.target.closest('.flashcard');  // 클릭된 요소의 조상 탐색
  if (card) card.classList.toggle('flipped');
});
```

- `closest('.cls')`: 자신부터 위로 올라가며 조건에 맞는 첫 번째 조상 반환
- DOM 요소가 나중에 추가돼도 이벤트가 자동 적용됨

---

### [완료] problems.html — 문제 세트

**배우는 개념**: 진행 바 (progress bar)

```javascript
// JS로 CSS 속성을 직접 변경
document.getElementById('progressFill').style.width = (solved / 12 * 100) + '%';
// CSS에 transition이 있으면 자동으로 부드럽게 채워짐
```

- `element.style.속성 = '값'`: JS에서 인라인 CSS 직접 변경
- CSS의 `transition`은 JS로 값이 바뀔 때도 적용됨

---

### 파일 라인 수 (모두 500줄 이내 ✅)

| 파일 | 줄 수 |
|---|---|
| shared.css | 176 |
| sieve.html | 438 |
| index.html | 176 |
| concepts.html | 332 |
| problems.html | 447 |

---

## Session 2 · 2026-05-02 — HyperFrames + GSAP 동영상

### 작업 순서 및 근거

```
scoop install ffmpeg          ← HyperFrames가 요구하는 인코더
npm install -g hyperframes    ← HTML → MP4 렌더링 도구
90_video/unit01_소인수분해/
└── sieve-video/
    ├── index.html            ← GSAP 기반 composition (230줄)
    └── sieve.mp4             ← 렌더링 결과 (332 KB, 16초, 24fps)
```

---

### [완료] FFmpeg + HyperFrames 환경 구성

**HyperFrames 프로젝트 구조**

HyperFrames는 단일 파일이 아니라 **프로젝트 폴더** 기반으로 동작한다.
폴더 안에 `index.html` 하나만 있으면 최소 프로젝트로 인식된다.

렌더 명령:
```bash
hyperframes render sieve-video -o sieve-video/sieve.mp4 -f 24 -q draft
```

내부 동작 파이프라인:
```
index.html
   ↓ Headless Chrome (Puppeteer)
   ↓ GSAP timeline을 frame 단위로 seek
   ↓ 각 프레임을 PNG로 캡처
   ↓ FFmpeg로 PNG 시퀀스 → MP4 인코딩
sieve.mp4
```

---

### [완료] sieve-video/index.html — GSAP 기반 소수의 체 애니메이션

**배우는 개념 1**: HyperFrames Composition 구조

```html
<div
  id="root"
  data-composition-id="sieve"   ← 필수: composition 식별자
  data-start="0"
  data-duration="16"            ← 영상 길이 (초)
  data-width="1280"
  data-height="720"
>
```

- `data-composition-id`: HyperFrames가 이 div를 렌더링 대상으로 인식
- `data-duration`: 총 영상 길이. 이 값이 MP4 길이가 됨.
- 1280×720 = HD 해상도 (16:9)

**배우는 개념 2**: GSAP 타임라인

```javascript
const tl = gsap.timeline({ paused: true });

// 0.6초에 #c2를 노란색으로 (0.3초 동안)
tl.to('#c2', { backgroundColor: '#fef3c7', scale: 1.12, duration: 0.3 }, 0.6);

// 1.0초에 #c4를 흐리게
tl.to('#c4', { opacity: 0.2, scale: 0.86, duration: 0.14 }, 1.0);

// HyperFrames가 이 타임라인을 frame 단위로 제어
window.__timelines['sieve'] = tl;
```

- `gsap.timeline({ paused: true })`: 자동 재생 안 함. HyperFrames가 직접 seek함.
- `.to(타겟, 속성들, 시작시간)`: 3번째 인자가 **절대 시간** (+=0.5 식으로 상대 지정도 가능)
- `window.__timelines[id] = tl`: HyperFrames가 이 key로 타임라인을 찾음

**배우는 개념 3**: 타임라인 위에 순서 쌓기 패턴

```javascript
// 상수처럼 재사용 가능한 속성 묶음
const CROSSED = { opacity: 0.2, scale: 0.86, backgroundColor: '#0f172a', duration: 0.14 };
const PRIME   = { backgroundColor: '#ef4444', color: '#fff', duration: 0.25 };

// 배열로 루프 → 각 숫자에 순차 딜레이
const mult2 = [4,6,8,10,...,50];
mult2.forEach((n, i) => tl.to('#c' + n, CROSSED, 1.0 + i * 0.13));

// 이전 페이즈 끝 시간을 변수로 추적
const t2done = 1.0 + mult2.length * 0.13 + 0.15;  // ~4.5s
const t3 = t2done + 0.5;                            // 다음 페이즈 시작
```

- 타임라인의 각 `to()` 호출은 **독립적으로 절대 시간에 배치**됨
- 이전 단계가 끝나는 시간을 `const`로 계산해두면 전체 타이밍을 쉽게 조정 가능

**배우는 개념 4**: 상태 텍스트 교체 (여러 div를 opacity로 스왑)

```javascript
// ❌ 이렇게 하면 GSAP이 텍스트 자체를 애니메이션 못 함
tl.call(() => { el.textContent = '새 텍스트'; }, null, 5.0);  // seek 시 발동 안 됨

// ✅ 이렇게: 여러 div를 미리 만들어두고 opacity로 교체
function switchStatus(t, outId, inId) {
  if (outId) tl.to('#' + outId, { opacity: 0, duration: 0.25 }, t);
  tl.to('#' + inId, { opacity: 1, duration: 0.25 }, t + 0.1);
}
```

- `tl.call(콜백)` 은 타임라인이 forward 재생될 때만 발동 → seek에 안전하지 않음
- 시각적 요소는 모두 GSAP `to()`로 직접 애니메이션해야 frame-accurate 렌더링 보장

---

### 렌더링 결과 및 경고

| 항목 | 결과 |
|---|---|
| 출력 파일 | `sieve-video/sieve.mp4` |
| 크기 | 332 KB |
| 길이 | 16초 |
| 해상도 | 1280×720 (HD) |
| FPS | 24 |

**경고 (비치명적)**:
1. 한글 폰트 매핑 없음 → `Malgun Gothic` 미인식, 대체 폰트 사용
   - 수정법: `@font-face`로 Noto Sans KR CDN 선언
2. `caption_exit_missing_hard_kill` → opacity 0 exit 후 `tl.set(el, {visibility:'hidden'})` 추가하면 해결

---

## Session 3 · 2026-05-02 — TTS 한국어 음성 추가

### 목표 및 결과

한국어 내레이션을 생성하고 영상에 합성.
HyperFrames `<audio>` 통합 시도 → 오류 발생 → **FFmpeg 직접 합성**으로 해결.

### 작업 결과

```
python -m pip install edge-tts              ← edge-tts 7.2.8 설치
edge-tts --voice ko-KR-SunHiNeural ...     ← narration.mp3 (169 KB, 28.2초) 생성
hyperframes render → sieve_29s.mp4         ← 29초 무음 영상 재렌더링 (Noto Sans KR 폰트 포함)
ffmpeg -i sieve_29s.mp4 -i narration.mp3   ← 영상+음성 합성
→ sieve_with_audio.mp4 (764 KB, 28.2초) ✅
```

### 최종 파일 구조

```
sieve-video/
├── narration.txt          ← 음성 스크립트 (원문)
├── narration.mp3          ← edge-tts 생성 (169 KB, 28.2초, SunHiNeural)
├── sieve.mp4              ← v1: 무음 16초 draft
├── sieve_29s.mp4          ← v2: 무음 29초 standard (Noto Sans KR)
└── sieve_with_audio.mp4   ← v3: 음성 포함 28.2초 ✅ 완성본
```

---

### 배운 개념

**배우는 개념 1**: edge-tts CLI

```bash
# Python -m 방식으로 실행
python -m edge_tts --voice ko-KR-SunHiNeural --file narration.txt --write-media narration.mp3

# 사용 가능한 한국어 목소리
ko-KR-SunHiNeural       Female  Friendly (교육용 추천)
ko-KR-InJoonNeural      Male    Friendly
ko-KR-HyunsuMultilingualNeural  Male  다국어
```

- `--write-media output.mp3`: 텍스트 → MP3 파일 저장
- `--write-subtitles output.vtt`: 단어별 타임스탬프가 있는 WebVTT 자막도 동시 생성 가능

**배우는 개념 2**: FFmpeg 오디오 합성

```bash
ffmpeg \
  -i sieve_29s.mp4 \        # 입력 1: 영상 (29초)
  -i narration.mp3 \         # 입력 2: 음성 (28.2초)
  -map 0:v \                 # 출력 비디오 스트림 = 입력 1의 비디오
  -map 1:a \                 # 출력 오디오 스트림 = 입력 2의 오디오
  -c:v copy \                # 비디오는 재인코딩 없이 복사 (속도↑)
  -c:a aac \                 # 오디오를 AAC로 인코딩 (MP4 표준)
  -shortest \                # 더 짧은 스트림 기준으로 출력 길이 결정
  sieve_with_audio.mp4
```

- `-map 0:v -map 1:a`: 영상과 오디오를 각각 다른 입력에서 가져옴
- `-c:v copy`: 비디오를 픽셀 단위로 재처리 안 함 → 빠르고 화질 손실 없음
- `-c:a aac`: MP4 컨테이너 표준 오디오 코덱 (MP3는 MP4에서 비호환 가능)
- `-shortest`: 영상(29s)과 음성(28.2s) 중 짧은 음성 기준으로 28.2초에서 종료

**배우는 개념 3**: 한글 폰트 (@font-face 방식)

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Noto Sans KR', system-ui, sans-serif; }
</style>
```

- HyperFrames 렌더링 시 한글 폰트를 CDN에서 직접 로드 → 한국어 텍스트가 정확히 렌더링됨
- `display=swap`: 폰트 로드 전 fallback 폰트로 표시, 로드 후 교체

**트러블슈팅**: HyperFrames `<audio>` 통합 실패

```html
<!-- 이 방식은 exit code 9 오류 발생 (오디오 처리 단계에서 실패) -->
<audio src="narration.mp3" data-start="0" data-duration="29" data-track-index="1" data-volume="1"></audio>
```

원인 추정: local MP3 파일 경로를 headless Chrome이 올바르게 로드하지 못하거나,
HyperFrames가 오디오 처리 시 비-TTY 환경에서 실패하는 것으로 보임.

→ 해결: HyperFrames는 영상만 렌더링, FFmpeg로 오디오 후합성 (더 안전하고 유연한 방식)

---

### TTS 기술 스택 비교 (조사 결과)

---

### TTS 기술 스택 비교

| 도구 | 한국어 | 품질 | 설치 | 비용 | 로컬/클라우드 |
|---|---|---|---|---|---|
| **edge-tts** | ✅ | ★★★★☆ | `pip install edge-tts` | 무료 | 클라우드 (Microsoft Azure) |
| HyperFrames TTS (Kokoro) | ❌ | ★★★★★ | 내장 | 무료 | 로컬 |
| gTTS (Google) | ✅ | ★★★☆☆ | `pip install gtts` | 무료 | 클라우드 |
| Coqui XTTS v2 | ✅ | ★★★★☆ | `pip install TTS` (1 GB+) | 무료 | 로컬 |
| Naver CLOVA | ✅ | ★★★★★ | API 키 필요 | 유료 | 클라우드 |

**선택: edge-tts**
- 이유: 설치 간단, 무료, Microsoft Azure 급 품질, Korean 전용 목소리 2종 보유
- `ko-KR-SunHiNeural` (여성, 밝고 명확) — 교육 콘텐츠에 최적
- `ko-KR-InJoonNeural` (남성, 차분함)

---

### 작업 계획

#### Step 1 — 스크립트 작성

영상 타임라인에 맞춰 음성 대본 설계 (16초):

| 시각 | 화면 상태 | 내레이션 |
|---|---|---|
| 0.0-1.0s | 타이틀 등장 | "기원전 240년, 에라토스테네스는 소수를 걸러내는 방법을 발견했습니다." |
| 0.6-4.5s | 2 강조 → 배수 지우기 | "2는 소수입니다. 2의 배수를 모두 지웁니다." |
| 5.0-7.4s | 3 강조 → 배수 지우기 | "3은 소수. 3의 새 배수를 지웁니다." |
| 7.9-10.6s | 5, 7 | "5도, 7도 소수입니다." |
| 11.0-14.0s | 남은 소수 확정 | "체에 남은 수들은 모두 소수. 2부터 50까지, 소수는 15개입니다." |
| 14.5-16.0s | 결과 텍스트 | "이것이 에라토스테네스의 체입니다." |

→ 하나의 연속 스크립트로 합쳐서 `narration.txt`에 저장.

#### Step 2 — edge-tts 설치 및 음성 생성

```bash
# 설치
pip install edge-tts

# 생성
edge-tts --voice ko-KR-SunHiNeural \
         --text "기원전 240년..." \
         --write-media narration.mp3 \
         --write-subtitles narration.vtt   # 자막 파일도 동시 생성

# 또는 파일에서 읽기
edge-tts --voice ko-KR-SunHiNeural \
         --file narration.txt \
         --write-media narration.mp3
```

**배우는 개념**: TTS CLI — 텍스트 → MP3 파일 변환. `--write-subtitles`로 WebVTT 자막도 자동 생성됨.

#### Step 3 — HyperFrames에 오디오 통합

`sieve-video/index.html`에 아래 추가:

```html
<!-- data-start: 오디오 시작 시각 (초) -->
<audio
  id="narration"
  src="narration.mp3"
  data-start="0"
  data-duration="16"
  data-track-index="1"
  data-volume="1"
></audio>
```

**배우는 개념**: HyperFrames `<audio>` 요소. `data-start/duration/volume`으로 타임라인에 음성 배치.

#### Step 4 — 재렌더링

```bash
hyperframes render sieve-video -o sieve-video/sieve_with_audio.mp4 -f 24 -q standard
```

---

### 예상 결과물

```
90_video/unit01_소인수분해/sieve-video/
├── index.html         ← audio 요소 추가 버전
├── narration.txt      ← 음성 스크립트 원문
├── narration.mp3      ← edge-tts 생성 음성
├── sieve.mp4          ← 무음 버전 (기존)
└── sieve_with_audio.mp4 ← 음성 포함 완성본
```

---

## Session 4 · 계획 — Remotion으로 다시 만들기

### 왜 Remotion인가

HyperFrames는 HTML/CSS/JS 그대로 영상화 → 빠르고 친숙함
Remotion은 React 컴포넌트로 영상 설계 → **TypeScript + React를 배우는 기회**

같은 주제(소수의 체)를 두 도구로 만들면:
- 도구별 패러다임 차이를 몸으로 이해
- React 컴포넌트 설계, `useCurrentFrame()`, `interpolate()` 개념 체득

---

### 작업 계획

#### Step 1 — Remotion 프로젝트 생성

```bash
cd 90_video/unit01_소인수분해/
npx create-video@latest remotion-sieve
cd remotion-sieve
npm install
```

생성되는 구조:
```
remotion-sieve/
├── src/
│   ├── Composition.tsx   ← 영상 구조 정의
│   ├── Root.tsx          ← 컴포지션 등록
│   └── HelloWorld/       ← 예제 컴포넌트
├── package.json
└── remotion.config.ts
```

#### Step 2 — 핵심 개념: useCurrentFrame + interpolate

```tsx
import { useCurrentFrame, interpolate } from 'remotion';

const SieveScene: React.FC = () => {
  const frame = useCurrentFrame();   // 현재 프레임 번호 (0, 1, 2, ...)
  const fps = 24;
  const time = frame / fps;          // 초 단위로 변환

  // 0초~0.5초 동안 opacity 0 → 1
  const titleOpacity = interpolate(time, [0, 0.5], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return <div style={{ opacity: titleOpacity }}>에라토스테네스의 체</div>;
};
```

**HyperFrames와의 차이**:
- HyperFrames: GSAP timeline이 시간 축. HTML/CSS/JS 그대로.
- Remotion: `useCurrentFrame()` 훅이 시간 축. React 컴포넌트로 선언적 설계.

#### Step 3 — 렌더링

```bash
# 미리보기 (개발 서버)
npm run dev   # http://localhost:3000 에서 타임라인 확인

# 렌더링
npx remotion render src/index.ts SieveScene out/sieve.mp4
```

---

### HyperFrames vs Remotion 비교 (체험 후 기록 예정)

| 항목 | HyperFrames | Remotion |
|---|---|---|
| 언어 | HTML/CSS/JS | TypeScript + React |
| 애니메이션 | GSAP timeline | useCurrentFrame + interpolate |
| 렌더링 방식 | Puppeteer + FFmpeg | Node.js canvas + FFmpeg |
| 설치 | npx 1줄 | npm + 빌드 환경 |
| 학습 곡선 | 낮음 | 높음 (React 필요) |
| 재사용성 | HTML 파일 | 컴포넌트 (재조합 가능) |
| 적합한 경우 | 빠른 프로토타이핑 | 복잡하고 반복적인 영상 |

---

## 기술 용어 메모

| 용어 | 설명 |
|---|---|
| CSS Custom Property | `--이름: 값` 형태의 CSS 변수. `:root`에 정의하면 전역 사용 가능. |
| CSS Grid | 2차원 격자 레이아웃. `grid-template-columns`로 열 구조 정의. |
| CSS Transition | 속성 변화를 부드럽게. `transition: 속성 시간 타이밍`. |
| async/await | 비동기 코드를 동기처럼 읽히게. `await`는 Promise가 끝날 때까지 대기. |
| Promise | 미래에 완료될 작업. `resolve()` 호출로 완료 신호 전달. |
| classList | DOM 요소의 CSS 클래스 목록. `.add()`, `.remove()`, `.toggle()`. |
| data-* 속성 | HTML에 커스텀 데이터 저장. JS에서 `dataset.이름`으로 접근. |
| querySelector | CSS 선택자로 DOM 요소 찾기. `[data-num="5"]`처럼 속성 선택자도 사용 가능. |
| GSAP | GreenSock Animation Platform. JS 애니메이션 라이브러리. `tl.to(타겟, 속성, 시간)`으로 타임라인 구성. |
| GSAP Timeline | 여러 애니메이션을 시간 축에 배치하는 컨테이너. `paused:true`로 시작 후 외부에서 제어 가능. |
| HyperFrames | HTML/JS/CSS → MP4 렌더링 도구. `window.__timelines[id] = tl`로 GSAP 타임라인 등록. |
| data-composition-id | HyperFrames가 렌더링 대상 div를 인식하는 속성. |
| data-duration | HyperFrames composition의 총 재생 길이 (초). |
| FFmpeg | 영상/오디오 인코딩·변환 CLI 도구. HyperFrames가 PNG 시퀀스 → MP4 변환에 내부적으로 사용. |
| edge-tts | Microsoft Azure TTS를 무료로 쓰는 Python CLI. `ko-KR-SunHiNeural` 등 한국어 목소리 지원. |
| TTS | Text-to-Speech. 텍스트를 음성으로 변환. |
| WebVTT | 웹 자막 형식 (`.vtt`). edge-tts가 `--write-subtitles`로 자동 생성. |
| Remotion | React + TypeScript로 영상을 만드는 프레임워크. `useCurrentFrame()`으로 현재 프레임 접근. |
| useCurrentFrame | Remotion 훅. 현재 렌더링 중인 프레임 번호(0, 1, 2...) 반환. |
| interpolate | Remotion 유틸. 입력 범위를 출력 범위로 선형 매핑. `interpolate(frame, [0,24], [0,1])`. |
