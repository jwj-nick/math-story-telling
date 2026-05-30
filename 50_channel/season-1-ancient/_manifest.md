<!-- _manifest.md / season-1-ancient 영상 양산 manifest (batch run 대상) -->

# Season 1 (Ancient) — 영상 Manifest

> **용도**: `se-video-orchestrator` batch 실행 대상 단원 목록. 한 줄 = 한 단원.
> **상태**: pending(대기) / running(진행) / done(완성) / hold(보류).
> **산출**: `50_channel/season-1-ancient/unit-NN-<인물>/` (8-final.mp4 = 완성).
> **양산 설계**: `11_video_gen_process/00_charter/PRODUCTION_SETUP.md`.

---

## 단원 목록

| unit | 개념 | 인물 | voice (Q/A) | 상태 | 산출 |
|---|---|---|---|---|---|
| 01 | 소인수분해 | 에라토스테네스 | Kanna(여)/Kyle(남) | ✅ done | [unit-01-eratosthenes/](./unit-01-eratosthenes/) 8-final.mp4 140s |
| 02 | 정수와 유리수 | 브라마굽타 | Kyle(남)/Mina(여) | ✅ done | [unit-02-brahmagupta/](./unit-02-brahmagupta/) 8-final.mp4 161.67s |
| 03 | 문자와 식 | 알콰리즈미 | Kanna(여)/Mike(남) | ✅ done | [unit-03-al-khwarizmi/](./unit-03-al-khwarizmi/) 8-final.mp4 174.88s |
| 04 | 일차방정식 | 디오판토스 | 남/여 | ⚪ pending | — |
| 05~06 | 좌표·함수 | 데카르트 | 여/남 | ⚪ pending | — |

## 시즌 2 (기하·통계) — 인물 배정 대기

| unit | 개념 | 인물 후보 | 상태 |
|---|---|---|---|
| 07~ | 기본도형/작도 | 탈레스/유클리드 | ⚪ 인물 선정 필요 (se-people-pick) |
| 09~ | 평면·입체도형 | 아르키메데스 | ⚪ (unit01 카메오→주연 승격 가능) |
| 11~ | 통계 | (근현대) 나이팅게일/가우스 | ⚪ ancient 밖 → 시즌3? |

---

## Batch 실행 규칙

- Q/A 성별 = 단원마다 반대 (시즌 내 균형, voice-pool §3.1)
- 같은 성별 Q↔A 금지 (풀 내 다른 voice)
- 단원 독립 실행 (실패 격리)
- API rate limit 인식: ElevenLabs 5h sliding window, Gemini Tier1 한도
- 완료 시 본 manifest 상태 갱신 (pending→done) + unit 폴더 retro.md

---

## 변경 이력

- 2026-05-29: 신설. unit-01 done (exp-002 졸업). unit-02~06 인물 확정/pending.
- 2026-05-30: **unit-02 done** (브라마굽타, Kyle/Mina, 161.53s). 정식 구조 첫 자율 양산. retro.md 참조.
- 2026-05-30: **unit-03 done** (알콰리즈미, Kanna/Mike, 174.88s). unit-02 학습(네이티브16:9·논리·필러) 반영 첫 단원. 시즌 이어달리기 강화.
