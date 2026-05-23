<!-- GOALS.md -->

# Goals — 영상 R&D Sub-Project

> ⚠️ **placeholder**. compact 후 작성.

## 채워야 할 항목 (작성 시 구조)

### 단기 (1~3주)
- 진화 메커니즘 본격화 (insights 미반영 2건 → STORY_VIDEO_v1_5 반영)
- skill (`se_story_video_v1_5`) Phase E (자동 retrospective) 추가
- STORY_VIDEO_v1_5.md → v1.6 갱신 (캐릭터 시트 분리 / length dry run / 인물 voice 매핑 / 디렉토리)
- 19인 캐릭터 시트 (또는 5인 시즌1 한정)
- unit-02 (브라마굽타) 파일럿 빌드 — 신 표준 검증

### 중기 (1~3개월)
- 시즌1 5편 완성 (unit-01 existing + 02·03·04·05)
- 표준 v1.6 → v1.7 (시즌1 회고 후)
- audit skill (`se_ncc_audit_video`) 신설 여부 결정
- ElevenLabs · MJ 도입 후 비용·품질 회고

### 장기 (3개월+)
- 시즌2~3 (단원 06~13) 진입 여부 결정
- 창의 제안 8개 중 채택 항목 (편지함 framing 등) 통합
- 이북 트랙 (`00_Publishing/`?) 호환성 1항 (PDF/벡터 인쇄 해상도) 반영

---

## 측정 지표 (정량)

| 지표 | 목표 | 측정 방법 |
|---|---|---|
| 영상 1편 작업 시간 | ?시간 | (compact 후 결정) |
| 품질 게이트 통과율 | ?% | STORY_VIDEO_v1_5 §5 rules audit |
| Nick 외부 의존 시간 | ?시간/편 (이미지·TTS 생성) | Nick_TODO 진행 로그 |
| narration 재합성 횟수 | <2회/편 | length dry run 효과 검증 |
| 인물 캐릭터 일관성 | 정성 + 정량 (Nick 만족도) | MJ `--cref` 검증 |

---

## scope 결정 (D-004 / 상위 D6 — math-story-telling current-plan §2.C.3)
- α 13편 일괄
- β 시즌1 5편 (평준화)
- γ 시즌1 + 시즌2 일부
- **δ 시즌1 5편 + Cornerstone 차등 (3+2) — NCC 권장 (R6 통합 후)**

→ compact 후 첫 결정 항목. 본 sub-project 의 거의 모든 후속 결정 의존.

### δ 시간 모델 (R6 §5)

| 작업 종류 | 시즌1 5편 | 시간 |
|---|---|---|
| 표준 v1.6 (2단원) | 30h | |
| Cornerstone (3단원) | 180h | |
| Polish + 진화 메커니즘 | 25h | |
| **총 시즌1** | | **~235h** |

→ **주당 15h × 16주 = 4개월 (2026-05~09) 권장**. Nick 본업·5 study 고려 시 현실적.

---

## 우선순위 후보 (R6 통합 후 — δ 옵션 기준)

1. 🔴 **NCC 자율 sprint 0** (5건, R1.9 + R6 §5)
   - insights 2건 → STORY_VIDEO_v1_5 반영
   - skill 점검
   - STORY_VIDEO_v1_5 4 항목 갱신 (= v1.6 시드)
   - 옛 70_meta audit (D-012 후 처리)
   - ⭐ R6 7 원칙 운영화 시드 (`20_principles/POLISH_LOOP_OPERATING.md`)
2. 🔴 STORY_VIDEO_v1_5.md → v1.6 확정 (4 항목 + R6 §3 quality 절 추가)
3. 🟡 시즌1 5인 voice 매핑 (D-005 ElevenLabs 결정 후)
4. 🟡 unit-02 표준 파일럿 (v1.6 검증)
5. 🟡 ⭐ Cornerstone 01 재빌드 — Set-piece [A] + BGM [C] 적용 (D-015 + D-016)
6. 🟢 Cornerstone 04 or 03 빌드 (D-014 후)
7. 🟢 Cornerstone 05 빌드
8. 🟢 시즌1 종합 회고 + 시즌2 진입 결정 (D-011 창의 제안 검토 포함)

## 마일스톤 (INTEGRATED_PLAN §6.3)

- **M1 (~2026-06-15, 3주)**: NCC 자율 5건 + v1.6 + unit-02 파일럿
- **M2 (~2026-07-15, 7주)**: Cornerstone 01 재빌드 + D-014 확정
- **M3 (~2026-08-15, 12주)**: Cornerstone 04 or 03 + 표준 unit-04 빌드
- **M4 (~2026-09-15, 16주)**: Cornerstone 05 + 시즌1 종합 회고 + 시즌2 진입 결정

---

## 변경 이력

- 2026-05-23: placeholder 신설.
- 2026-05-23 (compact 후): R6 통합 — D-004 옵션 δ 추가, δ 시간 모델 (235h/4개월) 추가, 우선순위 8 후보 + 마일스톤 M1~M4 (16주).
