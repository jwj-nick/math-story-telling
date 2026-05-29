<!-- MATH1_VIDEO_ROADMAP.md / 중1 전체 영상 production 로드맵 -->

# 중1 전체 영상 Production 로드맵

> **질문**: `C:/Kids/math-story-telling/`에서 중학 1학년 **전체** 영상을 쭉 만들려면 어떻게? — 우리가 셋업한 8 STEP 프로세스를 이용해서.
> **전제**: unit01(에라토스테네스)로 8 STEP 파이프라인이 실제 영상 1편을 끝까지 만들어냄(exp-002). 이 자산 위에서 양산.
> **작성**: 2026-05-29. 상위: [INTEGRATED_PLAN.md](./INTEGRATED_PLAN.md), [PURPOSE.md](./PURPOSE.md), [final-retrospective](../40_experiments/exp-002-build-unit01/final-retrospective.md)

---

## 0. 한 장 요약

```
단원명 + 인물 1줄 의뢰
   │
   ▼  [영상 production orchestrator] — 8 STEP 자동 실행
STEP1 서사 → 2 스토리 → 3 스토리보드 → 4 나레이션(음성)
   → 5 이미지 → 6 모션 → 7 렌더 → 8 합성
   │
   ▼
NN-final.mp4 (단원 1편) + 품질 게이트(audit) 통과
```

8 STEP 스킬은 정형화 완료. **남은 건 "단원마다 반복" + "자율화 수준 올리기".**

---

## 1. 목표·범위·우선순위

- **목표**: 중1 각 단원 = 인물 이야기 영상 1편 (~140초). 우선순위 = **(a) 흥미 유발** (PURPOSE).
- **범위**: 중1 13단원. 단, *전 단원 동시*가 아니라 **인물 서사가 강한 단원부터** 순차.
- **품질 > 진도**: 단원 1개 = 며칠. 흥미·정확성 우선.

---

## 2. 우리가 셋업한 시스템 (재사용 자산)

| 자산 | 위치 | 역할 |
|---|---|---|
| 8 STEP 스킬 | `70_tools/se-{people-narrate,video-*}/` | 단계별 제작 |
| 합성 config SSOT | `voice-pool.md §0` | voice·speed·pause 재현 |
| 도구 가이드 | `tts-tools-guide.md`, `image-tools-guide.md`, `google-cloud-tts-guide.md` | 도구 선택·setup |
| 톤·구조 결정 | `00_charter/TONE_STRUCTURE.md` v3.5 | 2화자 dialog 표준 |
| STEP 심화 가이드 | `20_step_guides/01~08` | 각 단계 깊이·고급 기법 |
| 렌더 파이프라인 | exp-002 FFmpeg 스크립트(zoompan+drawtext+concat) | config→mp4 |
| 인물 풀 | `30_content/people/` + se-people-pick | 단원별 인물 |

---

## 3. 단원·인물 로드맵

### 시즌 1 — Ancient (수·대수·함수, 인물 확정)

| 단원 | 개념 | 인물 | 상태 |
|---|---|---|---|
| 1 | 소인수분해 | 에라토스테네스 | ✅ 영상 완성 (exp-002) |
| 2 | 정수와 유리수 | 브라마굽타 | 다음 (자율 시범 대상) |
| 3 | 문자와 식 | 알콰리즈미 | 대기 |
| 4 | 일차방정식 | 디오판토스 | 대기 |
| 5~6 | 좌표·함수 | 데카르트 | 대기 |

### 시즌 2 — 기하·통계 (단원 7~13, 인물 배정 필요)

| 단원(예) | 개념 | 인물 후보 | 비고 |
|---|---|---|---|
| 7 | 기본도형 | 탈레스 / 유클리드 | 유클리드는 unit01 S5 카메오 — 중복 주의 |
| 8 | 작도·합동 | 유클리드 | 「원론」 작도 |
| 9 | 평면도형(원·다각형) | 아르키메데스 | unit01 카메오 → 주연 승격 가능 |
| 10 | 입체도형 | 아르키메데스 / 플라톤 | 다면체 |
| 11~ | 통계 | (근현대) 나이팅게일 / 가우스 | ancient 밖 → 시즌3? |

→ 7~13 인물 = **se-people-pick으로 단원 착수 시 선정** (exp-001 패턴). 시대 일관성(ancient) vs 적합 인물 trade-off는 단원별 결정.

---

## 4. 단원당 워크플로우 (8 STEP)

unit01에서 검증된 흐름. 단원2부터는 **시범 단계 생략, 바로 실행**.

