<!-- TODO_video_deploy_encoding.md / 영상 배포·인코딩 후속 (1차에서 분리) -->

# TODO — 영상 배포 인코딩 최적화 (옵션 1·3)

> 1차 배포는 **원본 mp4 그대로 커밋**(Nick 결정 2026-05-31). 본 문서는 후속 최적화 2안 기록.
> Nick = 20년 video codec IP HW 엔지니어 → 전문 수준으로 기술.

## 현재 인코딩 실측 (render_compile.py libx264 crf18 → `-c:v copy` mux)
| 항목 | 값 |
|---|---|
| Video | H.264 **High@L3.1**, 1280×720p25 CFR, yuv420p(8b 4:2:0) |
| Rate control | **CRF 18** (캡 없는 constant quality), 실측 평균 ~1.28 Mbps |
| GOP | B-frames=2 reorder(x264 기본 bframes≈3 피라미드), IDR keyint 기본 250(=10s)+scenecut |
| Color | primaries/trc/matrix **untagged** (플레이어 추정 — bt601/709 모호) |
| Audio | AAC-LC 44.1k **mono** ~143–192 kbps (음성 mono엔 과투자) |
| Container | MP4, **faststart 미설정** → moov atom 말미 → 웹 전체 다운로드 후 재생 |
| 합계 | 13편 ~279MB (편당 11~30MB, 콘텐츠 의존) |

## 옵션 1 — 웹 최적화 재인코딩 (권장 후속)
목표: 모바일 즉시재생 + repo·전송량 절감, 호환성 유지.

```
ffmpeg -i 8-final.mp4 \
  -c:v libx264 -profile:v high -level 4.0 -preset slow -crf 23 \
  -pix_fmt yuv420p -g 50 -keyint_min 50 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 112k -ac 1 \
  -movflags +faststart  web/unitNN.mp4
```
- **코덱 유지 = H.264 High**: 전 스마트폰 HW decode 보편 보장(1차 핵심=딸 폰 즉시). HEVC/Main10·AV1 대비 호환 리스크 0.
- **CRF 18→23**: painterly·저모션·정적 다이어그램 콘텐츠는 720p에서 지각상 near-transparent. +6 CRF ≈ 비트레이트 절반. 예상 ~0.5–0.7 Mbps → **~7–10MB/편 (합 ~110MB)**.
- **+faststart**: moov atom 선두 이동 → progressive(부분 다운로드 재생). 코덱과 무관한 최대 모바일 UX 이득.
- **GOP 50(2s)**: seek 응답·미래 HLS/DASH 패키징 대비(단일 progressive엔 필수 아님).
- **bt709 태깅**: untagged 색공간 모호 제거.
- **AAC mono 112k + (-ac 1)**: 음성 transparent, 192k→112k 절감.

### HEVC/AV1 평가 (1차 부적합, 미래 옵션)
- **H.265/HEVC Main**: 동일 화질 ~40–50% 절감. iOS/Safari OK, 최신 안드로이드 대부분 HW decode OK이나 일부 안드로이드 브라우저 `<video>` mp4/hevc 재생 불안정 + GitHub Pages MIME. → 호환 리스크로 1차 제외.
- **AV1**: 최고 압축이나 대다수 폰 SW decode = 발열·배터리, 인코딩 느림. 단편 교육영상엔 과투자.
- 결론: 보편 배포는 **H.264 High + faststart**, 화질 마스터는 crf18 원본 보존.

## 옵션 3 — YouTube 비공개 + 임베드
- 13편 YouTube 미등록(unlisted) 업로드 → 앱에서 `<iframe>`/lite-embed.
- 장점: repo 0 부담, CDN 적응형 스트리밍, 로딩 빠름. 단점: **Nick 업로드 작업 필요** + 앱이 외부(YouTube) 의존 + 광고·추천 노출 가능성(unlisted는 추천 제한적).
- 적합 시점: 시리즈 공개 출판/채널화 단계(3차 이후). Nick_TODO T5(출판 채널)와 연계.

## 결정 로그
- 2026-05-31: 1차 = 원본 커밋. 옵션1·3 = 후속. (Nick)
