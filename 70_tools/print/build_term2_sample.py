"""build_term2_sample.py — 중1 2학기 기말(교과서 6·7단원) 그림 문제 샘플 6문항

figgen 으로 그림을 계산해 그리고, build_exam 의 Q/K 빌더로 문제지·해답묶음 HTML을 만든다.
정답 수치는 아래 check() 에서 다시 계산해 문항의 정답과 맞는지 확인한다.

사용: python build_term2_sample.py <html 출력 폴더> <pdf 출력 폴더>
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_exam  # noqa: E402
import figgen as F  # noqa: E402

PI = 'π'
X = F.X_ITAL

# ───────────────────────────── 문항 1: 오각형의 내각·외각
INT1 = [105, 120, 100, 95, 120]          # A B C D E (반시계), C는 외각 80°로 보이고 E가 x
P1 = {
    'id': 't2s-01', 'format': 'choice5', 'level': 'M', 'unit': 6, 'points': 4,
    'topic': '다각형의 내각과 외각',
    'stem_print': '다음 그림에서 ∠' + X + '의 크기는?',
    'figure': F.fig_pentagon_exterior(INT1, show={0: '105°', 1: '120°', 3: '95°'}, ext_at=2, unknown_at=4),
    'figure_sol': F.fig_pentagon_exterior(INT1, show={0: '105°', 1: '120°', 3: '95°'}, ext_at=2, unknown_at=4,
                                          sol_label='100°'),
    'choices': ['100°', '110°', '120°', '130°', '140°'], 'answer_choice': 3,
    'distractor_why': ['계산 없이 그림 모양만 보고 어림함 (그림만으로는 10° 차이를 구별할 수 없어요)',
                       '계산 없이 그림 모양만 보고 어림함',
                       '덧셈 실수: 105 + 120 + 100 + 95 = 420을 다시 확인해요',
                       '외각 80°를 그대로 내각처럼 더해 540 − 400 = 140으로 계산함'],
    'answer_print': '120°',
    'hint': '오각형의 내각의 합은 180° × (5 − 2) = 540°예요. 그림의 80°는 <b>외각</b>이라 내각으로 바꿔야 해요.',
    'solution': '① 오각형의 내각의 합: 180° × 3 = 540°<br>'
                '② 80°는 변을 연장한 선과 이루는 <b>외각</b>이므로 그 꼭짓점의 내각은 180° − 80° = 100°<br>'
                '③ 105° + 120° + 100° + 95° + ∠' + X + ' = 540° → ∠' + X + ' = 120°',
}

# ───────────────────────────── 문항 2: 한 원에서 호·현·중심각
P2 = {
    'id': 't2s-02', 'format': 'choice5', 'level': 'M', 'unit': 6, 'points': 4,
    'topic': '호·현·중심각의 관계',
    'stem_print': '다음 그림의 원 O에서 ∠AOB = 40°, ∠COD = 120°이고 호 AB의 길이가 6 cm일 때, '
                  '다음 중 옳지 <b>않은</b> 것은?',
    'figure': F.fig_two_sectors(3.2, 40, 120),
    'choices': ['호 CD의 길이는 18 cm이다.',
                '부채꼴 COD의 넓이는 부채꼴 AOB의 넓이의 3배이다.',
                '현 CD의 길이는 현 AB의 길이의 3배이다.',
                '∠AOB의 크기가 2배가 되면 호 AB의 길이도 2배가 된다.',
                '원 O의 둘레의 길이는 54 cm이다.'],
    'answer_choice': 3,
    'distractor_why': ['중심각이 3배 → 호도 3배: 6 × 3 = 18 cm, 옳음',
                       '부채꼴의 넓이도 중심각에 정비례하므로 옳음',
                       '호의 길이는 중심각에 정비례하므로 옳음',
                       '40° : 360° = 6 : (둘레) → 둘레 54 cm, 옳음'],
    'answer_print': '현 CD는 현 AB의 3배가 아니다',
    'hint': '한 원에서 <b>호의 길이와 부채꼴의 넓이</b>는 중심각에 정비례해요. <b>현의 길이</b>는 정비례하지 않아요.',
    'solution': '중심각이 3배이면 호와 부채꼴 넓이는 3배가 되지만, 현은 3배보다 짧아요. '
                '그림에서 현 CD를 현 AB 세 개를 이은 꺾은선과 비교하면 현 CD가 더 짧다는 것을 볼 수 있어요. '
                '따라서 옳지 않은 것은 ③이에요.',
}

# ───────────────────────────── 문항 3: 그림을 보고 입체 판별 → 면·모서리·꼭짓점
P3 = {
    'id': 't2s-03', 'format': 'choice5', 'level': 'M', 'unit': 7, 'points': 4,
    'topic': '다면체의 구성 요소',
    'stem_print': '다음 그림과 같은 입체도형의 면의 개수를 <i>a</i>, 모서리의 개수를 <i>b</i>, '
                  '꼭짓점의 개수를 <i>c</i>라 할 때, <i>a</i> + <i>b</i> − <i>c</i>의 값은?',
    'figure': F.fig_frustum(),
    'choices': ['7', '10', '11', '12', '17'], 'answer_choice': 4,
    'distractor_why': ['모서리를 옆모서리만 세지 않고 10개로 셈: 7 + 10 − 10',
                       '오각뿔(면 6, 모서리 10, 꼭짓점 6)로 잘못 봄',
                       '두 밑면 중 하나만 세어 면을 6개로 셈',
                       '꼭짓점을 한 밑면의 5개만 셈: 7 + 15 − 5'],
    'answer_print': '12',
    'hint': '먼저 그림이 무슨 입체인지 이름을 붙여요. 두 밑면이 평행하고 크기가 다른 오각형이면 <b>오각뿔대</b>예요.',
    'solution': '그림은 오각뿔대예요. 면은 밑면 2 + 옆면 5 = 7, 모서리는 5 × 3 = 15, 꼭짓점은 5 × 2 = 10이에요. '
                '따라서 <i>a</i> + <i>b</i> − <i>c</i> = 7 + 15 − 10 = 12',
}

# ───────────────────────────── 문항 4: 색칠한 부분의 둘레
P4 = {
    'id': 't2s-04', 'format': 'short', 'level': 'M', 'unit': 6, 'points': 4,
    'topic': '색칠한 부분의 둘레',
    'stem_print': '다음 그림에서 색칠한 부분의 둘레의 길이를 구하시오.',
    'figure': F.fig_sector_band(6, 3, 120),
    'answer_print': '(6' + PI + ' + 6)', 'answer_unit': 'cm',
    'answer_format': '○π + △ 꼴',
    'hint': '둘레는 <b>바깥 호 + 안쪽 호 + 곧은 선분 2개</b>예요. 선분을 빠뜨리기 쉬워요.',
    'solution': '바깥 호: 2' + PI + ' × 6 × 120/360 = 4' + PI + '<br>'
                '안쪽 호: 2' + PI + ' × 3 × 120/360 = 2' + PI + '<br>'
                '곧은 선분: 3 + 3 = 6<br>'
                '둘레 = 4' + PI + ' + 2' + PI + ' + 6 = (6' + PI + ' + 6) cm',
}

# ───────────────────────────── 문항 5: 회전체의 단면
P5 = {
    'id': 't2s-05', 'format': 'short', 'level': 'M', 'unit': 7, 'points': 4,
    'topic': '회전체의 단면',
    'stem_print': '다음 그림의 사다리꼴을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체를 '
                  '<b>회전축을 포함하는 평면</b>으로 자른 단면의 넓이를 구하시오.',
    'figure': F.fig_rotation_trapezoid(2, 4, 3),
    'figure_sol': F.fig_rotation_trapezoid(2, 4, 3, mirror=True),
    'answer_print': '18', 'answer_unit': 'cm²',
    'answer_format': '수',
    'hint': '회전체는 원뿔대예요. 회전축을 포함하는 평면으로 자르면 처음 사다리꼴과 그 거울상이 붙은 모양이 나와요.',
    'solution': '단면은 윗변 2 × 2 = 4 cm, 아랫변 4 × 2 = 8 cm, 높이 3 cm인 등변사다리꼴이에요.<br>'
                '넓이 = (4 + 8) × 3 ÷ 2 = 18 cm²<br>'
                '처음 사다리꼴의 넓이 9 cm²만 답하면 틀려요. 단면은 그 2배예요.',
}

# ───────────────────────────── 문항 6: 반구 + 원뿔 (서술형)
P6 = {
    'id': 't2s-06', 'format': 'essay', 'level': 'M', 'unit': 7, 'points': 8,
    'topic': '붙인 입체의 부피와 겉넓이',
    'stem_print': '다음 그림은 반구와 원뿔을 붙여 만든 입체도형이다. 이 입체도형의 부피와 겉넓이를 각각 구하시오.',
    'figure': F.fig_hemi_cone(3, 4, slant=5),
    'answer_print': '부피 30' + PI + ' cm³, 겉넓이 33' + PI + ' cm²', 'answer_unit': None,
    'hint': '부피는 두 입체를 더해요. 겉넓이는 <b>붙은 원(밑면)은 바깥에 드러나지 않으니</b> 빼고 더해요.',
    'solution': '반구의 부피 = (4/3)' + PI + ' × 3³ ÷ 2 = 18' + PI + '<br>'
                '원뿔의 부피 = (1/3) × ' + PI + ' × 3² × 4 = 12' + PI + '<br>'
                '부피 = 18' + PI + ' + 12' + PI + ' = 30' + PI + ' cm³<br>'
                '반구의 곡면 = 4' + PI + ' × 3² ÷ 2 = 18' + PI + '<br>'
                '원뿔의 옆면 = ' + PI + ' × 3 × 5 = 15' + PI + '<br>'
                '겉넓이 = 18' + PI + ' + 15' + PI + ' = 33' + PI + ' cm² (붙은 원 9' + PI + '은 넣지 않아요)',
    'rubric': [{'step': '반구의 부피 18π를 구함', 'points': 2},
               {'step': '원뿔의 부피 12π를 구하고 부피 30π cm³를 구함', 'points': 2},
               {'step': '반구의 곡면 18π와 원뿔의 옆면 15π를 각각 구함', 'points': 2},
               {'step': '붙은 원을 빼고 겉넓이 33π cm²를 구함', 'points': 2}],
}

PROBLEMS = [P1, P2, P3, P4, P5, P6]


def check():
    """정답을 다시 계산한다. 하나라도 어긋나면 멈춘다."""
    assert 540 - (105 + 120 + (180 - 80) + 95) == 120
    assert abs(6 * 120 / 40 - 18) < 1e-9 and abs(6 * 360 / 40 - 54) < 1e-9
    # 현은 정비례하지 않음: chord = 2R sin(θ/2)
    R = 1.0
    assert abs(2 * R * math.sin(math.radians(60)) / (2 * R * math.sin(math.radians(20))) - 3) > 0.3
    n = 5
    assert (n + 2) + 3 * n - 2 * n == 12
    per = 2 * math.pi * 6 / 3 + 2 * math.pi * 3 / 3 + 6
    assert abs(per - (6 * math.pi + 6)) < 1e-9
    assert (4 + 8) * 3 / 2 == 18
    vol = 4 / 3 * math.pi * 27 / 2 + math.pi * 9 * 4 / 3
    surf = 4 * math.pi * 9 / 2 + math.pi * 3 * 5
    assert abs(vol - 30 * math.pi) < 1e-9 and abs(surf - 33 * math.pi) < 1e-9
    assert 3 ** 2 + 4 ** 2 == 5 ** 2  # 그림의 모선 5 cm 와 반지름·높이가 맞는지
    for p in PROBLEMS:
        if p['format'] == 'choice5':
            assert len(p['choices']) == 5 and len(p['distractor_why']) == 4
        if p['format'] == 'essay':
            assert sum(s['points'] for s in p['rubric']) == p['points']
    print('check OK: 6문항 정답 재계산 일치')


def head_block(cfg, kind_label):
    return ('<div class="head">\n'
            '  <div class="crumb">중1 수학 · 2학기 기말 대비 · 교과서 6단원 평면도형 · 7단원 입체도형</div>\n'
            '  <h1>' + cfg['title'] + ' <span style="font-size:11pt;color:#888;font-weight:700">— '
            + kind_label + '</span></h1>\n'
            '  <div class="sub">' + cfg['subtitle'] + '</div>\n</div>\n')


def main():
    check()
    html_dir, pdf_dir = Path(sys.argv[1]), Path(sys.argv[2])
    html_dir.mkdir(parents=True, exist_ok=True)
    cfg = {'id': 'm1-term2-sample', 'grade': 'math1', 'title': '그림 문제 샘플',
           'subtitle': '그림을 읽어야 풀리는 도형 문제 6개 · 형식 확인용', 'time_min': 15, 'total_points': 28}
    build_exam.head_block = head_block
    resolved = [({'unit': p['unit'], 'points': p['points']}, p) for p in PROBLEMS]
    resolved_k = [(it, dict(p, figure=p.get('figure_sol', p['figure']))) for it, p in resolved]
    plan = []
    for kind, html, kname in (('Q', build_exam.build_Q(cfg, resolved), '문제지'),
                              ('K', build_exam.build_K(cfg, resolved_k), '해답묶음')):
        f = html_dir / (cfg['id'] + '_' + kind + '.html')
        f.write_text(html, encoding='utf-8')
        plan.append({'html': str(f.resolve()), 'pdf': str((pdf_dir / ('샘플_그림문제_' + kname + '.pdf')).resolve())})
    (html_dir / (cfg['id'] + '_pdfplan.json')).write_text(json.dumps(plan, ensure_ascii=False, indent=2),
                                                         encoding='utf-8')
    bank = [{k: v for k, v in p.items()} for p in PROBLEMS]
    (html_dir / (cfg['id'] + '_bank.json')).write_text(json.dumps(bank, ensure_ascii=False, indent=1),
                                                      encoding='utf-8')
    print('html -> %s' % html_dir)


if __name__ == '__main__':
    main()
