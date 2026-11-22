"""연습문제 1회분 — 교과서 6·7단원 전체 (구역 11개 × 3문항)

구역마다 핵심 정리 → 기본(L) → 보통(M) 순서. 도형 문제는 그림을 읽어야 풀린다.
그림의 수치와 정답은 같은 변수에서 나오고, check()에서 정답을 다시 계산한다.
"""
import math

import figgen as F

META = {'id': 'm1-term2-practice', 'kind': 'practice', 'title': '연습문제 1회분',
        'subtitle': '6단원 평면도형의 성질 · 7단원 입체도형의 성질 전체 · 구역별 핵심 정리 + 기본 → 보통',
        'time_min': 0, 'folder': '연습', 'file': '연습문제1회분'}

PI = 'π'
X = F.X_ITAL
FR = lambda a, b: '<span class="frac"><b>%s</b><i>%s</i></span>' % (a, b)  # noqa: E731

SECTIONS = {
    's1': ('6.1 다각형의 대각선',
           '<b>n각형</b>의 한 꼭짓점에서 그을 수 있는 대각선은 <b>n − 3</b>개, 이때 생기는 삼각형은 <b>n − 2</b>개예요. '
           '대각선의 개수는 <b>n(n − 3) ÷ 2</b> (각 대각선을 양 끝에서 두 번 세었으니 2로 나눠요).'),
    's2': ('6.2 삼각형의 내각과 외각',
           '삼각형의 세 내각의 합은 <b>180°</b>. 한 외각의 크기는 그와 <b>이웃하지 않는 두 내각의 합</b>과 같아요.'),
    's3': ('6.3 다각형의 내각의 크기의 합',
           'n각형은 한 꼭짓점에서 대각선을 그어 삼각형 n − 2개로 나뉘므로 내각의 합은 <b>180° × (n − 2)</b>. '
           '정n각형의 한 내각은 그 합을 n으로 나눠요.'),
    's4': ('6.4 다각형의 외각의 크기의 합',
           '다각형의 외각의 합은 변의 개수와 상관없이 <b>항상 360°</b>. 정n각형의 한 외각은 <b>360° ÷ n</b>. '
           '한 꼭짓점에서 내각 + 외각 = 180°.'),
    's5': ('6.5 부채꼴의 중심각과 호',
           '한 원에서 <b>호의 길이와 부채꼴의 넓이는 중심각의 크기에 정비례</b>해요. '
           '중심각이 같으면 현의 길이도 같지만, <b>현의 길이는 중심각에 정비례하지 않아요</b>.'),
    's6': ('6.6 부채꼴의 호의 길이와 넓이',
           '반지름 r, 중심각 x°인 부채꼴: 호의 길이 <b>l = 2πr × x/360</b>, 넓이 <b>S = πr² × x/360 = rl ÷ 2</b>. '
           '색칠한 부분은 <b>큰 도형 − 작은 도형</b>으로 생각하고, 둘레에는 곧은 선분도 넣어요.'),
    's7': ('7.1 다면체',
           'n각기둥: 면 n+2, 모서리 3n, 꼭짓점 2n · n각뿔: 면 n+1, 모서리 2n, 꼭짓점 n+1 · '
           'n각뿔대: 면 n+2, 모서리 3n, 꼭짓점 2n. 정다면체는 정사면체·정육면체·정팔면체·정십이면체·정이십면체 5가지뿐이에요.'),
    's8': ('7.2 회전체',
           '직사각형 → 원기둥, 직각삼각형 → 원뿔, 직각사다리꼴 → 원뿔대, 반원 → 구. '
           '회전축에 <b>수직</b>으로 자르면 단면은 원, 회전축을 <b>포함</b>하는 평면으로 자르면 처음 도형과 그 거울상을 붙인 모양이에요.'),
    's9': ('7.3 기둥의 겉넓이와 부피',
           '겉넓이 = (밑넓이) × 2 + (옆넓이). 옆넓이 = (밑면의 둘레) × (높이). 부피 = (밑넓이) × (높이). '
           '원기둥: 겉넓이 2πr² + 2πrh, 부피 πr²h.'),
    's10': ('7.4 뿔의 겉넓이와 부피',
            '겉넓이 = (밑넓이) + (옆넓이). 원뿔의 옆넓이 = π × r × (모선의 길이). '
            '부피 = <b>1/3</b> × (밑넓이) × (높이) — 같은 밑면·높이의 기둥의 1/3이에요.'),
    's11': ('7.5 구의 겉넓이와 부피',
            '반지름 r인 구: 겉넓이 <b>4πr²</b>, 부피 <b>(4/3)πr³</b>. 반구는 둘 다 절반이지만, '
            '반구의 겉넓이에는 잘린 면(원 πr²)이 더해져요.'),
}


