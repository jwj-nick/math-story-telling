"""verify_bank.py — 문제 은행 검증 (지면화의 안전장치)

원본 HTML에서 다시 추출해 은행과 대조한다. 사람이 다시 쓴 부분(stem_print/answer_print)이
원본 수학과 어긋나면 여기서 걸린다.

검사
  V1 문항 수      은행 문항 수 == 원본 추출 문항 수
  V2 정답 원자    answer_atoms == 원본 P(...)/MJ.check(...) 값 (순서까지)
  V3 합성 정답    answer_print 안에 모든 원자가 들어 있는가 (원자 "1" 은 생략 허용)
  V4 발문 규약    □·앱 의존 표현 없음 / 요구문 있음 / answer_format 있음
  V5 오개념       태그가 카탈로그에 존재 / 카드에 그 문제의 정답이 새지 않음
  V6 어투         학생에게 보이는 문구가 해요체인가 (문어체 '~다.' 종결 검출)

사용:
    python verify_bank.py <bank.json> [<misconceptions.json>]
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK_ROOT = ROOT / '30_content' / 'problem_bank'

APP_WORDS = ['□', '버튼', '슬라이더', '눌러', '탭을', '클릭', '위 그림에서 값을']
KATEX_LEFT = re.compile(r'(\$|\\dfrac|\\frac|\\overline|\\overrightarrow|\\overleftrightarrow|\\angle|\\times|\\div|\\pi)')
NUMERIC = re.compile(r'^[−\-]?\d+(\.\d+)?$')
DEMAND = ['하시오', '구하시오', '나타내시오', '쓰시오', '고르시오', '까요?', '얼마인가요']
VOICE_BAD = re.compile(r'(한다|된다|이다|뺀다|더한다|곱한다|나눈다|계산한다|넣는다|바뀐다|사라진다)\.')

errs, warns, infos = [], [], []


def norm(s):
    s = re.sub(r'<[^>]+>', '', s or '')
    return re.sub(r'\s+', '', s)


def norm_math(s):
    """V3 비교용. 중1 원자는 KaTeX 를 품은 채 추출되고 지면 정답은 HTML 이라, 그대로 비교하면
    V3(원자 포함)과 V4(KaTeX 금지)가 서로 반대를 요구한다. 양쪽을 같은 평면으로 내린다."""
    s = re.sub(r'<[^>]+>', '', s or '').replace('$', '')
    s = re.sub(r'\\(?:dfrac|frac)\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'\1/\2', s)
    s = re.sub(r'\\(?:overline|overrightarrow|overleftrightarrow|text|mathrm|mathbf)\s*\{([^{}]*)\}', r'\1', s)
    for a, b in (('\\angle', '∠'), ('\\times', '×'), ('\\div', '÷'), ('\\pi', 'π'),
                 ('\\triangle', '△'), ('\\cong', '≡'), ('\\cdot', '·')):
        s = s.replace(a, b)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    # 원본 정답은 객관식 번호(①②③…)를 달고 있는데 지면은 단답형이라 뗀다. 비교에서도 뗀다.
    s = re.sub(r'[①-⑳㉠-㉿]', '', s)
    s = re.sub(r'[{}\s]', '', s)
    return s.replace('-', '−')


def re_extract(bank):
    """원본을 다시 추출해서 (유형no, 문항idx) → atoms 맵을 만든다. 세대별로 추출기를 고른다."""
    src = ROOT / bank['meta']['source']
    gen = bank['meta'].get('generation', 'D')
    tool = Path(__file__).with_name(
        'extract_math2_p.py' if gen == 'D' else 'extract_gen_ac.py')
    if not src.exists() or not tool.exists():
        warns.append('원본 재추출 건너뜀 (source 또는 extractor 없음): %s' % src)
        return None
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / 'draft.json'
        subprocess.run([sys.executable, str(tool), str(src), str(bank['meta']['unit']), str(out)],
                       check=True, capture_output=True)
        d = json.loads(out.read_text(encoding='utf-8'))
    m = {}
    for t in d['types']:
        # ⚠️ p['idx'] 를 키로 쓰면 안 된다. 세대 A 의 idx 는 .q-num 값이라 난이도(L/M/H)마다
        #    1,2,3 으로 리셋된다 → L1·M1·H1 이 모두 idx=1 로 충돌해 유형당 9문항이 3개로 뭉개진다.
        #    은행 쪽도 enumerate 로 세므로 여기서도 순번으로 센다.
        for i, p in enumerate(t['problems'], start=1):
            m[(t['no'], i)] = p['answer_atoms']
    return m


def main():
    bank_path = Path(sys.argv[1])
    if not bank_path.is_absolute():
        bank_path = BANK_ROOT / bank_path
    bank = json.loads(bank_path.read_text(encoding='utf-8'))

    mis = None
    if len(sys.argv) > 2:
        mp = Path(sys.argv[2])
        if not mp.is_absolute():
            mp = BANK_ROOT / mp
        mis = json.loads(mp.read_text(encoding='utf-8'))

    src_atoms = re_extract(bank)

    n = 0
    for t in bank['types']:
        if VOICE_BAD.search(re.sub(r'<[^>]+>', '', t.get('principle', ''))):
            errs.append('V6 유형 %d principle 이 문어체입니다: %s' % (t['no'], t['principle'][:40]))
        for idx, p in enumerate(t['problems'], start=1):
            n += 1
            pid = p['id']

            # V2 정답 원자
            if src_atoms is not None:
                exp = src_atoms.get((t['no'], idx))
                if exp is None:
                    errs.append('V2 %s 원본에서 대응 문항을 찾지 못함 (유형%d #%d)' % (pid, t['no'], idx))
                elif not exp:
                    # 원본 앱에 자동 채점이 없는 문항(서술형·복수정답 등)은 추출값이 비어 있다.
                    # 은행 정답은 사람이 원본 해설을 읽고 채운 것이므로 오류가 아니라 확인 대상이다.
                    warns.append('V2 %s 원본에 기계 판독 가능한 정답이 없음 — 사람이 원본과 대조해야 함 (은행=%s)'
                                 % (pid, p['answer_atoms']))
                elif exp != p['answer_atoms']:
                    errs.append('V2 %s 정답 원자 불일치 원본=%s 은행=%s' % (pid, exp, p['answer_atoms']))

            # V3 합성 정답 — 원자가 전부 수치면 엄격, 텍스트/수식이면 경고
            # 단위는 R4 에 따라 답란에 따로 인쇄되므로 원자(`9개`, `$60°$`)와 맞추려면 다시 붙여서 본다.
            ap = norm_math((p['answer_print'] or '') + (p.get('answer_unit') or ''))
            strict = all(NUMERIC.match(a or '') for a in p['answer_atoms']) if p['answer_atoms'] else False
            for a in p['answer_atoms']:
                if a == '1':
                    continue
                # 양쪽 모두 정규화(+KaTeX 걷어내기)해서 비교한다. 한쪽만 정규화하면
                # "평행 (안 만남)" 처럼 공백이 든 정답이 완전히 같아도 불일치로 잡힌다.
                if norm_math(a) not in ap:
                    msg = 'V3 %s 원자 %s 가 지면 정답 "%s" 에 없음' % (pid, a, p['answer_print'])
                    (errs if strict else warns).append(msg + ('' if strict else ' (수식·서술형 — 사람이 확인)'))
            if not (p.get('answer_print') or '').strip():
                errs.append('V3 %s answer_print 가 비어 있음' % pid)

            # V4 발문 규약
            sp = p['stem_print']
            for w in APP_WORDS:
                if w in sp:
                    errs.append('V4 %s 발문에 앱 의존/모호 표현 "%s"' % (pid, w))
            for field in ('stem_print', 'answer_print', 'hint', 'solution'):
                v = p.get(field) or ''
                m = KATEX_LEFT.search(v)
                if m:
                    errs.append('V4 %s %s 에 KaTeX 잔재 "%s" — HTML(<sup>/유니코드/.frac)로 변환할 것'
                                % (pid, field, m.group(1)))
            if not any(d in sp for d in DEMAND) and not sp.rstrip().endswith('?'):
                errs.append('V4 %s 발문에 요구문이 없음: %s' % (pid, sp[:40]))
            if not p.get('answer_format'):
                errs.append('V4 %s answer_format 누락' % pid)
            if p.get('answer_unit') is None and '단위' not in (p.get('answer_format') or '') \
                    and '수로' not in (p.get('answer_format') or '') and '꼴로' not in (p.get('answer_format') or '') \
                    and '식으로' not in (p.get('answer_format') or ''):
                warns.append('V4 %s 단위/형태 지정이 모호할 수 있음: %s' % (pid, p.get('answer_format')))

            # V5 오개념
            if mis:
                for m in p.get('misconceptions', []):
                    it = mis['items'].get(m)
                    if not it:
                        errs.append('V5 %s 오개념 태그 "%s" 가 카탈로그에 없음' % (pid, m))
                        continue
                    leak = norm(p['answer_print'])
                    for field in ('counter', 'ask', 'empathy'):
                        if len(leak) >= 2 and leak in norm(it[field]):
                            errs.append('V5 %s 오개념 %d번 %s 에 정답 "%s" 노출' % (pid, it['no'], field, p['answer_print']))

            # V6 어투
            for field in ('hint',):
                if VOICE_BAD.search(re.sub(r'<[^>]+>', '', p.get(field, ''))):
                    errs.append('V6 %s %s 가 문어체입니다' % (pid, field))

    # V1 문항 수
    if src_atoms is not None:
        if len(src_atoms) != n:
            errs.append('V1 문항 수 불일치 원본=%d 은행=%d' % (len(src_atoms), n))
        else:
            infos.append('V1 문항 수 일치: %d' % n)

    # 오개념 카탈로그 자체 점검
    if mis:
        used = set()
        for t in bank['types']:
            for p in t['problems']:
                used.update(p.get('misconceptions', []))
        for k, it in mis['items'].items():
            if k not in used:
                warns.append('V5 오개념 %d번 "%s" 은 어떤 문항에도 붙지 않음' % (it['no'], k))
            for field in ('counter', 'ask'):
                if VOICE_BAD.search(re.sub(r'<[^>]+>', '', it[field])):
                    errs.append('V6 오개념 %d번 %s 가 문어체입니다' % (it['no'], field))
        infos.append('오개념 카탈로그 %d개 · 사용 %d개' % (len(mis['items']), len(used)))

    print('=== verify_bank: %s ===' % bank_path.name)
    for s in infos:
        print('  ok   ' + s)
    for s in warns:
        print('  WARN ' + s)
    for s in errs:
        print('  FAIL ' + s)
    print('  문항 %d · 오류 %d · 경고 %d' % (n, len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
