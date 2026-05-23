<!-- DECISIONS.md -->

# Decisions — 영상 R&D Sub-Project 누적 결정

> `D-NNN-주제` 형식. 각 결정: **날짜 / 맥락 / 옵션 / 선택 / 이유**.
> 결정 후 GOALS/VISION/principles 에 어떻게 반영됐는지 link.

---

## D-001-sub-project 분리 ✅ 확정

- **날짜**: 2026-05-23
- **맥락**: math-story-telling C R0+R1 진단 후, "영상 잘 만들기 R&D" 가 단순 산출물 폴더가 아니라 단계·실험·표준·평가의 본격 R&D 성격임이 명확해짐. Nick 결정: sub-project 로 분리.
- **옵션**: A 50_channel 안 sub-dir / B 10_system 안 / **C top-level `11_video_gen_process/`** (Nick 선택)
- **선택**: C
- **이유**: top-level `##_` prefix 일관성. `10_system` (메타) 옆에 `11_` (R&D) 자연스러움. 50_channel 은 산출물·소스이므로 R&D 와 책임 분리.
- **반영**: `11_video_gen_process/` 신설. 풀세팅 9 sub-dir. CLAUDE.md + current-plan.md 갱신.

---

## D-002-시작 구조 ✅ 확정

- **날짜**: 2026-05-23
- **옵션**: A 미니멀(3) / B 표준(6) / **C 풀세팅(9)** (Nick 선택)
- **선택**: C
- **이유**: 영상 R&D 본격 진행. 30_pipeline 단계별 + 40_experiments + 60_evaluation + 70_tools + 90_archive 모두 필요. 처음부터 골격을 깔아두면 후에 추가 부담 없음.
- **반영**: 9 sub-dir + 30_pipeline 내 6 stages 생성.

---

## D-003-reference 가져오기 방식 ✅ 확정 (NCC 자율)

- **날짜**: 2026-05-23
- **옵션**: A 핵심 발췌 + 원본 path (NCC 권장) / B 전체 복사 / C 참조 path 만
- **선택**: A
- **이유**: 발췌는 sub-project 자기완결성 + 외부 sync 부담 없음의 균형. 전체 복사는 원본 변경 시 stale 위험. 참조만은 매번 외부 읽기 부담.
- **반영**: `10_reference/_origin.md` 에 원본 path 일괄 명시. 발췌 3개 (01_R0_R1_summary / 02_baseline_unit01 / 03_current_plan_C) 작성.

---

## 결정 대기 항목 (compact 후 처리)

> math-story-telling current-plan §2.C.3 의 D6~D10 과 본 sub-project D-004 이하.

### D-004 (= 상위 D6) — scope ⭐ R6 통합 후 옵션 δ 신설
- α 13편 일괄
- β 시즌1 5편 (평준화)
- γ 시즌1 + 시즌2 일부
- **δ 시즌1 5편 + Cornerstone 차등 (3 Cornerstone + 2 표준) — NCC 권장 (R6 통합 후)**
- 본 sub-project 의 거의 모든 후속 결정이 여기에 의존.
- δ 채택 시 총 시간 ≈ 235h / 16주 (주당 15h) / 2026-09 시즌1 완성.
- 참조: `INTEGRATED_PLAN.md` §3 + §6.

### D-005 — TTS 도구 (= 상위 D1)
- **ElevenLabs 전환 (NCC 권장)** / edge-tts 유지 / Azure
- 5인 voice 매핑 결정도 함께.

### D-006 — AI 이미지 도구 (= 상위 D2)
- ChatGPT (DALL-E 3) / **Midjourney `--cref` (NCC 권장)** / Stable Diffusion 로컬

### D-007 — 이중 트리 이동 시점 (= 상위 D3)
- **지금 (NCC 권장)** / 시즌1 후 / 13편 후

### D-008 — 시드 자동 생성 vs 단원별 (= 상위 D4)
- **시즌1 4단원 시드 + unit-02 파일럿 (NCC 권장)** / 순차

### D-009 — audit skill `se_ncc_audit_video` 신설 (= 상위 D5)
- 지금 / **R2 점검 후 결정 (NCC 권장)** / 미신설

### D-010 — 4편 분할 구조 (= 상위 D7)
- 1단원 1편 (110s) / 다편 분할

### D-011 — 창의 제안 8개 채택 (= 상위 D8)
- "수학자의 편지함" framing / 딸 #001 / Lab Notes / 그림책 자매 / 시그니처 사물 / Phase 0 캡슐 / Audio Story / 문해력 노트
- 기본값: 시즌1 끝나고 회고 시 검토 — 지금은 0개 채택.

