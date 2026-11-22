"""모의고사 1회 — 중1 2학기 기말 대비 (교과서 6단원 평면도형의 성질 · 7단원 입체도형의 성질)

성격: 기본 다지기. 22문항 · 100점 · 45분. L 8문항, 나머지 M.
그림의 라벨 수치와 정답 계산은 모두 이 파일 위쪽의 같은 변수에서 나온다. check() 가 다시 계산한다.
"""
import math

import figgen as F

PI = 'π'
X = F.X_ITAL
XI = '<i>x</i>'


def num(v):
    """정수면 정수로, 아니면 소수 한 자리까지."""
    return str(int(round(v))) if abs(v - round(v)) < 1e-9 else ('%.1f' % v)


META = {'id': 'm1-term2-mock1', 'kind': 'exam', 'title': '모의고사 1회',
        'subtitle': '기본 다지기 · 6단원 평면도형의 성질 · 7단원 입체도형의 성질 · 22문항 100점',
        'time_min': 45, 'folder': '모의고사', 'file': '모의고사1회'}


# ═════════════════════════════════════════ 세트 전용 그림
@F.autofit
def fig_circle_three(R, a0, step, lab, chords, scale=22, width=200, height=170):
    """원 O에서 같은 중심각 step 세 개(A→B→C→D, 반시계). 각 라벨은 겹치지 않게 반지름을 번갈아 둔다."""
    c = F.Canvas(scale)
    O = (0, 0)
    names = 'ABCD'
    angs = [a0 + step * i for i in range(4)]
    pt = {n: F._add(O, F._u(a), R) for n, a in zip(names, angs)}
    c.poly([O] + c.arc_pts(O, R, angs[0], angs[3], n=60), fill=F.FILL['g'], stroke='none', opacity=0.7)
    c.circle(O, R)
    for n in names:
        c.line(O, pt[n])
    for a, b in chords:
        c.line(pt[a], pt[b], sw=1.2, stroke=F.ACCENT2)
    for i in range(3):
        c.angle_mark(O, angs[i], angs[i + 1], r=14, label=lab, size=12)
    for n, a in zip(names, angs):
        c.text(pt[n], n, size=12, d=F._scale(F._u(a), 10))
    c.dot(O)
    c.text(O, 'O', size=12, d=(0, -11))
    return c.svg(width, height)


@F.autofit
def fig_two_sectors_x(R, pts, ang_labels, arc_labels, fill='p', lr=50, scale=22, width=200, height=200):
    """원 O에서 부채꼴 두 개(색칠). 좁은 중심각의 라벨이 반지름 선에 걸리지 않도록 라벨 거리 lr(px)을 크게 둔다.
    pts {'A': 각도, ...}, ang_labels [('A','B','30°')], arc_labels [('A','B','4cm')]"""
    c = F.Canvas(scale)
    O = (0, 0)
    P = {k: F._add(O, F._u(a), R) for k, a in pts.items()}
    for a, b, _ in ang_labels:
        span = (pts[b] - pts[a]) % 360
        c.poly([O] + c.arc_pts(O, R, pts[a], pts[a] + span, n=60), fill=F.FILL[fill], stroke='none')
    c.circle(O, R)
    for k in pts:
        c.line(O, P[k])
    for a, b, lab in ang_labels:
        c.angle_mark(O, pts[a], pts[b], r=12, label=lab, size=12, lr=lr)
    for a, b, lab in arc_labels:
        m = pts[a] + ((pts[b] - pts[a]) % 360) / 2
        c.text(F._add(O, F._u(m), R), lab, size=12, d=F._scale(F._u(m), 20))
    for k, a in pts.items():
        c.text(P[k], k, size=12, d=F._scale(F._u(a), 10))
    c.dot(O)
    c.text(O, 'O', size=12, d=(0, 11))
    return c.svg(width, height)


@F.autofit
def fig_cyl_cone(r, hc, hk, r_label, hc_label=None, hk_label=None, l_label=None, fills=('g', 'p'), tilt=17,
                 scale=22, width=170, height=220):
    """원기둥(높이 hc, 0이면 없음) 위에 원뿔(높이 hk)을 붙인 회전체. fig_round 와 같은 그림 규칙
    (보이는 밑면 앞쪽 실선·뒤쪽 점선)으로 그리되, 라벨이 옆선·타원에 걸리지 않게 위치를 따로 잡는다."""
    c = F.Canvas(scale)
    t = math.radians(tilt)
    k, ch = math.sin(t), math.cos(t)
    y0, y1 = 0.0, hc * ch
    y2 = y1 + hk * ch

    def ell(yc, a0, a1):
        return c.arc_pts((0, yc), r, a0, a1, n=60, ry=r * k)

    if hc > 0:
        c.poly(ell(y0, 180, 360) + ell(y1, 0, 180), fill=F.FILL[fills[0]], stroke='none')
    c.poly(ell(y1, 180, 360) + [(0, y2)], fill=F.FILL[fills[-1]], stroke='none')
    phi = math.asin(min(1, r * k / (y2 - y1)))
    for sg in (1, -1):
        c.line((sg * r * math.cos(phi), y1 + r * k * math.sin(phi)), (0, y2))
        if hc > 0:
            c.line((sg * r, y0), (sg * r, y1))
    levels = [y0, y1] if hc > 0 else [y1]
    for yc in levels:
        c.poly(ell(yc, 180, 360), close=False)
        c.poly(ell(yc, 0, 180), close=False, dash='4 3', sw=1.0)
    # 원뿔의 높이(축)
    c.line((0, y1), (0, y2), dash='3 2', sw=1.0)
    c.right_mark((0, y1), 0, 90, k=6)
    # 밑면 반지름: 맨 아래 밑면, 라벨은 반지름 선 위쪽(뒤쪽 점선 호 아래)
    c.line((0, y0), (r, y0), dash='3 2', sw=1.0)
    c.dot((0, y0), r=1.8)
    c.text((r / 2, y0), r_label, size=12, d=(0, 9))
    if hc_label:
        c.text((r, (y0 + y1) / 2), hc_label, size=12, d=(20, 0))
    if hk_label:
        c.text((0, y1 + (y2 - y1) * 0.3), hk_label, size=12, d=(-20, 0))
    if l_label:
        a = math.atan2(y2 - y1, -r)                      # 오른쪽 옆선 방향
        nx, ny = math.sin(a), -math.cos(a)               # 바깥쪽 법선
        c.text((r / 2, (y1 + y2) / 2), l_label, size=12, d=(nx * 18, ny * 18))
    return c.svg(width, height)


@F.autofit
def fig_prism_net(a, b, hyp, h, scale=22, width=250, height=210):
    """직각삼각형(빗변이 아닌 두 변 a, b, 빗변 hyp) 밑면의 삼각기둥 전개도.
    옆면 직사각형 세 개(가로 a, b, hyp, 세로 h)를 잇고, 가로 b인 직사각형 위아래에 밑면 삼각형을 붙인다."""
    c = F.Canvas(scale)
    xs = [0, a, a + b, a + b + hyp]
    cols = ['c', 'y', 'c']
    for i in range(3):
        c.poly([(xs[i], 0), (xs[i + 1], 0), (xs[i + 1], h), (xs[i], h)], fill=F.FILL[cols[i]])
    top = [(a, h), (a + b, h), (a, h + a)]
    bot = [(a, 0), (a + b, 0), (a, -a)]
    c.poly(top, fill=F.FILL['m'])
    c.poly(bot, fill=F.FILL['m'])
    c.right_mark((a, h), 0, 90)
    c.right_mark((a, 0), 0, -90)
    c.text((a / 2, 0), F.cm(a), size=12, d=(0, -10))
    c.text((a + b / 2, h), F.cm(b), size=12, d=(0, -10))
    c.text((a + b + hyp / 2, 0), F.cm(hyp), size=12, d=(0, -10))
    c.text((xs[3], h / 2), F.cm(h), size=12, d=(20, 0))
    return c.svg(width, height)


