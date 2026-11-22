"""build_term2.py — 중1 2학기 기말(교과서 6단원 평면도형의 성질 · 7단원 입체도형의 성질) 세트 빌더

세트 파일: 70_tools/print/term2/<name>.py 가 아래를 정의한다.
    META = {'id', 'title', 'subtitle', 'kind': 'exam'|'practice', 'time_min'}
    PROBLEMS = [문항 dict, ...]      (형식은 build_exam 의 exam.json 문항과 같다 + 'unit', 'points',
                                      practice 는 'sec' 로 구역을 나눈다)
    def check(): ...                 정답을 다시 계산해 assert 한다.
    SECTIONS = {sec 키: (제목, 핵심 정리 HTML)}   (practice 만)

사용:
    python build_term2.py <세트이름> [<세트이름> ...]        HTML + pdfplan 생성
    python build_term2.py --all

출력: HTML  → 40_grades/middle/math1/print/term2_final/<id>_{Q,K}.html
      PDF   → C:/세은/수학/중1_정기고사/<폴더>/  (pdfplan.json, print_pdf.ps1 로 인쇄)
"""
import importlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'term2'))
import build_exam as BE  # noqa: E402
from build_sheet import ksec, esc  # noqa: E402

ROOT = HERE.parents[1]
HTML_DIR = ROOT / '40_grades' / 'middle' / 'math1' / 'print' / 'term2_final'
PDF_ROOT = Path('C:/세은/수학/중1_정기고사')
ALL_SETS = ['practice', 'mock1', 'mock2', 'mock3']

# ───────────────────────────── 잉크: 총량 최소 + 남은 색은 고르게
# 1) 바탕 면(문항 칸·풀이 칸 줄무늬·안내 상자·해설 바탕·표 머리)을 모두 없앤다. 잉크 총량의 대부분이 여기서 나온다.
# 2) 테두리는 얇은 선 하나만, 색은 청록·자홍·노랑(주황) 중 하나씩 나눠 맡긴다.
# 3) 본문 글자는 검정(가독성·선명도). 보조 글자(번호·라벨·힌트)만 색 글자로 해서 검정 사용을 조금 덜어 낸다.
INK_CSS = """
.head { border-bottom: 1pt solid #29a3d6; }
.head h1 { color: #1c3266; }
.head .crumb { color: #0288d1; }
.head .sub { color: #c2185b; }
.idbar { color: #1c3266; }
.idbar .f { border-bottom: 0.8px solid #29a3d6; }
.notice { background: none; border-left: 2pt solid #f2a900; color: #1c3266; padding: 2px 8px; }
.prob { border: 0.8px solid #8fd0ec; background: none; }
.pn { background: none; color: #c2185b; border: 1.2px solid #c2185b; }
.lv-L { color: #0288d1; } .lv-M { color: #c2185b; }
.lvn { color: #0288d1; }
.tname { color: #c2185b; }
.fmt { color: #0288d1; }
.fmt b { color: #c2185b; }
.work { border: 0.8px dashed #f2b705; background: none; background-image: none; }
.ansline .lab { color: #c2185b; }
.ansline .blank { border-bottom: 1pt solid #29a3d6; }
.pts { color: #c2185b; border: 0.8px solid #c2185b; background: none; }
th { background: none; color: #0277bd; border-bottom: 1.2px solid #29a3d6; }
th, td { border-color: #b3e0f2; }
.sol { border-left: 1.6pt solid #c2185b; background: none; padding: 3px 9px; }
.sol .sq { color: #1c3266; }
.sol .hint { background: none; color: #a15c00; padding: 0; }
.sol .ans { color: #c2185b; }
.why { color: #0277bd; }
.why b { color: #0277bd; }
.rub { border: 0.8px solid #29a3d6; background: none; }
.rub .rh { color: #0277bd; }
.rub .rq { color: #1c3266; }
.legend { background: none; border: 0.8px solid #f2b705; }
.foot { border-top: 0.6px solid #8fd0ec; color: #0288d1; }
.ksec { border-top: 1pt solid #c2185b; }
.ksec .kt { color: #c2185b; }
.ksec .kd { color: #0288d1; }
.sum { border: 0.8px solid #f2a900; background: none; border-radius: 4px; padding: 5px 10px; margin: 4px 0 8px;
       font-size: 9.6pt; color: #1c3266; page-break-inside: avoid; break-inside: avoid; }
.sum b { color: #c2185b; }
.chs .fig-ch { display: inline-block; vertical-align: middle; }
.secblk { break-inside: avoid; page-break-inside: avoid; }
"""


def page(title, body):
    return ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
            '<title>' + esc(title) + '</title>\n<style>' + BE.CSS + BE.EXAM_CSS + INK_CSS + '</style>\n</head>\n'
            '<body>\n<div class="sheet">\n' + body + '\n</div>\n</body>\n</html>\n')


