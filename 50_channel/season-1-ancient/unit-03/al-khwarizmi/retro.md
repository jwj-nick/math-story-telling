<!-- 50_channel/season-1-ancient/unit-03-al-khwarizmi/retro.md / unit-03 제작 retrospective -->

# unit-03 알콰리즈미 — 제작 retrospective

> **단원**: math1 단원 3 — 문자와 식 / **인물**: 알콰리즈미 / **한 단어**: 균형
> **산출**: `8-final.mp4` 174.88s (1280×720, 25fps, h264+aac)
> **제작**: 2026-05-30, NCC 자율 8-STEP (unit-02 학습 반영 첫 단원)
> **음성**: Q=Kanna(여) + A=Mike(남) — unit02(남Q·여A) 반대 (시즌 균형, §3.1)

---

## 1. 의의 — unit-02 학습이 반영된 첫 자율 양산

unit-02 피드백(R7~R9)을 스킬 SSOT에 반영한 뒤 처음 만든 단원. 학습이 **실제로 작동**했는지 검증.

| unit-02 학습 | unit-03 적용 결과 |
|---|---|
| R8: 네이티브 16:9 (`aspect_ratio="16:9"`) | 7장 전부 1344×768 → **크롭 손실 0, 머리 잘림 없음** ✅ |
| R8: 인물 headroom 명시 | ref·S2·S5 머리 위 여백 확보 ✅ |
| R7: 직업≠설명언어 | 저울=균형 비유를 *교육 가공*으로 §C 명시, 알콰리즈미 활동(상속 계산)과 분리 ✅ |
| R9: bare filler 회피 | dialog 전체 "음..." 단독 시작 0 ✅ |

## 2. STEP별 결과

| STEP | 산출 | 비고 |
|---|---|---|
| 1 서사 | 1-narrative.md | 균형(저울) + 축 C("글자 없이 풀다=문자는 발명품") + 시즌 이어달리기 |
| 2 스토리 | 2-story-seed.md | 약속2 정서 2장면(상속 동기 + 글자 역설). 저울 모티프 |
| 3 스토리보드 | 3-storyboard.md | era-medieval(이슬람) 팔레트, 저울 시각 자산, 네이티브 16:9 명시 |
| 4 나레이션 | 4-narration.mp3 174.88s | 43 turn. Q=Kanna/A=Mike. bare filler 0 |
| 5 이미지 | 5-images/ 7장 | 네이티브 16:9, ref→S2·S5 일관, 무텍스트 |
| 6 모션 | 6-motion-config.json | turn 타임라인 정렬. 저울 ken_burns |
| 7 렌더 | 7-raw.mp4 174.88s | render_compile.py 재사용(무수정) |
| 8 합성 | 8-final.mp4 174.88s | S3·S5·S6 프레임 검증 통과 |

## 3. 시즌 아크 강화 (3편 누적)

| unit | 인물 | 한 단어 | 연결 |
|---|---|---|---|
| 01 | 에라토스테네스 | 정리 | (니코마우스 기록) |
| 02 | 브라마굽타 | 발명 | S6 "알콰리즈미가 읽음" → unit03 예고 |
| 03 | 알콰리즈미 | 균형 | S1 "브라마굽타 책 callback" + S6 "데카르트 예고" |

→ **이어달리기 서사**: 브라마굽타(음수) → 알콰리즈미(대수) → 데카르트(좌표). 시즌 연속성이 단원마다 명시적 callback/예고로 묶임.

## 4. 발견·개선 시드

| # | 발견 | 제안 |
|---|---|---|
| R10 | 길이 174.88s — unit02(161s)보다 김. 43 turn + 긴 A turn(Mike) | 목표 150~180 내이나, dialog turn 수·길이 가이드 필요(se-video-narration) |
| R11 | `pan_right` motion = render_compile.py 미구현(상수 zoom으로 렌더) | v0.2 컴파일러에 x-translation pan 표현식 추가 (S4 동→서 실제 패닝) |
| R12 | S5 split 양피지에 illegible 손글씨 texture 발생(의도된 "prose 질감") | no-legible-text 원칙 충족. 단 "글자처럼 보이는 squiggle" 허용 범위 명문화 |
| R13 | 네이티브 16:9 첫 적용 = 전 단원 크롭 손실 0 | se-video-image 표준 확정. unit01·02 구작도 향후 재생성 시 적용 |

## 5. Nick 검수 포인트

- 🔊 음성: Kanna(여 Q) youth 톤 + Mike(남 A) 자연도 / 의문문·"헐~~"
- 🎬 자막 sync: "알지브르→대수"(S2) / "양변을 늘 균형있게"(S3) / "문자 x=발명품"(S5) / "균형"(S6)
- 🖼 이미지: 알콰리즈미 일관성(S2·S5) / 저울(S3) / 이슬람 황금기 고증
- 📐 수학: 균형(양변 같은 연산) 개념 정확. 축 C(문자=발명품) 단원3 본질 부합
