<!-- 260521_migration_plan.md -->

# Migration Plan — math-story-telling 신규 Repo 일괄 마이그레이션

> **대상 독자**: 새 세션 (Claude Code, math-story-telling/ 디렉토리에서 열림).
> **이 파일 위치 (참조용)**: `260426_MathTelling_Idea/00_project_hub/plan/260521_migration_plan.md`
> **선행 문서**:
> - Round 1: `00_project_hub/chatlog/260521_repo_consolidation.md` — 결정 맥락
> - Round 2: `00_project_hub/chatlog/260521_repo_consolidation_r2.md` — 최종 구조 (이 파일과 짝)
>
> 작성일: 2026-05-21

---

## 0. 작업 전 준비 (Nick 수동 작업)

### 0.1 GitHub repo 생성
```
이름: math-story-telling
소유자: jwj-nick
공개 여부: Public (민감 자료는 .private/ gitignore)
초기화: README, .gitignore, LICENSE 모두 체크 해제 (로컬에서 생성)
URL: https://github.com/jwj-nick/math-story-telling
```

### 0.2 로컬 clone 위치 결정 (Q1)
- **권장**: `C:/Kids/math-story-telling/`
- (Nick 확정 후 새 세션이 그 폴더에서 시작)

### 0.3 첫 명령 (clone)
```bash
cd C:/Kids/
git clone https://github.com/jwj-nick/math-story-telling.git
cd math-story-telling/
```

→ 빈 디렉토리 (또는 .git만).

### 0.4 ⭐ 마이그 가이드 3개 파일을 새 repo로 미리 복사

새 세션이 새 repo에서 시작될 때 이 가이드 파일들을 즉시 읽을 수 있도록.

```bash
# (Nick이 새 세션 열기 전에 수동 실행)
SRC=C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/00_project_hub
DST=C:/Kids/math-story-telling

mkdir -p "$DST/_migration_docs"
cp "$SRC/chatlog/260521_repo_consolidation.md"    "$DST/_migration_docs/R1_decisions.md"
cp "$SRC/chatlog/260521_repo_consolidation_r2.md" "$DST/_migration_docs/R2_structure.md"
cp "$SRC/plan/260521_migration_plan.md"           "$DST/_migration_docs/MIGRATION_PLAN.md"

# 새 repo에 첫 commit (가이드만)
cd "$DST"
git add _migration_docs/
git commit -m "docs: migration guide (R1 decisions, R2 structure, step-by-step plan)"
```

이제 `C:/Kids/math-story-telling/`에서 Claude Code 새 세션 열 수 있음.

### 0.5 새 세션 첫 입력 (Nick이 새 세션에 보낼 메시지)

```
이 repo는 math-story-telling. 마이그 셋업 진행해주세요.

먼저 _migration_docs/MIGRATION_PLAN.md를 읽고, 그 다음 R1/R2를 읽으세요.
Step 1부터 차례로 진행. Open Questions (Q1-Q9)는 권장 기본값으로 진행하되,
중요 결정은 나에게 확인. 일괄 진행해주세요.
```

### 0.6 마이그 완료 후 `_migration_docs/` 정리

```bash
# Step 14 (첫 commit) 이후 정리
git mv _migration_docs/R1_decisions.md       00_project_hub/10_chatlog/260521_repo_consolidation.md
git mv _migration_docs/R2_structure.md       00_project_hub/10_chatlog/260521_repo_consolidation_r2.md
git mv _migration_docs/MIGRATION_PLAN.md     00_project_hub/20_plan/260521_migration_plan.md
git rm -r _migration_docs/  # 빈 디렉토리 제거
git commit -m "chore: settle migration docs into 00_project_hub/"
```

---

## 1. 마이그레이션 원칙

### 1.1 D2 — 깨끗한 git 시작
- 옛 git history는 **가져오지 않음**
- 대신 `00_project_hub/40_context/external_repos.md`에 metadata 안내
- 옛 repo들은 GitHub에 그대로 둠 (README에 "moved to" 안내만)

