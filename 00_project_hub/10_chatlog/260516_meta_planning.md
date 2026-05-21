<!-- 260516_meta_planning.md -->

# 메타 플래닝 — Repo 구조 · 자산 관리 · 학습 시스템 비전 — 라운드 1

> Nick 질문 (요지):
> 1. Phase 0-A가 어디 정리되어 있나?
> 2. Git directory 새로 만들어 운영? 대량 데이터 관리?
> 3. 영상 제작 / 수학 교육 *분리* — skill을 plugin처럼?
> 4. `C:\Kids\00_LearningSystem\` 한번 더 정리 (최종 모습 비전 명확화)
> 5. 수학 교육 확장 (중1 이후) — 앱 먼저, 영상은 따라가는
> 6. 학습 앱 일관성 + 과목 특성
> 7. E-book 출판 가능성 고려

---

## 0. Phase 0-A 위치 답변

**1차 정의처**: `80_professional_idea/first_research/260516_skill_internalization_roadmap.md` §2.1
> Phase 0-A : 0~3개월 (v1.5 안정화)
> - ElevenLabs 도입 / AI 이미지 도입 / 음악 라이브러리 / 페르소나 audit 4 스킬 / 영상 60~90s 확장

**관련 분산 위치**:
- `260516_vision_and_audience.md` §2 Phase 표
- `260516_ncc_synthesis_and_proposals.md` §6 (NCC 추가 권장 4건)

→ Phase 0-A는 *영상 채널 한정* 개념. 본 문서에서 다루는 *학습 시스템 전체*의 Phase는 별도 정의 필요 (§4 참조).

---

## 1. 현재 상태 진단

### 1.1 디렉토리 사실

```
C:\Kids\
├── 00_LearningSystem\           메타 레이어 (패턴·청사진·원칙) — Q03~Q07 1차 정리 완료
│   ├── 10_VISION.md             "흥미·이해·자신감" 최우선
│   ├── 50_BLUEPRINTS.md         B01~B08 skill/agent 청사진 (se_* prefix 규칙)
│   ├── 80_ROADMAP.md            now/3m/12m 마일스톤
│   └── ...
├── 30_MiddleSchool\
│   └── 260426_MathTelling_Idea\ ← 현재 작업 (딸/중1/수학, git: mid_eun)
│       ├── 50_units\            7.5MB (13단원 HTML 앱)
│       ├── 90_video\            **37MB** (13개 final.mp4, raw, mp3)
│       └── 80_professional_idea\ 채널 비전 (이번 라운드 산출)
└── 70_HighSchool\
    └── 2604_고1_중간고사\        아들/고1 (자식 프로젝트 2)
```

### 1.2 Git 사실
- 현재 working repo = `https://github.com/jwj-nick/mid_eun.git`
- `90_video/` 37MB 모두 **아직 untracked** (commit 안 됨)
- `80_professional_idea/` 도 untracked
- 배포는 `jwj-nick.github.io/mid1/math1` (Pages, 별도 동기화 스크립트)

### 1.3 데이터 증가 전망 (v1.5/v2 가면)
| 시점 | 단원수 | 단원당 영상 크기 | 영상 자산 합 |
|---|---|---|---|
| 지금 (v1) | 13 × 50s | ~3MB | **37MB** |
| Phase 0-A (v1.5) | 20 × 60~90s | ~10MB | ~200MB |
| Phase 1 (v2) | 30+ × 90~120s | ~30MB + LoRA 학습 데이터 | ~3GB |
| Phase 2 (v3) | 시즌 2 + I2V | ~100MB / 영상 | ~10GB+ |

→ git에 binary 모두 두면 **6개월 안에 repo 1GB 돌파**. 클론 무거워짐.

---

## 2. 결정 영역 8개 — 옵션과 NCC 권고

### Q1. **영상 프로젝트 = 별도 repo로 분리?** (Repository 구조)

| 옵션 | 구조 | 장점 | 단점 |
|---|---|---|---|
| A. 현행 유지 | `mid_eun` 안에 `90_video/` 같이 | 단순. 하나만 관리. | binary 누적·클론 무거움 |
| B. 영상만 별도 repo | `mid_eun` (수학앱) + `mid_eun-video` (영상) | 영상 자산 격리 | 두 repo 동기화 부담 |
| C. **monorepo + 영상 binary는 git 밖** | `mid_eun` 유지 + 영상 binary는 외부 스토리지, *source만 git* | git 가벼움, 한 repo의 단순성 | 외부 스토리지 운영 필요 |
| D. 채널 자체를 별도 repo | `mid_eun` (수학교육 자식 1) + `mathtelling-channel` (채널·시즌·공개물) | 공개·비공개 분리 깨끗 | 자산 중복 가능 |

