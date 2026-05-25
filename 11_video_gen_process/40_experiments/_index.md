<!-- 40_experiments/_index.md -->

# Experiments Index

> 본 프로젝트의 실험들. 각 실험 = 가설·setup·결과·회고 1세트.
>
> 단일 진입점: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)
> 결정 누적: INTEGRATED_PLAN §8
> 검증 가설: INTEGRATED_PLAN §10.2

## 완료 (done)

| 실험 | 대상 | 검증 가설 | 결과 |
|---|---|---|---|
| ✅ [`exp-001-selection-unit01/`](./exp-001-selection-unit01/) | `se-people-pick` 시범 (단원 1 소인수분해) | 스킬 자체 patterns 검증 + 옛 1편 비교 검증 | Top 3 (에라토 / 유클리드 / 류후이) 선정. 1순위 = 에라토 유지. SKILL.md 정련 6건 도출. |

## 진행 (running)

| 실험 | 대상 | 검증 가설 | 현재 |
|---|---|---|---|
| 🟢 [`exp-002-build-unit01/`](./exp-002-build-unit01/) | unit 01 vertical slice (서사→스토리→영상 1~6) + 8 스킬 시드 작성 | §10.2 가설 1 (표준 일반화) + 가설 4 (단계 진화) | CHECKLIST.md 작성 완료, step 1 [서사] 진입 대기 |

## 계획 (planned)

다음 단계 [서사] / [스토리] / [영상 1~6] 진행 시 신규 실험 추가.

후보 실험:
- 단계 [선정] 추가 시범 (exp-002 = 단원 2 등) — 스킬 patterns 일반화 검증
- 단계 [서사] 시범 — `se-people-narrate` 정의 후 첫 인물 서사 생성
- 능력 흡수 검증 (INTEGRATED_PLAN §7) — 핵심 시각화 30초 / 음성 도구 비교 / 음향 등

## 아카이브 (archived)

(없음)

## 폴더 구조 (각 실험)

```
exp-NNN-<주제>/
├── output.md           ← 핵심 산출물 (스킬 명세에 따른 양식)
├── log.md              ← 실행 과정 로그 (자료원·검색 쿼리·인용)
└── retrospective.md    ← 스킬 자체 개선점 (스킬 진화 시드)
```