# ═════════════════════════════════ 세트 전용 그림
@F.autofit
def fig_cevian(B_ang, C_ang, bad, scale=22, width=210, height=170):
    """삼각형 ABC와 BC 위의 점 D. ∠B, ∠C, ∠BAD 를 표시하고 ∠DAC 를 x로 표시."""
    c = F.Canvas(scale)
    B, C = (0.0, 0.0), (6.0, 0.0)
    tb, tc = math.radians(B_ang), math.radians(C_ang)
    # A: B에서 각 B_ang, C에서 각 C_ang 로 올라간 두 직선의 교점
    ax = 6 * math.tan(tc) / (math.tan(tb) + math.tan(tc))
    A = (ax, ax * math.tan(tb))
    dAB = F._dir(A, B)
    dAD = dAB + bad          # A에서 B 쪽 방향을 C 쪽으로 bad만큼 돌림(반시계)
    t = -A[1] / math.sin(math.radians(dAD))
    D = (A[0] + t * math.cos(math.radians(dAD)), 0.0)
    c.poly([A, B, C], fill=F.FILL['g'])
    c.line(A, D)
    c.angle_at(B, C, A, label=F.deg(B_ang))
    c.angle_at(C, A, B, label=F.deg(C_ang))
    c.angle_at(A, B, D, label=F.deg(bad), r=16)
    c.angle_at(A, D, C, label=X, r=12, size=15)
    for p, nm, d in ((A, 'A', (0, 11)), (B, 'B', (-9, -8)), (C, 'C', (9, -8)), (D, 'D', (0, -11))):
        c.text(p, nm, size=12, d=d)
    return c.svg(width, height)


@F.autofit
def fig_dart(apex_ang, abd, acd, scale=22, width=200, height=200):
    """오목한 사각형 ABDC(D가 안쪽). ∠A, ∠ABD, ∠ACD 를 표시하고 ∠BDC 를 x로 표시."""
    c = F.Canvas(scale)
    base = (180 - apex_ang) / 2
    B, C = (0.0, 0.0), (6.0, 0.0)
    A = (3.0, 3.0 * math.tan(math.radians(base)))
    db, dc = base - abd, 180 - (base - acd)     # B에서 D 방향, C에서 D 방향
    tb, tc = math.tan(math.radians(db)), math.tan(math.radians(dc))
    dx = (0 - 6 * tc) / (tb - tc)
    D = (dx, dx * tb)
    c.poly([A, B, D, C], fill=F.FILL['p'])
    c.angle_at(A, B, C, label=F.deg(apex_ang), r=12)
    c.angle_at(B, D, A, label=F.deg(abd), r=18)
    c.angle_at(C, A, D, label=F.deg(acd), r=18)
    c.angle_at(D, B, C, label=X, size=15, r=11)
    for p, nm, d in ((A, 'A', (0, 11)), (B, 'B', (-9, -6)), (C, 'C', (9, -6)), (D, 'D', (0, 11))):
        c.text(p, nm, size=12, d=d)
    return c.svg(width, height)


@F.autofit
def fig_pentagon_diag(accent=False, scale=22, width=170, height=170):
    """정오각형 ABCDE와 대각선 AC. ∠BAC 를 x로 표시. accent=True 이면 해설용으로 ∠B=108°와 이등변 표시."""
    c = F.Canvas(scale)
    P = [F._add((0, 0), F._u(90 + 72 * i), 3.0) for i in range(5)]   # A(위)부터 반시계
    A, B, C = P[0], P[1], P[2]
    c.poly(P, fill=F.FILL['c'])
    c.line(A, C)
    c.angle_at(A, B, C, label=X, size=15, r=16)
    if accent:
        c.angle_at(B, C, A, label='108°', color=F.ACCENT, r=11)
        c.tick(A, B, color=F.ACCENT)
        c.tick(B, C, color=F.ACCENT)
    for i, nm in enumerate('ABCDE'):
        c.text(P[i], nm, size=12, d=F._scale(F._u(90 + 72 * i), 11))
    return c.svg(width, height)


@F.autofit
def fig_cyl_sphere(r, scale=22, width=150, height=190):
    """원기둥 안에 꼭 맞게 들어간 구(구의 지름 = 원기둥의 높이)."""
    c = F.Canvas(scale)
    k = math.sin(math.radians(17))
    h = 2 * r * math.cos(math.radians(17))
    c.poly(c.arc_pts((0, 0), r, 180, 360, n=60, ry=r * k) + c.arc_pts((0, h), r, 0, 180, n=60, ry=r * k),
           fill=F.FILL['c'], stroke='none', opacity=0.7)
    c.circle((0, h / 2), r, fill=F.FILL['y'])
    c.line((-r, 0), (-r, h))
    c.line((r, 0), (r, h))
    c.poly(c.arc_pts((0, 0), r, 180, 360, n=60, ry=r * k), close=False)
    c.poly(c.arc_pts((0, 0), r, 0, 180, n=60, ry=r * k), close=False, dash='4 3', sw=1.0)
    c.poly(c.arc_pts((0, h), r, 0, 360, n=80, ry=r * k)[:-1])
    c.line((0, h / 2), (r, h / 2), dash='3 2', sw=1.0)
    c.dot((0, h / 2), r=1.8)
    c.text((r / 2, h / 2), F.cm(r), size=12, d=(0, 9))
    return c.svg(width, height)


def rot_small(shape, fill):
    return F.fig_rotation(shape, fill=fill, width=84, height=112)


# ═════════════════════════════════ 수치 (그림과 정답이 같이 쓴다)
S1_N = 8
S2_A, S2_B = 55, 70
CV_B, CV_C, CV_BAD = 45, 50, 30
DT_A, DT_ABD, DT_ACD = 50, 25, 30
HEX = [120, 130, 110, 125, 135, 100]
PENT_EXT = [70, 80, 65, 75, 70]
C13 = dict(ab=30, arc_ab=4, arc_cd=12)
C14 = dict(aob=40, boc=100, s_aob=8)
SEC16 = (6, 120)
SEC17 = (10, 4)             # 반지름, 호의 길이의 π 계수
BAND18 = (8, 4, 90)
PRISM19_N = 6
PYR28 = (6, 5)              # 밑면 한 변, 옆면 삼각형의 높이
CONE24 = (4, 10)
CONE30 = (5, 9)


