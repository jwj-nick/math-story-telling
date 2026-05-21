<!-- 260514_story_video_worklog.md -->

# Story 영상 13단원 자율 제작 — 작업 로그

> NCC 자율 진행. 주요 산출물 완료 시점마다 entry 추가.
> 마스터 계획: `00_project_hub/plan/story_video_master_plan.md`
> 기획 chatlog: `00_project_hub/chatlog/260514_story_video_plan.md`

---

## 2026-05-14 시작

**위임 받음**: Nick이 13단원 전체 자율 진행 위임. NCC가 순서·세부 결정.
**전체 흐름**: Phase 0 (Step 2~5) → Phase 1~3 (13단원) → Phase 4 (렌더) → Phase 5 (리뷰 가이드)

---

## Entry 1 — 셋업 (시작 시각)

- ✅ TaskCreate 7개 등록
- ✅ master_plan.md 작성
- ✅ worklog 파일 생성
- ▶ 다음: Step 2 (palettes.css)

---

## Entry 2 — Phase 0 완료

- ✅ Step 2 `90_video/_assets/palettes.css` (13단원 × 5토큰 + 공통 :root)
- ✅ Step 3 `90_video/_templates/story-master.html` (5장면, GSAP 타임라인 골격, 15개 placeholder)
- ✅ Step 4 SVG 심볼 14개 + README
  - star, scroll, book, sun, compass, balance, coord-axes, ruler
  - circle-sector, polyhedra, infinity, lamp, sieve-grid, coxcomb
- ✅ Step 5 `.claude/commands/se_story_video.md` (8 STAGE 파이프라인)
- ✅ 시스템에 `/se_story_video` 등록 확인됨

**인물 매핑 확정 (13단원)**

| Unit | 인물 | 단원 |
|---|---|---|
| 01 | 에라토스테네스 | 소인수분해 |
| 02 | 브라마굽타 | 정수와 유리수 |
| 03 | 알콰리즈미 | 문자와 식 |
| 04 | 디오판토스 | 일차방정식 |
| 05 | 데카르트 | 좌표와 그래프 |
| 06 | 데카르트(2) | 정비례와 반비례 |
| 07 | 유클리드 | 기본도형 |
| 08 | 유클리드(2) | 작도와 합동 |
| 09 | 가우스 | 다각형 |
| 10 | 아르키메데스 | 원과 부채꼴 |
| 11 | 케플러 | 다면체와 회전체 |
| 12 | 카발리에리 | 입체도형 겉넓이·부피 |
| 13 | 나이팅게일 | 자료의 정리와 해석 |

- ▶ 다음: Phase 1~3 Unit 01부터 순차 진행

---

## Entry 3 — Unit 01 파이프라인 end-to-end 검증 ✅

**산출물**:
- ✅ `90_video/unit01/storyboard.md` (5장면 설계, 총 250자)
- ✅ `90_video/unit01/narration.txt`
- ✅ `90_video/unit01/config.json`
- ✅ `90_video/unit01/index.html` (template + data 주입)
- ✅ `90_video/unit01/narration.mp3` (edge-tts, **45.07초**)
- ✅ `90_video/unit01/raw.mp4` (HyperFrames, 1104 frames @ 24fps = 46s)
- ✅ `90_video/unit01/final.mp4` (FFmpeg, **45.07s, 1.25MB**)

**부가 산출물**:
- ✅ `90_video/_plan/build_index.py` — 13단원 자동 빌드 스크립트
- ✅ 마스터 템플릿에 비례 스케일링 추가 (`SCALE = DUR / 51`)
  - 실제 audio 길이 ± 5초 차이를 자동 보정
- ✅ doc comment 제거 (placeholder 치환 시 깔끔)

**확인된 사실**:
- TTS 속도: 한국어 250자 → 약 45초 (예상 5자/초 → 실제 5.5자/초)
- 가이드 §2 정책 (45~55초) 안에 들어옴
- 파이프라인 end-to-end 작동

**남은 작업**: Unit 02~13 (12개)
- 각 단원 storyboard + narration + config.json + index.html
- 일괄 렌더

▶ 다음: Unit 02~13 콘텐츠 작성

---

## Entry 4 — Phase 1~3 13단원 콘텐츠 일괄 작성 ✅

**13단원 각각 3개 산출물**:
- `storyboard.md` (5장면 메타)
- `narration.txt` (한국어 240~270자)
- `config.json` (템플릿 주입용 데이터)

**그 후**:
- `build_index.py all` → 13개 index.html 일괄 생성

---

## Entry 5 — Phase 4 13단원 일괄 렌더 ✅

**렌더 결과** (모든 단원 성공):

| Unit | 인물 | 영상 길이 | 파일 크기 |
|---|---|---|---|
| 01 | 에라토스테네스 | 45.07s | 1252 KB |
| 02 | 브라마굽타 | 42.46s | 1541 KB |
| 03 | 알콰리즈미 | 41.81s | 1494 KB |
| 04 | 디오판토스 | 43.20s | 1348 KB |
| 05 | 데카르트 | 41.69s | 1378 KB |
| 06 | 데카르트(2) | 45.05s | 1388 KB |
| 07 | 유클리드 | 46.82s | 1355 KB |
| 08 | 유클리드(2) | 39.43s | 1454 KB |
| 09 | 가우스 | 44.23s | 1470 KB |
| 10 | 아르키메데스 | 45.26s | 1667 KB |
| 11 | 케플러 | 47.52s | 1605 KB |
| 12 | 카발리에리 | 39.17s | 1566 KB |
| 13 | 나이팅게일 | 44.11s | 1431 KB |

**총 13개 final.mp4 · 합계 약 19MB · 평균 43초**

**파이프라인 이슈/수정**:
- 첫 시도 시 hyperframes가 `subprocess` PATH에서 안 보임 → `shell=True` 사용으로 해결
- `render_all.py`에 duration 자동 갱신 + index.html 재빌드 로직 통합

---

## Entry 6 — Phase 5 & Nick 요청 처리 ✅

**산출물**:
- ✅ `90_video/_docs/REVIEW_GUIDE.md` (10개 섹션, 마스터 검토 가이드)
- ✅ 13개 `90_video/unitNN/feedback_hitl.md` (Nick 작업판)
- ✅ `90_video/_plan/build_feedback.py` (피드백 파일 일괄 생성기)

**feedback_hitl.md 구조** (각 단원):
1. 영상 정보 (인물·시대·길이·글자수)
2. NCC 제작 방식 (사용 자료, 파이프라인, SVG 심볼, 5장면 시간)
3. 나레이션 전문
4. 검토 체크리스트 (4분류 × 5항목 = 20체크)
5. Nick 자유 피드백 3섹션 + 종합 판정 3택
6. 수정 작업 시 명령어 참고

---

## 자율 진행 완료 — 최종 산출물 요약

| 영역 | 개수 | 위치 |
|---|---|---|
| 인프라 문서 | 2 | `90_video/_docs/` (GUIDE, REVIEW_GUIDE) |
| 마스터 템플릿 | 1 | `90_video/_templates/story-master.html` |
| 컬러 토큰 | 13단원 | `90_video/_assets/palettes.css` |
| SVG 심볼 | 14 | `90_video/_assets/symbols/` |
| 빌더 스크립트 | 3 | `90_video/_plan/` (build_index, render_all, build_feedback) |
| 단원별 영상 산출물 | 13 × 7 = 91 | `90_video/unit01~13/` |
| 신규 스킬 | 1 | `.claude/commands/se_story_video.md` |

**Nick 다음 단계**: `REVIEW_GUIDE.md` §1의 검토 순서 따라 진행.