| STEP | 입력 | 산출물 | 자율화 |
|---|---|---|---|
| 1 서사 | 인물 사실(se-people-pick) | N-narrative.md | NCC 자율 |
| 2 스토리 | 서사 | N-story-seed.md (6장면) | NCC 자율 |
| 3 스토리보드 | 스토리 | N-storyboard.md (부록 A/B/C) | NCC 자율 |
| 4 나레이션 | 스토리보드 + voice-pool §0 | N-narration.mp3 | NCC 자율 (ElevenLabs key) |
| 5 이미지 | 스토리보드 부록 B | N-images/ | **이미지 billing 활성 시 자율** / 미활성 시 web 수동(HITL) |
| 6 모션 | 음성 길이 + 이미지 | N-motion-config.json | NCC 자율 |
| 7 렌더 | config + 이미지 | N-raw.mp4 | NCC 자율 (FFmpeg) |
| 8 합성 | raw + 음성 | N-final.mp4 | NCC 자율 |

**HITL(사람 개입) 지점**: ① 인물 확정(STEP 1 전) ② 이미지 검토/생성(STEP 5, billing 미활성 시) ③ 최종 영상 확인(STEP 8 후). 나머지는 자율.

---

## 5. 자율화 수준 — 3단계

| 수준 | 조건 | 사람 개입 |
|---|---|---|
| **현재 (반자율)** | 이미지 = web 수동 | 인물 확정 + 이미지 생성 + 최종 확인 |
| **목표 (거의 자율)** | 이미지 billing 활성 | 인물 확정 + 최종 확인만 |
| **완전 자율** | + 인물 자동선정 신뢰 | 최종 확인만 (또는 batch 검토) |

→ **즉시 해결 과제 = 이미지 billing 활성화** (Gemini paid 전파/프로젝트 일치). 이것만 되면 STEP 5도 자율 → 단원 전체 NCC 자율.

---

## 6. 영상 production orchestrator (제안)

현재 `se_agent_unit_orchestrator`(4축: 개념·이야기·앱·문제)와 **별개**로, **영상 8 STEP 전용 orchestrator** 신설 제안:

```
se_agent_video_orchestrator
  입력: "unit NN [인물]" 한 줄
  동작: STEP 1~8 순차 자동 실행 (각 STEP = 해당 skill)
        - STEP 5에서 billing 미활성 시 → web 프롬프트 출력 + HITL 대기
        - 각 STEP 후 자가검증, 실패 시 재시도
  출력: NN-final.mp4 + retro
  HITL 게이트: 인물 확정 / 이미지(조건부) / 최종
```

→ 단원2를 이 orchestrator의 **첫 시범**으로 (vertical slice 일반화 검증).

---

## 7. 진행 순서 (권장)

```
① 이미지 billing 활성화 확인 (전제조건)
② 단원2 (브라마굽타/정수·유리수) — 8 STEP 자율 시범
   → 단원1 자산 재사용 검증 + 시간 단축률 측정
   → orchestrator 시드 작성 (reverse-eng)
③ 단원3·4 (알콰리즈미·디오판토스) — orchestrator로 가속
④ 단원5~6 (데카르트) — 함수 (인터랙티브 연계 가능)
⑤ 시즌2 단원7~13 — 인물 배정(se-people-pick) 후 진행
```

단원2가 **분수령**: 시범 없이 자산만으로 영상이 나오는지 = 시스템 완성 신호.

---

## 8. 비용·시간

- **TTS**: ElevenLabs $10 충전 → 1편 ~1,000자 = 충전분으로 수십 편
- **이미지**: Nano Banana $0.039/장 × ~8장 = 단원당 ~$0.3. 시즌 13단원 = ~$4
- **렌더**: FFmpeg 로컬 = $0
- **시간**: 단원1 = 탐색 多(며칠). 단원2~ = 스킬 정형화로 대폭 단축 목표. orchestrator 후 = 단원당 수 시간(이미지 자율 시)

---

## 9. 품질 게이트 (audit)

각 단원 영상 = 다음 자가검증 통과:
- 약속 3겹 운반 (특히 발견 필연성 서사)
- 캐릭터 일관성 (인물 동일 얼굴)
- 시대 정확성 (anachronism 0)
- 음성-자막-이미지 sync
- 길이 ~140s, 자막 가독성
- 수학 개념 정확성 (se_ncc_audit_math 연계 가능)

---

## 10. 확장 (중1 이후)

- 8 STEP 시스템은 **학년·과목 무관** (인물+개념만 교체)
- 중2·중3 수학, 또는 타 과목으로 확장 가능
- voice-pool·렌더 파이프라인·orchestrator = 그대로 재사용
- 시즌 단위(ancient→medieval→modern) 인물 그룹핑

---

## 11. 다음 액션 (요약)

1. **이미지 billing 활성** (Gemini, 전제조건)
2. **단원2 자율 시범** + orchestrator 시드 작성
3. 단원2 결과로 시간 단축률·자율도 측정 → 양산 진입 판단
4. 시즌2 인물 배정 (se-people-pick)