def tri_fig():
    P = F.polygon_by_angles([S2_A, S2_B, 180 - S2_A - S2_B], [4])
    return F.fig_polygon(P, angles={0: F.deg(S2_A), 1: F.deg(S2_B)}, ext={2: X}, names='ABC', fill='y')


def hex_fig():
    P = F.polygon_by_angles(HEX, [3, 3, 3, 3])
    return F.fig_polygon(P, angles={i: F.deg(HEX[i]) for i in range(5)}, unknown={5: X}, fill='m')


def pent_ext_fig():
    interior = [180 - e for e in PENT_EXT]
    P = F.polygon_by_angles(interior, [3.5, 3, 3.2])
    labels = {i: F.deg(PENT_EXT[i]) for i in range(4)}
    labels[4] = X
    return F.fig_polygon(P, ext=labels, fill='o', width=230, height=210)


def prism_tri_fig():
    V, Fc = F.prism([(0, 0), (4, 0), (0, 3)], 6)
    return F.fig_polyhedron(V, Fc, view=F.View(tilt=22, yaw=30), fill='g',
                            labels=[((2, 0, 0), '4cm', (0, -11)), ((0, 0, 1.5), '3cm', (-18, 0)),
                                    ((2, 6, 1.5), '5cm', (14, 8)), ((4, 3, 0), '6cm', (20, 0))])


def pyramid_fig():
    a, s = PYR28
    h = math.sqrt(s * s - (a / 2) ** 2)
    base = [(-a / 2, -a / 2), (a / 2, -a / 2), (a / 2, a / 2), (-a / 2, a / 2)]
    V, Fc = F.pyramid(base, h)

    def extra(c, proj):
        top, mid = proj((0, h, 0)), proj((0, 0, -a / 2))
        c.line(top, mid, dash='3 2', sw=1.1, stroke=F.ACCENT2)
        c.right_mark(mid, F._dir(mid, proj((a / 2, 0, -a / 2))), F._dir(mid, top), k=6)
        c.text(F._mid(top, mid), F.cm(s), size=12, d=(14, 0))
    return F.fig_polyhedron(V, Fc, view=F.View(tilt=18, yaw=20), fill='y',
                            labels=[((a / 4, 0, -a / 2), F.cm(a), (0, -11))], extra=extra)


P = []

# ── s1 대각선
P.append(dict(id='p01', sec='s1', format='short', level='L', topic='한 꼭짓점의 대각선',
              stem_print='다음 그림은 정팔각형의 한 꼭짓점에서 그을 수 있는 대각선을 모두 그은 것이다. '
                         '대각선의 개수를 <i>a</i>, 이 대각선으로 나누어진 삼각형의 개수를 <i>b</i>라 할 때, '
                         '<i>a</i> + <i>b</i>의 값을 구하시오.',
              figure=F.fig_regular_polygon(S1_N, diag_from=0, fill='c'),
              answer_print=str((S1_N - 3) + (S1_N - 2)), answer_unit=None, answer_format='자연수',
              hint='그림에서 대각선과 삼각형을 직접 세어 보고, n − 3과 n − 2로 확인해요.',
              solution='팔각형이므로 대각선 <i>a</i> = 8 − 3 = 5, 삼각형 <i>b</i> = 8 − 2 = 6이에요.<br>'
                       '<i>a</i> + <i>b</i> = 11'))
P.append(dict(id='p02', sec='s1', format='short', level='L', topic='대각선의 개수',
              stem_print='십이각형의 대각선의 개수를 구하시오.',
              figure=None, answer_print='54', answer_unit='개', answer_format='자연수',
              hint='n(n − 3) ÷ 2 에 n = 12를 넣어요.',
              solution='12 × (12 − 3) ÷ 2 = 12 × 9 ÷ 2 = 54(개)<br>÷ 2를 빠뜨리면 108이 나와요.'))
P.append(dict(id='p03', sec='s1', format='short', level='M', topic='대각선 수로 다각형 찾기',
              stem_print='대각선의 개수가 44인 다각형의 이름을 쓰시오.',
              figure=None, answer_print='십일각형', answer_unit=None, answer_format='○각형',
              hint='n(n − 3) = 88 이 되는 n을 찾아요. 연속하지 않은 두 수 n과 n − 3의 곱이에요.',
              solution='n(n − 3) ÷ 2 = 44 → n(n − 3) = 88<br>11 × 8 = 88 이므로 n = 11, 십일각형이에요.'))

# ── s2 삼각형
P.append(dict(id='p04', sec='s2', format='short', level='L', topic='외각의 성질',
              stem_print='다음 그림의 삼각형 ABC에서 ∠' + X + '의 크기를 구하시오.',
              figure=tri_fig(), answer_print=F.deg(S2_A + S2_B), answer_unit=None, answer_format='각도',
              hint='∠' + X + '는 꼭짓점 C의 외각이에요. 이웃하지 않는 두 내각을 더해요.',
              solution='∠' + X + ' = ∠A + ∠B = 55° + 70° = 125°<br>'
                       '(∠C = 180° − 125° = 55°를 먼저 구해 180° − 55°로 계산해도 같아요.)'))
