<!-- 3_image/README.md -->

# 3_image — AI 이미지 프롬프트 + 생성 + 캐릭터 일관성

**입력**: `../1_storyboard/seeds/<단원>.md` + `character_sheets/<인물>.md`
**출력**: `seeds/<단원>_image_prompts.md` (영문 프롬프트) + (Nick 작업) `_assets/*.png` (5장)

## 현 표준 (1편 = 에라토스테네스 기준)

- 단원당 5장 (S2 1 + S3 1 + S4 1~2 + S5 1 + S6 0~1)
- 16:9 비율 (1920×1080 또는 1280×720)
- 각 프롬프트 3블록: 영문 / 부정 프롬프트 / 스타일 노트
- **공통 캐릭터 시트** 패턴 (S3·S4 인물 일관성)
- 1편 정밀 데이터: `../../10_reference/02_baseline_unit01.md` §4

## 진행 우선순위

### 🔴 캐릭터 시트 분리

(INTEGRATED_PLAN §3.3 4가지 갱신 중 하나 — 자율 작업 1)

- `image_prompts.md` 최상단에 ## 인물 공통 묘사 섹션
- 각 장면 프롬프트는 "use the common character" 참조
- 시즌1 5인 (또는 전체 19인) 모두 시트 작성

### 🔴 Midjourney `--cref` 도입

(INTEGRATED_PLAN §7 결정 ⑤ — 채택 시)

- Midjourney basic 월 $10
- 인물 1명당 reference 이미지 1장 → 모든 장면 동일 인물
- Discord 또는 API
- 도구: `../../70_tools/mj_prompt_convert.py` (프롬프트 → MJ 사양)

### 🟡 캐릭터 시트 라이브러리

- `character_sheets/eratosthenes.md` (1편 image_prompts.md 에서 추출)
- `character_sheets/brahmagupta.md`
- `character_sheets/al-khwarizmi.md`
- `character_sheets/diophantus.md`
- `character_sheets/descartes.md`

## 함정

- 이미지에 글자 X (부정 프롬프트에 명시 필수)
- 시대 anachronism X (시계·안경·종이책 등)
- 텍스트 들어갈 여백 30% 확보 (프롬프트에 `generous empty space on left`)
- 이미지 확장자 통일 (`.png` 기본 — `STORY_VIDEO_v1_5.md` §2.4)

## 작성 후보

- `CHARACTER_SHEET_STANDARD.md` — 시트 작성 양식 + 활용 규칙
- `MJ_PROMPT_GUIDE.md` — Midjourney 변환 표준
- `character_sheets/` 시즌1 5인 (또는 전체 19인)
- `seeds/unit_02_image_prompts.md` (첫 신규)
