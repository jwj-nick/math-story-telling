"""모의고사 2회 — 중1 2학기 기말(교과서 6단원 평면도형의 성질 · 7단원 입체도형의 성질), 실전 표준.

소재: 별 모양의 끝각 · 칠각형/오각형의 외각 · 정육면체 전개도 · 직각사다리꼴 회전(원뿔대) ·
큰 반원 안의 두 반원 · 원기둥 위 반구 · 직육면체에서 작은 직육면체를 잘라 낸 입체.
그림의 라벨 수치와 정답은 같은 변수에서 나오고, check() 가 모든 정답을 다시 계산한다.
"""
import math

import figgen as F

PI = 'π'
X = F.X_ITAL
XI = '<i>x</i>'

META = {'id': 'm1-term2-mock2', 'kind': 'exam', 'title': '모의고사 2회',
        'subtitle': '실전 표준 · 6단원 평면도형의 성질 · 7단원 입체도형의 성질 · 22문항 100점',
        'time_min': 45, 'folder': '모의고사', 'file': '모의고사2회'}


def dg(v):
    return '%d°' % v


def pis(k):
    return ('%dπ' % k) if k != 1 else 'π'


# ═════════════════════════════════════════ 세트 전용 그림
@F.autofit
def fig_two_shaded(R, sectors, r_label, r_dir, fill='p', scale=22, width=190, height=180):
    """원 O 안에 색칠한 부채꼴 여러 개와 반지름 라벨 하나. sectors [(시작각, 끝각, 중심각 라벨)]."""
    c = F.Canvas(scale)
    O = (0, 0)
    for a0, a1, lab in sectors:
        c.poly([O] + c.arc_pts(O, R, a0, a1, n=60), fill=F.FILL[fill])
    c.circle(O, R)
    for a0, a1, lab in sectors:
        c.angle_mark(O, a0, a1, label=lab, size=12)
    p = F._add(O, F._u(r_dir), R)
    c.line(O, p)
    c.seg_label(O, p, r_label, side=1)
    c.dot(O)
    c.text(O, 'O', size=12, d=F._scale(F._u(r_dir + 180), 11))
    return c.svg(width, height)


@F.autofit
def fig_rot_apex(rb, rt, h, apex_h, labels, fill='c', scale=22, width=180, height=220):
    """직선 l 을 축으로 하는 직각사다리꼴 + 빗변을 연장해 축과 만나는 점까지 점선."""
    c = F.Canvas(scale)
    lo, hi = -c.px(20), apex_h + c.px(30)
    c.line((0, lo), (0, hi), sw=1.0, dash='7 3 2 3')
    c.text((0, hi), F.it('l'), size=14, d=(8, 6))
    c.poly([(0, 0), (rb, 0), (rt, h), (0, h)], fill=F._fc(fill))
    c.line((rt, h), (0, apex_h), dash='4 3', sw=1.1)
    c.dot((0, apex_h), r=2.0)
    c.right_mark((0, 0), 0, 90)
    c.right_mark((0, h), 0, -90)
    c.labels(labels)
    cy = hi - c.px(12)
    arc = c.arc_pts((0, cy), c.px(13), 200, 520, n=40, ry=c.px(4))
    c.poly(arc[:-6], sw=1.0, close=False)
    tip = arc[-6]
    c.poly([F._add(tip, (-c.px(4), c.px(2))), tip, F._add(tip, (-c.px(3.5), -c.px(2.5)))], sw=1.0, close=False)
    return c.svg(width, height)


def _pip(q, poly):
    x, y = q
    ins = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                ins = not ins
    return ins