**NCC 권고: C → 6개월 후 D 검토**.

이유:
- 지금 영상 = 수학교육의 *일부*. 분리하면 인물 자료·storyboard.md 중복.
- 단, raw.mp4·mp3 같은 *재생성 가능* binary는 git 밖. `final.mp4`도 git 밖 가능 (외부 스토리지).
- 6개월 후 채널이 *독립 정체성* 가지면 그때 D로 split.

**필요 결정**: A/B/C/D 중 1개.

---

### Q2. **대량 데이터 관리** (Storage)

binary 영상·이미지 자산을 어떻게 둘 것인가.

| 옵션 | 방법 | 비용 | 적합도 |
|---|---|---|---|
| α. Git LFS | GitHub LFS bandwidth/storage 구매 | $5/월~ | 작은 팀 표준 |
| β. **Google Drive (Nick 보유?)** + git에 manifest | binary는 Drive, git에는 경로 + sha256 | Drive 기존 사용량 | 1인 운영 적합 |
| γ. AWS S3 / Cloudflare R2 | API 통합 | $1~5/월 (10GB) | 자동화 강 |
| δ. 로컬 NAS / DGX 디스크 | Nick HW 활용 | 0 | 백업 위험 |
| ε. **하이브리드** (final.mp4 = YouTube + GitHub Release, raw = 로컬 only) | binary 종류별 분리 | 0~$5 | 권장 |

**NCC 권고: ε 하이브리드**.

구체:
- `narration.txt`, `storyboard.md`, `config.json`, `index.html` → **git** (텍스트 소스, 가벼움)
- `narration.mp3` → **gitignore** (edge-tts/ElevenLabs로 재생성 가능)
- `raw.mp4` → **gitignore** (HyperFrames 재생성)
- `final.mp4` → **GitHub Release** (단원별 릴리스 태그) 또는 YouTube unlisted
- 인물 LoRA 학습 데이터 (Phase 1) → **로컬 only** + 별도 백업

**필요 결정**: α/β/γ/δ/ε 중. 권고는 ε.

---

### Q3. **Skill을 plugin처럼 분리?**

현재: `mid_eun/.claude/commands/` 안에 모든 skill (수학 + 영상 섞임).

| 옵션 | 구조 | 비고 |
|---|---|---|
| A. 한 폴더 유지 | 현행 | 가장 단순 |
| B. **카테고리 폴더 분리** | `commands/math/`, `commands/video/`, `commands/audit/` | 가독성 ↑ |
| C. **외부 skill repo (npm-like)** | `~/.claude/skills/se-mathtelling-core/` 등 | 재사용 가능 |
| D. 00_LearningSystem 메타로 승격 | canonical은 00_LS, 자식 repo는 *복사* | 두 자식 공유 |

**NCC 권고: B + 일부 D**.

이유:
- 현재 `.claude/commands/`는 `se_story_video.md`, `se_video_make.md`, `se_math_practice.md`, `se_unit_plan.md` 등 약 15개 — 카테고리 분리 시점.
- `se_person_research`처럼 두 자식 공유하는 skill만 *00_LS canonical* + 자식 동기화 (이미 BLUEPRINTS B02a로 결정됨).
- C(외부 repo)는 *Phase 2*. 지금은 과한 추상화.

**필요 결정**:
- 카테고리 분리 시작할지? (Phase 0-A 안에)
- 분리하면 어떤 카테고리? (예: `math/`, `video/`, `audit/`, `meta/`)

---

### Q4. **`C:\Kids\00_LearningSystem\` 재정리** (Vision 명확화)

현재 `00_LS`의 본질:
- ✅ "메타 레이어" 명문화 (`CLAUDE.md`)
- ✅ `se_*` prefix 규칙 (B07 응답)
- ✅ 패턴·청사진·원칙 디렉토리
- ⚠️ 그런데 **"최종 모습"이 명시되지 않음** — Nick 인식 정확함.

**NCC 진단**:
- `10_VISION.md`는 *학생 산출물* 비전. 시스템 자체의 *최종 모습*은 80_ROADMAP §1년에 *암시*만 있음.
- 빠진 것: "이 시스템이 **다음 다음** 자식(예: 70_HighSchool 졸업 후, 또는 새 학년)에도 그대로 상속될 수 있는가?"의 명문화.

