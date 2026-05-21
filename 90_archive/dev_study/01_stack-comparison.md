# 01 — 기술 스택 비교표

> 작성: 2026-04-29 / MathTelling unit01 시각화 결정용

---

## 한눈에 비교

| 레이어 | 도구 | 빌드 필요 | 난이도 | 결과물 | 권장 시점 |
|---|---|---|---|---|---|
| **정적 웹** | HTML + CSS | ❌ 없음 | ★☆☆ | .html 파일 | 지금 |
| **인터랙티브 웹** | + Vanilla JS | ❌ 없음 | ★★☆ | .html + .js | 지금 |
| **컴포넌트 웹** | Astro (SSG) | ✅ 있음 (npm) | ★★☆ | 정적 사이트 | 규모 커지면 |
| **인터랙티브 SPA** | React + Vite | ✅ 있음 (npm) | ★★★ | 앱 배포 | 필요할 때만 |
| **HTML → 영상** | **HyperFrames** | ✅ 있음 (CLI) | ★★☆ | MP4 | 단기 |
| **React → 영상** | **Remotion** | ✅ 있음 (npm) | ★★★ | MP4 | 중기 |
| **수학 애니메이션** | **Motion Canvas** | ✅ 있음 (npm) | ★★★ | MP4 / SVG | 장기 |
| **수학 애니메이션** | **Manim** | ✅ 있음 (Python) | ★★★ | MP4 | 장기, Python선호시 |

---

## 정적·인터랙티브: Vanilla JS vs React

### Vanilla HTML/CSS/JS (현재 노선)
```
장점
 - 빌드 없음, 파일 열면 바로 실행
 - Node.js 설치 불필요
 - 파일 하나 = 독립 실행
 - L2 슬라이더처럼 Claude Code가 바로 만들어줌
단점
 - 컴포넌트 재사용 수동 관리
 - 규모 커지면 코드 중복 발생
```

**결론**: 이 프로젝트 규모(단원당 파일 4~6개)에서는 충분히 최적.  
파일 하나가 500줄 안쪽이면 유지보수도 쉬움.

### React + Vite (나중에 필요하면)
```
장점
 - 컴포넌트 재사용, 상태 관리 편리
 - TypeScript 지원
단점
 - npm install, 빌드 단계 추가
 - 딸이 코드 보기 어려워짐 (JSX 낯섦)
```

**결론**: 단원이 8개 이상 쌓이고 공통 컴포넌트가 필요해지면 그때 검토.

---

## 영상 레이어: 3가지 옵션

### Option A: HyperFrames (HeyGen, 오픈소스)
```
핵심: HTML/CSS/JS 그대로 → MP4
원리: headless Chrome이 페이지를 렌더링 → 프레임 캡처 → FFmpeg 인코딩
```
- Apache 2.0 라이선스, 무료, 상업 이용 가능
- **Claude Code에 first-class 지원** (skill로 통합 가능)
- CSS/GSAP/Lottie/Three.js 애니메이션 그대로 사용
- CLI 명령 하나로 렌더링: `hyperframes render --output out.mp4`
- 50+ 사전 제작 블록 (전환 효과 등)
- **적합한 경우**: 이미 만든 HTML 인터랙티브 → 영상으로 변환, 설명용 자막 영상

```
필요한 것: Node.js + npm + FFmpeg (또는 Docker)
```

### Option B: Remotion
```
핵심: React 컴포넌트 = 영상 프레임 → MP4
원리: 각 프레임을 React로 렌더링, currentFrame 훅으로 애니메이션 제어
```
- 소스 공개, 회사 사용 시 유료 라이선스 필요 (개인/교육용은 무료)
- React 지식 필요
- Claude Code + Remotion 조합으로 AI 생성 영상 사례 많음
- **적합한 경우**: 데이터 기반 영상, 파라메트릭 콘텐츠, 여러 버전 자동 생성

```
필요한 것: Node.js + npm + React 기초
```

### Option C: Motion Canvas
```
핵심: TypeScript generator 함수 → 시퀀스 애니메이션 → MP4/SVG
원리: yield로 애니메이션 시퀀스를 순서대로 기술 (3B1B 스타일)
```
- MIT 라이선스, 완전 무료
- 제어력이 가장 높음 (프레임 단위 타이밍 제어)
- **적합한 경우**: 소수의 체처럼 "단계별로 진행되는" 수학 개념 애니메이션

```
필요한 것: Node.js + npm + TypeScript 기초
```

### Option D: Manim (3Blue1Brown)
```
핵심: Python → LaTeX + 기하 → MP4
```
- Math-To-Manim 플러그인으로 Claude Code에서 바로 사용 가능
- 수학 전용 라이브러리 (수식, 기하, 그래프 내장)
- Python 환경 필요
- **적합한 경우**: 순수 수학 시각화 (방정식 변환, 기하 증명)

---

## 이 프로젝트에서의 권장 진행 순서

```
Phase 1 (지금)     → Vanilla HTML/CSS/JS
                     unit01 인터랙티브 4페이지 완성

Phase 2 (단기)     → HyperFrames 설치 + 소수의 체 영상 제작
                     이미 만든 HTML sieve.html → MP4 변환 시도

Phase 3 (중기)     → Remotion 검토
                     단원 3~4개 이후, 공통 컴포넌트 필요해지면

Phase 4 (선택)     → Motion Canvas
                     "에라토스테네스의 체" 같은 공들인 수학 애니메이션
```
