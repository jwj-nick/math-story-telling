<!-- tts-tools-guide.md / TTS 도구 비교 + setup 가이드 -->

# TTS 도구 가이드 (한국어 영상 나레이션)

> **목적**: 본 스킬 (`se-video-narration`) 이 호출 가능한 TTS 도구들의 가격·기능·setup·voice 비교.
> **단일 진입점**: [SKILL.md](./SKILL.md)
> **본 문서의 결정 효과**: STEP 4 시범 선택 + 다음 단원·시즌 도구 선정 + Nick 의 setup 단계
> **최근 갱신**: 2026-05-25 (가격 정보는 공식 사이트 확인 필수 — 변동 가능)

---

## 0. 한 줄 요약 (2026-05-26 갱신 — Google 1차 마이그)

| 우선 | 도구 | 핵심 | 본 프로젝트 사용 |
|---|---|---|---|
| 🥇 **1차** | **Google Cloud TTS** | **SSML 풀 + Neural2 한국어 우수 + 무료 한도 100만 chars/월** | **exp-002 STEP 4 v3.2 진행** |
| 🥈 2차 | ElevenLabs | 감정 표현 최강 (premade voice 만 free) | Free tier API 차단 (library voice 불가) — Starter $5 결제 시 사용 |
| 🥉 3차 | edge-tts | 완전 무료 + 한국어 3 voice 한정 | 청소년 voice 부재로 v2 폐기, fallback 가능 |

> **마이그 사유**: ElevenLabs Free tier 가 library voice (Mono Beige/Onyu/Kyle/Mike) API 호출 = HTTP 402 차단. Nick 결정 → 옵션 B (Google Cloud TTS) 선정.
> 상세 setup: [`google-cloud-tts-guide.md`](./google-cloud-tts-guide.md)

본 프로젝트 110초 영상 1편 = ~550자. Google Neural2 무료 한도 = **1,800편/월** → 0원.

---

## 1. 옵션 비교 표

| 도구 | 가격 | SSML | 한국어 voice | 감정 표현 | NCC 호출 |
|---|---|---|---|---|---|
| **edge-tts** | 무료 | 부분 (prosody / break) | Azure Neural (5종+) | 기본 (style 일부) | ✅ Python CLI |
| **ElevenLabs** | 유/무료 (아래 상세) | 미지원 | English voice 다국어 portable | ★★★★★ 최고 | ⚠️ API key 필요 |
| **Google Cloud TTS** | 종량제 (무료 한도 큼) | ✅ 풀 지원 | ko-KR-Neural2/Wavenet | 중간 | ⚠️ 서비스 계정 |
| **Amazon Polly** | 종량제 (12개월 무료) | ✅ 풀 지원 | ko-KR-Seoyeon (Neural) | 중간 | ⚠️ AWS credentials |
| **OpenAI TTS** | $15/$30 per 1M chars | ❌ 미지원 | English voice 한국어 portable | 좋음 | ⚠️ API key |
| **Azure Speech** | 종량제 (무료 한도) | ✅ 풀 지원 | ko-KR-* (edge-tts 와 동일 backend) | 중간 | ⚠️ subscription key |

---

## 2. 금액 상세 (2026-05 기준, 공식 사이트 확인 필수)

### edge-tts
- **완전 무료**, 사용량 제한 없음 (rate limit 가능성)
- Microsoft Edge 브라우저 "read aloud" backend (Azure Neural) 재사용
- **본 프로젝트 110초 영상 1편 = $0**

### ElevenLabs
- **Free**: 매월 10,000 글자 (한국어 영상 약 **18편/월**)
- Starter $5/월: 30,000 글자 (영상 약 54편/월)
- Creator $22/월: 100,000 글자 + voice cloning
- Pro $99/월: 500,000 글자
- 공식: https://elevenlabs.io/pricing
- **본 프로젝트 영상 1편 = $0 (Free 한도 내)**

### Google Cloud TTS
- **무료 (월별 갱신)**:
  - Standard 400만 글자
  - WaveNet 100만 글자
  - Neural2 100만 글자
- 초과 시:
  - Neural2: $16 / 100만 글자
  - WaveNet: $16 / 100만 글자
  - Standard: $4 / 100만 글자
- 공식: https://cloud.google.com/text-to-speech/pricing
- **본 프로젝트 영상 1편 = $0 (무료 한도 매우 큼)**

### Amazon Polly
- **무료 (가입 후 12개월)**:
  - Neural 100만 글자/월
  - Standard 500만 글자/월
