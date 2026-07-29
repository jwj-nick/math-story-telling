"""extract_gen_ac.py — 중1 유형앱(type_NN_app.html) → 문제 은행 draft(JSON)

두 마크업 세대를 자동 판별한다.
  세대 A (단원 03~12) : .card.lv-{L|M|H} + .q-text + #h-XX(힌트) + #s-XX(정답·풀이)
                        정답 = .sol-panel 의 첫 <strong>
  세대 C (단원 13)    : .q-card + .q-num("L1") + .q-body + #L1h(힌트) + #L1a(정답)
                        정답 = .ans

⚠️ 중1 자료는 KaTeX 문법($...$)을 쓴다. 지면은 CDN 없이 HTML <sup>/유니코드/.frac 을 쓰므로
   stem_print 를 쓸 때 사람이(또는 저작 에이전트가) 변환해야 한다. 여기서는 원문 그대로 넘긴다.

사용:
    python extract_gen_ac.py <problems_dir> <단원번호> <출력JSON경로>
"""
import json
import re
import sys
from pathlib import Path


def slice_balanced_div(html, start):
    open_tag_end = html.index('>', start)
    depth, i = 1, html.index('>', start) + 1
    body_start = i
    while depth > 0:
        nxt_open = html.find('<div', i)
        nxt_close = html.find('</div>', i)
        if nxt_close == -1:
            return html[body_start:], len(html)
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open + 4
        else:
            depth -= 1
            if depth == 0:
                return html[body_start:nxt_close], nxt_close + 6
            i = nxt_close + 6
    return html[body_start:], len(html)


def strip_tags(s):
    # ⚠️ <[^>]+> 로 지우면 부등식 "$a < 0, b > 0$" 의 "< 0, b >" 를 태그로 오인해 먹는다.
    #    태그 이름은 반드시 영문자·/·! 로 시작하므로 그 조건을 건다.
    s = re.sub(r'<[a-zA-Z/!][^>]*>', ' ', s or '')
    return re.sub(r'\s+', ' ', s).strip()


def panel_map(html, pattern):
    """id -> 내부 HTML (짝 맞는 </div> 까지)"""
    out = {}
    for m in re.finditer(pattern, html):
        body, _ = slice_balanced_div(html, m.start())
        out[m.group(1)] = body.strip()
    return out


def title_of(html, fallback):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    if m:
        return strip_tags(m.group(1))
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return strip_tags(m.group(1)) if m else fallback


def inner_div(body, cls):
    """카드 본문 안에서 class 가 cls 인 div 의 내부 HTML. id 접두어가 단원마다 다르므로
    id 로 찾지 않고 클래스로 찾는다 (hint-L1 / h-L1 등 표기 흔들림 흡수)."""
    m = re.search(r'<div class="' + cls + r'"[^>]*>', body)
    if not m:
        return None
    inner, _ = slice_balanced_div(body, m.start())
    return inner.strip() or None


def parse_gen_a(html):
    problems = []
    for m in re.finditer(r'<div class="card lv-([LMH])"', html):
        body, _ = slice_balanced_div(html, m.start())
        lv = m.group(1)
        num = re.search(r'<div class="q-num">(\d+)</div>', body)
        qt = re.search(r'<div class="q-text">(.*?)</div>', body, re.S)
        svg = re.search(r'(<svg\b.*?</svg>)', body, re.S)
        hint_html = inner_div(body, 'hint-panel')
        sol_html = inner_div(body, 'sol-panel') or ''
        # 정답 표기는 두 가지다: <strong>답</strong><br>풀이  또는  정답: 답<br>풀이
        ans = re.search(r'<strong>(.*?)</strong>', sol_html, re.S) \
            or re.search(r'정답\s*[:：]\s*(.*?)(?:<br\s*/?>|$)', sol_html, re.S)
        rest = re.sub(r'^\s*<strong>.*?</strong>\s*(<br\s*/?>)?', '', sol_html, count=1, flags=re.S)
        problems.append({
            'idx': int(num.group(1)) if num else len(problems) + 1,
            'level': lv,
            'ask_html': (qt.group(1).strip() if qt else ''),
            'ask_text': strip_tags(qt.group(1) if qt else ''),
            'figure_svg': (svg.group(1).strip() if svg else None),
            'answer_atoms': [strip_tags(ans.group(1))] if ans else [],
            'answer_html': (ans.group(1).strip() if ans else None),
            'hint_html': hint_html,
            'solution_html': rest.strip() or None,
            'response': 'short',
        })
    return problems


