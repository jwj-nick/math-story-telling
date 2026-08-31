"""verify_exam3.py — 중3 실전 모의고사 문항 풀(exam.json)·회차 config 검증

verify_exam.py(중1판)의 math3 전용 사본. 원본은 무변형 — grade/단원수/할당표/금지어/커버리지만 다르다.

사용:
    python 70_tools/print/verify_exam3.py u07       # 단원 풀 1개 검증
    python 70_tools/print/verify_exam3.py --all      # 12단원 풀 전부
    python 70_tools/print/verify_exam3.py --sets     # 6회차 config + 풀 교차 검증

검사 (단원 풀)
  X1 할당표    id·format·level 이 EXAM_SPEC3.md 할당표와 정확히 일치
  X2 choice5   보기 5개·중복 없음·answer_choice 유효·정답 보기 == answer_print
               ·수치 보기 오름차순·정답 위치 편중(같은 번호 3회+)
  X3 essay     rubric 존재·합계 8점·단계 2~4개
  X4 발문/표기  KaTeX 잔재·앱 의존 표현·요구문·answer_format·해요체(hint)
  X5 원본 대조  cv/sh 의 source_id 가 practice.json 에 존재·level 일치
               ·sh 는 answer_print 동일·cv 는 정답 값 포함(경고)
  X6 교육과정   금지 키워드(미분·적분·로그·지수함수·수열·벡터·행렬·허수·복소수·이차부등식·판별식)

검사 (--sets)
  S1 회차 구성  22문항·배점 합 100·format 수(choice15/short3/essay4)
  S2 난이도    kind 별 quota (std L9M10H3 / easy L22 / hard M11H11)
  S3 참조     모든 pid 가 풀에 존재·6회차 전체에서 각 문항 정확히 1회 사용
  S4 커버리지  2학기 단원(7~12) 회차당 1~4문항·1학기 합 7~9문항·1학기 단원당 최대 2
"""
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BANK_ROOT = ROOT / '30_content' / 'problem_bank'
SETS_DIR = BANK_ROOT / 'sets' / 'exam'
GRADE = 'math3'

# EXAM_SPEC3.md §5 할당표. (format, [levels]) — id 는 접두사+순번으로 파생된다.
QUOTA = {
    1:  {'cn': 'LMH',   'cv': 'LM',    'sh': 'L',  'es': 'LM'},
    2:  {'cn': 'LMH',   'cv': 'LM',    'sh': 'L',  'es': 'MH'},
    3:  {'cn': 'LMMH',  'cv': 'LM',    'sh': 'L',  'es': 'LM'},
    4:  {'cn': 'LMMH',  'cv': 'LM',    'sh': 'L',  'es': 'MH'},
    5:  {'cn': 'LMH',   'cv': 'LM',    'sh': 'L',  'es': 'LM'},
    6:  {'cn': 'LMH',   'cv': 'LM',    'sh': 'L',  'es': 'MH'},
    7:  {'cn': 'LMMMH', 'cv': 'LLMHH', 'sh': 'LM', 'es': 'LM'},
    8:  {'cn': 'LMMH',  'cv': 'LLMHH', 'sh': 'LM', 'es': 'MH'},
    9:  {'cn': 'LLMMH', 'cv': 'LLMHH', 'sh': 'LM', 'es': 'LM'},
    10: {'cn': 'LMMHH', 'cv': 'LLMHH', 'sh': 'LM', 'es': 'MH'},
    11: {'cn': 'LMMMH', 'cv': 'LLMHH', 'sh': 'LM', 'es': 'LM'},
    12: {'cn': 'LMMH',  'cv': 'LLMHH', 'sh': 'LM', 'es': 'MH'},
}
FMT_OF = {'cn': 'choice5', 'cv': 'choice5', 'sh': 'short', 'es': 'essay'}

KIND_QUOTA = {'std': {'L': 9, 'M': 10, 'H': 3}, 'easy': {'L': 22}, 'hard': {'M': 11, 'H': 11}}