- 12개월 이후:
  - Neural: $16 / 100만 글자
  - Standard: $4 / 100만 글자
- 공식: https://aws.amazon.com/polly/pricing
- **본 프로젝트 영상 1편 = $0~$0.01**

### OpenAI TTS
- Standard (tts-1): $15 / 1M chars
- HD (tts-1-hd): $30 / 1M chars
- 무료 tier 없음
- **본 프로젝트 영상 1편 (550자) = $0.008 (standard) / $0.017 (HD)**

### Azure Speech (직접)
- **무료 (월별)**: Neural 50만 글자
- 초과: $16 / 1M chars
- **본 프로젝트 영상 1편 = $0 (무료 한도 900편/월)**

---

## 3. NCC 추천 (본 프로젝트 기준 — 2026-05-26 v3.2 마이그)

| 우선 | 도구 | 이유 |
|---|---|---|
| 🥇 **1차** | **Google Cloud TTS** | ko-KR-Neural2 한국어 voice 우수 + SSML 풀 + 무료 한도 100만 chars/월 + 결제 안정 (Free tier 차단 X) |
| 🥈 2차 | **ElevenLabs Starter $5** | premade voice 만 Free 가능, library voice (Mono Beige/Mike) = $5 결제 시 사용. 감정 표현 최강 |
| 🥉 3차 (fallback) | **edge-tts** | 한국어 3 voice 한정, 청소년 voice 부재 |

본 시범 시퀀스 (현재 진행):
1. STEP 4 v1 = edge-tts SunHi (단일 voice) — 평면 톤 → 폐기
2. STEP 4 v2 = edge-tts SunHi+InJoon (2 화자) — 211s, 청소년 voice 부재 → 폐기
3. STEP 4 v3 = ElevenLabs Jessica+Will (premade) — 127.6s, 미국식 한국말 → 폐기
4. STEP 4 v3.1 = ElevenLabs Mono Beige+Mike (library) — HTTP 402 Free tier 차단 → 결제 보류
5. **STEP 4 v3.2 = Google Cloud TTS Neural2-A+C (현재)** — Nick setup + 시범 진행

비교 결과 → 본 문서 §7 채움 + voice-pool.md Google section.

---

## 4. Google Cloud TTS Setup 가이드 (1차, 현행)

> **상세 가이드**: [`google-cloud-tts-guide.md`](./google-cloud-tts-guide.md) — 13 섹션 full setup.
> 본 § = 요약.