@F.autofit
def fig_solid(faces, view=None, fill='y', labels=(), scale=22, width=230, height=190):
    """볼록이 아닌 다면체도 그리는 겨냥도. faces [(3D 꼭짓점 목록, 바깥 법선)].
    모서리를 잘게 나눠 앞쪽 면에 가려지는 부분만 점선으로 그린다(정사영)."""
    view = view or F.View()
    t = view.t
    vd = (0, -math.sin(t), math.cos(t))
    ct, st = math.cos(t), math.sin(t)

    def dot3(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    front = []
    for pts, nrm in faces:
        nr = view.rot(nrm)
        if dot3(nr, vd) < -1e-9:
            front.append((pts, nr, view.rot(pts[0]), [view.proj(p) for p in pts]))

    def hidden(p3):
        r = view.rot(p3)
        q = view.proj(p3)
        dp = dot3(r, vd)
        for pts, nr, r0, p2 in front:
            if not _pip(q, p2):
                continue
            s = (dot3(nr, r0) - q[0] * nr[0] - q[1] * (nr[1] * ct + nr[2] * st)) / dot3(nr, vd)
            if s < dp - 1e-6:
                return True
        return False

    c = F.Canvas(scale)
    for pts, nr, r0, p2 in front:
        c.poly(p2, fill=F._fc(fill), stroke='none')
    edges = {}
    for pts, nrm in faces:
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            key = tuple(sorted((tuple(round(v, 6) for v in a), tuple(round(v, 6) for v in b))))
            edges[key] = (a, b)
    N = 48
    segs = []
    for a, b in edges.values():
        flags = []
        for k in range(N):
            u = (k + 0.5) / N
            flags.append(hidden(tuple(a[j] + (b[j] - a[j]) * u for j in range(3))))
        k0 = 0
        for k in range(1, N + 1):
            if k == N or flags[k] != flags[k0]:
                p = tuple(a[j] + (b[j] - a[j]) * k0 / N for j in range(3))
                q = tuple(a[j] + (b[j] - a[j]) * k / N for j in range(3))
                segs.append((flags[k0], view.proj(p), view.proj(q)))
                k0 = k
    for hid, p, q in sorted(segs, key=lambda s: not s[0]):
        c.line(p, q, dash='4 3' if hid else None, sw=1.0 if hid else 1.4)
    for lab in labels:
        c.text(view.proj(lab[0]), lab[1], size=12, d=lab[2] if len(lab) > 2 else (0, 0))
    return c.svg(width, height)


def notched_box(W, H, D, a, b, cc):
    """직육면체 [0,W]×[0,H]×[0,D] 의 위·앞·오른쪽 모서리에서 a×b×cc 직육면체를 잘라 낸 입체의 면."""
    x0, y0 = W - a, H - b
    return [
        ([(0, 0, 0), (W, 0, 0), (W, 0, D), (0, 0, D)], (0, -1, 0)),
        ([(0, 0, D), (W, 0, D), (W, H, D), (0, H, D)], (0, 0, 1)),
        ([(0, 0, 0), (0, 0, D), (0, H, D), (0, H, 0)], (-1, 0, 0)),
        ([(0, 0, 0), (W, 0, 0), (W, y0, 0), (x0, y0, 0), (x0, H, 0), (0, H, 0)], (0, 0, -1)),
        ([(W, 0, 0), (W, 0, D), (W, H, D), (W, H, cc), (W, y0, cc), (W, y0, 0)], (1, 0, 0)),
        ([(0, H, 0), (x0, H, 0), (x0, H, cc), (W, H, cc), (W, H, D), (0, H, D)], (0, 1, 0)),
        ([(x0, y0, 0), (W, y0, 0), (W, y0, cc), (x0, y0, cc)], (0, 1, 0)),
        ([(x0, y0, 0), (x0, y0, cc), (x0, H, cc), (x0, H, 0)], (1, 0, 0)),
        ([(x0, y0, cc), (W, y0, cc), (W, H, cc), (x0, H, cc)], (0, 0, -1)),
    ]


def cube_fold(cells):
    """정육면체 전개도 칸 → 각 칸이 접힌 뒤의 물리적 면 번호(굴리기). 마주 보는 면: (0,1)(2,3)(4,5)."""
    rolls = {(1, 0): ('D', 'E', 'U', 'W'), (-1, 0): ('D', 'W', 'U', 'E'),
             (0, 1): ('D', 'N', 'U', 'S'), (0, -1): ('D', 'S', 'U', 'N')}
    start = cells[0]
    seen = {start: {'D': 0, 'U': 1, 'N': 2, 'S': 3, 'E': 4, 'W': 5}}
    stack = [start]
    while stack:
        cur = stack.pop()
        o = seen[cur]
        for (dx, dy), (d, e, u, w) in rolls.items():
            nb = (cur[0] + dx, cur[1] + dy)
            if nb in cells and nb not in seen:
                n = dict(o)
                n[d], n[e], n[u], n[w] = o[e], o[u], o[w], o[d]
                seen[nb] = n
                stack.append(nb)
    face = [seen[cl]['D'] for cl in cells]
    assert sorted(face) == list(range(6)), '정육면체 전개도가 아니다'
    return face


def opposite_cell(cells, i):
    face = cube_fold(cells)
    want = face[i] ^ 1
    return face.index(want)


# ═════════════════════════════════════════ 1. 대각선 (L, 3점)
Q1_FROM = 6
Q1_N = Q1_FROM + 3
Q1_ANS = Q1_N * (Q1_N - 3) // 2
Q1_CH = [6, 14, 20, Q1_ANS, 54]
P1 = {
    'id': 'm2-01', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '대각선의 개수',
    'stem_print': '한 꼭짓점에서 그을 수 있는 대각선의 개수가 %d인 다각형의 대각선의 개수는?' % Q1_FROM,
    'figure': None,
    'choices': [str(v) for v in Q1_CH], 'answer_choice': 4,
    'distractor_why': ['한 꼭짓점에서 그은 대각선의 개수 6을 그대로 답함',
                       '<i>n</i> − 3 대신 <i>n</i> − 1 = 6으로 보고 칠각형(7 × 4 ÷ 2)으로 계산함',
                       '<i>n</i> − 3 대신 <i>n</i> − 2 = 6으로 보고 팔각형(8 × 5 ÷ 2)으로 계산함',
                       '구각형은 맞지만 9 × 6에서 2로 나누지 않음 (대각선을 두 번 셈)'],
    'answer_print': str(Q1_ANS),
    'hint': '한 꼭짓점에서 그을 수 있는 대각선은 <i>n</i> − 3개예요. 먼저 <i>n</i>을 구해요.',
    'solution': '① <i>n</i> − 3 = %d → <i>n</i> = %d, 구각형이에요.<br>'
                '② 대각선의 개수 = %d × (%d − 3) ÷ 2 = %d<br>'
                '÷ 2를 빼먹으면 한 대각선을 양 끝에서 두 번 센 54가 돼요.' % (Q1_FROM, Q1_N, Q1_N, Q1_N, Q1_ANS),
}

# ═════════════════════════════════════════ 2. 별 모양 끝각 (L, 3점)
Q2_TIPS = [38, 42, None, 26, 44]
Q2_X = 180 - sum(v for v in Q2_TIPS if v)
Q2_ALL = [v if v else Q2_X for v in Q2_TIPS]
Q2_LAB = [dg(v) if v else X for v in Q2_TIPS]
Q2_CH = [25, Q2_X, 36, 210, 390]
P2 = {
    'id': 'm2-02', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '별 모양의 끝각',
    'stem_print': '다음 그림과 같은 별 모양에서 ∠' + XI + '의 크기는?',
    'figure': F.fig_star(Q2_ALL, Q2_LAB, fill='g'),
    'choices': [dg(v) for v in Q2_CH], 'answer_choice': 2,
    'distractor_why': ['덧셈 실수: 38 + 42 + 26 + 44 = 150을 다시 확인해요',
                       '다섯 끝각이 모두 같다고 보고 180° ÷ 5 = 36°로 어림함',
                       '다섯 끝각의 합을 외각의 합 360°로 착각함: 360° − 150°',
                       '다섯 끝각의 합을 오각형의 내각의 합 540°로 착각함: 540° − 150°'],
    'answer_print': dg(Q2_X),
    'hint': '별의 다섯 끝각의 합은 <b>180°</b>예요. 삼각형의 한 외각은 이웃하지 않는 두 내각의 합이라는 성질로 '
            '다섯 각이 한 삼각형 안에 모여요.',
    'solution': '① 별의 두 끝각의 합은 가운데 오각형 쪽 삼각형의 외각과 같아서, 다섯 끝각이 한 삼각형의 세 내각으로 '
                '모여요. 그래서 다섯 끝각의 합 = 180°<br>'
                '② 38° + 42° + ∠' + XI + ' + 26° + 44° = 180° → ∠' + XI + ' = 180° − 150° = ' + dg(Q2_X) + '<br>'
                '자주 하는 실수: 끝각의 합을 360°로 기억하는 것. 360°는 외각의 합이에요.',
}

# ═════════════════════════════════════════ 3. 칠각형 내각 (M)
Q3_KNOWN = {0: 130, 1: 125, 3: 140, 4: 135, 6: 120}
Q3_K = 30                                   # 꼭짓점 5 = x + 30°
Q3_X = (180 * 5 - sum(Q3_KNOWN.values()) - Q3_K) // 2
Q3_INT = [Q3_KNOWN.get(i) for i in range(7)]
Q3_INT[2], Q3_INT[5] = Q3_X, Q3_X + Q3_K
Q3_P = F.polygon_by_angles(Q3_INT, [3.2, 3.2, 3.2, 2.4, 2.4])
Q3_LAB = {i: dg(v) for i, v in Q3_KNOWN.items()}
Q3_CH = [95, Q3_X, 125, 140, 155]
P3 = {
    'id': 'm2-03', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '칠각형의 내각',
    'stem_print': '다음 그림과 같은 칠각형에서 ∠' + XI + '의 크기는?',
    'figure': F.fig_polygon(Q3_P, angles=Q3_LAB, unknown={2: X, 5: X + ' + %d°' % Q3_K}, fill='c',
                            width=240, height=210),
    'choices': [dg(v) for v in Q3_CH], 'answer_choice': 2,
    'distractor_why': ['30°를 두 번 빼서 2∠' + XI + ' = 250° − 60°로 계산함',
                       '∠' + XI + ' + 30°의 30°를 빼먹고 2∠' + XI + ' = 250°로 계산함',
                       '∠' + XI + ' + 30°의 크기(140°)를 ∠' + XI + '로 답함',
                       '30°를 빼지 않고 더해서 2∠' + XI + ' = 250° + 60°로 계산함'],
    'answer_print': dg(Q3_X),
    'hint': '칠각형의 내각의 합은 180° × (7 − 2) = 900°예요. ∠' + XI + '가 두 번 들어 있어요.',
    'solution': '① 칠각형의 내각의 합: 180° × 5 = 900°<br>'
                '② 주어진 다섯 각의 합: 130° + 125° + 140° + 135° + 120° = 650°<br>'
                '③ ∠' + XI + ' + (∠' + XI + ' + 30°) = 900° − 650° = 250° → 2∠' + XI + ' = 220° → ∠' + XI
                + ' = ' + dg(Q3_X) + '<br>'
                '자주 하는 실수: ∠' + XI + ' + 30° 자리를 ∠' + XI + '와 따로 세지 않는 것.',
}

# ═════════════════════════════════════════ 4. 외각의 합 (M)
Q4_EXT = [65, 60, None, 80, 70]             # 꼭짓점 4 는 내각으로 보여 준다
Q4_X = 360 - sum(v for v in Q4_EXT if v)
Q4_EXT_ALL = [v if v else Q4_X for v in Q4_EXT]
Q4_INT = [180 - e for e in Q4_EXT_ALL]
Q4_P = F.polygon_by_angles(Q4_INT, [3.4, 3.0, 3.2])
Q4_CH = [45, 75, Q4_X, 95, 115]
P4 = {
    'id': 'm2-04', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '다각형의 외각의 합',
    'stem_print': '다음 그림과 같이 오각형의 변을 연장했을 때, ∠' + XI + '의 크기는?',
    'figure': F.fig_polygon(Q4_P, ext={0: dg(Q4_EXT[0]), 1: dg(Q4_EXT[1]), 2: X, 3: dg(Q4_EXT[3])},
                            angles={4: dg(Q4_INT[4])}, fill='m', width=240, height=210),
    'choices': [dg(v) for v in Q4_CH], 'answer_choice': 3,
    'distractor_why': ['내각 110°를 외각처럼 그대로 더함: 360° − (65° + 60° + 80° + 110°)',
                       '덧셈 실수: 65 + 60 + 80 + 70 = 275를 285로 계산함',
                       '∠' + XI + '가 있는 꼭짓점의 내각(180° − 85°)을 답함',
                       '65°가 있는 꼭짓점의 내각 115°와 헷갈림'],
    'answer_print': dg(Q4_X),
    'hint': '다각형의 외각의 크기의 합은 항상 360°예요. 110°는 <b>내각</b>이니 외각으로 바꿔요.',
    'solution': '① 110°는 내각이므로 그 꼭짓점의 외각은 180° − 110° = 70°<br>'
                '② 외각의 합 360°: 65° + 60° + ∠' + XI + ' + 80° + 70° = 360°<br>'
                '③ ∠' + XI + ' = 360° − 275° = ' + dg(Q4_X) + '<br>'
                '자주 하는 실수: 그림의 각이 내각인지 외각인지 확인하지 않고 모두 더하는 것.',
}

# ═════════════════════════════════════════ 5. 정다각형 (L, 3점)
Q5_EXT = 45
Q5_N = 360 // Q5_EXT
Q5_INT = 180 - Q5_EXT
Q5_CH = [45, 108, 120, Q5_INT, 140]
P5 = {
    'id': 'm2-05', 'unit': 6, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '정다각형의 한 내각',
    'stem_print': '한 외각의 크기가 %d°인 정다각형의 한 내각의 크기는?' % Q5_EXT,
    'figure': None,
    'choices': [dg(v) for v in Q5_CH], 'answer_choice': 4,
    'distractor_why': ['한 외각의 크기를 그대로 답함',
                       '정오각형의 한 내각과 헷갈림',
                       '정육각형의 한 내각과 헷갈림',
                       '정구각형의 한 내각과 헷갈림 (360 ÷ 45를 9로 계산)'],
    'answer_print': dg(Q5_INT),
    'hint': '한 내각 + 한 외각 = 180°예요. 정다각형의 이름을 구하지 않아도 돼요.',
    'solution': '① 한 꼭짓점에서 내각과 외각의 합은 180°이므로 한 내각 = 180° − 45° = 135°<br>'
                '② 확인: 360° ÷ 45° = 8이므로 정팔각형, 한 내각 = 180° × 6 ÷ 8 = 135°<br>'
                '자주 하는 실수: 외각 45°를 그대로 답하는 것.',
}

# ═════════════════════════════════════════ 6. 중심각과 호 (M)
Q6_A, Q6_LAB, Q6_L2 = 40, 6, 15
Q6_X = Q6_A * Q6_L2 // Q6_LAB
Q6_PTS = {'A': 140, 'B': 140 + Q6_A, 'C': 250, 'D': 250 + Q6_X}
Q6_CH = [16, 49, 80, Q6_X, 120]
P6 = {
    'id': 'm2-06', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '중심각과 호의 길이',
    'stem_print': '다음 그림의 원 O에서 ∠' + XI + '의 크기는?',
    'figure': F.fig_circle_parts(3.2, Q6_PTS, radii='ABCD',
                                 angles=[('A', 'B', dg(Q6_A)), ('C', 'D', X)],
                                 arc_labels=[('A', 'B', '%dcm' % Q6_LAB), ('C', 'D', '%dcm' % Q6_L2)],
                                 shade=[('C', 'D', 'g')]),
    'choices': [dg(v) for v in Q6_CH], 'answer_choice': 4,
    'distractor_why': ['비를 거꾸로 세움: 40° × 6 ÷ 15',
                       '호의 길이의 차 9를 중심각에 더함: 40° + 9°',
                       '15 ÷ 6 = 2.5를 2로 어림함',
                       '15 ÷ 6 = 2.5를 3으로 어림함'],
    'answer_print': dg(Q6_X),
    'hint': '한 원에서 호의 길이는 중심각의 크기에 정비례해요.',
    'solution': '① 40° : ∠' + XI + ' = 6 : 15<br>'
                '② ∠' + XI + ' = 40° × 15 ÷ 6 = ' + dg(Q6_X) + '<br>'
                '자주 하는 실수: 호의 길이가 9cm 늘었다고 각도 9° 늘린다고 생각하는 것(더하기가 아니라 곱하기 관계).',
}

# ═════════════════════════════════════════ 7. 부채꼴의 성질 (M)
Q7_PTS = {'A': 175, 'B': 220, 'C': 265, 'D': 355}
Q7_ANG = {k: (Q7_PTS[b] - Q7_PTS[a]) for k, (a, b) in {'AB': ('A', 'B'), 'BC': ('B', 'C'), 'CD': ('C', 'D')}.items()}
P7 = {
    'id': 'm2-07', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '부채꼴의 성질',
    'stem_print': '다음 그림의 원 O에서 ∠AOB = ∠BOC = %d°, ∠COD = %d°일 때, 다음 중 옳지 <b>않은</b> 것은?'
                  % (Q7_ANG['AB'], Q7_ANG['CD']),
    'figure': F.fig_circle_parts(3.2, Q7_PTS, radii='ABCD', chords=[('A', 'B'), ('B', 'C'), ('C', 'D')],
                                 angles=[('A', 'B', dg(Q7_ANG['AB'])), ('B', 'C', dg(Q7_ANG['BC'])),
                                         ('C', 'D', dg(Q7_ANG['CD']))]),
    'choices': ['△COD의 넓이는 △AOB의 넓이의 2배이다.',
                '(호 AC의 길이) = 2 × (호 AB의 길이)',
                '현 AB와 현 BC의 길이는 같다.',
                '호 CD의 길이는 호 AC의 길이와 같다.',
                '부채꼴 COD의 넓이는 부채꼴 AOB의 넓이의 2배이다.'],
    'answer_choice': 1,
    'distractor_why': ['∠AOC = 70°는 ∠AOB의 2배이고 호의 길이는 중심각에 정비례하므로 옳음',
                       '같은 크기의 중심각에 대한 현의 길이는 같으므로 옳음',
                       '∠COD = ∠AOC = 70°이므로 두 호의 길이가 같아 옳음',
                       '부채꼴의 넓이는 중심각에 정비례하므로 옳음'],
    'answer_print': '△COD의 넓이는 △AOB의 2배가 아니다',
    'hint': '중심각에 정비례하는 것은 <b>호의 길이와 부채꼴의 넓이</b>뿐이에요. 현의 길이와 삼각형의 넓이는 아니에요.',
    'solution': '① 중심각이 2배이면 호의 길이와 부채꼴의 넓이는 2배예요. ②·④·⑤는 옳아요.<br>'
                '② 같은 크기의 중심각에 대한 현의 길이는 같아요. ③은 옳아요.<br>'
                '③ 삼각형 COD는 부채꼴 COD에서 활꼴(현 CD와 호 CD 사이)을 뺀 것이에요. 중심각이 2배일 때 '
                '삼각형의 넓이는 2배보다 작아요. 따라서 옳지 않은 것은 ①이에요.<br>'
                '자주 하는 실수: 현과 삼각형도 중심각에 정비례한다고 생각하는 것.',
}

# ═════════════════════════════════════════ 8. 부채꼴의 넓이 (M)
Q8_R, Q8_T = 6, 150
Q8_L = Q8_R * Q8_T // 180                   # 호의 길이 = 5π
Q8_S = Q8_R * Q8_L // 2                     # 넓이 = 15π
Q8_CH = [Q8_L, Q8_R ** 2 // 4, Q8_S, Q8_R ** 2 // 2, Q8_R * Q8_L]
P8 = {
    'id': 'm2-08', 'unit': 6, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '부채꼴의 넓이',
    'stem_print': '다음 그림과 같이 반지름의 길이가 %dcm, 호의 길이가 %s cm인 부채꼴의 넓이는?' % (Q8_R, pis(Q8_L)),
    'figure': F.fig_sector(Q8_R, Q8_T, fill='p', r_label='%dcm' % Q8_R, arc_label=pis(Q8_L) + 'cm'),
    'choices': [pis(v) + ' cm²' for v in Q8_CH], 'answer_choice': 3,
    'distractor_why': ['호의 길이를 넓이로 답함',
                       '중심각을 90°로 어림해 원의 넓이 %dπ의 1/4로 계산함' % Q8_R ** 2,
                       '반원으로 어림해 %dπ의 1/2로 계산함' % Q8_R ** 2,
                       '(반지름) × (호의 길이)에서 2로 나누지 않음'],
    'answer_print': pis(Q8_S) + ' cm²',
    'hint': '중심각을 몰라도 S = (1/2) × r × l 로 넓이를 구할 수 있어요.',
    'solution': '① 부채꼴의 넓이 S = (1/2) × (반지름) × (호의 길이)<br>'
                '② S = (1/2) × %d × %s = %s cm²<br>'
                '③ 확인: 중심각은 %d°이고 π × %d² × %d/360 = %s예요.<br>'
                '자주 하는 실수: 그림 모양만 보고 반원·사분원으로 어림하는 것.'
                % (Q8_R, pis(Q8_L), pis(Q8_S), Q8_T, Q8_R, Q8_T, pis(Q8_S)),
}

# ═════════════════════════════════════════ 9. 육각뿔 (L, 3점)
Q9_N = 8
Q9_E, Q9_V = 2 * Q9_N, Q9_N + 1
Q9_CH = [Q9_N + Q9_V, Q9_V + Q9_V, Q9_E + Q9_N, Q9_E + Q9_V, 3 * Q9_N + 2 * Q9_N]
P9 = {
    'id': 'm2-09', 'unit': 7, 'points': 3, 'format': 'choice5', 'level': 'L', 'topic': '각뿔의 모서리·꼭짓점',
    'stem_print': '다음 그림과 같은 입체도형의 모서리의 개수와 꼭짓점의 개수의 합은?',
    'figure': F.fig_polyhedron(*F.pyramid(F.reg_base(Q9_N, 2.6, 0), 4.0), fill='o', view=F.View(tilt=20, yaw=15),
                               width=180, height=170),
    'choices': [str(v) for v in Q9_CH], 'answer_choice': 4,
    'distractor_why': ['모서리를 옆모서리 8개만 셈: 8 + 9',
                       '모서리 대신 면의 개수 9를 더함: 9 + 9',
                       '꼭짓점을 밑면의 8개만 셈: 16 + 8',
                       '팔각기둥(모서리 24, 꼭짓점 16)으로 잘못 봄'],
    'answer_print': str(Q9_E + Q9_V),
    'hint': '먼저 입체의 이름을 붙여요. 밑면이 팔각형 하나이고 옆면이 삼각형이면 <b>팔각뿔</b>이에요.',
    'solution': '① 그림은 팔각뿔이에요.<br>'
                '② 모서리: 밑면 8 + 옆모서리 8 = 16, 꼭짓점: 밑면 8 + 꼭대기 1 = 9<br>'
                '③ 16 + 9 = 25<br>'
                '자주 하는 실수: 그림의 점선(숨은 모서리)을 빼고 세는 것.',
}

# ═════════════════════════════════════════ 10. 정육면체 전개도 (M)
Q10_CELLS = [(1, 2), (0, 1), (1, 1), (2, 1), (2, 0), (3, 0)]
Q10_LET = 'CBDEAF'
Q10_ASK = Q10_LET.index('C')
Q10_OPP = Q10_LET[opposite_cell(Q10_CELLS, Q10_ASK)]
Q10_CH = ['A', 'B', 'D', 'E', 'F']
P10 = {
    'id': 'm2-10', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '정육면체의 전개도',
    'stem_print': '다음 그림의 전개도로 정육면체를 만들 때, 면 C와 마주 보는 면은?',
    'figure': F.fig_net(*F.cube_net(Q10_CELLS, a=1.0, letters=Q10_LET), width=200, height=160),
    'choices': ['면 ' + s for s in Q10_CH], 'answer_choice': Q10_CH.index(Q10_OPP) + 1,
    'distractor_why': ['면 B는 접으면 면 C의 옆면이 됨 (모서리를 하나 나눠 가짐)',
                       '면 D는 전개도에서 면 C와 바로 붙어 있는 면',
                       '면 E는 면 B와 마주 보는 면 (B–D–E가 한 줄)',
                       '면 F는 면 D와 마주 보는 면'],
    'answer_print': '면 ' + Q10_OPP,
    'hint': '한 줄로 이어진 세 면에서 <b>양 끝 면</b>이 서로 마주 봐요. 줄을 바꿔 가며 찾아요.',
    'solution': '① 면 D를 바닥에 놓고 접으면 B와 E는 왼쪽·오른쪽 벽이 되어 서로 마주 봐요.<br>'
                '② 면 C는 D의 위쪽 변에 붙어 있어 뒤쪽 벽이 되고, 면 A는 E의 아래쪽 변에 붙어 있어 '
                'E를 세우면 앞쪽 벽이 돼요. 그래서 C와 A가 마주 봐요.<br>'
                '③ 남은 F는 A에 붙어 뚜껑이 되어 바닥 D와 마주 봐요.<br>'
                '자주 하는 실수: 전개도에서 멀리 떨어진 면을 마주 보는 면이라고 짐작하는 것.',
}

# ═════════════════════════════════════════ 11. 회전체의 단면 (M) — 보기가 그림
_ch_w, _ch_h = 84, 118
Q11_SHAPES = [
    ([(0, 0), (2.4, 0), (0, 3.2)], '이등변삼각형(원뿔)', 'c'),
    ([(0, 0), (2.2, 0), (2.2, 3.0), (0, 3.0)], '직사각형(원기둥)', 'c'),
    ([(1.6 * math.cos(math.radians(a)), 1.6 + 1.6 * math.sin(math.radians(a))) for a in range(-90, 91, 6)],
     '원(구)', 'c'),
    ([(0, 0)] + [(2.6 * math.cos(math.radians(a)), 2.6 * math.sin(math.radians(a))) for a in range(0, 91, 6)],
     '반원(반구)', 'c'),
    ([(0, 0), (2.8, 0), (1.4, 3.0), (0, 3.0)], '등변사다리꼴(원뿔대)', 'c'),
]
P11 = {
    'id': 'm2-11', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '회전체의 단면',
    'stem_print': '다음 평면도형을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체를 '
                  '<b>회전축을 포함하는 평면</b>으로 자르면 단면이 등변사다리꼴이 되는 것은?',
    'figure': None,
    'choices': ['<span class="fig-ch">' + F.fig_rotation(s, fill=col, width=_ch_w, height=_ch_h) + '</span>'
                for s, _, col in Q11_SHAPES],
    'answer_choice': 5,
    'distractor_why': ['회전체는 원뿔, 단면은 이등변삼각형',
                       '회전체는 원기둥, 단면은 직사각형',
                       '회전체는 구, 단면은 원',
                       '회전체는 반구, 단면은 반원'],
    'answer_print': '직각사다리꼴(원뿔대)',
    'hint': '회전축을 포함하는 평면으로 자른 단면은 <b>처음 도형과 그 거울상(축에 대해 뒤집은 도형)</b>을 붙인 모양이에요.',
    'solution': '각 도형을 직선 <i>l</i>에 대해 뒤집어 붙여 봐요.<br>'
                '① 직각삼각형 → 이등변삼각형 ② 직사각형 → 직사각형 ③ 반원 → 원 ④ 사분원 → 반원<br>'
                '⑤ 직각사다리꼴 → 등변사다리꼴 (회전체는 원뿔대)<br>'
                '자주 하는 실수: 회전축에 <b>수직인</b> 평면으로 자른 단면(항상 원)과 헷갈리는 것.',
}

# ═════════════════════════════════════════ 12. 삼각기둥의 겉넓이 (M)
Q12_A, Q12_B, Q12_C, Q12_H = 8, 6, 10, 5
Q12_BASE = Q12_A * Q12_B // 2
Q12_SIDE = (Q12_A + Q12_B + Q12_C) * Q12_H
Q12_ANS = 2 * Q12_BASE + Q12_SIDE
Q12_P2 = (Q12_A + Q12_B) * Q12_H            # 빗변을 뺀 옆넓이
Q12_CH = [Q12_P2 + Q12_BASE, Q12_P2 + 2 * Q12_BASE, Q12_SIDE, Q12_SIDE + Q12_BASE, Q12_ANS]
_v12 = F.prism([(0, 0), (Q12_A, 0), (0, Q12_B)], Q12_H)
P12 = {
    'id': 'm2-12', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '각기둥의 겉넓이',
    'stem_print': '다음 그림과 같이 밑면이 직각삼각형인 삼각기둥의 겉넓이는?',
    'figure': F.fig_polyhedron(*_v12, fill='c', view=F.View(tilt=22, yaw=30),
                               labels=[((Q12_A / 2, 0, 0), '%dcm' % Q12_A, (0, -11)),
                                       ((0, 0, Q12_B / 2), '%dcm' % Q12_B, (-18, -4)),
                                       ((Q12_A / 2, Q12_H, Q12_B / 2), '%dcm' % Q12_C, (12, 8)),
                                       ((Q12_A, Q12_H / 2, 0), '%dcm' % Q12_H, (18, 0))],
                               width=170, height=210),
    'choices': ['%d cm²' % v for v in Q12_CH], 'answer_choice': 5,
    'distractor_why': ['빗변 10cm를 빼고 둘레를 14로 보고, 밑면도 1개만 더함: 70 + 24',
                       '빗변 10cm를 빼고 둘레를 14로 봄: 70 + 48',
                       '옆넓이만 구함: (8 + 6 + 10) × 5',
                       '밑면을 1개만 더함: 120 + 24'],
    'answer_print': '%d cm²' % Q12_ANS,
    'hint': '겉넓이 = (밑넓이) × 2 + (옆넓이)예요. 옆넓이는 (밑면의 둘레) × (높이)예요.',
    'solution': '① 밑넓이 = 8 × 6 ÷ 2 = 24 cm²<br>'
                '② 옆넓이 = (8 + 6 + 10) × 5 = 120 cm²<br>'
                '③ 겉넓이 = 24 × 2 + 120 = %d cm²<br>'
                '자주 하는 실수: 밑면을 두 개 넣지 않거나, 둘레에서 빗변을 빼먹는 것.' % Q12_ANS,
}

# ═════════════════════════════════════════ 13. 원기둥 전개도 → 부피 (M)
Q13_R, Q13_H = 4, 5
Q13_W = 2 * Q13_R                           # 가로 = 8π
Q13_V = Q13_R ** 2 * Q13_H                  # 80π
Q13_CH = [16, 20, 40, 72, Q13_V]
P13 = {
    'id': 'm2-13', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '원기둥의 부피',
    'stem_print': '다음 그림과 같은 전개도로 만들어지는 원기둥의 부피는?',
    'figure': F.fig_net_cylinder(Q13_R, Q13_H, h_label='%dcm' % Q13_H, w_label=pis(Q13_W) + 'cm',
                                 width=220, height=200),
    'choices': [pis(v) + ' cm³' for v in Q13_CH], 'answer_choice': 5,
    'distractor_why': ['밑넓이 16π만 구하고 높이를 곱하지 않음',
                       '8π를 지름의 원주로 보고 반지름을 2로 계산함: π × 2² × 5',
                       '옆면 직사각형의 넓이(8π × 5)를 부피로 답함',
                       '겉넓이를 구함: 16π × 2 + 40π'],
    'answer_print': pis(Q13_V) + ' cm³',
    'hint': '옆면 직사각형의 가로는 밑면인 원의 둘레와 같아요. 2π × (반지름) = 8π',
    'solution': '① 2π × r = 8π → r = 4 cm<br>'
                '② 밑넓이 = π × 4² = 16π cm²<br>'
                '③ 부피 = 16π × 5 = %s cm³<br>'
                '자주 하는 실수: 가로 8π를 보고 반지름을 바로 8로 읽는 것.' % pis(Q13_V),
}

# ═════════════════════════════════════════ 14. 정사각뿔의 겉넓이 (M)
Q14_A, Q14_SL = 8, 6
Q14_H3 = math.sqrt(Q14_SL ** 2 - (Q14_A / 2) ** 2)   # 그림용 실제 높이(학생에게는 주지 않음)
Q14_ANS = Q14_A ** 2 + 4 * (Q14_A * Q14_SL // 2)
Q14_CH = [88, 96, Q14_ANS, 224, 256]
_v14 = F.pyramid(F.rect_base(Q14_A, Q14_A), Q14_H3)


def _q14_extra(c, proj):
    apex = proj((Q14_A / 2, Q14_H3, Q14_A / 2))
    mid = proj((Q14_A / 2, 0, 0))
    c.line(apex, mid, dash='3 2', sw=1.1, stroke=F.ACCENT2)
    c.right_mark(mid, F._dir(mid, apex), F._dir(mid, proj((Q14_A, 0, 0))), k=6)


P14 = {
    'id': 'm2-14', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'M', 'topic': '각뿔의 겉넓이',
    'stem_print': '다음 그림과 같이 밑면은 한 변의 길이가 %dcm인 정사각형이고 옆면은 모두 합동인 이등변삼각형인 '
                  '사각뿔이 있다. 옆면인 삼각형의 높이가 %dcm일 때, 이 사각뿔의 겉넓이는?' % (Q14_A, Q14_SL),
    'figure': F.fig_polyhedron(*_v14, fill='m', view=F.View(tilt=28, yaw=28), extra=_q14_extra,
                               labels=[((Q14_A * 0.72, 0, 0), '%dcm' % Q14_A, (0, -11)),
                                       ((Q14_A / 2, Q14_H3 / 2, Q14_A / 4), '%dcm' % Q14_SL, (16, 0))],
                               width=200, height=180),
    'choices': ['%d cm²' % v for v in Q14_CH], 'answer_choice': 3,
    'distractor_why': ['옆면을 1개만 더함: 64 + 24',
                       '옆넓이만 구함: 24 × 4',
                       '기둥처럼 밑면을 2개 더함: 64 × 2 + 96',
                       '삼각형의 넓이에서 2로 나누지 않음: 64 + 48 × 4'],
    'answer_print': '%d cm²' % Q14_ANS,
    'hint': '각뿔의 겉넓이 = (밑넓이) + (옆넓이)예요. 각뿔은 밑면이 <b>하나</b>예요.',
    'solution': '① 밑넓이 = 8 × 8 = 64 cm²<br>'
                '② 옆면 하나 = 8 × 6 ÷ 2 = 24 cm², 옆넓이 = 24 × 4 = 96 cm²<br>'
                '③ 겉넓이 = 64 + 96 = %d cm²<br>'
                '자주 하는 실수: 옆면 삼각형의 높이 6cm를 사각뿔의 높이로 착각하는 것.' % Q14_ANS,
}

# ═════════════════════════════════════════ 15. 반구의 겉넓이 (L)
Q15_R = 4
Q15_ANS = 2 * Q15_R ** 2 + Q15_R ** 2       # 곡면 32π + 원 16π
Q15_CH = [2 * Q15_R ** 2, Q15_ANS, 4 * Q15_R ** 2, 5 * Q15_R ** 2, 2 * Q15_R ** 2 + (2 * Q15_R) ** 2]
P15 = {
    'id': 'm2-15', 'unit': 7, 'points': 4, 'format': 'choice5', 'level': 'L', 'topic': '반구의 겉넓이',
    'stem_print': '다음 그림과 같이 반지름의 길이가 %dcm인 반구의 겉넓이는?' % Q15_R,
    'figure': F.fig_round([{'t': 'hemi_down', 'r': Q15_R}], labels=[('r', 1, '%dcm' % Q15_R)], fill=['g'],
                          width=180, height=120),
    'choices': [pis(v) + ' cm²' for v in Q15_CH], 'answer_choice': 2,
    'distractor_why': ['둥근 곡면만 구하고 평평한 원을 빠뜨림',
                       '구 전체의 겉넓이 4π × 4²를 답함',
                       '구 전체의 겉넓이에 원까지 더함',
                       '원의 넓이를 지름 8로 계산함: 32π + 64π'],
    'answer_print': pis(Q15_ANS) + ' cm²',
    'hint': '반구의 겉면은 <b>곡면(구 겉넓이의 절반)</b>과 <b>평평한 원</b> 두 부분이에요.',
    'solution': '① 곡면 = 4π × 4² ÷ 2 = 32π cm²<br>'
                '② 원 = π × 4² = 16π cm²<br>'
                '③ 겉넓이 = 32π + 16π = %s cm²<br>'
                '자주 하는 실수: 잘린 면(원)을 빠뜨리는 것.' % pis(Q15_ANS),
}

# ═════════════════════════════════════════ 16. 색칠한 두 부채꼴 (단답, L)
Q16_R = 6
Q16_SECT = [(20, 70), (200, 270)]
Q16_ANG = [b - a for a, b in Q16_SECT]
Q16_ANS = Q16_R ** 2 * sum(Q16_ANG) // 360  # 12π
P16 = {
    'id': 'm2-16', 'unit': 6, 'points': 4, 'format': 'short', 'level': 'L', 'topic': '색칠한 부채꼴의 넓이',
    'stem_print': '다음 그림의 원 O에서 색칠한 두 부채꼴의 넓이의 합을 구하시오.',
    'figure': fig_two_shaded(Q16_R, [(a, b, dg(b - a)) for a, b in Q16_SECT], '%dcm' % Q16_R, 135, fill='p'),
    'answer_print': pis(Q16_ANS), 'answer_unit': 'cm²', 'answer_format': '○π 꼴',
    'hint': '두 부채꼴의 반지름이 같으니, 중심각을 더해 한 부채꼴처럼 계산해요.',
    'solution': '① 두 중심각의 합 = 50° + 70° = 120°<br>'
                '② 넓이 = π × 6² × 120/360 = 36π × 1/3 = %s cm²<br>'
                '자주 하는 실수: 반지름 대신 지름 12를 넣는 것.' % pis(Q16_ANS),
}

# ═════════════════════════════════════════ 17. 원뿔대의 단면 둘레 (단답, M)
Q17_RT, Q17_RB, Q17_H, Q17_SL = 2, 5, 4, 5
Q17_ANS = 2 * Q17_RT + 2 * Q17_RB + 2 * Q17_SL
_q17_shape = [(0, 0), (Q17_RB, 0), (Q17_RT, Q17_H), (0, Q17_H)]
_q17_right = [((0, 0), 0, 90), ((0, Q17_H), 0, -90)]
P17 = {
    'id': 'm2-17', 'unit': 7, 'points': 4, 'format': 'short', 'level': 'M', 'topic': '원뿔대의 단면',
    'stem_print': '다음 그림의 직각사다리꼴을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체를 '
                  '<b>회전축을 포함하는 평면</b>으로 자른 단면의 둘레의 길이를 구하시오.',
    'figure': F.fig_rotation(_q17_shape, fill='o', right=_q17_right,
                             labels=[((Q17_RT / 2, Q17_H), '%dcm' % Q17_RT, (0, 10)),
                                     ((Q17_RB / 2, 0), '%dcm' % Q17_RB, (0, -10)),
                                     ((0, Q17_H / 2), '%dcm' % Q17_H, (-20, 0)),
                                     (((Q17_RT + Q17_RB) / 2, Q17_H / 2), '%dcm' % Q17_SL, (18, 4))],
                             width=180, height=190),
    'figure_sol': F.fig_rotation(_q17_shape, fill='o', right=_q17_right, mirror=True,
                                 labels=[((0, Q17_H), '%dcm' % (2 * Q17_RT), (0, 10)),
                                         ((0, 0), '%dcm' % (2 * Q17_RB), (0, -10)),
                                         (((Q17_RT + Q17_RB) / 2, Q17_H / 2), '%dcm' % Q17_SL, (18, 4)),
                                         ((-(Q17_RT + Q17_RB) / 2, Q17_H / 2), '%dcm' % Q17_SL, (-18, 4))],
                                 width=250, height=190),
    'answer_print': str(Q17_ANS), 'answer_unit': 'cm', 'answer_format': '수',
    'hint': '단면은 처음 사다리꼴과 그 거울상을 붙인 등변사다리꼴이에요. 윗변·아랫변은 2배가 돼요.',
    'solution': '① 회전체는 원뿔대, 단면은 등변사다리꼴이에요.<br>'
                '② 윗변 = 2 × 2 = 4 cm, 아랫변 = 5 × 2 = 10 cm, 두 빗변 = 5 cm씩<br>'
                '③ 둘레 = 4 + 10 + 5 + 5 = %d cm<br>'
                '자주 하는 실수: 회전축 위의 높이 4cm를 둘레에 넣는 것(단면 안쪽 선이라 둘레가 아니에요).' % Q17_ANS,
}

# ═════════════════════════════════════════ 18. 잘라 낸 직육면체의 부피 (단답, M)
Q18_W, Q18_H, Q18_D = 8, 6, 5
Q18_A, Q18_B, Q18_C = 3, 2, 2
Q18_ANS = Q18_W * Q18_H * Q18_D - Q18_A * Q18_B * Q18_C
_v18 = F.View(tilt=24, yaw=-32)
P18 = {
    'id': 'm2-18', 'unit': 7, 'points': 4, 'format': 'short', 'level': 'M', 'topic': '잘라 낸 입체의 부피',
    'stem_print': '다음 그림은 직육면체에서 작은 직육면체를 잘라 낸 입체도형이다. 이 입체도형의 부피를 구하시오.',
    'figure': fig_solid(notched_box(Q18_W, Q18_H, Q18_D, Q18_A, Q18_B, Q18_C), view=_v18, fill='y',
                        labels=[((Q18_W / 2, 0, 0), '%dcm' % Q18_W, (0, -11)),
                                ((0, Q18_H / 2, 0), '%dcm' % Q18_H, (-18, 0)),
                                ((Q18_W, 0, Q18_D / 2), '%dcm' % Q18_D, (16, -8)),
                                ((Q18_W - Q18_A / 2, Q18_H - Q18_B, 0), '%dcm' % Q18_A, (0, -10)),
                                ((Q18_W - Q18_A, Q18_H - Q18_B / 2, 0), '%dcm' % Q18_B, (-14, 0)),
                                ((Q18_W, Q18_H, Q18_C / 2), '%dcm' % Q18_C, (14, 4))],
                        width=240, height=200),
    'answer_print': str(Q18_ANS), 'answer_unit': 'cm³', 'answer_format': '수',
    'hint': '(처음 직육면체의 부피) − (잘라 낸 작은 직육면체의 부피)로 구해요.',
    'solution': '① 처음 직육면체 = 8 × 5 × 6 = 240 cm³<br>'
                '② 잘라 낸 직육면체 = 3 × 2 × 2 = 12 cm³<br>'
                '③ 부피 = 240 − 12 = %d cm³<br>'
                '자주 하는 실수: 잘라 낸 부분의 가로·세로·높이를 그림에서 잘못 짝짓는 것.' % Q18_ANS,
}

# ═════════════════════════════════════════ 19. 정다각형 조건 (서술)
Q19_RI, Q19_RE = 4, 1
Q19_EXT = 180 * Q19_RE // (Q19_RI + Q19_RE)
Q19_N = 360 // Q19_EXT
Q19_ANS = Q19_N * (Q19_N - 3) // 2
P19 = {
    'id': 'm2-19', 'unit': 6, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '정다각형과 대각선',
    'stem_print': '한 내각의 크기와 한 외각의 크기의 비가 %d : %d인 정다각형이 있다. 이 정다각형의 '
                  '대각선의 개수를 구하시오.' % (Q19_RI, Q19_RE),
    'figure': None,
    'answer_print': str(Q19_ANS), 'answer_unit': '개',
    'hint': '한 내각 + 한 외각 = 180°예요. 이것을 4 : 1로 나눠요.',
    'solution': '① 한 외각 = 180° × 1/(4 + 1) = %d°<br>'
                '② 외각의 합은 360°이므로 360° ÷ %d° = %d → 정%s각형<br>'
                '③ 대각선의 개수 = %d × (%d − 3) ÷ 2 = %d<br>'
                '자주 하는 실수: 4 : 1을 내각 : 외각 = 4 : 1이 아니라 360°를 나누는 비로 쓰는 것.'
                % (Q19_EXT, Q19_EXT, Q19_N, '십', Q19_N, Q19_N, Q19_ANS),
    'rubric': [{'step': '한 내각 + 한 외각 = 180°임을 이용해 한 외각 36°를 구함', 'points': 2},
               {'step': '360° ÷ 36° = 10으로 정십각형임을 구함', 'points': 2},
               {'step': '대각선의 개수 공식 n(n − 3) ÷ 2를 바르게 세움', 'points': 2},
               {'step': '대각선의 개수 35를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 20. 큰 반원 안의 두 반원 (서술)
Q20_D1, Q20_D2 = 6, 4
Q20_D = Q20_D1 + Q20_D2
# 넓이·둘레를 π 계수로 (반원 넓이 = π r² / 2, 반원 호 = π r)
Q20_AREA2 = (Q20_D // 2) ** 2 - (Q20_D1 // 2) ** 2 - (Q20_D2 // 2) ** 2   # 넓이의 2배 계수
Q20_AREA = Q20_AREA2 // 2
Q20_PER = Q20_D // 2 + Q20_D1 // 2 + Q20_D2 // 2
P20 = {
    'id': 'm2-20', 'unit': 6, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '반원으로 된 도형',
    'stem_print': '다음 그림은 지름의 길이가 %dcm인 반원 안에 지름의 길이가 각각 %dcm, %dcm인 두 반원을 그린 '
                  '것이다. 색칠한 부분의 넓이와 둘레의 길이를 각각 구하시오.' % (Q20_D, Q20_D1, Q20_D2),
    'figure': F.fig_semicircles(Q20_D1, Q20_D2, fill='m', width=240, height=140),
    'answer_print': '넓이 %s cm², 둘레 %s cm' % (pis(Q20_AREA), pis(Q20_PER)), 'answer_unit': None,
    'hint': '넓이는 (큰 반원) − (두 작은 반원), 둘레는 <b>세 반원의 호</b>를 모두 더해요(곧은 선은 없어요).',
    'solution': '① 큰 반원의 넓이 = π × 5² ÷ 2 = 25π/2<br>'
                '② 두 작은 반원의 넓이 = π × 3² ÷ 2 + π × 2² ÷ 2 = 9π/2 + 4π/2 = 13π/2<br>'
                '③ 넓이 = 25π/2 − 13π/2 = 12π/2 = %s cm²<br>'
                '④ 둘레 = (π × 10 ÷ 2) + (π × 6 ÷ 2) + (π × 4 ÷ 2) = 5π + 3π + 2π = %s cm<br>'
                '자주 하는 실수: 지름 10을 반지름으로 넣는 것, 둘레에 지름(곧은 선)을 더하는 것.'
                % (pis(Q20_AREA), pis(Q20_PER)),
    'rubric': [{'step': '큰 반원의 넓이 25π/2를 구함', 'points': 2},
               {'step': '두 작은 반원의 넓이 9π/2, 2π를 빼서 넓이 6π cm²를 구함', 'points': 2},
               {'step': '세 호의 길이 5π, 3π, 2π를 각각 구함', 'points': 2},
               {'step': '둘레의 길이 10π cm를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 21. 원뿔대의 부피 (서술)
Q21_RB, Q21_RT, Q21_H, Q21_EXT = 6, 3, 4, 4
Q21_HB = Q21_H + Q21_EXT                    # 큰 원뿔의 높이 8
Q21_VB = Q21_RB ** 2 * Q21_HB // 3          # 96π
Q21_VS = Q21_RT ** 2 * Q21_EXT // 3         # 12π
Q21_ANS = Q21_VB - Q21_VS
P21 = {
    'id': 'm2-21', 'unit': 7, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '원뿔대의 부피',
    'stem_print': '다음 그림의 직각사다리꼴을 직선 <i>l</i>을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 '
                  '구하시오. (점선은 사다리꼴의 빗변을 연장한 선이고, 직선 <i>l</i>과 만나는 점까지 그렸다.)',
    'figure': fig_rot_apex(Q21_RB, Q21_RT, Q21_H, Q21_HB, fill='c',
                           labels=[((Q21_RB / 2, 0), '%dcm' % Q21_RB, (0, -10)),
                                   ((Q21_RT / 2, Q21_H), '%dcm' % Q21_RT, (0, 10)),
                                   ((0, Q21_H / 2), '%dcm' % Q21_H, (-20, 0)),
                                   ((0, Q21_H + Q21_EXT / 2), '%dcm' % Q21_EXT, (-20, 0))],
                           width=190, height=230),
    'answer_print': pis(Q21_ANS), 'answer_unit': 'cm³',
    'hint': '원뿔대는 <b>큰 원뿔에서 작은 원뿔을 잘라 낸</b> 입체예요. 두 원뿔의 반지름과 높이를 그림에서 읽어요.',
    'solution': '① 회전체는 원뿔대예요. 큰 원뿔(반지름 6, 높이 4 + 4 = 8)에서 작은 원뿔(반지름 3, 높이 4)을 뺀 것이에요.<br>'
                '② 큰 원뿔 = (1/3) × π × 6² × 8 = %s<br>'
                '③ 작은 원뿔 = (1/3) × π × 3² × 4 = %s<br>'
                '④ 부피 = %s − %s = %s cm³<br>'
                '자주 하는 실수: 큰 원뿔의 높이를 8이 아니라 4로 쓰는 것, 1/3을 빠뜨리는 것.'
                % (pis(Q21_VB), pis(Q21_VS), pis(Q21_VB), pis(Q21_VS), pis(Q21_ANS)),
    'rubric': [{'step': '원뿔대를 큰 원뿔(반지름 6, 높이 8) − 작은 원뿔(반지름 3, 높이 4)로 나타냄', 'points': 2},
               {'step': '큰 원뿔의 부피 96π를 구함', 'points': 2},
               {'step': '작은 원뿔의 부피 12π를 구함', 'points': 2},
               {'step': '원뿔대의 부피 84π cm³를 구함', 'points': 2}],
}

# ═════════════════════════════════════════ 22. 원기둥 위 반구의 겉넓이 (서술)
Q22_R, Q22_H = 3, 6
Q22_BOT = Q22_R ** 2                        # 9π
Q22_SIDE = 2 * Q22_R * Q22_H                # 36π
Q22_DOME = 2 * Q22_R ** 2                   # 18π
Q22_ANS = Q22_BOT + Q22_SIDE + Q22_DOME     # 63π
P22 = {
    'id': 'm2-22', 'unit': 7, 'points': 8, 'format': 'essay', 'level': 'M', 'topic': '붙인 입체의 겉넓이',
    'stem_print': '다음 그림은 원기둥 위에 반구를 붙여 만든 입체도형이다. 이 입체도형의 겉넓이를 구하시오.',
    'figure': F.fig_round([{'t': 'cyl', 'r': Q22_R, 'h': Q22_H}, {'t': 'hemi', 'r': Q22_R}],
                          labels=[('r', 1, '%dcm' % Q22_R), ('hs', 0, '%dcm' % Q22_H)], fill=['p', 'y'],
                          width=170, height=230),
    'answer_print': pis(Q22_ANS), 'answer_unit': 'cm²',
    'hint': '원기둥과 반구가 붙은 원은 겉에 드러나지 않아요. <b>아래 밑면 + 옆면 + 반구의 곡면</b>만 더해요.',
    'solution': '① 아래 밑면 = π × 3² = %s<br>'
                '② 원기둥의 옆면 = (2π × 3) × 6 = %s<br>'
                '③ 반구의 곡면 = 4π × 3² ÷ 2 = %s<br>'
                '④ 겉넓이 = %s + %s + %s = %s cm² (붙은 원은 넣지 않아요)<br>'
                '자주 하는 실수: 원기둥의 윗면 9π를 더하는 것.'
                % (pis(Q22_BOT), pis(Q22_SIDE), pis(Q22_DOME), pis(Q22_BOT), pis(Q22_SIDE), pis(Q22_DOME),
                   pis(Q22_ANS)),
    'rubric': [{'step': '아래 밑면의 넓이 9π를 구함', 'points': 2},
               {'step': '원기둥의 옆넓이 36π를 구함', 'points': 2},
               {'step': '반구의 곡면 18π를 구함', 'points': 2},
               {'step': '붙은 원을 빼고 겉넓이 63π cm²를 구함', 'points': 2}],
}

PROBLEMS = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15,
            P16, P17, P18, P19, P20, P21, P22]


def _chk_choice(p, val):
    assert p['choices'][p['answer_choice'] - 1].startswith(val), (p['id'], val)


def check():
    """모든 정답을 문항을 만든 같은 변수에서 다시 계산한다."""
    # 1
    n = Q1_FROM + 3
    assert n * (n - 3) / 2 == 27 and Q1_CH[P1['answer_choice'] - 1] == 27
    # 2 별: 다섯 끝각의 합 180, 그림에 넣은 각이 정답과 같은 변수
    assert sum(Q2_ALL) == 180 and Q2_X == 30 and Q2_ALL[2] == Q2_X
    _chk_choice(P2, dg(30))
    # 3 칠각형: 그림의 실제 내각이 라벨과 일치하는지
    real = F.interior_angles(Q3_P)
    assert all(abs(real[i] - Q3_INT[i]) < 1e-6 for i in range(7))
    assert all(a < 180 for a in real)
    assert Q3_X + (Q3_X + 30) + 650 == 900 and Q3_X == 110
    _chk_choice(P3, dg(110))
    # 4 외각
    real = F.interior_angles(Q4_P)
    assert all(abs(real[i] - Q4_INT[i]) < 1e-6 for i in range(5))
    assert sum(Q4_EXT_ALL) == 360 and Q4_X == 85 and 180 - Q4_INT[4] == 70
    _chk_choice(P4, dg(85))
    # 5
    assert 360 / 45 == 8 and 180 * 6 / 8 == 135 == Q5_INT
    _chk_choice(P5, dg(135))
    # 6
    assert abs(Q6_X / Q6_A - Q6_L2 / Q6_LAB) < 1e-12 and Q6_X == 100
    assert (Q6_PTS['D'] - Q6_PTS['C']) == Q6_X and Q6_PTS['B'] - Q6_PTS['A'] == Q6_A
    _chk_choice(P6, dg(100))
    # 7: ①만 틀림 — 넓이 비교(반지름 1)
    a, b = Q7_ANG['AB'], Q7_ANG['CD']
    assert Q7_ANG['BC'] == a and b == 2 * a
    tri = lambda t: 0.5 * math.sin(math.radians(t))
    assert abs(tri(b) - 2 * tri(a)) > 0.03          # ① 거짓
    assert b == a + Q7_ANG['BC']                     # ④ 호 CD = 호 AC
    assert P7['answer_choice'] == 1
    # 8
    l = 2 * math.pi * Q8_R * Q8_T / 360
    S = math.pi * Q8_R ** 2 * Q8_T / 360
    assert abs(l - Q8_L * math.pi) < 1e-9 and abs(S - Q8_S * math.pi) < 1e-9 and Q8_S == 15
    assert abs(0.5 * Q8_R * l - S) < 1e-9 and Q8_CH == sorted(Q8_CH)
    _chk_choice(P8, '15π')
    # 9 팔각뿔: 그림의 꼭짓점·면 수에서 다시 셈
    V9, F9 = F.pyramid(F.reg_base(Q9_N, 2.6, 0), 4.0)
    E9 = {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in F9 for k in range(len(f))}
    assert len(E9) + len(V9) == 25 and len(V9) - len(E9) + len(F9) == 2 and Q9_CH == sorted(Q9_CH)
    _chk_choice(P9, '25')
    # 10 전개도: 접어서 마주 보는 면
    face = cube_fold(Q10_CELLS)
    opp = {Q10_LET[i]: Q10_LET[face.index(face[i] ^ 1)] for i in range(6)}
    assert opp['C'] == 'A' and opp['B'] == 'E' and opp['D'] == 'F'
    assert P10['choices'][P10['answer_choice'] - 1] == '면 A'
    # 11 ⑤만 축에 붙은 변이 수직이고 위·아래 변이 축에 수직인 사다리꼴(원뿔대)
    s5 = Q11_SHAPES[4][0]
    assert s5[0][0] == 0 and s5[3][0] == 0 and s5[0][1] == s5[1][1] and s5[2][1] == s5[3][1] and s5[1][0] != s5[2][0]
    assert P11['answer_choice'] == 5
    # 12
    assert Q12_A ** 2 + Q12_B ** 2 == Q12_C ** 2
    assert Q12_ANS == 2 * 24 + 24 * 5 == 168 and Q12_CH == sorted(Q12_CH)
    _chk_choice(P12, '168 ')
    # 13
    assert abs(2 * math.pi * Q13_R - Q13_W * math.pi) < 1e-9
    assert abs(math.pi * Q13_R ** 2 * Q13_H - 80 * math.pi) < 1e-9
    _chk_choice(P13, '80π')
    # 14 그림의 옆면 높이 = 6 (실제 3D 거리)
    apex = (Q14_A / 2, Q14_H3, Q14_A / 2)
    mid = (Q14_A / 2, 0, 0)
    assert abs(math.dist(apex, mid) - Q14_SL) < 1e-9
    assert Q14_ANS == 64 + 4 * 24 == 160
    _chk_choice(P14, '160 ')
    # 15
    assert abs(4 * math.pi * 16 / 2 + math.pi * 16 - 48 * math.pi) < 1e-9 and Q15_CH == sorted(Q15_CH)
    _chk_choice(P15, '48π')
    # 16
    assert sum(Q16_ANG) == 120 and abs(math.pi * 36 * 120 / 360 - 12 * math.pi) < 1e-9 and Q16_ANS == 12
    # 17 그림의 빗변 길이가 라벨 5cm와 맞는지
    assert abs(math.hypot(Q17_RB - Q17_RT, Q17_H) - Q17_SL) < 1e-9
    assert Q17_ANS == 4 + 10 + 5 + 5 == 24
    # 18
    assert Q18_ANS == 240 - 12 == 228
    # 19
    assert Q19_EXT * Q19_RI == (180 - Q19_EXT) * Q19_RE
    assert Q19_N == 10 and Q19_ANS == 35
    # 20
    area = (math.pi * 25 - math.pi * 9 - math.pi * 4) / 2
    per = math.pi * 10 / 2 + math.pi * 6 / 2 + math.pi * 4 / 2
    assert abs(area - Q20_AREA * math.pi) < 1e-9 and abs(per - Q20_PER * math.pi) < 1e-9
    assert Q20_AREA == 6 and Q20_PER == 10
    # 21 연장선이 축과 만나는 높이가 그림의 수치와 맞는지(닮음 확인은 출제자 몫)
    apex_y = Q21_H * Q21_RB / (Q21_RB - Q21_RT)
    assert abs(apex_y - Q21_HB) < 1e-9
    vol = math.pi * 36 * 8 / 3 - math.pi * 9 * 4 / 3
    assert abs(vol - Q21_ANS * math.pi) < 1e-9 and Q21_ANS == 84
    # 22
    surf = math.pi * 9 + 2 * math.pi * 3 * 6 + 4 * math.pi * 9 / 2
    assert abs(surf - Q22_ANS * math.pi) < 1e-9 and Q22_ANS == 63
    # 구성
    assert sum(p['points'] for p in PROBLEMS) == 100
    assert sum(1 for p in PROBLEMS if p['level'] == 'L') == 6
    three = [p for p in PROBLEMS if p['points'] == 3]
    assert len(three) == 4 and all(p['level'] == 'L' and p['format'] == 'choice5' for p in three)
    for p in PROBLEMS:
        if p['format'] == 'essay':
            assert sum(s['points'] for s in p['rubric']) == p['points']
    print('check OK: mock2 22문항 정답 재계산 일치')
