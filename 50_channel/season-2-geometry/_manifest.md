<!-- _manifest.md / season-2-geometry 영상 양산 manifest -->

# Season 2 (Geometry, 기하) — 영상 Manifest

> **용도**: `se-video-orchestrator` batch 대상. math1 단원 7~12 (기하).
> **산출**: `50_channel/season-2-geometry/unit-NN-<인물>/` (8-final.mp4 = 완성).
> **시즌 명명**: 테마 기반(수·대수·함수=season-1 / 기하=season-2 / 통계=season-3). 2026-05-30 결정.
> **인물 배정**: `30_content/units/NN/meta.json` 확정.

---

## 단원 목록

| unit | 개념 | 주연(조연) | voice (Q/A) | 상태 | 산출 |
|---|---|---|---|---|---|
| 07 | 기본도형 | 유클리드 (탈레스) | Mina(여)/Mike(남) | ✅ done | [unit-07-euclid/](./unit-07-euclid/) 8-final.mp4 201s (약속) |
| 08 | 작도와 합동 | 유클리드 (가우스) | Kyle(남)/Kanna(여) | ✅ done | [unit-08-euclid-construction/](./unit-08-euclid-construction/) 8-final.mp4 146s (규칙) |
| 09 | 다각형 | 피타고라스 (케플러) | Kanna(여)/Mike(남) | ✅ done | [unit-09-pythagoras/](./unit-09-pythagoras/) 8-final.mp4 180s (수) |
| 10 | 원과 부채꼴 | 아르키메데스 (류후이) | 남/여 | ⚪ pending | — (unit01 카메오→주연) |
| 11 | 다면체와 회전체 | 플라톤 (케플러) | 여/남 | ⚪ pending | — |
| 12 | 겉넓이와 부피 | 아르키메데스 (카발리에리) | 남/여 | ⚪ pending | — (아르키메데스 재등장) |

> u13 자료의 정리와 해석 / 나이팅게일(플레이페어) = **Season 3 (통계)** — 별도 시즌.

---

## Batch 규칙 (시즌1과 동일)
- Q/A 성별 = 단원마다 반대 (시즌 내 균형). 같은 성별 Q↔A 금지.
- 단원 독립 실행(실패 격리). API rate limit 인식.
- 같은 인물 2단원(유클리드 07·08, 아르키메데스 10·12) = **각각 따로 1편**, 서사·개념 차버화(Nick 결정 2026-05-30).
- 학습 누적 자동 적용: 네이티브 16:9·리미터·letter한글음차·그래프정확성·자막x위치·필러회피·길이관리(≤180s 목표).

## 변경 이력
- 2026-05-31: 신설. unit-07 done (유클리드, 약속). u08~12 pending.
- 2026-05-31: **unit-08 done** (유클리드 작도, 규칙, Kyle/Kanna, 146s). 길이 관리 성공(u07 201→146, R24). 가우스 정17각형.
- 2026-05-31: **unit-09 done** (피타고라스, 수, Kanna/Mike, 180s). 외각합 360°·펜타그램·무리수·히파소스. 케플러 테셀레이션. 다음=u10 아르키메데스(원과 부채꼴).
