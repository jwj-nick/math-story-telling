"""extract_math2_p.py — 중2 app2 연습 페이지(p*.html, 마크업 세대 D) → 문제 은행 draft(JSON)

결정적 추출만 한다. 지면 발문(stem_print)·지면 정답(answer_print)은 여기서 만들지 않는다.
정답 원자(answer_atoms)는 script의 P(...) 호출에서 그대로 가져온다 = 검증 기준.

사용:
    python extract_math2_p.py <p파일경로> <단원번호> <출력JSON경로>
"""
import json
import re
import sys
from pathlib import Path


def slice_balanced_div(html, start):
    """start = '<div' 의 인덱스. 짝 맞는 </div> 까지의 (내부HTML, 끝인덱스) 반환."""
    open_tag_end = html.index('>', start)
    depth = 1
    i = open_tag_end + 1
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


def find_divs(html, cls):
    """class="cls" 인 div 들의 내부 HTML 목록."""
    out = []
    for m in re.finditer(r'<div class="' + cls + r'"[^>]*>', html):
        body, _ = slice_balanced_div(html, m.start())
        out.append((m.start(), body))
    return out


def strip_tags(s):
    # ⚠️ <[^>]+> 로 지우면 부등식 "a < 0, b > 0" 의 "< 0, b >" 를 태그로 오인해 먹는다.
    #    태그 이름은 반드시 영문자·/·! 로 시작하므로 그 조건을 건다.
    s = re.sub(r'<[a-zA-Z/!][^>]*>', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def parse_picks(html):
    """script 의 pick('cN', btnOk, btnNo, out, ...) 파싱 → 정답 버튼 id 집합.

    pick() 의 두 번째 인자가 정답 버튼이다. 2지선다는 지면에서 단답형으로 바꿔야 하므로
    여기서는 '정답 선택지의 텍스트'만 원자로 넘긴다.
    """
    ok = {}
    for m in re.finditer(r"pick\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'", html):
        a, b, c = m.group(1), m.group(2), m.group(3)
        if re.fullmatch(r'c\d+', a):          # pick('cN', btnOk, btnNo, out, ...)   — p2 계열
            ok[b] = {'type': a, 'wrong': c}
        else:                                  # pick(btnOk, btnNo, out, pid, type, ...) — p1 계열
            ok[a] = {'wrong': b, 'out': c}
    return ok


def button_labels(html):
    out = {}
    for m in re.finditer(r'<button[^>]*id="([^"]+)"[^>]*>(.*?)</button>', html, re.S):
        out[m.group(1)] = strip_tags(m.group(2))
    return out


def parse_answers(html):
    """script 의 prob('cN',[P(btn,input,ans,out,disp),...],'wXX') 파싱 → input id → (ans, disp)"""
    amap = {}
    probs = []
    for m in re.finditer(r"prob\('(c\d+)'\s*,\s*\[(.*?)\]\s*(?:,\s*'(\w+)')?\s*\)\s*;", html, re.S):
        type_id, parts_src, why_id = m.group(1), m.group(2), m.group(3)
        parts = []
        for p in re.finditer(
            r"P\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*(.+?)\s*,\s*'([^']+)'\s*(?:,\s*'([^']*)'\s*)?\)",
            parts_src,
        ):
            btn, inp, ans, out, disp = p.group(1), p.group(2), p.group(3).strip(), p.group(4), p.group(5)
            parts.append({"input": inp, "ans": ans, "disp": disp if disp is not None else ans})
            amap[inp] = {"ans": ans, "disp": disp if disp is not None else ans}
        probs.append({"type": type_id, "parts": parts, "why": why_id})

    # p1 계열: num(btn, input, ans, out, disp, pid, type, why) — prob()/P() 래퍼 없이 직접 바인딩
    for m in re.finditer(
            r"num\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*(.+?)\s*,\s*'([^']+)'\s*,\s*'([^']*)'", html):
        inp, ans, disp = m.group(2), m.group(3).strip(), m.group(5)
        amap.setdefault(inp, {"ans": ans, "disp": disp if disp else ans})

    # 그 밖의 직접 호출: MJ.check('id', 정답, 'out', {correct:'표시값'})
    for m in re.finditer(
            r"MJ\.check\(\s*'([^']+)'\s*,\s*(.+?)\s*,\s*'([^']+)'\s*,\s*\{[^}]*correct\s*:\s*'([^']*)'", html):
        inp, ans, disp = m.group(1), m.group(2).strip(), m.group(4)
        amap.setdefault(inp, {"ans": ans, "disp": disp if disp else ans})

    return amap, probs


def main():
    src = Path(sys.argv[1])
    unit = int(sys.argv[2])
    dst = Path(sys.argv[3])
    html = src.read_text(encoding='utf-8')

    amap, _probs = parse_answers(html)
    pmap = parse_picks(html)
    blabels = button_labels(html)

    types = []
    for sm in re.finditer(r'<section class="mission[^"]*" id="(c\d+)">(.*?)</section>', html, re.S):
        type_id, body = sm.group(1), sm.group(2)
        no = re.search(r'class="m-no">(\d+)<', body)
        title = re.search(r'class="m-title">(.*?)</span>', body, re.S)
        tip = re.search(r'<p class="tip">(.*?)</p>', body, re.S)
        chips = re.findall(r'<span class="chip[^"]*">(.*?)</span>', body)

        problems = []
        for idx, (_pos, pq) in enumerate(find_divs(body, 'pq'), start=1):
            ask = re.search(r'<p class="ask">(.*?)</p>', pq, re.S)
            ask_html = ask.group(1) if ask else ''
            ask_html = re.sub(r'<span class="qi">.*?</span>', '', ask_html, flags=re.S).strip()
            inputs = re.findall(r'<input[^>]*id="([^"]+)"', pq)
            why = re.search(r'<div class="why" id="(\w+)"[^>]*>(.*?)</div>', pq, re.S)
            atoms = [amap[i]["disp"] for i in inputs if i in amap]
            missing = [i for i in inputs if i not in amap]

            # 2지선다(.picks) — 정답 선택지 텍스트를 원자로. 지면에서는 단답형으로 재작성해야 한다.
            response = 'short'
            choices = []
            if 'class="picks"' in pq:
                btn_ids = re.findall(r'<button[^>]*id="([^"]+)"', pq)
                choices = [blabels.get(b, '') for b in btn_ids]
                ok_ids = [b for b in btn_ids if b in pmap]
                if ok_ids:
                    response = 'choice2'
                    atoms = [blabels.get(ok_ids[0], '')]
                else:
                    missing = missing + btn_ids

            problems.append({
                "idx": idx,
                "ask_html": ask_html.strip(),
                "ask_text": strip_tags(ask_html),
                "response": response,
                "choices": choices,
                "inputs": inputs,
                "answer_atoms": atoms,
                "unmatched_inputs": missing,
                "why_html": (why.group(2).strip() if why else None),
            })

        types.append({
            "type_id": type_id,
            "no": int(no.group(1)) if no else None,
            "title": strip_tags(title.group(1)) if title else '',
            "chips": [strip_tags(c) for c in chips],
            "tip_html": tip.group(1).strip() if tip else '',
            "tip_text": strip_tags(tip.group(1)) if tip else '',
            "problems": problems,
        })

    n_prob = sum(len(t["problems"]) for t in types)
    n_atom = sum(len(p["answer_atoms"]) for t in types for p in t["problems"])
    n_miss = sum(len(p["unmatched_inputs"]) for t in types for p in t["problems"])
    n_choice = sum(1 for t in types for p in t["problems"] if p["response"] == 'choice2')

    out = {
        "meta": {
            "grade": "math2",
            "unit": unit,
            "generation": "D",
            "source": str(src).replace('\\', '/'),
            "extractor": "extract_math2_p.py",
            "counts": {"types": len(types), "problems": n_prob, "atoms": n_atom,
                       "unmatched_inputs": n_miss, "choice2": n_choice},
        },
        "types": types,
    }
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print("types=%d problems=%d atoms=%d choice2=%d unmatched=%d -> %s"
          % (len(types), n_prob, n_atom, n_choice, n_miss, dst))


if __name__ == '__main__':
    main()