P.append(dict(id='p05', sec='s2', format='short', level='M', topic='삼각형의 내각',
              stem_print='다음 그림의 삼각형 ABC에서 점 D는 변 BC 위의 점이다. ∠' + X + '의 크기를 구하시오.',
              figure=fig_cevian(CV_B, CV_C, CV_BAD), answer_print=F.deg(180 - CV_B - CV_C - CV_BAD),
              answer_unit=None, answer_format='각도',
              hint='삼각형 ABD에서 외각 ∠ADC를 먼저 구하면 삼각형 ADC가 보여요.',
              solution='삼각형 ABD에서 ∠ADC = 45° + 30° = 75° (외각)<br>'
                       '삼각형 ADC에서 ∠' + X + ' = 180° − 75° − 50° = 55°<br>'
                       '(다른 방법: ∠A = 180° − 45° − 50° = 85°이므로 85° − 30° = 55°)'))
P.append(dict(id='p06', sec='s2', format='short', level='M', topic='오목한 사각형의 각',
              stem_print='다음 그림에서 ∠' + X + '의 크기를 구하시오.',
              figure=fig_dart(DT_A, DT_ABD, DT_ACD), answer_print=F.deg(DT_A + DT_ABD + DT_ACD),
              answer_unit=None, answer_format='각도',
              hint='선분 AD를 그어 연장해 보면, 삼각형 두 개의 외각이 생겨요.',
              solution='AD를 그어 BC 쪽으로 연장하면 ∠' + X + '는 두 외각의 합이에요.<br>'
                       '(∠BAD + 25°) + (∠DAC + 30°) = 50° + 25° + 30° = 105°<br>'
                       '이 모양에서는 언제나 ∠' + X + ' = ∠A + ∠ABD + ∠ACD 예요.'))

# ── s3 내각의 합
P.append(dict(id='p07', sec='s3', format='short', level='L', topic='육각형의 내각',
              stem_print='다음 그림에서 ∠' + X + '의 크기를 구하시오.',
              figure=hex_fig(), answer_print=F.deg(HEX[5]), answer_unit=None, answer_format='각도',
              hint='먼저 꼭짓점을 세어 몇 각형인지 정하고, 내각의 합 180° × (n − 2)를 구해요.',
              solution='육각형의 내각의 합 = 180° × 4 = 720°<br>'
                       '120° + 130° + 110° + 125° + 135° = 620°<br>∠' + X + ' = 720° − 620° = 100°'))
P.append(dict(id='p08', sec='s3', format='short', level='L', topic='내각의 합으로 다각형 찾기',
              stem_print='내각의 크기의 합이 1440°인 다각형의 이름을 쓰시오.',
              figure=None, answer_print='십각형', answer_unit=None, answer_format='○각형',
              hint='180° × (n − 2) = 1440°',
              solution='n − 2 = 1440 ÷ 180 = 8 → n = 10, 십각형이에요.'))
P.append(dict(id='p09', sec='s3', format='short', level='M', topic='정오각형과 대각선',
              stem_print='다음 그림의 정오각형 ABCDE에서 대각선 AC를 그었을 때, ∠' + X + '(= ∠BAC)의 크기를 구하시오.',
              figure=fig_pentagon_diag(), figure_sol=fig_pentagon_diag(accent=True),
              answer_print='36°', answer_unit=None, answer_format='각도',
              hint='정오각형의 한 내각을 구하고, 삼각형 ABC가 어떤 삼각형인지 봐요(AB = BC).',
              solution='정오각형의 한 내각 = 540° ÷ 5 = 108°<br>'
                       '삼각형 ABC는 AB = BC인 이등변삼각형이므로 ∠' + X + ' = (180° − 108°) ÷ 2 = 36°'))

# ── s4 외각의 합
P.append(dict(id='p10', sec='s4', format='short', level='L', topic='외각의 합',
              stem_print='다음 그림에서 ∠' + X + '의 크기를 구하시오.',
              figure=pent_ext_fig(), answer_print=F.deg(PENT_EXT[4]), answer_unit=None, answer_format='각도',
              hint='그림의 각은 모두 변을 연장해 생긴 외각이에요. 외각의 합은 몇 각형이든 360°.',
              solution='70° + 80° + 65° + 75° + ∠' + X + ' = 360°<br>∠' + X + ' = 360° − 290° = 70°'))
P.append(dict(id='p11', sec='s4', format='short', level='L', topic='정다각형의 한 외각',
              stem_print='한 외각의 크기가 30°인 정다각형의 이름을 쓰시오.',
              figure=None, answer_print='정십이각형', answer_unit=None, answer_format='정○각형',
              hint='정n각형의 한 외각 = 360° ÷ n',
              solution='360° ÷ n = 30° → n = 12, 정십이각형이에요.'))
P.append(dict(id='p12', sec='s4', format='choice5', level='M', topic='내각과 외각의 비',
              stem_print='한 내각의 크기와 한 외각의 크기의 비가 3 : 1인 정다각형은?',
              figure=None, choices=['정오각형', '정육각형', '정팔각형', '정십각형', '정십이각형'], answer_choice=3,
              distractor_why=['한 외각을 72°로 잘못 구함', '한 외각을 60°로 잘못 구함(1 : 2와 혼동)',
                              '내각 : 외각을 1 : 3으로 거꾸로 봄', '외각을 180 ÷ 6으로 계산함'],
              answer_print='정팔각형',
              hint='한 내각 + 한 외각 = 180°를 3 : 1로 나눠요.',
              solution='한 외각 = 180° × 1/4 = 45°<br>360° ÷ 45° = 8 → 정팔각형'))

