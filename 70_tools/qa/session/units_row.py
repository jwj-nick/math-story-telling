import io, sys
# usage: units_row.py <N> <name> <date>  — UNITS.md 진행 현황에 N행 삽입, "N+1~12" 준비 중 행으로 갱신
n = int(sys.argv[1]); name = sys.argv[2]; date = sys.argv[3]
p = 'C:/Kids/math-story-telling/40_grades/middle/math3/UNITS.md'
s = io.open(p, encoding='utf-8').read()
old = '| %d~12 | — | — | — | — | — | 준비 중 카드 |' % n
new = '| %d %s | ✅ | ✅ | ✅ 21 | ✅ | ✅ a/b/c/mock 8장 | ✅ %s |' % (n, name, date)
if n < 12:
    new += '\n| %d~12 | — | — | — | — | — | 준비 중 카드 |' % (n + 1)
assert old in s, 'marker row not found: ' + old
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('UNITS.md: unit %d row added' % n)
