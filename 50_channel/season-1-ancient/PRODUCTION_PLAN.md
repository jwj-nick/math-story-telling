<!-- PRODUCTION_PLAN.md / Season 1 영상 양산 plan + 단원별 8-STEP checklist + process 안내 -->

# Season 1 (Ancient) — 영상 양산 Plan & Checklist

> **목적**: 단원2~6 영상을 정식 구조(50_channel)에서 자율 양산. unit01(에라토스테네스)에서 검증된 8-STEP 파이프라인 재현.
> **핵심 원칙 (Nick)**: 중간 관여 최소 = **자율**. orchestrator가 STEP 1~8 자동 → 완료 보고.
> **연관 문서**: 프로세스 = §A 아래 / 대상 목록 = [_manifest.md](./_manifest.md) / 설계 = `11_video_gen_process/00_charter/PRODUCTION_SETUP.md`

---

## A. 프로세스 — 어떻게 진행되는가

### A.1 실행 주체
```
Nick: "영상 unit02 만들어"  (한 줄 의뢰)
  │
  ▼
se-video-orchestrator (agent)   ← 10_system/35_agents/se-video-orchestrator.md
  │  STEP 1~8 순차 자동 실행, 각 STEP = 해당 kebab 스킬 호출
  ▼
50_channel/season-1-ancient/unit-NN-<인물>/   (산출)
```

### A.2 8-STEP 파이프라인
| STEP | 스킬 | 입력 | 산출 | 외부도구 |
|---|---|---|---|---|
| 1 서사 | se-people-narrate | 인물 사실(30_content/people) | 1-narrative.md | — |
| 2 스토리 | se-video-story | 서사 | 2-story-seed.md (6장면) | — |
| 3 스토리보드 | se-video-storyboard | 스토리 | 3-storyboard.md (부록 A/B/C) | — |
| 4 나레이션 | se-video-narration | 스토리보드 + voice-pool §0 | 4-narration.{txt,jsonl,mp3} | **ElevenLabs** |
| 5 이미지 | se-video-image | 부록 B | 5-image_prompts.md + 5-images/ | **Nano Banana** |
| 6 모션 | se-video-motion | 음성 길이 + 이미지 | 6-motion-config.json | — |
| 7 렌더 | se-video-render | config + 이미지 | 7-raw.mp4 | **FFmpeg** |
| 8 합성 | se-video-compose | raw + 음성 | 8-final.mp4 + 8-poster.jpg | **FFmpeg** |

### A.3 재현 자산 (자율 실행 핵심)
- **음성**: `se-video-narration/voice-pool.md §0` = config SSOT. 단원별 Q/A 성별 randomize(§3.1). speed 1.15, +dB balance, pause 300/1000ms.
- **이미지**: Nano Banana(gemini-2.5-flash-image, **Tier1 활성**). reference 1장 → 후속 장면 일관성. (se-video-image §IM6 코드)
- **키 추출**: `powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('<VAR>','User')"` (ELEVENLABS_API_KEY, GEMINI_API_KEY)
- **렌더**: FFmpeg 1280x720/25fps, zoompan+drawtext(NotoSerifCJKkr, textfile UTF-8)+fade, scene concat(-c copy).

### A.4 품질 게이트 (각 STEP 자가검증)
약속 3겹 운반 · 캐릭터 일관성(멀티모달 Read) · 시대 정확성(anachronism 0) · 음성-자막-이미지 sync · 길이 ~140s · no-text 이미지 · 수학 개념 정확성.

### A.5 완료 처리
완료 시 → 해당 unit `retro.md` + [_manifest.md](./_manifest.md) 상태 갱신(pending→done) + 본 파일 체크리스트 체크.

---

## B. 단원별 진행 Checklist

> 범례: ☐ 대기 / ◐ 진행 / ☑ 완료

### unit-01 — 소인수분해 / 에라토스테네스 / Kanna(여)·Kyle(남)  ✅ DONE
8-final.mp4 140.27s. (exp-002 졸업, 검증 완료)

