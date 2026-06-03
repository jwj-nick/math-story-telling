<!-- 0603_big_batch_planning.md -->
# v2 진화 계획 — 다인물 + 감싼 설명

> 질문(Nick): "directory new or this repo tagging and update?? 굉장히 큰 작업이므로 brainstorming level 생각정리·계획 필요."
> 참조: 직전 라운드 `0602_skill_cleanup_retro_and_open.md` (스킬 정리 + A2 연결망 + A3 수학지도 완료). 이 문서는 그 다음 "큰 batch"를 NCC 관점 순서로 재정리한 것.
> NCC: 코딩 없음. 현 상태 정밀 확인 → 구조 결정 → 단계 인덱스 → QnA.

---

## Round 0 — NCC 생각정리

### 0. 먼저 확인한 사실 (계획의 토대)

**사실 ①: 2nd 인물이 이미 graph에 정해져 있다.**
`connections.json`의 `persons[]`가 단원마다 **2인**을 명시. 두 번째 인물 = **아직 영상 없는 확장 타깃**.

| 단원 | primary (영상 있음) | 2nd 인물 (미제작) |
|---|---|---|
| u01 소인수분해 | 에라토스테네스 | *(없음 — 추가 결정 필요)* |
| u02 정수·유리수 | 브라마굽타 | 알콰리즈미 |
| u03 문자·식 | 알콰리즈미 | 비에트 |
| u04 일차방정식 | 디오판토스 | 알콰리즈미 |
| u05 좌표·그래프 | 데카르트 | 페르마 |
| u06 정비례·반비례 | 케플러 | 보일 |
| u07 기본도형 | 유클리드 | 탈레스 |
| u08 작도·합동 | 유클리드 | 가우스 |
| u09 다각형 | 피타고라스 | 케플러 |
| u10 원·부채꼴 | 아르키메데스 | 유휘 |
| u11 다면체·회전체 | 플라톤 | 케플러 |
| u12 겉넓이·부피 | 아르키메데스 | 카발리에리 |
| u13 자료·통계 | 나이팅게일 | 플레이페어 |

→ 확장 = **12단원 × 2nd 인물 영상 신규** (8-STEP 파이프라인 재가동 ~12회). u01만 1인.
→ 케플러·알콰리즈미·아르키메데스가 여러 단원에 재등장 = "같은 인물" 연결의 실체.

**사실 ②: `50_channel/season-1-ancient/unit-01` = 옛 v1_5 잔재.**
`final_v1_5.mp4` 등 폐기 포맷. `unit-01-eratosthenes`(8-STEP)와 별개. 정리 때 청소 대상.

현 영상 자산 = `8-final.mp4` **13편** (primary 인물만).

---

### 1. repo 질문에 대한 답 — **새 디렉토리/repo ✗. 같은 repo + git tag + in-place 진화 ✓** *(확정·실행됨)*

근거:
- SSOT가 전부 현 repo에 있다 — `30_content/people`(인물), `concepts`/`units`/`graph`(개념·연결), `10_system`(파이프라인 skill 22 + agent 2), `50_channel`(영상 소스), `40_grades`(앱).
- 분리하면 둘 중 하나: **SSOT 복제(drift)** 또는 **cross-repo 참조**(이미 `external_repos.md`로 겪은 고통). 둘 다 손해.
- 이건 *새 시스템*이 아니라 **같은 시스템의 major 진화(v1 단일인물 → v2 다인물 + 감싼 설명)**.

✅ **실행됨 (2026-06-03):** `git tag v1-season-complete` @ `a8a526b` 생성 + push. 봉인 완료. 이후 main을 v2로 전진.
`(deploy repo jwj-nick.github.io은 별개 유지 — 지금처럼 산출물만 복사.)`

---

### 2. 할 일 순서 — NCC 인덱스 (의존성 따라 재정렬)

> "한번에"의 진짜 의미 = **한 프로젝트로 일관되게**, 동시 실행 아님. 토대를 먼저 깔지 않으면 불일치가 곱해진다.

```
단계 0  봉인          git tag v1-season-complete                    ✅ 완료
단계 1  정본화        인물배정 SSOT 통일 + 디렉토리 2단 재편 + 잔재 청소
단계 2  영상 위생     faststart 재mux 13편 (독립·배경 가능)
단계 3  인물 확장     12단원 2nd 인물 영상 8-STEP ×~12 (시즌급·다회 세션)
단계 4  감싼 설명     unit index = 다인물 도입 + 인물 간 연결 서술
```

