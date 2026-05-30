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
| 04 | 일차방정식 | 디오판토스 | Mike(남)/Kanna(여) | ✅ done | [unit-04-diophantus/](./unit-04-diophantus/) 8-final.mp4 175.23s |
| 05 | 좌표와 그래프 | 데카르트 | Mina(여)/Kyle(남) | ✅ done | [unit-05-descartes/](./unit-05-descartes/) 8-final.mp4 171.75s |
| 06 | 정비례와 반비례 | 케플러 (보일 조연) | Mike(남)/Mina(여) | ✅ done | [unit-06-kepler/](./unit-06-kepler/) 8-final.mp4 183.82s (딸 약점 y=a/x 정조준) |

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
- 2026-05-30: **unit-04 done** (디오판토스, Mike/Kanna, 176.44s). 묘비 수수께끼=일차방정식 본질 직결. 시즌 3중 callback 절정. (피드백 수정: 클리핑 리미터 + 단원번호 한글)
- 2026-05-30: **unit-05 done** (데카르트, Mina/Kyle, 171.75s). 시즌 피날레 — 5중 callback 좌표평면 만남. 식↔그림(딸 약점) 정조준. **meta 정정**: 05=데카르트(좌표) / 06=케플러(정비례·반비례)로 분리(기존 manifest "05~06 데카르트"는 부정확).
- 2026-05-30: **unit-06 done** (케플러, Mike/Mina, 183.82s). 딸 약점(반비례) 정면 단원 — S4 정비례 직선 vs 반비례 쌍곡선 대비. **시즌1(수·대수·함수) 6편 완결**. 다음=시즌2 기하(u07~12).
