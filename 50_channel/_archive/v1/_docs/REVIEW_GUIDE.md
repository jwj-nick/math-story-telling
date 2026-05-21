<!-- REVIEW_GUIDE.md — Nick의 13단원 Story 영상 검토 가이드 -->

# 13단원 Story 영상 검토 가이드 (v1)

> NCC가 13단원 Story 영상 자율 제작을 완료했습니다. Nick의 검토를 위한 안내문서.
> 작업 일자: 2026-05-14
> 단일 진실 원본: `90_video/_docs/STORY_VIDEO_GUIDE.md`

---

## 0. 한 줄 요약

- 13개 영상 모두 제작 완료. 평균 길이 **43초**. 평균 파일 크기 **1.4MB**.
- 각 단원 디렉토리에 검토용 `feedback_hitl.md` 파일이 준비됨.
- 시각 수준은 **v1 (텍스트 + SVG 심볼)**. 인물 일러스트는 v2 이후.

---

## 1. 검토 방법 — 빠른 순서

### Step 1: 환경 준비
```bash
cd C:\Kids\30_MiddleSchool\260426_MathTelling_Idea
python 00_project_hub/plan/serve.py
```
브라우저 → `http://localhost:8765/` 에서 mp4 파일 직접 접근 가능.

### Step 2: 13개 영상 차례로 시청
권장 순서 — 단원 번호 순:
```
http://localhost:8765/../90_video/unit01/final.mp4
http://localhost:8765/../90_video/unit02/final.mp4
...
```

또는 파일 탐색기에서 `90_video/unitNN/final.mp4` 직접 더블클릭.

### Step 3: 각 영상마다 feedback_hitl.md 작성
- 위치: `90_video/unitNN/feedback_hitl.md`
- 4개 체크리스트 (기술/내용/학습자 적합성/시각 디자인)
- 자유 피드백 3섹션 (잘된 점/개선/v2 제안)
- 종합 판정 3택 (OK / 부분 수정 / 재제작)

### Step 4: 전체 종합 의견 (이 파일 §7 참조)

---

## 2. 영상 일람표

| Unit | 인물 | 단원 | 길이 | 톤 | 핵심 메타포 |
|---|---|---|---|---|---|
| 01 | 에라토스테네스 | 소인수분해 | 45.07s | night sky + sand | 체로 거르다 |
| 02 | 브라마굽타 | 정수와 유리수 | 42.46s | saffron + indigo | 빚과 재산 |
| 03 | 알콰리즈미 | 문자와 식 | 41.81s | gold + teal | 알지브르 |
| 04 | 디오판토스 | 일차방정식 | 43.20s | parchment + crimson | 미지수의 발견 |
| 05 | 르네 데카르트 | 좌표와 그래프 | 41.69s | snow + ink | 두 숫자로 위치를 |
| 06 | 다시, 데카르트 | 정비례와 반비례 | 45.05s | snow + sky | 정비례와 반비례 |
| 07 | 유클리드 | 기본도형 | 46.82s | marble + olive | 왕도는 없다 |
| 08 | 다시, 유클리드 | 작도와 합동 | 39.43s | marble + terracotta | 같은 모양, 같은 크기 |
| 09 | 카를 가우스 | 다각형 | 44.23s | forest + bronze | 17각형의 비밀 |
| 10 | 아르키메데스 | 원과 부채꼴 | 45.26s | mediterranean + amber | 원주율을 찾아서 |
| 11 | 요하네스 케플러 | 다면체와 회전체 | 47.52s | cosmos + copper | 다섯 정다면체 |
| 12 | 카발리에리 | 입체도형 부피 | 39.17s | tuscan + slate | 카발리에리의 원리 |
| 13 | 플로렌스 나이팅게일 | 자료의 정리와 해석 | 44.11s | rose + slate | 그림이 글을 이겼다 |

---

## 3. 영상의 표준 5장면 구조

모든 영상은 동일한 5장면 골격:

| 장면 | 시간(50초 기준) | 목적 |
|---|---|---|
| S1 | 0~5s | 타이틀 — 인물명·시대·단원 |
| S2 | 5~15s | 인물 등장 — 헤드라인 + 본문 + 심볼 |
| S3 | 15~32s | 결정적 순간 — 키워드 + 메타포 SVG |
| S4 | 32~45s | 수학 연결 — 단원 핵심 개념과 다리 |
| S5 | 45~50s | 마무리 — "이 단원에서, 만나봅시다" |

각 영상은 실제 오디오 길이에 비례하여 자동 스케일링됨 (`SCALE = DUR / 51`).

---

## 4. NCC가 사용한 자료

각 단원별로 다음 source를 참고:

1. **`50_units/NN_단원명/story/unitNN.md`** — 단원별 인물 서사 원문 (5장 narrative)
2. **`50_units/NN_단원명/story.html`** — 인터랙티브 서사 페이지
3. **`20_research/02_R2-people-map.md`** — R2 인물 자료 (5명: 에라토스테네스/알콰리즈미/데카르트/유클리드/나이팅게일)
4. **NCC 일반 수학사 지식** — 가우스, 아르키메데스, 케플러, 카발리에리, 디오판토스, 브라마굽타 등

R2에 없는 8명에 대해서는 NCC의 일반 지식 + 단원 story.md 기반으로 작성. **이 부분은 역사적 사실 검증 필요.**

---

## 5. 시각 자산 — SVG 심볼 14종

`90_video/_assets/symbols/` 디렉토리:

