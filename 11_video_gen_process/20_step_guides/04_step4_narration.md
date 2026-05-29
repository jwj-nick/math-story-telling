<!-- 20_step_guides/04_step4_narration.md / STEP 4 [영상 2] 나레이션·음성 심화 가이드 -->

# STEP 4 — 나레이션(음성) 심화 가이드

> **STEP**: 4 / 8 · **단계명**: 나레이션(음성) · **skill**: `se-video-narration` (v0.5.2)
> **실제 산출물**: [`../40_experiments/exp-002-build-unit01/4-narration.{jsonl,txt,xml,mp3}`](../40_experiments/exp-002-build-unit01/) + `voice-pool.md §0`
> **상위 frame**: [`../00_charter/PURPOSE.md`](../00_charter/PURPOSE.md) · [`../00_charter/TONE_STRUCTURE.md`](../00_charter/TONE_STRUCTURE.md) · [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)
> **합성 config SSOT**: [`../70_tools/se-video-narration/voice-pool.md`](../70_tools/se-video-narration/voice-pool.md) §0

---

## 1. Step 개요

STEP 4는 STEP 3 스토리보드의 **나레이션 시드(부록 A의 Q/A turn 초안)** 를 받아, ①실제 발화용 텍스트로 정련하고 ②2화자 dialog의 voice를 매핑하고 ③TTS 엔진으로 음성을 합성해 ④길이를 검증하는 단계다. 입력은 "글로 적힌 대화의 뼈대", 출력은 "귀로 들리는 110~180초의 완성된 대화 음성"이다. 이 사이의 변환 — *글자를 소리로, 의도를 억양으로* — 이 STEP 4의 본질이다.

**4축 기여**: 주축은 **B(흥미)**. 인물 이야기를 *친근한 두 목소리의 대화*로 만들어 몰입과 정서적 연결을 만든다. 부차적으로 **A(개념 이해)** — A 화자가 소수의 체·소인수분해를 자연스러운 설명으로 풀어내며, **C(언어)** — "2 곱하기 3", "배수를 지운다" 같은 수학 표현을 음성 리듬에 실어 전달한다.

**8단계 파이프라인 위치**:

```
STEP 3 스토리보드 ──(나레이션 시드, 부록 A)──▶ [STEP 4 나레이션·음성] ──┬──▶ STEP 7 렌더 (음성 길이 = 장면 타이밍 기준)
                                                                       └──▶ STEP 8 합성 (음성 트랙 = 영상의 척추)
```

선행 STEP 3은 "무엇을 말할지"의 시드를, 후행 STEP 7/8은 "음성의 실제 길이"를 타이밍 기준으로 받는다. **음성이 먼저 확정되고 영상이 거기에 맞춰진다** (audio-first). 그래서 STEP 4의 mp3 길이(`4-narration.mp3` = 140s)가 사실상 전체 영상의 골격을 결정한다.

**본질적 난제 2가지**:

1. **"외국인 한국말"의 함정** — 한국어 TTS는 자연도가 천차만별이다. 영문 voice를 multilingual model로 돌리면 "미국 사람이 한국말 하는" 어색한 톤이 나온다(실제로 Jessica/Will 폐기 원인). voice·도구·파라미터를 **실제 합성해서 귀로 들어봐야** 판정 가능하고, 1-shot으로 안 정해진다.
2. **두 목소리의 "함께 발견하는 대화" 만들기** — 단일 voice 낭독이 아니라, Q(청소년 존댓말)와 A(대학원생 친절 반말)가 호기심과 설명을 주고받는 *살아있는 대화*여야 한다. 단조로운 평문 나열은 실패다. 어투 분화·의문/감탄/평문 다양화·호흡(pause)·음량 balance를 모두 제어해야 한다.

---

## 2. Workflow (절차)

skill `se-video-narration`의 동작은 **NR1~NR7** 7단계로 정의된다. 입력 align → 정련 → 마크업 → 합성 → 검증 → 출력의 흐름이다.

