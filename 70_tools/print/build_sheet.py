"""build_sheet.py — 문제 은행 + 회차 config → 인쇄용 정적 HTML (Q/A/S/M/D)

의존성 없음. 외부 CDN 없음(오프라인 인쇄 안전). 수식은 HTML <sup> + 유니코드.

사용:
    python build_sheet.py <set_config.json> <출력디렉토리>

산출:
    <id>_Q.html  문제지        <id>_A.html  정답지(빠른 채점)
    <id>_S.html  해설지        <id>_M.html  오개념 카드
    <id>_D.html  오답 진단표
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK_ROOT = ROOT / '30_content' / 'problem_bank'

LEVEL_MARK = {'L': '●○○', 'M': '●●○', 'H': '●●●'}
LEVEL_NAME = {'L': '기본', 'M': '보통', 'H': '도전'}
WORK_MM = {'sm': 24, 'md': 34, 'lg': 48}

CSS = """
@page { size: A4; margin: 14mm 13mm 12mm 13mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Malgun Gothic','맑은 고딕',sans-serif; color: #1a1a1a; font-size: 11pt; line-height: 1.55; }
sup { font-size: .72em; vertical-align: super; line-height: 0; }
.sheet { max-width: 182mm; margin: 0 auto; }

/* ── 머리말 ── */
.head { border-bottom: 2.4pt solid #2b4c9b; padding-bottom: 6px; margin-bottom: 10px; }
.head .crumb { font-size: 9pt; color: #2b4c9b; font-weight: 700; letter-spacing: .04em; }
.head h1 { font-size: 17pt; font-weight: 800; margin: 2px 0 1px; }
.head .sub { font-size: 9.5pt; color: #555; }
.idbar { display: flex; gap: 10px; align-items: flex-end; margin: 8px 0 4px; font-size: 9.5pt; color: #333; }
.idbar .f { border-bottom: 1px solid #999; min-width: 30mm; display: inline-block; height: 15px; }
.idbar .meta { margin-left: auto; color: #2b4c9b; font-weight: 700; white-space: nowrap; }
.notice { background: #f3f6fd; border-left: 3pt solid #2b4c9b; padding: 6px 9px; font-size: 9.5pt;
          color: #24406f; margin-bottom: 12px; border-radius: 2px; }

/* ── 유형 구분 ── */
.tsec { margin: 14px 0 8px; page-break-inside: avoid; break-inside: avoid;
        page-break-after: avoid; break-after: avoid; }
/* 유형 머리말이 페이지 끝에 홀로 남지 않도록 첫 문항까지 한 덩어리로 묶는다 */
.tgroup { page-break-inside: avoid; break-inside: avoid; }
.tsec .tt { font-size: 11.5pt; font-weight: 800; color: #2b4c9b; }
.tsec .tp { font-size: 9.5pt; color: #444; background: #f7f8fa; border: 1px solid #e2e5ec;
            border-radius: 3px; padding: 5px 8px; margin-top: 3px; }

/* ── 문항 ── */
.prob { page-break-inside: avoid; break-inside: avoid; margin-bottom: 11px;
        border: 1px solid #dfe3ea; border-radius: 4px; padding: 8px 10px 9px; }
.ph { display: flex; align-items: center; gap: 7px; margin-bottom: 5px; }
.pn { width: 19px; height: 19px; border-radius: 50%; background: #2b4c9b; color: #fff;
      font-size: 9.5pt; font-weight: 800; display: inline-flex; align-items: center;
      justify-content: center; flex-shrink: 0; }
.lv { font-size: 8.5pt; font-weight: 700; letter-spacing: .1em; }
.lv-L { color: #2f7d4f; } .lv-M { color: #b07000; } .lv-H { color: #b3352c; }
.lvn { font-size: 8.5pt; color: #777; }
.tname { font-size: 8.5pt; color: #888; margin-left: auto; }
.stem { font-size: 11.5pt; margin: 2px 0 5px; }
.fmt { font-size: 8.8pt; color: #6b6b6b; margin-bottom: 5px; }
.fmt b { color: #b07000; }
.work { border: 1px dashed #c9cfda; border-radius: 3px; background: #fcfcfd;
        background-image: repeating-linear-gradient(#fcfcfd 0 7mm, #eef0f4 7mm 7.2mm); }
.ansline { margin-top: 6px; font-size: 11pt; display: flex; align-items: flex-end; gap: 6px; }
.ansline .lab { font-weight: 800; color: #2b4c9b; }
.ansline .blank { flex: 1; border-bottom: 1.4pt solid #333; height: 17px; }
.ansline .unit { font-weight: 700; }
.fig { text-align: center; margin: 3px 0 6px; }
.fig svg, .fig img { max-width: 100%; height: auto; }
/* 세로 분수 — KaTeX 없이 CSS 로. <span class="frac"><b>n</b><i>d</i></span> */
.frac { display: inline-block; vertical-align: middle; text-align: center; font-size: .92em; }
.frac b { display: block; border-bottom: 1.2px solid currentColor; padding: 0 .3em; font-weight: 400; }
.frac i { display: block; padding: 0 .3em; font-style: normal; }

/* ── 표 ── */
table { width: 100%; border-collapse: collapse; font-size: 10pt; }
th, td { border: 1px solid #ccd2dd; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #eef2fa; color: #24406f; font-weight: 700; font-size: 9.5pt; }
td.c, th.c { text-align: center; }
tr { page-break-inside: avoid; break-inside: avoid; }

/* ── 해설 ── */
.sol { page-break-inside: avoid; break-inside: avoid; margin-bottom: 9px;
       border-left: 3pt solid #2f7d4f; background: #f5faf7; padding: 7px 10px; border-radius: 3px; }
.sol .sh { font-weight: 800; font-size: 10.5pt; }
.sol .sq { font-size: 10pt; color: #555; margin: 2px 0 4px; }
.sol .hint { font-size: 9.5pt; color: #7a5a00; background: #fff7e6; border-radius: 3px;
             padding: 3px 7px; display: inline-block; margin-bottom: 4px; }
.sol .st { font-size: 10.5pt; }
.sol .ans { font-weight: 800; color: #2f7d4f; }

/* ── 오개념 카드 ── */
.mis { page-break-inside: avoid; break-inside: avoid; border: 1.4pt solid #7b4bbd;
       border-radius: 5px; padding: 9px 11px; margin-bottom: 10px; background: #faf7ff; }
.mis .mh { display: flex; align-items: center; gap: 7px; margin-bottom: 5px; }
.mis .mn { width: 20px; height: 20px; border-radius: 4px; background: #7b4bbd; color: #fff;
           font-size: 9.5pt; font-weight: 800; display: inline-flex; align-items: center;
           justify-content: center; flex-shrink: 0; }
.mis .ml { font-weight: 800; font-size: 10.5pt; color: #4b2d78; }
.mis .row { font-size: 10pt; margin: 3px 0; }
.mis .tag { display: inline-block; min-width: 56px; padding-right: 9px; font-weight: 700;
            color: #7b4bbd; font-size: 9pt; }
.mis .ask { background: #fff; border: 1px solid #dfd2f2; border-radius: 3px; padding: 5px 8px; margin-top: 4px; }
.mis .chk { margin-top: 5px; font-size: 10pt; }
.mis .chk .blank { display: inline-block; border-bottom: 1.2pt solid #555; min-width: 34mm; height: 15px; }
.keys { margin-top: 10px; border-top: 1px dashed #aaa; padding-top: 6px; font-size: 9pt; color: #666; }

/* ── 진단표 ── */
.legend { font-size: 9.5pt; background: #f7f8fa; border: 1px solid #e2e5ec; border-radius: 3px;
          padding: 7px 9px; margin-bottom: 10px; }
.legend b { color: #2b4c9b; }
.foot { margin-top: 12px; padding-top: 5px; border-top: 1px solid #ddd;
        font-size: 8.5pt; color: #999; display: flex; }
.foot .r { margin-left: auto; }
.pagebreak { page-break-before: always; break-before: page; }
.ksec { margin: 16px 0 8px; border-top: 2pt solid #2b4c9b; padding-top: 7px; }
.ksec .kt { font-size: 13pt; font-weight: 800; color: #2b4c9b; }
.ksec .kd { font-size: 9pt; color: #666; margin-top: 1px; }

/* ── 세로 2단 (구역 단위로 씌운다. 표는 감싸지 않는다 — 표는 1단이 읽기 좋다) ── */
.cols { columns: 2; column-gap: 7mm; }
.cols > * { break-inside: avoid; page-break-inside: avoid; }
.cols .mis { padding: 7px 9px; margin-bottom: 8px; }
.cols .mis .ml { font-size: 9.8pt; }
.cols .mis .row, .cols .mis .ask { font-size: 9.2pt; }
.cols .mis .tag { min-width: 0; padding-right: 6px; font-size: 8.4pt; }
.cols .mis .chk { font-size: 9.2pt; }
.cols .mis .chk .blank { min-width: 22mm; }
.cols .sol { padding: 6px 9px; margin-bottom: 7px; }
.cols .sol .sh { font-size: 9.8pt; }
.cols .sol .sq { font-size: 9pt; margin: 1px 0 3px; }
.cols .sol .hint { font-size: 8.6pt; padding: 2px 6px; }
.cols .sol .st { font-size: 9.4pt; }
"""

# 문제집처럼 세로 2단. 칸이 좁아지므로 글자·여백을 함께 줄인다.
CSS_2COL = """
body { font-size: 10pt; }
.tsec { margin: 0 0 6px; }
.tsec .tt { font-size: 10.5pt; }
.tsec .tp { font-size: 8.6pt; padding: 4px 6px; }
.tgroup { margin-bottom: 9px; }
.prob { margin-bottom: 8px; padding: 6px 8px 7px; }
.stem { font-size: 10.5pt; margin: 1px 0 4px; }
.fmt { font-size: 8.2pt; margin-bottom: 4px; }
.ph { gap: 5px; margin-bottom: 4px; }
.pn { width: 17px; height: 17px; font-size: 8.8pt; }
.lv { font-size: 8pt; }
.lvn { font-size: 8pt; }
.tname { display: none; }
.ansline { margin-top: 5px; font-size: 10pt; }
.work { background-image: repeating-linear-gradient(#fcfcfd 0 6.5mm, #eef0f4 6.5mm 6.7mm); }
"""

WORK_MM_2COL = {'sm': 21, 'md': 29, 'lg': 41}


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def page(title, body, two_col=False):
    css = CSS + (CSS_2COL if two_col else '')
    return ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
            '<title>' + esc(title) + '</title>\n<style>' + css + '</style>\n</head>\n<body>\n'
            '<div class="sheet">\n' + body + '\n</div>\n</body>\n</html>\n')


def ksec(title, desc):
    return ('<div class="ksec"><div class="kt">' + title + '</div>'
            '<div class="kd">' + desc + '</div></div>\n')


def head_block(cfg, kind_label, extra_meta=''):
    return (
        '<div class="head">\n'
        '  <div class="crumb">중' + cfg['grade'][-1] + ' 수학 · 단원 ' + str(cfg['unit']) + ' ' + esc(cfg['unit_name']) + '</div>\n'
        '  <h1>' + esc(cfg['title']) + ' <span style="font-size:11pt;color:#888;font-weight:700">— ' + kind_label + '</span></h1>\n'
        '  <div class="sub">' + esc(cfg.get('subtitle', '')) + '</div>\n'
        '</div>\n' + extra_meta
    )


def id_bar(cfg, n):
    return ('<div class="idbar">이름 <span class="f"></span> 날짜 <span class="f"></span>'
            '<span class="meta">목표 ' + str(cfg.get('time_min', 15)) + '분 · ' + str(n) + '문항</span></div>\n')


def foot(cfg, kind):
    return ('<div class="foot"><span>' + esc(cfg['id']) + ' · ' + kind + '</span>'
            '<span class="r">math-story-telling</span></div>\n')


def select_problems(cfg, bank):
    types = {t['no']: t for t in bank['types']}
    picked = []
    if cfg.get('kind') == 'mock':
        pick = cfg.get('pick', {})
        quota = pick.get('quota')          # {"L":1,"M":1} — 난이도별 개수를 직접 지정
        per = pick.get('per_type', 1)
        order = pick.get('levels', ['L', 'M', 'H'])
        for tno in cfg['types']:
            t = types[tno]
            if quota:
                # per_type + levels 로는 "유형마다 L 1개 + M 1개"를 표현할 수 없다.
                # 정렬 후 앞에서 자르면 L 만 2개가 뽑히기 때문. quota 는 그걸 정확히 표현한다.
                for lv in ['L', 'M', 'H']:
                    k = int(quota.get(lv, 0))
                    if k:
                        picked.extend((t, p) for p in [q for q in t['problems'] if q['level'] == lv][:k])
            else:
                ps = sorted(t['problems'], key=lambda p: order.index(p['level']) if p['level'] in order else 9)
                picked.extend((t, p) for p in ps[:per])
        picked.sort(key=lambda tp: (['L', 'M', 'H'].index(tp[1]['level']), tp[0]['no']))
    else:
        for tno in cfg['types']:
            t = types[tno]
            for p in t['problems']:
                picked.append((t, p))
    return picked


# ────────────────────────────────────────────── Q 문제지
def build_Q(cfg, bank, picked):
    two = int(cfg.get('columns', 2)) == 2
    work_mm = WORK_MM_2COL if two else WORK_MM
    b = head_block(cfg, '문제지')
    b += id_bar(cfg, len(picked))
    b += ('<div class="notice">먼저 스스로 풀어 보고, <b>다 푼 뒤에</b> 정답지를 꺼내요. '
          '풀이는 점선 칸 안에 적고, 답은 맨 아래 줄에 적어요. '
          '채점은 <b>○</b>(맞음) · <b>△</b>(틀렸지만 어디서 틀렸는지 알겠음) · <b>X</b>(왜 틀렸는지 모르겠음) 로 해요.</div>\n')
    if two:
        b += '<div class="cols">\n'

    last_type = None
    open_group = False
    for i, (t, p) in enumerate(picked, start=1):
        if cfg.get('kind') != 'mock' and t['no'] != last_type:
            if open_group:
                b += '</div>\n'
                open_group = False
            b += ('<div class="tgroup">\n'
                  '<div class="tsec"><div class="tt">유형 ' + str(t['no']) + ' · ' + esc(t['title']) + '</div>'
                  '<div class="tp">' + t['principle'] + '</div></div>\n')
            last_type = t['no']
            open_group = True
        lv = p['level']
        unit = p.get('answer_unit')
        b += ('<div class="prob">\n'
              '  <div class="ph"><span class="pn">' + str(i) + '</span>'
              '<span class="lv lv-' + lv + '">' + LEVEL_MARK[lv] + '</span>'
              '<span class="lvn">' + LEVEL_NAME[lv] + '</span>'
              '<span class="tname">유형 ' + str(t['no']) + ' ' + esc(t['title']) + '</span></div>\n'
              '  <div class="stem">' + p['stem_print'] + '</div>\n'
              + ('  <div class="fig">' + p['figure'] + '</div>\n' if p.get('figure') else '')
              + '  <div class="fmt">답의 형태 — <b>' + esc(p['answer_format']) + '</b></div>\n'
              '  <div class="work" style="height:' + str(work_mm[p['work_space']]) + 'mm"></div>\n'
              '  <div class="ansline"><span class="lab">답</span><span class="blank"></span>'
              + ('<span class="unit">' + esc(unit) + '</span>' if unit else '') + '</div>\n'
              '</div>\n')
        if open_group:
            b += '</div>\n'
            open_group = False
    if open_group:
        b += '</div>\n'
    if two:
        b += '</div>\n'
    b += foot(cfg, '문제지 Q')
    return page(cfg['title'] + ' 문제지', b, two_col=two)


# ────────────────────────────────────────────── A 정답지
GRADING_NOTICE = ('<b>채점 방법</b> — 답만 비교해요. 점수는 적지 않아요.<br>'
                  '<b>○</b> 맞음 → 넘어가요 &nbsp;·&nbsp; '
                  '<b>△</b> 틀렸지만 <b>어디서 틀렸는지 알겠어요</b> → 그 자리에서 다시 풀어요 &nbsp;·&nbsp; '
                  '<b>X</b> <b>왜 틀렸는지 모르겠어요</b> → 번호에 맞는 <b>오개념 카드</b>를 읽어요.<br>'
                  '<b>이렇게 써도 맞아요</b> 칸에 있는 답도 정답이에요.')


def body_A(cfg, picked, mis, embedded=False):
    b = '' if embedded else ('<div class="notice">' + GRADING_NOTICE + '</div>\n')
    b += ('<table>\n<thead><tr><th class="c" style="width:9%">번호</th><th style="width:30%">정답</th>'
          '<th style="width:31%">이렇게 써도 맞아요</th>'
          '<th style="width:30%">X 일 때 볼 오개념 카드</th></tr></thead>\n<tbody>\n')
    for i, (t, p) in enumerate(picked, start=1):
        acc = ' / '.join(p.get('answer_accept') or []) or '—'
        nos = sorted(mis['items'][m]['no'] for m in p.get('misconceptions', []) if m in mis['items'])
        cards = [str(x) + '번' for x in nos]
        b += ('<tr><td class="c">' + str(i) + '</td>'
              '<td><b>' + p['answer_print'] + '</b>'
              + ((' <span style="color:#777">' + esc(p['answer_unit']) + '</span>') if p.get('answer_unit') else '')
              + '</td>'
              '<td style="color:#555">' + esc(acc) + '</td>'
              '<td style="color:#7b4bbd">' + (', '.join(cards) or '—') + '</td></tr>\n')
    b += '</tbody>\n</table>\n'
    return b


def build_A(cfg, bank, picked, mis):
    b = head_block(cfg, '정답지 (빠른 채점)') + body_A(cfg, picked, mis) + foot(cfg, '정답지 A')
    return page(cfg['title'] + ' 정답지', b)


# ────────────────────────────────────────────── S 해설지
def body_S(cfg, picked, embedded=False):
    b = '' if embedded else (
        '<div class="notice">채점이 끝난 뒤에 봐요. <b>△</b> 표시한 문제는 해설을 보기 전에 '
        '한 번 더 풀어 보면 훨씬 오래 남아요.</div>\n')
    for i, (t, p) in enumerate(picked, start=1):
        b += ('<div class="sol">\n'
              '  <div class="sh">' + str(i) + '. <span class="ans">' + p['answer_print'] + '</span>'
              + ((' <span style="color:#777;font-weight:400">' + esc(p['answer_unit']) + '</span>') if p.get('answer_unit') else '')
              + '</div>\n'
              '  <div class="sq">' + p['stem_print'] + '</div>\n'
              + ('  <div class="fig">' + p['figure'] + '</div>\n' if p.get('figure') else '')
              + '  <div class="hint">힌트 · ' + p['hint'] + '</div>\n'
              '  <div class="st">' + p['solution'] + '</div>\n'
              '</div>\n')
    return b


def build_S(cfg, bank, picked):
    b = head_block(cfg, '해설지') + body_S(cfg, picked) + foot(cfg, '해설지 S')
    return page(cfg['title'] + ' 해설지', b)


# ────────────────────────────────────────────── M 오개념 카드
def used_misconceptions(picked, mis):
    seen, out = set(), []
    for _t, p in picked:
        for m in p.get('misconceptions', []):
            if m in mis['items'] and m not in seen:
                seen.add(m)
                out.append((m, mis['items'][m]))
    out.sort(key=lambda kv: kv[1]['no'])
    return out


def body_M(cfg, picked, mis, embedded=False, with_keys=True):
    items = used_misconceptions(picked, mis)
    b = '' if embedded else (
        '<div class="notice">정답지에서 <b>X</b> 표시가 나온 번호만 찾아 읽으면 돼요. 전부 읽지 않아도 괜찮아요.<br>'
        '읽고 나서 <b>확인 문제</b>를 꼭 한 번 풀어 봐요. 확인 문제의 답은 맨 마지막 줄에 모아 두었어요.</div>\n')
    for _k, it in items:
        b += ('<div class="mis">\n'
              '  <div class="mh"><span class="mn">' + str(it['no']) + '</span>'
              '<span class="ml">' + it['label'] + '</span></div>\n'
              '  <div class="row"><span class="tag">괜찮아요</span>' + it['empathy'] + '</div>\n'
              '  <div class="row"><span class="tag">이렇게 볼까요</span>' + it['counter'] + '</div>\n'
              '  <div class="ask"><span class="tag">스스로 답해 봐요</span>' + it['ask'] + '</div>\n'
              '  <div class="chk"><b>확인 문제</b> · ' + it['check']['q'] + ' &nbsp; <span class="blank"></span></div>\n'
              '</div>\n')
    if with_keys:
        b += keys_line(items)
    return b


def keys_line(items):
    keys = ' &nbsp;·&nbsp; '.join(str(it['no']) + '번 ' + it['check']['a'] for _k, it in items)
    return '<div class="keys"><b>확인 문제 정답</b> — ' + keys + '</div>\n'


def build_M(cfg, picked, mis):
    b = head_block(cfg, '오개념 카드') + body_M(cfg, picked, mis) + foot(cfg, '오개념 카드 M')
    return page(cfg['title'] + ' 오개념 카드', b)


# ────────────────────────────────────────────── D 오답 진단표
def body_D(cfg, picked, mis, embedded=False):
    items = used_misconceptions(picked, mis)
    b = '' if embedded else (
        '<div class="legend">채점한 뒤 이 표를 채워요. <b>점수는 적지 않아요.</b><br>'
        '<b>○</b> 맞음 &nbsp;·&nbsp; <b>△</b> 틀렸지만 어디서 틀렸는지 알겠음 (계산 실수 등) → 다시 풀면 끝 &nbsp;·&nbsp; '
        '<b>X</b> 왜 틀렸는지 모르겠음 → <b>오개념 카드</b>를 읽고, 카드 번호를 오른쪽에 적어요.</div>\n')
    b += ('<table>\n<thead><tr><th class="c" style="width:9%">번호</th>'
          '<th class="c" style="width:23%">○ △ X</th>'
          '<th style="width:34%">X 였다면 · 오개념 카드 번호</th>'
          '<th style="width:34%">다시 풀어 본 날</th></tr></thead>\n<tbody>\n')
    for i, (_t, _p) in enumerate(picked, start=1):
        b += ('<tr><td class="c">' + str(i) + '</td>'
              '<td class="c" style="letter-spacing:.5em;color:#888">○ △ X</td><td></td><td></td></tr>\n')
    b += '</tbody>\n</table>\n'
    b += ('<div class="tsec" style="margin-top:14px"><div class="tt">이번에 걸린 오개념</div>'
          '<div class="tp">X 가 나온 카드 번호에 동그라미를 쳐요. 같은 번호가 여러 번 나오면 그게 지금 가장 약한 곳이에요.</div></div>\n')
    b += ('<table>\n<thead><tr><th class="c" style="width:9%">번호</th><th>무엇을 헷갈렸나</th>'
          '<th class="c" style="width:24%">몇 번 나왔나</th></tr></thead>\n<tbody>\n')
    for _k, it in items:
        b += ('<tr><td class="c">' + str(it['no']) + '</td><td>' + it['label'] + '</td>'
              '<td class="c" style="color:#bbb">□ □ □ □ □</td></tr>\n')
    b += '</tbody>\n</table>\n'
    return b


def build_D(cfg, picked, mis):
    b = head_block(cfg, '오답 진단표') + id_bar(cfg, len(picked)) + body_D(cfg, picked, mis) \
        + foot(cfg, '오답 진단표 D')
    return page(cfg['title'] + ' 오답 진단표', b)


# ───────────────────────────────── K 정답·진단·오개념 묶음 (양면 인쇄 절약용)
def build_K(cfg, picked, mis):
    """해답 묶음 = 정답 → 진단표 → 오개념 카드 → 해설. 표는 1단, 카드·해설은 2단."""
    b = head_block(cfg, '해답 묶음 · 정답 · 진단 · 오개념 · 해설')
    b += ('<div class="notice">문제를 <b>다 푼 뒤에</b> 이 묶음을 꺼내요. '
          '① 정답으로 채점 → ② 진단표 작성 → ③ <b>X</b> 가 나온 번호의 오개념 카드 읽기 → ④ 그래도 막히면 해설.<br>'
          + GRADING_NOTICE + '</div>\n')

    b += ksec('① 정답 · 빠른 채점', '답만 비교해요. 점수는 적지 않아요.')
    b += body_A(cfg, picked, mis, embedded=True)

    b += ksec('② 오답 진단표', '채점한 뒤 직접 채워요. 여기가 다음에 무엇을 볼지 알려 줘요.')
    b += body_D(cfg, picked, mis, embedded=True)

    b += ksec('③ 오개념 카드', 'X 가 나온 번호만 읽으면 돼요. 전부 읽지 않아도 괜찮아요. '
                              '읽고 나서 확인 문제를 꼭 한 번 풀어 봐요 (정답은 이 절 맨 끝에).')
    b += '<div class="cols">\n' + body_M(cfg, picked, mis, embedded=True, with_keys=False) + '</div>\n'
    b += keys_line(used_misconceptions(picked, mis))

    b += ksec('④ 해설', '△ 표시한 문제는 해설을 보기 전에 한 번 더 풀어 보면 훨씬 오래 남아요.')
    b += '<div class="cols">\n' + body_S(cfg, picked, embedded=True) + '</div>\n'

    b += foot(cfg, '해답 묶음 K')
    return page(cfg['title'] + ' 해답 묶음', b)


def main():
    cfg_path = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
    bank = json.loads((BANK_ROOT / cfg['bank']).read_text(encoding='utf-8'))
    mis = json.loads((BANK_ROOT / cfg['misconceptions']).read_text(encoding='utf-8'))

    picked = select_problems(cfg, bank)
    outdir.mkdir(parents=True, exist_ok=True)

    builders = {
        'Q': lambda: build_Q(cfg, bank, picked),
        'A': lambda: build_A(cfg, bank, picked, mis),
        'S': lambda: build_S(cfg, bank, picked),
        'M': lambda: build_M(cfg, picked, mis),
        'D': lambda: build_D(cfg, picked, mis),
        'K': lambda: build_K(cfg, picked, mis),
    }
    kind_name = {'Q': '문제지', 'A': '정답지', 'S': '해설지', 'M': '오개념카드',
                 'D': '오답진단표', 'K': '해답묶음'}
    safe_title = re.sub(r'[\\/:*?"<>|\s·]', '', cfg['title'])
    pdf_dir = Path(cfg.get('pdf_dir') or (
        ROOT / '40_grades' / 'middle' / cfg['grade'] / 'print' / ('u%02d' % cfg['unit'])))

    made, plan = [], []
    for kind in cfg.get('outputs', ['Q', 'K']):
        html = builders[kind]()
        f = outdir / (cfg['id'] + '_' + kind + '.html')
        f.write_text(html, encoding='utf-8')
        made.append(f.name)
        plan.append({
            'html': str(f.resolve()),
            'pdf': str((pdf_dir / (cfg['id'] + '_' + safe_title + '_' + kind_name[kind] + '.pdf')).resolve()),
        })
    (outdir / (cfg['id'] + '_pdfplan.json')).write_text(
        json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print('set=%s problems=%d misconceptions=%d -> %s' % (
        cfg['id'], len(picked), len(used_misconceptions(picked, mis)), ', '.join(made)))


if __name__ == '__main__':
    main()