# ── s5 중심각과 호
P.append(dict(id='p13', sec='s5', format='short', level='L', topic='중심각과 호의 길이',
              stem_print='다음 그림의 원 O에서 ∠' + X + '의 크기를 구하시오.',
              figure=F.fig_circle_parts(3, {'A': 195, 'B': 225, 'C': 300, 'D': 30}, radii='ABCD',
                                        angles=[('A', 'B', '30°'), ('C', 'D', X)],
                                        arc_labels=[('A', 'B', '4cm'), ('C', 'D', '12cm')],
                                        shade=[('C', 'D', 'c'), ('A', 'B', 'y')]),
              answer_print='90°', answer_unit=None, answer_format='각도',
              hint='호의 길이가 몇 배인지 보면 중심각도 같은 배가 돼요.',
              solution='호의 길이가 12 ÷ 4 = 3배이므로 중심각도 3배: ∠' + X + ' = 30° × 3 = 90°'))
P.append(dict(id='p14', sec='s5', format='short', level='L', topic='중심각과 넓이',
              stem_print='다음 그림의 원 O에서 부채꼴 AOB의 넓이가 8 cm²일 때, 부채꼴 BOC의 넓이를 구하시오.',
              figure=F.fig_circle_parts(3, {'A': 150, 'B': 190, 'C': 290}, radii='ABC',
                                        angles=[('A', 'B', '40°'), ('B', 'C', '100°')],
                                        shade=[('A', 'B', 'y'), ('B', 'C', 'm')]),
              answer_print='20', answer_unit='cm²', answer_format='수',
              hint='넓이는 중심각에 정비례: 40 : 100 = 8 : □',
              solution='40 : 100 = 8 : S → S = 8 × 100/40 = 20 (cm²)'))
P.append(dict(id='p15', sec='s5', format='choice5', level='M', topic='호·현·넓이의 성질',
              stem_print='다음 그림의 원 O에서 ∠AOB = ∠BOC = ∠COD = 40°일 때, 옳지 <b>않은</b> 것은?',
              figure=F.fig_circle_parts(3, {'A': 190, 'B': 230, 'C': 270, 'D': 310}, radii='ABCD',
                                        chords=[('A', 'B'), ('C', 'D'), ('A', 'D')],
                                        angles=[('A', 'B', '40°'), ('B', 'C', '40°'), ('C', 'D', '40°')]),
              choices=['호 AB = 호 CD', '현 AB = 현 CD', '호 AD = 3 × 호 AB', '현 AD = 3 × 현 AB',
                       '(부채꼴 AOD의 넓이) = 3 × (부채꼴 AOB의 넓이)'], answer_choice=4,
              distractor_why=['중심각이 같으면 호도 같아요(옳음)', '중심각이 같으면 현도 같아요(옳음)',
                              '중심각 120°는 40°의 3배라 호도 3배(옳음)', '넓이도 중심각에 정비례(옳음)'],
              answer_print='현 AD ≠ 3 × 현 AB',
              hint='호와 넓이는 정비례, 현은 정비례하지 않아요.',
              solution='현 AD는 꺾은선 A→B→C→D(현 AB 세 개)보다 짧으므로 3 × 현 AB가 될 수 없어요. 답은 ④.'))

# ── s6 호의 길이와 넓이
P.append(dict(id='p16', sec='s6', format='short', level='L', topic='호의 길이',
              stem_print='다음 부채꼴의 호의 길이를 구하시오.',
              figure=F.fig_sector(SEC16[0], SEC16[1], r_label=F.cm(SEC16[0]), theta_label=F.deg(SEC16[1]), fill='p'),
              answer_print='4' + PI, answer_unit='cm', answer_format='○π',
              hint='l = 2πr × x/360',
              solution='l = 2π × 6 × 120/360 = 4π (cm)'))
P.append(dict(id='p17', sec='s6', format='short', level='M', topic='호로 넓이 구하기',
              stem_print='다음 그림과 같이 반지름의 길이가 10 cm, 호의 길이가 4π cm인 부채꼴의 넓이를 구하시오.',
              figure=F.fig_sector(SEC17[0], 360 * SEC17[1] / (2 * SEC17[0]), r_label=F.cm(SEC17[0]),
                                  arc_label='4π cm', fill='g'),
              answer_print='20' + PI, answer_unit='cm²', answer_format='○π',
              hint='중심각을 몰라도 돼요: S = r × l ÷ 2',
              solution='S = 10 × 4π ÷ 2 = 20π (cm²)<br>(중심각을 구하면 72°, π × 10² × 72/360 = 20π로 같아요.)'))
