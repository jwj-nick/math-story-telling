<!-- story_video_master_plan.md -->

# Story 영상 13단원 자율 제작 — 마스터 체크리스트

> Nick 자율진행 위임 (2026-05-14). NCC가 순서 결정·실행. Nick은 최종 리뷰 가이드로 확인.
> 진행 상황은 `00_project_hub/chatlog/260514_story_video_worklog.md`에 실시간 기록.

---

## 작업 전체 흐름

```
Phase 0 (인프라)
├─ Step 1 ✅ STORY_VIDEO_GUIDE.md
├─ Step 2 □ palettes.css
├─ Step 3 □ story-master.html
├─ Step 4 □ symbols/ SVG
└─ Step 5 □ se_story_video.md (skill)
                ↓
Phase 1~3 (단원별 콘텐츠) — 13단원 × 3단계
                ↓
Phase 4 (렌더) — 13단원 일괄
                ↓
Phase 5 (리뷰 가이드 작성)
```

---

## Phase 0 — 인프라 셋업

- [x] **Step 1** `90_video/_docs/STORY_VIDEO_GUIDE.md` (완료 2026-05-14)
- [x] **Step 2** `90_video/_assets/palettes.css` — 13단원 시대 분위기 컬러 토큰
- [x] **Step 3** `90_video/_templates/story-master.html` — 5장면 마스터 템플릿 (GSAP 타임라인 골격)
- [x] **Step 4** `90_video/_assets/symbols/*.svg` — 공통 심볼 5~7개 (star, scroll, book, sun, geometry-shapes, etc)
- [x] **Step 5** `.claude/commands/se_story_video.md` — 신규 스킬 정의

---

## Phase 1~3 — 단원별 콘텐츠 (13단원 × 각 3개 산출물)

각 단원당 3개 파일:
- `storyboard.md` — 5장면 설계 (인물 메타포, 시각 요소, 시간 배분)
- `narration.txt` — 한국어 240~270자
- `index.html` — story-master 적용, 단원 데이터 주입

| Unit | 인물 | 단원 | storyboard | narration | index.html |
|------|------|------|------------|-----------|------------|
| 01 | 에라토스테네스 | 소인수분해 | ✅ | ✅ | ✅ |
| 02 | 브라마굽타 | 정수와유리수 | ✅ | ✅ | ✅ |
| 03 | 알콰리즈미 | 문자와식 | ✅ | ✅ | ✅ |
| 04 | 디오판토스 | 일차방정식 | ✅ | ✅ | ✅ |
| 05 | 데카르트 | 좌표와그래프 | ✅ | ✅ | ✅ |
| 06 | 데카르트(2) | 정비례와반비례 | ✅ | ✅ | ✅ |
| 07 | 유클리드 | 기본도형 | ✅ | ✅ | ✅ |
| 08 | 모르 | 작도와합동 | ✅ | ✅ | ✅ |
| 09 | 탈레스 | 다각형 | ✅ | ✅ | ✅ |
| 10 | 아르키메데스 | 원과부채꼴 | ✅ | ✅ | ✅ |
| 11 | 케플러 | 다면체와회전체 | ✅ | ✅ | ✅ |
| 12 | 카발리에리 | 입체도형 겉넓이·부피 | ✅ | ✅ | ✅ |
| 13 | 나이팅게일 | 자료의 정리와 해석 | ✅ | ✅ | ✅ |

**진행 순서**: Unit 01부터 차례대로. 각 단원당 3개 산출물 연속 작성 후 다음 단원으로.

---

## Phase 4 — 일괄 렌더 (13단원)

각 단원당:
- [x] 4-1 edge-tts → `narration.mp3`
- [x] 4-2 ffprobe로 AUDIO_DURATION 측정 → index.html data-duration 보정
- [x] 4-3 hyperframes render → `raw.mp4`
- [x] 4-4 ffmpeg 합성 → `final.mp4`

13단원 모두 완료까지 wall-clock ~30~60분 예상 (단원당 2~5분).

---

## Phase 5 — Nick 리뷰 가이드

- [x] `90_video/_docs/REVIEW_GUIDE.md` 작성
  - 13개 final.mp4 재생 순서
  - 각 영상 체크포인트
  - 발견된 이슈 기록 템플릿
  - 다음 진화(v2) 의사결정 항목

---

## NCC 자율 진행 원칙

1. **순서**: 위 체크리스트 위→아래
2. **속도**: 각 산출물 자체의 품질 우선. 서두르지 않음.
3. **워크로그**: 주요 산출물 완료마다 worklog 파일에 기록
4. **블로커 발생**: chatlog에 명시, 가능한 우회하여 진행
5. **렌더 실패**: 해당 단원 표시 후 다음 단원 진행. 마지막에 일괄 재시도
6. **NCC 판단**: 인물 매핑 등 사소한 결정은 `20_research/02_R2-people-map.md` 참조 후 자체 판단

---

## 작업 산출물 위치

```
00_project_hub/
├── chatlog/260514_story_video_plan.md     ← 기획 chatlog (Round 1~4 완료)
├── chatlog/260514_story_video_worklog.md  ← 실시간 작업 로그
└── plan/story_video_master_plan.md         ← 이 파일

90_video/
├── _docs/STORY_VIDEO_GUIDE.md             ← Step 1 완료
├── _docs/REVIEW_GUIDE.md                  ← Phase 5에서 작성
├── _templates/story-master.html           ← Step 3
├── _assets/palettes.css                   ← Step 2
├── _assets/symbols/                       ← Step 4
└── unit01~13/                              ← Phase 1~4 산출물
    ├── storyboard.md
    ├── narration.txt
    ├── narration.mp3
    ├── index.html
    ├── raw.mp4
    └── final.mp4

.claude/commands/se_story_video.md         ← Step 5
```