**제안: `00_LS` 재정리 작업 = 별도 라운드**.

목적:
1. **최종 모습 한 그림** (5년 후): N명 자식 × M개 과목 × K개 학년 = 같은 패턴으로 운영
2. **승급 규칙 명문화**: 자식 프로젝트의 어떤 결과가 00_LS로 *승급* 되는가
3. **Cross-cutting 자산** 정의: 두 자식이 *공유*하는 skill, 컴포넌트, 디자인 시스템
4. **버저닝**: `00_LS`가 v1.0인가 v0.3인가 (현재 1차 정리는 미명시)

→ **본 라운드에서는 이 작업의 *진행 여부*만 결정**. 본격 작업은 다음 라운드.

**필요 결정**: 00_LS 재정리 라운드 진행? (예/아니오 + 시점)

---

### Q5. **수학 교육 확장 — 중1 이후** (Subject scope)

Nick 의도 인용:
> "수학교육은 중1 과정 말고 이후 과정들 (동영상 이외의 일반 학습 앱부터 진행하고 동영상은 하나씩 따라가는... 분리된 프로젝트인데 연결성이 있는 정도?)"

**핵심**: 영상 ≠ 학습 앱. 학습 앱이 *기본*, 영상은 *선행/장식 트랙*.

| 옵션 | 확장 방향 | 비고 |
|---|---|---|
| A. 중2 단원 앱 부터 (`260700_Mid2_Math/`) | 같은 학생 같은 과목 | 가장 단순 |
| B. 학년 가로 + 영상 채널 트랙 | 앱 트랙 (중1→중2→중3) + 영상 트랙 (시즌 1→2→3) 별도 | 분리 명확 |
| C. 과목 확장 (영어, 과학) | 다른 과목으로 가로 확장 | 70_HighSchool 패턴과 합류 |
| D. **B + 부산물(그림책·이북) 트랙 추가** | 앱·영상·이북 3트랙 | 자산 재활용 극대화 |

**NCC 권고: D**.

이유:
- 앱 트랙이 *생산성 백본*. 영상은 *흥미 유발 보조*.
- E-book 출판 의도(Q7) = 앱 콘텐츠 + 영상 자산의 *제3 출력*. 이미 만든 것 재포장.

**디렉토리 구조 제안**:
```
C:\Kids\30_MiddleSchool\
├── 260426_MathTelling_Idea\    중1 수학 (현재) — *앱 + 영상 v1*
├── 26??_Mid1_Math_Season2\     v2 (Phase 2+, 별도 git?)
├── 27??_Mid2_Math\             중2 수학 (앱 먼저, 영상 1년 늦게)
└── 28??_Mid3_Math\             중3 수학

C:\Kids\00_Publishing\          ⭐ 새 디렉토리 (이북·인쇄 트랙)
├── ebook_pipeline\             앱·영상 → PDF/EPUB 변환
└── season1_chapters\           시즌별 이북 산출
```

**필요 결정**:
- A/B/C/D 중. 권고 D.
- 중2 시작 시점? (v1.5 끝나는 8월? 시즌 1 끝나는 12월?)
- 새 `C:\Kids\00_Publishing\` 디렉토리 만들지?

---

### Q6. **학습 앱 일관성 + 과목 특성** (Design System)

Nick 의도: 일관성(같은 시리즈로 보임) + 과목 특성(수학·영어·과학이 *구분*되어 보임).

| 옵션 | 접근 |
|---|---|
| A. APP_PRINCIPLES.md 한 개 + 과목별 색만 다름 | 가장 단순 |
| B. **공통 디자인 토큰 + 과목별 테마** | CSS 변수로 일관성·차별성 양립 |
| C. 과목별 완전 독립 디자인 | 일관성 포기 |

**NCC 권고: B**.

이유:
- `90_video/_assets/palettes.css` (단원별 컬러) + visual_identity (양피지 톤) 이미 *디자인 토큰* 패턴 사용 중.
- 같은 패턴을 **앱 디자인 시스템**으로 확장 가능.

**구체 제안**:
```
C:\Kids\00_LearningSystem\design-system\
├── tokens\
│   ├── colors.css       기본 팔레트 (양피지 톤 글로벌)
│   ├── typography.css   Pretendard + JetBrains Mono
│   ├── motion.css       ease-in-out 등
│   └── spacing.css
├── subjects\
│   ├── math.css         수학 색·아이콘
│   ├── science.css      과학 색·아이콘
│   └── ...
└── components\          공통 컴포넌트 CSS
    ├── card.css
    ├── walkthrough.css
    └── ...
