# 70_dev_study — 앱·영상 개발 리서치

> **목적**: unit01(소인수분해)을 시작으로, MathTelling 콘텐츠를 정적·인터랙티브·영상으로
> 만들기 위한 기술 스택 연구 및 프로토타입 계획.
>
> **원칙**: 파일 하나 = 목적 하나, 500줄 이내. 로그인 없음. 가능하면 빌드 없음.

---

## 문서 구조

| 파일 | 내용 |
|---|---|
| `01_stack-comparison.md` | 전체 기술 스택 비교표 (한눈에) |
| `02_web-interactive.md`  | HTML/CSS/JS 정적 + 인터랙티브 설계 가이드 |
| `03_video-tools.md`      | Remotion · HyperFrames · Motion Canvas · Manim 비교 |
| `04_unit01-plan.md`      | unit01 구체적 구현 단계 계획 |

---

## 결론 미리보기 (상세는 각 문서에)

| 레이어 | 도구 | 언제 |
|---|---|---|
| 정적·인터랙티브 웹 | Vanilla HTML/CSS/JS | 지금 즉시 |
| 영상 (1순위) | **HyperFrames** (HeyGen) | 단기 — HTML 그대로 MP4 |
| 영상 (2순위) | **Remotion** | 중기 — React 기반, 파라메트릭 |
| 수학 애니메이션 | **Motion Canvas** | 장기 — 공들인 시퀀스 필요할 때 |

---

## Playwright 필요한가?

**불필요.** HTML 파일은 브라우저에서 그냥 열면 됨.
Playwright MCP는 Claude가 자율적으로 브라우저를 제어/테스트해야 할 때 쓰는 것.
이 프로젝트는 그 단계가 아님.
