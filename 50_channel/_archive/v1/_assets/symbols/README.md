# 90_video/_assets/symbols/

> Story 영상에서 재사용되는 공통 SVG 심볼. 각 심볼은 1:1 viewBox, currentColor 사용.
> 단원별 매핑은 unitNN/index.html의 `{{S2_SYMBOL}}` `{{S3_METAPHOR}}` `{{S4_DIAGRAM}}` 슬롯에 인라인 또는 use 참조.

## 심볼 목록

| 파일 | 의미 | 사용 단원 후보 |
|---|---|---|
| star.svg | 별 (밤하늘, 천문) | 01, 11 |
| scroll.svg | 두루마리 (고대 문서, 도서관) | 01, 04, 07 |
| book.svg | 책 (지식, 학자) | 03, 09 |
| sun.svg | 태양 (햇빛, 그림자, 측정) | 01, 10 |
| compass.svg | 컴퍼스 (작도) | 07, 08 |
| balance.svg | 양팔 저울 (평형, 이항) | 03, 04 |
| coord-axes.svg | 좌표축 | 05, 06 |
| ruler.svg | 자 (측정, 작도) | 07, 08 |
| circle-sector.svg | 부채꼴 | 10, 13 |
| polyhedra.svg | 다면체 | 11, 12 |
| infinity.svg | 무한대 (음수, 무한) | 02 |
| lamp.svg | 등불 (나이팅게일) | 13 |
| sieve-grid.svg | 체 그리드 (소수 찾기) | 01 |
| coxcomb.svg | 코크스콤 차트 | 13 |

## 인라인 vs 외부 참조

HyperFrames는 SVG `<use>`도 처리하지만 안전하게 인라인 권장.
템플릿 주입 단계에서 SVG 본문을 직접 `{{S2_SYMBOL}}` 자리에 삽입.

## 색상 규칙

- 단일 색은 `currentColor` 사용 → CSS `.s2 .visual { color: var(--accent); }` 에서 색 결정
- 다색 필요 시 명시적 색 지정 (단, 단원 팔레트 안에서)