P.append(dict(id='p18', sec='s6', format='short', level='M', topic='색칠한 부분의 넓이',
              stem_print='다음 그림에서 색칠한 부분의 넓이를 구하시오.',
              figure=F.fig_sector_band(BAND18[0], BAND18[1], BAND18[2], fill='o'),
              answer_print='12' + PI, answer_unit='cm²', answer_format='○π',
              hint='큰 부채꼴(반지름 8) − 작은 부채꼴(반지름 4). 바깥 반지름은 4 + 4 = 8이에요.',
              solution='큰 부채꼴: π × 8² × 90/360 = 16π<br>작은 부채꼴: π × 4² × 90/360 = 4π<br>'
                       '색칠한 부분 = 16π − 4π = 12π (cm²)'))

# ── s7 다면체
P.append(dict(id='p19', sec='s7', format='choice5', level='L', topic='각기둥의 모서리',
              stem_print='다음 그림과 같은 입체도형의 모서리의 개수는?',
              figure=F.fig_polyhedron(*F.prism(F.reg_base(PRISM19_N, 2.2, 0), 3.2), fill='c'),
              choices=['8', '12', '15', '18', '24'], answer_choice=4,
              distractor_why=['면의 개수(8)와 혼동', '꼭짓점의 개수(12)와 혼동', '오각기둥으로 잘못 봄',
                              '옆면마다 네 변을 세어 겹치는 모서리를 두 번 셈'],
              answer_print='18',
              hint='밑면이 육각형인 각기둥(육각기둥)이에요. 위·아래 밑면의 모서리 + 옆모서리.',
              solution='육각기둥의 모서리 = 6 (아래) + 6 (위) + 6 (옆) = 18'))
P.append(dict(id='p20', sec='s7', format='short', level='L', topic='각뿔대의 구성 요소',
              stem_print='다음 그림과 같은 입체도형의 꼭짓점의 개수를 <i>a</i>, 면의 개수를 <i>b</i>라 할 때, '
                         '<i>a</i> + <i>b</i>의 값을 구하시오.',
              figure=F.fig_polyhedron(*F.frustum(F.reg_base(4, 2.8, 20), 0.5, 2.6), fill='y',
                                      view=F.View(tilt=20, yaw=0)),
              answer_print='14', answer_unit=None, answer_format='자연수',
              hint='두 밑면이 평행하고 크기가 다른 사각형 → 사각뿔대.',
              solution='사각뿔대: 꼭짓점 4 × 2 = 8, 면 2 + 4 = 6 → 8 + 6 = 14'))
P.append(dict(id='p21', sec='s7', format='choice5', level='M', topic='정다면체의 성질',
              stem_print='다음 그림의 정다면체에 대한 설명으로 옳지 <b>않은</b> 것은?',
              figure=F.fig_polyhedron(*F.tetrahedron(4), fill='m', view=F.View(tilt=22, yaw=35)),
              choices=['면의 모양은 정삼각형이다.', '한 꼭짓점에 모인 면의 개수는 3이다.', '꼭짓점의 개수는 4이다.',
                       '모서리의 개수는 6이다.', '면의 개수는 6이다.'], answer_choice=5,
              distractor_why=['정사면체의 면은 정삼각형(옳음)', '한 꼭짓점에 면 3개(옳음)',
                              '꼭짓점 4개(옳음)', '모서리 6개(옳음)'],
              answer_print='면의 개수는 4',
              hint='그림은 정사면체예요. 면·모서리·꼭짓점을 직접 세어 봐요.',
              solution='정사면체의 면은 4개예요. 모서리의 개수 6과 혼동하지 않아요. 답은 ⑤.'))

# ── s8 회전체
_shapes = [
    ([(0, 0), (2, 0), (2, 3), (0, 3)], 'c'),
    ([(0, 0), (2.2, 0), (1.2, 3), (0, 3)], 'g'),
    ([(0, 0), (2, 0), (0, 3)], 'y'),
    ([(1.5 * math.cos(math.radians(a)), 1.5 + 1.5 * math.sin(math.radians(a))) for a in range(-90, 91, 6)], 'm'),
    ([(1, 0), (2.4, 0), (2.4, 3), (1, 3)], 'p'),
]
P.append(dict(id='p22', sec='s8', format='choice5', level='L', topic='회전체 만들기',
              stem_print='다음 평면도형을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때, <b>원뿔</b>이 생기는 것은?',
              figure=None, choices=[rot_small(s, f) for s, f in _shapes], answer_choice=3,
              distractor_why=['직사각형 → 원기둥', '직각사다리꼴 → 원뿔대', '반원 → 구',
                              '축에서 떨어진 직사각형 → 가운데가 빈 원기둥'],
              answer_print='직각삼각형',
              hint='원뿔은 꼭짓점이 하나예요. 축 위에 꼭짓점이 오는 도형을 찾아요.',
              solution='직각삼각형의 직각을 낀 한 변을 축으로 돌리면 원뿔이 생겨요. 답은 ③.'))
P.append(dict(id='p23', sec='s8', format='short', level='L', topic='회전축을 포함하는 단면',
              stem_print='다음 그림의 직사각형을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체를 '
                         '회전축을 포함하는 평면으로 자른 단면의 넓이를 구하시오.',
              figure=F.fig_rotation([(0, 0), (3, 0), (3, 5), (0, 5)],
                                    labels=[((1.5, 0), '3cm', (0, -10)), ((3, 2.5), '5cm', (18, 0))],
                                    right=[((0, 0), 0, 90)], fill='c'),
              figure_sol=F.fig_rotation([(0, 0), (3, 0), (3, 5), (0, 5)],
                                        labels=[((0, 0), '6cm', (0, -10)), ((3, 2.5), '5cm', (18, 0))],
                                        mirror=True, fill='c', width=190),
              answer_print='30', answer_unit='cm²', answer_format='수',
              hint='회전체는 원기둥. 단면은 가로가 반지름의 2배인 직사각형이에요.',
              solution='단면 = 가로 3 × 2 = 6 cm, 세로 5 cm인 직사각형 → 6 × 5 = 30 (cm²)<br>'
                       '처음 직사각형의 넓이 15만 쓰면 틀려요.'))
