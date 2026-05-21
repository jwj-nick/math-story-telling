<!-- ERA_PALETTES.md -->

# 시대 팔레트 — 영상·앱 공통 시각 톤

> 단원별 인물의 시대에 맞는 색·서체·분위기 표준.
> v1.5 영상 `index_v1_5.html` 인라인 CSS, story.html / concepts.html 헤더 영역에서 참조.
>
> **확정**: era-ancient (Unit 01에서 검증)
> **슬롯**: 나머지 시대 — 단원 제작 진행하며 하나씩 확정

---

## 1. 팔레트 슬롯 매핑

| 팔레트 | 시대 | 단원 | 대표 인물 | 상태 |
|---|---|---|---|---|
| **era-ancient** | 헬레니즘 (BC 3C ~ AD 2C) | Unit 01, 04 | 에라토스테네스, 디오판토스 | ✅ 확정 |
| **era-india** | 굽타·고전 인도 (5~12C) | Unit 02 | 브라마굽타 | ⬜ 슬롯 |
| **era-islamic** | 이슬람 황금기 (8~13C) | Unit 03 | 알콰리즈미 | ⬜ 슬롯 |
| **era-renaissance** | 르네상스·근세 (15~17C) | Unit 05~06 | 데카르트 | ⬜ 슬롯 |
| **era-modern** | 19~20C | Unit 07~13 (예정) | TBD | ⬜ 슬롯 |

각 슬롯은 그 단원 제작 시 확정. 미리 다 채우지 않음 (D4 정신).

---

## 2. era-ancient (확정)

### 2.1 콘셉트
- 키워드: "sand gold + night sky", 알렉산드리아 등대 / 별이 박힌 사막 밤하늘
- 분위기: 따뜻한 황금빛 + 깊은 밤색. 도서관의 양피지 + 항구의 어둠.

### 2.2 색상 토큰
```css
:root {
  --bg:         #1a1610;   /* 깊은 갈색 (밤사막) */
  --bg-deep:    #0e0b07;   /* 더 어두운 부분 (그라데이션 끝) */
  --text:       #f0e6d2;   /* 양피지 베이지 */
  --muted:      #b89968;   /* 흐릿한 금빛 (보조 텍스트) */
  --accent:     #D4A843;   /* 황금 (강조) */
  --accent-soft: rgba(212, 168, 67, 0.18);  /* 황금 글로우 */
  --ink:        #2a1f12;   /* 잉크 — 밝은 배경 위 어두운 글자용 */
}
```

### 2.3 서체
```css
--font-serif: 'Nanum Myeongjo', serif;     /* 본문·인용 */
--font-sans:  'Noto Sans KR', sans-serif;  /* UI·번호·자막 */
```

### 2.4 사이즈 표준 (1280×720 영상 기준)
```css
--title-size:    88px;   /* S1 메인 타이틀 */
--subtitle-size: 26px;   /* S1 부제 */
--headline-size: 48px;   /* S2~S6 헤드라인 */
--body-size:     28px;   /* S2~S6 본문 */
--caption-size:  20px;   /* 자막·메타 */
```

### 2.5 시각 모티프 (이미지 프롬프트용)
- 시각 키워드: `golden hour`, `oil lamp`, `papyrus scroll`, `marble columns`, `desert night`, `lighthouse beacon`, `astronomical instruments`
- 인물 시대 의상: 헬레니즘식 chiton/himation, 노년 학자 (회백색 수염), 차분한 자세
- 금기: 현대 의상, 시계, 안경, 종이책(현대식 제본)

### 2.6 검증
- Unit 01 v1.5 (2026-05-20): 21MB final.mp4에서 톤 일관성 확인. Nick 승인.

---

## 3. 팔레트 슬롯 (미확정)

> 각 슬롯은 그 단원 제작이 다가오면 다음 항목을 채운다:
> (1) 콘셉트 키워드, (2) 색 토큰 5개, (3) 서체 2종, (4) 시각 모티프 키워드 5~7개, (5) 금기.

### 3.1 era-india
- **참고**: 인도 산스크리트 문헌, 사원 색채(주황·진홍·금색·흑색), 우물·천문 관측대
- 잠정 키워드: 사프란 오렌지 + 인디고. 별의 천문도, 모래에 그은 숫자.
- 확정 시점: Unit 02 제작 시작 시

### 3.2 era-islamic
- **참고**: 바그다드 지혜의 집, 기하학적 타일 무늬, 청록·금색
- 잠정 키워드: 모자이크 청록 + 따뜻한 모래색. 별 모양 기하 패턴.
- 확정 시점: Unit 03 제작 시작 시

### 3.3 era-renaissance
- **참고**: 데카르트 17C 유럽, 양초·책상·수기 노트, 차분한 어둠
- 잠정 키워드: 자줏빛 어둠 + 차가운 회청색. 좌표축의 직교.
- 확정 시점: Unit 05 제작 시작 시

### 3.4 era-modern
- 확정 시점: Unit 07 이후 인물 확정 후

---

## 4. 적용 위치

| 산출물 | 어떻게 적용 |
|---|---|
| 영상 `index_v1_5.html` | `:root` 내 CSS 변수 인라인 복사 |
| 영상 `config_v1_5.json` | `"palette": "era-ancient"` 메타 표시 (실제 색은 HTML에) |
| Story.html | `<link>` 또는 인라인. 동일 토큰 |
| Concepts.html | 동일 |
| Channel 공용 CSS | `channel/_assets/palettes.css` (TODO: 다중 팔레트 모이면 생성) |

---

## 5. Audit 체크

각 단원 영상·앱:
- [ ] 명시된 팔레트(era-X) 사용
- [ ] 색 토큰 5개 다 정의됨
- [ ] 시대 anachronism 없음 (이미지 프롬프트 §2.5 참고)

---

## 6. 변경 이력

- 2026-05-21 v0.1 — era-ancient 확정, 나머지 4개 슬롯 (잠정 키워드만).
