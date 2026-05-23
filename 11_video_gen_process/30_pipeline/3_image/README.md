<!-- 3_image/README.md -->

# 3_image — AI 이미지 프롬프트 + 생성 + 캐릭터 일관성

**입력**: `1_storyboard/seeds/<unit>.md` + `character_sheets/<person>.md`
**출력**: `image_prompts_<unit>.md` (영문 프롬프트) + (Nick 작업) `_assets/*.png` (5장)

## 현 표준 (baseline = unit-01)
- 단원당 5장 (S2 1 + S3 1 + S4 1~2 + S5 1 + S6 0~1)
- 16:9 (1920×1080 또는 1280×720)
- 각 프롬프트 3블록: 영문 / Negative / Style notes
- **공통 캐릭터 시트** (S3·S4 인물 일관성)
- baseline: `../../10_reference/02_baseline_unit01.md` §4

## 진행 우선순위 (compact 후)

### 🔴 캐릭터 시트 분리 (D4 from 260520 insight)
- `image_prompts.md` 최상단 ## 인물 공통 묘사 섹션
- 각 장면 프롬프트는 "use the common character" 참조
- 19인 (또는 시즌1 5인) 모두 시트 작성

### 🔴 MJ `--cref` 도입 (D-006)
- Midjourney basic $10/월
- 인물 1명당 reference 이미지 1장 → 모든 장면 동일 인물
- Discord 또는 API
- 도구: `70_tools/mj_prompt_convert.py` (프롬프트 → MJ 사양)

### 🟡 캐릭터 시트 라이브러리
- `character_sheets/eratosthenes.md` (이미 unit-01 image_prompts.md 에 존재 — 분리)
- `character_sheets/brahmagupta.md`
- `character_sheets/al-khwarizmi.md`
- `character_sheets/diophantus.md`
- `character_sheets/descartes.md`

## 함정
- 이미지에 글자 X (Negative 명시 필수)
- 시대 anachronism X (시계·안경·종이책 등)
- 텍스트 들어갈 여백 30% 확보 (프롬프트에 `generous empty space on left`)
- 이미지 확장자 통일 (`.png` 기본 — `STORY_VIDEO_v1_5.md` §2.4)

## 작성 후보
- `CHARACTER_SHEET_STANDARD.md` — 시트 작성 양식 + 활용 규칙
- `MJ_PROMPT_GUIDE.md` — MJ 변환 표준
- `character_sheets/` 5인 (또는 19인)
- `seeds/unit_02_image_prompts.md` (첫 신규)
