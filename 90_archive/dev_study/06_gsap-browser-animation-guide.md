# Story 영상 앱 — 구동 원리 설명서

> 이 문서는 MathTelling story 영상 앱의 기술 구조를 실용적 관점에서 정리한다.

---

## 1. 핵심 개념 — "영상 파일 없는 영상"

**GSAP(GreenSock Animation Platform)**은 JavaScript 애니메이션 라이브러리다.
HTML 페이지 안에서 SVG·텍스트·색상을 **JS가 직접 움직인다**.

```
일반 동영상 플레이어:  [.mp4 파일] → 브라우저가 재생
GSAP 애니메이션:      [JS 코드]   → 브라우저가 직접 그리며 애니메이션
```

두 결과물은 사용자 눈에 비슷하게 보이지만 작동 방식이 전혀 다르다.

---

## 2. 우리 프로젝트의 파이프라인

```
①  GSAP HTML 작성
    └─ 90_video/unit*/index.html
       - 5개 장면(scene) SVG + 텍스트 레이아웃
       - 장면 전환·텍스트 등장은 gsap.timeline()으로 제어
       - paused: true  ← Puppeteer가 외부에서 재생 시점을 제어하기 위해

②  edge-tts → narration.mp3
    └─ 한국어 TTS로 나레이션 오디오 생성

③  Puppeteer (headless Chrome) → 프레임 캡처
    └─ JS로 tl.play() 호출 → 브라우저 화면을 초당 30프레임 PNG로 캡처

④  FFmpeg → final.mp4
    └─ PNG 시퀀스 + narration.mp3 합성 → mp4

⑤  배포 선택지
    A. GSAP HTML 직접 배포  → GitHub Pages에서 브라우저가 실시간으로 그림
    B. final.mp4 배포       → 외부 호스팅 필요 (GitHub Releases, YouTube 등)
```

---

## 3. 왜 "Option A"가 작동하는가

`mid1/story/unit*/index.html`은 mp4 파일을 `<video>` 태그로 재생하는 페이지가 **아니다**.
JavaScript(GSAP)가 브라우저 DOM을 직접 그리는 페이지다.

- 파일 업로드 필요: `palettes.css`, 단원별 `index.html` — 텍스트 파일, git으로 배포 가능
- 파일 업로드 불필요: mp4, mp3 — 이미 JS 코드 안에 내용이 있으므로 불필요

**단, `paused: true`가 있으면 JS 애니메이션이 시작되지 않는다** → 빈 화면.
→ `tl.play()` 추가로 해결 (2026-05-17 완료).

---

## 4. Option A가 불가능한 경우

미래에 "진짜 영상"을 사용한다면 GSAP 자동재생 방식은 작동하지 않는다.

| 영상 유형 | Option A 가능? | 이유 |
|---|---|---|
| GSAP JS 애니메이션 (현재) | ✅ 가능 | 영상 파일 없이 JS가 그림 |
| 배우 촬영 영상 | ❌ 불가 | mp4 파일을 브라우저가 받아야 함 |
| AI 생성 이미지 슬라이드 | ❌ 불가 | 이미지 파일 호스팅 필요 |
| Manim / Motion Canvas 렌더 | ❌ 불가 | 최종 산출물이 mp4 |

→ 진짜 영상 쓸 경우: GitHub Releases, YouTube embed, Cloudflare R2 등 외부 호스팅 필요.

---

## 5. 배포 구조

```
소스 레포: github.com/jwj-nick/mid_eun  (비공개 또는 공개)
  └─ 260426_MathTelling_Idea/
      └─ 90_video/unit*/index.html   ← paused:true 유지 (FFmpeg 캡처용)

배포 레포: github.com/jwj-nick/jwj-nick.github.io
  └─ mid1/
      ├─ index.html                  ← 중1 앱 허브
      ├─ math1/                      ← 수학 개념·문제 앱
      └─ story/
          ├─ index.html              ← 13단원 갤러리
          ├─ _assets/palettes.css    ← 단원별 색상 팔레트
          └─ unit01~13/index.html   ← tl.play() 추가 완료
```

---

## 6. 주요 기술 요소

### GSAP timeline
```js
const tl = gsap.timeline({ paused: true });   // 소스용 (Puppeteer)
const tl = gsap.timeline({});                  // 브라우저용 (자동재생)

tl.to('#scene1', { opacity: 1, duration: 0.8 }, 0);
tl.to('#scene1', { opacity: 0, duration: 0.8 }, 4.6);
tl.to('#scene2', { opacity: 1, duration: 0.8 }, 5.0);
// ... 장면 전환 체인
```

### palettes.css — 단원별 색상 팔레트
```css
/* unit07 — 유클리드 */
[data-unit="07"] {
  --bg: #e7e5e4;
  --accent: #65a30d;
  --text: #292524;
  --muted: #57534e;
}
```
13개 단원 각각 고유 색상 테마. `story/unit*/index.html`에서 `../_assets/palettes.css`로 참조.

### 1280×720 고정 캔버스
```html
<meta name="viewport" content="width=1280, height=720" />
```
```css
html, body { width: 1280px; height: 720px; overflow: hidden; }
```
16:9 비율, FFmpeg 표준 HD 해상도. 브라우저 데스크톱에서 보면 좌우가 잘릴 수 있음.
→ 향후 브라우저 뷰 전용 반응형 래퍼(`transform: scale()`) 추가 가능.

---

## 7. 각 파일 역할 요약

| 파일 | 역할 | 수정 가능? |
|---|---|---|
| `90_video/unit*/index.html` | FFmpeg 캡처 소스 (`paused: true` 유지) | 스토리 수정 시만 |
| `mid1/story/unit*/index.html` | GitHub Pages 배포본 (`tl.play()` 포함) | 자유롭게 |
| `mid1/story/_assets/palettes.css` | 단원 색상 팔레트 | 색상 변경 시 |
| `90_video/unit*/narration.mp3` | TTS 오디오 (gitignore, 로컬 전용) | TTS 재생성 시 |
| `90_video/unit*/final.mp4` | 최종 영상 (gitignore, 로컬 전용) | FFmpeg 재렌더 시 |