@F.autofit
def fig_quarter_minus_semi(r, fill='m', scale=22, width=170, height=170):
    """반지름 r인 사분원 OAB 안에서 반지름 OA를 지름으로 하는 반원을 뺀 부분을 색칠."""
    c = F.Canvas(scale)
    O, A, B = (0, 0), (0, r), (r, 0)
    quarter = c.arc_pts(O, r, 0, 90, n=60)                  # B → A
    semi = c.arc_pts((0, r / 2), r / 2, 90, -90, n=60)       # A → O (오른쪽으로 볼록)
    c.poly([O] + quarter + semi[1:-1], fill=F.FILL[fill])
    c.line(O, A)
    c.dot(O)
    c.text(O, 'O', size=12, d=(-9, -9))
    c.text(A, 'A', size=12, d=(-9, 6))
    c.text(B, 'B', size=12, d=(8, -8))
    c.text((r / 2, 0), F.cm(r), size=12, d=(0, -10))
    return c.svg(width, height)


def _box(x0, y0, z0, w, h, d):
    V = [(x0 + x, y0 + y, z0 + z) for y in (0, h) for x, z in ((0, 0), (w, 0), (w, d), (0, d))]
    Fc = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return V, Fc


def _draw_convex(c, view, V, Fc, fills, cover=False):
    """fig_polyhedron 과 같은 방식(볼록 입체 하나): 보이는 면 색칠, 숨은 모서리 점선."""
    R = [view.rot(p) for p in V]
    cen = tuple(sum(p[k] for p in R) / len(R) for k in range(3))
    vd = view.vdir()

    def normal(face):
        a, b, cc = R[face[0]], R[face[1]], R[face[2]]
        u = [b[k] - a[k] for k in range(3)]
        v = [cc[k] - a[k] for k in range(3)]
        nn = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        fc = [sum(R[i][k] for i in face) / len(face) for k in range(3)]
        if sum(nn[k] * (fc[k] - cen[k]) for k in range(3)) < 0:
            nn = tuple(-x for x in nn)
        return nn

    vis = [sum(n_ * d for n_, d in zip(normal(f), vd)) < -1e-9 for f in Fc]
    P2 = [view.proj(p) for p in V]
    for fi, f in enumerate(Fc):
        if vis[fi]:
            if cover:
                c.poly([P2[i] for i in f], fill='#ffffff', stroke='none')
            c.poly([P2[i] for i in f], fill=F.FILL[fills[fi % len(fills)]], stroke='none', opacity=0.8)
    edges = {}
    for fi, f in enumerate(Fc):
        for k in range(len(f)):
            edges.setdefault(tuple(sorted((f[k], f[(k + 1) % len(f)]))), []).append(fi)
    for (a, b), fs in sorted(edges.items(), key=lambda e: any(vis[i] for i in e[1])):
        v_ = any(vis[i] for i in fs)
        c.line(P2[a], P2[b], dash=None if v_ else '4 3', sw=1.4 if v_ else 1.0)


@F.autofit
def fig_box_cube(W, D, H, a, cx, cz, scale=22, width=270, height=220):
    """직육면체(가로 W, 깊이 D, 높이 H) 윗면 위에 한 모서리 a인 정육면체를 올린 입체."""
    c = F.Canvas(scale)
    view = F.View(tilt=22, yaw=25)
    V1, F1 = _box(0, 0, 0, W, H, D)
    _draw_convex(c, view, V1, F1, ['c', 'c', 'y', 'c', 'c', 'g'])
    V2, F2 = _box(cx, H, cz, a, a, a)
    _draw_convex(c, view, V2, F2, ['m', 'm', 'o', 'm', 'm', 'p'], cover=True)
    pj = view.proj
    c.text(pj((W / 2, 0, 0)), F.cm(W), size=12, d=(0, -11))
    c.text(pj((0, 0, D / 2)), F.cm(D), size=12, d=(-20, -4))
    c.text(pj((W, H / 2, 0)), F.cm(H), size=12, d=(18, 0))
    c.text(pj((cx, H + a / 2, cz + a)), F.cm(a), size=12, d=(-18, 0))
    return c.svg(width, height)


def trap_prism(B, T, H, D):
    """앞면이 등변사다리꼴(아랫변 B, 윗변 T, 높이 H)이고 깊이 D인 사각기둥."""
    front = [(0, 0), (B, 0), ((B + T) / 2, H), ((B - T) / 2, H)]
    V = [(x, y, 0) for x, y in front] + [(x, y, D) for x, y in front]
    Fc = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return V, Fc


# ═════════════════════════════════════════ 1. 대각선 (글)
N1_FROM = 3                          # 한 꼭짓점에서 그은 대각선 수
N1 = N1_FROM + 3                     # 육각형
D1 = N1 * (N1 - 3) // 2
P1 = {
    'id': 'm1-01', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L',
    'topic': '대각선의 개수',
    'stem_print': '한 꼭짓점에서 그을 수 있는 대각선의 개수가 %d인 다각형의 대각선의 총 개수는?' % N1_FROM,
    'figure': None,
    'choices': ['5', '6', str(D1), '15', '18'], 'answer_choice': 3,
    'distractor_why': ['n − 2 = 3으로 잘못 세워 오각형으로 봄 (5 × 2 ÷ 2 = 5)',
                       '다각형의 변의 개수 6을 대각선의 개수로 답함',
                       '변까지 포함해 두 꼭짓점을 잇는 선분을 모두 셈 (6 × 5 ÷ 2 = 15)',
                       '6 × 3 = 18에서 2로 나누지 않음 (대각선 하나를 두 번 셈)'],
    'answer_print': str(D1),
    'hint': 'n각형의 한 꼭짓점에서 그을 수 있는 대각선은 (n − 3)개예요. 먼저 n을 구해요.',
    'solution': '① n − 3 = %d 이므로 n = %d, 육각형이에요.<br>'
                '② 대각선의 총 개수 = n(n − 3) ÷ 2 = %d × %d ÷ 2 = %d<br>'
                '자주 하는 실수: 2로 나누지 않으면 대각선 하나(양 끝 두 꼭짓점)를 두 번 세게 돼요.'
                % (N1_FROM, N1, N1, N1 - 3, D1),
}

# ═════════════════════════════════════════ 2. 삼각형의 외각
A2, X2 = 45, 70                      # ∠A, ∠B(=x)
C2 = 180 - A2 - X2                   # ∠C 내각
E2 = 180 - C2                        # ∠C 외각
T2 = F.polygon_by_angles([A2, X2, C2], [4])
P2 = {
    'id': 'm1-02', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'L',
    'topic': '삼각형의 외각',
    'stem_print': '다음 그림의 삼각형 ABC에서 ∠' + XI + '의 크기는?',
    'figure': F.fig_polygon(T2, angles={0: F.deg(A2)}, unknown={1: X}, ext={2: F.deg(E2)}, names='ABC',
                            fill='o', width=210, height=170),
    'choices': ['65°', '70°', '115°', '135°', '160°'], 'answer_choice': 2,
    'distractor_why': ['180° − 115° = 65°로 꼭짓점 C의 내각을 구하고 멈춤',
                       '외각 115°를 ∠x와 같은 각으로 봄',
                       '180° − 45° = 135°로 꼭짓점 A의 외각을 구함',
                       '115° + 45° = 160°로 빼야 할 것을 더함'],
    'answer_print': F.deg(X2),
    'hint': '삼각형의 한 외각의 크기는 그와 이웃하지 않는 두 내각의 크기의 합과 같아요.',
    'solution': '① 꼭짓점 C의 외각 %d°는 이웃하지 않는 두 내각 ∠A와 ∠B의 합이에요.<br>'
                '② %d° = %d° + ∠<i>x</i> → ∠<i>x</i> = %d°<br>'
                '(확인: ∠C = 180° − %d° = %d°, %d° + %d° + %d° = 180°)'
                % (E2, E2, A2, X2, E2, C2, A2, X2, C2),
}