def head_block(meta, kind_label):
    return ('<div class="head">\n'
            '  <div class="crumb">중1 수학 · 2학기 기말 대비 · 6단원 평면도형의 성질 · 7단원 입체도형의 성질</div>\n'
            '  <h1>' + meta['title'] + ' <span style="font-size:11pt;color:#0277bd;font-weight:700">— '
            + kind_label + '</span></h1>\n'
            '  <div class="sub">' + meta['subtitle'] + '</div>\n</div>\n')


BE.page = page
BE.head_block = head_block


# ───────────────────────────── 문항 한 개 (연습용, 배점 없음)
def prob_html(i, p, show_unit=True):
    lv = p['level']
    wmm = p.get('work_mm') or BE.WORK_MM_EXAM[p['format']][lv]
    b = ('<div class="prob">\n'
         '  <div class="ph"><span class="pn">' + str(i) + '</span>'
         '<span class="lv lv-' + lv + '">' + BE.LEVEL_MARK[lv] + '</span>'
         '<span class="lvn">' + BE.LEVEL_NAME[lv] + '</span>'
         '<span class="tname">' + esc(p.get('topic') or '') + '</span></div>\n'
         '  <div class="stem">' + p['stem_print'] + '</div>\n'
         + ('  <div class="fig">' + p['figure'] + '</div>\n' if p.get('figure') else ''))
    if p['format'] == 'choice5':
        b += BE.choices_html(p)
        b += ('  <div class="work" style="height:' + str(wmm) + 'mm"></div>\n'
              '  <div class="ansline"><span class="lab">답</span>'
              '<span class="blank" style="max-width:16mm"></span><span class="unit">번</span></div>\n')
    else:
        if p['format'] == 'short' and p.get('answer_format'):
            b += '  <div class="fmt">답의 형태 — <b>' + esc(p['answer_format']) + '</b></div>\n'
        if p['format'] == 'essay':
            b += '  <div class="fmt">풀이 과정을 꼭 써요.</div>\n'
        b += ('  <div class="work" style="height:' + str(wmm) + 'mm"></div>\n'
              '  <div class="ansline"><span class="lab">답</span><span class="blank"></span>'
              + ('<span class="unit">' + esc(p['answer_unit']) + '</span>' if p.get('answer_unit') else '')
              + '</div>\n')
    return b + '</div>\n'


def build_practice_Q(meta, probs, sections):
    b = head_block(meta, '문제지')
    b += ('<div class="idbar">이름 <span class="f"></span> 날짜 <span class="f"></span> '
          '맞은 개수 <span class="f" style="min-width:16mm"></span> / ' + str(len(probs)) + '</div>\n')
    b += ('<div class="notice">구역마다 <b>핵심 정리</b>를 먼저 읽고 풀어요. 도형 문제는 <b>그림에 주어진 수치를 '
          '먼저 표시</b>하고 시작해요. 다 푼 뒤 해답 묶음으로 채점하고, 틀린 문제는 해설을 읽고 다시 풀어요.</div>\n')
    cur = None
    for i, p in enumerate(probs, start=1):
        if p['sec'] != cur:
            if cur is not None:
                b += '</div></div>\n'
            cur = p['sec']
            t, s = sections[cur]
            # 구역 머리말이 쪽 끝에 홀로 남지 않도록 구역 전체를 한 덩어리로 묶는다
            b += '<div class="secblk">' + ksec(t, '')
            b += '<div class="sum">' + s + '</div>\n<div class="cols">\n'
        b += prob_html(i, p)
    b += '</div></div>\n'
    b += BE.foot(meta, '문제지')
    return page(meta['title'] + ' 문제지', b)


def build_practice_K(meta, probs, sections):
    b = head_block(meta, '해답 묶음 · 정답 · 해설')
    b += ('<div class="notice">① 정답표로 채점 → ② 틀린 문제는 해설을 읽고 <b>그림에 직접 표시하며</b> 다시 풀어요.</div>\n')
    b += ksec('① 정답 한눈에', '')
    b += ('<table>\n<thead><tr><th class="c" style="width:8%">번호</th><th style="width:44%">정답</th>'
          '<th style="width:36%">구역 · 무엇을 재나</th><th class="c" style="width:12%">채점</th></tr></thead>\n<tbody>\n')
    for i, p in enumerate(probs, start=1):
        b += ('<tr><td class="c">' + str(i) + '</td><td><b>' + BE.answer_disp(p) + '</b></td>'
              '<td>' + esc(sections[p['sec']][0]) + ' · ' + esc(p.get('topic') or '') + '</td><td></td></tr>\n')
    b += '</tbody>\n</table>\n'
    b += ksec('② 해설', '그림은 문제와 같고, 풀이에 필요한 보조 표시를 자홍색으로 더했어요.')
    b += '<div class="cols">\n'
    for i, p in enumerate(probs, start=1):
        b += sol_html(i, p)
    b += '</div>\n' + BE.foot(meta, '해답 묶음')
    return page(meta['title'] + ' 해답 묶음', b)


