# 40_PRINCIPLES/math — 수학 한정 원칙

> 수학 오답노트·연습 앱, MathTelling 단원 앱에 적용.
> 출처: `70_HighSchool/2604_고1_중간고사/APP_PRINCIPLES.md` (오답노트), MathTelling APP_PRINCIPLES.md (단원 앱).

## M1. page-0 (문제 페이지)

### 반드시 표시
- 원본 시험지 문제 텍스트 — **단어·기호 하나도 추가/삭제 금지**
- 선택지 ①~⑤ (객관식)
- 원본 시험지 그림과 구도가 동일한 **정적 SVG** 또는 원본 JPG
- 배점

### 절대 금지
| 금지 | 이유 |
|---|---|
| 풀이 중 도출해야 할 수치/좌표 | 풀이 흐름 파괴 |
| JSXGraph 슬라이더 | 탐구는 풀이 단계에서 |
| 정답 힌트 공식/변환 | 스스로 발견해야 할 과정 |
| 축 좌표 수치 표기 | 원본에 없는 정보 |

## M2. page-1~N (풀이 페이지)

- 각 페이지 = **하나의 단계** (번호 + 제목 + "왜 이 단계인가" 필수)
- 해당 단계에서 새로 도출한 정보만 공개

### JSXGraph 인터랙티브
- 파라미터(m, a 등) 변화 탐구 시
- 해당 단계에서 파라미터를 **처음 도입하는 시점**
- 초기화: `goTo(n)` 호출 시 lazy init (hidden 시 초기화 실패)

### warn-box 필수
- 학생이 실제로 틀리는 포인트 명시

## M3. 요약 페이지

- 핵심 풀이 흐름 3~5줄 (번호 목록)
- 정답 (큰 글자, answer-box)
- 약점 태그 (tag 요소)

## M4. 수식 표기

- KaTeX (`$...$`, `$$...$$`)
- 도형: Mermaid 또는 ASCII art
- 그림 의도가 모호하면 `[FIG: 설명]` 플레이스홀더

## M5. MathTelling 추가 원칙

- 4축 (개념·이야기·언어·문제) 모두 운영
- 단원당 5단계: index → story → concepts → problems/basic → problems/type → problems/deep
- 5/12 update: app/ 폴더 폐기, unit root로 이동
- 인물 서사 5단계 흐름 (10_docs/02_concept.md)

## 검토 자동화
- agent `se_agent_app_reviewer` (개발 예정) 가 이 원칙 위반 감지·보고
- 현재는 자식 프로젝트의 `app-reviewer` (수학 한정) 활용
