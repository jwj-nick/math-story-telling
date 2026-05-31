---
name: se_story_video_v1_5
description: Story 영상 v1.5 제작 파이프라인. 6장면 110초 + AI 이미지 4~6장 + edge-tts. 호출 예시 — "/se_story_video_v1_5 unit-01", "/se_story_video_v1_5 unit-02 브라마굽타".
---

# se_story_video_v1_5 — Story 영상 v1.5 제작 스킬

> **명세 SSOT**: `C:/Kids/90_Workspace/mathtelling/system/principles/STORY_VIDEO_v1_5.md` (2026-05-21 이동)
>
> **참조 context**:
> - `system/context/TONE_GUIDE.md` — narration 톤·호흡
> - `system/context/ERA_PALETTES.md` — 시대 팔레트 (era-ancient 등)
>
> v1(50초·SVG)에서 v1.5(110초·AI 이미지)로의 진화. 이 skill은 한 단원의 v1.5 영상 소스를 처음부터 끝까지 만든다.

## 인자 형태

```
/se_story_video_v1_5 unit-01
/se_story_video_v1_5 unit-02 브라마굽타
/se_story_video_v1_5 unit-03 --rebuild   # 기존 자료 재활용
```

## 산출물 위치

```
C:/Kids/90_Workspace/mathtelling/channel/season-X-Y/unit-NN/
├── storyboard.md       (NCC 작성)
├── narration.txt       (NCC 작성, 480~600자)
├── image_prompts.md    (NCC 작성, 4~6장)
├── config.json         (NCC 작성)
├── index.html          (NCC 작성, v1.5 템플릿 + 단원 데이터)
├── _assets/            (Nick이 AI 이미지 생성 후 배치)
├── narration.mp3       (빌드 산출물 — gitignore)
├── raw.mp4             (빌드 산출물 — gitignore)
└── final.mp4           (빌드 산출물 — gitignore)
```

## 절차

### Phase A — 리서치·내러티브 작성 (NCC 자동)

1. **소스 확인**
   - `content/people/{person}.md` — 인물 데이터
   - `content/units/{NN}/meta.json` — 단원 메타
   - `40_BaseDocs/NN_단원명/` (base resource)
   - 기존 `apps/math1/unit-NN/story.html` (있다면, 톤·세부 재사용)

2. **storyboard.md 작성** — 6장면 구조 (`PIPELINE_v1_5.md §1`)
   - S1 타이틀(5s) → S2 시대 풍경(20s) → S3 인물 등장(25s) → S4 결정적 순간(30s) → S5 수학 연결(25s) → S6 마무리(10s)
   - 각 장면: 헤드라인 + 본문 + 시각 메모

3. **narration.txt 작성** — 480~600자
   - 장면별 분량 가이드 따름
   - 5자/초 기준 110초 안에 들어오는지 확인
   - 이야기 톤, 짧은 문장

### Phase B — AI 이미지 프롬프트 (NCC 작성, Nick 실행)

4. **image_prompts.md 작성** — 4~6장
   - 각 프롬프트: scene 번호 · 파일명 · **English 프롬프트** · negative · style notes
   - 시대 정확성·인물 일관성·여백 확보 규칙 (`PIPELINE_v1_5.md §2.2`)
   - 첫 단원 또는 새 인물 추가 시 인물 외모 캐릭터 시트 먼저 (얼굴·나이·복장)

5. **Nick TODO 알림**
   - chat에 "다음 이미지 프롬프트를 Claude/ChatGPT 이미지 생성에 복붙해서 `channel/.../unit-NN/_assets/`에 저장하세요" 안내
   - 또는 SD/MJ 사용자면 그쪽 포맷으로 변환

### Phase C — 컴포지션 (NCC 자동)

6. **config.json 작성**
   - 장면별 텍스트, 이미지 파일명, 팔레트, duration 기본값

7. **index.html 작성**
   - `_templates/story-master-v1_5.html` 복제 + 단원 데이터 치환
   - 6 scene div + GSAP 타임라인 + ken burns motion + AI 이미지 src

### Phase D — 빌드 (Bash, 가능 범위까지 NCC 자동)

8. **TTS 합성**
   - `edge-tts --voice ko-KR-SunHiNeural --rate=-5% --text "$(cat narration.txt)" --write-media narration.mp3`
   - **SSML 사용 금지** — edge-tts CLI는 `<break>` 등 XML 태그를 그대로 읽음. 휴지는 단문 + 빈 줄로.
   - 실패 시 Nick 환경에 edge-tts 없음 → 설치 가이드

8a. **Length dry run (의무)**
   - 합성된 narration.mp3 길이 확인: `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3`
   - 95~120s 범위 밖이면 narration.txt 조정 후 8 재실행
   - 너무 짧음(<95s) → 빈 줄 추가 또는 자 수 늘리기
   - 너무 김(>120s) → 자 수 줄이기 또는 `--rate=-3%`로 변경

9. **길이 측정 + index.html 갱신**
   - `data-duration` = `narration 길이 + 2s` (오디오 안 잘리도록)

10. **HyperFrames 렌더**
    - `hyperframes render -f 24 -q standard index.html`
    - 출력 → raw.mp4

11. **FFmpeg 합성**
    - `ffmpeg -i raw.mp4 -i narration.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest final.mp4`

### Phase E — 검증 + 회고 (NCC 자동)

12. **Rule 체크리스트** (`system/principles/STORY_VIDEO_v1_5.md §5`)
    - 길이 95~120초, 6장면 존재
    - 이미지 4장 이상, 16:9
    - 나레이션 480~620자
    - SSML 0개

13. **Retrospective 자동 작성 (의무)**
    - 위치: `mathtelling/system/insights/{YYMMDD}_unitNN_story_video_v1_5.md`
    - 양식: `mathtelling/system/insights/_template.md`
    - 작성 후 `_index.md` 미반영 섹션에 한 줄 추가
    - 작성 항목: 잘 된 것 / 아쉬운 것 / 다음에 다르게 / 일반 원칙 후보 / 반영 상태

14. **결과 보고**
    - 최종 파일 위치, 파일 크기, 길이
    - retrospective 경로
    - 누적된 미반영 insight 개수 — 3편 이상이면 `/se_distill_principles` 호출 제안
    - 다음 단원 진행 또는 Nick 리뷰 안내

## 갈래

| 조건 | 대응 |
|---|---|
| AI 이미지 없음 | Phase D 진행 — index.html은 이미지 경로 비워둠 (placeholder 색 면) |
| edge-tts 설치 안 됨 | Phase D 중단 — Nick에게 설치 가이드 |
| HyperFrames 없음 | Phase D 중단 — 빌드는 Nick이 수동 진행, NCC는 소스까지만 |
| 기존 v1 영상 있음 | storyboard/narration는 v1을 참조해 확장 (재사용 ratio 60%+) |

## audit 연계

영상 완성 후:
- `/se_ncc_audit_story` — 인물 서사 적합성
- (선택) `/se_audit_storyteller`, `/se_audit_educator`, `/se_audit_designer`, `/se_audit_learner` — 페르소나 audit (Nick TODO)

## 변경 이력

- v0.1 (2026-05-20): 초안. v1.5 PIPELINE 명세 기반.
- v0.2 (2026-05-21): SSOT 경로 system/principles/로 갱신. Phase D에 length dry run 의무화, --rate=-5% 표준화, SSML 금지 명시. Phase E에 retrospective 자동 작성 추가 (system/insights/). TONE_GUIDE / ERA_PALETTES 참조 추가.
