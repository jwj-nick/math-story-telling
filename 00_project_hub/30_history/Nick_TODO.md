# Nick TODO — Tools & Skills

> NCC가 진행 중 발견한, Nick이 직접 챙겨야 할 외부 도구 가입·학습 항목.
> 일정 강제 없음. 가용해지면 v1.5 → v2 진화에 반영.

---

## 🔥 단기 (Sprint — Story 영상 v1.5 위해)

### T1. ElevenLabs 한국어 TTS 가입
- **why**: edge-tts(ko-KR-SunHiNeural)는 자연스러운 편이나, ElevenLabs의 한국어 합성이 감정·억양 표현에서 한 단계 위. 50초 영상에서 차이는 미세하지만 90~120초로 길어지면 단조로움이 도드라짐.
- **단계**:
  1. https://elevenlabs.io 무료 가입
  2. 무료 quota: 월 10,000 글자 (한국어 ≈ 30분 분량, 13단원 × 600자 = 7,800자 → 무료로 한 번 가능)
  3. Voice Library에서 한국어 화자 청취 → 1~2개 즐겨찾기
  4. API 키 발급 후 NCC에 알려주거나 `.env`에 보관
- **next**: 가입 완료되면 NCC가 unit-01 narration을 ElevenLabs로 재합성, v1과 청취 비교 라운드

### T2. AI 이미지 생성 워크플로우 손에 익히기
현재 v1.5는 **Claude/ChatGPT 이미지 생성**으로 시작 (브라우저 + 수동 다운로드). 이건 "한 번에 한 장" 워크플로우이고, 13단원 × 5장면 = 65장 이상이 되면 부담스러워짐. 다음 둘 중 하나는 익숙해질 필요.

#### Option A. Stable Diffusion 로컬 (권장)
- **why**: 캐릭터 일관성 유지(LoRA), 배치 생성, 무료, 오프라인
- **단계**:
  1. ComfyUI 또는 A1111(Automatic1111) 설치 — Windows GPU 8GB+ 필요
  2. 모델 1개 골라 다운로드 (DreamShaper, RealVis 또는 SDXL Base)
  3. ControlNet 확장 설치 (구도 유지)
  4. 인물 1명을 위한 LoRA 학습 (예: "에라토스테네스 노년 학자") — 사진 5~10장 모아 dreambooth/kohya로 1시간 학습
  5. 같은 프롬프트로 5장면 일관성 검증
- **참고**: Civitai.com, ComfyUI tutorials

#### Option B. Midjourney 구독
- **why**: 톤·미감 최상위, 한 화면에 4-variant
- **비용**: $10/월 (basic) ~ $30/월 (standard)
- **단계**:
  1. https://midjourney.com Discord 가입
  2. `/imagine` 명령 + `--style raw --ar 16:9 --v 6.1` 옵션 학습
  3. `--cref [URL]` 캐릭터 참조 학습 (인물 일관성)
  4. 다운로드 자동화 — DiscordChatExporter or 수동

→ Nick이 둘 중 하나를 결정하면 NCC가 unit별 프롬프트 시트를 그 도구 사양에 맞게 재작성.

---

## 🟡 중기 (Story 영상 v2 준비)

### T3. Motion Canvas (TypeScript) 학습
- **why**: GSAP 타임라인이 영상 단원 7+로 가면 관리 한계. 코드 기반 키프레임이 더 정밀.
- **참고**: https://motioncanvas.io
- **단계**: 튜토리얼 한 사이클 완주 → unit-01을 Motion Canvas로 포팅 파일럿

### T4. Manim Community
- **why**: Concept 영상(수학 개념 시각화) 별도 트랙. Story는 인물 서사라 Manim과는 결이 다름.
- **단계**: `pip install manim` → 30분 입문 → 사인 함수·소수 시각화 등 1개 만들어보기

---

## 🟢 장기 (e-book / 출판)

### T5. 출판 채널 선정
- **후보**: Lulu (POD), 리디 (한국 e-book), Apple Books, 직접 PDF
- **결정 시점**: 13단원 앱·영상 모두 완성 후

### T6. ElevenLabs 유료 전환 검토
- 무료 quota 한 사이클 돌려보고, 영상 시리즈 본격 출판 시 Starter($5/월) 또는 Creator($22/월) 검토

---

## 진행 로그

| 날짜 | 항목 | 메모 |
|---|---|---|
| 2026-05-20 | T1, T2 신설 | v1.5 진행 중 Nick과 확인. 이번 unit-01은 edge-tts + Claude 이미지로 진행. |

---

## NCC가 도와줄 수 있는 부분

- T1 가입 완료 후: `narration.txt` → ElevenLabs API 호출 코드 작성
- T2-A SD 설치 후: 캐릭터 LoRA 학습 가이드, 배치 프롬프트 시트 작성
- T2-B MJ 가입 후: Midjourney 프롬프트 변환기 작성
- T3 진행 시: Motion Canvas 파일럿 코드 페어 디버깅
- T4 진행 시: 첫 Concept 영상 (예: 소수의 분포) 코드 페어