APP_WORDS = ['□', '버튼', '슬라이더', '눌러', '탭을', '클릭', '위 그림에서 값을']
KATEX_LEFT = re.compile(r'(\$|\\dfrac|\\frac|\\overline|\\overrightarrow|\\overleftrightarrow|\\angle|\\times|\\div|\\pi)')
DEMAND = ['하시오', '구하시오', '나타내시오', '쓰시오', '고르시오', '까요?', '얼마인가요']
VOICE_BAD = re.compile(r'(한다|된다|이다|뺀다|더한다|곱한다|나눈다|계산한다|넣는다|바뀐다|사라진다)\.')
BANNED = ['미분', '적분', '로그', '지수함수', '수열', '벡터', '행렬', '허수', '복소수', '이차부등식', '판별식']
NUMLIKE = re.compile(r'^[−\-]?\d+(\.\d+)?')

errs, warns, infos = [], [], []


def norm(s):
    s = re.sub(r'<span class="frac"><b>([^<]*)</b><i>([^<]*)</i></span>', r'\1/\2', s or '')
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', '', s).replace('-', '−')


def expected_ids(unit):
    out = []
    for kind in ('cn', 'cv', 'sh', 'es'):
        for i, lv in enumerate(QUOTA[unit][kind], start=1):
            out.append(('e%02d-%s%d' % (unit, kind, i), FMT_OF[kind], lv, kind))
    return out


def load_bank(unit):
    p = BANK_ROOT / GRADE / ('u%02d' % unit) / 'practice.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    m = {}
    for t in d['types']:
        for pr in t['problems']:
            m[pr['id']] = pr
    return m