| 액션 | 이름 | 핵심 동작 | 의사결정 포인트 |
|---|---|---|---|
| **NR1** | 입력 align | 스토리보드 부록 A(Q/A turn 분리·자수) + TONE_STRUCTURE v3 + TTS 도구(ElevenLabs 1차) 확인 | 입력 누락 시 보강 |
| **NR2** | (필요 시) Q&A 보강 | Q/A 성별 결정(단원1 = Q여+A남) + voice 선택 + speed/pitch 차등 | **voice 매핑** = voice-pool §0 확정 조합으로 시작 |
| **NR3** | Dialog 정련 | 시드를 *실제 발화용*으로: Q 존댓말 / A 친절 반말 / 의문·감탄·평문 다양화 / text 정련 규칙 적용 | 연속 평문 ≤ 2 turn 검사 |
| **NR4** | SSML 마크업 | `4-narration.xml` multi-voice 풀스펙 (Azure/Google reference) | (ElevenLabs는 SSML 미사용 → reference 보관) |
| **NR5** | jsonl 분할 | `4-narration.jsonl` turn별 분할 + `4-narration.txt` 평문(marker 포함) | turn id / scene 필드 부여 |
| **NR6** | TTS 합성 | voice-pool §0.6 6-step: 키 추출 → turn 합성(speed 포함) → post-proc(A volume) → concat(silence) → 길이 측정 | **도구 분기** (ElevenLabs / Google / edge-tts) |
| **NR7** | 자체 평가 + 출력 | TONE_STRUCTURE 부합 체크리스트 + 4개 파일 출력 | 길이 ±10% 외 → 재정련 / 톤 청취 후 voice 변경 |

**NR6 합성의 실제 동작 순서** (voice-pool §0.6, ElevenLabs 1차):

```
1. key 추출   PowerShell User scope → ELEVENLABS_API_KEY (NCC Bash가 registry 직접 못 읽음)
2. turn 합성  jsonl loop → voice_id 직접(조회 X) → eleven_multilingual_v2
              Q turn = voice_settings에 speed=1.15 포함, retry 4회(ConnectionReset 10054 대비)
3. post-proc  Q 없음(speed 합성 반영) / A volume(Mike +8dB, Kyle +3.8dB) / 공통 재인코딩 libmp3lame 128k 44100 mono
4. concat.txt Q/A 사이 300ms + scene 경계 1000ms silence 삽입
5. ffmpeg concat → 4-narration.mp3
6. ffprobe 길이 측정 (목표 150~180s)
```

**의사결정 분기 (도구 선택)**: 1차 = ElevenLabs(credit 있을 때, 표현력 최강) → credit 소진/무료 전환 시 2차 = Google Cloud TTS(SSML 풀 + 무료 100만 chars/월) → 둘 다 막히면 3차 = edge-tts(완전 무료, 청소년 voice 부재). 도구가 바뀌어도 jsonl 형식은 동일 — voice 필드와 합성 함수만 교체한다.

---

## 3. Skill / Agent / Tools / Context

### 3.1 Skill

| 항목 | 값 |
|---|---|
| skill | `se-video-narration` |
| version | **0.5.2** (status: 시드 — 시범 후 retrospective로 정련 중) |
| SSOT | `70_tools/se-video-narration/SKILL.md` |
| allowed-tools | Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch |
| 핵심 동작 | NR1~NR7 (위 §2) |

### 3.2 외부 도구 (TTS 엔진) + 선택 근거

| 우선 | 도구 | 선택 근거 | 본 프로젝트 상태 |
|---|---|---|---|
| 🥇 1차 | **ElevenLabs API** | 감정·표현력 최강 + `speed` 파라미터 직접 + Nick $10 credits 충전 | **현행 확정** (Kanna/Kyle, Mina/Mike) |
| 🥈 2차 | **Google Cloud TTS** | ko-KR-Neural2 자연 + SSML 풀 + 무료 100만 chars/월(1,800편/월) | 백업 (credit 소진 시) |
| 🥉 3차 | edge-tts | 완전 무료 | fallback (청소년 voice 부재로 v2 폐기) |

부수 도구: **ffmpeg**(post-processing volume·재인코딩·silence·concat), **ffprobe**(길이 측정), **PowerShell**(User scope 환경 변수 키 추출).

### 3.3 참조 Context (SSOT)