# ═════════════════════════════════════════ 3. 육각형의 내각의 합
INT3 = [125, 110, 140, 115, 100, 130]     # 꼭짓점 0~5(반시계), 2가 x, 4는 외각으로 표시
X3 = INT3[2]
E3 = 180 - INT3[4]
H3 = F.polygon_by_angles(INT3, [4, 3, 3, 3.5])
_show3 = {0: F.deg(INT3[0]), 1: F.deg(INT3[1]), 3: F.deg(INT3[3]), 5: F.deg(INT3[5])}
P3 = {
    'id': 'm1-03', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '육각형의 내각의 합',
    'stem_print': '다음 그림의 육각형에서 ∠' + XI + '의 크기는?',
    'figure': F.fig_polygon(H3, angles=_show3, unknown={2: X}, ext={4: F.deg(E3)}, fill='y',
                            width=220, height=210),
    'figure_sol': F.fig_polygon(H3, angles=_show3, unknown={2: X}, ext={4: F.deg(E3)}, fill='y',
                                accent={4: F.deg(INT3[4])}, width=220, height=210),
    'choices': ['80°', '100°', '120°', '140°', '160°'], 'answer_choice': 4,
    'distractor_why': ['외각 80°를 ∠x로 착각함',
                       '외각이 있는 꼭짓점의 내각 100°를 답으로 씀',
                       '정육각형의 한 내각 120°로 어림함 (이 육각형은 정육각형이 아니에요)',
                       '외각 80°를 내각처럼 그대로 더해 720° − 560° = 160°로 계산함'],
    'answer_print': F.deg(X3),
    'hint': '육각형의 내각의 합은 180° × (6 − 2) = 720°예요. 그림의 %d°는 <b>외각</b>이에요.' % E3,
    'solution': '① 육각형의 내각의 합: 180° × 4 = 720°<br>'
                '② 외각 %d°인 꼭짓점의 내각: 180° − %d° = %d° (자홍색)<br>'
                '③ %d° + %d° + ∠<i>x</i> + %d° + %d° + %d° = 720° → ∠<i>x</i> = %d°<br>'
                '자주 하는 실수: 변을 연장한 선과 이루는 각은 외각이라 내각으로 바꿔서 더해야 해요.'
                % (E3, E3, INT3[4], INT3[0], INT3[1], INT3[3], INT3[4], INT3[5], X3),
}

# ═════════════════════════════════════════ 4. 오각형의 외각의 합
EXT4 = [72, 65, 60, 85, 78]               # 꼭짓점 2가 x
X4 = EXT4[2]
INT4 = [180 - e for e in EXT4]
Q4 = F.polygon_by_angles(INT4, [4, 3.6, 3.4])
_ext4 = {i: F.deg(EXT4[i]) for i in range(5) if i != 2}
_ext4[2] = X
P4 = {
    'id': 'm1-04', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '다각형의 외각의 합',
    'stem_print': '다음 그림의 오각형에서 ∠' + XI + '의 크기는?',
    'figure': F.fig_polygon(Q4, ext=_ext4, fill='c', width=230, height=220),
    'choices': ['60°', '72°', '108°', '120°', '240°'], 'answer_choice': 1,
    'distractor_why': ['정오각형의 한 외각 360° ÷ 5 = 72°로 어림함',
                       '정오각형의 한 내각 108°로 어림함',
                       '∠x를 구한 뒤 그 꼭짓점의 내각 180° − 60°를 답함',
                       '외각의 합을 내각의 합 540°로 착각해 540° − 300°로 계산함'],
    'answer_print': F.deg(X4),
    'hint': '다각형의 외각의 크기의 합은 변의 개수와 상관없이 항상 360°예요.',
    'solution': '① 오각형의 외각의 합은 360°예요.<br>'
                '② %d° + %d° + ∠<i>x</i> + %d° + %d° = 360°<br>'
                '③ %d° + ∠<i>x</i> = 360° → ∠<i>x</i> = %d°'
                % (EXT4[0], EXT4[1], EXT4[3], EXT4[4], 360 - X4, X4),
}

# ═════════════════════════════════════════ 5. 정다각형 한 내각·한 외각 (글)
K5 = 2                                     # 한 내각 = 한 외각 × 2
N5 = 2 * (K5 + 1)                          # 360/n × (k+1) = 180 → n = 2(k+1)
P5 = {
    'id': 'm1-05', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L',
    'topic': '정다각형 한 내각·외각',
    'stem_print': '한 내각의 크기가 한 외각의 크기의 %d배인 정다각형은?' % K5,
    'figure': None,
    'choices': ['정삼각형', '정사각형', '정오각형', '정육각형', '정팔각형'], 'answer_choice': 4,
    'distractor_why': ['정삼각형은 한 내각 60°, 한 외각 120°로 내각이 외각의 1/2배예요',
                       '정사각형은 한 내각과 한 외각이 모두 90°로 1배예요',
                       '정오각형은 108°와 72°로 1.5배예요',
                       '정팔각형은 135°와 45°로 3배예요'],
    'answer_print': '정육각형',
    'hint': '한 내각 + 한 외각 = 180°예요. 한 외각을 1로 놓으면 한 내각은 2예요.',
    'solution': '① 한 내각과 한 외각의 합은 180°이고, 크기의 비가 2 : 1이에요.<br>'
                '② 한 외각 = 180° × 1/3 = 60°<br>'
                '③ 외각의 합 360°이므로 360° ÷ 60° = 6 → 정육각형<br>'
                '확인: 정육각형의 한 내각은 120°, 한 외각은 60°예요.',
}

