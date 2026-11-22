"""mock3.py — 중1 2학기 기말 모의고사 3회 (교과서 6단원 평면도형의 성질 · 7단원 입체도형의 성질)

22문항 · 100점 · 45분. 실전 표준 + 중급 변형(L 5문항, 나머지 M).
그림의 라벨 수치와 정답은 같은 변수에서 나오고, check() 가 모든 정답을 다시 계산한다.
"""
import math

import figgen as F

X = F.X_ITAL
PI = 'π'


def I(s):
    return '<i>%s</i>' % s


def pi(k):
    return '%dπ' % k


META = {'id': 'm1-term2-mock3', 'kind': 'exam', 'title': '모의고사 3회',
        'subtitle': '실전 표준 + 중급 변형 · 맞꼭지각과 외각 · 정다각형의 비 · 정이십면체 · 속이 빈 회전체 · 그릇 옮겨 담기',
        'time_min': 45, 'folder': '모의고사', 'file': '모의고사3회'}


def choice(vals, ans, fmt=str):
    """보기 목록(크기 순)과 정답 번호."""
    return [fmt(v) for v in vals], vals.index(ans) + 1


# ═════════════════════════════════════════ 세트 전용 그림
@F.autofit
def fig_bowtie(al, be, ga, de, labs, accent=None, scale=22, width=240, height=150):
    """두 선분 AC, BD가 O에서 만나 생기는 두 삼각형 OAB, OCD (∠AOB = ∠COD 맞꼭지각).
    al, be: 삼각형 OAB의 ∠A, ∠B / ga, de: 삼각형 OCD의 ∠C, ∠D (al + be = ga + de)."""
    assert abs((al + be) - (ga + de)) < 1e-9
    c = F.Canvas(scale)
    th = 180 - al - be
    O = (0.0, 0.0)
    A = F._add(O, F._u(180 - th / 2), 3.8 * math.sin(math.radians(be)))
    B = F._add(O, F._u(180 + th / 2), 3.8 * math.sin(math.radians(al)))
    C = F._add(O, F._u(-th / 2), 3.8 * math.sin(math.radians(de)))
    D = F._add(O, F._u(th / 2), 3.8 * math.sin(math.radians(ga)))
    c.poly([O, A, B], fill=F.FILL['y'])
    c.poly([O, C, D], fill=F.FILL['c'])
    c.angle_at(A, B, O, label=labs[0])
    c.angle_at(B, O, A, label=labs[1])
    c.angle_at(C, D, O, label=labs[2])
    c.angle_at(D, O, C, label=labs[3], size=15)
    if accent:
        c.angle_mark(O, 180 + th / 2, 360 - th / 2, r=10, label=accent, color=F.ACCENT)
    for p, nm in ((A, 'A'), (B, 'B'), (C, 'C'), (D, 'D')):
        c.text(p, nm, size=12, d=F._scale(F._u(F._dir(O, p)), 11))
    c.text(O, 'O', size=12, d=(0, 13))
    return c.svg(width, height)


@F.autofit
def fig_sector_prism(r, th, h, r_lab, th_lab, h_lab, tilt=30, scale=22, width=210, height=180):
    """밑면이 부채꼴(반지름 r, 중심각 th)인 기둥. 부채꼴이 앞쪽을 향하게 세운다."""
    c = F.Canvas(scale)
    t = math.radians(tilt)
    k, ch = math.sin(t), math.cos(t)
    a0, a1 = 270 - th / 2, 270 + th / 2
    H = h * ch

    def P(a, y, rr=r):
        return (rr * math.cos(math.radians(a)), y + rr * k * math.sin(math.radians(a)))

    def arc(y, b0, b1, rr=r, n=48):
        return [P(b0 + (b1 - b0) * i / n, y, rr) for i in range(n + 1)]

    Ob, Ot = (0.0, 0.0), (0.0, H)
    c.poly(arc(0, a0, a1) + arc(H, a1, a0), fill=F.FILL['o'], stroke='none')
    c.poly([Ot] + arc(H, a0, a1), fill=F.FILL['y'], stroke='none')
    for q in (P(a0, 0), P(a1, 0), Ot):                       # 숨은 모서리
        c.line(Ob, q, dash='4 3', sw=1.0)
    c.poly(arc(0, a0, a1), close=False)
    c.poly([Ot] + arc(H, a0, a1))
    c.line(P(a0, 0), P(a0, H))
    c.line(P(a1, 0), P(a1, H))
    rho = c.px(15)
    c.poly(arc(H, a0, a1, rr=rho, n=24), sw=1.1, close=False)
    c.text(Ot, th_lab, size=12, d=(0, -(15 * k + 11)))
    c.seg_label(Ot, P(a1, H), r_lab, side=1)
    c.text(P(a1, H / 2), h_lab, size=12, d=(20, 0))
    return c.svg(width, height)


@F.autofit
def fig_quarter_minus_semi(R, fill='g', scale=22, width=170, height=170):
    """반지름 R인 사분원 안에서, 한 반지름을 지름으로 하는 반원을 뺀 부분을 색칠."""
    c = F.Canvas(scale)
    O = (0.0, 0.0)
    big = c.arc_pts(O, R, 90, 0, n=60)
    semi = c.arc_pts((R / 2, 0), R / 2, 0, 180, n=60)
    c.poly([O] + big + semi[1:], fill=F.FILL[fill])
    c.line(O, (R, 0))
    c.right_mark(O, 0, 90)
    c.dot(O)
    c.text(O, 'O', size=12, d=(-9, -9))
    c.text((0, R / 2), F.cm(R), size=12, d=(-20, 0))
    c.text((R / 2, 0), F.cm(R), size=12, d=(0, -10))
    return c.svg(width, height)


@F.autofit
def fig_two_cyl(R1, h1, R2, h2, labs, tilt=17, scale=22, width=190, height=210):
    """반지름 R1·높이 h1 원기둥 위에 반지름 R2(< R1)·높이 h2 원기둥을 중심을 맞춰 올린 입체.
    아래 원기둥 윗면의 뒤쪽 테두리는 위 원기둥에 가린 부분만 점선."""
    c = F.Canvas(scale)
    t = math.radians(tilt)
    k, ch = math.sin(t), math.cos(t)
    y1, y2 = h1 * ch, (h1 + h2) * ch

    def ell(yc, r, a0, a1):
        return c.arc_pts((0, yc), r, a0, a1, n=60, ry=r * k)

    c.poly(ell(0, R1, 180, 360) + ell(y1, R1, 0, 180), fill=F.FILL['c'], stroke='none')
    c.poly(ell(y1, R1, 0, 360)[:-1], fill=F.FILL['y'], stroke='none')
    c.poly(ell(y1, R2, 180, 360) + ell(y2, R2, 0, 180), fill=F.FILL['m'], stroke='none')
    c.poly(ell(y2, R2, 0, 360)[:-1], fill=F.FILL['m'], stroke='none')
    # 아래 원기둥
    c.poly(ell(0, R1, 180, 360), close=False)
    c.poly(ell(0, R1, 0, 180), close=False, dash='4 3', sw=1.0)
    c.line((-R1, 0), (-R1, y1))
    c.line((R1, 0), (R1, y1))
    ac = math.degrees(math.acos(R2 / R1))
    c.poly(ell(y1, R1, 180, 360), close=False)
    c.poly(ell(y1, R1, 0, ac), close=False)
    c.poly(ell(y1, R1, 180 - ac, 180), close=False)
    c.poly(ell(y1, R1, ac, 180 - ac), close=False, dash='4 3', sw=1.0)
    # 위 원기둥
    c.poly(ell(y1, R2, 180, 360), close=False)
    c.poly(ell(y1, R2, 0, 180), close=False, dash='4 3', sw=1.0)
    c.line((-R2, y1), (-R2, y2))
    c.line((R2, y1), (R2, y2))
    c.poly(ell(y2, R2, 0, 360)[:-1])
    # 치수
    c.line((0, 0), (R1, 0), dash='3 2', sw=1.0)
    c.dot((0, 0), r=1.8)
    c.text((R1 / 2, 0), labs[0], size=12, d=(0, 9))
    c.line((0, y2), (R2, y2), dash='3 2', sw=1.0)
    c.dot((0, y2), r=1.8)
    c.text((R2 / 2, y2), labs[1], size=12, d=(0, 9))
    c.text((R1, y1 / 2), labs[2], size=12, d=(20, 0))
    c.text((R2, (y1 + y2) / 2), labs[3], size=12, d=(20, 0))
    return c.svg(width, height)