### 1.2 D6 — 일괄 마이그레이션
- 한 세션 안에서 모두 cp
- 중간 commit 하나 (스켈레톤 완성 시점)
- 마지막 commit (전체 완료 시점)

### 1.3 파일 처리 모드
| 모드 | 의미 | 적용 |
|---|---|---|
| **COPY** | cp -r (원본 보존) | 모든 마이그 — 옛 repo는 손대지 않음 |
| **MERGE** | 두 곳 자료를 새 위치에 합침 | apps/math1 + 50_units, content/units + 50_units meta 등 |
| **ARCHIVE** | 그대로 90_archive/로 | 옛 CLAUDE.md, 옛 README, 미분류 자료 |
| **GITIGNORE** | 복사 안 함 | .private/ 자료 (feedback 등) |

---

## 2. Step-by-Step 실행

### Step 1 — 폴더 스켈레톤 생성
```bash
cd C:/Kids/math-story-telling/

# 최상위 디렉토리 (##_prefix)
mkdir -p 00_project_hub/{10_chatlog,20_plan,30_history,40_context}
mkdir -p 10_system/{10_principles,20_context,30_skills,35_agents,40_proposals,50_insights,60_workflows,70_meta}
mkdir -p 20_packages/{design-system,video-pipeline}
mkdir -p 30_content/{people,concepts,literacy,research,units}
mkdir -p 40_grades/middle/math1
mkdir -p 40_grades/high
mkdir -p 50_channel/{_templates,_docs,_archive,season-1-ancient}
mkdir -p 60_deploy/{middle-school,high-school,channel}
mkdir -p 70_tools
mkdir -p 90_archive
mkdir -p .claude/{skills,agents}
mkdir -p .private/feedback

# 60_deploy/는 .gitignore 대상 (빌드 산출물). 빈 디렉토리는 .gitkeep으로 표시.
touch 60_deploy/.gitkeep
touch .private/.gitkeep
```

### Step 2 — .gitignore 작성
파일: `.gitignore`
```gitignore
# 민감 자료
.private/
!.private/.gitkeep

# 빌드 산출물
60_deploy/middle-school/*
60_deploy/high-school/*
60_deploy/channel/*
!60_deploy/.gitkeep

# 영상·이미지 binary (생성 가능 자산)
*.mp4
*.mp3
*.wav
50_channel/**/_assets/*.png
50_channel/**/_assets/*.jpg
50_channel/**/_assets/*.jpeg
50_channel/**/_assets/*.webp
50_channel/**/poster*.jpg
50_channel/**/poster*.png

# OS·에디터
.DS_Store
Thumbs.db
*.swp
.vscode/settings.json

# 일시 파일
*.tmp
*.log
```

### Step 3 — 첫 marker commit (빈 스켈레톤)
```bash
git add -A
git commit -m "init: math-story-telling skeleton with ##_ prefix layout"
```

### Step 4 — `(1) mathtelling-design-system` 마이그 (COPY)
```bash
SRC1=C:/Kids/90_Workspace/mathtelling-design-system
cp -r "$SRC1/tokens"   "20_packages/design-system/tokens"
cp -r "$SRC1/subjects" "20_packages/design-system/subjects"
cp -r "$SRC1/dist"     "20_packages/design-system/dist"
cp    "$SRC1/README.md" "20_packages/design-system/README.md"
cp    "$SRC1/CLAUDE.md" "20_packages/design-system/CLAUDE.md"
```