```

→ `00_LS/design-system/`이 두 자식 + 미래 자식에 *공유 import*.

**필요 결정**:
- B 채택?
- `design-system/`을 `00_LS`에 둘지, 별도 npm 패키지로 갈지

---

### Q7. **E-book 출판 트랙** (Long-term output)

Nick 의도: 앞으로 이북 출판 가능성 고려.

**NCC 진단**: 이미 NCC synthesis §5.4 "수학 그림책 트랙" 제안에 시드 있음. 확장하면:

```
[원천 자산]    storyboard.md / narration.txt / 인물 그림 / SVG / 팔레트
   ↓
[1차 출력]    학습 앱 HTML
[2차 출력]    영상 60~90s
[3차 출력]    그림책 PDF (단원별)
[4차 출력]    시즌 이북 EPUB (5단원 묶음, Amazon KDP 가능)
[5차 출력]    인쇄책 (POD: 부크크 / 교보문고 POD)
```

**핵심 인사이트**: 출판 트랙은 *마지막에 만드는 게 아니라 처음부터 *호환되게 자산을 만드는 것*. 인물 그림이 *영상용 SVG로만* 만들어지면 인쇄 해상도가 부족. *PDF/인쇄 호환 벡터*로 처음부터 만들어두면 5년 후 출판 시 *추가 비용 0*.

**필요 결정**:
- 이북 트랙 *지금부터* 호환성 고려? (= visual_identity v1.0 승급 시 "인쇄 호환" 1항 추가)
- 디렉토리 `00_Publishing/` 신설? (Q5와 합쳐서)
- 1차 이북 출판 목표 시점? (시즌 1 끝나는 12월? 시즌 2 끝나는 2027-?)

---

### Q8. **본 라운드 결정의 우선순위**

8개 영역 중 *지금 결정해야* 하는 것 vs *나중에 해도* 되는 것:

| Q | 영역 | 긴급도 | 권고 |
|---|---|---|---|
| Q1 | Repo 구조 | 🔴 High | 1주 안 결정 (영상 commit 전) |
| Q2 | Storage | 🔴 High | Q1과 함께 |
| Q3 | Skill 분리 | 🟡 Med | 1개월 안 (Phase 0-A 안) |
| Q4 | 00_LS 재정리 | 🟡 Med | 진행 여부만 지금 결정 |
| Q5 | 중1 이후 확장 | 🟢 Low | 시즌 1 끝(8~12월) 직전 |
| Q6 | 디자인 시스템 | 🟡 Med | Phase 0-A 동안 점진 |
| Q7 | 이북 트랙 | 🟢 Low | 호환성 1항만 지금 추가 |
| Q8 | 우선순위 | — | 본 라운드 결과 |

---

## 3. NCC 종합 — 최종 모습 한 장 (5년 후 가설)

```
C:\Kids\                                    학습 시스템 전체
├── 00_LearningSystem\                      메타 레이어 (canonical)
│   ├── design-system\                      ⭐ 공통 디자인 토큰
│   ├── patterns\                           추출된 패턴
│   ├── skills-canonical\                   공유 skill 원본
│   └── docs\                               VISION, ROADMAP, GUIDE
├── 00_Publishing\                          ⭐ 출판 트랙
│   ├── ebooks\                             단원/시즌별 EPUB
│   └── print-ready\                        인쇄용 PDF
├── 30_MiddleSchool\
│   ├── 260426_MathTelling_Idea\            중1 수학 (앱 + 영상 v1)
│   ├── 26??_Mid2_Math\                     중2 수학
│   └── ...
├── 60_Channel\                             ⭐ 영상 채널 트랙 (Phase 2+ 별도)
│   ├── season-1-ancient\                   고대편 5인
│   ├── season-2-medieval\
│   └── ...
└── 70_HighSchool\
    ├── 2604_고1_중간고사\                   고1 (현재 아들)
    └── ...

[Git 전략]
mid_eun           = 30_MiddleSchool/260426_MathTelling_Idea/ (소스만, binary 제외)
mathtelling-ch    = 60_Channel/ (Phase 2 시점 신설)
kids-learning-sys = 00_LearningSystem/ (메타, 공개 가능)
[binary]        = GitHub Releases + YouTube unlisted + 로컬 백업