### unit-02 — 정수와 유리수 / 브라마굽타 / Kyle(남,Q)·Mina(여,A)  ✅ DONE
8-final.mp4 161.67s. 정식 구조 첫 자율 양산(HITL 0). [retro](./unit-02-brahmagupta/retro.md)
- ☑ STEP1 서사 (약속3 ★★★★★, 알콰리즈미=unit03 예고)
- ☑ STEP2 스토리 (약속2 정서 2장면화 — unit01 약점 개선)
- ☑ STEP3 스토리보드 (수직선 모티프, 수식·한글 전부 drawtext)
- ☑ STEP4 나레이션+음성 (42 turn, 161.67s, 역할기반 settings)
- ☑ STEP5 이미지 (7장, ref→S2·S3 캐릭터 일관, 무텍스트)
- ☑ STEP6 모션 (turn 타임라인 정렬 자막)
- ☑ STEP7 렌더 (render_compile.py 신규, 161.68s)
- ☑ STEP8 합성 (8-final.mp4 + 8-poster.jpg, 프레임 검증)
- ☑ retro.md + manifest 갱신

### unit-03 — 문자와 식 / 알콰리즈미 / Kanna(여,Q)·Mike(남,A)  ✅ DONE
8-final.mp4 174.88s. unit-02 학습(네이티브16:9·직업≠설명언어·bare filler) 반영 첫 단원. [retro](./unit-03-al-khwarizmi/retro.md)
- ☑ STEP1~8 + retro. 균형(저울) + 축 C(문자=발명품) + 시즌 이어달리기(브라마굽타 callback→데카르트 예고)

### unit-04 — 일차방정식 / 디오판토스 / Mike(남,Q)·Kanna(여,A)  ✅ DONE
8-final.mp4 175.23s. 묘비 수수께끼(x=84)=일차방정식 본질 직결. [retro](./unit-04-diophantus/retro.md)
- ☑ STEP1~8 + retro. 수수께끼 + 시즌 3중 callback(에라토·브라마굽타·알콰리즈미) + 페르마 카메오

### unit-05 — 좌표와 그래프 / 데카르트 / Mina(여,Q)·Kyle(남,A)  ✅ DONE
8-final.mp4 171.75s. 시즌 피날레 — 5중 callback. 식↔그림(딸 약점) 정조준. [retro](./unit-05-descartes/retro.md)
- ☑ STEP1~8 + retro. 만남(좌표) + 천장의 파리 + 5인물 좌표평면 만남

### unit-06 — 정비례와 반비례 / 케플러 (보일 조연) / Mike(남,Q)·Mina(여,A)  ✅ DONE
8-final.mp4 183.82s. **딸 약점(반비례) 정면 단원** — S4 정비례 직선 vs 반비례 쌍곡선 대비. [retro](./unit-06-kepler/retro.md)
- ☑ STEP1~8. 조화 + 면적속도(시소) + 아름다운 실패(위로) + 보일. **시즌1(수·대수·함수) 6편 완결**

---

## 🎬 시즌1 완결 (2026-05-30) → 시즌2 기하 (u07~12) 대기
- u07 기본도형/유클리드, u08 작도와합동/유클리드, u09 다각형/피타고라스, u10 원과부채꼴/아르키메데스, u11 다면체회전체/플라톤, u12 겉넓이부피/아르키메데스 (전부 따로 1편, 인물 meta 배정 완료)
- u13 자료정리/나이팅게일 = 시즌3 통계

---

## C. 양산 규칙 (batch)

- Q/A 성별 = 단원마다 반대 (시즌 내 균형, voice-pool §3.1). 같은 성별 Q↔A 금지.
- 단원 독립 실행 (실패 격리 — 한 단원 실패해도 나머지 진행).
- **API rate limit 인식**: ElevenLabs 5h sliding window 잔량 / Gemini Tier1 한도. 단원 착수 전 확인.
- 각 단원 완료마다 산출물 + retro + manifest 갱신 → 다음 단원.

---

## D. 진행 로그

| 날짜 | 단원 | 상태 | 메모 |
|---|---|---|---|
| 2026-05-29 | unit-01 | ✅ done | exp-002 졸업. 검증 파이프라인 기준점. |
| 2026-05-30 | unit-02 | ✅ done | 정식 구조 첫 자율 양산(HITL 0). 161.67s. render_compile.py 도출. |