### Step 5 — `(2) mathtelling` 마이그 (COPY + MERGE)
```bash
SRC2=C:/Kids/90_Workspace/mathtelling

# 5.1 system/ → 10_system/ (구조 매핑)
cp -r "$SRC2/system/principles/."  "10_system/10_principles/"
cp -r "$SRC2/system/context/."     "10_system/20_context/"
cp -r "$SRC2/system/skills/."      "10_system/30_skills/"
cp -r "$SRC2/system/proposals/."   "10_system/40_proposals/"
cp -r "$SRC2/system/insights/."    "10_system/50_insights/"
cp    "$SRC2/system/README.md"     "10_system/README.md"
cp    "$SRC2/system/sync-skills.sh" "70_tools/sync-skills.sh"

# 5.2 channel/ → 50_channel/ (직접)
cp -r "$SRC2/channel/_templates" "50_channel/_templates"
cp -r "$SRC2/channel/_docs"      "50_channel/_docs"       # 비어있을 수 있음 (이미 system/principles로 이동)
cp -r "$SRC2/channel/_assets"    "50_channel/_assets"
cp -r "$SRC2/channel/season-1-ancient" "50_channel/season-1-ancient"

# 5.3 content/ → 30_content/ (people만 우선)
cp -r "$SRC2/content/people" "30_content/people"
# content/units는 mid_eun/50_units와 머지 (Step 6.4 참조)

# 5.4 apps/math1 → 40_grades/middle/math1/ (Step 6.5와 머지)
# 일단 staging에 두고 50_units 머지 시 함께

# 5.5 tools/ → 70_tools/
cp -r "$SRC2/tools/." "70_tools/"

# 5.6 Nick_TODO.md → 00_project_hub/30_history/
cp "$SRC2/Nick_TODO.md" "00_project_hub/30_history/Nick_TODO.md"
```

### Step 6 — `(3) mid_eun (260426_MathTelling_Idea)` 마이그 (COPY + MERGE)
```bash
SRC3=C:/Kids/30_MiddleSchool/260426_MathTelling_Idea

# 6.1 00_project_hub/ → 00_project_hub/ (chatlog/plan/history)
cp -r "$SRC3/00_project_hub/chatlog/." "00_project_hub/10_chatlog/"
cp -r "$SRC3/00_project_hub/plan/."    "00_project_hub/20_plan/"
cp -r "$SRC3/00_project_hub/history/." "00_project_hub/30_history/"
# 40_context/는 비어있음 → external_repos.md 신규 작성 (Step 9)

# 6.2 10_docs/ → 10_system/20_context/ + 30_content/literacy/
cp    "$SRC3/10_docs/01_learner-profile.md"   "10_system/20_context/LEARNER_PROFILE.md"
cp    "$SRC3/10_docs/02_concept.md"           "10_system/70_meta/concept.md"
cp    "$SRC3/10_docs/03_literacy-track.md"    "30_content/literacy/00_track_overview.md"
cp -r "$SRC3/10_docs/." "90_archive/10_docs_original/"   # 안전 백업

# 6.3 20_research/ → 30_content/research/
cp -r "$SRC3/20_research/." "30_content/research/"

# 6.4 40_BaseDocs/ → 30_content/concepts/ + literacy/
cp -r "$SRC3/40_BaseDocs/00_literacy/." "30_content/literacy/"
# 나머지 NN_단원명 폴더는 30_content/concepts/로
for d in "$SRC3/40_BaseDocs"/*/; do
  name=$(basename "$d")
  if [[ "$name" != "00_literacy" ]]; then
    cp -r "$d" "30_content/concepts/$name"
  fi
done

# 6.5 50_units/ → 40_grades/middle/math1/ (mathtelling/apps/math1과 머지)
cp -r "$SRC3/50_units/." "40_grades/middle/math1/"
# mathtelling/apps/math1/unit-01/ 안에 50_units에 없는 새 파일만 머지
# (확인 후 NCC가 판단; 기본은 50_units가 더 성숙)
SRC2_APP=$SRC2/apps/math1
# 머지 도우미 — 새 파일만 추가, 충돌 시 안 덮어씀
cp -rn "$SRC2_APP/." "40_grades/middle/math1/" 2>/dev/null || true
cp    "$SRC2_APP/index.html" "40_grades/middle/math1/_index_v_mathtelling.html"  # 충돌 회피, 검토용

# 6.6 80_professional_idea/ → 10_system/70_meta/professional/
cp -r "$SRC3/80_professional_idea/." "10_system/70_meta/professional/"

# 6.7 90_video/ → 50_channel/_archive/v1/
cp -r "$SRC3/90_video/." "50_channel/_archive/v1/"

# 6.8 APP_PRINCIPLES.md → 10_system/10_principles/
cp "$SRC3/APP_PRINCIPLES.md" "10_system/10_principles/APP_PRINCIPLES.md"

# 6.9 .claude/skills/ → 10_system/30_skills/ + .claude/skills/
# 단, mathtelling/system/skills/와 충돌 가능 — mathtelling이 SSOT여야 함
# se_distill_principles는 이미 5.1에서 mathtelling/system/skills로부터 옴
# 나머지 12개 skill (se_concept_review, ... 등)은 mid_eun이 SSOT
for skill in "$SRC3/.claude/skills"/*/; do
  name=$(basename "$skill")
  if [[ ! -d "10_system/30_skills/$name" ]]; then
    cp -r "$skill" "10_system/30_skills/$name"
  fi
done
# .claude/skills/ 거울은 sync-skills.sh로 채움 (Step 10)

# 6.10 .claude/agents/ → 10_system/35_agents/ + .claude/agents/
cp -r "$SRC3/.claude/agents/." "10_system/35_agents/"
cp -r "$SRC3/.claude/agents/." ".claude/agents/"

# 6.11 .claude/settings.local.json → .claude/
cp "$SRC3/.claude/settings.local.json" ".claude/settings.local.json"

# 6.12 CLAUDE.md → 90_archive/ (새 CLAUDE.md는 신규 작성)
cp "$SRC3/CLAUDE.md" "90_archive/mid_eun_CLAUDE.md"

# 6.13 01_dev_study/ → 90_archive/dev_study/
cp -r "$SRC3/01_dev_study/." "90_archive/dev_study/"

# 6.14 archive/ → 90_archive/mid_eun_archive/
cp -r "$SRC3/archive/." "90_archive/mid_eun_archive/" 2>/dev/null || true

# 6.15 feedback/ → .private/feedback/ (gitignore)
# 단, feedback는 50_units/NN/feedback/ 안에도 있음 — 그건 mid_eun에서 옮길 때 같이 옴 (40_grades/.../feedback/)
# 안전을 위해 그것도 .private로 이동
find "40_grades/middle/math1" -type d -name "feedback" | while read fbdir; do
  rel=${fbdir#40_grades/middle/math1/}
  mkdir -p ".private/feedback/$rel"
  mv "$fbdir"/* ".private/feedback/$rel/" 2>/dev/null || true
  rmdir "$fbdir" 2>/dev/null || true
done
```