| 파일 | 역할 |
|---|---|
| **`voice-pool.md §0`** ⭐ | **합성 config SSOT** — voice_id / voice_settings / speed / post-processing dB / pause / text 규칙. 다른 세션·다른 NCC도 §0만 읽으면 동일 음성 재현 |
| `TONE_STRUCTURE.md` | 톤·구조 결정 (2화자 / 존댓말·반말 / 의문·감탄·평문 / pause 표 §8 / 길이 §9) |
| `3-storyboard.md` 부록 A | 나레이션 시드 입력 (Q/A turn + 자수) |
| `tts-tools-guide.md` | 도구 비교 + setup 요약 |
| `elevenlabs-detailed-guide.md` / `google-cloud-tts-guide.md` | 도구별 step-by-step |

### 3.4 Agent 활용

본 STEP은 단독 skill 호출. 단원 전체 파이프라인에서는 `se_agent_unit_orchestrator`가 STEP 3 산출물을 받아 본 skill을 chaining한다. 다만 음성 품질 판정(청취)은 **Nick HITL**이 필수라 완전 자율 X (§4 참조).

---

## 4. User Input (Nick 입력)

| 입력 | 시점 | 형식 | 필수/선택 |
|---|---|---|---|
| TTS 도구 setup (API key) | STEP 4 진입 전 (최초 1회) | PowerShell User scope 환경 변수 (`ELEVENLABS_API_KEY`) | **필수** (도구 사용의 전제) |
| voice 추가·청취 평가 | 새 voice 진입 시 | Voice Library 청취 → voice_id 전달 + 🟢/🟡/❌ 판정 | **필수 (HITL)** |
| 합성 mp3 청취 + 승인 | NR6 후 | 귀로 듣고 톤·음량·속도 판정 | **필수 (HITL)** |
| Q/A 성별·voice 조합 지정 | NR2 | "이번 단원 Q=여, Kanna" 등 | 선택 (기본 = voice-pool §3.1 randomize) |

**HITL(사람 개입) 지점이 STEP 4의 특징**이다. 텍스트 단계(STEP 1~3)는 NCC 자율도가 높지만, **음성은 "들어봐야 안다"** — 자동 메트릭(길이)만으로는 자연도·정서를 판정 불가. 그래서:

- voice 진입: Nick이 ElevenLabs Voice Library에서 직접 청취 → "Add to My Voices" → NCC에 voice_id 전달 (key에 `user_read` 권한 없어 NCC가 `/v1/voices` 조회 불가, voice_id 직접 받아야 함).
- 합성 후: Nick 청취 → 음량/속도/톤 피드백 → NCC가 post-processing(dB)·speed 미세조정.

키 값 자체는 chat에 절대 출력 X (보안). NCC는 `[ -n "$ELEVENLABS_API_KEY" ]`로 *존재만* 확인한다.

---

## 5. Step Output (산출물)

### 5.1 산출 파일 (위치 규약: `40_experiments/exp-NNN/`)

| 파일 | 내용 | git |
|---|---|---|
| `4-narration.jsonl` | turn별 분할 (speaker / scene / voice / voice_settings / text) — **합성 입력** | 추적 |
| `4-narration.txt` | 평문 + `[Q-S1]` 마커 (참조·검수용) | 추적 |
| `4-narration.xml` | SSML 풀스펙 (Azure/Google reference, ElevenLabs 미사용) | 추적 |
| `4-narration.mp3` | 합성 결과 concat (단원1 확정 = Kanna+Kyle 140s) | **gitignore** |
| `turns/turn-NNN.mp3` | turn별 중간 산출 | **gitignore** |

### 5.2 다음 step 연결

- **STEP 7 렌더**: `4-narration.mp3`의 ffprobe 길이가 zoompan 클립 타이밍의 기준. scene 경계(1000ms silence)가 이미지 전환점과 정렬.
- **STEP 8 합성**: 음성 트랙이 최종 영상의 척추. 자막(vtt) 동기화도 음성 turn 경계 기준.

### 5.3 품질 검증 기준

**자동 (ffprobe/ffmpeg)**:
- 길이 150~180s 범위 (TONE_STRUCTURE §9). 실측: Kanna+Kyle 140s / Mina+Mike 152s.
- 음량 balance: `ffmpeg volumedetect`로 화자별 mean_volume 측정 → 낮은 쪽 boost.

