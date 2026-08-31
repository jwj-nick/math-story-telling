"""plan_exam3.py — 12단원 exam.json 풀(132문항)을 6회차(m3-exam-a~f)로 자동 배정.

제약:
  - 회차당 22문항 = 선택형(cn+cv) 15 + 단답(sh) 3 + 서술(es) 4, 배점 합 100
    (선택형 15개 중 11개 4점 + 4개 3점 = 56, 단답 3×4=12, 서술 4×8=32)
  - 난이도 quota(회차 kind별, 22문항 전체 기준): std L9M10H3(a/b/c) · easy L22(d) · hard M11H11(e/f)
  - 커버리지: 2학기(u07~12) 회차당 1~4문항 · 1학기(u01~06) 합 7~9 · 1학기 단원당 최대 2
  - 132문항 전부 정확히 1회씩 사용

무작위 그리디 + 백트래킹(재시도)으로 배정한다. 실행마다 다른 배정이 나올 수 있으나
verify_exam3.py --sets 로 항상 검증한다.

사용:
    python 70_tools/print/plan_exam3.py
    (성공하면 30_content/problem_bank/sets/exam/m3-exam-{a..f}.json 6개를 씀)
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
GRADE = 'math3'
UNITS = range(1, 13)

SHEETS = [
    ('m3-exam-a', 'std', '실전 모의고사 1회', '기본 9·보통 10·도전 3 — 실제 시험과 같은 난이도 배합'),
    ('m3-exam-b', 'std', '실전 모의고사 2회', '기본 9·보통 10·도전 3'),
    ('m3-exam-c', 'std', '실전 모의고사 3회', '기본 9·보통 10·도전 3'),
    ('m3-exam-d', 'easy', '워밍업 모의고사', '전부 기본 난이도 — 처음 시작할 때, 자신감을 채우는 회차'),
    ('m3-exam-e', 'hard', '도전 모의고사 1회', '보통 11·도전 11 — 실력이 붙은 뒤, 마무리용'),
    ('m3-exam-f', 'hard', '도전 모의고사 2회', '보통 11·도전 11'),
]
KIND_QUOTA = {'std': {'L': 9, 'M': 10, 'H': 3}, 'easy': {'L': 22}, 'hard': {'M': 11, 'H': 11}}


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
    """1학기/2학기 부분 제약을 배정 도중에도 미리 걸러 백트래킹을 줄인다."""
    if unit <= 6:
        h1 = sum(v for u, v in unit_counts.items() if u <= 6)
        if h1 + 1 > 9:
            return False
        if unit_counts.get(unit, 0) + 1 > 2:
            return False
    else:
        if unit_counts.get(unit, 0) + 1 > 4:
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

    # easy(전부 L)는 L 재고를 정확히 소진해야 하므로 가장 먼저 배정하고,
    # hard(M/H만, L 없음)를 다음에, 유연한 std(L/M/H 혼합)를 마지막에 배정한다.
    # 이렇게 해야 std 가 "남는 레벨"을 자연스럽게 흡수할 수 있다.
    order_key = {'easy': 0, 'hard': 1, 'std': 2}
    process_order = sorted(SHEETS, key=lambda s: order_key[s[1]])

    for name, kind, title, subtitle in process_order:
        target = sheet_level_target(kind)
        chosen = []
        unit_counts = {}
        lvl_left = dict(target)

        for fmt in ('essay', 'short', 'choice5'):
            need = FMT_NEED[fmt]
            for _ in range(need):
                # 남은 레벨 수요 중 아직 값이 있고, 해당 포맷/레벨 후보가 있는 것을 우선순위로 시도
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
                    return None  # 실패 — 재시도
                chosen.append(picked)
                remaining[fmt].remove(picked)
                lvl_left[picked['level']] -= 1
                unit_counts[picked['unit']] = unit_counts.get(picked['unit'], 0) + 1

        h1 = sum(v for u, v in unit_counts.items() if u <= 6)
        if not 7 <= h1 <= 9:
            return None
        for u in range(7, 13):
            if not 1 <= unit_counts.get(u, 0) <= 4:
                return None

        sheets_out.append((name, kind, title, subtitle, chosen))

    # 전부 소진됐는지 확인
    if any(remaining[k] for k in remaining):
        return None
    return sheets_out


def points_for(items_by_fmt_order):
    """15 선택형 중 11개 4점+4개 3점(합56), 단답 3×4=12, 서술 4×8=32 → 합 100."""
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
    for seed in range(2000):
        result = try_assign(pool, seed)
        if result:
            print('배정 성공 (seed=%d)' % seed)
            break
    if result is None:
        print('배정 실패 — 제약을 완화하거나 재시도 횟수를 늘리세요.')
        return 1

    SETS_DIR.mkdir(parents=True, exist_ok=True)
    for name, kind, title, subtitle, chosen in result:
        # 출력 순서: essay/short/choice5로 뽑았지만 파일은 choice5 -> short -> essay 순서로 정렬해 build_exam.py 가정과 맞춘다
        order = {'choice5': 0, 'short': 1, 'essay': 2}
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
        print('  wrote', out.name, len(chosen_sorted), 'items')
    return 0


if __name__ == '__main__':
    sys.exit(main())