def check_unit(unit):
    path = BANK_ROOT / GRADE / ('u%02d' % unit) / 'exam.json'
    if not path.exists():
        errs.append('u%02d exam.json 이 없음' % unit)
        return
    d = json.loads(path.read_text(encoding='utf-8'))
    probs = d.get('problems', [])
    bank = load_bank(unit)

    exp = expected_ids(unit)
    got = [(p.get('id'), p.get('format'), p.get('level')) for p in probs]
    if [(i, f, l) for i, f, l, _k in exp] != got:
        errs.append('X1 u%02d id/format/level 이 할당표와 다름\n        기대=%s\n        실제=%s'
                    % (unit, [(i, f, l) for i, f, l, _k in exp], got))

    used_src = set()
    ans_pos = []
    for p, (eid, efmt, elv, kind) in zip(probs, exp):
        pid = p.get('id', '?')
        sp = p.get('stem_print') or ''

        # X4 공통
        for w in APP_WORDS:
            if w in sp:
                errs.append('X4 %s 발문에 앱 의존 표현 "%s"' % (pid, w))
        for field in ('stem_print', 'answer_print', 'hint', 'solution'):
            v = p.get(field) or ''
            m = KATEX_LEFT.search(v)
            if m:
                errs.append('X4 %s %s 에 KaTeX 잔재 "%s"' % (pid, field, m.group(1)))
        if not any(dm in sp for dm in DEMAND) and not sp.rstrip().rstrip('</b>').endswith('?') \
                and '?' not in sp[-12:]:
            errs.append('X4 %s 발문에 요구문이 없음: %s…' % (pid, sp[:40]))
        if not p.get('answer_format'):
            errs.append('X4 %s answer_format 누락' % pid)
        if VOICE_BAD.search(re.sub(r'<[^>]+>', '', p.get('hint') or '')):
            errs.append('X4 %s hint 가 문어체' % pid)
        if not (p.get('answer_print') or '').strip():
            errs.append('X4 %s answer_print 비어 있음' % pid)
        if not (p.get('solution') or '').strip():
            errs.append('X4 %s solution 비어 있음' % pid)
        if not (p.get('topic') or '').strip():
            warns.append('X4 %s topic 비어 있음' % pid)

        # X6 교육과정
        blob = sp + (p.get('solution') or '')
        for wbad in BANNED:
            if wbad in blob:
                errs.append('X6 %s 교육과정 밖 키워드 "%s"' % (pid, wbad))

        # X2 choice5
        if p.get('format') == 'choice5':
            ch = p.get('choices')
            if not isinstance(ch, list) or len(ch) != 5:
                errs.append('X2 %s 보기가 5개가 아님' % pid)
                ch = None
            ac = p.get('answer_choice')
            if not isinstance(ac, int) or not 1 <= ac <= 5:
                errs.append('X2 %s answer_choice 가 1~5 정수가 아님: %r' % (pid, ac))
                ac = None
            if ch is not None:
                nrm = [norm(c) for c in ch]
                if len(set(nrm)) != 5:
                    errs.append('X2 %s 보기에 중복 있음: %s' % (pid, ch))
                if ac is not None and norm(ch[ac - 1]) != norm(p.get('answer_print') or ''):
                    errs.append('X2 %s 정답 보기(%d번 "%s") != answer_print "%s"'
                                % (pid, ac, ch[ac - 1], p.get('answer_print')))
                nums = [NUMLIKE.match(norm(c)) for c in ch]
                if all(nums):
                    vals = [float(m.group(0).replace('−', '-')) for m in nums]
                    if vals != sorted(vals) and vals != sorted(vals, reverse=True):
                        warns.append('X2 %s 수치 보기가 정렬돼 있지 않음' % pid)
                dw = p.get('distractor_why')
                if not isinstance(dw, list) or len(dw) != 4:
                    errs.append('X2 %s distractor_why 는 4개 배열이어야 함' % pid)
            if ac is not None:
                ans_pos.append(ac)

        # X3 essay
        if p.get('format') == 'essay':
            rb = p.get('rubric')
            if not isinstance(rb, list) or not 2 <= len(rb) <= 4:
                errs.append('X3 %s rubric 은 2~4단계 배열이어야 함' % pid)
            else:
                tot = sum(int(s.get('points', 0)) for s in rb)
                if tot != 8:
                    errs.append('X3 %s rubric 합계 %d != 8' % (pid, tot))
                for s in rb:
                    if not (s.get('step') or '').strip():
                        errs.append('X3 %s rubric 에 빈 step' % pid)
            if '풀이 과정' not in sp:
                warns.append('X3 %s 발문에 "풀이 과정" 안내 없음' % pid)

        # X5 원본 대조
        if kind in ('cv', 'sh'):
            sid = p.get('source_id')
            src = bank.get(sid) if sid else None
            if not src:
                errs.append('X5 %s source_id "%s" 가 practice.json 에 없음' % (pid, sid))
            else:
                if sid in used_src:
                    errs.append('X5 %s source_id "%s" 중복 사용' % (pid, sid))
                used_src.add(sid)
                if src['level'] != elv:
                    errs.append('X5 %s 원본 level %s != 할당 %s' % (pid, src['level'], elv))
                if kind == 'sh' and norm(src['answer_print']) != norm(p.get('answer_print') or ''):
                    errs.append('X5 %s sh 정답이 원본과 다름: 원본"%s" 풀"%s"'
                                % (pid, src['answer_print'], p.get('answer_print')))
                if kind == 'cv' and norm(src['answer_print']) not in norm(p.get('answer_print') or '') \
                        and norm(p.get('answer_print') or '') not in norm(src['answer_print']):
                    warns.append('X5 %s cv 정답 "%s" 가 원본 "%s" 와 형태가 다름 — 사람이 확인'
                                 % (pid, p.get('answer_print'), src['answer_print']))
        else:
            if p.get('source_id'):
                warns.append('X5 %s 신규 문항인데 source_id 가 있음' % pid)

    from collections import Counter
    for pos, cnt in Counter(ans_pos).items():
        if cnt >= 4:
            warns.append('X2 u%02d 정답 위치 %d번이 %d회 — 편중' % (unit, pos, cnt))
    infos.append('u%02d 문항 %d개 점검' % (unit, len(probs)))


def load_pool():
    pool = {}
    for unit in QUOTA:
        path = BANK_ROOT / GRADE / ('u%02d' % unit) / 'exam.json'
        if not path.exists():
            errs.append('u%02d exam.json 없음' % unit)
            continue
        d = json.loads(path.read_text(encoding='utf-8'))
        for p in d.get('problems', []):
            pool[p['id']] = (unit, p)
    return pool


