# -*- coding: utf-8 -*-
"""verify_exam2.py — 중2 모의고사 문항 풀(exam.json)이 EXAM_SPEC2.md 를 지키는지 기계적으로 검사한다.

사용:
    python verify_exam2.py            # 있는 단원 전부
    python verify_exam2.py u03 u07    # 지정한 단원만
"""
import json, io, os, re, sys
from collections import Counter

BANK = 'C:/Kids/math-story-telling/30_content/problem_bank/math2/'

# EXAM_SPEC2.md §6 할당표 — 단원: (선택형, 단답, 서술, L, M, H)
PLAN = {
    1:  (8, 2, 2, 4, 5, 3), 2:  (8, 2, 2, 5, 4, 3), 3:  (8, 2, 2, 4, 5, 3),
    4:  (9, 1, 2, 4, 5, 3), 5:  (8, 1, 3, 5, 4, 3), 6:  (8, 2, 2, 4, 5, 3),
    7:  (8, 2, 2, 5, 5, 2), 8:  (9, 1, 2, 5, 4, 3), 9:  (8, 2, 2, 4, 5, 3),
    10: (8, 1, 3, 5, 5, 2), 11: (8, 2, 2, 4, 5, 3),
}
UNIT_NAMES = {
    1: '유리수와 순환소수', 2: '식의 계산', 3: '일차부등식', 4: '연립일차방정식',
    5: '일차함수와 그래프', 6: '일차함수와 일차방정식', 7: '삼각형의 성질',
    8: '사각형의 성질', 9: '도형의 닮음', 10: '피타고라스 정리', 11: '확률',
}
# 중2 과정 밖 — 발문·풀이에 나오면 안 되는 말
BANNED_TOPIC = [ '이차방정식', '이차함수', '근의 공식', '판별식', '삼각비',
                'sin', 'cos', 'tan', '원주각', '표준편차', '분산', '미분', '적분', '로그']
BANNED_MARKUP = ['$', '\\frac', '\\(', '\\)', '□', 'KaTeX']
REQUIRED = ['id', 'format', 'level', 'topic', 'source_id', 'stem_print', 'answer_print',
            'answer_accept', 'answer_unit', 'answer_format', 'figure', 'hint', 'solution',
            'work_space', 'misconceptions']

errors = []
def bad(unit, pid, msg):
    errors.append('u%02d %s — %s' % (unit, pid or '-', msg))

