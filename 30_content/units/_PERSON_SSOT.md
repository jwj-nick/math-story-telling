# 인물배정 정본 (PERSON SSOT)

> **정본 단일 출처 = 각 단원 `30_content/units/NN/meta.json` 의 `persons[]`.**
> connections.json·앱·영상·manifest 는 모두 여기서 파생/정합되어야 한다. 충돌 시 meta.json 이 이긴다.
> 신설: 2026-06-03 (v2 진화 단계 1 정본화). 검증: build_connections.py 재생성 시 무변화 = 일치.

---

## 1. 단원별 인물 (13단원)

`persons[]` 는 `role: primary | secondary` 로 구분. primary = 현재 영상 보유. secondary = v2 인물 확장(단계 3) 타깃.

| 단원 | 개념 | primary (영상 보유) | secondary (확장 타깃) | 비고 |
|---|---|---|---|---|
| u01 | 소인수분해 | 에라토스테네스 (eratosthenes) | *(미정)* | u01만 1인 — 2nd 인물 단계 3에서 결정 |
| u02 | 정수와 유리수 | 브라마굽타 (brahmagupta) | 알콰리즈미 (al-khwarizmi) | |
| u03 | 문자와 식 | 알콰리즈미 (al-khwarizmi) | 비에트 (viete) | |
| u04 | 일차방정식 | 디오판토스 (diophantus) | 알콰리즈미 (al-khwarizmi) | 알콰리즈미 3회 재등장 |
| u05 | 좌표와 그래프 | 데카르트 (descartes) | 페르마 (fermat) | |
| u06 | 정비례와 반비례 | 케플러 (kepler) | 보일 (boyle) | |
| u07 | 기본도형 | 유클리드 (euclid) | 탈레스 (thales) | |
| u08 | 작도와 합동 | 유클리드 (euclid) | 가우스 (gauss) | 유클리드 2회 |
| u09 | 다각형 | 피타고라스 (pythagoras) | 케플러 (kepler) | |
| u10 | 원과 부채꼴 | 아르키메데스 (archimedes) | 유휘 (liu-hui) | |
| u11 | 다면체와 회전체 | 플라톤 (plato) | 케플러 (kepler) | 케플러 3회 재등장 |
| u12 | 입체도형의 겉넓이와 부피 | 아르키메데스 (archimedes) | 카발리에리 (cavalieri) | 아르키메데스 2회 |
| u13 | 자료의 정리와 해석 | 나이팅게일 (nightingale) | 플레이페어 (playfair) | |

**재등장 인물**(같은인물 연결의 실체): 알콰리즈미(u02·u03·u04), 케플러(u06·u09·u11), 유클리드(u07·u08), 아르키메데스(u10·u12).
**2nd 인물 사실자료**: `30_content/people/` 에 전부 보유(누락 0). 단계 3 차단 요인 없음.

---

## 2. 디렉토리 target convention (단계 3에서 적용 — 현재는 미적용)

v2 다인물 구조의 목표. **물리적 rename 은 단계 3(2nd 인물 영상 제작) 착수 시 실행** — 콘텐츠 없이 미리 rename 하지 않는다(just-in-time, history 노이즈·리스크 회피).

### 2-a. 영상 소스 `50_channel/`
```
[현재 v1]  season-1-ancient/unit-06-kepler/        (1인 flat)
[목표 v2]  season-1-ancient/unit-06/
                            ├─ kepler/   (기존 8-STEP 산출물 이동)
                            └─ boyle/    (확장 신규)
```
- 같은인물 중복 접미사(`unit-08-euclid-construction`, `unit-12-archimedes-volume`)는 2단화 시 불필요 → `unit-08/euclid/`, `unit-12/archimedes/`.

### 2-b. 배포 `mid1/story/`
```
[현재 v1]  story/unit06/index.html      → ../_video/unit06.mp4   (단원 단위 1영상)
[목표 v2]  story/unit06/index.html      = 인물 2~3인 목록 + 감싼 설명(단계 4)
           story/unit06/kepler/ , boyle/ → 각 player
           _video/unit06-kepler.mp4 , unit06-boyle.mp4
```
- 수학앱 `mid1/math1/NN_slug/index.html` 의 "▶ 이야기" 버튼은 `story/unitNN/index.html`(목록)으로 연결 → 자동 다인물 대응.

---

## 3. 정합성 규칙

1. 인물 추가/변경은 **meta.json `persons[]` 먼저** → `python 70_tools/build_connections.py` 재생성 → 배포 복사.
2. `person-slug` = meta `ref` 값(kebab, 영문). 디렉토리·파일명에 이 slug 사용.
3. `connections.json` 의 `persons[]`·`primary-person` 은 meta 에서 자동 파생(수기 편집 금지).
4. 검증: `build_connections.py` 재생성 후 `git diff` 무변화 = 정합.