def sol_html(i, p):
    fig = p.get('figure_sol') or p.get('figure')
    b = ('<div class="sol">\n'
         '  <div class="sh">' + str(i) + '. <span class="ans">' + BE.answer_disp(p) + '</span></div>\n'
         '  <div class="sq">' + p['stem_print'] + '</div>\n'
         + ('  <div class="fig">' + fig + '</div>\n' if fig else '')
         + '  <div class="hint">힌트 · ' + p['hint'] + '</div>\n'
         '  <div class="st">' + p['solution'] + '</div>\n')
    if p['format'] == 'choice5' and p.get('distractor_why'):
        wrongs = [n for n in range(1, 6) if n != p['answer_choice']]
        b += ('  <div class="why"><b>함정 보기</b> · '
              + ' · '.join(BE.CIRC[n - 1] + ' ' + esc(w) for n, w in zip(wrongs, p['distractor_why'])) + '</div>\n')
    if p['format'] == 'essay' and p.get('rubric'):
        b += ('  <div class="why"><b>채점 기준</b> · '
              + ' · '.join(esc(s['step']) + ' (' + str(s['points']) + '점)' for s in p['rubric']) + '</div>\n')
    return b + '</div>\n'


# ───────────────────────────── 공통 검사
def lint(meta, probs):
    errs = []
    ids = set()
    for p in probs:
        pid = p.get('id')
        if pid in ids:
            errs.append('id 중복 %s' % pid)
        ids.add(pid)
        for k in ('id', 'format', 'level', 'topic', 'stem_print', 'answer_print', 'hint', 'solution'):
            if not p.get(k):
                errs.append('%s: %s 없음' % (pid, k))
        if p['level'] not in ('L', 'M'):
            errs.append('%s: 최상위(H) 문항은 넣지 않는다' % pid)
        if p['format'] == 'choice5':
            if len(p.get('choices', [])) != 5 or len(p.get('distractor_why', [])) != 4:
                errs.append('%s: 보기 5개·함정 설명 4개가 필요' % pid)
            if p.get('answer_choice') not in (1, 2, 3, 4, 5):
                errs.append('%s: answer_choice' % pid)
            plain = [re.sub(r'<[^>]+>', '', ch).strip() for ch in p.get('choices', [])]
            if len(set(plain)) != len(plain) and not any('<svg' in ch for ch in p.get('choices', [])):
                errs.append('%s: 보기 중복' % pid)
        if p['format'] == 'essay':
            if not p.get('rubric') or sum(s['points'] for s in p['rubric']) != p.get('points', 8):
                errs.append('%s: 채점 기준 합이 배점과 다름' % pid)
        if p.get('needs_figure', True) and not p.get('figure') and p.get('geo', True):
            pass
    if meta['kind'] == 'exam':
        if len(probs) != 22:
            errs.append('모의고사 문항 수 %d (22여야 함)' % len(probs))
        tot = sum(p['points'] for p in probs)
        if tot != 100:
            errs.append('배점 합 %d (100이어야 함)' % tot)
        order = [p['format'] for p in probs]
        if order != sorted(order, key=['choice5', 'short', 'essay'].index):
            errs.append('형식 순서: 선택형 → 단답형 → 서술형')
    nfig = sum(1 for p in probs if p.get('figure') or any('<svg' in c for c in p.get('choices', [])))
    return errs, nfig


def build(name):
    mod = importlib.import_module(name)
    meta, probs = mod.META, mod.PROBLEMS
    mod.check()
    errs, nfig = lint(meta, probs)
    if errs:
        raise SystemExit('[%s] 검사 실패:\n  ' % name + '\n  '.join(errs))
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    pdf_dir = PDF_ROOT / meta['folder']
    if meta['kind'] == 'exam':
        cfg = {'id': meta['id'], 'grade': 'math1', 'title': meta['title'], 'subtitle': meta['subtitle'],
               'time_min': meta['time_min'], 'total_points': 100}
        resolved = [({'unit': p['unit'], 'points': p['points']}, p) for p in probs]
        resolved_k = [(it_, dict(p, figure=p.get('figure_sol') or p.get('figure'))) for it_, p in resolved]
        outs = [('Q', BE.build_Q(cfg, resolved), '문제지'), ('K', BE.build_K(cfg, resolved_k), '해답묶음')]
    else:
        outs = [('Q', build_practice_Q(meta, probs, mod.SECTIONS), '문제지'),
                ('K', build_practice_K(meta, probs, mod.SECTIONS), '해답묶음')]
    plan = []
    for kind, html, kname in outs:
        f = HTML_DIR / (meta['id'] + '_' + kind + '.html')
        f.write_text(html, encoding='utf-8')
        plan.append({'html': str(f.resolve()),
                     'pdf': str((pdf_dir / (meta['file'] + '_' + kname + '.pdf')).resolve())})
    pf = HTML_DIR / (meta['id'] + '_pdfplan.json')
    pf.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print('[%s] 문항 %d · 그림 있는 문항 %d · 검사 OK -> %s' % (name, len(probs), nfig, pf))


def main():
    names = ALL_SETS if sys.argv[1:] == ['--all'] else sys.argv[1:]
    for n in names:
        build(n)


if __name__ == '__main__':
    main()
