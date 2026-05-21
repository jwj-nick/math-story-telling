# 40_PRINCIPLES/deploy — 앱 배포 원칙

## D1. 파일명 규칙

- 한국어 파일명 → URL 인코딩 이슈 방지 위해 영문 romanize
- 예: `한국사_정도전_가이드.html` → `1sem_perf_jeongdojeon_guide.html`
- 형식: `<학기>sem_<용도>_<주제>_<세부>.html`
- 용도 접두: `perf` (수행평가), `exam` (시험), `mid` (중간고사) 등

## D2. 디렉토리 = 과목 그룹

```
high1/
├── index.html              ← 과목 카드
├── math/                   ← Math_1_1
├── science/                ← Science_1_1
├── society/                ← Society_1_1
├── history/                ← History_1_1
└── korean/                 ← Korean_1_1 (2026-05-12 추가)
```

- 각 폴더에 `index.html` (랜딩 페이지)
- 최상위 `high1/index.html` 에 과목 카드
- 자식 폴더의 카드 = 학년·학기 표기 `Subject_<grade>_<sem>` (예: `Math_1_1`)

## D3. back-nav 필수

- 모든 세부 페이지 → 헤더 좌상단에 상위 index 링크
- 헤더 배경이 진하면 `rgba(255,255,255,0.85)` 흰색 톤
- 30_COMPONENTS.md C16 참조

## D4. 별도 repo: `jwj-nick.github.io`

- 학생용 배포 = `C:/Nick/30_Apps/jwj-nick.github.io/high1/`
- 본 프로젝트 (`C:/Kids/...`)는 작업·소스 repo (`jwj-nick/high_son`)와 별개
- 두 repo 동기화는 cp 또는 build script (현재 수동)

## D5. Commit 단위

- **한 commit = 한 과목** (2026-05-11 확정)
- 또는 한 commit = 한 cross-cutting 기능 (back-nav 같은 시스템 변경)
- Push 는 여러 commit 모은 후 한 번에 (2026-05-11 확정)

## D6. URL 한국어 회피

- GitHub Pages URL = `jwj-nick.github.io/high1/society/1sem_perf_megacity_step1.html`
- 한국어 디렉토리·파일은 URL 인코딩 문제 발생 가능 → 영문화 강제

## D7. 이미지 자산

- 원본 한국어 이름 → romanize (예: `정도전_초상.png` → `jeongdojeon_portrait.png`)
- HTML 내 `src` 도 함께 갱신
- 원본은 작업 repo에 유지 (한국어 이름 그대로)