### 4.0 단계 요약
1. Google Cloud 계정 + 새 프로젝트 + 결제 연결 (무료 한도 안 사용 시 0원)
2. "Cloud Text-to-Speech API" 활성화
3. IAM → 서비스 계정 `tts-narration` 생성 + 역할 "Cloud Text-to-Speech 사용자"
4. JSON key 발급 → `C:\Users\admin\.gcloud\tts-key.json` 저장
5. PowerShell setx:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'C:\Users\admin\.gcloud\tts-key.json', 'User')
   ```
6. `pip install google-cloud-texttospeech`
7. NCC 에 "Google TTS setup 완료" 알림 → NCC 자동 합성

### 4.1 NCC 자동 인식 패턴
```bash
GCRED=$(powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'User')" | tr -d '\r\n')
export GOOGLE_APPLICATION_CREDENTIALS="$GCRED"
```

(reference: [`memory/reference_powershell_key_extraction.md`](C:/Users/admin/.claude/projects/C--Kids-math-story-telling/memory/reference_powershell_key_extraction.md))

### 4.2 본 프로젝트 voice 매핑 (Neural2)

| 화자 | voice | 톤 |
|---|---|---|
| **Q (여, 청소년, 존댓말)** | `ko-KR-Neural2-A` | 표준, 따뜻 |
| **A (남, 대학원생, 친절 반말)** | `ko-KR-Neural2-C` | 차분, 친절 |

(Nick 청취 후 평가 → `voice-pool.md` Google section)

### 4.3 청취 페이지
https://cloud.google.com/text-to-speech/docs/voices

---

## 5. ElevenLabs Setup 가이드 (2차, Starter $5 결제 시)

### 4.1 계정 + key 발급

1. https://elevenlabs.io/ 회원가입 (이메일 + 비밀번호, 무료)
2. 로그인 → 우측 상단 프로필 클릭 → **"Profile + API Key"**
3. **"Generate API Key"** 클릭
4. 표시된 키 복사 (sk_xxx...). **1회만 표시됨** — 안전한 곳에 저장.

### 4.2 환경 변수 설정 (Windows)

**PowerShell** (영구 — User 환경 변수):
```powershell
[System.Environment]::SetEnvironmentVariable('ELEVENLABS_API_KEY', 'sk_xxx...', 'User')
```

검증 (새 터미널 열고):
```powershell
echo $env:ELEVENLABS_API_KEY
```

**MINGW64 Bash** (한 세션만):
```bash
export ELEVENLABS_API_KEY="sk_xxx..."
```

→ 영구 설정은 위 PowerShell 명령 사용 (재시작 후에도 유지).

### 4.3 NCC 검증

설정 완료 후 NCC 에게 *"ElevenLabs key 설정 완료"* 알림. NCC 는 다음 명령으로 *변수 존재만* 확인:

```bash
[ -n "$ELEVENLABS_API_KEY" ] && echo "SET" || echo "unset"
```

key 값은 chat 에 출력 X (보안).

### 4.4 사용량 확인

- https://elevenlabs.io/usage
- 무료 한도 (10,000자/월) 초과 시 음성 합성 차단

---

## 5. 한국어 voice 비교

### edge-tts (Azure Neural — 무료 backend)

전체 voice 리스트:
```bash
edge-tts --list-voices | grep ko-KR
```

주요 voice:
| voice | 성별 | 톤 | 본 프로젝트 추천 |
|---|---|---|---|
| `ko-KR-SunHiNeural` | 여성 | 표준, 따뜻 | ★ 1차 추천 (학습자 친화) |
| `ko-KR-InJoonNeural` | 남성 | 표준, 차분 | 1차 대안 |
| `ko-KR-HyunsuMultilingualNeural` | 남성 | 다국어 (영문 인명 자연) | S5 카메오 (유클리드·류후이 영문 발음) |
| `ko-KR-BongJinNeural` | 남성 | 캐주얼 | (단원 분위기 다름) |
| `ko-KR-GookMinNeural` | 남성 | 뉴스 톤 | (강의 톤 X 본 프로젝트 부적합) |

본 시범 1차 voice = `ko-KR-SunHiNeural` (NCC 추천).

### ElevenLabs

ElevenLabs 의 영어 voice 가 *multilingual_v2* model 로 한국어 발화 가능 (영문 풍 한국어, 한국어 자연도 검증 필요).

추천 voice (다국어 model):
- **Charlotte** (여성, 따뜻, V2)
- **Bella** (여성, 표현력 풍부)
- **Adam** (남성, 차분)
- **Rachel** (여성, 표준)

→ Nick 검토 시 voice 1~2개 선정 + 짧은 텍스트로 한국어 자연도 시범.

---

## 6. SSML 지원 비교

| 도구 | SSML 지원 | break | prosody (rate/pitch) | emphasis | phoneme | mark |
|---|---|---|---|---|---|---|
| Azure / Google / Amazon | ✅ 풀 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **edge-tts** | ⚠️ 부분 | ✅ | ✅ rate/pitch/volume | ❌ | ❌ | ❌ |
| ElevenLabs | ❌ | (텍스트 .) | (voice settings) | (자연 강조) | ❌ | ❌ |
| OpenAI TTS | ❌ | (텍스트 .) | (voice 선택) | (자연 강조) | ❌ | ❌ |

→ 본 프로젝트 = prosody + break 만 사용. edge-tts 충분.
→ phoneme (특정 단어 발음 교정) 필요 시 Azure 직접 / Google / Amazon.

---

## 7. 시범 결과 비교 표 (시범 완료 후 채움)

| 항목 | edge-tts | ElevenLabs |
|---|---|---|
| 자연도 (한국어) | (시범 후) | (시범 후) |
| 감정 표현 (S4 떨림) | (시범 후) | (시범 후) |
| 길이 정확도 (±10%) | (시범 후) | (시범 후) |
| 비용 (영상 1편) | $0 | $0 (무료 한도) |
| 호출 복잡도 | 낮음 (Python CLI 1줄) | 중간 (HTTP API) |
| SSML 지원 | 부분 (prosody/break) | 미지원 |
| 권장 사용 | **일상 / 대량 단원** | **결정적 순간 / 정밀 감정** |

(다음 단원·시즌에서 비교 결과로 업데이트)

---

## 8. 변경 이력

- 2026-05-25: 신규. exp-002 STEP 4 시범 진입 시 작성.