의존: **1 → (2 병렬) → 3 → 4.**

| 단계 | 무엇 | 성격 | 비용 | 비고 |
|---|---|---|---|---|
| **1 정본화** | meta.json·app·video·graph의 인물 배정/이름/경로 일치 + `50_channel`을 unit/person 2단 구조로 재편 + `unit-01` v1_5 잔재 삭제 | in-place 데이터/링크/디렉토리 정리 | 낮음 | **모든 것의 토대.** 이번에 처리. |
| **2 영상 위생** | 13편 `8-final.mp4` faststart 재mux (모바일 즉시 재생) | 순수 ffmpeg ops | 낮음·독립 | 언제든·배경. 이번에 처리 가능. |
| **3 인물 확장** | 2nd 인물 12편 8-STEP 신규. 인물 사실 부재분은 `se-people-narrate` 선행 | 콘텐츠 대량 생성 | **매우 높음** | rate-limit으로 **다회 세션 분할 필수**. 별도 큰 단계. |
| **4 감싼 설명** | 배포 `mid1/story/unitNN/index.html` = 인물 목록 + "왜 이 단원을 이 사람들로?" 서술 + 인물 간 연결 | 신규 콘텐츠 타입 | 중 | 단계 3 산출물 위에 얹음. |

→ **권고: 이번 세션은 단계 1(+여유 시 2)까지.** 단계 3·4는 다음 큰 단계로 분리, 착수 시 정교 플랜 별도 작성.

---

### 3. 디렉토리 구조 결정 — "new dir?"의 구체적 답

멀티인물 = **unit이 컨테이너, person이 자식**.

**3-a. 영상 소스 `50_channel/`** (현재 `unit-NN-person` flat = 1인):
```
[현재]  season-1-ancient/unit-06-kepler/
[제안]  season-1-ancient/unit-06/
                          ├─ kepler/   (기존 8-STEP 산출물 이동)
                          └─ boyle/    (확장 신규)
```
※ 이 이동 = 단계 1의 일부(13편 + 링크 갱신). `unit-01`(v1_5 잔재)도 이때 삭제.

**3-b. 배포 `mid1/story/unitNN/`** (현재 단일 영상 플레이어):
```
[제안]  mid1/story/unit06/
        ├─ index.html   ← 인물 2~3인 목록 + 감싼 설명(이 단원을 왜 이 사람들로?)
        ├─ kepler/      → player
        └─ boyle/       → player
```
→ "감싼 설명"(단계 4) = 바로 이 unit-level `index.html`의 도입부. 수학앱의 "▶ 이야기" 버튼은 이 목록 페이지로 연결(자동 다인물 대응).

---

### 4. NCC가 본 위험·기회

- **위험:** 인물 확장 12편은 단발 batch가 아니라 시즌급. rate-limit으로 세션 다회 분할 + manifest 갱신 필요. "한 세션에 끝"은 비현실적.
- **위험:** 2nd 인물 사실 자료(`30_content/people/`) 상당수 부재 → 영상 전 `se-people-narrate` 선행 = 추가 비용.
- **기회:** persons[]가 이미 정해져 범위 명확(추정 불필요). 단계 1만 깔끔하면 단계 3은 기계적 반복.
- **기회:** "감싼 설명"을 unit index로 정의하면 connections.json·수학지도와 자연 연결(같은 데이터 재사용).

---

### 5. Nick에게 QnA (답 주시면 Round 1 확정 → 단계 1 착수)

- **Q1 디렉토리 재편:** `50_channel`·`mid1/story`를 **unit/person 2단 구조**로 — 동의?
- **Q2 이번 범위:** 이번 세션은 **단계 1(정본화)** 중심, 여유 시 **단계 2(재mux)**. 단계 3·4는 별도 큰 단계로 분리 — 동의?
- **Q3 인물 확장 범위(단계 3):** 12단원 2nd 인물 **전부** 영상화? 일부 우선(예: 같은인물 연결 강한 케플러·알콰리즈미부터)? u01 2nd 인물 추가할지·누구?
- **Q4 "감싼 설명" 형태(단계 4):** (NCC안) unit index 도입 서술 = "이 단원을 왜 이 인물들로 보는가 + 인물 간 연결". 이 정의 OK? 더 원하는 형태?