**Nick (청취 HITL)**:
- 한국어 자연도 (외국인 한국말 X)
- Q/A 어투 분화 명확 (존댓말 vs 친절 반말)
- 의문문 끝 올림·감탄 활기·여운 자연
- 두 화자 음량 균형

**NR7 체크리스트 (TONE_STRUCTURE 부합)**: 2화자 turn 분리 / A "나도 찾아봤는데" ≥1 / Q 자연반응 ≥3종 / A 되묻기 ≥1 / S1 시대사실 ≥3 / 마무리 Q시도+A확인 / turn 자수 10~30 / 길이 범위.

---

## 6. 현재 구현 (exp-002 실제 사례)

### 6.1 unit01(에라토스테네스)에서 실제로 한 것

**38 turn dialog** (`4-narration.jsonl`, S1~S6 6장면). Q(청소년 여, 존댓말) + A(대학원생 남, 친절 반말). TONE_STRUCTURE의 모든 규칙을 실제로 구현:

- **어투 분화**: Q = `"들어봤어요?"`, `"무슨 뜻이에요?"`, `"혼자서요?"` (존댓말). A = `"응! 나도 찾아봤는데..."`, `"잘 봐."`, `"맞아!"` (친절 반말).
- **의문·감탄·평문 다양화**: Q turn은 감탄+의문 위주(`"어!"`, `"와!"`, `"오!"`, `"헐~~"`), A turn은 평문+되묻기 섞기. S6의 A 되묻기 = `"한 단어로 표현하면 뭘까?"`.
- **S1 풍부 배경 (≥3 사실)**: turn 2 = `"이집트의 큰 항구 도시 / 세상 모든 지식이 모인 도서관 / 두루마리만 50만 권!"`.
- **마무리 (Q시도+A확인)**: turn 34 Q `"음... 도서관에 책을 분류하고, 수도, 분류한 사람이니까..."` → turn 35~37 A `"잘 봤어! ... 한 단어로, '정리'!"`.

### 6.2 text 정련 규칙 적용 (voice-pool §0.5 — 음성 표현 ↑)

| 규칙 | 실제 적용 turn |
|---|---|
| 의문문 끝 올림 `?` | `"들어봤어요?"`, `"왜요?"` |
| 중요 단어 앞뒤 **쉼표** `,`로 호흡 | turn 3 `"와! 그럼, 그 도서관은, 누가 운영했어요?"` / turn 9 `"다재다능 한 거, 아니에요?"` |
| 감탄 **`~~`** elongation | turn 24 `"헐~~ 그 유명한, 아르키메데스요?"` |
| 여운 **`...`** | turn 29 `"오..."` / turn 34 `"음... ~니까..."` |

### 6.3 실제 겪은 시행착오 — 도구·voice는 반복 탐색 (retro 인용)

retro-4-narration.md §2: *"도구·voice가 1-shot으로 안 정해짐. 실제 청취 → 폐기 → 교체 반복이 본질."*

**도구 변천 (4단계)**:

```
edge-tts (한국어 3 voice, 청소년 X)
  → ElevenLabs Free (library voice = HTTP 402 차단)
  → Google Cloud TTS (결제 SMS 막힘 → 보류)
  → ElevenLabs API $10 credits 충전 (확정)
```

**voice 폐기 연쇄 (5단계)**:

```
Jessica/Will (미국식 한국말)
  → Mono Beige (음량 과대 + 의문문 표현 부족)
  → Annie/Onyu (발화 느림, atempo 해도 느림)
  → Yura (실제 청취 후 별로)
  → Mina/Kanna 확정
```

> jsonl 파일에는 변천의 *화석*이 남아있다: `4-narration.jsonl`의 voice 필드는 아직 `"Annie"`, `"Mike - Friendly, Balanced and Clear"` (구버전) — 합성 시점에 voice-pool §0의 확정 voice_id로 덮어쓴다.

### 6.4 핵심 기술 발견 (시스템 자산) — voice-pool §0 / retro §3

