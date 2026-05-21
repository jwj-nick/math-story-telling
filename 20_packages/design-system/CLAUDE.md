# CLAUDE.md — mathtelling-design-system

> 새 Claude 세션이 이 디렉토리에서 시작되면 이 파일을 먼저 읽는다.

## 이 repo의 본질

**디자인 토큰 & 컴포넌트 라이브러리 (CSS 전용).**

- 빌드 없음. 순수 CSS.
- `mathtelling` monorepo와 `Kids/` 자식 프로젝트들이 import해서 사용.
- 수정 시 `dist/all.css` 업데이트 (현재 수동 @import 관리).

## 작업 원칙

1. **토큰만 추가. 삭제 신중.** 삭제하면 import한 프로젝트 전체 영향.
2. **새 subject 테마 추가**: `subjects/<과목>.css` 신규 + `dist/all.css`에 @import 추가.
3. **새 컴포넌트 추가**: `components/<컴포넌트>.css` 신규 + `dist/all.css`에 @import 추가.
4. **5 원칙 유지** (README 참조): 폰트 2종 / 모션 3단계 / 양피지 팔레트 / 수식 클래스 / 색 강조만.

## 버저닝

- v0.x: 초안. breaking change 자유.
- v1.0: 첫 번째 앱에서 검증 후 안정화.
- v1.x~: 하위호환 유지. breaking change = major bump.