[Skill 운영]
- 카테고리: math/, video/, audit/, meta/, common/
- 공유 skill (se_person_research 등) = 00_LS canonical + 자식 동기화
- 카테고리별 독립 = 자식 .claude/commands/<카테고리>/

[디자인 시스템]
- 토큰 (color/typography/motion/spacing) = 00_LS/design-system/tokens/
- 과목 테마 = 00_LS/design-system/subjects/
- 두 자식이 import (CSS 또는 build-time copy)

[학습자 흐름]
1. 학습 앱 (앱이 기본) → 학생이 매일 사용
2. 영상 (보조) → 단원 진입 전 흥미 유발
3. 이북 (계절·연간) → 단원 정리 / 가족 공유 / 미래 출판
```

---

## 4. 다음 라운드 — Nick 답변 대기

본 라운드에서 답이 필요한 것 (긴급순):

1. **Q1 (Repo 구조)**: A/B/**C**/D ? *NCC 권고 C*
2. **Q2 (Storage)**: α/β/γ/δ/**ε** ? *NCC 권고 ε 하이브리드*
3. **Q4 (00_LS 재정리)**: 다음 라운드로 진행? (Y/N + 시점)
4. **Q3 (Skill 카테고리 분리)**: Phase 0-A 안에 시작? (Y/N)
5. **Q5 (중1 이후)**: A/B/C/**D** ? *권고 D + Publishing 디렉토리 신설*
6. **Q7 (이북 호환성 1항 추가)**: visual_identity v1.0에 추가 (Y/N)

대답은 *지금 가능한 것만*. 천천히. 1개씩 답해도 OK.

추가하고 싶은 우려·결정·아이디어 환영.

---

## 5. 변경 이력

- R1 (2026-05-16): 8개 결정 영역 정리 + 5년 후 가설 그림.
- R2 (2026-05-16): 방향 전환 — 기존 디렉토리는 base resource, 앞으로 *체계적 신규 git repo*로 진행.

---

# 라운드 2 — 방향 전환: Base Resource + 신규 Repo 체계

> Nick (R2): "현재 있는 디렉터리들은 그냥 base resource 이고 앞으로 만들것들 체계적인 git repo 생성 생각합시다."

## R2-1. 전환의 의미

**Before (R1 가정)**: 기존 `mid_eun` 안에서 영상·앱·이북을 운영. Repo 구조·디렉토리 *정리·재배치* 필요.

**After (R2 결정)**:
- 기존 `mid_eun` / `00_LearningSystem` / `260426_MathTelling_Idea` = **base resource** (참조용 자료 풀)
- *앞으로 만들 것*들 = **신규 git repo**로 *처음부터 체계적*으로 설계
- 기존 자료의 *재정리·마이그레이션 의무 없음*. 필요한 것만 *참조*.

장점:
- 과거의 *시행착오 흔적*에 발 묶이지 않음
- 처음부터 *최종 모습*에 맞춘 구조
- base resource는 *그대로 보존* (역사·디버깅 자료)

R1에서 다룬 Q1, Q3, Q4 일부는 *재정리 전제* — 이제 *신규 설계* 전제로 갱신.

---

## R2-2. 신규 Repo 후보 — Mono vs Multi

### 옵션 M. **Monorepo (Workspace 1개)**
```
mathtelling/                              ← 신규 단일 repo
├── apps/                                 학습 앱 시리즈 (수학·과목 확장)
│   ├── math1/                            중1 수학
│   ├── math2/
│   └── ...
├── channel/                              영상 채널 (시즌·인물)
│   ├── season-1-ancient/
│   └── ...
├── design-system/                        공통 디자인 토큰
│   ├── tokens/
│   ├── components/
│   └── subjects/                         과목별 테마
├── publishing/                           이북·인쇄 출력
│   ├── ebooks/
│   └── print-ready/
├── content/                              ⭐ 원천 자산 (단원·인물·서사)
│   ├── people/                           수학자 데이터
│   ├── units/                            단원별 메타·storyboard
│   └── assets/                           SVG·이미지·BGM
└── tools/                                Claude Code skill plugin
    ├── skills/
    └── agents/