### Step 7 — `(4) 00_LearningSystem` 마이그 (COPY)
```bash
SRC4=C:/Kids/00_LearningSystem

# 7.1 메타 비전 → 10_system/70_meta/
cp "$SRC4/10_VISION.md"        "10_system/70_meta/VISION.md"
cp "$SRC4/30_COMPONENTS.md"    "10_system/70_meta/COMPONENTS.md"
cp "$SRC4/50_BLUEPRINTS.md"    "10_system/70_meta/BLUEPRINTS.md"
cp "$SRC4/51_MASTER_PLAN.md"   "10_system/70_meta/MASTER_PLAN.md"
cp "$SRC4/60_LEARNERS.md"      "10_system/70_meta/LEARNERS.md"
cp "$SRC4/80_ROADMAP.md"       "10_system/70_meta/ROADMAP.md"
cp "$SRC4/README.md"           "10_system/70_meta/README.md"
cp "$SRC4/SYSTEM_GUIDE.md"     "10_system/70_meta/SYSTEM_GUIDE.md"
cp "$SRC4/CLAUDE.md"           "10_system/70_meta/_old_CLAUDE.md"

# 7.2 디렉토리들
cp -r "$SRC4/20_PATTERNS/."        "10_system/70_meta/PATTERNS/"
cp -r "$SRC4/40_PRINCIPLES/."      "10_system/70_meta/PRINCIPLES_legacy/"
cp -r "$SRC4/70_OPEN_QUESTIONS/."  "10_system/70_meta/OPEN_QUESTIONS/"
cp -r "$SRC4/00_chatlog/."         "10_system/70_meta/_chatlog/"

# 7.3 원본 백업
cp -r "$SRC4/." "90_archive/00_LearningSystem_original/"
```

