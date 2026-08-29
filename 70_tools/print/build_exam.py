"""build_exam.py — 실전 모의고사 회차 config + 단원별 exam.json 풀 → 인쇄용 HTML (Q/K)

build_sheet.py 의 CSS·페이지 골격을 재사용하는 별도 빌더 (기존 유형세트 파이프라인 무변형).
수식은 HTML <sup> + 유니코드. 외부 의존성 없음.

사용:
    python build_exam.py <exam_config.json> <출력디렉토리>

산출:
    <id>_Q.html  시험지 (선택형 15 + 단답형 3 + 서술형 4, 100점, 45분)
    <id>_K.html  해답 묶음 (정답 한눈에 · 점수 계산 · 서술형 채점기준 · 전체 해설)
    <id>_pdfplan.json
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_sheet import CSS, esc, ksec  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BANK_ROOT = ROOT / '30_content' / 'problem_bank'

LEVEL_MARK = {'L': '●○○', 'M': '●●○', 'H': '●●●'}
LEVEL_NAME = {'L': '기본', 'M': '보통', 'H': '도전'}
CIRC = ['①', '②', '③', '④', '⑤']
FMT_LABEL = {'choice5': '선택형', 'short': '단답형', 'essay': '서술형'}
FMT_DESC = {'choice5': '보기에서 하나를 골라 번호에 ○표 해요. (문항당 3~4점)',
            'short': '답을 빈칸에 적어요. (문항당 4점)',
            'essay': '풀이 과정을 함께 써야 점수를 받아요. 부분 점수가 있어요. (문항당 8점)'}
WORK_MM_EXAM = {'choice5': {'L': 13, 'M': 19, 'H': 25}, 'short': {'L': 22, 'M': 28, 'H': 32},
                'essay': {'L': 52, 'M': 52, 'H': 56}}

EXAM_CSS = """
.pts { font-size: 8.5pt; font-weight: 800; color: #b3352c; border: 1px solid #e6c4c1;
       border-radius: 3px; padding: 0 4px; }
