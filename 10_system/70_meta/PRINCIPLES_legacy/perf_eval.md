# 40_PRINCIPLES/perf_eval — 수행평가 한정 원칙

> P03 (다단계 Step형) + P04 (인물 3앱형) 에 적용.

## PE1. 양식 미러 (form-mirror)

- 학생이 실제 답안지에 적을 양식을 시각적으로 미러링
- 색 테두리 = "이건 실제 양식" 시각 신호
- Step별 색 톤 변경 (단계 인식성)

```css
.form-item { border: 2px solid <ACCENT>; ... }
.form-item .form-lines { background: <ACCENT_TINT>; }
.form-line { border-bottom: 1px solid #ddd; height: 32px; }
```

## PE2. 모범답안은 마지막 탭

- 학생이 먼저 생각·작성한 후 비교하는 흐름 강제
- 모범답안 + 암기 체크리스트 + 자기평가 가이드 묶음

## PE3. think-box (사고 가이드 박스)

- 학생 본인 생각 비중이 큰 단계 (Step 5 해결, Step 6 성찰)에 필수
- 자문 질문 3~5개 묶음
- 점선 테두리 + 그라데이션 배경으로 시각적 구분

```css
.think-box {
  background: linear-gradient(135deg, <PALE>, <TINT>);
  border: 2px dashed <ACCENT>;
}
```

## PE4. 좋은 예 / 나쁜 예 (good-vs-bad)

- 모든 양식 항목에 1쌍 이상 제공
- 나쁜 예 = 막연함·단순 나열
- 좋은 예 = 구체 수치·인과·교과 개념 포함

## PE5. 자료 출처 명시

- 출처 신뢰도 등급 (common.md C1) 준수
- 자료 1~2건 필수, 출처 표 (자료명·기관·연도·URL·핵심 수치)

## PE6. 인물 3앱형 (P04)

- **가이드**: 학습 모드 (밝음 톤), 타임라인·키워드·글자수 카운터
- **모범답안**: 명확 모드 (보라 등), 완성 답안 + 포스터 템플릿
- **심화**: 사색 모드 (네이비·금색), 스토리북·매칭·시뮬레이터·평생 질문
- 3 앱 = 3 가지 학습 모드. 한 앱에 다 넣지 않는다.

## PE7. 채점 기준 명시

- 첫 페이지 (개요 탭)에 배점·수준별 기준 표시
- 학생이 "내 답안은 몇 점 수준인가" 자가 진단 가능하게

## PE8. back-nav 필수 (배포 시)

- deploy.md 참조 — 모든 세부 앱 헤더 좌상단 `← 상위`