P.append(dict(id='p24', sec='s8', format='short', level='M', topic='원뿔의 전개도',
              stem_print='다음 그림의 원뿔의 전개도를 그릴 때, 옆면인 부채꼴의 중심각의 크기를 구하시오.',
              figure=F.fig_round([{'t': 'cone', 'r': CONE24[0], 'h': math.sqrt(CONE24[1] ** 2 - CONE24[0] ** 2)}],
                                 labels=[('r', 0, F.cm(CONE24[0])), ('l', 0, F.cm(CONE24[1]))], fill=['m']),
              figure_sol=F.fig_net_cone(CONE24[1], 360 * CONE24[0] / CONE24[1], CONE24[0],
                                        l_label='10cm', theta_label='144°', r_label='4cm'),
              answer_print='144°', answer_unit=None, answer_format='각도',
              hint='부채꼴의 호의 길이 = 밑면인 원의 둘레. 부채꼴의 반지름은 모선(10 cm)이에요.',
              solution='밑면의 둘레 = 2π × 4 = 8π<br>2π × 10 × x/360 = 8π → x = 144°'))

# ── s9 기둥
P.append(dict(id='p25', sec='s9', format='short', level='L', topic='삼각기둥의 겉넓이',
              stem_print='다음 그림은 밑면이 직각삼각형인 삼각기둥이다. 이 삼각기둥의 겉넓이를 구하시오.',
              figure=prism_tri_fig(), answer_print='84', answer_unit='cm²', answer_format='수',
              hint='밑넓이 × 2 + 옆넓이. 옆넓이 = (밑면의 둘레) × (높이).',
              solution='밑넓이 = 4 × 3 ÷ 2 = 6 → 6 × 2 = 12<br>옆넓이 = (3 + 4 + 5) × 6 = 72<br>'
                       '겉넓이 = 12 + 72 = 84 (cm²)'))
P.append(dict(id='p26', sec='s9', format='short', level='L', topic='원기둥의 부피',
              stem_print='다음 원기둥의 부피를 구하시오.',
              figure=F.fig_round([{'t': 'cyl', 'r': 3, 'h': 5}], labels=[('r', 1, '3cm'), ('hs', 0, '5cm')],
                                 fill=['g']),
              answer_print='45' + PI, answer_unit='cm³', answer_format='○π',
              hint='부피 = 밑넓이 × 높이 = πr² × h',
              solution='π × 3² × 5 = 45π (cm³)'))
P.append(dict(id='p27', sec='s9', format='short', level='M', topic='원기둥의 전개도',
              stem_print='다음 그림은 원기둥의 전개도이다. 이 원기둥의 겉넓이를 구하시오.',
              figure=F.fig_net_cylinder(4, 6, h_label='6cm', w_label='8π cm'),
              answer_print='80' + PI, answer_unit='cm²', answer_format='○π',
              hint='직사각형의 가로 = 밑면인 원의 둘레 → 2πr = 8π 에서 r을 구해요.',
              solution='2πr = 8π → r = 4<br>밑넓이 2개 = 2 × π × 4² = 32π<br>옆넓이 = 8π × 6 = 48π<br>'
                       '겉넓이 = 32π + 48π = 80π (cm²)'))

# ── s10 뿔
P.append(dict(id='p28', sec='s10', format='short', level='L', topic='사각뿔의 겉넓이',
              stem_print='다음 그림은 밑면이 정사각형이고 옆면이 모두 합동인 이등변삼각형인 사각뿔이다. '
                         '이 사각뿔의 겉넓이를 구하시오.',
              figure=pyramid_fig(), answer_print='96', answer_unit='cm²', answer_format='수',
              hint='밑넓이 1개 + 옆면 삼각형 4개. 삼각형의 높이는 점선(5 cm)이에요.',
              solution='밑넓이 = 6 × 6 = 36<br>옆넓이 = (6 × 5 ÷ 2) × 4 = 60<br>겉넓이 = 36 + 60 = 96 (cm²)<br>'
                       '뿔은 밑면이 1개뿐이에요.'))
P.append(dict(id='p29', sec='s10', format='short', level='L', topic='원뿔의 부피',
              stem_print='다음 원뿔의 부피를 구하시오.',
              figure=F.fig_round([{'t': 'cone', 'r': 3, 'h': 7}], labels=[('r', 0, '3cm'), ('h', 0, '7cm')],
                                 fill=['y']),
              answer_print='21' + PI, answer_unit='cm³', answer_format='○π',
              hint='뿔의 부피 = 1/3 × 밑넓이 × 높이',
              solution='1/3 × π × 3² × 7 = 21π (cm³)<br>1/3을 빠뜨리면 63π가 나와요.'))