`(Nick) ` 으로 답해 주세요.

---

> 표기 대응(연속성, 0602 기준): 단계 1 ⊇ 구 A1 + 디렉토리재편 · 단계 2 = 구 B4 · 단계 3 = 구 A5 · 단계 4 = 구 A4.

---

## Round 1 — 정밀 조사 결과 + 단계 1·2 상세 체크리스트 (자율진행 착수)

> Nick: "단계 1 완료 후 단계 2까지 자율진행. 필요한 질문만. 단계 2 detail checklist 만들고 시작."

### A. 조사로 드러난 사실 (계획 수정 근거)

1. **"정본 불일치"는 사실상 없다.** 4개 소스 — `meta.json` primary / `connections.json` / `50_channel` 디렉토리명 / 배포 `story/unitNN` 타이틀 — 이 **13단원 전부 primary 인물 일치**. (u06=케플러·u09=피타고라스·u11=플라톤·u12=아르키메데스 모두 meta와 동일.) 이전 "u06·u09·u11·u12 mismatch"는 connections.json 만들기 전의 stale 정보였음. → **단계 1은 "불일치 수정"이 아니라 "SSOT 선언 + 잔재 청소 + 구조 준비"로 축소.**
2. **`meta.json`이 이미 최상위 정본.** persons[]에 primary/secondary 2인 + role·era-palette·signature·story-hook·videos 슬러그까지 보유. connections.json은 여기서 파생. → **meta.json을 인물배정 SSOT로 공식 선언.**
3. **2nd 인물 사실자료 전부 보유** (`30_content/people/` 19개, 2nd 필요분 누락 0). → 단계 3 차단 요인 없음.
4. **배포 영상 13편 모두 faststart 미적용** (moov atom 뒤쪽). → 단계 2 실질 가치 확정(폰 재생 시작 지연 제거). ffmpeg 8.1 가용.
5. **영상 경로 구조**: 배포본은 `mid1/story/_video/unitNN.mp4`(단원 단위, 인물명 없음) + `story/unitNN/index.html`(플레이어). 소스는 `50_channel/SEASON/unit-NN-person/8-final.mp4`. u08·u12는 같은인물 중복 탓 `-construction`·`-volume` 접미사.

### B. 단계 1 자율진행 — 어려움·의문 + NCC 결정

- **의문 1 — 50_channel 2단 rename을 지금?** 2nd 인물 콘텐츠(단계 3)가 아직 없는데 13개 잘 작동하는 디렉토리를 지금 rename하면 = 즉시 이득 0 + git history 노이즈 + manifest/내부참조 수정 리스크.
  → **NCC 결정(자율): 물리적 rename은 단계 3 착수 시점으로 연기.** 단계 1에선 **목표 2단 구조를 convention 문서로 확정**만. (just-in-time, 되돌릴 일 없음)
- **의문 2 — u01 2nd 인물 미정.** meta가 u01만 1인. → 단계 1에서 강제 안 함. 단계 3 플랜에서 Nick에게 질문(아래 Q).
- **어려움 — 없음.** 단계 1은 저위험 문서+삭제 작업.

### C. 단계 1 상세 체크리스트 (lean)

- [ ] **1-1** `30_content/units/_PERSON_SSOT.md` 신설 — "인물배정 정본 = 각 단원 meta.json persons[]" 선언 + 13단원 primary/secondary 표 + 2단 디렉토리 target convention(`50_channel/SEASON/unit-NN/{person-slug}/`, 배포 `story/unitNN/{person}/`) 명문화. rename은 단계 3에서.
- [ ] **1-2** `connections.json` build_connections.py 재생성 → git diff로 meta와 무변화(일치) 검증.
- [ ] **1-3** `50_channel/season-1-ancient/unit-01` (옛 v1_5 잔재) 삭제 — `unit-01-eratosthenes`(8-STEP)와 중복. git rm.
- [ ] **1-4** `_manifest.md` 3개(시즌1/2/3) 점검 — 잔재 `unit-01` 참조 제거, 현 디렉토리와 정합.
- [ ] **1-5** commit (math-story-telling): `docs+chore: 단계1 정본화 — PERSON_SSOT 선언 + v1_5 잔재 삭제 + manifest 정합`.

