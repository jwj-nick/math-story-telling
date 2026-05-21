# Unit 01 — Eratosthenes (Channel)

> Season 1 · Ancient · ⏳ BCE 276–194

## 텍스트 소스 (git)
- `storyboard.md` — 5-scene 스토리보드
- `narration.txt` — TTS 입력 원문 (250자, ~50초)
- `config.json` — HyperFrames 렌더 설정 (장면 텍스트, 심볼, 팔레트)

## 빌드 산출물 (gitignored — ε storage)
- `narration.mp3` — edge-tts(ko-KR-SunHiNeural) 출력
- `raw.mp4` — HyperFrames(GSAP) 렌더본
- `final.mp4` — FFmpeg 합성 (영상+오디오)

빌드는 별도 toolchain. final.mp4는 GitHub Releases 또는 YouTube 업로드용.

## 인물·팔레트
- Person: 에라토스테네스 (도서관, 막대기, 체)
- Palette: `era-ancient` — sand gold + night sky
- Signature color: `#D4A843`

## 연관 앱
- `apps/math1/unit-01/story.html` — 같은 인물 인터랙티브 서사
- `apps/math1/unit-01/concepts.html` — 소인수분해/체 인터랙티브 도구