PHI = (1 + 5 ** 0.5) / 2


def icosahedron(a=3.0):
    s = a / 2
    V = []
    for p in (1, -1):
        for q in (1, -1):
            V += [(0, p * s, q * s * PHI), (p * s, q * s * PHI, 0), (q * s * PHI, 0, p * s)]

    def dist(i, j):
        return math.dist(V[i], V[j])

    n = len(V)
    Fc = [[i, j, m] for i in range(n) for j in range(i + 1, n) for m in range(j + 1, n)
          if abs(dist(i, j) - a) < 1e-6 and abs(dist(j, m) - a) < 1e-6 and abs(dist(i, m) - a) < 1e-6]
    return V, Fc


def side_by_side(*parts):
    """그림 여러 개를 가로로(캡션은 그림 아래)."""
    cells = ''.join('<span style="display:inline-block;vertical-align:bottom;margin:0 5px;text-align:center">'
                    + svg + ('<br><span style="font-size:9pt">' + cap + '</span>' if cap else '') + '</span>'
                    for svg, cap in parts)
    return cells


# ═════════════════════════════════════════ 1 대각선 (L, 3점)
N1 = 10
D1 = N1 - 3
ANS1 = N1 * (N1 - 3) // 2
V1 = [7 * (7 - 3) // 2, 9 * (9 - 3) // 2, ANS1, N1 * (N1 - 1) // 2, N1 * (N1 - 3)]
C1, K1 = choice(V1, ANS1)
P1 = {
    'id': 'm3-01', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '대각선의 총 개수',
    'stem_print': '한 꼭짓점에서 그을 수 있는 대각선의 개수가 %d개인 다각형의 대각선의 총 개수는?' % D1,
    'figure': None,
    'choices': C1, 'answer_choice': K1, 'answer_print': '%d' % ANS1,
    'distractor_why': ['대각선 수 7을 꼭짓점 수로 착각해 칠각형으로 봄: 7 × 4 ÷ 2 = 14',
                       'n − 2 = 7로 계산해 구각형으로 봄: 9 × 6 ÷ 2 = 27',
                       '변 10개까지 더함: 35 + 10 = 45 (두 꼭짓점을 잇는 선분 전체를 셈)',
                       '÷ 2를 빠뜨림: 10 × 7 = 70 (대각선 하나를 양 끝에서 두 번 셈)'],
    'hint': '한 꼭짓점에서는 자기 자신과 양옆 꼭짓점으로는 대각선을 못 그어요. 그래서 (n − 3)개예요.',
    'solution': '① 한 꼭짓점에서 그을 수 있는 대각선은 (n − 3)개예요. n − 3 = 7 → n = 10, 십각형이에요.<br>'
                '② 대각선의 총 개수 = 10 × (10 − 3) ÷ 2 = 35<br>'
                '자주 하는 실수: ÷ 2를 빠뜨리면 같은 대각선을 양 끝에서 두 번 세게 돼요.',
}

# ═════════════════════════════════════════ 2 맞꼭지각 + 외각 (L, 3점)
A2, B2, G2 = 45, 80, 60
TH2 = 180 - A2 - B2                  # ∠AOB = ∠COD
EX2 = A2 + B2                        # ∠BOC (두 삼각형 공통의 외각)
ANS2 = EX2 - G2
V2 = [TH2, G2, ANS2, EX2 - TH2, 180 - A2 - G2]
C2, K2 = choice(V2, ANS2, F.deg)
LAB2 = [F.deg(A2), F.deg(B2), F.deg(G2), X]
P2 = {
    'id': 'm3-02', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '맞꼭지각과 외각',
    'stem_print': '다음 그림에서 두 선분 AC와 BD가 점 O에서 만날 때, ∠' + X + '의 크기는?',
    'figure': fig_bowtie(A2, B2, G2, ANS2, LAB2),
    'figure_sol': fig_bowtie(A2, B2, G2, ANS2, LAB2, accent=F.deg(EX2)),
    'choices': C2, 'answer_choice': K2, 'answer_print': F.deg(ANS2),
    'distractor_why': ['맞꼭지각 ∠AOB = ∠COD = 55°를 ∠x로 착각함',
                       '그림에서 ∠C와 비슷해 보여 같은 크기라고 어림함',
                       '외각 125°에서 ∠C 대신 맞꼭지각 55°를 뺌',
                       '∠A와 ∠C를 한 삼각형의 두 내각으로 잘못 묶어 180 − 45 − 60으로 계산함'],
    'hint': '∠BOC는 <b>두 삼각형 모두의 외각</b>이에요. 외각 = 이웃하지 않는 두 내각의 합.',
    'solution': '① ∠BOC는 삼각형 OAB의 한 외각이므로 ∠BOC = 45° + 80° = 125°<br>'
                '② ∠BOC는 삼각형 OCD의 한 외각이기도 하므로 60° + ∠' + X + ' = 125°<br>'
                '③ ∠' + X + ' = 125° − 60° = 65°<br>'
                '맞꼭지각이 같으니 "두 삼각형에서 나머지 두 각의 합은 같다(45° + 80° = 60° + ∠' + X + ')"로 기억해도 돼요.',
}

# ═════════════════════════════════════════ 3 육각형 내각의 합 (M)
INT3 = [120, 135, 110, 125, 100, 130]
P3pts = F.polygon_by_angles(INT3, [2.5, 2.0, 3.0, 3.0])     # 여섯 변이 2.0~3.0 으로 고르게
S3 = 180 * (6 - 2)
ANS3 = S3 - sum(INT3[:5])
V3 = [120, ANS3, S3 - (120 + 135 + 110 + 125 + (180 - 100)), S3 - (120 + 135 + (180 - 110) + 125 + 100),
      S3 - (120 + 135 + (180 - 110) + 125 + (180 - 100))]
C3, K3 = choice(V3, ANS3, F.deg)
FIG3_ARGS = dict(angles={0: F.deg(INT3[0]), 1: F.deg(INT3[1]), 3: F.deg(INT3[3])},
                 ext={2: F.deg(180 - INT3[2]), 4: F.deg(180 - INT3[4])}, unknown={5: X}, fill='m')
P3 = {
    'id': 'm3-03', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '육각형의 내각의 합',
    'stem_print': '다음 그림의 육각형에서 ∠' + X + '의 크기는?',
    'figure': F.fig_polygon(P3pts, **FIG3_ARGS),
    'figure_sol': F.fig_polygon(P3pts, accent={2: F.deg(INT3[2]), 4: F.deg(INT3[4])}, **FIG3_ARGS),
    'choices': C3, 'answer_choice': K3, 'answer_print': F.deg(ANS3),
    'distractor_why': ['계산하지 않고 정육각형의 한 내각 120°로 어림함',
                       '80°가 외각인데 내각처럼 그대로 더함',
                       '70°가 외각인데 내각처럼 그대로 더함',
                       '70°와 80° 두 외각을 모두 내각처럼 더함'],
    'hint': '육각형의 내각의 합은 180° × (6 − 2) = 720°예요. 변을 연장한 바깥 각(70°, 80°)은 <b>외각</b>이에요.',
    'solution': '① 육각형의 내각의 합: 180° × 4 = 720°<br>'
                '② 외각 70°의 내각은 180° − 70° = 110°, 외각 80°의 내각은 180° − 80° = 100°<br>'
                '③ 120° + 135° + 110° + 125° + 100° + ∠' + X + ' = 720° → 590° + ∠' + X + ' = 720° → ∠' + X
                + ' = 130°<br>'
                '자주 하는 실수: 변을 연장해서 생긴 각을 내각으로 착각해요. 연장선이 보이면 먼저 내각으로 바꿔요.',
}

# ═════════════════════════════════════════ 4 외각의 합 (M)
INT4 = [108, 122, 115, 100, 95]
EXT4 = [180 - a for a in INT4]                  # 72, 58, 65, 80, 85
K4ADD = 20
ANS4 = (360 - EXT4[0] - EXT4[1] - EXT4[3] - K4ADD) // 2
P4pts = F.polygon_by_angles(INT4, [4.0, 3.4, 3.2])
REST4 = EXT4[0] + EXT4[1] + EXT4[3]
V4 = [ANS4, (360 - REST4) // 2, (360 - REST4 + K4ADD) // 2, 360 - REST4 - K4ADD, (540 - REST4 - K4ADD) // 2]
C4, K4 = choice(V4, ANS4, F.deg)
P4 = {
    'id': 'm3-04', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '다각형의 외각의 합',
    'stem_print': '다음 그림에서 ∠' + X + '의 크기는?',
    'figure': F.fig_polygon(P4pts, ext={0: F.deg(EXT4[0]), 1: F.deg(EXT4[1]), 2: X, 3: F.deg(EXT4[3]),
                                        4: X + ' + %d°' % K4ADD}, fill='g', width=230, height=210),
    'choices': C4, 'answer_choice': K4, 'answer_print': F.deg(ANS4),
    'distractor_why': ['∠x + 20°의 20°를 빠뜨림: 2∠x + 210° = 360°',
                       '∠x + 20°를 ∠x − 20°로 계산함',
                       '∠x를 한 번만 셈: ∠x + 230° = 360°',
                       '외각의 합을 오각형의 내각의 합 540°로 착각함'],
    'hint': '그림의 각은 모두 변을 연장해서 생긴 <b>외각</b>이에요. 다각형의 외각의 합은 항상 360°예요.',
    'solution': '① 다각형의 외각의 크기의 합은 360°예요.<br>'
                '② 72° + 58° + ∠' + X + ' + 80° + (∠' + X + ' + 20°) = 360°<br>'
                '③ 2 × ∠' + X + ' + 230° = 360° → 2 × ∠' + X + ' = 130° → ∠' + X + ' = 65°<br>'
                '자주 하는 실수: 내각의 합(540°)과 외각의 합(360°)을 섞어 써요. 연장선 바깥의 각이면 360°예요.',
}

# ═════════════════════════════════════════ 5 정다각형 한 외각 (L, 3점)
S5 = 1440
N5 = S5 // 180 + 2
ANS5 = 360 // N5
V5 = [ANS5, 360 // (N5 - 1), 360 // (N5 - 2), 720 // N5, 180 - ANS5]
C5, K5 = choice(V5, ANS5, F.deg)
P5 = {
    'id': 'm3-05', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '정다각형의 한 외각',
    'stem_print': '내각의 크기의 합이 %d°인 정다각형의 한 외각의 크기는?' % S5,
    'figure': None,
    'choices': C5, 'answer_choice': K5, 'answer_print': F.deg(ANS5),
    'distractor_why': ['n − 1 = 8로 계산해 정구각형으로 봄: 360° ÷ 9 = 40°',
                       '1440 ÷ 180 = 8을 그대로 n으로 봄: 360° ÷ 8 = 45°',
                       '외각의 합을 720°로 착각함: 720° ÷ 10 = 72°',
                       '한 외각이 아니라 한 내각을 답함: 180° − 36° = 144°'],
    'hint': '내각의 합 180° × (n − 2)에서 n을 먼저 구해요. 한 외각은 360° ÷ n이에요.',
    'solution': '① 180° × (n − 2) = 1440° → n − 2 = 8 → n = 10, 정십각형이에요.<br>'
                '② 정십각형의 한 외각 = 360° ÷ 10 = 36°<br>'
                '확인: 한 내각 = 180° − 36° = 144°, 144° × 10 = 1440° 맞아요.',
}

# ═════════════════════════════════════════ 6 중심각과 호의 비례 (M)
A6, L6a, L6b, C6 = 40, 6, 15, 120
X6 = L6b * A6 // L6a                    # 100
Y6 = L6a * C6 // A6                     # 18
ANS6 = X6 + Y6
INV_X6, INV_Y6 = A6 * L6a // L6b, L6a * A6 // C6      # 16, 2 (반비례로 착각)
V6 = [INV_X6 + INV_Y6, INV_X6 + Y6, X6 + INV_Y6, ANS6, (L6a + L6b) * A6 // L6a + Y6]
C6c, K6 = choice(V6, ANS6)
PTS6 = {'A': 200, 'B': 200 + A6, 'C': 200 + A6 + X6, 'D': (200 + A6 + X6 + C6) % 360}
P6 = {
    'id': 'm3-06', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '중심각과 호의 비례',
    'stem_print': '다음 그림의 원 O에서 ' + I('x') + ' + ' + I('y') + '의 값은?',
    'figure': F.fig_circle_parts(3.2, PTS6, radii='ABCD',
                                 angles=[('A', 'B', F.deg(A6)), ('B', 'C', X + '°'), ('C', 'D', F.deg(C6))],
                                 arc_labels=[('A', 'B', F.cm(L6a)), ('B', 'C', F.cm(L6b)),
                                             ('C', 'D', F.it('y') + 'cm')],
                                 shade=[('B', 'C', 'c')], width=220, height=210),
    'choices': C6c, 'answer_choice': K6, 'answer_print': '%d' % ANS6,
    'distractor_why': ['두 값을 모두 반비례로 계산함 (x = 16, y = 2)',
                       'x를 반비례로 계산함: 40 × 6 ÷ 15 = 16',
                       'y를 반비례로 계산함: 6 × 40 ÷ 120 = 2',
                       'x를 ∠AOC(호 AC = 21 cm)의 크기 140으로 계산함'],
    'hint': '한 원에서 호의 길이는 중심각의 크기에 <b>정비례</b>해요. 40° : 6 cm를 기준으로 삼아요.',
    'solution': '① 40 : 6 = ' + I('x') + ' : 15 → 6' + I('x') + ' = 600 → ' + I('x') + ' = 100<br>'
                '② 40 : 6 = 120 : ' + I('y') + ' → 40' + I('y') + ' = 720 → ' + I('y') + ' = 18<br>'
                '③ ' + I('x') + ' + ' + I('y') + ' = 100 + 18 = 118<br>'
                '확인: 중심각이 40°의 2.5배인 100°이면 호도 6 cm의 2.5배인 15 cm예요.',
}

# ═════════════════════════════════════════ 7 부채꼴 성질 (M)
A7, C7 = 30, 90
PTS7 = {'A': 190, 'B': 190 + A7, 'C': 290, 'D': (290 + C7) % 360}
P7 = {
    'id': 'm3-07', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '중심각과 현·넓이',
    'stem_print': '다음 그림의 원 O에서 ∠AOB = %d°, ∠COD = %d°일 때, 다음 중 옳지 <b>않은</b> 것은?' % (A7, C7),
    'figure': F.fig_circle_parts(3.0, PTS7, radii='ABCD', chords=[('A', 'B'), ('C', 'D')],
                                 angles=[('A', 'B', F.deg(A7)), ('C', 'D', F.deg(C7))],
                                 shade=[('A', 'B', 'y'), ('C', 'D', 'y')], width=200, height=200),
    'choices': ['호 CD의 길이는 호 AB의 길이의 3배이다.',
                '부채꼴 COD의 넓이는 부채꼴 AOB의 넓이의 3배이다.',
                '현 CD의 길이는 현 AB의 길이의 3배보다 짧다.',
                '∠AOB의 크기를 3배로 하면 호 AB의 길이는 호 CD의 길이와 같아진다.',
                '삼각형 COD의 넓이는 삼각형 AOB의 넓이의 3배이다.'],
    'answer_choice': 5, 'answer_print': '삼각형의 넓이는 3배가 아니다',
    'distractor_why': ['중심각이 3배이므로 호의 길이도 3배, 옳음',
                       '부채꼴의 넓이도 중심각에 정비례하므로 옳음',
                       '현의 길이는 중심각에 정비례하지 않고 3배보다 짧으므로 옳음',
                       '∠AOB가 90°가 되어 ∠COD와 같아지므로 호의 길이도 같아짐, 옳음'],
    'hint': '한 원에서 중심각에 정비례하는 것은 <b>호의 길이와 부채꼴의 넓이</b>뿐이에요.',
    'solution': '① 호의 길이와 부채꼴의 넓이는 중심각에 정비례하므로 ①, ②, ④는 옳아요.<br>'
                '② 현의 길이는 정비례하지 않아요. ∠COD를 30°씩 셋으로 나누면 작은 현 3개를 이은 꺾은선이 현 CD보다 길어요. 그래서 ③도 옳아요.<br>'
                '③ 삼각형 COD = 부채꼴 COD − 활꼴이에요. 부채꼴은 3배이지만 활꼴(현과 호 사이)은 중심각이 클수록 훨씬 커져서, '
                '삼각형의 넓이는 3배가 되지 않아요. 따라서 옳지 않은 것은 ⑤예요.',
}

# ═════════════════════════════════════════ 8 부채꼴의 넓이 S = rl/2 (M)
R8, L8 = 12, 5                        # 반지름 12 cm, 호 5π cm
TH8 = 360 * L8 / (2 * R8)             # 75°
ANS8 = R8 * L8 // 2                   # 30π
V8 = [(R8 // 2) * L8 // 2, ANS8, R8 * L8, 2 * R8 * L8, R8 * R8]
C8, K8 = choice(V8, ANS8, lambda v: pi(v) + ' cm²')
P8 = {
    'id': 'm3-08', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '부채꼴의 넓이',
    'stem_print': '다음 그림과 같이 반지름의 길이가 %d cm이고 호의 길이가 %dπ cm인 부채꼴의 넓이는?' % (R8, L8),
    'figure': F.fig_sector(R8, TH8, r_label=F.cm(R8), arc_label='%dπ cm' % L8, fill='g'),
    'choices': C8, 'answer_choice': K8, 'answer_print': pi(ANS8) + ' cm²',
    'distractor_why': ['12 cm를 지름으로 보고 반지름 6으로 계산함',
                       'S = ½rl에서 ½을 빠뜨림: 12 × 5π = 60π',
                       '원의 둘레 공식과 섞어 2 × 12 × 5π로 계산함',
                       '원 전체의 넓이 π × 12² = 144π를 답함'],
    'hint': '중심각을 몰라도 돼요. 부채꼴의 넓이 S = ½ × (반지름) × (호의 길이).',
    'solution': '① S = ½ × ' + I('r') + ' × ' + I('l') + ' = ½ × 12 × 5π = 30π (cm²)<br>'
                '② 다른 방법: 중심각을 ' + I('x') + '°라 하면 2π × 12 × ' + I('x') + '/360 = 5π → ' + I('x')
                + ' = 75, 넓이 = π × 12² × 75/360 = 30π<br>'
                '중심각이 주어지지 않으면 S = ½' + I('rl') + '이 가장 빨라요.',
}

# ═════════════════════════════════════════ 9 오각뿔 (L, 3점)
N9 = 5
E9, VX9, FC9 = 2 * N9, N9 + 1, N9 + 1
ANS9 = E9 + VX9
V9 = [E9, N9 + VX9, E9 + N9, ANS9, E9 + VX9 + FC9]
C9, K9 = choice(V9, ANS9)
P9 = {
    'id': 'm3-09', 'unit': 7, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '각뿔의 구성 요소',
    'stem_print': '다음 그림과 같은 입체도형의 모서리의 개수와 꼭짓점의 개수의 합은?',
    'figure': F.fig_polyhedron(*F.pyramid(F.reg_base(N9, 2.6, 0), 4.2), fill='o', view=F.View(tilt=18, yaw=12)),
    'choices': C9, 'answer_choice': K9, 'answer_print': '%d' % ANS9,
    'distractor_why': ['꼭짓점을 더하지 않고 모서리 10개만 답함',
                       '모서리를 옆모서리 5개만 셈: 5 + 6',
                       '꼭짓점을 밑면의 5개만 세고 맨 위 꼭짓점을 빠뜨림: 10 + 5',
                       '면의 개수 6까지 더함: 10 + 6 + 6'],
    'hint': '먼저 이름을 붙여요. 밑면이 오각형이고 옆면이 삼각형이면 <b>오각뿔</b>이에요.',
    'solution': '① 그림은 오각뿔이에요.<br>'
                '② 모서리 = 밑면의 모서리 5 + 옆모서리 5 = 10<br>'
                '③ 꼭짓점 = 밑면의 꼭짓점 5 + 맨 위 꼭짓점 1 = 6<br>'
                '④ 10 + 6 = 16<br>'
                'n각뿔: 면 (n + 1), 모서리 2n, 꼭짓점 (n + 1)이에요.',
}

# ═════════════════════════════════════════ 10 정사면체 · 정이십면체 비교 표 (M)
F10 = 20
a10 = 5                                     # 한 꼭짓점에 모인 면
b10 = F10 * 3 // 2                          # 모서리
c10 = F10 * 3 // a10                        # 꼭짓점
ANS10 = a10 + b10 + c10
V10 = [4 + b10 + c10, ANS10, a10 + b10 + F10, a10 + b10 + b10, a10 + F10 * 3 + c10]
C10, K10 = choice(V10, ANS10)
TBL10 = ('<table style="width:auto;margin:4px auto 2px;font-size:9.4pt">'
         '<tr><th></th><th class="c">정사면체</th><th class="c">정이십면체</th></tr>'
         '<tr><td>면의 모양</td><td class="c">정삼각형</td><td class="c">정삼각형</td></tr>'
         '<tr><td>한 꼭짓점에 모인 면의 개수</td><td class="c">3</td><td class="c">' + I('a') + '</td></tr>'
         '<tr><td>면의 개수</td><td class="c">4</td><td class="c">%d</td></tr>'
         '<tr><td>모서리의 개수</td><td class="c">6</td><td class="c">' + I('b') + '</td></tr>'
         '<tr><td>꼭짓점의 개수</td><td class="c">4</td><td class="c">' + I('c') + '</td></tr></table>') % F10
P10 = {
    'id': 'm3-10', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '정다면체 비교',
    'stem_print': '다음은 정사면체와 정이십면체의 성질을 비교한 표이다. ' + I('a') + ' + ' + I('b') + ' + '
                  + I('c') + '의 값은?' + TBL10,
    'figure': side_by_side((F.fig_polyhedron(*F.tetrahedron(3.6), fill='m', view=F.View(tilt=14, yaw=12),
                                             width=120, height=120), '정사면체'),
                           (F.fig_polyhedron(*icosahedron(2.2), fill='c', view=F.View(tilt=18, yaw=20),
                                             width=135, height=135), '정이십면체')),
    'choices': C10, 'answer_choice': K10, 'answer_print': '%d' % ANS10,
    'distractor_why': ['한 꼭짓점에 모인 면을 4개(정팔면체)로 착각함',
                       '꼭짓점의 개수를 면의 개수 20과 같다고 봄',
                       '꼭짓점의 개수를 모서리의 개수 30과 같다고 봄',
                       '모서리를 20 × 3 = 60으로 세고 2로 나누지 않음'],
    'hint': '면 20개의 변을 모두 세면 20 × 3 = 60인데, 모서리 하나에 면이 2개씩 만나요.',
    'solution': '① 그림에서 정이십면체의 한 꼭짓점에는 정삼각형 5개가 모여요 → ' + I('a') + ' = 5<br>'
                '② 모서리: 20 × 3 ÷ 2 = 30 (모서리 하나에 면 2개) → ' + I('b') + ' = 30<br>'
                '③ 꼭짓점: 20 × 3 ÷ 5 = 12 (꼭짓점 하나에 면 5개) → ' + I('c') + ' = 12<br>'
                '④ ' + I('a') + ' + ' + I('b') + ' + ' + I('c') + ' = 5 + 30 + 12 = 47<br>'
                '확인: 정사면체도 4 × 3 ÷ 2 = 6(모서리), 4 × 3 ÷ 3 = 4(꼭짓점)로 표와 맞아요.',
}

# ═════════════════════════════════════════ 11 원뿔대가 생기는 평면도형 (M)
_sw, _sh = 78, 96
SH11 = [
    F.fig_rotation([(0, 0), (2.2, 0), (0, 3)], right=[((0, 0), 0, 90)], fill='y', width=_sw, height=_sh),
    F.fig_rotation([(1.5 * math.cos(math.radians(a)), 1.5 + 1.5 * math.sin(math.radians(a)))
                    for a in range(-90, 91, 6)], fill='y', width=_sw, height=_sh),
    F.fig_rotation([(1.0, 0), (2.4, 0), (2.4, 3), (1.0, 3)], fill='y', width=_sw, height=_sh),
    F.fig_rotation([(0, 0), (2.0, 0), (2.0, 3), (0, 3)], right=[((0, 0), 0, 90)], fill='y', width=_sw,
                   height=_sh),
    F.fig_rotation([(0, 0), (2.4, 0), (1.2, 3), (0, 3)], right=[((0, 0), 0, 90), ((0, 3), 0, -90)], fill='y',
                   width=_sw, height=_sh),
]
P11 = {
    'id': 'm3-11', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '회전체와 단면',
    'stem_print': '다음 평면도형을 직선 ' + I('l') + '을 회전축으로 하여 1회전 시킬 때, 생기는 회전체를 '
                  '<b>회전축에 수직인 평면</b>으로 자를 때, 단면이 항상 <b>합동인 원</b>이 되는 것은?',
    'figure': None,
    'choices': SH11, 'answer_choice': 4, 'answer_print': '직사각형 → 원기둥',
    'distractor_why': ['직각삼각형 → 원뿔, 자르는 높이에 따라 원의 크기가 달라짐',
                       '반원 → 구, 가운데에서 자를 때 원이 가장 크고 위·아래로 갈수록 작아짐',
                       '축에서 떨어진 직사각형 → 가운데가 빈 원기둥, 단면은 합동이지만 원이 아니라 고리 모양',
                       '직각사다리꼴 → 원뿔대, 위로 갈수록 원이 작아짐'],
    'hint': '회전축에 수직으로 자른 단면은 원이에요. 그 원의 반지름은 그 높이에서 도형이 축에서 얼마나 떨어져 있는지예요.',
    'solution': '① 회전축에 수직인 평면으로 자르면 단면은 원(또는 고리)이고, 반지름은 그 높이에서 도형의 가로 길이예요.<br>'
                '② 높이에 상관없이 가로 길이가 같고 축에 붙어 있는 도형은 ④의 직사각형뿐이에요. 회전체는 원기둥이에요.<br>'
                '③ ③은 가로 길이는 같지만 축에서 떨어져 있어서 단면이 가운데가 빈 고리 모양이에요.',
}

# ═════════════════════════════════════════ 12 사다리꼴 기둥의 겉넓이 (M)
B12, T12, H12, S12, D12 = 6, 3, 4, 5, 7
BASE12 = (B12 + T12) * H12 // 2               # 18
PER12 = B12 + T12 + H12 + S12                 # 18
LAT12 = PER12 * D12                           # 126
ANS12 = 2 * BASE12 + LAT12                    # 162
V12 = [LAT12, 2 * BASE12 + (PER12 - S12) * D12, BASE12 + LAT12, ANS12, 2 * B12 * H12 + LAT12]
C12, K12 = choice(V12, ANS12, lambda v: '%d cm²' % v)
V12f = [(0, 0, 0), (B12, 0, 0), (T12, H12, 0), (0, H12, 0)]
V12f = V12f + [(x, y, D12) for x, y, _ in V12f]
F12 = [[0, 1, 2, 3], [4, 5, 6, 7]] + [[i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i] for i in range(4)]


def _rm12(c, proj):
    for v, a, b in (((0, 0, 0), (1, 0, 0), (0, 1, 0)), ((0, H12, 0), (1, H12, 0), (0, 0, 0))):
        pv = proj(v)
        c.right_mark(pv, F._dir(pv, proj(a)), F._dir(pv, proj(b)))


P12 = {
    'id': 'm3-12', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '각기둥의 겉넓이',
    'stem_print': '다음 그림과 같이 밑면이 사다리꼴인 사각기둥의 겉넓이는?',
    'figure': F.fig_polyhedron(V12f, F12, view=F.View(tilt=20, yaw=-28), fill='p', extra=_rm12,
                               labels=[((B12 / 2, 0, 0), F.cm(B12), (0, -10)),
                                       ((T12 / 2, H12, 0), F.cm(T12), (0, -9)),
                                       ((0, H12 / 2, 0), F.cm(H12), (-18, 0)),
                                       (((B12 + T12) / 2, H12 / 2, 0), F.cm(S12), (-16, -4)),
                                       ((B12, 0, D12 / 2), F.cm(D12), (16, -6))],
                               width=230, height=170),
    'choices': C12, 'answer_choice': K12, 'answer_print': '%d cm²' % ANS12,
    'distractor_why': ['옆넓이만 구함: 18 × 7 = 126',
                       '옆면 중 빗변 5 cm 쪽 직사각형을 빠뜨림',
                       '밑넓이를 한 번만 더함: 18 + 126',
                       '밑면을 6 × 4 직사각형으로 봄: 48 + 126'],
    'hint': '기둥의 겉넓이 = (밑넓이) × 2 + (옆넓이), 옆넓이 = (밑면의 둘레) × (높이)예요.',
    'solution': '① 밑넓이: 사다리꼴 (3 + 6) × 4 ÷ 2 = 18 (cm²)<br>'
                '② 밑면의 둘레: 3 + 4 + 6 + 5 = 18 (cm), 기둥의 높이는 7 cm<br>'
                '③ 옆넓이: 18 × 7 = 126 (cm²)<br>'
                '④ 겉넓이: 18 × 2 + 126 = 162 (cm²)<br>'
                '자주 하는 실수: 이 기둥은 사다리꼴이 앞·뒤에 있는 "누운 기둥"이에요. 사다리꼴 2개가 밑면이에요.',
}

# ═════════════════════════════════════════ 13 부채꼴 기둥의 부피 (M)
R13, T13, H13 = 6, 120, 5
BASE13 = R13 * R13 * T13 // 360              # 12 (π)
ANS13 = BASE13 * H13                          # 60π
V13 = [BASE13, ANS13 // 3, ANS13, R13 * R13 * (360 - T13) // 360 * H13, R13 * R13 * H13]
C13, K13 = choice(V13, ANS13, lambda v: pi(v) + ' cm³')
P13 = {
    'id': 'm3-13', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '기둥의 부피',
    'stem_print': '다음 그림은 밑면이 부채꼴인 기둥이다. 이 기둥의 부피는?',
    'figure': fig_sector_prism(R13, T13, H13, F.cm(R13), F.deg(T13), F.cm(H13)),
    'choices': C13, 'answer_choice': K13, 'answer_print': pi(ANS13) + ' cm³',
    'distractor_why': ['밑넓이 12π만 구하고 높이를 곱하지 않음',
                       '뿔의 부피처럼 ⅓을 곱함',
                       '중심각을 360° − 120° = 240°로 잘못 씀',
                       '부채꼴이 아니라 원기둥 전체의 부피 π × 6² × 5를 구함'],
    'hint': '밑면이 어떤 모양이든 기둥의 부피 = (밑넓이) × (높이)예요.',
    'solution': '① 밑넓이: π × 6² × 120/360 = 12π (cm²)<br>'
                '② 부피: 12π × 5 = 60π (cm³)<br>'
                '확인: 중심각 120°는 원의 ⅓이니까 원기둥(180π)의 ⅓인 60π예요.',
}

# ═════════════════════════════════════════ 14 사각뿔대의 겉넓이 (M)
B14, T14, S14 = 8, 4, 5                         # 밑변, 윗변, 옆면 사다리꼴의 높이
H14 = math.sqrt(S14 ** 2 - ((B14 - T14) / 2) ** 2)   # 그림용 실제 높이 (계산에는 쓰지 않음)
LAT14 = 4 * (B14 + T14) * S14 // 2              # 120
ANS14 = B14 * B14 + T14 * T14 + LAT14           # 200
V14 = [LAT14, T14 * T14 + LAT14, B14 * B14 + LAT14, ANS14, B14 * B14 + T14 * T14 + 2 * LAT14]
C14, K14 = choice(V14, ANS14, lambda v: '%d cm²' % v)
hb14, ht14 = B14 / 2, T14 / 2


def _slant14(c, proj):
    p0, p1 = proj((0, 0, -hb14)), proj((0, H14, -ht14))
    c.line(p0, p1, dash='3 2', sw=1.0)
    c.right_mark(p0, F._dir(p0, proj((hb14, 0, -hb14))), F._dir(p0, p1), k=6)
    c.text(F._mid(p0, p1), F.cm(S14), size=12, d=(-15, 0))


P14 = {
    'id': 'm3-14', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '각뿔대의 겉넓이',
    'stem_print': '다음 그림과 같이 두 밑면이 정사각형이고 옆면이 모두 합동인 사다리꼴인 사각뿔대의 겉넓이는?',
    'figure': F.fig_polyhedron(*F.frustum(F.reg_base(4, hb14 * math.sqrt(2), 45), T14 / B14, H14), fill='c',
                               view=F.View(tilt=22, yaw=18), extra=_slant14,
                               labels=[((0, 0, -hb14), F.cm(B14), (0, -11)),
                                       ((ht14, H14, 0), F.cm(T14), (16, 2))],
                               width=210, height=170),
    'choices': C14, 'answer_choice': K14, 'answer_print': '%d cm²' % ANS14,
    'distractor_why': ['옆넓이(사다리꼴 4개)만 구함',
                       '아래 밑면 8 × 8을 빠뜨림',
                       '위 밑면 4 × 4를 빠뜨림',
                       '사다리꼴의 넓이에서 ÷ 2를 빠뜨림: 80 + 240'],
    'hint': '각뿔대의 겉넓이 = (두 밑면의 넓이) + (옆면 사다리꼴 4개의 넓이)예요.',
    'solution': '① 두 밑면: 8 × 8 + 4 × 4 = 64 + 16 = 80 (cm²)<br>'
                '② 옆면 하나: 윗변 4, 아랫변 8, 높이 5인 사다리꼴 → (4 + 8) × 5 ÷ 2 = 30 (cm²)<br>'
                '③ 옆넓이: 30 × 4 = 120 (cm²)<br>'
                '④ 겉넓이: 80 + 120 = 200 (cm²)<br>'
                '자주 하는 실수: 5 cm는 입체의 높이가 아니라 옆면 사다리꼴의 높이예요.',
}

# ═════════════════════════════════════════ 15 반구의 겉넓이 (L)
R15 = 5
ANS15 = 3 * R15 * R15                           # 75π
V15 = [R15 * R15, 2 * R15 * R15, ANS15, 4 * R15 * R15, 5 * R15 * R15]
C15, K15 = choice(V15, ANS15, lambda v: pi(v) + ' cm²')
P15 = {
    'id': 'm3-15', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'L', 'topic': '반구의 겉넓이',
    'stem_print': '다음 그림과 같은 반구의 겉넓이는?',
    'figure': F.fig_round([{'t': 'hemi_down', 'r': R15}], labels=[('r', 1, F.cm(R15))], fill=['p'],
                          width=170, height=130),
    'choices': C15, 'answer_choice': K15, 'answer_print': pi(ANS15) + ' cm²',
    'distractor_why': ['평평한 원 부분 π × 5²만 구함',
                       '곡면 4π × 5² ÷ 2만 구하고 평평한 원을 빠뜨림',
                       '구 전체의 겉넓이 4π × 5²를 답함',
                       '곡면을 ÷ 2 하지 않고 4π × 5²에 원을 더함'],
    'hint': '반구의 겉넓이 = (구의 겉넓이의 절반인 곡면) + (잘린 면인 원)이에요.',
    'solution': '① 곡면: 4π × 5² ÷ 2 = 50π (cm²)<br>'
                '② 잘린 면(원): π × 5² = 25π (cm²)<br>'
                '③ 겉넓이: 50π + 25π = 75π (cm²)<br>'
                '자주 하는 실수: 반구의 겉넓이를 2π' + I('r') + '²(곡면)만으로 끝내요. 평평한 원도 겉면이에요.',
}

# ═════════════════════════════════════════ 16 렌즈 넓이 (단답, M)
A16 = 10
Q16 = A16 * A16 // 4                            # 사분원 하나 25π
ANS16 = (2 * Q16, A16 * A16)                    # 50π − 100
P16 = {
    'id': 'm3-16', 'unit': 6, 'points': 4, 'format': 'short', 'level': 'M', 'topic': '겹친 사분원의 넓이',
    'stem_print': '다음 그림은 한 변의 길이가 %d cm인 정사각형의 마주 보는 두 꼭짓점을 중심으로 하여 '
                  '사분원 2개를 그린 것이다. 색칠한 부분의 넓이를 구하시오.' % A16,
    'figure': F.fig_square_quarter(A16, 'lens', fill='m'),
    'answer_print': '(%dπ − %d)' % ANS16, 'answer_unit': 'cm²', 'answer_format': '○π − △ 꼴',
    'hint': '사분원 2개를 정사각형 위에 겹쳐 놓으면, 색칠한 부분만 <b>두 번</b> 덮여요.',
    'solution': '① 사분원 하나: π × 10² × ¼ = 25π (cm²)<br>'
                '② 사분원 2개의 넓이의 합은 정사각형 전체에 색칠한 부분을 한 번 더 더한 것이에요.<br>'
                '③ 색칠한 부분 = 25π × 2 − 10 × 10 = (50π − 100) cm²<br>'
                '다른 방법: 대각선으로 반을 나누면 한쪽은 (사분원 − 직각삼각형) = 25π − 50, 그 2배예요.',
}

# ═════════════════════════════════════════ 17 원뿔 전개도의 중심각 (단답, M)
L17, R17 = 12, 4
ANS17 = 360 * R17 // L17                        # 120
P17 = {
    'id': 'm3-17', 'unit': 7, 'points': 4, 'format': 'short', 'level': 'M', 'topic': '원뿔 전개도 중심각',
    'stem_print': '다음 그림은 원뿔의 전개도이다. 옆면인 부채꼴의 중심각 ∠' + X + '의 크기를 구하시오.',
    'figure': F.fig_net_cone(L17, ANS17, R17, l_label=F.cm(L17), theta_label=X, r_label=F.cm(R17)),
    'answer_print': '%d' % ANS17, 'answer_unit': '°', 'answer_format': '수',
    'hint': '전개도에서 <b>부채꼴의 호의 길이 = 밑면인 원의 둘레</b>예요.',
    'solution': '① 밑면인 원의 둘레: 2π × 4 = 8π (cm)<br>'
                '② 부채꼴의 호의 길이: 2π × 12 × ' + I('x') + '/360<br>'
                '③ 2π × 12 × ' + I('x') + '/360 = 8π → ' + I('x') + '/360 = ⅓ → ∠' + X + ' = 120°<br>'
                '빠른 확인: 중심각 = 360° × (밑면의 반지름) ÷ (모선의 길이) = 360° × 4 ÷ 12 = 120°',
}

# ═════════════════════════════════════════ 18 원뿔 그릇 → 원기둥 그릇 (단답, M)
R18c, H18c, R18 = 6, 8, 4
VOL18 = R18c * R18c * H18c // 3                 # 96π
ANS18 = VOL18 // (R18 * R18)                    # 6
FIG18 = side_by_side(
    (F.fig_round([{'t': 'cone_down', 'r': R18c, 'h': H18c}], labels=[('r', 1, F.cm(R18c)), ('h', 0, F.cm(H18c))],
                 fill=['c'], width=140, height=170), ''),
    ('<span style="font-size:16pt;color:#c2185b">⟶</span>', ''),
    (F.fig_round([{'t': 'cyl', 'r': R18, 'h': ANS18}, {'t': 'cyl', 'r': R18, 'h': 3}],
                 labels=[('r', 2, F.cm(R18)), ('hs', 0, F.it('h') + 'cm')], fill=['c', None],
                 width=130, height=170), ''))
P18 = {
    'id': 'm3-18', 'unit': 7, 'points': 4, 'format': 'short', 'level': 'M', 'topic': '그릇에 옮겨 담은 물',
    'stem_print': '다음 그림과 같은 원뿔 모양의 그릇에 물을 가득 채운 뒤, 이 물을 모두 밑면의 반지름의 길이가 '
                  '%d cm인 원기둥 모양의 그릇에 옮겨 담았다. 원기둥 모양 그릇의 물의 높이 ' % R18 + I('h')
                  + '를 구하시오. (단, 그릇의 두께는 생각하지 않는다.)',
    'figure': FIG18,
    'answer_print': '%d' % ANS18, 'answer_unit': 'cm', 'answer_format': '수',
    'hint': '옮겨 담아도 물의 <b>부피는 그대로</b>예요. 원뿔의 부피 = 원기둥 속 물의 부피.',
    'solution': '① 원뿔 그릇의 물: ⅓ × π × 6² × 8 = 96π (cm³)<br>'
                '② 원기둥 그릇의 물: π × 4² × ' + I('h') + ' = 16π' + I('h') + '<br>'
                '③ 16π' + I('h') + ' = 96π → ' + I('h') + ' = 6 (cm)<br>'
                '자주 하는 실수: 원뿔의 부피에서 ⅓을 빠뜨리면 ' + I('h') + ' = 18이 나와요.',
}

# ═════════════════════════════════════════ 19 정다각형 (서술, M)
R19 = (7, 2)
EXT19 = 180 * R19[1] // sum(R19)                # 40
N19 = 360 // EXT19                              # 9
DIAG19 = N19 * (N19 - 3) // 2                   # 27
SUM19 = 180 * (N19 - 2)                         # 1260
P19 = {
    'id': 'm3-19', 'unit': 6, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '내각·외각의 비',
    'stem_print': '한 내각의 크기와 한 외각의 크기의 비가 %d : %d인 정다각형이 있다. 다음을 차례로 구하시오.<br>'
                  '(1) 이 정다각형의 이름 &nbsp; (2) 대각선의 총 개수 &nbsp; (3) 내각의 크기의 합' % R19,
    'figure': None,
    'answer_print': '(1) 정구각형 (2) %d개 (3) %d°' % (DIAG19, SUM19), 'answer_unit': None,
    'hint': '한 내각과 한 외각의 합은 180°예요. 180°를 7 : 2로 나눠요.',
    'solution': '① 한 외각 = 180° × 2/9 = 40° (한 내각은 140°)<br>'
                '② 정다각형의 외각의 합은 360°이므로 360° ÷ 40° = 9 → 정구각형<br>'
                '③ 대각선의 총 개수 = 9 × (9 − 3) ÷ 2 = 27(개)<br>'
                '④ 내각의 크기의 합 = 180° × (9 − 2) = 1260°<br>'
                '확인: 140° × 9 = 1260° 맞아요.',
    'rubric': [{'step': '한 외각의 크기 40°를 구함', 'points': 2},
               {'step': '360° ÷ 40° = 9로 정구각형을 구함', 'points': 2},
               {'step': '대각선의 총 개수 27개를 구함', 'points': 2},
               {'step': '내각의 크기의 합 1260°를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 20 사분원 − 반원 (서술, M)
R20 = 8
QA20 = R20 * R20 // 4                           # 사분원 넓이 16π
SA20 = (R20 // 2) ** 2 // 2                     # 반원 넓이 8π
AREA20 = QA20 - SA20                            # 8π
QL20 = 2 * R20 // 4                             # 사분원 호 4π
SL20 = R20 // 2                                 # 반원 호 4π
PER20 = (QL20 + SL20, R20)                      # 8π + 8
P20 = {
    'id': 'm3-20', 'unit': 6, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '색칠한 부분 넓이·둘레',
    'stem_print': '다음 그림은 반지름의 길이가 %d cm인 사분원 안에, 한 반지름을 지름으로 하는 반원을 그린 것이다. '
                  '색칠한 부분의 넓이와 둘레의 길이를 각각 구하시오.' % R20,
    'figure': fig_quarter_minus_semi(R20, fill='g'),
    'answer_print': '넓이 %s cm², 둘레 (%s + %d) cm' % (pi(AREA20), pi(PER20[0]), PER20[1]), 'answer_unit': None,
    'hint': '넓이는 (사분원) − (반원). 둘레는 큰 호 + 반원의 호 + <b>곧은 선분 하나</b>예요.',
    'solution': '① 사분원의 넓이: π × 8² × ¼ = 16π, 반원의 넓이: π × 4² × ½ = 8π<br>'
                '② 넓이 = 16π − 8π = 8π (cm²)<br>'
                '③ 사분원의 호: 2π × 8 × ¼ = 4π, 반원의 호: 2π × 4 × ½ = 4π<br>'
                '④ 둘레 = 4π + 4π + 8 = (8π + 8) cm — 왼쪽 반지름 8 cm는 둘레에 들어가고, 아래쪽 반지름은 반원의 지름이라 들어가지 않아요.',
    'rubric': [{'step': '사분원의 넓이 16π와 반원의 넓이 8π를 구함', 'points': 2},
               {'step': '색칠한 부분의 넓이 8π cm²를 구함', 'points': 2},
               {'step': '사분원의 호 4π와 반원의 호 4π를 구함', 'points': 2},
               {'step': '선분 8 cm를 더해 둘레 (8π + 8) cm를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 21 속이 빈 원기둥의 부피 (서술, M)
G21, W21, H21 = 2, 3, 6                         # 축에서 떨어진 거리, 직사각형 가로, 세로
RO21 = G21 + W21                                # 5
VO21 = RO21 * RO21 * H21                        # 150π
VI21 = G21 * G21 * H21                          # 24π
ANS21 = VO21 - VI21                             # 126π
SHAPE21 = [(G21, 0), (RO21, 0), (RO21, H21), (G21, H21)]
LAB21 = [((G21 / 2, 0), F.cm(G21), (0, -10)), ((G21 + W21 / 2, 0), F.cm(W21), (0, -10)),
         ((RO21, H21 / 2), F.cm(H21), (18, 0))]
P21 = {
    'id': 'm3-21', 'unit': 7, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '속이 빈 회전체의 부피',
    'stem_print': '다음 그림과 같이 회전축 ' + I('l') + '에서 %d cm 떨어진 직사각형을 직선 ' % G21 + I('l')
                  + '을 회전축으로 하여 1회전 시킬 때 생기는 입체도형의 부피를 구하시오.',
    'figure': F.fig_rotation(SHAPE21, labels=LAB21, fill='o', width=190, height=200),
    'figure_sol': F.fig_rotation(SHAPE21, labels=LAB21, fill='o', mirror=True, width=260, height=200),
    'answer_print': pi(ANS21), 'answer_unit': 'cm³',
    'hint': '가운데가 빈 원기둥이에요. (큰 원기둥) − (빈 부분 원기둥)으로 구해요.',
    'solution': '① 회전체는 가운데가 빈 원기둥이에요. 바깥 반지름 2 + 3 = 5 cm, 빈 부분의 반지름 2 cm, 높이 6 cm<br>'
                '② 큰 원기둥: π × 5² × 6 = 150π (cm³)<br>'
                '③ 빈 부분: π × 2² × 6 = 24π (cm³)<br>'
                '④ 부피 = 150π − 24π = 126π (cm³)<br>'
                '자주 하는 실수: 바깥 반지름을 3 cm(직사각형의 가로)로 써요. 반지름은 <b>회전축에서</b> 재요.',
    'rubric': [{'step': '가운데가 빈 원기둥이고 바깥 반지름 5 cm, 안쪽 반지름 2 cm임을 앎', 'points': 2},
               {'step': '바깥 원기둥의 부피 150π를 구함', 'points': 2},
               {'step': '빈 부분의 부피 24π를 구함', 'points': 2},
               {'step': '부피 126π cm³를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 22 두 원기둥을 쌓은 입체의 겉넓이 (서술, M)
R22a, H22a, R22b, H22b = 5, 4, 3, 5
FLAT22 = 2 * R22a * R22a                        # 50π (위에서 보이는 평면 = 아래 밑면)
LATA22 = 2 * R22a * H22a                        # 40π
LATB22 = 2 * R22b * H22b                        # 30π
ANS22 = FLAT22 + LATA22 + LATB22                # 120π
P22 = {
    'id': 'm3-22', 'unit': 7, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '쌓은 입체의 겉넓이',
    'stem_print': '다음 그림은 두 원기둥의 밑면의 중심을 맞추어 쌓아 만든 입체도형이다. '
                  '이 입체도형의 겉넓이를 구하시오.',
    'figure': fig_two_cyl(R22a, H22a, R22b, H22b, [F.cm(R22a), F.cm(R22b), F.cm(H22a), F.cm(H22b)]),
    'answer_print': pi(ANS22), 'answer_unit': 'cm²',
    'hint': '위에서 내려다보면 보이는 평평한 면(위 원기둥의 윗면 + 아래 원기둥의 드러난 고리)을 합치면 큰 원 하나와 같아요.',
    'solution': '① 아래 밑면: π × 5² = 25π<br>'
                '② 위에서 보이는 면: 위 원기둥의 윗면 π × 3² = 9π, 아래 원기둥 윗면의 드러난 부분 25π − 9π = 16π → 합 25π<br>'
                '③ 아래 원기둥의 옆넓이: 2π × 5 × 4 = 40π, 위 원기둥의 옆넓이: 2π × 3 × 5 = 30π<br>'
                '④ 겉넓이 = 25π + 25π + 40π + 30π = 120π (cm²)<br>'
                '자주 하는 실수: 두 원기둥의 겉넓이를 각각 구해 더하면 붙은 면(9π)이 두 번 더해져 138π가 나와요.',
    'rubric': [{'step': '위·아래에서 보이는 평평한 면의 넓이 25π + 25π = 50π를 구함 (붙은 면 처리)', 'points': 2},
               {'step': '아래 원기둥의 옆넓이 40π를 구함', 'points': 2},
               {'step': '위 원기둥의 옆넓이 30π를 구함', 'points': 2},
               {'step': '겉넓이 120π cm²를 구함', 'points': 2}],
}

PROBLEMS = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15,
            P16, P17, P18, P19, P20, P21, P22]


def check():
    """모든 정답을 문항을 만든 변수에서 다시 계산한다."""
    # 1
    assert N1 - 3 == 7 and ANS1 == 35
    # 2 맞꼭지각: 두 삼각형의 나머지 두 각의 합이 같다
    assert TH2 == 55 and 180 - TH2 - G2 == ANS2 == 65
    # 3 육각형
    assert sum(INT3) == 720 and ANS3 == INT3[5] == 130
    got = F.interior_angles(P3pts)
    assert all(abs(g - a) < 1e-6 for g, a in zip(got, INT3)), got
    # 4 외각의 합
    assert sum(EXT4) == 360 and EXT4[2] == ANS4 == 65 and EXT4[4] == ANS4 + K4ADD
    got = F.interior_angles(P4pts)
    assert all(abs(g - a) < 1e-6 for g, a in zip(got, INT4)), got
    # 5
    assert 180 * (N5 - 2) == S5 and N5 == 10 and ANS5 == 36
    # 6 정비례
    assert X6 * L6a == L6b * A6 and Y6 * A6 == C6 * L6a and ANS6 == 118
    assert abs(3.2 * math.radians(A6) / (3.2 * math.radians(X6)) - L6a / L6b) < 1e-9
    assert sum([A6, X6, C6]) < 360
    # 7 삼각형 넓이는 3배가 아니다 (½r²sinθ), 현은 3배보다 짧다
    tri = lambda t: 0.5 * math.sin(math.radians(t))
    chord = lambda t: 2 * math.sin(math.radians(t / 2))
    assert C7 == 3 * A7 and abs(tri(C7) / tri(A7) - 3) > 0.5 and chord(C7) < 3 * chord(A7)
    # 8
    assert abs(2 * math.pi * R8 * TH8 / 360 - L8 * math.pi) < 1e-9
    assert abs(math.pi * R8 ** 2 * TH8 / 360 - ANS8 * math.pi) < 1e-9 and ANS8 == 30 and TH8 == 75
    # 9
    V, Fc = F.pyramid(F.reg_base(N9, 2.6, 0), 4.2)
    edges = {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in Fc for k in range(len(f))}
    assert len(edges) == E9 and len(V) == VX9 and len(Fc) == FC9 and ANS9 == 16
    # 10 정이십면체
    V, Fc = icosahedron(2.2)
    edges = {tuple(sorted((f[k], f[(k + 1) % 3]))) for f in Fc for k in range(3)}
    deg_ = [sum(1 for f in Fc if i in f) for i in range(len(V))]
    assert len(Fc) == F10 and len(edges) == b10 and len(V) == c10 and set(deg_) == {a10} and ANS10 == 47
    # 11: ④ 축에 붙은 직사각형만 높이마다 가로 길이가 같아 단면이 합동인 원
    assert P11['answer_choice'] == 4
    # 12
    assert math.dist(V12f[1], V12f[2]) == S12
    assert ANS12 == 2 * (B12 + T12) * H12 / 2 + (B12 + T12 + H12 + S12) * D12 == 162
    # 13
    assert abs(math.pi * R13 ** 2 * T13 / 360 * H13 - ANS13 * math.pi) < 1e-9 and ANS13 == 60
    # 14 그림의 옆면 높이(모선 방향 거리)가 S14 와 같은지
    assert abs(math.dist((0, 0, -hb14), (0, H14, -ht14)) - S14) < 1e-9 and ANS14 == 200
    # 15
    assert abs(4 * math.pi * R15 ** 2 / 2 + math.pi * R15 ** 2 - ANS15 * math.pi) < 1e-9
    # 16
    lens = 2 * (math.pi * A16 ** 2 / 4) - A16 ** 2
    assert abs(lens - (ANS16[0] * math.pi - ANS16[1])) < 1e-9 and lens > 0
    # 17
    assert abs(2 * math.pi * L17 * ANS17 / 360 - 2 * math.pi * R17) < 1e-9
    # 18
    assert abs(math.pi * R18c ** 2 * H18c / 3 - math.pi * R18 ** 2 * ANS18) < 1e-9 and ANS18 == 6
    # 19
    assert (180 - EXT19) * R19[1] == EXT19 * R19[0] and N19 == 9 and DIAG19 == 27 and SUM19 == 1260
    # 20
    area = math.pi * R20 ** 2 / 4 - math.pi * (R20 / 2) ** 2 / 2
    per = 2 * math.pi * R20 / 4 + math.pi * (R20 / 2) + R20
    assert abs(area - AREA20 * math.pi) < 1e-9 and abs(per - (PER20[0] * math.pi + PER20[1])) < 1e-9
    # 21
    assert abs(math.pi * (RO21 ** 2 - G21 ** 2) * H21 - ANS21 * math.pi) < 1e-9 and ANS21 == 126
    # 22
    tot = (math.pi * R22a ** 2 + (math.pi * R22a ** 2 - math.pi * R22b ** 2) + math.pi * R22b ** 2
           + 2 * math.pi * R22a * H22a + 2 * math.pi * R22b * H22b)
    assert abs(tot - ANS22 * math.pi) < 1e-9 and ANS22 == 120
    # 형식: 수치 보기는 크기 순이고 서로 다르다
    for vals in (V1, V2, V3, V4, V5, V6, V8, V9, V10, V12, V13, V14, V15):
        assert vals == sorted(vals) and len(set(vals)) == 5, vals
    ans_num = {1: (K1, C1, P1), 2: (K2, C2, P2), 3: (K3, C3, P3)}
    for k, (kk, cc, p) in ans_num.items():
        assert p['choices'][p['answer_choice'] - 1] == cc[kk - 1]
    pts = 0
    for p in PROBLEMS:
        pts += p['points']
        if p['format'] == 'choice5':
            assert len(p['choices']) == 5 and len(p['distractor_why']) == 4
            if p['points'] == 3:
                assert p['level'] == 'L'
        if p['format'] == 'essay':
            assert sum(s['points'] for s in p['rubric']) == p['points']
    assert pts == 100 and len(PROBLEMS) == 22
    assert sum(1 for p in PROBLEMS if p['level'] == 'L') == 5
    print('check OK: mock3 22문항 정답 재계산 일치')
