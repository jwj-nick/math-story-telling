---
name: se_unit_plan
description: 단원 파이프라인을 킥오프한다. chatlog 파일을 생성하고 Phase 1~5 체크리스트를 세팅. 호출 예시 — "/se_unit_plan unit02 정수와유리수", "/se_unit_plan unit03".
---

# se_unit_plan — 단원 파이프라인 킥오프 스킬

## 인자 형태
```
/se_unit_plan unit02 정수와유리수
/se_unit_plan unit03
```

## 절차

### 1. chatlog 파일 생성
`00_project_hub/chatlog/YYMMDD_unitNN_[단원명].md` 생성

### 2. 파이프라인 체크리스트 작성

```markdown
# Unit NN — [단원명] 제작 파이프라인

## Phase 1: 개념 (축 A)
- [ ] 40_BaseDocs/NN_단원명/ 검수 (/se_concept_review)
- [ ] Nick과 개념 범위·깊이 협의

## Phase 2: 이야기 (축 B)
- [ ] 인물/에피소드 리서치
- [ ] 스토리 텍스트 초안 (/se_story_write)
- [ ] Nick 리뷰 → 확정
- [ ] 50_units/NN/story/ 저장

## Phase 3: 수학 언어 (축 C)
- [ ] 연결 L모듈 결정
- [ ] 인터랙티브 도구 제작 → 40_BaseDocs/00_literacy/LN_*/

## Phase 4: 도구 (축 A+B 통합)
- [ ] 인터랙티브 HTML 앱 → 50_units/NN/app/
- [ ] 영상 스크립트 → 50_units/NN/video/
- [ ] /se_video_make 실행

## Phase 5: 문제 연습 (축 D)
- [ ] 대표 문제 선정
- [ ] 오답노트 체계 → 50_units/NN/problems/
- [ ] 연습 문제 생성

## 메모
[Nick과의 협의 내용 기록]
```

### 3. 디렉토리 준비
필요한 하위 폴더 생성:
- `50_units/NN_단원명/story/`
- `50_units/NN_단원명/app/`
- `50_units/NN_단원명/video/`
- `50_units/NN_단원명/problems/`
- `50_units/NN_단원명/feedback/`

### 4. 보고
> Unit NN [단원명] 파이프라인 킥오프 완료. chatlog: [파일명]. Phase 1부터 시작합니다.