def check_sets():
    pool = load_pool()
    cfgs = sorted(SETS_DIR.glob('m3-exam-*.json'))
    if len(cfgs) != 6:
        errs.append('S1 회차 config 가 6개가 아님: %d개' % len(cfgs))
    used = {}
    for cp in cfgs:
        cfg = json.loads(cp.read_text(encoding='utf-8'))
        name = cfg['id']
        items = cfg['problems']
        if len(items) != 22:
            errs.append('S1 %s 문항 수 %d != 22' % (name, len(items)))
        pts = sum(it['points'] for it in items)
        if pts != 100:
            errs.append('S1 %s 배점 합 %d != 100' % (name, pts))
        fmts = {'choice5': 0, 'short': 0, 'essay': 0}
        lvls = {'L': 0, 'M': 0, 'H': 0}
        units_used = {}
        for it in items:
            pid = it['pid']
            if pid not in pool:
                errs.append('S3 %s pid "%s" 를 풀에서 못 찾음' % (name, pid))
                continue
            unit, p = pool[pid]
            if unit != it.get('unit'):
                errs.append('S3 %s pid "%s" unit 표기 %s != 실제 %d' % (name, pid, it.get('unit'), unit))
            fmts[p['format']] += 1
            lvls[p['level']] += 1
            units_used[unit] = units_used.get(unit, 0) + 1
            used.setdefault(pid, []).append(name)
            if p['format'] == 'essay' and it['points'] != 8:
                errs.append('S1 %s %s essay 배점 %d != 8' % (name, pid, it['points']))
            if p['format'] == 'short' and it['points'] != 4:
                errs.append('S1 %s %s short 배점 %d != 4' % (name, pid, it['points']))
            if p['format'] == 'choice5' and it['points'] not in (3, 4):
                errs.append('S1 %s %s choice 배점 %d not in {3,4}' % (name, pid, it['points']))
        if fmts != {'choice5': 15, 'short': 3, 'essay': 4}:
            errs.append('S1 %s format 구성 %s != choice15/short3/essay4' % (name, fmts))
        kq = KIND_QUOTA.get(cfg.get('difficulty_kind'))
        if kq is None:
            errs.append('S2 %s difficulty_kind 누락/무효: %r' % (name, cfg.get('difficulty_kind')))
        else:
            want = {'L': 0, 'M': 0, 'H': 0}
            want.update(kq)
            if lvls != want:
                errs.append('S2 %s 난이도 %s != %s' % (name, lvls, want))
        for u in range(7, 13):
            if not 1 <= units_used.get(u, 0) <= 4:
                errs.append('S4 %s 단원 %d 문항 수 %d (1~4 범위 밖)' % (name, u, units_used.get(u, 0)))
        h1 = sum(units_used.get(u, 0) for u in range(1, 7))
        if not 7 <= h1 <= 9:
            errs.append('S4 %s 1학기 문항 합 %d (7~9 범위 밖)' % (name, h1))
        for u in range(1, 7):
            if units_used.get(u, 0) > 2:
                errs.append('S4 %s 1학기 단원 %d 이 %d문항 (최대 2)' % (name, u, units_used[u]))
        infos.append('%s: %d문항 %d점 L%d M%d H%d' % (name, len(items), pts, lvls['L'], lvls['M'], lvls['H']))

    for pid, names in used.items():
        if len(names) > 1:
            errs.append('S3 "%s" 가 여러 회차에 사용됨: %s' % (pid, names))
    n_unused = len(pool) - len(used)
    (infos if n_unused == 0 else warns).append('풀 %d문항 중 %d개 사용, %d개 미사용' % (len(pool), len(used), n_unused))


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else '--all'
    if arg == '--sets':
        check_sets()
    elif arg == '--all':
        for u in QUOTA:
            check_unit(u)
    else:
        check_unit(int(arg.lstrip('u')))
    for s in infos:
        print('  ok   ' + s)
    for s in warns:
        print('  WARN ' + s)
    for s in errs:
        print('  FAIL ' + s)
    print('  오류 %d · 경고 %d' % (len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
