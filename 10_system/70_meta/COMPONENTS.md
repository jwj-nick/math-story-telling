# 30_COMPONENTS — UI 공통 컴포넌트

> HTML 앱에서 반복 사용되는 UI 부품 모음. 컴포넌트별 의도·CSS 클래스 스니펫·사용 사례를 명시.
> 새 패턴에서 컴포넌트가 등장하면 여기에 추가. 코드 사본은 자식 프로젝트의 실제 HTML 파일에서 참조.

## 컴포넌트 표

| ID | 이름 | 어디서 첫 등장 | 핵심 CSS class |
|---|---|---|---|
| C01 | tab-nav | 사회 step1 (2604) | `.tab-bar`, `.tab-btn` |
| C02 | form-mirror | 사회 step2 | `.form-item`, `.form-label`, `.form-line` |
| C03 | hint-toggle | 사회 step2 | `.hint-toggle`, `.hint-body` |
| C04 | good-vs-bad | 사회 step2 | `.ex-bad`, `.ex-good`, `.ex-label` |
| C05 | concept-card | 사회 step2 | `.ccard`, `.concept-grid` |
| C06 | think-list | 사회 step2 | `.think-list`, `.think-q` |
| C07 | char-counter | 한국사 정도전 가이드 | (JS — `.length` 비공백/전체) |
| C08 | think-box ⭐ | 사회 step5 (신규) | `.think-box`, `.tb-title`, `.tb-q` |
| C09 | storybook | 한국사 정도전 심화 | `stories[]` 배열 + prev/next |
| C10 | matching-game | 한국사 정도전 심화 | 선택→매칭 로직 + alert/reveal |
| C11 | simulator | 한국사 정도전 심화 | 5 textarea → 합성 출력 + copy/reset |
| C12 | persistent-textarea | 한국사 정도전 심화 | localStorage(`_sim_v1`, `_q_v1`) |
| C13 | copy-btn | 한국사 모범답안 | `copyText()` 함수 |
| C14 | self-assessment | 사회 step6 | 별점 표 (★★★★ / ★★★ / ★★ / ★) |
| C15 | standard-box | 사회 step6 | 성취기준 박스 (`.standard-box`, `.sb-code`) |
| C16 | back-nav | 사회/한국사 deploy | 헤더 좌상단 `← Subject_1_1` 링크 |

---

## 컴포넌트별 상세 (선별)

### C02. form-mirror (실제 양식 미러)

**의도**: 학생이 실제 수업 시간에 답안지에 적을 양식을 미리 시각적으로 보여줌. 색 테두리 = "이건 진짜 양식"이라는 신호.

**기본 CSS**:
```css
.form-item { border: 2px solid <ACCENT>; border-radius: 10px; padding: 16px; }
.form-item .form-label { font-size: 13px; color: <ACCENT>; }
.form-item .form-lines { background: <ACCENT_TINT>; padding: 10px; }
.form-line { border-bottom: 1px solid #ddd; height: 32px; }
```

**색 매핑 사례** (사회 메가시티):
- Step 2 미디어연결: 주황 #e67e22
- Step 3 긍정: 주황
- Step 4 문제: 빨강 #c0392b
- Step 5 해결: 청록 #16a085
- Step 6 성찰: 보라 #8e44ad

### C08. think-box (사고 가이드 박스) ⭐ 신규

**의도**: 학생 본인 생각을 끌어내야 하는 단계에서 자문 질문 묶음을 시각적으로 제공.
**언제**: 답안의 절반 이상이 본인 의견인 단계 (Step 5 해결, Step 6 성찰).

**CSS**:
```css
.think-box {
  background: linear-gradient(135deg, <PALE>, <TINT>);
  border: 2px dashed <ACCENT>;
  border-radius: 10px;
  padding: 14px;
}
.think-box .tb-title { font-size: 12px; font-weight: 700; color: <DARK>; }
.think-box .tb-q { font-size: 13px; padding: 5px 0; }
.think-box .tb-q::before { content: "🤔 "; }  /* 또는 "💭 " */
```

**예시 사용**:
```html
<div class="think-box">
  <div class="tb-title">🧠 시작 전 자문 3가지</div>
  <div class="tb-q">내가 만약 정책 결정자라면, 첫 번째 카드는?</div>
  <div class="tb-q">그게 정말 효과 있을까? (한계는?)</div>
  <div class="tb-q">나 한 명이 오늘 시작할 수 있는 행동은?</div>
</div>
```

### C09. storybook

**의도**: 인물·사건을 5장면 정도로 prev/next로 넘기며 읽기. 책 같은 흐름.
**사용**: 한국사 정도전 인생 (1342→1375→1377→1392-1398→1398).

**구조**:
```js
const stories = [
  { year: '1342', title: '...', body: '...' },
  ...
];
let idx = 0;
function render() { /* idx 페이지 표시 */ }
```

### C10. matching-game

**의도**: 5쌍의 개념을 짝짓기로 능동 학습. 단순 표 암기보다 정착률 높음.
**사용**: 한국사 정도전 5개혁 ↔ 5처방.

**핵심 로직**:
- selectedLeft 추적
- 오답: alert + 자동 해제
- 정답: 매칭 표시 + 양쪽 disabled

### C16. back-nav

**의도**: 세부 앱에서 상위 인덱스로 복귀. mobile에서 브라우저 뒤로가기 대신 명시적 경로.
**사용**: high1/society/, high1/history/ 모든 세부 페이지.

**구현 (inline)**:
```html
<header>
  <a href="index.html" style="display:inline-block;font-size:12px;color:rgba(255,255,255,0.85);text-decoration:none;margin-bottom:8px;opacity:0.9;">← Society_1_1</a>
  <h1>...</h1>
</header>
```

> 향후 전체 컴포넌트를 `.claude/skills/_components/` 같은 공통 자산으로 추출하면, skill에서 `참조: C08 think-box` 식으로 호출 가능해질 듯 (Q02 참고).

---

## 새 컴포넌트 추가 절차

1. 자식 프로젝트의 실제 HTML에서 새 UI 부품 발견
2. 위 표에 한 줄 추가
3. 핵심 의도 + CSS 스니펫 (이 파일 본문)
4. 만약 3회 이상 사용되면 → `50_BLUEPRINTS.md` 에서 skill·component 자산화 후보로 등재