| 발견 | 내용 |
|---|---|
| **`speed` 파라미터** | `voice_settings.speed` (범위 0.7~1.2, eleven_multilingual_v2 포함 전 모델). **합성 시점 직접 가속 → ffmpeg atempo 후처리 폐기**(더 자연). Q 청소년 = **`speed: 1.15`**, A 남자 = 1.0 |
| **음량 balance** | voice마다 default 음량 다름. `volumedetect` 측정 → 낮은 쪽 boost. **Mike +8dB / Kyle +3.8dB** (Q는 보정 없음) |
| **pause 설계** | **Q/A turn 사이 300ms + scene 경계 1000ms** silence concat → 호흡 + 길이 보강. scene 변화 지점 5곳 |
| **key 권한** | ElevenLabs key에 `user_read` 없음 → `/v1/voices`·`/v1/user/subscription` = HTTP 401. **voice_id를 voice-pool §0.2 표에서 직접 사용** (조회 X) |
| **연결 안정** | ConnectionReset(10054) 빈발 → **retry 4회** (timeout 60, sleep 2×attempt) |
| **노이즈 대응** | 특정 turn 합성 아티팩트 → **그 turn만 재합성 + concat** (전체 재합성 X — credit 절약) |

### 6.5 확정 config (voice-pool §0.2)

| 항목 | Q = Kanna | A = Kyle | (대안) Q=Mina | (대안) A=Mike |
|---|---|---|---|---|
| voice_id | `5I7B1di44aCL15NkP0jn` | `RU7aSi6lT4uQBXMLgDxK` | `aiUUgjHa4mpHf6UenZuf` | `mgugV8tLa3KQE4mfYTw5` |
| stability | 0.2 | 0.5 | 0.2 | 0.5 |
| similarity_boost | 0.75 | 0.75 | 0.75 | 0.75 |
| style | 0.7 | 0.2 | 0.7 | 0.2 |
| speed | **1.15** | 1.0 | **1.15** | 1.0 |
| post-proc | 없음 | **+3.8dB** | 없음 | **+8dB** |

확정 mp3: `4-narration-kanna-kyle.mp3` (140s, 단원1 채택) / `4-narration-mina-mike.mp3` (152s, 대안).

### 6.6 강점과 한계

**강점**: ①config SSOT(voice-pool §0)로 cross-session 재현 보장. ②speed 파라미터로 atempo 후처리 제거(자연도 ↑). ③turn별 재합성으로 credit 절약. ④2화자 어투 분화가 텍스트~음성 일관.

**한계**: ①voice 진입이 Nick 청취 의존(완전 자율 X). ②ElevenLabs SSML 미지원 → 세밀한 억양 제어 불가(`?`·`,`·`~~`·`...` 텍스트 trick에 의존). ③turn별 합성+concat이라 turn 경계 prosody 단절(문맥 억양 X). ④BGM·효과음 없음(STEP 8 미구현). ⑤credit 종량(무한 free X).

---

## 7. 개선 방향 탐색 / 아이디어

### 7.1 실현 가능한 단기 개선

| 한계 | 단기 개선 |
|---|---|
| voice 진입 청취 의존 | **voice 평가 자동화 보조** — 신규 voice로 5턴 샘플 합성 → 음량(volumedetect)·길이(ffprobe)·발화속도(chars/sec) 자동 측정 표를 Nick에게 1장으로 제시. 정량 후보 추리고 청취는 최종 2~3개만 |
| turn 경계 prosody 단절 | **문맥 chunk 합성** — turn 단위가 아니라 *연속 같은 화자의 인접 turn을 1회 합성*으로 묶기. 단 scene 경계는 분리 유지. 같은 화자 연속 turn(예 turn 10·11, 36·37)에서 자연 억양 연결 |
| 길이 미세 조정 | **speed 자동 보정 루프** — ffprobe 길이가 150~180s 밖이면 speed를 0.05 step으로 자동 조정 후 재합성 (현재 수동) |
| credit 소진 위험 | **사용량 사전 추정** — jsonl chars 합계 × 도구별 단가로 합성 전 예상 비용 출력. ElevenLabs ~1,000 chars/편 = $10의 4% |

### 7.2 자동화·효율·품질