| 심볼 | 사용 단원 |
|---|---|
| `star.svg` | 01, 09, 11 |
| `scroll.svg` | 01, 02, 03, 04, 07, 10 |
| `book.svg` | 03, 05, 06, 09, 13 |
| `sun.svg` | 04, 10 |
| `compass.svg` | 07, 08 |
| `balance.svg` | 03, 04, 06 |
| `coord-axes.svg` | 02, 05, 06 |
| `ruler.svg` | 05, 07, 08, 12 |
| `circle-sector.svg` | 08, 10, 11, 12 |
| `polyhedra.svg` | 09, 11, 12 |
| `infinity.svg` | 02 |
| `lamp.svg` | 13 |
| `sieve-grid.svg` | 01 |
| `coxcomb.svg` | 13 |

색상은 단원 팔레트의 `--accent`로 `currentColor`로 렌더링.

---

## 6. 진화 단계 (참고)

| 버전 | 시각 수준 | 상태 |
|---|---|---|
| **v1** | 텍스트 + SVG 심볼만 | ✅ **현재 (이번 검토 대상)** |
| v2 | 인물 실루엣 + 시대 배경 SVG | 미래 (Unit 02~03부터 시도) |
| v3 | 컬러 일러스트 (AI 생성→SVG 트레이스) | 미래 (Unit 04~06) |
| v4 | 시네마틱 (parallax, particle, sound) | 미래 (Unit 07~13) |

v1 검토 후, **어느 단원이 v2 시각 진화의 첫 후보가 될지** 판단도 함께 부탁드립니다.

---

## 7. Nick 종합 의견 (이 파일에 직접 작성)

### 7.1 13단원 전체 인상
✏️ (영상들을 다 보고 받은 전체적인 인상)

### 7.2 가장 잘 나온 영상 Top 3
1. ✏️
2. ✏️
3. ✏️

### 7.3 가장 손볼 필요 있는 영상 Top 3
1. ✏️
2. ✏️
3. ✏️

### 7.4 시각 진화 (v2) 우선 후보
- 어느 단원이 인물 실루엣/일러스트로 가장 효과적일지?
- ✏️

### 7.5 v1 표준 형식 자체에 대한 의견
- 5장면 구조 적절한가?
- 50초 길이 적절한가?
- 톤·페이스 어떤가?
- ✏️

### 7.6 학습자(딸) 시청 후 반응 (있다면)
- ✏️

### 7.7 다음 단계 결정
- [ ] 13개 모두 OK → story.html에 일괄 임베드
- [ ] 몇 개 수정 후 → 다시 검토
- [ ] v2 진화 착수 (전체 또는 일부 단원)
- [ ] 기타: ✏️

---

## 8. 영상 재제작 시 명령어

```bash
# 단원별 수정 (TTS부터)
python 90_video/_plan/render_all.py 03

# narration 수정 안 했을 때 (TTS 건너뜀)
python 90_video/_plan/render_all.py 03 --skip-tts

# 모든 단원 재렌더
python 90_video/_plan/render_all.py

# config 수정만 했을 때 (index.html만 재빌드)
python 90_video/_plan/build_index.py 03

# feedback 파일 재생성 (config 변경 후 반영)
python 90_video/_plan/build_feedback.py
```

---

## 9. 다음 작업 (Nick 검토 후)

검토 결과에 따라 NCC가 자동 진행할 작업:

1. **OK 받은 단원**: `50_units/NN_단원명/story.html` 상단에 `<video>` 태그 임베드
2. **수정 요청**: feedback_hitl.md의 §5.2, §5.3 항목 반영하여 재작업
3. **v2 진화 결정 시**: 마스터 템플릿에 인물 일러스트 슬롯 추가 → 단원별 일러스트 SVG 작성

각 결정 후 NCC가 chatlog에 라운드 추가하며 진행.

---

## 10. 산출물 위치 정리

```
90_video/
├── _docs/
│   ├── STORY_VIDEO_GUIDE.md      ← 표준 명세 (SSOT)
│   └── REVIEW_GUIDE.md            ← 이 파일
├── _templates/
│   └── story-master.html          ← 마스터 템플릿
├── _assets/
│   ├── palettes.css               ← 13단원 컬러
│   └── symbols/                   ← 14 SVG 심볼
├── _plan/
│   ├── build_index.py             ← 13단원 index.html 빌더
│   ├── render_all.py              ← 13단원 렌더 파이프라인
│   └── build_feedback.py          ← feedback_hitl.md 빌더
└── unit01~13/
    ├── storyboard.md              ← 5장면 설계 문서
    ├── narration.txt              ← 한국어 나레이션
    ├── narration.mp3              ← TTS 출력
    ├── config.json                ← 단원별 데이터
    ├── index.html                 ← GSAP 컴포지션
    ├── raw.mp4                    ← HyperFrames 렌더 출력
    ├── final.mp4                  ← ⭐ 최종 영상 (오디오+영상)
    └── feedback_hitl.md           ← ⭐ Nick 검토 작업판
```

```
.claude/commands/
└── se_story_video.md              ← 신규 스킬 (개별 단원 작업 시)
```

```
00_project_hub/
├── plan/
│   └── story_video_master_plan.md ← 마스터 계획·체크리스트
└── chatlog/
    ├── 260514_story_video_plan.md ← 기획 chatlog (Round 1~4)
    └── 260514_story_video_worklog.md ← 실시간 작업 로그
```
