# Q06 — APP_PRINCIPLES 비수학 영역 확장

> 상태: 🟡 NCC가 부분적 통합. 정식 확장 필요.

## 질문

현재 `APP_PRINCIPLES.md`(70_HS/2604) 는 **수학 오답노트 앱**에 특화:
- page-0 (문제) / page-1~N (풀이) / 요약 구분
- JSXGraph 슬라이더 lazy init
- 그림 표시 원칙

비수학(사회·한국사·국어·영어) 앱에는:
- 양식 미러 박스 (form-item)
- 모범답안 마지막 탭
- think-box (사고 가이드)
- 글자수 카운터

같은 비-수학 원칙들이 적용 중인데, **명시적 원칙 문서로 통합**할 것인가?

## 옵션

### (A) 통합 v2 작성

- `40_PRINCIPLES.md` 안에 `A. 앱 설계 원칙` 섹션 (현재 형태)
- 수학·비수학 모두 적용되는 원칙 (점진적 공개·빈칸·단일파일)
- 영역별 부록 (수학 한정·비수학 한정)

### (B) 두 문서 병존

- `APP_PRINCIPLES_math.md` + `APP_PRINCIPLES_nonmath.md`
- 또는 `APP_PRINCIPLES_v2_general.md` + 수학 부록

### (C) 현행 유지

- 자식 프로젝트의 APP_PRINCIPLES.md 그대로
- 메타 시스템은 추상 원칙만 (현재)

## NCC 제안

**(A) 통합 v2**가 자연스러움.

구조 안:
```
40_PRINCIPLES.md
  A. 앱 설계 원칙
    A1. 점진적 공개 (모두 적용)
    A2. 빈칸 유지 (모두 적용)
    A3. 단일 HTML (모두 적용)
    A4. 모바일 대응
    A5. [수학 한정] JSXGraph lazy init, 슬라이더 page-0 금지
    A6. [수행평가 한정] 양식 미러 + 모범답안 마지막
    A7. [논술 한정] 글자수 카운터 + 공백/비공백 동시 표시
```

## (Nick) 응답

> (Nick):
> - (A) 통합 v2 가 좋은가?
> - 또는 영역별 별도 문서 (B)?
> - 우선 미루고 자식 프로젝트 그대로 (C)?

B 가 좋음. 나중에 많은 과목들 특수성 문서들이 생기고, common 문서가 있는 형태를 선호함.

---

## 결정 후 적용
- 자식 프로젝트의 APP_PRINCIPLES.md 와 이 문서 정합성 확인
- `app-reviewer` agent 의 검토 범위 확장