- **합성 캐시**: text+voice_settings 해시 → mp3 캐싱. 동일 turn 재합성 시 API 호출 skip (text 안 바뀐 turn은 재사용 — A turn은 speed 1.0 고정이라 특히 효과).
- **golden sample 회귀 테스트**: 확정 config로 합성한 mp3의 길이·음량 지문(fingerprint)을 baseline 저장. 도구·라이브러리 업데이트 후 동일 입력 → 지문 변화 감지(품질 드리프트 조기 발견).
- **2도구 A/B 자동 합성**: 같은 jsonl을 ElevenLabs + Google 양쪽으로 합성 → 나란히 비교 페이지 생성. 도구 비교가 시스템 자산(tts-tools-guide §7).

### 7.3 실패·리스크 요소와 대응

| 리스크 | 대응 |
|---|---|
| ConnectionReset(10054) | retry 4회 (이미 적용) + turn별 idempotent 합성 (실패 turn만 재시도) |
| 도구 차단/가격 변동 | jsonl 추상화 유지 → 도구 교체 시 voice 필드+합성 함수만 교체 (3차 fallback 항상 확보) |
| 발음 오류 (류후이→ryu hwi 등 외래어) | 텍스트 한국어 발음 변환 ("리우 후이"). ElevenLabs SSML phoneme 미지원이라 텍스트 trick만 |
| Nick 부재 시 진행 정체 | 확정 config로 *자동 합성 후 검토 대기*. 청취 없이는 "잠정 산출"로만 표시(승인 게이트 분리) |

---

## 8. 고급 Workflow (상상력·창의력)

> 현재 "turn별 합성 + concat + 텍스트 trick 억양"을 뛰어넘는 미래형 설계.

### 8.1 감정·억양·호흡의 정교한 제어 (라디오드라마 기법 차용)

라디오드라마는 *목소리만으로 장면을 그린다*. 그 연출 도구를 jsonl 스키마에 1급 시민으로 승격한다:

```jsonc
{
  "id": 24, "speaker": "Q", "scene": "S4",
  "text": "헐~~ 그 유명한, 아르키메데스요?",
  "emotion": "surprise",          // 감정 토큰 (차세대 TTS 입력)
  "intensity": 0.8,               // 감정 강도
  "intonation": "rising-sharp",   // 억양 곡선
  "breath_before": 250,           // 발화 전 들숨(ms) — 놀람 직전 멈칫
  "emphasis": ["유명한", "아르키메데스"],  // 단어 단위 강조
  "tempo_curve": "slow-fast"      // turn 내 속도 변화 (놀람 → 급가속)
}
```

- **호흡(breath) 트랙 분리**: 발화 전후 들숨/날숨을 silence가 아니라 *실제 호흡음 레이어*로. 결정적 순간(turn 24 아르키메데스 등장) 직전 0.25s 멈칫 = 청자의 기대를 만든다.
- **억양 곡선(intonation contour)**: 의문문도 다 같지 않다. 진짜 궁금한 의문(rising), 확인 의문("진짜네요!"의 깨달음, rising-then-fall), 되묻기("뭘까?"의 유도, gentle-rising)를 구분 마크업 → SSML `<prosody contour>` 또는 차세대 TTS 감정 토큰으로 전달.
- **tempo_curve**: turn 내부 속도 변화. 놀람("헐~~")은 느리게 시작해 급가속, 깨달음("아 진짜네요!")은 점점 빨라지는 흥분 곡선.

### 8.2 멀티보이스 자동 캐스팅

현재는 단원당 Q/A 2명 수동 매핑. 미래형:

- **캐스팅 디렉터 에이전트**: 인물 프로필(에라토스테네스=박학·온화, 아르키메데스=천재·열정)을 받아 voice 라이브러리에서 *성격 매칭 점수*로 자동 후보 추천. 시대(고대 그리스)·연령·성별·톤을 voice 메타데이터와 매칭.
- **인물별 voice 고정 (시리즈 정체성)**: 시즌 전체에서 에라토스테네스는 항상 같은 목소리. 카메오(아르키메데스·유클리드·류후이)도 *짧지만 고유한 voice*로 — 류후이는 약간 다른 톤(중국 위나라)으로 거리감 표현 (voice-pool §3.2 향후 검토 항목의 확장).
- **군중·내레이터 레이어**: 도서관(50만 권) 묘사 시 군중 웅성임 ambience, 결정적 전환에 별도 narrator voice 1줄 — 다성(polyphony) 캐스팅.

