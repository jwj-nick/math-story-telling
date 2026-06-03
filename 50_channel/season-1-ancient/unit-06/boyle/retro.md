<!-- 50_channel/season-1-ancient/unit-06/boyle/retro.md -->
# retro — unit 06 보일 (단계 3 파일럿)

- **유형**: 기존 단원(u06 정비례·반비례)의 secondary 인물. primary=케플러(이미 완성).
- **산출**: 8-final.mp4 152s / 1280×720 / 6장면 / 신규 캐릭터(ref-boyle) / 한 단어=**측정**.
- **개념 각도**: 케플러=천체·면적속도 / 보일=기체·압력×부피(P×V=k → y=k/x). 같은 반비례를 실험·측정 각도로 보완. 딸 약점(반비례) 2번째 시각.
- **서사 연속성**: 케플러 영상 S5 카메오(보일=공기 압축)를 자기 이야기로 확장 + 같은 시대 callback.
- **voice**: 케플러 영상과 다른 pairing(구분감).
- **품질 게이트**: 포스터 멀티모달 검증 — 17C 왕립학회 서재, 진공펌프·유리관, ruff collar, 반비례 곡선, 자막 "곱하면 일정=반비례 y=k/x". 시대고증·캐릭터·수학표기 OK.

## 파일럿으로 검증된 단계 3 flow (재현용)
1. Phase A: meta secondary 추출 → `git mv unit-NN-<primary> unit-NN/<primary>` + `unit-NN/<secondary>/` 생성.
2. Phase B: se-video-orchestrator (secondary 각도·다른 voice·신규/재사용 캐릭터).
3. Phase C: 포스터/장면 멀티모달 품질 게이트(+개념 정합).
4. Phase D: 8-final → 배포 `_video/unitNN-<secondary>.mp4` faststart + `story/unitNN/index.html` 2인 chooser.
5. Phase E: retro + manifest.

## 다음 배치 메모
- **캐릭터 재사용**(저비용): u02·u04 알콰리즈미(←u03), u09·u11 케플러(←u06) — 기존 5-images reference 전달.
- **신규 캐릭터**(7편): u03 비에트·u05 페르마·u07 탈레스·u08 가우스·u10 유휘·u12 카발리에리·u13 플레이페어.
- orchestrator 호출은 tool-result internal error가 떠도 실제 산출은 완주됨(이번 사례) — 산출물 ls로 확인할 것.
- 배포 chooser는 현재 단순 2버튼 = 단계 4(감싼 설명)에서 인물 소개·연결 서술로 확장.