### D. 단계 2 상세 체크리스트 (faststart 재mux)

- [ ] **2-1** 대상 = 배포 `mid1/story/_video/unit{01..13}.mp4` 13편. (소스 8-final.mp4는 아카이브 성격, 배포본만 폰 영향)
- [ ] **2-2** 각 파일 `ffmpeg -i unitNN.mp4 -c copy -movflags +faststart tmp_unitNN.mp4` (무손실 재컨테이너, 재인코딩 X).
- [ ] **2-3** 검증: tmp의 moov가 mdat 앞 + 재생길이/크기 sane(±수% 이내) → 원본 교체. 실패 시 원본 보존·중단.
- [ ] **2-4** 13편 일괄 처리 후 faststart 재검(moov@ < mdat@).
- [ ] **2-5** jwj-nick.github.io commit + push: `perf(video): 13편 faststart 재mux — 폰 즉시재생`.
- [ ] **2-6** (옵션) 폰 체감 확인은 Nick에게.

### E. Nick 질문 (단계 3 착수 전이라 지금 막힘 없음 — 참고용)

- **Q(단계3):** 12단원 2nd 인물 **전부** vs 일부 우선? u01 2nd 인물 추가할지·누구(예: 유클리드/메르센)? → 단계 2 끝나고 단계 3 플랜 때 확정.

→ **지금부터 단계 1 → 단계 2 자율진행.** 완료 시 이 파일에 결과 append.

### F. 실행 결과 (2026-06-03 자율진행 완료)

**단계 1 정본화 ✅** (commit `aa29b77`, math-story-telling)
- `30_content/units/_PERSON_SSOT.md` 신설 — 정본=meta.json persons[] 선언 + 13단원 표 + v2 2단 디렉토리 convention(rename은 단계 3).
- `connections.json` 재생성 → **무변화**(meta와 정합 확인).
- `50_channel/season-1-ancient/unit-01` (v1_5 잔재, 8-final 없음) 추적·미추적 모두 삭제.
- manifest 3개 정합 확인(잔재 dir 참조 없음).

**단계 2 faststart 재mux ✅** (commit `6ec0cc3`, jwj-nick.github.io, pushed)
- `mid1/story/_video/unit{01..13}.mp4` **13편 전부** `-c copy -movflags +faststart` 재mux.
- 검증: moov@36 (mdat 앞), size 무변화(x1.0, 무손실). 폰 스트리밍 시작 지연 제거.

**다음**: 단계 3(인물 확장 12편) = 별도 큰 단계. 착수 전 위 Q(2nd 인물 범위·u01 인물) 확정 필요.

---

## Round 2 — 단계 3 세부 제안: 한 유닛 detail flow

> Nick: u01 인물추가 불필요 확정. "한 unit 추가 detail flow 구체적으로 + 스킬 잘 사용 + 높은 퀄리티 + 좋은 계획."

### A. 단계 3 전체 범위 (확정)

**12편** (u01 제외, u02~u13 각 secondary 1인). 두 부류로 비용/리스크가 갈린다:

| 부류 | 단원·인물 | 캐릭터 | 비용 |
|---|---|---|---|
| **캐릭터 재사용** (이미 primary로 제작) | u02 알콰리즈미(←u03), u04 알콰리즈미(←u03), u09 케플러(←u06), u11 케플러(←u06) | 기존 reference 재사용 → 일관성 자동 | **낮음** (4편) |
| **신규 캐릭터** | u03 비에트, u05 페르마, u06 보일, u07 탈레스, u08 가우스, u10 유휘, u12 카발리에리, u13 플레이페어 | 신규 reference 생성 | 보통 (8편) |

**서사 연속성 자산**: secondary 다수가 primary 영상에 **이미 카메오**로 등장. 예) u06 케플러 영상 S5 = "보일 = 또 다른 반비례(공기 압축)". → 2nd 영상 = *그 카메오가 자기 이야기를 얻는다*. 같은 개념의 **보완적 facet**(케플러=면적속도 / 보일=압력·부피)으로 딸 약점(반비례)을 2각도 반복 학습.

### B. 한 유닛 detail flow (= 1편 + 통합) — 5 Phase

> 실행 주체 = `se-video-orchestrator` agent(8-STEP 검증됨). 아래는 2nd 인물 특화 wrapper.

