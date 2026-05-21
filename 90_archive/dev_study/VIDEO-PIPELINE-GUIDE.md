# Video Pipeline Guide — MathTelling

영상 제작 파이프라인 설명서. `/video-make` 스킬의 배경 문서.

---

## 전체 흐름

```
/video-make unit=## concept=slug person=이름 duration=초
        │
        ▼
STAGE 1  개념 선택 ──────────────── 20_research/ 문서 참조
        │
        ▼
STAGE 2  narration.txt 작성 ──────── 인물 이야기 기반, 사용자 검토
        │
        ▼
STAGE 3  edge-tts → narration.mp3 ── 실제 오디오 길이(AUDIO_DURATION) 측정
        │
        ▼
STAGE 4  index.html 작성 ──────────── _templates/{visual_type}.html + GSAP 타임라인
        │                              data-duration = AUDIO_DURATION + 1
        ▼
STAGE 5  hyperframes render ────────── raw.mp4 (AUDIO_DURATION+1 초 무음)
        │
        ▼
STAGE 6  ffmpeg merge ──────────────── raw.mp4 + narration.mp3 → final.mp4
```

---

## 필수 도구 설치

```powershell
# FFmpeg (오디오·영상 인코딩)
scoop install ffmpeg
ffmpeg -version   # 확인

# edge-tts (한국어 TTS)
python -m ensurepip --upgrade
python -m pip install edge-tts
python -m edge_tts --list-voices 2>&1 | Select-String "ko-KR"   # 확인

# HyperFrames (HTML → MP4)
npm install -g hyperframes
hyperframes browser ensure   # Chrome Headless Shell 다운로드 (~100 MB)
hyperframes doctor            # 환경 전체 점검
```

---

## 디렉토리 규칙

```
90_video/
├── _templates/              ← 시각 유형별 HTML 템플릿 (편집하지 말 것)
│   ├── number-grid.html
│   ├── number-line.html     (unit03 제작 시 추가)
│   ├── balance-scale.html   (unit04 제작 시 추가)
│   ├── coordinate-plane.html (unit08 제작 시 추가)
│   └── ...
│
└── unit{##}_{단원명}/       ← 단원별 폴더
    └── {concept-slug}/      ← 개념별 폴더 (HyperFrames 프로젝트)
        ├── narration.txt    ← 스크립트 원문
        ├── narration.mp3    ← TTS 음성
        ├── index.html       ← 시각적 컴포지션 (HyperFrames가 렌더링)
        ├── raw.mp4          ← 무음 렌더링 결과
        └── final.mp4        ← 완성본 (음성 포함) ★
```

---

## 한국어 TTS 목소리

```powershell
# 사용 가능한 한국어 목소리 확인
python -m edge_tts --list-voices 2>&1 | Select-String "ko-KR"
```

| Voice ID | 성별 | 특성 |
|---|---|---|
| `ko-KR-SunHiNeural` | 여성 | 밝고 명확, 교육 콘텐츠 추천 |
| `ko-KR-InJoonNeural` | 남성 | 차분하고 신뢰감 있음 |
| `ko-KR-HyunsuMultilingualNeural` | 남성 | 다국어 혼용 텍스트에 강함 |

기본값: `SunHiNeural`. 변경 시 skill 파일의 `--voice` 인수를 수정.

---

## 시각 유형 템플릿 추가 방법

새 단원에서 기존에 없는 시각 유형이 필요할 때:

1. `_templates/` 아래 `{visual_type}.html` 파일 생성
2. 필수 요소 포함 체크리스트:
   - `<meta name="viewport" content="width=1280, height=720">`
   - Noto Sans KR CDN link
   - GSAP CDN script
   - `body { width:1280px; height:720px; overflow:hidden; }`
   - Root div: `data-composition-id="{{COMPOSER_ID}}" data-duration="{{DURATION}}" data-width="1280" data-height="720"`
   - `window.__timelines['{{COMPOSER_ID}}'] = tl;` (스크립트 맨 끝)
3. `video-make.md` 스킬 파일의 **Visual Type 표**에 새 행 추가
4. `VIDEO-PIPELINE-GUIDE.md`의 `_templates/` 트리에 주석 추가

---

## FFmpeg 주요 패턴

```powershell
# 영상 + 오디오 합성 (기본)
ffmpeg -i raw.mp4 -i narration.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest -y final.mp4

# 오디오 길이 측정
ffprobe -v quiet -show_entries format=duration -of csv=p=0 narration.mp3

# 영상 길이 + 스트림 확인
ffprobe -v quiet -show_entries format=duration,stream=codec_type -of compact narration.mp3

# 영상 무음 구간 확인 (오디오 스트림 없으면 N/A)
ffprobe final.mp4 2>&1 | Select-String "Audio"
```

---

## HyperFrames 주요 패턴

```powershell
# 렌더링 (디렉토리 지정)
hyperframes render {concept폴더} -o {concept폴더}/raw.mp4 -f 24 -q standard

# 빠른 초안 확인
hyperframes render {concept폴더} -o {concept폴더}/draft.mp4 -f 24 -q draft

# 환경 재확인
hyperframes doctor
```

**주의**: exit code 9는 HyperFrames의 정상 종료 코드.
`Test-Path raw.mp4`로 파일 생성 여부를 직접 확인할 것.

---

## GSAP 핵심 패턴 레퍼런스

```javascript
// 타임라인 기본
const tl = gsap.timeline({ paused: true });
window.__timelines['composerId'] = tl;

// 절대 시간에 배치 (3번째 인수)
tl.to('#elem', { backgroundColor: '#ef4444', duration: 0.3 }, 5.0);

// 순차 딜레이 (forEach)
items.forEach((id, i) => tl.to(id, props, startTime + i * gap));

// 텍스트 교체 — tl.call() 금지, opacity 스왑 사용
function switchText(t, outId, inId) {
  if (outId) tl.to('#' + outId, { opacity: 0, duration: 0.25 }, t);
  tl.to('#' + inId, { opacity: 1, duration: 0.25 }, t + 0.1);
}

// 타이밍 변수 체인
const tPhase1End = startTime + items.length * gap + buffer;
const tPhase2Start = tPhase1End + pause;
```

---

## 트러블슈팅

| 증상 | 진단 명령 | 해결 |
|---|---|---|
| HyperFrames exit 9, raw.mp4 없음 | `hyperframes doctor` | Chrome 재설치: `hyperframes browser ensure` |
| 한글 폰트 깨짐 | HTML 열어서 폰트 확인 | Noto Sans KR CDN link 추가 |
| 오디오 없는 final.mp4 | `ffprobe final.mp4 2>&1 \| Select-String "Audio"` | `-map 1:a` 옵션 확인 |
| 애니메이션이 너무 빨리 끝남 | `ffprobe raw.mp4`로 길이 확인 | `data-duration` 증가, Stage 5 재실행 |
| edge-tts 네트워크 오류 | 인터넷 연결 확인 | VPN 해제 또는 잠시 후 재시도 |
| GSAP seek 시 텍스트 고정 | HTML에서 `tl.call()` 검색 | opacity 스왑 방식으로 교체 |