def check_unit(u):
    path = BANK + 'u%02d/exam.json' % u
    if not os.path.exists(path):
        bad(u, None, '파일 없음'); return None
    d = json.load(io.open(path, encoding='utf-8'))
    m, ps = d.get('meta', {}), d.get('problems', [])
    if m.get('grade') != 'math2': bad(u, None, 'meta.grade')
    if m.get('unit') != u: bad(u, None, 'meta.unit')
    if m.get('unit_name') != UNIT_NAMES[u]: bad(u, None, 'meta.unit_name = %r' % m.get('unit_name'))

    nc, ns, ne, nL, nM, nH = PLAN[u]
    fmt = Counter(p.get('format') for p in ps)
    lv = Counter(p.get('level') for p in ps)
    if fmt['choice5'] != nc: bad(u, None, '선택형 %d개 (기대 %d)' % (fmt['choice5'], nc))
    if fmt['short'] != ns:   bad(u, None, '단답 %d개 (기대 %d)' % (fmt['short'], ns))
    if fmt['essay'] != ne:   bad(u, None, '서술 %d개 (기대 %d)' % (fmt['essay'], ne))
    if (lv['L'], lv['M'], lv['H']) != (nL, nM, nH):
        bad(u, None, '난이도 L%d M%d H%d (기대 L%d M%d H%d)' % (lv['L'], lv['M'], lv['H'], nL, nM, nH))

    ids = [p.get('id') for p in ps]
    if len(set(ids)) != len(ids): bad(u, None, 'id 중복')
    for p in ps:
        pid = p.get('id', '?')
        if not re.match(r'^e%02d-(c[1-9]|s[12]|e[123])$' % u, pid or ''):
            bad(u, pid, 'id 형식')
        for k in REQUIRED:
            if k not in p: bad(u, pid, '필드 없음 %s' % k)
        if p.get('source_id') is not None: bad(u, pid, 'source_id 는 항상 null')
        if p.get('figure') is not None:    bad(u, pid, 'figure 는 항상 null')
        if p.get('level') not in ('L', 'M', 'H'): bad(u, pid, 'level')
        if p.get('work_space') not in ('sm', 'md', 'lg'): bad(u, pid, 'work_space')

        blob = ' '.join(str(p.get(k, '')) for k in
                        ('stem_print', 'solution', 'hint', 'answer_print')) + ' '.join(p.get('choices') or [])
        for w in BANNED_MARKUP:
            if w in blob: bad(u, pid, '금지 표기 %r' % w)
        for w in BANNED_TOPIC:
            if w in blob: bad(u, pid, '과정 밖 용어 %r' % w)
        # 다항식의 인수분해는 중3 과정 — 다만 '소인수분해'(중1)는 정상이므로 앞 글자를 확인한다
        for mm in re.finditer(r'인수분해', blob):
            if not blob[max(0, mm.start()-1):mm.start()].endswith('소'):
                bad(u, pid, "과정 밖 용어 인수분해")
                break
        # ASCII 하이픈으로 쓴 음수 (a - b 처럼 뺄셈 기호도 U+2212 로 통일)
        if re.search(r'[\s(]-\d', blob): bad(u, pid, 'ASCII 하이픈 음수 — U+2212 로')
        # 발문 어미
        st = re.sub(r'<[^>]+>', '', p.get('stem_print', '')).strip()
        if not re.search(r'(시오\.|은\?|는\?|면\?|가요\?|까요\?|무엇\?)$', st):
            bad(u, pid, '발문 어미: …%s' % st[-14:])
        # 해설 어투 — 문어체 종결 금지
        sol = re.sub(r'<[^>]+>', '', p.get('solution', ''))
        for w in ('한다.', '된다.', '이다.', '같다.', '구한다.', '아니다.'):
            if w in sol: bad(u, pid, '문어체 종결 %r' % w)
        if len(sol) < 25: bad(u, pid, 'solution 이 너무 짧음')
        if not p.get('hint'): bad(u, pid, 'hint 없음')

        f = p.get('format')
        if f == 'choice5':
            ch = p.get('choices') or []
            if len(ch) != 5: bad(u, pid, '보기 %d개' % len(ch))
            if len(set(ch)) != len(ch): bad(u, pid, '보기 중복')
            ac = p.get('answer_choice')
            if not isinstance(ac, int) or not (1 <= ac <= 5): bad(u, pid, 'answer_choice')
            elif p.get('answer_print') != ch[ac - 1]: bad(u, pid, 'answer_print 가 정답 보기와 다름')
            if len(p.get('distractor_why') or []) != 4: bad(u, pid, 'distractor_why 4개')
            if p.get('answer_accept') is not None: bad(u, pid, 'choice5 는 answer_accept null')
            for c in ch:
                if re.search(r'(정답 없음|모두 고르|없다)', c): bad(u, pid, '금지 보기 %r' % c)
        elif f == 'essay':
            rb = p.get('rubric') or []
            if not (2 <= len(rb) <= 3): bad(u, pid, 'rubric 단계 %d' % len(rb))
            if sum(r.get('points', 0) for r in rb) != 8: bad(u, pid, 'rubric 합계 8점 아님')
            if p.get('work_space') != 'lg': bad(u, pid, 'essay 는 work_space lg')
            if '풀이 과정을 함께 쓰시오' not in p.get('stem_print', ''):
                bad(u, pid, 'essay 발문에 "풀이 과정을 함께 쓰시오" 없음')
        elif f == 'short':
            if p.get('choices') is not None: bad(u, pid, 'short 는 choices null')

    # 정답 위치가 한쪽으로 몰리지 않게
    pos = Counter(p['answer_choice'] for p in ps if p.get('format') == 'choice5' and p.get('answer_choice'))
    for k, v in pos.items():
        if v > 3: bad(u, None, '정답 위치 %d번이 %d회 (3회 이하로)' % (k, v))
    # 유형(topic) 다양성
    topics = set(p.get('topic') for p in ps)
    if len(topics) < 5: bad(u, None, 'topic 이 %d가지뿐' % len(topics))
    return (fmt, lv)

want = [int(a[1:]) for a in sys.argv[1:] if re.match(r'^u\d+$', a)] or sorted(PLAN)
tot = Counter()
seen = 0
for u in want:
    r = check_unit(u)
    if r:
        seen += 1
        tot.update(r[0]); tot.update(r[1])

print('검사한 단원 %d개' % seen)
if seen == len(PLAN):
    print('합계 — 선택형 %d · 단답 %d · 서술 %d / L%d M%d H%d (기대 90·18·24 / L49 M52 H31)'
          % (tot['choice5'], tot['short'], tot['essay'], tot['L'], tot['M'], tot['H']))
    if (tot['choice5'], tot['short'], tot['essay']) != (90, 18, 24): errors.append('전체 format 합계 불일치')
    if (tot['L'], tot['M'], tot['H']) != (49, 52, 31): errors.append('전체 난이도 합계 불일치')

if errors:
    print('\n실패 %d건' % len(errors))
    for e in errors[:40]:
        print('  ', e)
    sys.exit(1)
print('PASS')
