# -*- coding: utf-8 -*-
"""고친 check_page.py 가 진짜 결함은 여전히 잡는지 확인한다.
   가짜 경고를 없애면서 검사가 물러지면 아무 소용이 없다."""
import io, os, re, subprocess, sys, tempfile

TOOL = 'C:/Kids/math-story-telling/70_tools/qa/check_page.py'
SRC = 'C:/Kids/math-story-telling/40_grades/middle/math2/app2/'
d = tempfile.mkdtemp(prefix='cpself_')
base = io.open(SRC + 'd1p.html', encoding='utf-8').read()
# 엔진도 같이 두어야 캐시버전 검사가 조용하다
for f in ['concept.css', 'concept.js']:
    io.open(d + '/' + f, 'w', encoding='utf-8').write(io.open(SRC + f, encoding='utf-8').read())

CASES = [
    ('멀쩡한 원본', base, False, None),
    ('출력 id 를 없앰', base.replace('id="o1"', 'id="o1-오타"', 1), True, "출력 id 'o1' 없음"),
    ('버튼 id 를 없앰', base.replace('<button id="b1">', '<button>', 1), True, '채점하는 버튼을 찾지 못함'),
    ('없는 id 를 참조', base.replace("MJ.check('a1'", "MJ.check('a1-없음'", 1), True, "참조 id 없음"),
]

bad = 0
for name, html, should_fail, needle in CASES:
    p = d + '/t.html'
    io.open(p, 'w', encoding='utf-8').write(html)
    r = subprocess.run([sys.executable, TOOL, p], capture_output=True, encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    failed = ('문제 0건' not in out)
    okc = (failed == should_fail) and (not needle or needle in out)
    print('%-4s %-16s → %s' % ('OK' if okc else 'X', name, '잡음' if failed else '통과'))
    if not okc:
        bad += 1
        print('     기대=%s / 찾던 문구=%s' % ('잡아야 함' if should_fail else '통과해야 함', needle))
        print('     ' + '\n     '.join(l for l in out.splitlines() if l.strip())[:400])

for f in os.listdir(d):
    os.remove(d + '/' + f)
os.rmdir(d)
print('\n자체 검사 %s' % ('통과' if not bad else '실패 %d건' % bad))
raise SystemExit(1 if bad else 0)
