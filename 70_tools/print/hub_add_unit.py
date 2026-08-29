# -*- coding: utf-8 -*-
"""hub_add_unit.py — 프린트 허브(print/index.html)에 단원 블록을 넣는다 (math3부터, 마커 기반).

    python 70_tools/print/hub_add_unit.py math3 1

허브 파일 = 40_grades/middle/<grade>/print/index.html. 마커:
  <!-- SB-U<N> -->  뒤의 <span class="ps-link soon">…</span> 을 <a class="ps-link" href="../u<N>.html"> 로 교체
  <!-- TOC -->      앞에 단원 바로가기 <a href="#uNN"> 삽입 (빈 안내 span#toc-empty 제거)
  <!-- UNITS -->    앞에 단원 블록 삽입 (빈 안내 div#units-empty 제거)
회차 = problem_bank/sets/m<g>-uNN-{a,b,c,d,mock}.json 중 존재하는 것 순서대로. PDF 파일명은
60_deploy/print/<grade>/uNN/<setid>_pdfplan.json 에서 읽는다(build_sheet.py 가 만든 실제 이름).
이미 같은 id="uNN" 블록이 있으면 교체한다(재실행 안전).
"""
import io, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    grade, unit = sys.argv[1], int(sys.argv[2])
    g = grade[-1]; nn = '%02d' % unit
    hub = ROOT / '40_grades' / 'middle' / grade / 'print' / 'index.html'
    html = io.open(hub, encoding='utf-8').read()
    sets_dir = ROOT / '30_content' / 'problem_bank' / 'sets'
    plan_dir = ROOT / '60_deploy' / 'print' / grade / ('u' + nn)

    rows = []
    unit_name = None
    for suf in ('a', 'b', 'c', 'd', 'mock'):
        sid = 'm%s-u%s-%s' % (g, nn, suf)
        cfg_p = sets_dir / (sid + '.json')
        if not cfg_p.exists():
            continue
        cfg = json.loads(cfg_p.read_text(encoding='utf-8'))
        unit_name = cfg['unit_name']
        plan = json.loads((plan_dir / (sid + '_pdfplan.json')).read_text(encoding='utf-8'))
        pdfs = {Path(it['pdf']).name.split('_')[-1].replace('.pdf', ''): Path(it['pdf']).name for it in plan}
        q, k = pdfs.get('문제지'), pdfs.get('해답묶음')
        if not (q and k):
            raise SystemExit('pdfplan 에 문제지/해답묶음 이 없음: ' + sid)
        tag = ('<span class="tag tag-mock">모의</span>' if cfg.get('kind') == 'mock'
               else '<span class="tag tag-type">유형</span>')
        rows.append('<div class="set">' + tag + '<span class="name">' + cfg['title'] + '</span>'
                    '<a class="btn btn-q" href="u' + nn + '/' + q + '" target="_blank">📄 문제지</a>'
                    '<a class="btn btn-k" href="u' + nn + '/' + k + '" target="_blank">📘 해답 묶음</a></div>')
    if not rows:
        raise SystemExit('회차 config 없음: m%s-u%s-*' % (g, nn))

    block = ('<div class="unit" id="u' + nn + '"><h2><span class="no">' + str(unit) + '.</span>' + unit_name + '</h2>'
             + ''.join(rows) + '</div>\n')
    toc = '<a href="#u' + nn + '">' + str(unit) + '. ' + unit_name + '</a>'

    # 1) 사이드바
    # 안쪽 <span class="ps-ico">N</span> 까지 명시적으로 잡는다 — 게으른 (.*?)</span> 은 안쪽 span 에서 끊겨 구조를 깨뜨린다(2026-08-30 사고).
    sb_pat = re.compile(r'(<!-- SB-U' + str(unit) + r' -->)<span class="ps-link soon">(<span class="ps-ico">\d+</span>[^<]*)</span>')
    html, n_sb = sb_pat.subn(r'\1<a class="ps-link" href="../u' + str(unit) + r'.html">\2</a>', html)
    # 2) TOC (기존 항목 있으면 교체)
    html = re.sub(r'<a href="#u' + nn + r'">[^<]*</a>', '', html)
    html = html.replace('<span class="soon" id="toc-empty">아직 열린 단원이 없어요</span>', '')
    html = html.replace('<!-- TOC -->', toc + '<!-- TOC -->', 1)
    # 3) 단원 블록 (기존 블록 있으면 제거 후 삽입)
    html = re.sub(r'<div class="unit" id="u' + nn + r'">.*?</div></div>\n', '', html, flags=re.S)
    html = re.sub(r'<div class="empty" id="units-empty">.*?</div>\n', '', html, flags=re.S)
    html = html.replace('<!-- UNITS -->', block + '<!-- UNITS -->', 1)
    io.open(hub, 'w', encoding='utf-8', newline='\n').write(html)
    print('hub: unit %d "%s" · sets %d · sidebar %s -> %s' % (unit, unit_name, len(rows), 'linked' if n_sb else 'already', hub))

if __name__ == '__main__':
    main()
