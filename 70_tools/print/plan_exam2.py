"""plan_exam2.py — 11단원 exam.json 풀(132문항)을 6회차(m2-exam-a~f)로 자동 배정.

plan_exam3.py 를 math2 에 맞춰 이식했다. 달라진 것은 학년·단원 수와 커버리지 제약뿐이다.

제약:
  - 회차당 22문항 = 선택형 15 + 단답 3 + 서술 4, 배점 합 100
    (선택형 15개 중 11개 4점 + 4개 3점 = 56, 단답 3×4=12, 서술 4×8=32)
  - 난이도 quota(회차 kind별, 22문항 전체 기준): std L9M10H3(a/b/c) · easy L22(d) · hard M11H11(e/f)
  - 커버리지: **모든 단원이 회차마다 1~3문항**, 1학기(u01~06) 합 11~13
    (중2 는 1학기 6단원·2학기 5단원이고 단원당 12문항이라, 회차당 1학기 12·2학기 10 이 자연스러운 몫이다)
  - 132문항 전부 정확히 1회씩 사용

사용:
    python 70_tools/print/plan_exam2.py
    (성공하면 30_content/problem_bank/sets/exam/m2-exam-{a..f}.json 6개를 씀)
"""
import json
import random
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BANK_ROOT = ROOT / '30_content' / 'problem_bank'
SETS_DIR = BANK_ROOT / 'sets' / 'exam'
GRADE = 'math2'
UNITS = range(1, 12)
H1_LAST = 6                      # 1학기 마지막 단원

SHEETS = [
    ('m2-exam-a', 'std', '실전 모의고사 1회', '기본 9·보통 10·도전 3 — 실제 시험과 같은 난이도 배합'),
    ('m2-exam-b', 'std', '실전 모의고사 2회', '기본 9·보통 10·도전 3'),
    ('m2-exam-c', 'std', '실전 모의고사 3회', '기본 9·보통 10·도전 3'),
    ('m2-exam-d', 'easy', '워밍업 모의고사', '전부 기본 난이도 — 처음 시작할 때, 자신감을 채우는 회차'),
    ('m2-exam-e', 'hard', '도전 모의고사 1회', '보통 11·도전 11 — 실력이 붙은 뒤, 마무리용'),
    ('m2-exam-f', 'hard', '도전 모의고사 2회', '보통 11·도전 11'),
]
KIND_QUOTA = {
    'std':  {'L': 9, 'M': 10, 'H': 3},
    'easy': {'L': 22},
    'hard': {'M': 11, 'H': 11},
}
MAX_PER_UNIT = 3
H1_RANGE = (11, 13)


def load_pool():
    items = []
    for u in UNITS:
        d = json.loads((BANK_ROOT / GRADE / ('u%02d' % u) / 'exam.json').read_text(encoding='utf-8'))
        for p in d['problems']:
            items.append({'id': p['id'], 'unit': u, 'format': p['format'], 'level': p['level']})
    return items


def sheet_level_target(kind):
    want = {'L': 0, 'M': 0, 'H': 0}
    want.update(KIND_QUOTA[kind])
    return want


def unit_ok_incremental(unit_counts, unit):
    """배정 도중에도 단원 상한과 1학기 상한을 미리 걸러 백트래킹을 줄인다."""
    if unit_counts.get(unit, 0) + 1 > MAX_PER_UNIT:
        return False
    if unit <= H1_LAST:
        h1 = sum(v for u, v in unit_counts.items() if u <= H1_LAST)
        if h1 + 1 > H1_RANGE[1]:
            return False
    return True


def try_assign(pool, seed):
    rnd = random.Random(seed)
    remaining = {'choice5': [], 'short': [], 'essay': []}
    for it in pool:
        remaining[it['format']].append(it)
    for k in remaining:
        rnd.shuffle(remaining[k])

    FMT_NEED = {'choice5': 15, 'short': 3, 'essay': 4}
    sheets_out = []

    # easy(전부 L)가 L 재고를 정확히 소진해야 하므로 먼저, hard(M/H) 다음, 유연한 std 를 마지막에.
    order_key = {'easy': 0, 'hard': 1, 'std': 2}
    process_order = sorted(SHEETS, key=lambda s: order_key[s[1]])

    for name, kind, title, subtitle in process_order:
        target = sheet_level_target(kind)
        chosen = []
        unit_counts = {}
        lvl_left = dict(target)

        for fmt in ('essay', 'short', 'choice5'):
            for _ in range(FMT_NEED[fmt]):
                cand_levels = [lv for lv, n in lvl_left.items() if n > 0]
                rnd.shuffle(cand_levels)
                picked = None
                for lv in cand_levels:
                    candidates = [it for it in remaining[fmt] if it['level'] == lv
                                  and unit_ok_incremental(unit_counts, it['unit'])]
                    if candidates:
                        picked = rnd.choice(candidates)
                        break
                if picked is None:
                    return None
                chosen.append(picked)
                remaining[fmt].remove(picked)
                lvl_left[picked['level']] -= 1
                unit_counts[picked['unit']] = unit_counts.get(picked['unit'], 0) + 1

        h1 = sum(v for u, v in unit_counts.items() if u <= H1_LAST)
        if not H1_RANGE[0] <= h1 <= H1_RANGE[1]:
            return None
        for u in UNITS:
            if not 1 <= unit_counts.get(u, 0) <= MAX_PER_UNIT:
                return None

        sheets_out.append((name, kind, title, subtitle, chosen))

    if any(remaining[k] for k in remaining):
        return None
    return sheets_out


def points_for(items_by_fmt_order):
    """선택형 15 중 11개 4점 + 4개 3점(56), 단답 3×4=12, 서술 4×8=32 → 합 100."""
    pts = {}
    choice_ids = [it['id'] for it in items_by_fmt_order if it['format'] == 'choice5']
    four = set(choice_ids[:11])
    for it in items_by_fmt_order:
        if it['format'] == 'choice5':
            pts[it['id']] = 4 if it['id'] in four else 3
        elif it['format'] == 'short':
            pts[it['id']] = 4
        else:
            pts[it['id']] = 8
    return pts


def main():
    pool = load_pool()
    if len(pool) != 132:
        print('경고: 풀 문항 수가 132가 아님: %d' % len(pool))

    result = None
    for seed in range(4000):
        result = try_assign(pool, seed)
        if result:
            print('배정 성공 (seed=%d)' % seed)
            break
    if result is None:
        print('배정 실패 — 제약을 완화하거나 재시도 횟수를 늘리세요.')
        return 1

    SETS_DIR.mkdir(parents=True, exist_ok=True)
    order = {'choice5': 0, 'short': 1, 'essay': 2}
    for name, kind, title, subtitle, chosen in result:
        chosen_sorted = sorted(chosen, key=lambda it: (order[it['format']], it['unit'], it['id']))
        pts = points_for(chosen_sorted)
        cfg = {
            'id': name, 'kind': 'exam', 'difficulty_kind': kind, 'grade': GRADE,
            'title': title, 'subtitle': subtitle, 'time_min': 45, 'total_points': 100,
            'outputs': ['Q', 'K'],
            'problems': [{'unit': it['unit'], 'pid': it['id'], 'points': pts[it['id']]} for it in chosen_sorted],
        }
        out = SETS_DIR / (name + '.json')
        out.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
        units = sorted(set(it['unit'] for it in chosen_sorted))
        print('  wrote %s — %d문항 · 단원 %s' % (out.name, len(chosen_sorted), units))
    return 0


if __name__ == '__main__':
    sys.exit(main())
