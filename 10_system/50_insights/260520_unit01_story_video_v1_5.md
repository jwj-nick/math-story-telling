<!-- 260520_unit01_story_video_v1_5.md -->

# Unit 01 v1.5 영상 — 에라토스테네스

## 메타
- 일자: 2026-05-20
- 단원/대상: unit-01 / 소인수분해 — 에라토스테네스
- skill: /se_story_video_v1_5
- 산출물: `channel/season-1-ancient/unit-01/final_v1_5.mp4` (21MB, 107.4s)
- 작업 시간: 약 3시간 (소스 + 빌드 + 2회 narration 정제)

## 잘 된 것 (Wins)
- **6장면 구조가 호흡에 잘 맞음** — S2 시대 풍경 20s가 v1 대비 큰 진보. "그 시대에 들어간 느낌" 확보.
- **AI 이미지 5장 효과 큼** — Claude/ChatGPT 생성으로 일관된 노년 학자 캐릭터. v1 SVG 추상에서 한 단계 진화.
- **edge-tts `--rate=-5%` + 단문 호흡** = 자연스러운 휴지 — Nick 톤 피드백 한 번에 해결.
- **HyperFrames + GSAP + ken burns** 검증 — scale 1.0 → 1.06, x -30 부드러움.
- **`data-duration = audio + 2s`** 패턴이 -shortest와 잘 맞음 (audio가 잘리지 않음).

## 아쉬운 것 (Misses)
- **SSML 시도 실패** — `<break time="500ms"/>` 등 XML 태그가 edge-tts CLI에서 그대로 읽힘. 300s짜리 망친 mp3 1회 생성. → 단문 + 빈 줄로 우회.
- **첫 narration 78.8s로 짧았음** — 5자/초 가정이 실제 7자/초였음. 길이·rate 측정 표준 필요.
- **이미지 확장자 mismatch** — index_v1_5.html에 `.jpg`로 작성했는데 Nick PNG 생성. Edit 5번으로 수정.
- **이미지 생성 도구 미정** — Nick이 Claude/ChatGPT로 생성. SD/MJ 전환은 Nick_TODO에만 적혀있음. 단원마다 도구 일관성 보장 없음.
- **인물 캐릭터 시트가 image_prompts.md에 산재** — 5장 프롬프트에 같은 묘사를 5번 반복. 헤더에 "공통 캐릭터" 섹션 두는 게 나음.
- **영상 retrospective가 NCC 작업의 일부가 아니었음** — Nick이 시켜야만 회고. 자동화 부재.

## 다음에 다르게 해볼 것 (Try Next)
- **edge-tts dry run 측정**: narration.txt 작성 후 즉시 `edge-tts --rate=-5% --text "$(cat narration.txt)" -w test.mp3 && ffprobe test.mp3 | grep Duration`으로 길이 확인 → 95~120s 안 되면 narration 재조정. 빌드 들어가기 전에.
- **이미지 명세에 확장자 명시**: image_prompts.md에 파일명을 `s2-vista.png` 형태로 미리 적고, index_v1_5.html도 png로 작성. 도구가 PNG 기본이면 PNG로 통일.
- **인물 캐릭터 시트 분리**: image_prompts.md 최상단에 `## 인물 공통 묘사` 섹션. 각 프롬프트는 "use the common character" 식 참조.
- **S2 풍경에 인물 미포함 원칙 확정** — Unit 01에서 우연히 그렇게 됨. 명시화 필요.
- **빌드 직후 retrospective 자동 작성** — skill Phase E 마지막 단계로.

## 일반 원칙 후보 (Principle Candidates)
1. **SSML 사용 금지** — edge-tts CLI에서 동작 안 함. 호흡은 단문 + 빈 줄 + `--rate=-5%`.
   - 근거: 1회 실패 시도 (narration_v1_5.xml).
   - 적용처: `principles/STORY_VIDEO_v1_5.md §5.3`, `context/TONE_GUIDE.md §1.3`.

2. **narration 길이 dry run 의무화** — 빌드 진입 전 TTS 합성 1회로 길이 검증.
   - 근거: 첫 78.8s 짧음 사고.
   - 적용처: `principles/STORY_VIDEO_v1_5.md §4 [6]` (TTS 합성 → 길이 확인 → narration 조정 분기).

3. **이미지 파일명 정합성** — image_prompts.md, config.json, index.html에서 동일 확장자.
   - 근거: jpg/png 5회 수정.
   - 적용처: `principles/STORY_VIDEO_v1_5.md §2.4` (파일명 표준에 ".png 기본" 명시 — 이미 갱신함).

4. **인물 캐릭터 시트 분리** — image_prompts.md 최상단에 공통 묘사.
   - 근거: 5장 반복 묘사.
   - 적용처: `principles/STORY_VIDEO_v1_5.md §2.2`에 추가 필요.

5. **retrospective는 skill의 의무 산출물** — Phase E에 포함.
   - 근거: 진화 사이클 자체.
   - 적용처: `principles/STORY_VIDEO_v1_5.md §5.6` (이미 추가), `se_story_video_v1_5/SKILL.md` Phase E 추가 필요.

## 반영 상태
- [x] 1번 (SSML 금지) → principles/STORY_VIDEO_v1_5.md §5.3 + §3.1
- [x] 5번 (retrospective 의무) → principles/STORY_VIDEO_v1_5.md §5.6
- [x] 3번 (.png 기본) → principles/STORY_VIDEO_v1_5.md §2.4
- [ ] 2번 (length dry run) — distill 후 §4 절차에 분기 추가 필요
- [ ] 4번 (캐릭터 시트 분리) — distill 후 §2.2에 추가 필요

부분 반영. 미반영 2건은 다음 distill에서.

## 변경 이력
- 2026-05-21: 초안. 5개 원칙 후보 도출, 3개 즉시 반영, 2개 dispense 대기.