.chs { margin: 4px 0 2px; font-size: 10.5pt; }
.chs.row { display: flex; flex-wrap: wrap; gap: 3px 13px; }
.chs.col span { display: block; margin: 2px 0; }
.scorebox td { font-size: 10.5pt; }
.scorebox .blankc { color: #bbb; letter-spacing: .05em; }
.rub { page-break-inside: avoid; break-inside: avoid; border: 1.4pt solid #2f7d4f;
       border-radius: 5px; padding: 8px 11px; margin-bottom: 10px; background: #f5faf7; }
.rub .rh { font-weight: 800; font-size: 10.5pt; color: #205c39; margin-bottom: 3px; }
.rub .rq { font-size: 9.5pt; color: #555; margin-bottom: 5px; }
.rub table { margin-top: 3px; }
.why { font-size: 9.3pt; color: #6b4a9e; margin-top: 3px; }
.why b { color: #4b2d78; }
"""


def page(title, body):
    return ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
            '<title>' + esc(title) + '</title>\n<style>' + CSS + EXAM_CSS + '</style>\n</head>\n<body>\n'
            '<div class="sheet">\n' + body + '\n</div>\n</body>\n</html>\n')


def head_block(cfg, kind_label):
    return (
        '<div class="head">\n'
        '  <div class="crumb">중' + cfg['grade'][-1] + ' 수학 · 전 범위 시험대비</div>\n'
        '  <h1>' + esc(cfg['title']) + ' <span style="font-size:11pt;color:#888;font-weight:700">— '
        + kind_label + '</span></h1>\n'
        '  <div class="sub">' + esc(cfg.get('subtitle', '')) + '</div>\n'
        '</div>\n'
    )


def id_bar(cfg, n):
    return ('<div class="idbar">이름 <span class="f"></span> 날짜 <span class="f"></span> '
            '점수 <span class="f" style="min-width:20mm"></span> / ' + str(cfg['total_points'])
            + '<span class="meta">제한시간 ' + str(cfg['time_min']) + '분 · ' + str(n) + '문항 · '
            + str(cfg['total_points']) + '점</span></div>\n')


def foot(cfg, kind):
    return ('<div class="foot"><span>' + esc(cfg['id']) + ' · ' + kind + '</span>'
            '<span class="r">math-story-telling</span></div>\n')


def load(cfg):
    pools = {}
    resolved = []
    for it in cfg['problems']:
        u = it['unit']
        if u not in pools:
            d = json.loads((BANK_ROOT / 'math1' / ('u%02d' % u) / 'exam.json').read_text(encoding='utf-8'))
            pools[u] = {p['id']: p for p in d['problems']}
        p = pools[u].get(it['pid'])
        if p is None:
            raise SystemExit('pid 를 풀에서 못 찾음: %s (u%02d)' % (it['pid'], u))
        resolved.append((it, p))
    return resolved


def choices_html(p):
    ch = p['choices']
    plain = [re.sub(r'<[^>]+>', '', c) for c in ch]
    mode = 'col' if max(len(c) for c in plain) > 10 else 'row'
    inner = ''.join('<span>' + CIRC[i] + ' ' + ch[i] + '</span>' for i in range(5))
    return '<div class="chs ' + mode + '">' + inner + '</div>\n'


def answer_disp(p):
    if p['format'] == 'choice5':
        return CIRC[p['answer_choice'] - 1] + ' <span style="font-weight:400">' + p['answer_print'] + '</span>'
    out = '<b>' + p['answer_print'] + '</b>'
    if p.get('answer_unit'):
        out += ' <span style="color:#777">' + esc(p['answer_unit']) + '</span>'
    return out


# ────────────────────────────────────────────── Q 시험지
def build_Q(cfg, resolved):
    b = head_block(cfg, '시험지')
    b += id_bar(cfg, len(resolved))
    b += ('<div class="notice">실제 시험처럼 <b>' + str(cfg['time_min']) + '분 타이머</b>를 맞추고 시작해요. '
          '선택형은 보기 번호에 ○표, 단답형은 빈칸에, 서술형은 <b>풀이 과정까지</b> 적어요. '
          '다 푼 뒤에 해답 묶음으로 채점해요 — 서술형은 채점기준표에 따라 부분 점수를 줘요.</div>\n')

    last_fmt = None
    in_cols = False
    for i, (it, p) in enumerate(resolved, start=1):
        if p['format'] != last_fmt:
            if in_cols:
                b += '</div>\n'
                in_cols = False
            b += ksec(FMT_LABEL[p['format']], FMT_DESC[p['format']])
            if p['format'] in ('choice5', 'short'):
                b += '<div class="cols">\n'
                in_cols = True
            last_fmt = p['format']
        lv = p['level']
        wmm = WORK_MM_EXAM[p['format']][lv]
        b += ('<div class="prob">\n'
              '  <div class="ph"><span class="pn">' + str(i) + '</span>'
              '<span class="lv lv-' + lv + '">' + LEVEL_MARK[lv] + '</span>'
              '<span class="lvn">' + LEVEL_NAME[lv] + '</span>'
              '<span class="pts">' + str(it['points']) + '점</span>'
              '<span class="tname">단원 ' + str(it['unit']) + ' · ' + esc(p.get('topic') or '') + '</span></div>\n'
              '  <div class="stem">' + p['stem_print'] + '</div>\n'
              + ('  <div class="fig">' + p['figure'] + '</div>\n' if p.get('figure') else ''))
        if p['format'] == 'choice5':
            b += choices_html(p)
            b += ('  <div class="work" style="height:' + str(wmm) + 'mm"></div>\n'
                  '  <div class="ansline"><span class="lab">답</span>'
                  '<span class="blank" style="max-width:16mm"></span><span class="unit">번</span></div>\n')
        elif p['format'] == 'short':
            b += ('  <div class="fmt">답의 형태 — <b>' + esc(p['answer_format']) + '</b></div>\n'
                  '  <div class="work" style="height:' + str(wmm) + 'mm"></div>\n'
                  '  <div class="ansline"><span class="lab">답</span><span class="blank"></span>'
                  + ('<span class="unit">' + esc(p['answer_unit']) + '</span>' if p.get('answer_unit') else '')
                  + '</div>\n')
        else:
            b += ('  <div class="fmt">풀이 과정을 꼭 써요 — 과정이 맞으면 답이 틀려도 부분 점수를 받아요.</div>\n'
                  '  <div class="work" style="height:' + str(wmm) + 'mm"></div>\n'
                  '  <div class="ansline"><span class="lab">답</span><span class="blank"></span>'
                  + ('<span class="unit">' + esc(p['answer_unit']) + '</span>' if p.get('answer_unit') else '')
                  + '</div>\n')
        b += '</div>\n'
    if in_cols:
        b += '</div>\n'
    b += foot(cfg, '시험지 Q')
    return page(cfg['title'] + ' 시험지', b)


# ────────────────────────────────────────────── K 해답 묶음
def build_K(cfg, resolved):
    b = head_block(cfg, '해답 묶음 · 정답 · 점수 · 채점기준 · 해설')
    b += ('<div class="notice">시험지를 <b>다 푼 뒤에</b> 꺼내요. ① 정답표로 채점 → ② 점수 계산 → '
          '③ 서술형은 채점기준표로 부분 점수 → ④ 틀린 문제는 해설을 읽고, 표에 적힌 단원의 '
          '유형 세트(프린트 a/b/c 회차)로 돌아가 복습해요.</div>\n')

    # ① 정답 한눈에
    b += ksec('① 정답 한눈에', '채점하며 맞은 문항의 배점을 오른쪽 끝 칸에 적어요.')
    b += ('<table>\n<thead><tr><th class="c" style="width:8%">번호</th><th style="width:34%">정답</th>'
          '<th class="c" style="width:9%">배점</th><th style="width:34%">단원 · 무엇을 재나</th>'
          '<th class="c" style="width:15%">받은 점수</th></tr></thead>\n<tbody>\n')
    for i, (it, p) in enumerate(resolved, start=1):
        b += ('<tr><td class="c">' + str(i) + '</td>'
              '<td><b>' + answer_disp(p) + '</b></td>'
              '<td class="c">' + str(it['points']) + '</td>'
              '<td style="color:#555">단원 ' + str(it['unit']) + ' · ' + esc(p.get('topic') or '') + '</td>'
              '<td></td></tr>\n')
    b += '</tbody>\n</table>\n'

    # ② 점수 계산
    sec_pts = {}
    for it, p in resolved:
        sec_pts[FMT_LABEL[p['format']]] = sec_pts.get(FMT_LABEL[p['format']], 0) + it['points']
    b += ksec('② 점수 계산', '영역별로 받은 점수를 더해 총점을 내요.')
    b += '<table class="scorebox">\n<tbody>\n'
    for lab in ('선택형', '단답형', '서술형'):
        b += ('<tr><th style="width:24%">' + lab + '</th>'
              '<td class="c blankc" style="width:38%">________</td>'
              '<td style="width:38%">/ ' + str(sec_pts.get(lab, 0)) + '점</td></tr>\n')
    b += ('<tr><th>총점</th><td class="c blankc">________</td><td>/ ' + str(cfg['total_points']) + '점</td></tr>\n'
          '</tbody>\n</table>\n')
    b += ('<div class="legend" style="margin-top:8px">'
          '<b>90점 이상</b> 실전 감각 최고예요! · <b>75~89</b> 든든해요 — 틀린 유형만 다져요 · '
          '<b>60~74</b> 기본기는 좋아요 — 틀린 단원의 유형 세트를 복습해요 · '
          '<b>60점 미만</b> 워밍업 모의고사와 단원 세트부터 차근차근 다시 가요. 점수보다 '
          '<b>어느 단원에서 틀렸는지</b>가 더 중요한 정보예요.</div>\n')

    # ③ 서술형 채점기준
    b += ksec('③ 서술형 채점기준', '단계별로 점수를 줘요. 그 단계까지 바르게 썼으면 그 단계 점수를 받아요.')
    for i, (it, p) in enumerate(resolved, start=1):
        if p['format'] != 'essay':
            continue
        b += ('<div class="rub">\n  <div class="rh">' + str(i) + '번 (' + str(it['points']) + '점) · '
              + esc(p.get('topic') or '') + '</div>\n'
              '  <div class="rq">' + p['stem_print'] + '</div>\n'
              '  <table><thead><tr><th>채점 단계</th><th class="c" style="width:14%">배점</th></tr></thead><tbody>\n')
        for s in p['rubric']:
            b += '<tr><td>' + s['step'] + '</td><td class="c">' + str(s['points']) + '점</td></tr>\n'
        b += ('</tbody></table>\n'
              '  <div class="why" style="color:#205c39;margin-top:4px"><b>정답</b> ' + p['answer_print']
              + ((' ' + esc(p['answer_unit'])) if p.get('answer_unit') else '') + '</div>\n'
              '</div>\n')

    # ④ 해설
    b += ksec('④ 해설', '틀린 문제만 읽어도 돼요. 선택형은 "함정 보기"까지 읽으면 실수 예방이 돼요.')
    b += '<div class="cols">\n'
    for i, (it, p) in enumerate(resolved, start=1):
        b += ('<div class="sol">\n'
              '  <div class="sh">' + str(i) + '. <span class="ans">' + answer_disp(p) + '</span></div>\n'
              '  <div class="sq">' + p['stem_print'] + '</div>\n'
              + ('  <div class="fig">' + p['figure'] + '</div>\n' if p.get('figure') else '')
              + '  <div class="hint">힌트 · ' + p['hint'] + '</div>\n'
              '  <div class="st">' + p['solution'] + '</div>\n')
        if p['format'] == 'choice5' and p.get('distractor_why'):
            wrongs = [n for n in range(1, 6) if n != p['answer_choice']]
            pairs = list(zip(wrongs, p['distractor_why']))
            b += ('  <div class="why"><b>함정 보기</b> · '
                  + ' · '.join(CIRC[n - 1] + ' ' + esc(w) for n, w in pairs) + '</div>\n')
        b += '</div>\n'
    b += '</div>\n'
    b += foot(cfg, '해답 묶음 K')
    return page(cfg['title'] + ' 해답 묶음', b)


def main():
    cfg_path = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
    resolved = load(cfg)

    tot = sum(it['points'] for it, _p in resolved)
    if tot != cfg['total_points'] or len(resolved) != 22:
        raise SystemExit('config 불일치: 문항 %d 배점 %d' % (len(resolved), tot))

    outdir.mkdir(parents=True, exist_ok=True)
    pdf_dir = ROOT / '40_grades' / 'middle' / cfg['grade'] / 'print' / 'exam'
    safe_title = re.sub(r'[\\/:*?"<>|\s·]', '', cfg['title'])

    made, plan = [], []
    for kind, builder, kname in (('Q', build_Q, '시험지'), ('K', build_K, '해답묶음')):
        if kind not in cfg.get('outputs', ['Q', 'K']):
            continue
        html = builder(cfg, resolved)
        f = outdir / (cfg['id'] + '_' + kind + '.html')
        f.write_text(html, encoding='utf-8')
        made.append(f.name)
        plan.append({
            'html': str(f.resolve()),
            'pdf': str((pdf_dir / (cfg['id'] + '_' + safe_title + '_' + kname + '.pdf')).resolve()),
        })
    (outdir / (cfg['id'] + '_pdfplan.json')).write_text(
        json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    n_es = sum(1 for _it, p in resolved if p['format'] == 'essay')
    print('set=%s problems=%d points=%d essays=%d -> %s' % (
        cfg['id'], len(resolved), tot, n_es, ', '.join(made)))


if __name__ == '__main__':
    main()