### 8.3 음성-자막-영상 프레임 단위 동기화

오디오북·더빙의 **forced alignment** 기법:

- **단어 단위 timestamp 추출**: 합성 mp3를 Whisper/aeneas forced-alignment로 단어별 시작/끝 시각 추출. → ①자막(vtt)이 단어 단위로 highlight (노래방식 karaoke 자막, 중1 학습자 가독성 ↑) ②STEP 7 모션이 "2 곱하기 3" 발화 *순간*에 숫자 애니메이션 동기.
- **음성 주도 키프레임**: "배수를 차례로 지우는 거지" 발화의 *지운다* 음절에 정확히 체(sieve) 격자에서 숫자 사라지는 모션. 음성이 영상 키프레임을 driving — STEP 4 출력에 word-level timing json 추가.
- **frame-accurate scene cut**: scene 경계 1000ms silence를 영상 dissolve 구간과 프레임 단위 정렬. 음성 무음 = 화면 전환의 호흡.

### 8.4 SSML 고급 활용 (Google/Azure 백업 도구의 잠재력)

ElevenLabs는 SSML 미지원이지만 Google Cloud TTS는 풀 지원. 백업 도구를 *정밀 제어가 필요한 turn에만* 선택적으로 쓰는 하이브리드:

```xml
<speak xml:lang="ko-KR">
  <prosody rate="95%" pitch="+2st">잘 봐.</prosody>
  <break time="400ms"/>
  6은 <emphasis level="strong">2 곱하기 3</emphasis>,
  8은 <say-as interpret-as="cardinal">2</say-as> 곱하기
  <say-as interpret-as="cardinal">4</say-as>.
  <break time="300ms"/>
  이렇게 나뉘는 수가 있지<prosody pitch="+15%">?</prosody>
</speak>
```

- `<say-as>`로 숫자 발음 명확화, `<phoneme>`로 외래어(류후이) 발음 교정, `<emphasis>`로 핵심 수학 표현 강조, `<prosody contour>`로 의문문 끝 올림 정밀 제어. **턴별로 도구를 다르게** — 감정 풍부 turn = ElevenLabs, 정밀 발음 turn = Google SSML.

### 8.5 음악·효과음 레이어링 (STEP 8 선반영 설계)

영화 사운드 디자인의 stem 분리:

| 레이어 | 내용 | 타이밍 |
|---|---|---|
| **dialog** | Q/A 음성 (STEP 4 현행) | turn 기준 |
| **ambience** | 항구·도서관·필사실 환경음 | scene 기준 ducking(대사 시 -12dB) |
| **score** | 시대 분위기 BGM (고대 지중해) | scene 전환에 motif 변화 |
| **SFX** | 두루마리 펼침, 체에서 숫자 떨어짐, 편지 봉인 | 키워드 발화 순간 |

핵심은 **sidechain ducking** — 대사가 나오는 동안 BGM/ambience를 자동으로 낮춰 명료도 보장. STEP 4 출력에 turn별 timing이 있으면 STEP 8에서 자동 ducking envelope 생성 가능.

### 8.6 차세대 TTS (감정 토큰·대화형 모델)

- **대화형(conversational) TTS 모델**: turn 단위 단독 합성이 아니라, *대화 전체 문맥*을 입력받아 화자 간 자연스러운 turn-taking·간투사·맞장구를 모델이 직접 생성 (ElevenLabs Conversational, OpenAI realtime 류). turn 경계 prosody 단절 문제 근본 해결.
- **감정 토큰 직접 입력**: `[surprised]`, `[curious]`, `[warm]` 같은 인라인 토큰을 지원하는 차세대 모델 → §8.1 emotion 스키마를 그대로 전달.
- **voice-to-voice 더빙**: Nick(또는 성우)이 *연기한 톤*을 voice conversion으로 확정 voice에 입히기. 텍스트→음성이 아니라 *연기→음성* — 정서의 정밀도가 한 차원 다름.

---

## 9. 고급 Contents 생성 방법 (품질 도약)