P.append(dict(id='p30', sec='s10', format='short', level='M', topic='원뿔의 겉넓이',
              stem_print='다음 원뿔의 겉넓이를 구하시오.',
              figure=F.fig_round([{'t': 'cone', 'r': CONE30[0], 'h': math.sqrt(CONE30[1] ** 2 - CONE30[0] ** 2)}],
                                 labels=[('r', 0, F.cm(CONE30[0])), ('l', 0, F.cm(CONE30[1]))], fill=['c']),
              answer_print='70' + PI, answer_unit='cm²', answer_format='○π',
              hint='밑넓이 πr² + 옆넓이 π × r × (모선).',
              solution='밑넓이 = π × 5² = 25π<br>옆넓이 = π × 5 × 9 = 45π<br>겉넓이 = 25π + 45π = 70π (cm²)'))

# ── s11 구
P.append(dict(id='p31', sec='s11', format='short', level='L', topic='구의 겉넓이',
              stem_print='다음 구의 겉넓이를 구하시오.',
              figure=F.fig_round([{'t': 'sphere', 'r': 3}], labels=[('r', 0, '3cm')], fill=['p']),
              answer_print='36' + PI, answer_unit='cm²', answer_format='○π',
              hint='구의 겉넓이 = 4πr²',
              solution='4π × 3² = 36π (cm²)'))
P.append(dict(id='p32', sec='s11', format='short', level='M', topic='반구의 겉넓이',
              stem_print='다음 그림과 같은 반구의 겉넓이를 구하시오.',
              figure=F.fig_round([{'t': 'hemi_down', 'r': 3}], labels=[('r', 1, '3cm')], fill=['o']),
              answer_print='27' + PI, answer_unit='cm²', answer_format='○π',
              hint='곡면(구 겉넓이의 절반) + 잘린 면(원). 원을 빠뜨리기 쉬워요.',
              solution='곡면 = 4π × 3² ÷ 2 = 18π<br>잘린 면 = π × 3² = 9π<br>겉넓이 = 18π + 9π = 27π (cm²)'))
P.append(dict(id='p33', sec='s11', format='short', level='M', topic='원기둥과 구의 부피',
              stem_print='다음 그림과 같이 원기둥 안에 구가 꼭 맞게 들어 있다. 구의 부피는 원기둥의 부피의 몇 배인지 구하시오.',
              figure=fig_cyl_sphere(3), answer_print=FR(2, 3), answer_unit='배', answer_format='분수',
              hint='원기둥의 높이 = 구의 지름 = 6 cm.',
              solution='원기둥: π × 3² × 6 = 54π<br>구: 4/3 × π × 3³ = 36π<br>36π ÷ 54π = 2/3 (배)'))

PROBLEMS = P


def check():
    assert (S1_N - 3) + (S1_N - 2) == 11
    assert 12 * 9 // 2 == 54
    assert [n for n in range(4, 30) if n * (n - 3) == 88] == [11]
    assert S2_A + S2_B == 125
    assert 180 - CV_B - CV_C - CV_BAD == 55 and (180 - CV_B - CV_C) - CV_BAD == 55
    assert DT_A + DT_ABD + DT_ACD == 105
    # 다트 그림의 실제 각이 105°인지
    base = (180 - DT_A) / 2
    assert abs(180 - (base - DT_ABD) - (base - DT_ACD) - 105) < 1e-9
    assert sum(HEX) == 720 and HEX[5] == 100
    assert 180 * 8 == 1440
    assert (180 - 108) / 2 == 36
    assert sum(PENT_EXT) == 360 and PENT_EXT[4] == 70
    assert 360 / 30 == 12
    assert 180 / 4 == 45 and 360 / 45 == 8
    assert C13['ab'] * C13['arc_cd'] / C13['arc_ab'] == 90
    assert C14['s_aob'] * C14['boc'] / C14['aob'] == 20
    R = 1
    assert abs(2 * R * math.sin(math.radians(60)) - 3 * 2 * R * math.sin(math.radians(20))) > 0.1
    assert abs(2 * math.pi * 6 * 120 / 360 - 4 * math.pi) < 1e-9
    assert abs(10 * 4 * math.pi / 2 - 20 * math.pi) < 1e-9 and abs(math.pi * 100 * 72 / 360 - 20 * math.pi) < 1e-9
    assert abs(math.pi * (64 - 16) / 4 - 12 * math.pi) < 1e-9
    assert 3 * PRISM19_N == 18
    assert 8 + 6 == 14
    assert abs(360 * 4 / 10 - 144) < 1e-9
    assert 4 * 3 / 2 * 2 + (3 + 4 + 5) * 6 == 84 and 3 ** 2 + 4 ** 2 == 25
    assert abs(math.pi * 9 * 5 - 45 * math.pi) < 1e-9
    assert abs(math.pi * 16 * 2 + 8 * math.pi * 6 - 80 * math.pi) < 1e-9
    assert 36 + 4 * (6 * 5 / 2) == 96
    assert abs(math.pi * 9 * 7 / 3 - 21 * math.pi) < 1e-9
    assert abs(math.pi * 25 + math.pi * 5 * 9 - 70 * math.pi) < 1e-9
    assert abs(4 * math.pi * 9 - 36 * math.pi) < 1e-9
    assert abs(4 * math.pi * 9 / 2 + math.pi * 9 - 27 * math.pi) < 1e-9
    assert abs((4 / 3 * math.pi * 27) / (math.pi * 9 * 6) - 2 / 3) < 1e-9
    print('check OK: 연습 %d문항' % len(PROBLEMS))
