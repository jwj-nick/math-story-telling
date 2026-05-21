# 03 — 영상 제작 도구 비교

> 리서치 날짜: 2026-04-29

---

## 요약 결론

| 순위 | 도구 | 이유 |
|---|---|---|
| 1순위 | **HyperFrames** | HTML 그대로 쓰고, Claude Code 통합, 무료 |
| 2순위 | **Remotion** | 파라메트릭·데이터 주도 영상 필요할 때 |
| 3순위 | **Motion Canvas** | 공들인 수학 시퀀스 애니메이션 |
| 참고용 | **Manim** | 순수 수학 시각화 (Python, 3B1B 스타일) |

---

## 1. HyperFrames (HeyGen, 오픈소스)

**한 줄**: "HTML/CSS/JS를 그대로 MP4로 렌더링한다"

### 작동 원리
```
index.html (CSS/JS 애니메이션 포함)
    ↓ headless Chrome이 각 타임스탬프에서 캡처
    ↓ 프레임 시퀀스
    ↓ FFmpeg 인코딩
output.mp4
```

### 장점
- **Apache 2.0 라이선스**: 완전 무료, 상업 이용도 가능
- **Claude Code 전용 skill 내장**: Claude가 바로 compositions 작성 + render 실행
- 기존 HTML 인터랙티브 → 영상으로 바로 변환 가능
- CSS, GSAP, Lottie, Three.js 모두 지원
- CLI 한 줄: `hyperframes render --input sieve.html --output sieve.mp4`
- 50+ pre-built 전환 효과 블록

### 단점
- headless Chrome + FFmpeg 필요 (Docker 이미지 있음)
- 복잡한 인터랙션은 타임라인 기반으로 별도 작성 필요
- React 기반이 아니라서 Remotion 에코시스템과 별개

### 이 프로젝트에서 쓰는 법
```
1. sieve.html의 애니메이션에 타임라인 CSS를 추가
2. hyperframes render → sieve.mp4 생성
3. 딸에게 동영상 파일로 전달 or 웹에 embed
```

### 설치
```bash
npm install -g @heygen/hyperframes
# 또는 Docker: docker pull heygen/hyperframes
```

### 참고
- GitHub: https://github.com/heygen-com/hyperframes
- Claude Code 가이드: `hyperframes/docs/guides/claude-design-hyperframes.md`

---

## 2. Remotion

**한 줄**: "React 컴포넌트가 곧 영상 프레임"

### 작동 원리
```jsx
// 30fps에서 60프레임짜리 영상 = 2초
export const SieveScene = () => {
  const frame = useCurrentFrame();        // 0~59
  const crossed = getCrossedAt(frame);   // 각 프레임에서 지워진 수
  return <Grid numbers={numbers} crossed={crossed} />;
};
```

### 장점
- React 개발자에게 가장 자연스러운 문법
- 데이터 주도 영상 (8개 단원 × 5개 파라미터 = 자동 40개 영상)
- Remotion Studio에서 실시간 프리뷰
- Claude Code + Remotion 조합 사례 풍부 (검색하면 튜토리얼 많음)

### 단점
- **회사 사용 시 유료 라이선스** (개인·교육은 무료)
- React + TypeScript 기초 필요
- 빌드 단계 있음 (npm run build)

### 이 프로젝트에서 쓰는 법
```
단원이 3~4개 이상 쌓인 후,
"에라토스테네스 이야기" → "알콰리즈미 이야기" 같은
패턴이 반복되는 콘텐츠를 파라미터로 자동 생성할 때
```

### 설치
```bash
npx create-video@latest
# 템플릿 선택 → npm start → localhost:3000에서 Remotion Studio
```

---

## 3. Motion Canvas

**한 줄**: "TypeScript generator 함수로 수학 시퀀스 애니메이션"

### 작동 원리
```typescript
// 3B1B 스타일: 순서대로 일어나는 애니메이션
export default makeScene2D(function* (view) {
  const grid = createRef<Grid>();
  yield view.add(<SieveGrid ref={grid} numbers={range(2, 50)} />);
  
  // 2의 배수 지우기 (1초 걸리는 애니메이션)
  yield* grid().crossMultiples(2, 1);
  yield* waitFor(0.5);
  yield* grid().crossMultiples(3, 1);
  // ...
});
```

### 장점
- **MIT 라이선스** (완전 무료)
- 타이밍 제어가 가장 정밀 (`yield*`로 순서 보장)
- 3B1B처럼 "설명하는 영상"에 최적
- 실시간 핫리로드 프리뷰

### 단점
- TypeScript generator 패턴이 낯설 수 있음
- Remotion보다 커뮤니티 작음 (8K vs 60K 주간 다운로드)
- 수학 특화 컴포넌트가 Manim보다 적음

### 이 프로젝트에서 쓰는 법
```
"소수의 체" 단계별 설명 영상을 손으로 공들여 만들 때.
각 소수를 찾고, 배수를 지우고, 다음 소수로 넘어가는
타이밍 제어된 설명 영상.
```

---

## 4. Manim (3Blue1Brown)

**한 줄**: "Python으로 수학 개념을 영상으로"

### 특징
- 3Blue1Brown이 직접 만들고 사용하는 도구
- LaTeX 수식, 기하 도형, 변환 애니메이션 내장
- Math-To-Manim: Claude Code 플러그인 — 자연어 → Manim 코드 자동 생성
- Python 환경 필요 (pip install manim)

### 이 프로젝트에서 쓰는 법
```
수학 공식이 변환되는 과정 (GCD 호제법, 소인수분해 트리)을
3B1B 스타일로 만들고 싶을 때.
단, Python 환경 세팅이 필요함.
```

---

## 비교 요약

| | HyperFrames | Remotion | Motion Canvas | Manim |
|---|---|---|---|---|
| 언어 | HTML/CSS/JS | React/TSX | TypeScript | Python |
| 빌드 | CLI 한 줄 | npm build | npm build | CLI |
| 라이선스 | Apache 2.0 ✅ | 부분 유료 | MIT ✅ | MIT ✅ |
| Claude 통합 | ★★★ | ★★☆ | ★★☆ | ★★★ |
| 수학 특화 | ★★☆ | ★★☆ | ★★★ | ★★★ |
| 학습곡선 | ★☆☆ | ★★☆ | ★★★ | ★★★ |
| 권장 시점 | **지금** | 중기 | 장기 | 선택적 |

---

## Playwright는 필요한가?

**결론: 이 프로젝트에서 불필요.**

- Playwright는 브라우저 자동화·E2E 테스트 도구
- Playwright MCP: Claude가 자율적으로 브라우저를 열고 조작할 때 사용
- HyperFrames가 내부적으로 headless Chrome을 사용하지만, 이건 사용자가 직접 제어 안 함
- HTML 파일 개발 중 테스트: 브라우저에서 그냥 열면 됨
- 나중에 Claude가 자동으로 "웹 페이지를 열고 스크린샷 찍어서 확인"을 시키고 싶을 때 설치 검토
