<!-- external_repos.md — 옛 git history 참조 메타데이터 -->

# 외부 Repo 참조 — math-story-telling 통합 전 원본들

> 이 repo는 D2 결정에 따라 깨끗한 git history로 시작됨 (2026-05-21).
> 옛 repo들의 코드 변경 이력이 필요하면 아래 GitHub URL을 체크아웃하라.

---

## 통합된 4개 원본

### 1. mid_eun (가장 성숙한 base)
- GitHub: https://github.com/jwj-nick/mid_eun
- 로컬: `C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/`
- 마지막 commit (마이그 시점): `68b6b3c feat: register se_story_video_v1_5 skill`
- 총 commit 수: 13
- 주요 commit:
  - `68b6b3c` feat: register se_story_video_v1_5 skill
  - `4e5e0ef` Add 90_video pipeline — 13단원 이야기 영상 소스 추가
  - `8c13c2e` Units 11-13 — types.html 및 단계별 풀이(walk) 추가
  - `609ab9f` Units 08-10 — types.html 및 단계별 풀이(walk) 추가
  - `b0ab5c0` Units 05-07 — types.html 및 단계별 풀이(walk) 추가
- 역할: 13단원 작업, skill SSOT (14개), chatlog, learner profile, 90_video v1

### 2. mathtelling (monorepo 골격)
- GitHub: https://github.com/jwj-nick/mathtelling
- 로컬: `C:/Kids/90_Workspace/mathtelling/`
- 마지막 commit: `ce8e1da fix(unit-01): switch image extension jpg→png`
- 총 commit 수: 5
- 주요 commit:
  - `ce8e1da` fix(unit-01): switch image extension jpg→png to match generated assets
  - `1be418f` feat(channel): v1.5 pipeline defined + unit-01 v1.5 source built
  - `34fe3d1` feat(unit-01): story·concepts·problems·channel seed + math1 home
  - `15cbe9c` feat: content/people 5인 + content/units/01 meta + apps/math1/unit-01/index
  - `673532a` init: mathtelling monorepo 골격 초기화
- 역할: apps/math1 (unit-01 신생), channel(v1.5), content/people·units 메타, system 메타 (principles·context·skills/se_distill_principles·proposals·insights)

### 3. mathtelling-design-system
- GitHub: https://github.com/jwj-nick/mathtelling-design-system
- 로컬: `C:/Kids/90_Workspace/mathtelling-design-system/`
- 마지막 commit: `68f725c init: design-system v0.1 — tokens 4종 + subjects/math + dist`
- 총 commit 수: 1
- 역할: CSS 토큰 4종 (colors, motion, spacing, typography), subjects/math, dist
- 새 위치: `20_packages/design-system/`
- public, OSS-able

### 4. 00_LearningSystem
- 위치: `C:/Kids/00_LearningSystem/` (git 아님)
- 역할: 메타 비전 (중1+고1 양쪽 패턴, VISION/COMPONENTS/BLUEPRINTS/MASTER_PLAN/LEARNERS/ROADMAP/PATTERNS/PRINCIPLES/OPEN_QUESTIONS/chatlog)
- 새 위치: `10_system/70_meta/`
- 원본 백업: `90_archive/00_LearningSystem_original/`

---

## 옛 repo들의 미래

- **GitHub**: 그대로 둠. README에 "moved to jwj-nick/math-story-telling" 한 줄 추가 권장 (Q8 — Nick 수동 결정).
- **로컬**: 마이그 검증 후 1주일 보관 → Nick이 안전 확인 후 폴더 삭제 가능.

---

## 마이그 메모

- 일자: 2026-05-21 (가이드 작성) / 2026-05-22 (실행)
- 방식: D2 깨끗 시작 (subtree merge 안 함)
- 안전망: `90_archive/`에 옛 구조 원본 복사 보관
  - `90_archive/00_LearningSystem_original/` — SRC4 전체
  - `90_archive/10_docs_original/` — mid_eun/10_docs 전체
  - `90_archive/dev_study/` — mid_eun/01_dev_study
  - `90_archive/mid_eun_archive/` — mid_eun/archive
  - `90_archive/mid_eun_CLAUDE.md` — 옛 진입점
- 참조 가이드: `00_project_hub/20_plan/260521_migration_plan.md`
- Round 1·2 결정: `00_project_hub/10_chatlog/260521_repo_consolidation*.md`