> STEP 4에서만 가능한 차별화 — "글이 아니라 소리로 가르친다".

### 9.1 콘텐츠 질을 올리는 구체 기법

**(a) 발화 설계 = 학습 설계.** 수학 표현을 음성 리듬에 싣는다.
- "6은 2 곱하기 3" 처럼 *곱셈을 소리로 듣게* — `2 곱하기 3` 사이 미세 pause로 인수의 경계를 귀로 분리. 중1 학습자가 소인수분해 구조를 청각적으로 체득.
- 핵심 개념어("소수의 체", "정리")는 앞에 짧은 pause + 강조 → 청자가 "지금 중요한 말"임을 안다.

**(b) "함께 발견하는" 대화 리듬.** Q의 호기심이 A의 설명을 끌어낸다 — 강의 톤(일방향) 회피.
- Q의 깨달음 turn("아 진짜네요!", "어! 신기해요.")이 *학습자 자신의 깨달음을 대리*한다. 청자가 Q에 감정이입 → A의 설명이 "나에게 하는 친절한 설명"으로 들림.
- A의 되묻기("한 단어로 표현하면 뭘까?")가 청자에게 *생각할 틈*(scene pause 1000ms)을 준다.

**(c) 정서 곡선 설계.** 110~180초에 감정 아크를 넣는다.
- S1 호기심 → S3 발견의 흥분("신기해요!") → S4 거장의 등장(놀람 "헐~~") → S5 인류 보편성의 경외("오...") → S6 따뜻한 정리. 음량·속도·pause를 이 곡선에 맞춰 변주.

### 9.2 학습 효과·몰입·정서 연결 강화

| 기법 | 효과 |
|---|---|
| Q에 학습자 또래(청소년 여) voice | 자기동일시 → "나도 저렇게 궁금해해도 돼" |
| A의 친절 반말 + "나도 찾아봤는데" | 권위 없는 학습 친구 → 수학 공포 완화 (LEARNER_PROFILE의 "수학 중하위·내성적" 배려) |
| 여운 `...` (turn 29 "오...") | 침묵이 만드는 경외 — 빈칸을 청자가 채움 (CLAUDE.md "빈칸을 남겨라" 원칙의 음성판) |
| scene 경계 1000ms | 정보 과부하 방지 — 호흡으로 단원 구조 청각 인지 |

### 9.3 시리즈 정체성·일관성·확장성

- **단원별 Q/A 성별 교차** (voice-pool §3.1): 단원1 Q여+A남 → 단원2 Q남+A여 … 시즌 내 균형. 시청자가 *다양한 목소리의 학습 친구*를 만난다.
- **config SSOT(voice-pool §0)가 일관성의 닻**: 어느 세션·어느 NCC가 와도 §0만 읽으면 동일 음성. 시리즈 톤이 우연이 아니라 *재현 가능한 표준*.
- **인물별 voice 고정(향후)**: 에라토스테네스 = 고정 voice → 시즌 재등장 시 즉시 인지. 시리즈 정체성의 음성 브랜딩.
- **확장**: jsonl 스키마 + voice-pool 풀 + 합성 6-step이 단원 무관 재사용 자산. 다음 단원은 voice 조합만 바꿔 바로 시작 (retro §2 교훈: "확정 config로 바로 시작, 단 신규 voice는 청취 없이 확정 금지").

### 9.4 이 STEP만의 차별화 포인트

다른 어떤 STEP도 *소리*를 만들지 않는다. STEP 4는 **인물 이야기에 인격(목소리)을 부여**하는 유일한 단계다. 같은 텍스트도 voice·억양·호흡·pause에 따라 "지루한 낭독"과 "친구의 신나는 이야기"로 갈린다. 그래서 STEP 4의 품질이 영상 전체의 *정서적 온도*를 결정한다 — 흥미(B축)가 최우선인 본 프로젝트(PURPOSE)에서, STEP 4는 흥미의 마지막 1마일이다.

---

## 부록: 변경 이력

- 2026-05-29: 신규. 00_index 9섹션 템플릿 기반. exp-002 STEP 4 (v0.1→v0.5.2) 실제 산출물 + voice-pool §0 확정 config + retro 도구 변천 인용.