### Step 8 — content/units 메타 머지
```bash
# mathtelling/content/units/01/meta.json → 30_content/units/01/meta.json
cp -r "$SRC2/content/units/." "30_content/units/"
# 50_units 산출물과 의미가 다름 — content/units는 학년 무관 메타 (인물, 시대 등),
# 40_grades/middle/math1/unit-01_*/는 학년별 산출물 (HTML)
```

### Step 9 — `00_project_hub/40_context/external_repos.md` 신규 작성

파일: `00_project_hub/40_context/external_repos.md`
```markdown
<!-- external_repos.md — 옛 git history 참조 메타데이터 -->

# 외부 Repo 참조 — math-story-telling 통합 전 원본들

> 이 repo는 D2 결정에 따라 깨끗한 git history로 시작됨 (2026-05-21).
> 옛 repo들의 코드 변경 이력이 필요하면 아래 GitHub URL을 체크아웃하라.

---

## 통합된 4개 원본

### 1. mid_eun (가장 성숙한 base)
- GitHub: https://github.com/jwj-nick/mid_eun
- 마지막 commit (마이그 시점): `68b6b3c feat: register se_story_video_v1_5 skill`
- 총 commit 수: ~68
- 역할: 13단원 작업, skill SSOT, chatlog, learner profile

### 2. mathtelling (monorepo 골격)
- GitHub: https://github.com/jwj-nick/mathtelling
- 마지막 commit: `ce8e1da fix(unit-01): switch image extension jpg→png`
- 총 commit 수: 5
- 역할: apps/math1, channel(v1.5), content, system(메타)

### 3. mathtelling-design-system
- GitHub: https://github.com/jwj-nick/mathtelling-design-system
- 역할: CSS 토큰, 디자인 어휘 (현 20_packages/design-system/)
- public, OSS-able

### 4. 00_LearningSystem
- 위치: C:/Kids/00_LearningSystem (git 아님)
- 역할: 메타 비전 (중1+고1 양쪽 패턴, 현 10_system/70_meta/)
- 백업: 90_archive/00_LearningSystem_original/

---

## 옛 repo들의 미래

- **GitHub**: 그대로 둠. README에 "moved to jwj-nick/math-story-telling" 한 줄 추가.
- **로컬**: 마이그 검증 후 1주일 보관 → Nick이 안전 확인 후 폴더 삭제 가능.

---

## 마이그 메모

- 일자: 2026-05-21
- 방식: D2 깨끗 시작 (subtree merge 안 함)
- 점검: `90_archive/`에 옛 구조 원본 복사 보관 (안전망)
- 참조 가이드: `00_project_hub/20_plan/260521_migration_plan.md`
- Round 1·2 결정: `00_project_hub/10_chatlog/260521_repo_consolidation*.md`
```

### Step 10 — sync-skills.sh 경로 갱신
파일: `70_tools/sync-skills.sh` (이미 step 5.1에서 복사)
- SOURCE 변수를 `mathtelling/system/skills` → `10_system/30_skills`로 갱신
- DEST 변수를 `260426_*/.claude/skills` → `.claude/skills` (이 repo 내부)
- agents도 처리하도록 일반화 가능

수정 부분:
```bash
SOURCE="C:/Kids/math-story-telling/10_system/30_skills"      # 또는 ../10_system/30_skills (상대경로)
DEST="C:/Kids/math-story-telling/.claude/skills"             # 또는 ../../.claude/skills
```
- 권장: 상대경로 사용 (스크립트가 70_tools/에서 실행되든 root에서 실행되든 일관성)
- 또는 환경변수로 ROOT 받기

실행:
```bash
bash 70_tools/sync-skills.sh
```

### Step 11 — `CLAUDE.md` 신규 작성

파일: `CLAUDE.md` (repo 루트, 새 세션 진입점)

템플릿 outline (자세한 내용은 90_archive/mid_eun_CLAUDE.md 참고하여 새 폴더 구조로 갱신):