```

**장점**: 한 곳에서 자산 공유, import 단순, 일관성 강제, 한 번 clone.
**단점**: repo 크기 빠르게 증가, 공개 단위 어려움.

### 옵션 P. **Polyrepo (자산 종류별 분리)**
```
mathtelling-apps              학습 앱 시리즈
mathtelling-channel           영상 채널 (Phase 2 공개 candidate)
mathtelling-design-system     디자인 토큰·컴포넌트 (npm publish 가능)
mathtelling-content           단원·인물 콘텐츠 (다른 repo가 import)
mathtelling-tools             Claude Code skill plugin
mathtelling-publishing        이북·인쇄 자동화
```

**장점**: 공개·비공개 분리 깨끗, 각 repo 독립 진화, design-system을 OSS 공개 가능.
**단점**: 6개 repo 동기화 부담, content가 다른 repo에 import되는 의존성 관리.

### 옵션 H. **하이브리드 (소수 분리 + monorepo)**
```
mathtelling                   메인 monorepo (apps + channel + content + tools)
mathtelling-design-system     별도 공개 OSS (재사용 가능)
mathtelling-publishing        별도 (작업 흐름이 매우 다름)
```

**장점**: M·P의 장점 절충. design-system만 외부 공개·재사용 가능.
**단점**: 절충 결정의 *기준선*이 흔들릴 수 있음.

**NCC 권고: H 하이브리드**.

이유:
- design-system은 *진정한 공유 자산*. OSS 공개 시 Nick 포트폴리오 + 외부 기여 가능.
- publishing은 *작업 리듬이 다름* (시즌·연간). 분리하면 main repo 가벼움.
- 나머지 (apps/channel/content/tools) = 자산이 *서로 깊게 의존*. monorepo가 자연스러움.

---

## R2-3. 신규 Repo 명명·범위 권고 (옵션 H 기준)

### Repo 1: `mathtelling` (main monorepo)
- 공개: Phase 2 결정 시점까지 private
- 워크스페이스: `apps/`, `channel/`, `content/`, `tools/`
- 첫 커밋부터 *최종 구조*로 (시행착오 없음)
- base resource 참조: `260426_MathTelling_Idea/`의 검증된 자료만 *선택적 복사*

### Repo 2: `mathtelling-design-system` ⭐
- 공개: 처음부터 public (포트폴리오 가치)
- 내용: 토큰(color/typography/motion/spacing) + 공통 컴포넌트 CSS + 과목 테마
- 배포: GitHub Pages 데모 + 후에 npm publish 가능
- 의존: 없음. *순수 원천*.
- 두 자식 (mid1·high1) 모두 import 대상

### Repo 3: `mathtelling-publishing`
- 공개: private (시즌 1 끝까지)
- 내용: 앱·영상·콘텐츠 → PDF/EPUB/POD 변환 파이프라인
- 시작 시점: Phase 0-B 후반 (3~6개월 후)
- 시작 전엔 main repo 안 `publishing/` 폴더로 시드 운영 후 분리

### (Phase 2 후보) Repo 4: `mathtelling-channel-public`
- 시즌 1 검증 후 *공개 채널 자산만* 분리
- 시즌별 release tag, YouTube 동기화 manifest

---

## R2-4. Base Resource ↔ 신규 Repo 관계

```
[Base Resource — 그대로 보존]
C:\Kids\
├── 00_LearningSystem\           메타 1차 정리 (참조)
├── 30_MiddleSchool\
│   └── 260426_MathTelling_Idea\ 13단원 앱·영상 v1 (참조 + 검증된 자료 추출용)
└── 70_HighSchool\
    └── 2604_고1_중간고사\        아들 자료 (참조)

       ↓ 선택적 참조·복사 (마이그레이션 의무 X)

