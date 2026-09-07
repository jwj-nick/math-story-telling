# -*- coding: utf-8 -*-
"""check_screen_bank.py — 화면 연습(pN.html)과 문제 은행(practice.json)이 갈라졌는지 본다.

    python 70_tools/qa/check_screen_bank.py math2
    python 70_tools/qa/check_screen_bank.py          # 세 학년 모두

왜 필요한가 (2026-09-08):
  중2 은행을 대폭 보강하면서 화면은 그대로 두어 **유형 수가 어긋나 있었다**(화면 6 · 은행 7).
  화면으로 공부하는 아이는 그 단원의 한 유형을 통째로 만나지 못한다.
  `verify_bank.py` 의 V1·V2 는 추출기가 읽을 수 있는 마크업 세대에서만 돌아 이 어긋남을 놓쳤다.
  이 검사는 마크업을 파싱하지 않고 **유형 제목만** 견주므로 세대에 상관없이 돈다.

무엇을 보는가
  ① 유형 수가 같은가            — 다르면 오류(화면에 없는 유형이 있다는 뜻)
  ② 유형 순서가 맞는가          — 제목을 정규화해 한쪽이 다른 쪽을 품는지로 판정
  ③ 문항 수                     — 화면 3 · 은행 4 처럼 다를 수 있고, 이는 오류가 아니라 알림이다
                                  (종이가 한 문제를 더 주는 것은 해롭지 않다)
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRADES = {
    'math1': ('app1', 13),
    'math2': ('app2', 11),
    'math3': ('app3', 12),
}


def norm(s):
    """제목 비교용. 조사·기호·공백을 걷어내 '삼각형의 세 각의 크기의 합' 과 '세 각의 합' 을 잇는다."""
    s = re.sub(r'<[^>]+>', '', s or '')
    s = re.sub(r'[\s·()（）\[\],．.]', '', s)
    return re.sub(r'(의|을|를|은|는|이|가|와|과)', '', s)


def screen_types(path):
    """화면에서 유형 제목과 문항 수를 읽는다. 마크업 세대마다 이름이 달라 몇 가지를 함께 본다."""
    s = io.open(path, encoding='utf-8').read()
    titles = re.findall(r'class="m-title">(.*?)</span>', s)
    if not titles:
        titles = re.findall(r'class="t-title">(.*?)</span>', s)
    n = s.count('class="pq"') or len(re.findall(r'class="prb', s))
    return [re.sub(r'<[^>]+>', '', t).strip() for t in titles], n


def main():
    want = sys.argv[1:] or list(GRADES)
    errs, notes, checked = [], [], 0
    for g in want:
        if g not in GRADES:
            sys.exit('!! 모르는 학년: %s' % g)
        app, units = GRADES[g]
        for u in range(1, units + 1):
            p = ROOT / '40_grades' / 'middle' / g / app / ('p%d.html' % u)
            b = ROOT / '30_content' / 'problem_bank' / g / ('u%02d' % u) / 'practice.json'
            if not p.exists() or not b.exists():
                notes.append('%s u%02d 건너뜀 (화면 %s · 은행 %s)'
                             % (g, u, '있음' if p.exists() else '없음', '있음' if b.exists() else '없음'))
                continue
            checked += 1
            st, sn = screen_types(p)
            bank = json.loads(b.read_text(encoding='utf-8'))
            bt = [t['title'] for t in bank['types']]
            bn = sum(len(t['problems']) for t in bank['types'])

            if len(st) != len(bt):
                errs.append('%s u%02d 유형 수 불일치 — 화면 %d · 은행 %d%s'
                            % (g, u, len(st), len(bt),
                               ('  (화면에 없는 유형: %s)' % ', '.join(bt[len(st):])) if len(bt) > len(st) else ''))
                continue
            for i, (a, c) in enumerate(zip(st, bt), start=1):
                na, nc = norm(a), norm(c)
                if na != nc and na not in nc and nc not in na:
                    errs.append('%s u%02d 유형%d 짝이 안 맞음 — 화면 "%s" · 은행 "%s"' % (g, u, i, a, c))
            if sn != bn:
                notes.append('%s u%02d 문항 수 화면 %d · 은행 %d (종이가 더 주는 것은 괜찮다)' % (g, u, sn, bn))

    for x in notes:
        print('  · ' + x)
    for x in errs:
        print('  ✗ ' + x)
    print('\n%d단원 점검 — %s' % (checked, ('불일치 %d건' % len(errs)) if errs else '유형 구성 일치'))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