```markdown
# CLAUDE.md — math-story-telling

> 새 Claude 세션이 시작되면 이 파일을 먼저 읽는다.

## 프로젝트 한 줄

수학 단원을 인물 이야기 + 수학 언어 + 인터랙티브 도구 + 문제 연습으로 구성하는 학습 시스템.
중학교 1학년부터 시작, 학년·과목 확장 가능. 시스템 일부는 다른 앱에도 재사용 가능 (packages/).

## 우선순위
1. (a) 흥미 + 이해 + 자신감 ← 최우선
2. (b) 기본 문제 실전력
3. (c) AI로 직접 만드는 경험

## 4축 구조
| 축 | 무엇 | 위치 |
|---|---|---|
| A. 개념 이해 | 각 단원 핵심 개념 명확히 | `30_content/concepts/`, `40_grades/middle/math1/unit-NN/{index,story,concepts}.html` |
| B. 흥미 유발 | 수학자 이야기, 영상 | `30_content/people/`, `50_channel/`, `40_grades/.../story.html` |
| C. 수학 언어 | 기호·표기 메타 학습 | `30_content/literacy/` |
| D. 문제 연습 | 대표 문제, 오답노트 | `40_grades/.../problems/` |

## 디렉토리 인덱스
(루트 ##_ 디렉토리들 한 줄씩)
- `00_project_hub/` — 대화·플랜·메타데이터
- `10_system/` — 원칙·skill·진화 메커니즘
- `20_packages/` — 떼서 다른 앱에 쓸 모듈
- `30_content/` — 학년·매체 무관 SSOT
- `40_grades/` — 학년별 산출물
- `50_channel/` — 영상 소스
- `60_deploy/` — 빌드 출력 (gitignore)
- `70_tools/` — 스크립트
- `90_archive/` — 옛 자료 보관

## 작업 방식 — chatlog 라운드 기반
- 모든 논의·결정·Q&A는 `00_project_hub/10_chatlog/` 파일에 # Round N
- NCC = Nick's Claude Code Co-worker

## 등록된 Skills
(주요 skill 표 — 90_archive/mid_eun_CLAUDE.md 참조하여 작성)

## 등록된 Agents
- `se_agent_unit_orchestrator` — 단원 전체 파이프라인

## 절대 원칙
1. 우선순위 순서 (a) > (b) > (c)
2. 페이스: 단원 1개 = 2~3주
3. `.private/feedback/`은 임의 수정 금지
4. 4축 모두 운영
5. 빈칸·미완성 의도적으로 남김
6. chatlog 파일 기반 대화
7. 시간·토큰 효율
8. Rate limit 인식

## 참고 문서
- 마이그 가이드: `00_project_hub/20_plan/260521_migration_plan.md`
- 옛 CLAUDE.md: `90_archive/mid_eun_CLAUDE.md`
- 외부 repo 참조: `00_project_hub/40_context/external_repos.md`
```

### Step 12 — README.md 신규 작성

파일: `README.md`
```markdown
# math-story-telling

수학 단원을 인물 이야기·인터랙티브 앱·영상으로 가르치는 학습 시스템.

- **대상**: 중학 1학년부터 시작, 학년·과목 확장 가능
- **방식**: 4축 구조 (개념·이야기·수학 언어·문제)
- **재사용**: `20_packages/`의 모듈은 다른 학습 앱에도 사용 가능

## 시작

새 Claude Code 세션은 `CLAUDE.md`부터 읽는다.
사람 독자는 `00_project_hub/10_chatlog/`에서 진행 상황을 확인.

## 라이선스

(TBD — Nick 확정 후)
```

### Step 13 — 검증 (Verification Checklist)
```bash
# 13.1 트리 구조 확인
ls -la
ls 00_project_hub/ 10_system/ 20_packages/ 30_content/ 40_grades/ 50_channel/

# 13.2 skill SSOT 개수 (mid_eun 14 + mathtelling 1 = 15 예상)
ls 10_system/30_skills/ | wc -l

# 13.3 단원 13개 모두 마이그됐는지
ls 40_grades/middle/math1/ | grep -c "^unit"

# 13.4 chatlog 파일 수 (mid_eun 11개 정도 예상 + 이번 r2)
ls 00_project_hub/10_chatlog/ | wc -l

# 13.5 sync-skills.sh 동작 검증
bash 70_tools/sync-skills.sh
ls .claude/skills/ | wc -l   # 위와 같아야 함

# 13.6 .private 안 보임 확인 (gitignore)
git status
# .private/ 가 untracked로 나오면 안 됨. .gitignore 동작 확인.

# 13.7 60_deploy gitignore 동작
ls 60_deploy/
git status   # .gitkeep만 보여야 함
```

