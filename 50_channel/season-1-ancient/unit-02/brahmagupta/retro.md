<!-- 50_channel/season-1-ancient/unit-02-brahmagupta/retro.md / unit-02 제작 retrospective -->

# unit-02 브라마굽타 — 제작 retrospective

> **단원**: math1 단원 2 — 정수와 유리수 / **인물**: 브라마굽타 / **한 단어**: 발명
> **산출**: `8-final.mp4` 161.67s (1280×720, 25fps, h264+aac)
> **제작**: 2026-05-29~30, NCC 자율 8-STEP (정식 50_channel 구조 첫 양산)
> **음성**: Q=Kyle(남) + A=Mina(여) — unit01(여Q·남A) 반대 (시즌 균형)

---

## 1. 의의 — 정식 구조 첫 자율 양산

exp-002(unit01)는 **샌드박스에서 스킬을 만들며** 영상을 뽑은 reverse-engineering 과정. unit-02는 **졸업된 스킬·config·구조를 그대로 써서** NCC가 1편을 자율 완주한 첫 사례. "중간 관여 없는 양산"의 첫 검증.

- HITL 0회 (인물 확정~최종까지 무인 진행)
- 외부 도구 3종(ElevenLabs/Nano Banana/FFmpeg) 모두 자율 호출 성공
- voice-pool §0 / IM6 코드 / 렌더 패턴 = SSOT 재현 검증 완료

## 2. STEP별 결과

| STEP | 산출 | 비고 |
|---|---|---|
| 1 서사 | 1-narrative.md | 약속3 ★★★★★ (회계→음수 + 그리스 막힘 대비). 알콰리즈미 카메오=unit03 예고 |
| 2 스토리 | 2-story-seed.md | 약속2(정서) **2장면화**(S2 회계출발+S4 한계) — unit01 약점(1장면) 개선 |
| 3 스토리보드 | 3-storyboard.md | 수직선=단원2 핵심 모티프. 수식·한글 전부 drawtext 결정(이미지 무텍스트) |
| 4 나레이션 | 4-narration.mp3 161.67s | 42 turn. 역할 기반 voice_settings(Q=youth, A=explainer). 재인코딩으로 타임라인 정합 |
| 5 이미지 | 5-images/ 7장 | Nano Banana Tier1. ref→S2·S3 캐릭터 일관성 성공. 전부 1024사각·무텍스트 |
| 6 모션 | 6-motion-config.json | turn 타임라인 정렬 자막. 음성 sync 기준 scene 경계 |
| 7 렌더 | 7-raw.mp4 161.68s | render_compile.py 신규(config→클립 자동). 한글·기호 글리프 정상 |
| 8 합성 | 8-final.mp4 161.67s | A/V mux. S2/S5/S6 프레임 검증 통과 |

## 3. unit01 대비 개선·차이

| 항목 | unit01 | unit02 |
|---|---|---|
| 약속2 정서 장면 | 1장면(약점) | **2장면**(개선) |
| 핵심 시각 모티프 | 1~30 격자 | **수직선(0 기준 좌우)** |
| 이미지 내 텍스트 | 일부 SVG 별도 | **전부 drawtext**(무텍스트 이미지 일관) |
| 렌더 | 수동 ffmpeg 명령 | **render_compile.py**(config 컴파일러, SKILL v0.2 실현) |
| 음성 성별 | 여Q·남A | 남Q·여A(시즌 균형) |
| 카메오 | 니코마우스(기록자) | 알콰리즈미(**다음 단원 주연** 예고) |

## 4. 발견한 개선점 (다음 단원/스킬 진화 시드)

| # | 발견 | 제안 |
|---|---|---|
| R1 | render_compile.py = config→mp4 결정론 컴파일러로 검증됨 | se-video-render v0.2 body에 정식 편입. motion 5종 z표현식 테이블 일반화 |
| R2 | synth.py concat `-c copy`가 컨테이너 길이 ~3s 부풀림 | **재인코딩 concat 표준화**(libmp3lame). voice-pool §0.6에 반영 |
| R3 | 역할 기반 voice_settings(성별 무관 Q=youth/A=explainer) | 단원별 성별 randomize 시 settings는 역할 고정 — voice-pool §0.2 명문화 |
| R4 | 이미지 전부 1024사각 → center-crop 16:9(상하 손실) | Nano Banana에 "16:9 wide" 강제 or 구도 시 상하 여백 더 확보 |
| R5 | 남성 youth Q(Kyle, style0.7/speed1.15) 음성 적합성 | Nick 청취 평가 필요 — 부적합 시 남성 youth 전용 voice 발굴 |
| R6 | S4 추상 수직선 이미지 = 숫자 없이 톤만 | 효과적. drawtext 0/수식 오버레이와 잘 결합 |
| **R7** | **나레이션 논리 비약**: "천문 계산→자연수 부족→재산·빚"이 비약(브라마굽타=회계사 암시) | **직업≠설명언어 규칙** → se-people-narrate N5 + se-video-narration 평가기준 반영. 수정=천문학자→"0보다 작은 수를 빚/재산으로 설명" |
| **R8** | **정사각 이미지 center-crop이 인물 머리 잘림** | **네이티브 16:9**(`aspect_ratio="16:9"`)+headroom 지시 → se-video-image SKILL 표준화. unit-02 S2 1344×768 재생성 |
| **R9** | **bare filler "음..."이 남성 Q(Kyle style0.7/speed1.15)에서 뭉개짐** | voice-pool §0.5 회피 규칙. 단독 필러 금지→실질 단어 시작 |

## 6. S2 수정 이력 (2026-05-30, Nick 피드백)

| 이슈 | 수정 |
|---|---|
| 포스터/영상 머리 잘림 | S2 이미지 네이티브 16:9(1344×768) 재생성 + headroom. 크롭손실 21.9%→1.5%. 새 포스터 @21.5s |
| 나레이션 논리 비약 | turn5·7·9 재작성("천문학자→0보다 작은 수→빚/재산 *설명*"). turn만 재합성 |
| 23s "음..." 이상한 소리 | turn6 "음... 모자라다고요?"→"0보다 작은 수요?" (필러 제거) |
| 결과 | 161.67→161.53s. S1·S3~S6 불변(텍스트 동일), 전체 재렌더(타임라인 −0.14 시프트) |

## 5. Nick 검수 포인트

- 🔊 **음성**: 남(Kyle) Q youth 톤 적합성 / 여(Mina) A explainer 자연도 / 의문문·"헐~~" 표현
- 🎬 **자막 sync**: 음수 규칙 4줄(S3) / "음수×음수=양수" / "발명" 타이밍
- 🖼 **이미지**: 브라마굽타 캐릭터 일관성(S2·S3) / 그리스vs인도 split(S5) 대비
- 📐 **수학 정확성**: 음수 연산 규칙 4종, 0÷0 한계 서술 (se_ncc_audit_math 연계 권장)