def parse_gen_c(html):
    problems = []
    for m in re.finditer(r'<div class="q-card"', html):
        body, _ = slice_balanced_div(html, m.start())
        qn = re.search(r'<span class="q-num">([^<]+)</span>', body)
        key = qn.group(1).strip() if qn else ''
        lv = re.search(r'<span class="diff ([LMH])"', body)
        qb_html = inner_div(body, 'q-body') or ''
        svg = re.search(r'(<svg\b.*?</svg>)', body, re.S)
        # 카드 안의 panel 들: id 가 …h 면 힌트, …a 면 정답
        pans = {}
        for pm in re.finditer(r'<div class="panel[^"]*" id="([^"]+)"[^>]*>', body):
            inner, _ = slice_balanced_div(body, pm.start())
            pans[pm.group(1)] = inner.strip()
        hint_html = next((v for k, v in pans.items() if k.endswith('h')), None)
        ans_body = next((v for k, v in pans.items() if k.endswith('a')), '')
        ans = re.search(r'<div class="ans">(.*?)</div>', ans_body, re.S)
        rest = re.sub(r'<div class="ans">.*?</div>', '', ans_body, count=1, flags=re.S)
        problems.append({
            'idx': len(problems) + 1,
            'key': key,
            'level': lv.group(1) if lv else (key[0] if key else 'L'),
            'ask_html': qb_html.strip(),
            'ask_text': strip_tags(qb_html),
            'figure_svg': (svg.group(1).strip() if svg else None),
            'answer_atoms': [strip_tags(ans.group(1))] if ans else [],
            'answer_html': (ans.group(1).strip() if ans else None),
            'hint_html': hint_html,
            'solution_html': rest.strip() or None,
            'response': 'short',
        })
    return problems


def parse_gen_b(html):
    """세대 B (중1 01 소인수분해) — .prob-card + .prob-num(class 에 난이도) + .prob-text
    + .ans-content#XX-ans(.ans-box 가 정답) / #XX-hint(.hint-box 가 힌트)"""
    problems = []
    for m in re.finditer(r'<div class="prob-card"[^>]*>', html):
        body, _ = slice_balanced_div(html, m.start())
        num = re.search(r'<div class="prob-num ([LMH])">(\d+)</div>', body)
        qt = re.search(r'<div class="prob-text">(.*?)</div>', body, re.S)
        svg = re.search(r'(<svg\b.*?</svg>)', body, re.S)
        ids = re.findall(r"toggleAns\(this,\s*'([^']+)'\)", body)
        panels = {}
        for pm in re.finditer(r'<div class="ans-content" id="([^"]+)"[^>]*>', body):
            inner, _ = slice_balanced_div(body, pm.start())
            panels[pm.group(1)] = inner.strip()
        aid = next((i for i in ids if i.endswith('-ans')), None)
        hid = next((i for i in ids if i.endswith('-hint')), None)
        ans_body = panels.get(aid, '')
        box = inner_div(ans_body, 'ans-box')
        rest = re.sub(r'<div class="ans-box">.*?</div>', '', ans_body, count=1, flags=re.S) if box else ans_body
        hint_body = panels.get(hid, '')
        hbox = inner_div(hint_body, 'hint-box') or hint_body
        problems.append({
            'idx': len(problems) + 1,
            'level': num.group(1) if num else 'L',
            'ask_html': (qt.group(1).strip() if qt else ''),
            'ask_text': strip_tags(qt.group(1) if qt else ''),
            'figure_svg': (svg.group(1).strip() if svg else None),
            'answer_atoms': [strip_tags(box)] if box else [],
            'answer_html': box,
            'hint_html': hbox or None,
            'solution_html': rest.strip() or None,
            'response': 'short',
        })
    return problems