**Phase A — 준비 (정본·디렉토리·각도)**
- A1. `30_content/units/NN/meta.json` persons[role=secondary]에서 ref·story-hook·videos-slug·era-palette·signature 추출 (= 서사 시드).
- A2. **디렉토리 2단화**(단계 1 연기분 실행): `git mv unit-NN-<primary> unit-NN/<primary>` → `unit-NN/<secondary>/` 생성. (시즌 폴더 내)
- A3. 인물 사실자료 `30_content/people/<ref>.md` 확인(전부 보유). 재사용 인물이면 primary 디렉토리의 `5-images/` 캐릭터 reference 경로 확보.
- A4. **개념 각도 정의**: 이 단원 핵심개념(`30_content/concepts/NN/`) + primary가 다룬 facet → secondary가 다룰 **보완 facet** 1줄 확정. (모순·중복 방지 기준)

**Phase B — 영상 8-STEP** (se-video-orchestrator, 산출=`unit-NN/<secondary>/`)
- STEP1 서사 `se-people-narrate`: 약속 3겹 + secondary story-hook 각도. primary 영상의 카메오와 callback.
- STEP2 스토리 `se-video-story`: 6장면 ~140s, 한 단어 키워드, 같은 개념 보완.
- STEP3 스토리보드 `se-video-storyboard`: 부록 A/B/C.
- STEP4 나레이션 `se-video-narration`: voice-pool §0. **voice = 해당 단원 primary와 다른 pairing**(두 영상 구분감, §3.1 randomize 활용).
- STEP5 이미지 `se-video-image`: 신규=캐릭터 reference 1장→후속 일관성 / 재사용=기존 reference 전달.
- STEP6 모션 / STEP7 렌더 / STEP8 합성 → `8-final.mp4` + `8-poster.jpg`.

**Phase C — 품질 게이트 (기존 + 신규 2)**
- 기존: 약속 3겹·캐릭터 일관성(멀티모달 Read)·시대 정확성·sync·길이 ~140s·자막 가독성.
- 🆕 **개념 정합 게이트**: secondary 영상이 primary와 같은 개념을 **모순 없이 보완**하는가 (`se-audit-math`/`se-audit-concept` 연계).
- 🆕 **인물 재사용 일관성**: 케플러·알콰리즈미는 primary 얼굴과 동일 디자인인가 (재사용 reference 검증).

**Phase D — 배포 hookup (경량, 단계 4 precursor)**
- D1. `8-final.mp4`→ `mid1/story/_video/unitNN-<secondary>.mp4` (+ poster). **faststart 적용**(단계 2 규칙).
- D2. 기존 `_video/unitNN.mp4` → `unitNN-<primary>.mp4` 리네임. `story/unitNN/index.html`을 **인물 2버튼 선택**으로 경량 갱신(단계 4에서 "감싼 설명"으로 확장).
- D3. 수학앱 버튼은 그대로 `story/unitNN/index.html` → 자동 다인물 대응.

**Phase E — 기록**
- `unit-NN/<secondary>/retro.md`, manifest 상태 갱신, connections.json은 이미 secondary 포함(무변화 확인).

### C. 배치 순서 (rate-limit 인식)

ElevenLabs 5h window + Gemini Tier1 한도 → **세션당 2~3편**. 권장 웨이브:
1. **파일럿 1편** (신규 캐릭터 = 가장 비싼 경로 검증 + 배포 chooser 첫 구현).
2. 재사용 4편(저비용) → 신규 7편. 캐릭터 재사용 인물(알콰리즈미·케플러)을 묶어 reference 일관성 유지.

### D. 파일럿 제안 + 자율진행 방침

- **파일럿 = u06 보일** 추천. 이유: ① 신규 캐릭터(풀 경로 검증) ② 케플러 영상에 이미 카메오 → 서사 연속성 시범 최적 ③ 반비례=딸 핵심 약점, 보완 facet(압력×부피) 가치 큼 ④ 디렉토리 2단화·배포 2버튼 chooser를 u06에서 첫 검증.
- 파일럿 1편 완성→폰 확인 OK면 **나머지 11편 자율 batch**(웨이브 분할).

**→ Nick 확인 1개만**: 파일럿을 **u06 보일**로 바로 착수할지, 다른 단원 선호 있는지. (영상 1편은 재작업 비싸 파일럿 타깃만 확인)
