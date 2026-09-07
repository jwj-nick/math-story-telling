# -*- coding: utf-8 -*-
"""selftest_smoke_all.py — smoke_all.js 가 실제로 결함을 잡는지 확인한다.

    python 70_tools/qa/selftest_smoke_all.py <스크래치>/node_modules

결함을 하나씩 일부러 심고, 스모크가 잡아내는지 본다. 잡지 못하면 검사가 무른 것이다.
**스모크를 손댈 때마다 이걸 먼저 돌린다** — 가짜 경보를 없애다 진짜를 놓치기 쉽다.

심는 결함
  ① 클릭했을 때 터지는 코드  — 놀이터에서 나온 `classList.add('')` 와 같은 종류
  ② 없는 파일을 가리키는 링크
  ③ 중복 id
  ④ 안내 문구의 문어체 종결

한계도 적어 둔다 — `classList.add('')` 처럼 **특정 답을 골랐을 때만** 터지는 결함은
버튼을 누르는 순서와 문제 데이터에 달려 있어 이 그물에 걸리지 않을 수 있다.
그런 종류는 페이지 종류별 스모크(smoke_playground · smoke_pn · smoke_dnp)가 답을 직접 넣어 확인한다.
"""
import io
import os
import subprocess
import sys

ROOT = 'C:/Kids/math-story-telling/'
TARGET = ROOT + '40_grades/middle/math2/app2/g3.html'
NODE_PATH = sys.argv[1] if len(sys.argv) > 1 else ''


def run(grade='math2'):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    if NODE_PATH:
        env['NODE_PATH'] = NODE_PATH
    r = subprocess.run(['node', '70_tools/qa/smoke_all.js', grade],
                       capture_output=True, encoding='utf-8', errors='replace', cwd=ROOT, env=env)
    return (r.stdout or '') + (r.stderr or '')


def inject(orig, kind):
    """결함을 하나 심은 HTML 을 돌려준다."""
    if kind == 'click':
        # 어떤 버튼을 누르든 반드시 터지도록, 문서 전체에 클릭 리스너를 하나 건다
        return orig.replace('</body>',
                            "<script>document.addEventListener('click',function(){"
                            "document.body.classList.add('');});</script>\n</body>", 1)
    if kind == 'link':
        return orig.replace('</body>', '<a href="없는파일-자체검사.html">x</a>\n</body>', 1)
    if kind == 'dupid':
        return orig.replace('</body>', '<div id="prog"></div><div id="prog"></div>\n</body>', 1)
    if kind == 'voice':
        return orig.replace('</body>', '<p class="tip">이렇게 쓰면 안 된다.</p>\n</body>', 1)
    raise SystemExit('!! 모르는 결함 종류: %s' % kind)


CASES = [
    ('click', '클릭했을 때 터지는 코드'),
    ('link', '없는 파일을 가리키는 링크'),
    ('dupid', '중복 id'),
    ('voice', '안내 문구의 문어체 종결'),
]

orig = io.open(TARGET, encoding='utf-8').read()
base = run()
clean = 'ALL PASS' in base
print('먼저 멀쩡한 상태 → %s' % ('통과' if clean else '이미 실패가 있어요 (아래 자체 검사가 무의미해요)'))
if not clean:
    print([l for l in base.splitlines() if '실패' in l][:1])

bad = 0
for kind, label in CASES:
    io.open(TARGET, 'w', encoding='utf-8').write(inject(orig, kind))
    out = run()
    io.open(TARGET, 'w', encoding='utf-8').write(orig)      # 반드시 원상 복구
    caught = 'ALL PASS' not in out
    print('%-4s %-28s → %s' % ('OK' if caught else 'X', label, '잡음' if caught else '못 잡음'))
    if not caught:
        bad += 1

# 원상 복구가 됐는지 마지막으로 확인
assert io.open(TARGET, encoding='utf-8').read() == orig, '!! 원상 복구 실패'
print('\n자체 검사 %s' % ('통과' if not bad else '실패 %d건 — 검사가 무릅니다' % bad))
raise SystemExit(1 if bad else 0)