def parse_gen_e(html):
    """세대 E (중1 02 정수와 유리수) — .q-card + .q-num("L-1") + .q-text
    + 객관식 .choices(mc(this,true) 가 정답) 또는 단답 input#inXX(checkXX() 안의 비교 리터럴)"""
    # 함수 본문을 중괄호로 끊으면 포맷 흔들림에 약하다. 다음 function 선언까지를 본문으로 본다.
    checks = {}
    heads = [(m.group(1), m.end()) for m in re.finditer(r"function\s+check([A-Za-z0-9]+)\s*\(", html)]
    starts = [m.start() for m in re.finditer(r"\bfunction\s+", html)] + [len(html)]
    for key, pos in heads:
        nxt = next((s for s in starts if s > pos), len(html))
        bodyjs = html[pos:nxt]
        lits = (re.findall(r"===\s*'([^']*)'", bodyjs)
                or re.findall(r"\[\s*'([^']*)'", bodyjs)
                or re.findall(r"includes\(\s*'([^']*)'", bodyjs)
                or re.findall(r"==\s*'([^']*)'", bodyjs))
        if lits:
            checks[key.lower()] = lits[0]
        else:
            nums = re.findall(r"===\s*(-?\d+(?:\.\d+)?)", bodyjs) or re.findall(r"==\s*(-?\d+(?:\.\d+)?)", bodyjs)
            if nums:
                checks[key.lower()] = nums[0]

    problems = []
    for m in re.finditer(r'<div class="q-card"[^>]*>', html):
        body, _ = slice_balanced_div(html, m.start())
        qn = re.search(r'<div class="q-num">\s*([LMH])-?(\d+)', body)
        qt = re.search(r'<div class="q-text">(.*?)</div>', body, re.S)
        svg = re.search(r'(<svg\b.*?</svg>)', body, re.S)

        atoms, choices, response = [], [], 'short'
        ok = re.search(r'<button class="c-btn" onclick="mc\(this,\s*true\)">(.*?)</button>', body, re.S)
        if 'class="choices"' in body:
            response = 'choice'
            choices = [strip_tags(x) for x in
                       re.findall(r'<button class="c-btn"[^>]*>(.*?)</button>', body, re.S)]
            if ok:
                atoms = [strip_tags(ok.group(1))]
        else:
            # ① onclick="finShort('inXX','cbXX','fbXX','정답','메시지')" — 정답이 인라인에 있다
            fs = re.search(r"finShort\(\s*'[^']*'\s*,\s*'[^']*'\s*,\s*'[^']*'\s*,\s*'([^']*)'", body)
            if fs:
                atoms = [fs.group(1).split('|')[0]]
            else:
                # ② <script> 의 checkXX() 안 비교 리터럴
                inp = re.search(r'<input[^>]*id="in([A-Za-z0-9]+)"', body)
                if inp and inp.group(1).lower() in checks:
                    atoms = [checks[inp.group(1).lower()]]

        problems.append({
            'idx': len(problems) + 1,
            'level': qn.group(1) if qn else 'L',
            'ask_html': (qt.group(1).strip() if qt else ''),
            'ask_text': strip_tags(qt.group(1) if qt else ''),
            'figure_svg': (svg.group(1).strip() if svg else None),
            'answer_atoms': atoms,
            'answer_html': (atoms[0] if atoms else None),
            'hint_html': None,
            'solution_html': None,
            'response': response,
            'choices': choices,
        })
    return problems


def main():
    pdir = Path(sys.argv[1])
    unit = int(sys.argv[2])
    dst = Path(sys.argv[3])

    types = []
    for f in sorted(pdir.glob('type_*_app.html')):
        html = f.read_text(encoding='utf-8', errors='replace')
        if 'class="card lv-' in html:
            gen = 'A'
        elif 'class="prob-card"' in html:
            gen = 'B'
        elif 'class="q-card"' in html:
            # 세대 C 는 .q-body + .panel, 세대 E 는 .q-text + .choices/.ans-inp
            gen = 'C' if 'class="q-body"' in html else 'E'
        else:
            gen = '?'
        probs = {'A': parse_gen_a, 'B': parse_gen_b, 'C': parse_gen_c,
                 'E': parse_gen_e}.get(gen, lambda _h: [])(html)
        no = int(re.search(r'type_(\d+)_app', f.name).group(1))
        sub = re.search(r'<div class="sub">(.*?)</div>', html, re.S)
        types.append({
            'no': no,
            'file': f.name,
            'generation': gen,
            'title': title_of(html, f.stem),
            'principle_src': strip_tags(sub.group(1)) if sub else '',
            'problems': probs,
        })

    n_prob = sum(len(t['problems']) for t in types)
    n_noans = sum(1 for t in types for p in t['problems'] if not p['answer_atoms'])
    n_fig = sum(1 for t in types for p in t['problems'] if p['figure_svg'])
    gens = sorted(set(t['generation'] for t in types))

    out = {
        'meta': {
            'grade': 'math1',
            'unit': unit,
            'generation': '+'.join(gens),
            'source': str(pdir).replace('\\', '/'),
            'extractor': 'extract_gen_ac.py',
            'counts': {'types': len(types), 'problems': n_prob,
                       'no_answer': n_noans, 'figures': n_fig},
        },
        'types': types,
    }
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print('gen=%s types=%d problems=%d no_answer=%d figures=%d -> %s'
          % ('+'.join(gens), len(types), n_prob, n_noans, n_fig, dst))


if __name__ == '__main__':
    main()