### D-012 — 옛 70_meta 처리 (= 상위 D9)
- A 그대로 / **B `90_archive/` 이동 + 신규 작성 (NCC 권장)** / C "outdated" 헤더

### D-013 — 진화 메커니즘 본격화 시점 (= 상위 D10)
- **지금 (NCC 권장)** / 시즌1 후

---

## R6 통합 후 신설 결정 항목 (D-014 ~ D-019)

> reference: `../10_reference/04_R6_quality_essence.md` + `INTEGRATED_PLAN.md` §3 + §4.

### D-014 — Cornerstone 단원 확정 (δ 선택 시)
- 시즌1 5편 중 어느 3편을 Cornerstone 으로?
- 후보:
  - **A**: 01 에라토스테네스 + 04 디오판토스 + 05 데카르트 (NCC 추천 — 방정식은 중1 시험 최대 비중)
  - B: 01 + 03 알콰리즈미 + 05 (R6 §1 원안 후보 1)
  - C: 01 + 03 + 04 + 05 (4편 Cornerstone — 시간 부담 커짐)
- 영향: D-005·D-015·D-016·D-017·D-018 의 적용 범위 결정.
- 결정 주체: Nick (NCC 자율 X).

### D-015 — Set-piece [A] 30s 채택 시점
- Cornerstone 단원에 동적 다이어그램 (JSXGraph/D3.js) S4 30초 set-piece 추가.
- 옵션: **Cornerstone 01 즉시 (NCC 권장)** / Cornerstone 1편 시범 후 / 시즌1 끝나고
- 영향: `30_pipeline/4_motion/` + `40_experiments/exp-006-set-piece-01-eratosthenes/`
- 에라토스테네스 set-piece 후보: 막대기+그림자 각도 + 시에네 우물 + 지구 곡률 + 7.2°=1/50바퀴 + 둘레 마니멍.

### D-016 — BGM + SFX [C] 채택 시점
- BGM (era-팔레트별 ambient) + SFX (결정적 순간 sting).
- 옵션:
  - A: 전 단원 BGM ambient + Cornerstone 만 sting (NCC 권장)
  - B: Cornerstone 만 BGM+sting
  - C: 시즌1 끝나고
- 영향: `30_pipeline/4_motion/` + `40_experiments/exp-007-bgm-sfx/` + 라이선스 (CC0 source 결정).

### D-017 — 일러스트 [D] 외주 채택
- Cornerstone 3단원 인물 한 장 외주 (단가 5~10만원/장 추정).
- 옵션:
  - A: Cornerstone 3편 모두 (15~30만원)
  - B: Cornerstone 01 (에라토스테네스) 만 우선 시범
  - C: AI 만 (외주 X) — D-006 MJ --cref 로 대체
- NCC 권장: **B 시범 → 만족 시 A 확장**.
- 영향: `30_pipeline/3_image/` + Nick_TODO 신규 + 시즌1 일정 +1주.

### D-018 — Sub-3min [E] 보조 영상 도입
- 본 영상 (115s) 외 30~60s "한 컷 영상". 인스타·쇼츠·"다시 보고 싶은 부분" 추출.
- 옵션:
  - A: 전 단원 1개 (단원 결론 30s) + Cornerstone 추가 1~2개 (NCC 권장)
  - B: Cornerstone 만
  - C: 시즌1 끝나고 검토
- 영향: `30_pipeline/` 신 stage 또는 산출물 종류 +1. STORY_VIDEO_v1_6 시드 §3.2 추가.

### D-019 — Polish Loop + manifesto 운영 (R6 P1·P6)
- 매 단원 완성 직후 retrospective + "양보하지 않은 것" 1줄 manifesto.
- 옵션:
  - A: 단원 빌드 직후 매번 (NCC 권장) — `60_evaluation/retrospectives/` 양식에 "Polish 1건" + "양보하지 않은 것" 필드
  - B: 시즌 단위
  - C: 미운영 (안 함)
- 신설 파일: `../../10_system/50_insights/manifesto.md` (math-story-telling 외부 SSOT). 누적 1줄씩.
- 영향: 진화 메커니즘의 4단계 사이클 (Build→Retrospect→Distill→Apply) 의 Retrospect 단계 강화.

---

## 변경 이력

- 2026-05-23: D-001/002/003 확정. D-004 이하 placeholder.
- 2026-05-23 (compact 후, R6 통합): D-004 옵션 δ 추가. D-014~D-019 신설. NCC 추천 정렬.