[신규 Repo — 체계적 설계]
C:\Kids\90_Workspace\            ⭐ 신규 작업 공간 (또는 다른 위치)
├── mathtelling\                 main monorepo
│   ├── content\people\          ← 인물 자료 (base에서 정선 후 정제)
│   ├── content\units\           ← 단원 자료 (base에서 검증된 것만)
│   └── ...
├── mathtelling-design-system\
└── mathtelling-publishing\      (Phase 0-B 후 신설)
```

base resource는 *원본*. 신규 repo는 *깨끗한 시작*. 둘은 *서로 commit 의존성 없음*.

**Nick에게 자유**: base의 어떤 자료를 *새 repo로 가져갈지*는 작업 진행하며 자연스럽게 결정. 통째로 옮길 의무 X.

---

## R2-5. 신규 Repo 시작 — Phase 0-A 통합

기존 Phase 0-A (v1.5 안정화)와 결합:

| 시점 | 작업 | Repo |
|---|---|---|
| **W1 (5-3주차)** | `mathtelling-design-system` 초기화 + 토큰 1차 (양피지 톤 등) | 신규 #2 |
| **W2** | `mathtelling` main repo 초기화 + content/people 5인 + content/units 1편 | 신규 #1 |
| **W3** | apps/math1 1단원 (현행 unit01의 *체계적 재작성*) | 신규 #1 |
| **W4** | channel/season-1 1편 (현행 v1을 design-system import 버전으로 재제작) | 신규 #1 |
| **W5~W12** | 시즌 1 5편 + 시즌 1 5단원 앱 + audit skill 4개 (tools/) | 신규 #1 |
| **W13~** | Phase 0-B 진입. publishing/ 시드 시작 | 신규 #1 (분리는 후) |

→ Phase 0-A = *base resource를 신규 repo로 재출시(re-launch)하는 기간*. 양 = 적음 (5단원, 5편), 질 = 최종 구조 기준.

---

## R2-6. 즉시 결정해야 할 것 (R2)

R1의 Q1~Q8 일부는 *무효*. 신규 repo 전제로 재정렬:

| # | 결정 항목 | 옵션 | NCC 권고 |
|---|---|---|---|
| **R2-D1** | Mono vs Poly vs Hybrid | M / P / **H** | H |
| **R2-D2** | 신규 repo 위치 | `C:\Kids\90_Workspace\` 신설 / 다른 위치 | 90_Workspace |
| **R2-D3** | repo 공개 정책 | design-system은 public, 나머지 private | 동의 |
| **R2-D4** | base resource는 *그대로 동결*? 또는 부분 정리? | 동결 / 정리 | **동결** (시간 절약) |
| **R2-D5** | 신규 시작 시점 | 즉시 / Phase 0-A 끝나고 | **즉시** (Phase 0-A = 신규에서 진행) |

R1의 Q5 (중1 이후 확장), Q6 (디자인 시스템), Q7 (이북 트랙)은 *신규 repo 구조에 이미 포함됨*. 별도 결정 불필요.

---

## R2-7. NCC가 R2 결정 후 자율 진행 가능한 작업

Nick이 R2-D1~D5에 답을 주면, NCC가 자율 진행:

1. `90_Workspace/mathtelling-design-system/` repo 초기화 (README, LICENSE, tokens 1차)
2. `90_Workspace/mathtelling/` monorepo 초기화 (디렉토리 골격 + CLAUDE.md + 워크스페이스 설정)
3. base에서 검증된 자료 *선별 복사* (인물 5인 + 단원 1편 + 영상 v1 1편 reference)
4. design-system token v0.1 (양피지 톤 컬러 + Pretendard 등) 적용한 첫 앱 1개 재출시
5. 새 chatlog 라운드로 진행 보고

NCC 보장: base resource는 *건드리지 않음*.

---

## R2-8. 다음 라운드 — Nick 답변 대기

R2 즉시 결정: D1~D5 중 답 가능한 것.

(R1의 결정 항목 중 *살아남는* 것은 별도 답변 가능):
- R1-Q2 (Storage 정책): 신규 repo에도 그대로 적용 — ε 하이브리드 권고 유지

추가 우려·아이디어 환영.

---

# 라운드 3 — 결정 확정 + 자율 진행 선언

> Nick (R3, 2026-05-19): "NCC 권고에 따름"
> → R2 D1~D5 + R1 Q2 모두 NCC 권고로 확정.

## 확정 결정 요약

| 결정 | 내용 |
|---|---|
| D1 Repo 구조 | **H 하이브리드** — `mathtelling` (monorepo) + `mathtelling-design-system` (공개 분리) + `mathtelling-publishing` (Phase 0-B 후) |
| D2 위치 | `C:\Kids\90_Workspace\` 신설 |
| D3 공개 정책 | `mathtelling-design-system` public / `mathtelling` private |
| D4 base resource | **동결** — 재정리·마이그레이션 없음 |
| D5 시작 | **즉시** — Phase 0-A = 신규 repo에서 진행 |
| Q2 Storage | **ε 하이브리드** — 텍스트 소스만 git / binary는 gitignore + GitHub Releases |

## 자율 진행 계획 (NCC)

**Step 1 (오늘)**: 로컬 구조 초기화
- `C:\Kids\90_Workspace\` 신설
- `mathtelling-design-system\` git init + tokens v0.1 + CLAUDE.md
- `mathtelling\` git init + monorepo 골격 + CLAUDE.md + .gitignore

**Step 2 (로컬 완료 후, GitHub push 전 Nick 확인)**:
- `gh repo create jwj-nick/mathtelling --private`
- `gh repo create jwj-nick/mathtelling-design-system --public`

**Step 3 (repo 연결 후 자율)**:
- base에서 인물 5인 data 정선 → `content/people/`
- base unit01 storyboard/narration 정선 → `content/units/01/`
- apps/math1 unit01 재출시 (design-system import 기반)

진행 상황은 이 chatlog에 Step별 기록.

## R3 Step 1 완료 (2026-05-19)

### GitHub repos 생성
- `jwj-nick/mathtelling-design-system` — public ✅
- `jwj-nick/mathtelling` — private ✅

### mathtelling-design-system (commit 68f725c)
```
tokens/colors.css      양피지 팔레트 B + 과목 테마(math/science/korean/social/english) + 시대 팔레트(ancient/india/renaissance/modern)
tokens/typography.css  Pretendard + JetBrains Mono + 타입 스케일
tokens/motion.css      3단계(0.3/0.6/1.0s) + ease 토큰
tokens/spacing.css     8px grid + 레이아웃 변수
subjects/math.css      수학 테마 (.math-block, .math-inline)
dist/all.css           단일 @import entry
```

### mathtelling (commit 15cbe9c)
```
content/people/    eratosthenes, al-khwarizmi, descartes, euclid, nightingale (5인)
content/units/01/  meta.json (7유형 정의)
apps/math1/unit-01/index.html  design-system import 기반 단원 허브
.gitignore         ε storage policy (mp3/raw.mp4 제외, final.mp4 제외)
```

### 다음 Step
- apps/math1/unit-01/story.html (에라토스테네스 서사)
- apps/math1/unit-01/concepts.html (소수·소인수분해 인터랙티브)
- apps/math1/unit-01/problems/basic.html (기본 10문제)
- channel/season-1-ancient/unit-01/ 영상 소스 이식
- apps/math1/index.html (중1 수학 홈)

## R3 Step 2 완료 (2026-05-20)

### apps/math1/unit-01 본격 가동
| 파일 | 내용 |
|---|---|
| `story.html` | 5-scene 스크롤 서사 (베타 별명 → 도서관 → 지구 둘레 7.2°·5000 stadia 계산 → 체 시각화 1~30 → 소인수분해 + 작문 미션). IntersectionObserver로 dot 네비 동기화. |
| `concepts.html` | 인터랙티브 3종: ① 1~50 체 (2/3/5/7 단계별 클릭), ② 소인수분해 계산기 (2~1000, 거듭제곱·트리 출력), ③ GCD/LCM 계산기 (두 수의 소인수분해 동시 표시) |
| `problems/basic.html` | T01~T07 전 유형 커버 10문제. 각 문제에 [문제·힌트·정답] 탭. 상단 진행 도트(10)로 점프 + 시도/완료 상태 추적 |
| `problems/types.html` | T01~T07 카드 랜딩. 난이도 표시 핍(L/M/H). 현재 전 카드 Coming Soon (Phase 5-c에서 채움) |

### apps/math1/index.html (중1 수학 홈)
- 13단원 카드 그리드, 각 단원에 인물·시대·시대팔레트 색 띠
- 유클리드: 단원 7·8·9, 아르키메데스: 단원 10·12 (한 인물 다단원 등장 케이스)
- 단원 01만 Ready, 나머지는 Soon 배지

### channel/season-1-ancient/unit-01/
- base `90_video/unit01/` → 텍스트 소스 3종만 복사 (storyboard.md, narration.txt, config.json)
- mp3·mp4·raw는 .gitignore (ε storage policy 적용)
- README.md로 빌드 산출물 위치 가이드

### Commits
- `mathtelling` 34fe3d1 — 9 files / 2240 insertions
- design-system은 v0.1로 push 완료 상태 (변경 없음)

### 다음 Step 후보 (Phase 5-c 진입 또는 Unit 02 착수)
- 유형별 type_01~07_app.html (Phase 5-c) — `se_math_practice` 활용
- Unit 02 (정수·유리수, 브라마굽타) 킥오프 — `se_agent_unit_orchestrator`
- mathtelling-design-system v0.2 — science/korean/social/english 테마 보강
- HTML 앱들 `se_ncc_audit_app` 1-shot 점검

## 변경 이력
- R3 (2026-05-19): 모든 결정 확정. 자율 진행 선언. Step 1 완료.
- R3 Step 2 (2026-05-20): apps/math1/unit-01 풀세트 + math1 홈 + channel 시드 push.