# ═════════════════════════════════════════ 6. 중심각과 호의 길이 비례
TH6, L6, M6 = 30, 4, 12                    # ∠AOB, 호 AB, 호 CD
X6 = TH6 * M6 // L6
_pts6 = {'A': 150, 'B': 150 + TH6, 'C': 270, 'D': (270 + X6) % 360}
P6 = {
    'id': 'm1-06', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'L',
    'topic': '중심각과 호의 길이',
    'stem_print': '다음 그림의 원 O에서 ∠COD = ' + XI + '°일 때, ' + XI + '의 값은?',
    'figure': fig_two_sectors_x(3, _pts6, [('A', 'B', F.deg(TH6)), ('C', 'D', X + '°')],
                                [('A', 'B', F.cm(L6)), ('C', 'D', F.cm(M6))], fill='p'),
    'choices': ['10', '38', '60', '90', '120'], 'answer_choice': 4,
    'distractor_why': ['비를 거꾸로 세워 30 ÷ 3 = 10으로 계산함',
                       '호의 길이 차 12 − 4 = 8을 각에 더함 (정비례는 곱해서 늘어나요)',
                       '계산 없이 그림 모양만 보고 2배로 어림함',
                       '30 × 4 = 120으로 호 AB의 길이를 곱함'],
    'answer_print': str(X6),
    'hint': '한 원에서 호의 길이는 중심각의 크기에 정비례해요.',
    'solution': '① 호의 길이가 %d cm에서 %d cm로 %d배가 되었어요.<br>'
                '② 중심각도 %d배: %d° × %d = %d° → <i>x</i> = %d<br>'
                '(비례식으로: %d : <i>x</i> = %d : %d)'
                % (L6, M6, M6 // L6, M6 // L6, TH6, M6 // L6, X6, X6, TH6, L6, M6),
}

# ═════════════════════════════════════════ 7. 부채꼴의 성질 (옳지 않은 것)
TH7 = 40
P7 = {
    'id': 'm1-07', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '호·현·넓이의 성질',
    'stem_print': '다음 그림의 원 O에서 ∠AOB = ∠BOC = ∠COD = %d°일 때, 다음 중 옳지 <b>않은</b> 것은?' % TH7,
    'figure': fig_circle_three(3, 20, TH7, None, [('A', 'B'), ('C', 'D'), ('A', 'D')]),
    'choices': ['호 AB와 호 CD의 길이는 같다.',
                '현 AB와 현 CD의 길이는 같다.',
                '호 AD의 길이는 호 AB의 길이의 3배이다.',
                '현 AD의 길이는 현 AB의 길이의 3배이다.',
                '부채꼴 AOC의 넓이는 부채꼴 AOB의 넓이의 2배이다.'],
    'answer_choice': 4,
    'distractor_why': ['중심각이 같으면 호의 길이도 같아요. 옳아요',
                       '중심각이 같으면 현의 길이도 같아요. 옳아요',
                       '∠AOD = 120°로 ∠AOB의 3배이고 호는 중심각에 정비례해요. 옳아요',
                       '∠AOC = 80°로 2배이고 부채꼴의 넓이는 중심각에 정비례해요. 옳아요'],
    'answer_print': '현 AD는 현 AB의 3배가 아니다',
    'hint': '호의 길이와 부채꼴의 넓이는 중심각에 정비례하지만, <b>현의 길이는 정비례하지 않아요</b>.',
    'solution': '① ∠AOD = %d° × 3 = %d°예요.<br>'
                '② 호 AD는 호 AB의 3배, 부채꼴 넓이도 중심각에 정비례해요.<br>'
                '③ 현 AD는 현 AB, 현 BC, 현 CD 세 개를 이은 꺾은선보다 짧아요(두 점을 잇는 가장 짧은 선은 선분). '
                '그래서 현 AD는 현 AB의 3배보다 작아요. 옳지 않은 것은 ④예요.' % (TH7, 3 * TH7),
}

# ═════════════════════════════════════════ 8. 부채꼴의 넓이
R8, TH8 = 8, 135
S8 = R8 * R8 * TH8 / 360                    # π 계수
P8 = {
    'id': 'm1-08', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '부채꼴의 넓이',
    'stem_print': '다음 그림과 같은 부채꼴의 넓이는?',
    'figure': F.fig_sector(R8, TH8, fill='p', r_label=F.cm(R8), theta_label=F.deg(TH8), width=190, height=160),
    'choices': ['3π cm²', '6π cm²', num(S8) + 'π cm²', '48π cm²', '64π cm²'], 'answer_choice': 3,
    'distractor_why': ['πr² 대신 πr를 써서 8π × 3/8 = 3π로 계산함',
                       '호의 길이 2π × 8 × 135/360 = 6π를 구함',
                       '360 대신 180으로 나눠 64π × 135/180 = 48π로 계산함',
                       '중심각을 빠뜨리고 원 전체의 넓이를 구함'],
    'answer_print': num(S8) + PI + ' cm²',
    'hint': '부채꼴의 넓이 = πr² × (중심각)/360이에요. 135/360 = 3/8로 약분하면 편해요.',
    'solution': '① 반지름 %d cm, 중심각 %d°를 그림에서 읽어요.<br>'
                '② 넓이 = π × %d² × %d/360 = 64π × 3/8 = %sπ (cm²)<br>'
                '자주 하는 실수: 호의 길이(2πr × x/360)와 넓이(πr² × x/360) 공식을 섞어 쓰지 않아요.'
                % (R8, TH8, R8, TH8, num(S8)),
}

# ═════════════════════════════════════════ 9. 육각뿔의 구성 요소
N9 = 6
E9, F9, V9 = 2 * N9, N9 + 1, N9 + 1
V9_, F9_ = F.pyramid(F.reg_base(N9, 2.4, 15), 3.6)
P9 = {
    'id': 'm1-09', 'unit': 7, 'points': 3, 'format': 'choice5', 'level': 'L',
    'topic': '다면체의 구성 요소',
    'stem_print': '다음 그림과 같은 입체도형의 모서리의 개수를 <i>a</i>, 면의 개수를 <i>b</i>라 할 때, '
                  '<i>a</i> + <i>b</i>의 값은?',
    'figure': F.fig_polyhedron(V9_, F9_, view=F.View(tilt=18, yaw=0), fill='y', width=190, height=170),
    'choices': ['13', '16', '18', str(E9 + F9), '26'], 'answer_choice': 4,
    'distractor_why': ['모서리를 옆모서리 6개만 셈 (6 + 7)',
                       '밑면을 오각형으로 잘못 세어 오각뿔로 봄 (10 + 6)',
                       '면을 옆면 6개만 세고 밑면을 빠뜨림 (12 + 6)',
                       '육각기둥으로 봄 (모서리 18 + 면 8)'],
    'answer_print': str(E9 + F9),
    'hint': '먼저 이름을 붙여요. 밑면이 육각형이고 옆면이 모두 삼각형이면 육각뿔이에요.',
    'solution': '① 그림은 밑면이 육각형인 <b>육각뿔</b>이에요.<br>'
                '② 모서리: 밑면 6 + 옆모서리 6 = %d → <i>a</i> = %d<br>'
                '③ 면: 밑면 1 + 옆면 6 = %d → <i>b</i> = %d<br>'
                '④ <i>a</i> + <i>b</i> = %d' % (E9, E9, F9, F9, E9 + F9),
}

# ═════════════════════════════════════════ 10. 정팔면체
F10, V10, E10 = 8, 6, 12
OV, OF = F.octahedron(3.4)
P10 = {
    'id': 'm1-10', 'unit': 7, 'points': 3, 'format': 'choice5', 'level': 'L',
    'topic': '정팔면체',
    'stem_print': '다음 그림의 정팔면체에 대한 설명으로 옳은 것은?',
    'figure': F.fig_polyhedron(OV, OF, view=F.View(tilt=15, yaw=20), fill='c', width=170, height=180),
    'choices': ['면의 모양은 정사각형이다.',
                '한 꼭짓점에 모인 면의 개수는 3이다.',
                '꼭짓점의 개수는 8이다.',
                '모서리의 개수는 %d이다.' % E10,
                '면의 개수는 6이다.'],
    'answer_choice': 4,
    'distractor_why': ['정팔면체의 면은 정삼각형이에요 (정사각형은 정육면체)',
                       '정팔면체는 한 꼭짓점에 면이 4개 모여요',
                       '꼭짓점은 6개예요 (8개는 정육면체의 꼭짓점 수)',
                       '면은 8개예요 (6개는 정육면체의 면의 수)'],
    'answer_print': '모서리의 개수는 12',
    'hint': '그림에서 위쪽 꼭짓점 하나에 모인 면을 세고, 위아래 사각뿔 두 개가 붙은 모양으로 보면 세기 쉬워요.',
    'solution': '① 면: 위 사각뿔의 옆면 4 + 아래 4 = %d (모두 정삼각형)<br>'
                '② 꼭짓점: 위 1 + 가운데 4 + 아래 1 = %d<br>'
                '③ 모서리: 가운데 4 + 위로 4 + 아래로 4 = %d, 한 꼭짓점에 모인 면은 4개<br>'
                '정육면체(면 6, 꼭짓점 8, 모서리 12)와 면·꼭짓점 수가 서로 바뀐 것에 주의해요.' % (F10, V10, E10),
}

# ═════════════════════════════════════════ 11. 직각삼각형 회전 → 원뿔, 단면
R11, H11 = 3, 5
P11 = {
    'id': 'm1-11', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'L',
    'topic': '회전체와 단면',
    'stem_print': '다음 그림의 직각삼각형을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체에 대한 '
                  '설명으로 옳지 <b>않은</b> 것은?',
    'figure': F.fig_rotation([(0, 0), (R11, 0), (0, H11)],
                             labels=[((R11 / 2, 0), F.cm(R11), (0, -10)), ((0, H11 / 2), F.cm(H11), (-20, 0))],
                             right=[((0, 0), 0, 90)], fill='g', width=150, height=190),
    'choices': ['회전체는 원뿔이다.',
                '밑면인 원의 반지름의 길이는 %d cm이다.' % R11,
                '회전축에 수직인 평면으로 자른 단면은 원이다.',
                '회전축에 수직인 평면으로 자른 단면은 모두 합동이다.',
                '회전축을 포함하는 평면으로 자른 단면은 이등변삼각형이다.'],
    'answer_choice': 4,
    'distractor_why': ['직각을 낀 한 변을 축으로 직각삼각형을 돌리면 원뿔이에요. 옳아요',
                       '축에서 가장 먼 거리인 밑변 3 cm가 밑면의 반지름이에요. 옳아요',
                       '회전체를 회전축에 수직으로 자르면 단면은 항상 원이에요. 옳아요',
                       '처음 삼각형과 거울상이 붙어 두 변이 같은 삼각형이 돼요. 옳아요'],
    'answer_print': '수직 단면은 모두 합동이 아니다',
    'hint': '원뿔을 위쪽에서 자를 때와 아래쪽에서 자를 때 단면인 원의 크기를 비교해요.',
    'solution': '① 회전체는 밑면의 반지름 %d cm, 높이 %d cm인 원뿔이에요.<br>'
                '② 회전축에 수직인 평면으로 자르면 단면은 원이지만, 꼭짓점에 가까울수록 원이 작아져요. '
                '그래서 모두 합동은 아니에요.<br>'
                '③ 원기둥은 수직 단면이 모두 합동이지만 원뿔은 아니에요. 옳지 않은 것은 ④예요.' % (R11, H11),
}

# ═════════════════════════════════════════ 12. 삼각기둥 전개도 → 겉넓이
A12, B12, C12, H12 = 3, 4, 5, 7            # 직각을 낀 두 변 3, 4, 빗변 5
BASE12 = A12 * B12 / 2
LAT12 = (A12 + B12 + C12) * H12
S12 = 2 * BASE12 + LAT12
P12 = {
    'id': 'm1-12', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '각기둥의 전개도·겉넓이',
    'stem_print': '다음 그림과 같은 전개도로 만들어지는 삼각기둥의 겉넓이는?',
    'figure': fig_prism_net(A12, B12, C12, H12),
    'choices': ['42 cm²', '84 cm²', '90 cm²', num(S12) + ' cm²', '108 cm²'], 'answer_choice': 4,
    'distractor_why': ['밑넓이 6 × 높이 7로 부피를 구함',
                       '옆넓이 (3 + 4 + 5) × 7만 구하고 밑넓이를 빠뜨림',
                       '밑면을 한 개만 더함 (84 + 6)',
                       '직각삼각형의 넓이를 3 × 4 = 12로 2로 나누지 않음 (84 + 24)'],
    'answer_print': num(S12) + ' cm²',
    'hint': '전개도에서 밑면(자홍색 직각삼각형) 2개와 옆면(직사각형 3개를 이은 큰 직사각형)을 나눠 구해요.',
    'solution': '① 밑면: 직각을 낀 두 변이 %d cm, %d cm인 직각삼각형 → %d × %d ÷ 2 = %s, 2개 → %s<br>'
                '② 옆면: 가로 %d + %d + %d = %d, 세로 %d인 직사각형 → %d<br>'
                '③ 겉넓이 = %s + %d = %s (cm²)'
                % (A12, B12, A12, B12, num(BASE12), num(2 * BASE12), A12, B12, C12, A12 + B12 + C12, H12,
                   LAT12, num(2 * BASE12), LAT12, num(S12)),
}

# ═════════════════════════════════════════ 13. 사다리꼴 기둥의 부피
B13, T13, H13, D13 = 6, 3, 4, 5
BA13 = (B13 + T13) * H13 / 2
V13 = BA13 * D13
TV, TF = trap_prism(B13, T13, H13, D13)
_hx = (B13 + T13) / 2


def _extra13(c, pj):
    c.line(pj((_hx, 0, 0)), pj((_hx, H13, 0)), dash='3 2', sw=1.0)
    c.right_mark(pj((_hx, 0, 0)), 180, 90, k=6)


P13 = {
    'id': 'm1-13', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '각기둥의 부피',
    'stem_print': '다음 그림은 밑면이 사다리꼴인 사각기둥이다. 이 사각기둥의 부피는?',
    'figure': F.fig_polyhedron(TV, TF, view=F.View(tilt=20, yaw=20), fill='m',
                               labels=[((B13 / 2, 0, 0), F.cm(B13), (0, -11)),
                                       ((B13 / 2, H13, 0), F.cm(T13), (0, -10)),
                                       ((_hx, H13 / 2, 0), F.cm(H13), (-16, 0)),
                                       ((0, 0, D13 / 2), F.cm(D13), (-16, -10))],
                               extra=_extra13, width=220, height=190),
    'choices': ['30 cm³', '60 cm³', num(V13) + ' cm³', '120 cm³', '180 cm³'], 'answer_choice': 3,
    'distractor_why': ['기둥을 뿔로 착각해 1/3을 곱함 (90 ÷ 3)',
                       '밑넓이를 윗변 × 높이 = 3 × 4 = 12로 구함',
                       '밑넓이를 아랫변 × 높이 = 6 × 4 = 24로 구함',
                       '사다리꼴 넓이에서 2로 나누지 않음 (36 × 5)'],
    'answer_print': num(V13) + ' cm³',
    'hint': '기둥의 부피 = 밑넓이 × 높이예요. 이 기둥의 밑면은 앞쪽의 사다리꼴이고, 기둥의 높이는 깊이 5 cm예요.',
    'solution': '① 밑넓이(사다리꼴) = (%d + %d) × %d ÷ 2 = %s (cm²)<br>'
                '② 기둥의 높이는 두 밑면 사이의 거리 %d cm예요.<br>'
                '③ 부피 = %s × %d = %s (cm³)<br>'
                '자주 하는 실수: 사다리꼴의 높이 %d cm를 기둥의 높이로 쓰지 않아요.'
                % (T13, B13, H13, num(BA13), D13, num(BA13), D13, num(V13), H13),
}

# ═════════════════════════════════════════ 14. 원뿔의 겉넓이
R14, H14, L14 = 5, 12, 13
S14 = R14 * R14 + R14 * L14                  # π 계수
P14 = {
    'id': 'm1-14', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '원뿔의 겉넓이',
    'stem_print': '다음 그림과 같은 원뿔의 겉넓이는?',
    'figure': fig_cyl_cone(R14, 0, H14, F.cm(R14), hk_label=F.cm(H14), l_label=F.cm(L14), fills=('o',),
                           width=180, height=220),
    'choices': ['65π cm²', '85π cm²', num(S14) + 'π cm²', '115π cm²', '155π cm²'], 'answer_choice': 3,
    'distractor_why': ['옆넓이 π × 5 × 13 = 65π만 구하고 밑넓이를 빠뜨림',
                       '옆넓이에 모선 13 대신 높이 12를 써서 60π + 25π로 계산함',
                       '원기둥처럼 밑면을 2개 더함 (65π + 50π)',
                       '옆넓이를 2πrl = 130π로 구함 (130π + 25π)'],
    'answer_print': num(S14) + PI + ' cm²',
    'hint': '원뿔의 겉넓이 = 밑넓이 πr² + 옆넓이 πrl이에요. 옆넓이에는 높이가 아니라 <b>모선의 길이</b>를 써요.',
    'solution': '① 밑넓이 = π × %d² = %dπ<br>'
                '② 옆넓이 = π × %d × %d = %dπ (r = %d, 모선 l = %d)<br>'
                '③ 겉넓이 = %dπ + %dπ = %dπ (cm²)<br>'
                '높이 %d cm는 부피를 구할 때 써요.'
                % (R14, R14 * R14, R14, L14, R14 * L14, R14, L14, R14 * R14, R14 * L14, S14, H14),
}

# ═════════════════════════════════════════ 15. 반구의 겉넓이
R15 = 6
S15 = 2 * R15 * R15 + R15 * R15              # 곡면 2πr² + 밑면 πr²
P15 = {
    'id': 'm1-15', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M',
    'topic': '반구의 겉넓이',
    'stem_print': '다음 그림은 반지름의 길이가 %d cm인 구를 반으로 자른 반구이다. 이 반구의 겉넓이는?' % R15,
    'figure': F.fig_round([{'t': 'hemi_down', 'r': R15}], labels=[('r', 1, F.cm(R15))], fill=['y'],
                          width=190, height=130),
    'choices': ['36π cm²', '72π cm²', num(S15) + 'π cm²', '144π cm²', '180π cm²'], 'answer_choice': 3,
    'distractor_why': ['평평한 원 πr² = 36π만 구함',
                       '곡면 4πr² ÷ 2 = 72π만 구하고 잘린 원을 빠뜨림',
                       '구 전체의 겉넓이 4πr²를 구함',
                       '구 전체의 겉넓이 144π에 잘린 원 36π를 더함'],
    'answer_print': num(S15) + PI + ' cm²',
    'hint': '반구의 겉면은 <b>구 겉넓이의 절반인 곡면</b>과 <b>잘린 면인 원</b> 두 부분이에요.',
    'solution': '① 곡면 = 4π × %d² ÷ 2 = %dπ<br>'
                '② 잘린 면(원) = π × %d² = %dπ<br>'
                '③ 겉넓이 = %dπ + %dπ = %dπ (cm²)'
                % (R15, 2 * R15 * R15, R15, R15 * R15, 2 * R15 * R15, R15 * R15, S15),
}

# ═════════════════════════════════════════ 16. 색칠한 부분의 둘레 (단답)
R16 = 8
ARC_Q16 = 2 * R16 / 4                        # 사분원 호: 2πr/4 의 π 계수
ARC_S16 = (R16 / 2)                          # 지름 r 반원 호: π(r/2) 의 π 계수
PER16_PI, PER16_N = ARC_Q16 + ARC_S16, R16
P16 = {
    'id': 'm1-16', 'unit': 6, 'points': 4, 'format': 'short', 'level': 'M',
    'topic': '색칠한 부분의 둘레',
    'stem_print': '다음 그림은 반지름의 길이가 %d cm인 사분원 OAB에서 선분 OA를 지름으로 하는 반원을 '
                  '잘라 낸 것이다. 색칠한 부분의 둘레의 길이를 구하시오.' % R16,
    'figure': fig_quarter_minus_semi(R16, fill='m'),
    'answer_print': '(%sπ + %d)' % (num(PER16_PI), PER16_N), 'answer_unit': 'cm',
    'answer_format': '(○π + △) 꼴',
    'hint': '색칠한 부분의 둘레를 손가락으로 따라가 봐요. 큰 호, 작은 반원의 호, 선분 OB 세 부분이에요.',
    'solution': '① 사분원의 호 AB = 2π × %d × 1/4 = %sπ<br>'
                '② 반원의 호(지름 %d cm, 반지름 %s cm) = 2π × %s × 1/2 = %sπ<br>'
                '③ 선분 OB = %d<br>'
                '④ 둘레 = %sπ + %sπ + %d = (%sπ + %d) cm<br>'
                '자주 하는 실수: 선분 OA는 색칠한 부분의 둘레가 아니에요(반원이 닿는 지름일 뿐). 더하면 (8π + 16)이 돼요.'
                % (R16, num(ARC_Q16), R16, num(R16 / 2), num(R16 / 2), num(ARC_S16), R16,
                   num(ARC_Q16), num(ARC_S16), R16, num(PER16_PI), PER16_N),
}

# ═════════════════════════════════════════ 17. 원뿔 전개도의 중심각 (단답)
R17, H17, L17 = 4, 3, 5
TH17 = 360 * R17 // L17
P17 = {
    'id': 'm1-17', 'unit': 7, 'points': 4, 'format': 'short', 'level': 'M',
    'topic': '원뿔 전개도의 중심각',
    'stem_print': '다음 그림의 직각삼각형을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 '
                  '전개도에서, 옆면인 부채꼴의 중심각의 크기를 구하시오.',
    'figure': F.fig_rotation([(0, 0), (R17, 0), (0, H17)],
                             labels=[((R17 / 2, 0), F.cm(R17), (0, -10)), ((0, H17 / 2), F.cm(H17), (-20, 0)),
                                     ((R17 / 2, H17 / 2), F.cm(L17), (14, 8))],
                             right=[((0, 0), 0, 90)], fill='c', width=170, height=160),
    'figure_sol': F.fig_net_cone(L17, TH17, R17, l_label=F.cm(L17), theta_label=F.deg(TH17),
                                 r_label=F.cm(R17), width=170, height=230),
    'answer_print': str(TH17), 'answer_unit': '°',
    'answer_format': '수',
    'hint': '회전체는 원뿔이에요. 부채꼴의 반지름은 모선 %d cm, 호의 길이는 밑면의 둘레와 같아요.' % L17,
    'solution': '① 회전체는 밑면의 반지름 %d cm, 모선 %d cm인 원뿔이에요(높이 %d cm는 쓰지 않아요).<br>'
                '② 부채꼴의 호의 길이 = 밑면의 둘레 = 2π × %d = %dπ<br>'
                '③ 2π × %d × <i>x</i>/360 = %dπ → <i>x</i>/360 = %d/%d → <i>x</i> = %d<br>'
                '자주 하는 실수: 모선 대신 높이 %d cm를 부채꼴의 반지름으로 쓰면 480°가 나와요.'
                % (R17, L17, H17, R17, 2 * R17, L17, 2 * R17, R17, L17, TH17, H17),
}

# ═════════════════════════════════════════ 18. 원기둥 + 원뿔 부피 (단답)
R18, HC18, HK18 = 3, 5, 4
V18 = R18 * R18 * HC18 + R18 * R18 * HK18 / 3
P18 = {
    'id': 'm1-18', 'unit': 7, 'points': 4, 'format': 'short', 'level': 'L',
    'topic': '붙인 입체의 부피',
    'stem_print': '다음 그림은 원기둥 위에 원뿔을 붙여 만든 입체도형이다. 이 입체도형의 부피를 구하시오.',
    'figure': fig_cyl_cone(R18, HC18, HK18, F.cm(R18), hc_label=F.cm(HC18), hk_label=F.cm(HK18),
                           fills=('g', 'p'), width=180, height=230),
    'answer_print': num(V18) + PI, 'answer_unit': 'cm³',
    'answer_format': '○π 꼴',
    'hint': '원기둥의 부피(πr²h)와 원뿔의 부피(1/3 × πr²h)를 따로 구해 더해요. 밑면의 반지름은 같아요.',
    'solution': '① 원기둥: π × %d² × %d = %dπ<br>'
                '② 원뿔: 1/3 × π × %d² × %d = %sπ<br>'
                '③ 부피 = %dπ + %sπ = %sπ (cm³)<br>'
                '자주 하는 실수: 원뿔에 1/3을 곱하는 것을 잊으면 81π가 돼요.'
                % (R18, HC18, R18 * R18 * HC18, R18, HK18, num(R18 * R18 * HK18 / 3), R18 * R18 * HC18,
                   num(R18 * R18 * HK18 / 3), num(V18)),
}

# ═════════════════════════════════════════ 19. 정다각형 (서술, 글)
D19 = 5
N19 = next(n for n in range(3, 20) if n * (n - 3) // 2 == D19 and n * (n - 3) % 2 == 0)
SUM19 = 180 * (N19 - 2)
IN19, EX19 = SUM19 // N19, 360 // N19
P19 = {
    'id': 'm1-19', 'unit': 6, 'points': 8, 'format': 'essay', 'level': 'M',
    'topic': '정다각형의 내각·외각',
    'stem_print': '대각선의 총 개수가 %d인 정다각형이 있다. 이 정다각형의 한 내각의 크기와 한 외각의 크기를 '
                  '각각 구하시오.' % D19,
    'figure': None,
    'answer_print': '한 내각 %d°, 한 외각 %d°' % (IN19, EX19), 'answer_unit': None,
    'hint': '먼저 n(n − 3) ÷ 2 = %d을 만족하는 n을 찾아 몇 각형인지 정해요.' % D19,
    'solution': '① n(n − 3) ÷ 2 = %d → n(n − 3) = %d → n = %d, 정오각형이에요.<br>'
                '② 내각의 크기의 합 = 180° × (%d − 2) = %d°<br>'
                '③ 한 내각 = %d° ÷ %d = %d°<br>'
                '④ 한 외각 = 360° ÷ %d = %d° (또는 180° − %d° = %d°)'
                % (D19, 2 * D19, N19, N19, SUM19, SUM19, N19, IN19, N19, EX19, IN19, EX19),
    'rubric': [{'step': 'n(n − 3) ÷ 2 = 5에서 n = 5, 정오각형임을 구함', 'points': 2},
               {'step': '내각의 크기의 합 540°를 구함', 'points': 2},
               {'step': '한 내각 108°를 구함', 'points': 2},
               {'step': '한 외각 72°를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 20. 정사각형 − 사분원 (서술)
A20 = 8
AREA20_N, AREA20_PI = A20 * A20, A20 * A20 / 4
PER20_N, PER20_PI = 2 * A20, 2 * A20 / 4
P20 = {
    'id': 'm1-20', 'unit': 6, 'points': 8, 'format': 'essay', 'level': 'M',
    'topic': '색칠한 부분의 넓이·둘레',
    'stem_print': '다음 그림은 한 변의 길이가 %d cm인 정사각형에서 한 꼭짓점을 중심으로 하는 사분원을 '
                  '잘라 낸 것이다. 색칠한 부분의 넓이와 둘레의 길이를 각각 구하시오.' % A20,
    'figure': F.fig_square_quarter(A20, 'outside', fill='y', width=160, height=160),
    'answer_print': '넓이 (%d − %sπ) cm², 둘레 (%sπ + %d) cm' % (AREA20_N, num(AREA20_PI), num(PER20_PI), PER20_N),
    'answer_unit': None,
    'hint': '넓이는 정사각형 − 사분원, 둘레는 <b>정사각형의 두 변 + 사분원의 호</b>예요.',
    'solution': '① 정사각형의 넓이 = %d × %d = %d<br>'
                '② 사분원의 넓이 = π × %d² × 1/4 = %sπ<br>'
                '③ 색칠한 부분의 넓이 = (%d − %sπ) cm²<br>'
                '④ 둘레: 색칠한 부분을 따라가면 정사각형의 두 변 %d + %d = %d와 사분원의 호 2π × %d × 1/4 = %sπ<br>'
                '⑤ 둘레 = (%sπ + %d) cm<br>'
                '자주 하는 실수: 둘레에 정사각형의 네 변을 모두 넣지 않아요. 사분원의 반지름인 두 변은 둘레가 아니에요.'
                % (A20, A20, AREA20_N, A20, num(AREA20_PI), AREA20_N, num(AREA20_PI), A20, A20, PER20_N,
                   A20, num(PER20_PI), num(PER20_PI), PER20_N),
    'rubric': [{'step': '정사각형의 넓이 64와 사분원의 넓이 16π를 구함', 'points': 2},
               {'step': '색칠한 부분의 넓이 (64 − 16π) cm²를 구함', 'points': 2},
               {'step': '둘레가 두 변 16과 사분원의 호 4π로 이루어짐을 알고 각각 구함', 'points': 2},
               {'step': '둘레 (4π + 16) cm를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 21. 회전체의 부피 (서술): 직사각형 + 사분원 → 원기둥 + 반구
R21, H21 = 3, 4
CYL21 = R21 * R21 * H21                       # π 계수
HEM21 = 2 * R21 ** 3 / 3                      # (4/3)πr³ ÷ 2 의 π 계수
V21 = CYL21 + HEM21
_shape21 = [(0, 0), (R21, 0)] + [(R21 * math.cos(math.radians(a)), H21 + R21 * math.sin(math.radians(a)))
                                 for a in range(0, 91, 3)]
P21 = {
    'id': 'm1-21', 'unit': 7, 'points': 8, 'format': 'essay', 'level': 'M',
    'topic': '회전체의 부피',
    'stem_print': '다음 그림은 직사각형 위에 반지름의 길이가 %d cm인 사분원을 붙인 도형이다. 이 도형을 직선 '
                  '<i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 구하시오.' % R21,
    'figure': F.fig_rotation(_shape21, labels=[((R21 / 2, 0), F.cm(R21), (0, -10)),
                                               ((R21, H21 / 2), F.cm(H21), (18, 0))],
                             right=[((0, 0), 0, 90)], fill='o', width=160, height=200),
    'figure_sol': F.fig_round([{'t': 'cyl', 'r': R21, 'h': H21}, {'t': 'hemi', 'r': R21}],
                              labels=[('r', 1, F.cm(R21)), ('hs', 0, F.cm(H21))], fill=['o', 'm'],
                              width=170, height=200),
    'answer_print': '%sπ cm³' % num(V21), 'answer_unit': None,
    'hint': '직사각형은 원기둥이 되고, 사분원은 반구가 돼요. 두 부피를 더해요.',
    'solution': '① 회전체는 밑면의 반지름 %d cm, 높이 %d cm인 원기둥 위에 반지름 %d cm인 반구를 붙인 모양이에요.<br>'
                '② 원기둥의 부피 = π × %d² × %d = %dπ<br>'
                '③ 반구의 부피 = 4/3 × π × %d³ × 1/2 = %sπ<br>'
                '④ 부피 = %dπ + %sπ = %sπ (cm³)<br>'
                '자주 하는 실수: 반구를 구 전체(36π)로 계산하지 않아요.'
                % (R21, H21, R21, R21, H21, CYL21, R21, num(HEM21), CYL21, num(HEM21), num(V21)),
    'rubric': [{'step': '회전체가 원기둥과 반구를 붙인 모양임을 앎', 'points': 2},
               {'step': '원기둥의 부피 36π를 구함', 'points': 2},
               {'step': '반구의 부피 18π를 구함', 'points': 2},
               {'step': '부피 54π cm³를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 22. 직육면체 + 정육면체 겉넓이 (서술)
W22, D22, H22, A22 = 6, 4, 3, 2
BOX22 = 2 * (W22 * D22 + W22 * H22 + D22 * H22)
SIDE22 = 4 * A22 * A22
S22 = BOX22 + SIDE22
P22 = {
    'id': 'm1-22', 'unit': 7, 'points': 8, 'format': 'essay', 'level': 'M',
    'topic': '붙인 입체의 겉넓이',
    'stem_print': '다음 그림은 직육면체의 윗면 위에 한 모서리의 길이가 %d cm인 정육면체를 올려 붙인 입체도형이다. '
                  '이 입체도형의 겉넓이를 구하시오.' % A22,
    'figure': fig_box_cube(W22, D22, H22, A22, 2, 1),
    'answer_print': '%d cm²' % S22, 'answer_unit': None,
    'hint': '정육면체가 직육면체 윗면의 일부를 가리지만, 정육면체의 윗면이 그만큼을 다시 채워요.',
    'solution': '① 직육면체의 겉넓이 = 2 × (%d × %d + %d × %d + %d × %d) = %d<br>'
                '② 붙은 면: 직육면체 윗면에서 가려진 %d × %d = %d과 정육면체의 아랫면 %d은 드러나지 않아요. '
                '대신 정육면체의 윗면 %d이 위에서 보이므로, 위에서 보이는 넓이는 직육면체 윗면 %d 그대로예요.<br>'
                '③ 그래서 정육면체는 옆면 4개만 더해요: 4 × %d × %d = %d<br>'
                '④ 겉넓이 = %d + %d = %d (cm²)<br>'
                '자주 하는 실수: 정육면체의 겉넓이 24를 통째로 더하면 132가 돼요.'
                % (W22, D22, W22, H22, D22, H22, BOX22, A22, A22, A22 * A22, A22 * A22, A22 * A22,
                   W22 * D22, A22, A22, SIDE22, BOX22, SIDE22, S22),
    'rubric': [{'step': '직육면체의 겉넓이 108을 구함', 'points': 2},
               {'step': '붙은 면(가려진 윗면 4와 정육면체 아랫면 4)이 드러나지 않음을 설명함', 'points': 2},
               {'step': '정육면체의 옆넓이 16을 더해야 함을 알고 구함', 'points': 2},
               {'step': '겉넓이 124 cm²를 구함', 'points': 2}],
}

PROBLEMS = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22]


def check():
    """모든 정답을 문항을 만든 같은 변수에서 다시 계산한다."""
    def ans(p):
        return p['choices'][p['answer_choice'] - 1]

    # 1
    n = N1_FROM + 3
    assert n == 6 and n * (n - 3) / 2 == 9 and ans(P1) == '9'
    # 2: 그림의 실제 각과 라벨 수치
    ia = F.interior_angles(T2)
    assert all(abs(a - b) < 1e-6 for a, b in zip(ia, [A2, X2, C2]))
    assert E2 == A2 + X2 == 115 and ans(P2) == '70°'
    # 3
    ia = F.interior_angles(H3)
    assert all(abs(a - b) < 1e-6 for a, b in zip(ia, INT3))
    assert 720 - (INT3[0] + INT3[1] + INT3[3] + (180 - E3) + INT3[5]) == X3 == 140 and ans(P3) == '140°'
    assert 720 - (INT3[0] + INT3[1] + INT3[3] + E3 + INT3[5]) == 160      # 함정 ⑤
    # 4
    ia = F.interior_angles(Q4)
    assert all(abs(a - b) < 1e-6 for a, b in zip(ia, INT4))
    assert sum(INT4) == 540 and 360 - (EXT4[0] + EXT4[1] + EXT4[3] + EXT4[4]) == X4 == 60 and ans(P4) == '60°'
    # 5
    assert N5 == 6 and ans(P5) == '정육각형'
    assert (180 * (N5 - 2) / N5) / (360 / N5) == K5
    # 6
    assert TH6 / L6 == X6 / M6 and X6 == 90 and ans(P6) == '90'
    assert (_pts6['D'] - _pts6['C']) % 360 == X6 and _pts6['B'] - _pts6['A'] == TH6
    # 7: 현은 정비례하지 않음
    ch = lambda t: 2 * math.sin(math.radians(t / 2))  # noqa: E731
    assert ch(3 * TH7) < 3 * ch(TH7) - 0.1
    # 8
    assert abs(math.pi * R8 ** 2 * TH8 / 360 - 24 * math.pi) < 1e-9 and ans(P8) == '24π cm²'
    assert abs(2 * math.pi * R8 * TH8 / 360 - 6 * math.pi) < 1e-9
    # 9: 그림의 입체에서 직접 센다
    edges = {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in F9_ for k in range(len(f))}
    assert len(edges) == E9 == 12 and len(F9_) == F9 == 7 and len(V9_) == V9 == 7 and ans(P9) == '19'
    # 10
    edges = {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in OF for k in range(len(f))}
    assert len(OF) == F10 and len(OV) == V10 and len(edges) == E10 and P10['answer_choice'] == 4
    assert all(len(f) == 3 for f in OF)
    assert sum(1 for f in OF if 4 in f) == 4                               # 한 꼭짓점에 면 4개
    # 11
    assert P11['answer_choice'] == 4
    # 12
    assert A12 ** 2 + B12 ** 2 == C12 ** 2
    assert 2 * (A12 * B12 / 2) + (A12 + B12 + C12) * H12 == S12 == 96 and ans(P12) == '96 cm²'
    # 13: 그림의 사다리꼴 치수
    assert abs(TV[1][0] - TV[0][0] - B13) < 1e-9 and abs(TV[2][0] - TV[3][0] - T13) < 1e-9
    assert abs(TV[2][1] - H13) < 1e-9 and abs(TV[4][2] - D13) < 1e-9
    assert (B13 + T13) * H13 / 2 * D13 == V13 == 90 and ans(P13) == '90 cm³'
    # 14
    assert R14 ** 2 + H14 ** 2 == L14 ** 2
    assert abs(math.pi * R14 ** 2 + math.pi * R14 * L14 - 90 * math.pi) < 1e-9 and ans(P14) == '90π cm²'
    # 15
    assert abs(4 * math.pi * R15 ** 2 / 2 + math.pi * R15 ** 2 - 108 * math.pi) < 1e-9 and ans(P15) == '108π cm²'
    # 16
    per = 2 * math.pi * R16 / 4 + math.pi * R16 / 2 + R16
    assert abs(per - (8 * math.pi + 8)) < 1e-9 and P16['answer_print'] == '(8π + 8)'
    # 17
    assert R17 ** 2 + H17 ** 2 == L17 ** 2
    assert abs(2 * math.pi * L17 * TH17 / 360 - 2 * math.pi * R17) < 1e-9 and TH17 == 288
    assert P17['answer_print'] == '288'
    # 18
    v = math.pi * R18 ** 2 * HC18 + math.pi * R18 ** 2 * HK18 / 3
    assert abs(v - 57 * math.pi) < 1e-9 and P18['answer_print'] == '57π'
    # 19
    assert N19 == 5 and N19 * (N19 - 3) / 2 == D19 and IN19 == 108 and EX19 == 72 and IN19 + EX19 == 180
    # 20
    area = A20 ** 2 - math.pi * A20 ** 2 / 4
    per = 2 * A20 + 2 * math.pi * A20 / 4
    assert abs(area - (64 - 16 * math.pi)) < 1e-9 and abs(per - (16 + 4 * math.pi)) < 1e-9
    assert P20['answer_print'] == '넓이 (64 − 16π) cm², 둘레 (4π + 16) cm'
    # 21
    v = math.pi * R21 ** 2 * H21 + 4 / 3 * math.pi * R21 ** 3 / 2
    assert abs(v - 54 * math.pi) < 1e-9 and P21['answer_print'] == '54π cm³'
    assert abs(_shape21[-1][0]) < 1e-9 and abs(_shape21[-1][1] - (H21 + R21)) < 1e-9
    # 22
    surf = 2 * (W22 * D22 + W22 * H22 + D22 * H22) + 6 * A22 ** 2 - 2 * A22 ** 2
    assert surf == S22 == 124 and P22['answer_print'] == '124 cm²'
    assert 2 + A22 <= W22 and 1 + A22 <= D22                               # 정육면체가 윗면 안에 있음
    # 형식
    assert sum(p['points'] for p in PROBLEMS) == 100
    assert sum(1 for p in PROBLEMS if p['level'] == 'L') == 8
    assert [p['id'] for p in PROBLEMS if p['points'] == 3] == ['m1-01', 'm1-05', 'm1-09', 'm1-10']
    assert all(p['level'] == 'L' for p in PROBLEMS if p['points'] == 3)
    assert sum(1 for p in PROBLEMS if not p.get('figure')) <= 6
    for p in PROBLEMS:
        if p['format'] == 'essay':
            assert sum(s['points'] for s in p['rubric']) == p['points'] == 8
    print('check OK: 22문항 정답 재계산 일치')