### Step 14 — 첫 본격 commit + push
```bash
git add -A
git status   # 검토

git commit -m "feat: migrate from mid_eun + mathtelling + design-system + 00_LearningSystem

- D2 깨끗 시작 (옛 history는 external_repos.md로 참조)
- ##_ prefix 9 최상위 디렉토리
- 14 skill SSOT in 10_system/30_skills + .claude/skills 미러
- 13단원 (Unit 01~13) → 40_grades/middle/math1/
- 90_archive/ 안전망 (옛 구조 백업)
- .private/ gitignore 게이트"

git push origin main
```

### Step 15 — 마이그 완료 보고 + 옛 repo README 갱신 (선택)

옛 GitHub repo들의 README 상단에 한 줄 추가:
```markdown
> ⚠️ This repo has been consolidated into [jwj-nick/math-story-telling](https://github.com/jwj-nick/math-story-telling). This repo is archived.
```

대상:
- jwj-nick/mid_eun
- jwj-nick/mathtelling
- jwj-nick/mathtelling-design-system

---

## 3. 안전·롤백

### 3.1 안전망
- **90_archive/**: 옛 구조 원본 복사 → 마이그 중 잃은 게 있으면 복구 가능
- **옛 로컬 디렉토리 유지**: 1주일은 삭제 안 함
- **옛 GitHub repo**: 그대로 둠 (코드 변경 안 함)

### 3.2 롤백 (필요 시)
- 새 repo가 잘못됐다 → 그냥 마이그 다시. 옛 자료가 사라지지 않음.
- 옛 repo로 돌아가도 됨 (mid_eun에서 계속 작업 가능).

---

## 4. 마이그 후 첫 작업 (다음 chatlog)

새 세션에서 마이그 완료 후:
1. `00_project_hub/10_chatlog/260521_migration_complete.md` 신설
   - 마이그 결과 보고 (몇 개 파일, 검증 결과)
   - Q1~Q9 답변 기록
2. Unit 02 시작 — 새 구조 첫 사용 사례
3. Round 3 — 진화 시작

---

## 5. Open Questions (마이그 중 결정)

> 새 세션이 작업 시작 시 Nick에게 묻거나, 본 가이드의 "권장"으로 진행.

| Q | 질문 | 권장 기본값 | Nick 답변 |
|---|---|---|---|
| Q1 | 로컬 clone 위치 | `C:/Kids/math-story-telling/` |  |
| Q2 | apps/math1 vs 50_units 머지 | 50_units SSOT, apps/math1 신생만 보강 |  |
| Q3 | content/units 메타 vs 50_units | content/units=메타 / 40_grades=산출물 분리 |  |
| Q4 | design-system OSS 별 repo | 새 repo로 흡수 (별 repo는 archive) |  |
| Q5 | 70_HighSchool 통합 | 이번 마이그 범위 밖, 빈 폴더만 생성 |  |
| Q6 | .claude/agents 처리 | 10_system/35_agents/ SSOT, .claude/agents/ 미러 |  |
| Q7 | CLAUDE.md 진입점 | 신규 작성 (mid_eun CLAUDE.md 기반 갱신) |  |
| Q8 | 옛 GitHub repo 처리 | README에 "moved to" 한 줄 (코드 변경 X) |  |
| Q9 | mid_eun deploy 인계 | 60_deploy/middle-school → jwj-nick.github.io/mid1 push (현재 유지) |  |

---

## 6. 변경 이력
- v1 (2026-05-21): Nick D1-D8 답변 기반 일괄 마이그 가이드. 15 step + verification + rollback.
