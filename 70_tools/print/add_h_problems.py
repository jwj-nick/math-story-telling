# -*- coding: utf-8 -*-
"""add_h_problems.py — 단원 p 페이지 + 문제은행에 유형당 심화(H) 문항 1개를 4번째로 추가하고
심화 모의고사 회차(quota H:1) config 를 만든다 (math1 Round 15 방식, math3 부터 도구화).

    python 70_tools/print/add_h_problems.py <spec.json>

spec.json:
{
  "grade": "math3", "unit": 9, "unit_name": "원과 직선",
  "problems": [
    {"type": 1, "stem": "…앱 발문(HTML)…", "ans": "6", "disp": "6", "inputmode": "numeric",
     "why": "…왜? 박스(HTML)…", "expr": "(13+14-15)/2",
     "stem_print": "…지면 발문…", "answer_atoms": ["6"], "answer_print": "6", "answer_accept": [],
     "answer_unit": null, "answer_format": "자연수로", "hint": "…", "solution": "…",
     "work_space": "md", "misconceptions": ["…"]}
  ]
}
- p{N}.html: 각 유형 section 끝에 chips(심화·도전) + .pq (4) 삽입, prob('cN',[P('bN4','aN4',ans,'oN4','disp')],'wN4') 추가,
  TYPES 3→4, TOTAL 21→28, "/ 21" → "/ 28".
- practice.json: 각 유형 problems 에 H 문항 append (id m3-uNN-tNN-04).
- sets/m3-uNN-d.json: kind mock, quota {H:1}, "<단원명> 심화 모의고사".
재실행 방지: 이미 aN4 가 있으면 중단.
"""
import io, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    grade, unit = spec['grade'], int(spec['unit'])
    g = grade[-1]; nn = '%02d' % unit
    app = ROOT / '40_grades' / 'middle' / grade / ('app' + g)
    page = app / ('p%d.html' % unit)
    html = io.open(page, encoding='utf-8').read()
    if 'id="a14"' in html:
        raise SystemExit('이미 심화 문항이 있음: ' + str(page))
    probs = spec['problems']
    if len(probs) != 7 or sorted(p['type'] for p in probs) != [1, 2, 3, 4, 5, 6, 7]:
        raise SystemExit('유형 1~7 각 1문항이어야 함')

    # 1) 섹션에 4번째 문항 삽입
    for p in probs:
        n = p['type']
        start = html.find('<section class="mission reveal" id="c%d">' % n)
        if start < 0:
            raise SystemExit('section c%d 없음' % n)
        end = html.find('</section>', start)
        im = p.get('inputmode', 'numeric')
        block = ('    <div class="chips" style="margin:14px 0 4px"><span class="chip principle">심화</span><span class="chip lv3">도전</span></div>\n'
                 '    <div class="pq"><p class="ask"><span class="qi">(4)</span>' + p['stem'] + '</p>\n'
                 '      <div class="row"><input class="num" id="a%d4" inputmode="%s" style="width:80px" aria-label="답"><button id="b%d4">확인</button></div><div class="out" id="o%d4"></div>\n' % (n, im, n, n)
                 + '      <div class="why" id="w%d4" style="display:none"><span class="why-h">왜?</span>' % n + p['why'] + '</div></div>\n')
        ws = end
        while ws > 0 and html[ws - 1] in ' \t':
            ws -= 1
        html = html[:ws] + block + '  </section>' + html[end + len('</section>'):]

    # 2) prob 라인
    lines = ''.join("  prob('c%d',[P('b%d4','a%d4',%s,'o%d4','%s')],'w%d4');\n"
                    % (p['type'], p['type'], p['type'], p['ans'], p['type'], p['disp'].replace("'", "\\'"), p['type'])
                    for p in sorted(probs, key=lambda x: x['type']))
    marker = '\n})();\n</script>'
    idx = html.rfind(marker)
    if idx < 0:
        raise SystemExit('script 끝 마커 없음')
    html = html[:idx] + '\n' + lines.rstrip('\n') + html[idx:]

    # 3) TYPES / TOTAL
    html, n1 = re.subn(r'var TYPES=\{c1:3,c2:3,c3:3,c4:3,c5:3,c6:3,c7:3\}, TOTAL=21;',
                       'var TYPES={c1:4,c2:4,c3:4,c4:4,c5:4,c6:4,c7:4}, TOTAL=28;', html)
    html, n2 = re.subn(r'(<b id="score">0</b> / )21', r'\g<1>28', html)
    if n1 != 1 or n2 != 1:
        raise SystemExit('TYPES/TOTAL 치환 실패 (%d, %d)' % (n1, n2))
    io.open(page, 'w', encoding='utf-8', newline='\n').write(html)

    # 4) practice.json
    bank_p = ROOT / '30_content' / 'problem_bank' / grade / ('u' + nn) / 'practice.json'
    bank = json.loads(bank_p.read_text(encoding='utf-8'))
    by_no = {t['no']: t for t in bank['types']}
    for p in probs:
        t = by_no[p['type']]
        if any(x['level'] == 'H' for x in t['problems']):
            raise SystemExit('은행에 이미 H 문항: 유형 %d' % p['type'])
        entry = {
            'id': 'm%s-u%s-t%02d-04' % (g, nn, p['type']),
            'level': 'H',
            'stem_src': re.sub(r'<[^>]+>', '', p['stem']),
            'stem_print': p['stem_print'],
            'answer_atoms': p['answer_atoms'],
            'answer_print': p['answer_print'],
            'answer_accept': p.get('answer_accept', []),
            'answer_unit': p.get('answer_unit'),
            'answer_format': p['answer_format'],
            'figure': None,
            'hint': p['hint'],
            'solution': p['solution'],
            'work_space': p.get('work_space', 'md'),
            'misconceptions': p.get('misconceptions', []),
        }
        t['problems'].append(entry)
    bank['meta']['h_added'] = spec.get('date', '2026-08-30')
    bank_p.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # 5) 심화 모의고사 회차
    sets_dir = ROOT / '30_content' / 'problem_bank' / 'sets'
    cfg = {
        'id': 'm%s-u%s-d' % (g, nn),
        'kind': 'mock',
        'grade': grade,
        'unit': unit,
        'unit_name': spec['unit_name'],
        'title': spec['unit_name'].replace(' ', '') + ' 심화 모의고사',
        'subtitle': '7유형 심화 통합 · 유형마다 도전 1문항 · 7문항',
        'bank': '%s/u%s/practice.json' % (grade, nn),
        'misconceptions': 'misconceptions/%s_u%s.json' % (grade, nn),
        'types': [1, 2, 3, 4, 5, 6, 7],
        'pick': {'quota': {'H': 1}},
        'time_min': 20,
        'outputs': ['Q', 'K'],
        'columns': 2,
    }
    (sets_dir / (cfg['id'] + '.json')).write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('u%s: p%d.html +7 H, practice.json +7, set %s' % (nn, unit, cfg['id']))


if __name__ == '__main__':
    main()
