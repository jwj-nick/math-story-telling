"""figgen.py — 도형 문제용 정적 SVG 생성기 (중1 평면도형·입체도형)

원칙
- 그림은 손으로 좌표를 찍지 않고, 문제의 수치(각도·길이)에서 좌표를 계산해 그린다.
  그래서 그림에 적힌 수치와 실제 모양이 맞는다.
- 색은 잉크 소모가 검정·청록(C)·자홍(M)·노랑(Y)에 고르게 가도록 쓴다.
  선·라벨은 남색, 면은 C·M·Y·초록·보라·주황의 연한 색을 돌려 쓴다.
- 크기: 모든 fig_* 함수는 width(최대 가로 px)·height(최대 세로 px) 안에 들어가도록 축척을 자동으로 정한다.
  글자 크기·라벨 간격·선 두께는 축척과 상관없이 일정한 px이다.
- 외부 의존성 없음. 모든 fig_* 함수는 inline SVG 문자열을 돌려준다.

좌표: 도형은 수학 좌표(cm, y 위쪽)로 계산하고, Canvas 가 scale(px/cm)로 SVG(y 아래쪽)로 옮긴다.
라벨 위치를 줄 때는 (점, 문자) 또는 (점, 문자, (dx_px, dy_px)) 로 준다. dy_px 는 위쪽이 +.

저수준 API (세트 파일에서 그림을 직접 조립할 때) — 반드시 @autofit 함수 안에서 Canvas(scale) 를 쓴다.
    @autofit
    def my_fig(..., scale=22, width=200, height=200):
        c = Canvas(scale)
        c.poly(pts, fill=FILL['y']); c.line(p, q, dash='4 3')
        c.angle_at(v, p_from, p_to, '40°')      # v에서 p_from 방향 → p_to 방향(반시계) 각
        c.right_mark(v, d1, d2)                  # 직각 표시(방향은 도)
        c.text(p, '5cm', d=(0, 10))              # p에서 위로 10px
        c.seg_label(p, q, '5cm', side=1)         # 선분 왼쪽(진행 방향 기준) 라벨
        return c.svg(width, height)
"""
import functools
import inspect
import math

# ───────────────────────────── 색 (잉크 균형)
INK = '#1c3266'
LABEL = '#1c3266'
ACCENT = '#c2185b'
ACCENT2 = '#0277bd'
# 면 색은 아주 연하게(잉크 총량 최소). 색칠한 부분을 구별할 정도만 남긴다.
FILL = {
    'y': '#fdf1bd', 'c': '#dcf1fa', 'm': '#fbe0ed',
    'g': '#e2f3d8', 'p': '#ebe3f8', 'o': '#feead6',
}
FILL_ORDER = ['y', 'c', 'm', 'g', 'p', 'o']
FONT = 13
PAD = 12
X_ITAL = '<tspan font-style="italic">x</tspan>'


def it(s):
    return '<tspan font-style="italic">%s</tspan>' % s


def deg(n):
    return '%s°' % n


def cm(n):
    return '%scm' % n


def _u(d):
    r = math.radians(d)
    return (math.cos(r), math.sin(r))


def _add(p, q, k=1.0):
    return (p[0] + k * q[0], p[1] + k * q[1])


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def _ang(v):
    return math.degrees(math.atan2(v[1], v[0])) % 360


def _dir(p, q):
    return _ang(_sub(q, p))


def _mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def _fc(col):
    return FILL.get(col, col) if col else 'none'


# ───────────────────────────── 자동 축척
_STATE = {'mode': None, 'ext': None}


def autofit(fn):
    """한 번 그려 크기를 재고, width·height 안에 들어가는 축척으로 다시 그린다."""
    sig = inspect.signature(fn)

    @functools.wraps(fn)
    def wrap(*a, **kw):
        if _STATE['mode'] is not None:          # 다른 autofit 함수 안에서 불림
            return fn(*a, **kw)
        b = sig.bind_partial(*a, **kw)
        b.apply_defaults()
        W = b.arguments.get('width', 200)
        H = b.arguments.get('height', 220)
        try:
            _STATE['mode'] = 'measure'
            kw1 = dict(b.arguments)
            kw1['scale'] = 22.0
            fn(**kw1)
            gw, gh, tw, th = _STATE['ext']
            s = 22.0 * min(max(W - 2 * PAD - tw, 40) / max(gw, 1e-6), max(H - 2 * PAD - th, 40) / max(gh, 1e-6))
            _STATE['mode'] = 'final'
            kw1['scale'] = s
            return fn(**kw1)
        finally:
            _STATE['mode'] = None
    return wrap


class Canvas:
    def __init__(self, scale=22.0):
        self.s = float(scale)
        self.items = []
        self.gpts = []       # 도형 점(축척에 따라 움직임)
        self.tpts = []       # 글자 점(px 단위 여유 포함)

    def px(self, n):
        """px → cm(도형 단위)."""
        return n / self.s

    def _P(self, p, text=False):
        (self.tpts if text else self.gpts).append(p)
        return (p[0] * self.s, -p[1] * self.s)

    def _fmt(self, p):
        x, y = self._P(p)
        return '%.2f,%.2f' % (x, y)

    @staticmethod
    def _stroke(stroke, sw, dash):
        return ' stroke="%s" stroke-width="%s"%s stroke-linejoin="round" stroke-linecap="round"' % (
            stroke, sw, ' stroke-dasharray="%s"' % dash if dash else '')

    def poly(self, pts, fill='none', stroke=INK, sw=1.4, dash=None, close=True, opacity=None):
        d = ' '.join(self._fmt(p) for p in pts)
        tag = 'polygon' if close else 'polyline'
        op = ' fill-opacity="%s"' % opacity if opacity is not None else ''
        self.items.append('<%s points="%s" fill="%s"%s%s/>' % (tag, d, fill if close else 'none', op,
                                                             self._stroke(stroke, sw, dash)))

    def line(self, p, q, stroke=INK, sw=1.4, dash=None):
        self.poly([p, q], stroke=stroke, sw=sw, dash=dash, close=False)

    def arc_pts(self, c, r, a0, a1, n=48, ry=None):
        ry = r if ry is None else ry
        return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 c[1] + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

    def circle(self, c, r, fill='none', stroke=INK, sw=1.4, dash=None):
        self.poly(self.arc_pts(c, r, 0, 360, n=120)[:-1], fill=fill, stroke=stroke, sw=sw, dash=dash)

    def text(self, p, s, size=FONT, color=LABEL, anchor='middle', weight='normal', d=(0, 0)):
        q = (p[0] + d[0] / self.s, p[1] + d[1] / self.s)
        x, y = self._P(q, text=True)
        hw = 0.32 * size * max(1, len(_plain(s))) / self.s
        hh = 0.6 * size / self.s
        self.tpts += [(q[0] - hw, q[1] - hh), (q[0] + hw, q[1] + hh)]
        self.items.append('<text x="%.2f" y="%.2f" font-size="%s" fill="%s" text-anchor="%s" '
                          'dominant-baseline="central" font-weight="%s" stroke="#fff" stroke-width="3" '
                          'paint-order="stroke" stroke-linejoin="round">%s</text>'
                          % (x, y, size, color, anchor, weight, s))

    def dot(self, p, r=2.2, color=INK):
        x, y = self._P(p)
        self.items.append('<circle cx="%.2f" cy="%.2f" r="%s" fill="%s"/>' % (x, y, r, color))

    def angle_mark(self, v, a_from, a_to, r=12, label=None, color=INK, lr=None, size=FONT, double=False):
        """꼭짓점 v에서 방향 a_from → a_to(반시계) 각. r·lr 은 px."""
        span = (a_to - a_from) % 360
        rr_ = r * (1.35 if span < 35 else 1)
        self.poly(self.arc_pts(v, self.px(rr_), a_from, a_from + span, n=24), stroke=color, sw=1.1, close=False)
        if double:
            self.poly(self.arc_pts(v, self.px(rr_ + 3), a_from, a_from + span, n=24), stroke=color, sw=1.1,
                      close=False)
        if label:
            mid = a_from + span / 2
            if lr is None:
                lr = rr_ + 11 + (10 if span < 35 else 0) + (4 if span < 60 else 0)
            self.text(_add(v, _u(mid), self.px(lr)), label, color=color if color != INK else LABEL, size=size)

    def angle_at(self, v, p_from, p_to, label=None, **kw):
        self.angle_mark(v, _dir(v, p_from), _dir(v, p_to), label=label, **kw)

    def right_mark(self, v, d1, d2, k=7, color=INK):
        k = self.px(k)
        a = _add(v, _u(d1), k)
        c = _add(v, _u(d2), k)
        b = _add(a, _u(d2), k)
        self.poly([a, b, c], stroke=color, sw=1.0, close=False)

    def seg_label(self, p, q, s, side=1, off=10, size=12, color=LABEL):
        d = _u(_dir(p, q) + 90 * side)
        self.text(_add(_mid(p, q), d, self.px(off)), s, size=size, color=color)

    def tick(self, p, q, n=1, k=4, color=INK):
        m = _mid(p, q)
        d = _dir(p, q)
        for i in range(n):
            c0 = _add(m, _u(d), self.px((i - (n - 1) / 2) * 3.5))
            self.line(_add(c0, _u(d + 90), self.px(k)), _add(c0, _u(d - 90), self.px(k)), stroke=color, sw=1.1)

    def labels(self, labels):
        """[(점, 문자) | (점, 문자, (dx_px, dy_px))]"""
        for lab in labels:
            p, s = lab[0], lab[1]
            d = lab[2] if len(lab) > 2 else (0, 0)
            self.text(p, s, size=12, d=d)

    def svg(self, width=None, height=None):
        allp = self.gpts + self.tpts
        xs = [p[0] * self.s for p in allp]
        ys = [-p[1] * self.s for p in allp]
        gx = [p[0] for p in self.gpts]
        gy = [p[1] for p in self.gpts]
        if _STATE['mode'] == 'measure':
            # 도형 범위(축척 따라 변함)와 글자 여유(px 고정)를 나눠 잰다
            gw, gh = (max(gx) - min(gx)) * self.s, (max(gy) - min(gy)) * self.s
            tw, th = (max(xs) - min(xs)) - gw, (max(ys) - min(ys)) - gh
            _STATE['ext'] = (gw, gh, tw, th)
            return ''
        x0, x1 = min(xs) - PAD, max(xs) + PAD
        y0, y1 = min(ys) - PAD, max(ys) + PAD
        w, h = x1 - x0, y1 - y0
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.1f %.1f %.1f %.1f" width="%.0f" height="%.0f" '
                'style="font-family:inherit;max-width:100%%">%s</svg>'
                % (x0, y0, w, h, w, h, ''.join(self.items)))


def _plain(s):
    import re
    return re.sub(r'<[^>]+>', '', s)


# ═════════════════════════════════════════ 평면: 다각형
def polygon_by_angles(interior, lengths_head):
    """내각 목록(반시계)과 앞쪽 변 길이(n-2개)로 닫힌 다각형 꼭짓점을 계산한다.
    마지막 두 변 길이는 닫힘 조건으로 푼다(양수여야 한다). 첫 변은 오른쪽(0°) 방향."""
    n = len(interior)
    assert abs(sum(interior) - 180 * (n - 2)) < 1e-9, '내각의 합이 맞지 않는다'
    assert len(lengths_head) == n - 2
    heads = [0.0]
    for i in range(1, n):
        heads.append(heads[-1] + (180 - interior[i]))
    P = [(0.0, 0.0)]
    for i, L in enumerate(lengths_head):
        P.append(_add(P[-1], _u(heads[i]), L))
    u1, u2 = _u(heads[n - 2]), _u(heads[n - 1])
    rx, ry = -P[-1][0], -P[-1][1]
    det = u1[0] * u2[1] - u1[1] * u2[0]
    a = (rx * u2[1] - ry * u2[0]) / det
    b = (u1[0] * ry - u1[1] * rx) / det
    assert a > 0 and b > 0, '변 길이가 음수: lengths_head를 바꿔야 한다'
    P.append(_add(P[-1], u1, a))
    return P


def interior_angles(P):
    n = len(P)
    return [(_dir(P[i], P[i - 1]) - _dir(P[i], P[(i + 1) % n])) % 360 for i in range(n)]


@autofit
def fig_polygon(P, angles=None, ext=None, ext_next=None, names=None, fill='y', unknown=None,
                extra=None, accent=None, scale=22, width=210, height=200):
    """반시계 꼭짓점 P의 다각형.
    angles {i: 라벨} 내각 · unknown {i: 라벨} 미지 각(크게) · accent {i: 라벨} 해설용 강조 내각
    ext {i: 라벨}      앞 변(P[i-1]→P[i])을 P[i] 너머로 연장한 외각
    ext_next {i: 라벨} 다음 변(P[i+1]→P[i])을 P[i] 너머로 연장한 외각
    names 꼭짓점 이름 · extra callable(c, P) 추가 그림"""
    c = Canvas(scale)
    n = len(P)
    c.poly(P, fill=_fc(fill))
    cen = (sum(p[0] for p in P) / n, sum(p[1] for p in P) / n)
    for i in range(n):
        v, prv, nxt = P[i], P[i - 1], P[(i + 1) % n]
        if ext and i in ext:
            d = _dir(prv, v)
            c.line(v, _add(v, _u(d), c.px(34)))
            c.angle_mark(v, d, _dir(v, nxt), label=ext[i])
        if ext_next and i in ext_next:
            d = _dir(nxt, v)
            c.line(v, _add(v, _u(d), c.px(34)))
            c.angle_mark(v, _dir(v, prv), d, label=ext_next[i])
        if angles and i in angles:
            c.angle_at(v, nxt, prv, label=angles[i])
        if unknown and i in unknown:
            c.angle_at(v, nxt, prv, label=unknown[i], size=15)
        if accent and i in accent:
            c.angle_at(v, nxt, prv, label=accent[i], color=ACCENT, r=9)
        if names:
            c.text(v, names[i], size=12, d=_scale(_u(_dir(cen, v)), 11))
    if extra:
        extra(c, P)
    return c.svg(width, height)


def _scale(v, k):
    return (v[0] * k, v[1] * k)


@autofit
def fig_regular_polygon(n, diag_from=None, all_diag=False, names=None, fill='c', accent_diag=False,
                        scale=22, width=170, height=170):
    """정n각형. diag_from=i 이면 꼭짓점 i에서 그을 수 있는 대각선, all_diag=True 이면 모든 대각선."""
    c = Canvas(scale)
    R = 3.0
    P = [_add((0, 0), _u(90 + 360 * i / n), R) for i in range(n)]
    c.poly(P, fill=_fc(fill))
    if all_diag:
        for i in range(n):
            for j in range(i + 2, n):
                if not (i == 0 and j == n - 1):
                    c.line(P[i], P[j], sw=0.9, stroke=ACCENT2)
    if diag_from is not None:
        for j in range(n):
            if j not in (diag_from, (diag_from + 1) % n, (diag_from - 1) % n):
                c.line(P[diag_from], P[j], sw=1.1, stroke=ACCENT if accent_diag else INK)
    if names:
        for i, nm in enumerate(names):
            c.text(P[i], nm, size=12, d=_scale(_u(90 + 360 * i / n), 11))
    return c.svg(width, height)


@autofit
def fig_regular_turn(n, names=None, fill='c', scale=22, width=190, height=170):
    """정n각형 둘레를 따라 변을 연장하고 한 외각을 표시(외각의 합 설명용)."""
    c = Canvas(scale)
    R = 3.0
    P = [_add((0, 0), _u(-90 - 180 / n + 360 * i / n), R) for i in range(n)]
    c.poly(P, fill=_fc(fill))
    for i in range(n):
        d = _dir(P[i - 1], P[i])
        c.line(P[i], _add(P[i], _u(d), c.px(22)), sw=1.0)
    d = _dir(P[0], P[1])
    c.angle_mark(P[1], d, _dir(P[1], P[2]), label=None)
    return c.svg(width, height)


@autofit
def fig_star(tips, labels, rot=90, fill='g', scale=22, width=200, height=190):
    """오각별. 다섯 끝각 tips(합 180)를 정확히 만족하도록 원 위의 점을 배치한다.
    (원주각: 끝 i의 각 = 점 i+2와 i+3 사이 호의 절반) labels: 끝마다 표시할 문자열(None이면 생략)."""
    assert abs(sum(tips) - 180) < 1e-9
    arcs = [2 * tips[(k - 2) % 5] for k in range(5)]
    angs = [rot]
    for k in range(4):
        angs.append(angs[-1] + arcs[k])
    R = 3.0
    P = [_add((0, 0), _u(a), R) for a in angs]
    S = [P[i] for i in [0, 2, 4, 1, 3]]
    c = Canvas(scale)
    c.poly(S, fill=_fc(fill), opacity=0.8)
    for i in range(5):
        if labels[i]:
            c.angle_at(P[i], P[(i + 2) % 5], P[(i + 3) % 5], label=labels[i], size=12)
    return c.svg(width, height)


# ═════════════════════════════════════════ 평면: 원과 부채꼴
@autofit
def fig_circle_parts(R, points, radii=(), chords=(), angles=(), arc_labels=(), shade=(), seg_labels=(),
                     center='O', circle=True, scale=22, width=200, height=200):
    """원 O 위의 점들.
    points {'A': 각도}, radii 'AB' 또는 ['A','B'], chords [('A','B')],
    angles [('A','B','40°')] (A→B 반시계), arc_labels [('A','B','6cm')], shade [('A','B','y')],
    seg_labels [('A','B','5cm', side)]"""
    c = Canvas(scale)
    O = (0, 0)
    pt = {k: _add(O, _u(a), R) for k, a in points.items()}
    for a, b, col in shade:
        a0 = points[a]
        span = (points[b] - a0) % 360
        c.poly([O] + c.arc_pts(O, R, a0, a0 + span, n=60), fill=_fc(col), stroke='none')
    if circle:
        c.circle(O, R)
    for k in radii:
        c.line(O, pt[k])
    for a, b in chords:
        c.line(pt[a], pt[b], sw=1.2)
    for a, b, lab in angles:
        c.angle_mark(O, points[a], points[b], label=lab, size=12)
    for a, b, lab in arc_labels:
        span = (points[b] - points[a]) % 360
        c.text(_add(O, _u(points[a] + span / 2), R), lab, size=12, d=_scale(_u(points[a] + span / 2), 17))
    for a, b, lab, side in seg_labels:
        c.seg_label(pt[a], pt[b], lab, side=side)
    for k, a in points.items():
        c.text(pt[k], k, size=12, d=_scale(_u(a), 10))
    c.dot(O)
    if center:
        c.text(O, center, size=12, d=_scale(_u(_free_dir(points, radii)), 10))
    return c.svg(width, height)


def _free_dir(points, radii):
    dirs = sorted(points[k] % 360 for k in radii)
    if not dirs:
        return 270
    if len(dirs) == 1:
        return dirs[0] + 180
    best, bd = 0, -1
    for i in range(len(dirs)):
        a = dirs[i]
        b = dirs[(i + 1) % len(dirs)] + (360 if i == len(dirs) - 1 else 0)
        if b - a > bd:
            bd, best = b - a, (a + b) / 2
    return best


@autofit
def fig_sector(r, theta, start=None, fill='y', r_label=None, theta_label=None, arc_label=None, r_side=-1,
               scale=22, width=170, height=160):
    """부채꼴 하나(반지름 r, 중심각 theta)."""
    c = Canvas(scale)
    start = 90 - theta / 2 if start is None else start
    O = (0, 0)
    a0, a1 = start, start + theta
    c.poly([O] + c.arc_pts(O, r, a0, a1, n=60), fill=_fc(fill))
    c.dot(O)
    if theta_label:
        c.angle_mark(O, a0, a1, label=theta_label, size=12)
    if r_label:
        c.seg_label(O, _add(O, _u(a0), r), r_label, side=r_side)
    if arc_label:
        m = (a0 + a1) / 2
        c.text(_add(O, _u(m), r), arc_label, size=12, d=_scale(_u(m), 14))
    c.text(O, 'O', size=12, d=_scale(_u(a0 + theta / 2 + 180), 10))
    return c.svg(width, height)


@autofit
def fig_sector_band(R, r, theta, start=None, fill='y', labels=None, scale=22, width=220, height=160):
    """큰 부채꼴 − 작은 부채꼴(띠). labels=(안쪽 반지름 라벨, 띠 폭 라벨)"""
    c = Canvas(scale)
    start = 90 - theta / 2 if start is None else start
    O = (0, 0)
    a0, a1 = start, start + theta
    outer = c.arc_pts(O, R, a0, a1, n=60)
    inner = c.arc_pts(O, r, a1, a0, n=60)
    c.poly(outer + inner, fill=_fc(fill))
    c.line(O, inner[-1])
    c.line(O, inner[0])
    c.dot(O)
    c.text(O, 'O', size=12, d=(0, -10))
    c.angle_mark(O, a0, a1, label=deg(theta))
    l1, l2 = labels or (cm(r), cm(R - r))
    nrm = _u(a0 - 90)
    c.text(_add(O, _u(a0), r / 2), l1, size=12, d=_scale(nrm, 10))
    c.text(_add(O, _u(a0), (r + R) / 2), l2, size=12, d=_scale(nrm, 10))
    for k in (r, R):
        q = _add(O, _u(a0), k)
        c.line(_add(q, nrm, c.px(3)), _add(q, nrm, -c.px(3)), sw=1.0)
    return c.svg(width, height)


@autofit
def fig_square_quarter(a, kind='outside', fill='c', label=None, scale=22, width=160, height=160):
    """한 변이 a인 정사각형과 사분원.
    'outside' 왼쪽 아래 꼭짓점 중심 사분원의 바깥(정사각형 − 사분원) 색칠
    'inside'  사분원 안쪽 색칠
    'lens'    마주 보는 두 꼭짓점 중심 두 사분원의 겹친 부분 색칠"""
    c = Canvas(scale)
    S = [(0, 0), (a, 0), (a, a), (0, a)]
    q1 = c.arc_pts((0, 0), a, 0, 90, n=60)
    if kind == 'outside':
        c.poly([(a, 0), (a, a), (0, a)] + q1[::-1][1:-1], fill=_fc(fill), stroke='none')
    elif kind == 'inside':
        c.poly([(0, 0)] + q1, fill=_fc(fill), stroke='none')
    elif kind == 'lens':
        q2 = c.arc_pts((a, a), a, 180, 270, n=60)
        c.poly(q1 + q2[1:-1], fill=_fc(fill), stroke='none')
        c.poly(q2, close=False)
    c.poly(S)
    c.poly(q1, close=False)
    c.text((a / 2, 0), label or cm(a), size=12, d=(0, -10))
    c.text((0, a / 2), label or cm(a), size=12, d=(-20, 0))
    return c.svg(width, height)


@autofit
def fig_semicircles(d1, d2, fill='m', labels=None, scale=22, width=220, height=140):
    """지름 d1+d2인 큰 반원 안에 지름 d1, d2인 두 반원. 큰 반원 − 두 반원 색칠."""
    c = Canvas(scale)
    D = d1 + d2
    big = c.arc_pts((D / 2, 0), D / 2, 0, 180, n=80)
    s1 = c.arc_pts((d1 / 2, 0), d1 / 2, 180, 0, n=60)
    s2 = c.arc_pts((d1 + d2 / 2, 0), d2 / 2, 180, 0, n=60)
    c.poly(big + s1[1:] + s2[1:-1], fill=_fc(fill))
    c.poly(s1, close=False)
    c.poly(s2, close=False)
    l1, l2 = labels or (cm(d1), cm(d2))
    c.text((d1 / 2, 0), l1, size=12, d=(0, -10))
    c.text((d1 + d2 / 2, 0), l2, size=12, d=(0, -10))
    for x in (0, d1, D):
        c.dot((x, 0), r=1.8)
    return c.svg(width, height)


# ═════════════════════════════════════════ 입체: 볼록 다면체 겨냥도
class View:
    def __init__(self, tilt=20, yaw=25):
        self.t = math.radians(tilt)
        self.y = math.radians(yaw)

    def rot(self, p):
        x, y, z = p
        cy, sy = math.cos(self.y), math.sin(self.y)
        return (x * cy - z * sy, y, x * sy + z * cy)

    def proj(self, p):
        x, y, z = self.rot(p)
        return (x, y * math.cos(self.t) + z * math.sin(self.t))

    def vdir(self):
        return (0, -math.sin(self.t), math.cos(self.t))


@autofit
def fig_polyhedron(V, F, view=None, fill='c', labels=(), vnames=None, face_fills=None, extra=None,
                   scale=22, width=190, height=180):
    """볼록 다면체. V: 3D 꼭짓점(x, y 위, z 안쪽), F: 면(꼭짓점 번호 목록).
    보이는 면은 연한 색, 숨은 모서리는 점선.
    labels: [((x,y,z), '5cm') | ((x,y,z), '5cm', (dx_px, dy_px))]  vnames: 꼭짓점 이름 목록
    face_fills {면 번호: 색키}  extra: callable(c, proj)"""
    view = view or View()
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

    vis = [sum(n_ * d for n_, d in zip(normal(f), vd)) < -1e-9 for f in F]
    edge_faces = {}
    for fi, f in enumerate(F):
        for k in range(len(f)):
            e = tuple(sorted((f[k], f[(k + 1) % len(f)])))
            edge_faces.setdefault(e, []).append(fi)
    c = Canvas(scale)
    P2 = [view.proj(p) for p in V]
    for fi, f in enumerate(F):
        if vis[fi]:
            col = (face_fills or {}).get(fi, fill)
            if col:
                c.poly([P2[i] for i in f], fill=_fc(col), stroke='none', opacity=0.8)
    for (a, b), fs in sorted(edge_faces.items(), key=lambda e: any(vis[i] for i in e[1])):
        v_ = any(vis[i] for i in fs)
        c.line(P2[a], P2[b], dash=None if v_ else '4 3', sw=1.4 if v_ else 1.0)
    pc = (sum(p[0] for p in P2) / len(P2), sum(p[1] for p in P2) / len(P2))
    if vnames:
        for i, nm in enumerate(vnames):
            if nm:
                c.text(P2[i], nm, size=12, d=_scale(_u(_dir(pc, P2[i])), 11))
    for lab in labels:
        c.text(view.proj(lab[0]), lab[1], size=12, d=lab[2] if len(lab) > 2 else (0, 0))
    if extra:
        extra(c, view.proj)
    return c.svg(width, height)


def prism(base, h):
    """밑면 base(xz 평면 2D 점)를 높이 h로 세운 각기둥."""
    n = len(base)
    V = [(x, 0, z) for x, z in base] + [(x, h, z) for x, z in base]
    F = [list(range(n)), list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return V, F


def pyramid(base, h, apex=None):
    n = len(base)
    ax, az = apex if apex else (sum(p[0] for p in base) / n, sum(p[1] for p in base) / n)
    V = [(x, 0, z) for x, z in base] + [(ax, h, az)]
    F = [list(range(n))] + [[i, (i + 1) % n, n] for i in range(n)]
    return V, F


def frustum(base, k, h):
    """각뿔대: 윗면 = 밑면을 무게중심 기준 k배."""
    n = len(base)
    cx, cz = sum(p[0] for p in base) / n, sum(p[1] for p in base) / n
    top = [(cx + k * (x - cx), cz + k * (z - cz)) for x, z in base]
    V = [(x, 0, z) for x, z in base] + [(x, h, z) for x, z in top]
    F = [list(range(n)), list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return V, F


def reg_base(n, R, rot=0):
    return [(R * math.cos(math.radians(rot + 360 * i / n)), R * math.sin(math.radians(rot + 360 * i / n)))
            for i in range(n)]


def rect_base(w, d):
    """가로 w, 깊이 d 직사각형(앞쪽 변이 z=0)."""
    return [(0, 0), (w, 0), (w, d), (0, d)]


def box(w, d, h):
    return prism(rect_base(w, d), h)


def tetrahedron(a=3.0):
    return pyramid(reg_base(3, a / math.sqrt(3), rot=90), a * math.sqrt(2 / 3))


def octahedron(a=3.0):
    r = a / math.sqrt(2)
    V = [(r, 0, 0), (0, 0, r), (-r, 0, 0), (0, 0, -r), (0, r, 0), (0, -r, 0)]
    F = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [1, 0, 5], [2, 1, 5], [3, 2, 5], [0, 3, 5]]
    return V, F


def cube(a=3.0):
    return box(a, a, a)


# ═════════════════════════════════════════ 입체: 회전체 겨냥도
@autofit
def fig_round(parts, labels=(), fill=None, tilt=17, scale=22, width=170, height=200):
    """아래에서 위로 쌓은 회전체.
    parts: {'t':'cyl','r','h'} | {'t':'cone','r','h'}(꼭짓점 위) | {'t':'cone_down','r','h'}(꼭짓점 아래, 맨 아래만)
           | {'t':'frustum','r1'(아래),'r2'(위),'h'} | {'t':'hemi','r'}(돔, 맨 위만) | {'t':'hemi_down','r'}(그릇, 맨 아래만)
           | {'t':'sphere','r'}(단독)
    labels: ('r', 층, '3cm') 반지름 점선 · ('d', 층, '6cm') 지름 점선 · ('h', 부품, '5cm') 축 점선 + 왼쪽 라벨
            ('hs', 부품, '5cm') 오른쪽 옆선 라벨 · ('l', 부품, '5cm') 원뿔 모선 라벨
    층 번호: 아래 면 0부터 부품 경계마다 하나."""
    t = math.radians(tilt)
    k = math.sin(t)
    ch = math.cos(t)
    c = Canvas(scale)
    cols = fill or ['c', 'y', 'm', 'g']
    parts = [dict(p) for p in parts]
    if parts[0]['t'] == 'sphere':
        r = parts[0]['r']
        c.circle((0, 0), r, fill=_fc(cols[0]))
        c.poly(c.arc_pts((0, 0), r, 180, 360, n=60, ry=r * k), close=False)
        c.poly(c.arc_pts((0, 0), r, 0, 180, n=60, ry=r * k), close=False, dash='4 3', sw=1.0)
        c.dot((0, 0), r=1.8)
        for lab in labels:
            if lab[0] == 'r':
                c.line((0, 0), (r, 0), dash='3 2', sw=1.0)
                c.text((r / 2, 0), lab[2], size=12, d=(0, 9))
        return c.svg(width, height)
    levels = []
    y = 0.0
    for i, p in enumerate(parts):
        tp = p['t']
        rb, rt, h = {
            'cyl': lambda: (p['r'], p['r'], p['h']), 'cone': lambda: (p['r'], 0, p['h']),
            'cone_down': lambda: (0, p['r'], p['h']), 'frustum': lambda: (p['r1'], p['r2'], p['h']),
            'hemi': lambda: (p['r'], 0, 0), 'hemi_down': lambda: (0, p['r'], 0)}[tp]()
        if i == 0:
            levels.append((y, rb))
        y += h * ch
        levels.append((y, rt))
        p['_y0'], p['_y1'], p['_rb'], p['_rt'] = y - h * ch, y, rb, rt

    def ell(yc, r, a0, a1):
        return c.arc_pts((0, yc), r, a0, a1, n=60, ry=r * k)

    for i, p in enumerate(parts):
        col = _fc(cols[i % len(cols)])
        tp, y0, y1, rb, rt = p['t'], p['_y0'], p['_y1'], p['_rb'], p['_rt']
        if tp == 'hemi':
            c.poly(c.arc_pts((0, y0), rb, 0, 180, n=60) + ell(y0, rb, 180, 360), fill=col, stroke='none')
        elif tp == 'hemi_down':
            c.poly(c.arc_pts((0, y1), rt, 180, 360, n=60) + ell(y1, rt, 0, 180), fill=col, stroke='none')
        else:
            low = ell(y0, rb, 180, 360) if rb > 0 else [(0, y0)]
            up = ell(y1, rt, 0, 180) if rt > 0 else [(0, y1)]
            c.poly(low + up, fill=col, stroke='none')
    for p in parts:
        tp, y0, y1, rb, rt = p['t'], p['_y0'], p['_y1'], p['_rb'], p['_rt']
        if tp == 'hemi':
            c.poly(c.arc_pts((0, y0), rb, 0, 180, n=60), close=False)
        elif tp == 'hemi_down':
            c.poly(c.arc_pts((0, y1), rt, 180, 360, n=60), close=False)
        elif rt == 0:
            phi = math.asin(min(1, (rb * k) / (y1 - y0)))
            for sg in (1, -1):
                c.line((sg * rb * math.cos(phi), y0 + rb * k * math.sin(phi)), (0, y1))
        elif rb == 0:
            phi = math.asin(max(-1, -(rt * k) / (y1 - y0)))
            for sg in (1, -1):
                c.line((0, y0), (sg * rt * math.cos(phi), y1 + rt * k * math.sin(phi)))
        else:
            c.line((-rb, y0), (-rt, y1))
            c.line((rb, y0), (rt, y1))
    top_i = len(levels) - 1
    for li, (yc, r) in enumerate(levels):
        if r <= 0:
            continue
        if li == top_i:
            c.poly(ell(yc, r, 0, 360)[:-1])
        else:
            c.poly(ell(yc, r, 180, 360), close=False)
            c.poly(ell(yc, r, 0, 180), close=False, dash='4 3', sw=1.0)
    for lab in labels:
        kind, idx, s = lab[0], lab[1], lab[2]
        if kind in ('r', 'd'):
            yc, r = levels[idx]
            x0 = 0 if kind == 'r' else -r
            c.line((x0, yc), (r, yc), dash='3 2', sw=1.0)
            c.dot((0, yc), r=1.8)
            c.text(((x0 + r) / 2, yc), s, size=12, d=(0, 9 if idx == top_i else -9))
        elif kind == 'h':
            p = parts[idx]
            c.line((0, p['_y0']), (0, p['_y1']), dash='3 2', sw=1.0)
            c.right_mark((0, p['_y0'] if p['_rt'] == 0 or p['t'] != 'cone_down' else p['_y1']), 0,
                         90 if p['t'] != 'cone_down' else -90, k=6)
            c.text((0, (p['_y0'] + p['_y1']) / 2), s, size=12, d=(-20, 0))
        elif kind == 'hs':
            p = parts[idx]
            c.text((max(p['_rb'], p['_rt']), (p['_y0'] + p['_y1']) / 2), s, size=12, d=(20, 0))
        elif kind == 'l':
            p = parts[idx]
            r_ = max(p['_rb'], p['_rt'])
            c.text((r_ / 2, (p['_y0'] + p['_y1']) / 2), s, size=12, d=(18, 0))
    return c.svg(width, height)


# ═════════════════════════════════════════ 전개도
@autofit
def fig_net_cylinder(r, h, r_label=None, h_label=None, w_label=None, scale=22, width=230, height=200):
    """원기둥 전개도: 가로 2πr, 세로 h 직사각형 + 위아래 원."""
    c = Canvas(scale)
    W = 2 * math.pi * r
    c.poly([(0, 0), (W, 0), (W, h), (0, h)], fill=FILL['c'])
    cx = W / 2
    c.circle((cx, h + r), r, fill=FILL['y'])
    c.circle((cx, -r), r, fill=FILL['y'])
    if r_label:
        c.line((cx, h + r), (cx + r, h + r), dash='3 2', sw=1.0)
        c.dot((cx, h + r), r=1.8)
        c.text((cx + r / 2, h + r), r_label, size=12, d=(0, 9))
    if h_label:
        c.text((0, h / 2), h_label, size=12, d=(-20, 0))
    if w_label:
        c.text((W * 0.22, h), w_label, size=12, d=(0, 9))
    return c.svg(width, height)


@autofit
def fig_net_cone(l, theta, r, l_label=None, theta_label=None, r_label=None, scale=22, width=180, height=220):
    """원뿔 전개도: 반지름 l·중심각 theta 부채꼴 + 반지름 r 밑면 원. theta = 360r/l 인지 확인한다."""
    assert abs(theta - 360 * r / l) < 1e-6, '전개도 치수 불일치'
    c = Canvas(scale)
    O = (0, 0)
    a0 = 270 - theta / 2
    c.poly([O] + c.arc_pts(O, l, a0, a0 + theta, n=80), fill=FILL['m'])
    cc = (0, -(l + r))
    c.circle(cc, r, fill=FILL['y'])
    c.dot(O)
    if l_label:
        c.seg_label(O, _add(O, _u(a0), l), l_label, side=1)
    if theta_label:
        c.angle_mark(O, a0, a0 + theta, label=theta_label, size=12)
    if r_label:
        c.line(cc, _add(cc, (r, 0)), dash='3 2', sw=1.0)
        c.dot(cc, r=1.8)
        c.text(_add(cc, (r / 2, 0)), r_label, size=12, d=(0, 9))
    return c.svg(width, height)


@autofit
def fig_net(polys, labels=(), scale=22, width=220, height=200):
    """일반 전개도: polys = [(점 목록, 색키)], labels = [(점, 문자) | (점, 문자, (dx, dy))]"""
    c = Canvas(scale)
    for pts, col in polys:
        c.poly(pts, fill=_fc(col))
    c.labels(labels)
    return c.svg(width, height)


def cube_net(cells, a=1.0, letters=None, cols=None):
    """정육면체 전개도 칸. cells: [(열, 행)] 6칸(행은 위로 증가). letters: 칸 글자."""
    polys, labels = [], []
    for i, (x, y) in enumerate(cells):
        pts = [(x * a, y * a), ((x + 1) * a, y * a), ((x + 1) * a, (y + 1) * a), (x * a, (y + 1) * a)]
        polys.append((pts, (cols or FILL_ORDER)[i % len(cols or FILL_ORDER)]))
        if letters:
            labels.append((((x + .5) * a, (y + .5) * a), letters[i]))
    return polys, labels


# ═════════════════════════════════════════ 회전체: 축과 평면도형
@autofit
def fig_rotation(shape, labels=(), right=(), mirror=False, fill='y', scale=22, width=170, height=190):
    """직선 l(x=0)을 회전축으로 하는 평면도형. shape: 2D 점(x ≥ 0).
    labels [(점, 문자) | (점, 문자, (dx, dy))], right [(꼭짓점, 방향1, 방향2)].
    mirror=True: 해설용. 회전축을 포함하는 평면으로 자른 단면(거울상 포함)을 함께 그린다."""
    c = Canvas(scale)
    ys = [p[1] for p in shape]
    lo, hi = min(ys) - c.px(20), max(ys) + c.px(34)
    c.line((0, lo), (0, hi), sw=1.0, dash='7 3 2 3')
    c.text((0, hi), it('l'), size=14, d=(8, 6))
    if mirror:
        c.poly([(-x, y) for x, y in shape], fill='#f6d9d4', stroke=ACCENT, sw=1.3, dash='5 3')
    c.poly(shape, fill=_fc(fill))
    for v, d1, d2 in right:
        c.right_mark(v, d1, d2)
    c.labels(labels)
    cy = hi - c.px(12)
    arc = c.arc_pts((0, cy), c.px(13), 200, 520, n=40, ry=c.px(4))
    c.poly(arc[:-6], sw=1.0, close=False)
    tip = arc[-6]
    c.poly([_add(tip, (-c.px(4), c.px(2))), tip, _add(tip, (-c.px(3.5), -c.px(2.5)))], sw=1.0, close=False)
    return c.svg(width, height)


def fig_rotation_trapezoid(rt, rb, h, mirror=False):
    if mirror:
        lab = [((0, h), cm(2 * rt), (0, 10)), ((0, 0), cm(2 * rb), (0, -10)), ((rb, h / 2), cm(h), (14, 0))]
    else:
        lab = [((rt / 2, h), cm(rt), (0, 10)), ((rb / 2, 0), cm(rb), (0, -10)), ((0, h / 2), cm(h), (-20, 0))]
    return fig_rotation([(0, 0), (rb, 0), (rt, h), (0, h)], labels=lab,
                        right=[((0, 0), 0, 90), ((0, h), 0, -90)], mirror=mirror,
                        width=250 if mirror else 170)


# ═════════════════════════════════════════ 예전 샘플 호환
def fig_pentagon_exterior(interior, show, ext_at=None, unknown_at=None, lengths=(4, 3.5, 5.5), sol_label=None):
    P = polygon_by_angles(interior, lengths)
    return fig_polygon(P, angles=show, ext={ext_at: deg(180 - interior[ext_at])} if ext_at is not None else None,
                       unknown={unknown_at: X_ITAL} if unknown_at is not None else None,
                       accent={ext_at: sol_label} if sol_label else None)


def fig_two_sectors(R, ab, cd, a_start=200, c_start=300, arc_label='6cm'):
    pts = {'A': a_start, 'B': a_start + ab, 'C': c_start, 'D': (c_start + cd) % 360}
    return fig_circle_parts(R, pts, radii='ABCD', chords=[('A', 'B'), ('C', 'D')],
                            angles=[('A', 'B', deg(ab)), ('C', 'D', deg(cd))], arc_labels=[('A', 'B', arc_label)])


def fig_frustum(n=5, Rb=3.0, Rt=1.6, H=3.4, tilt=18, rot=12):
    V, F = frustum(reg_base(n, Rb, rot), Rt / Rb, H)
    return fig_polyhedron(V, F, view=View(tilt=tilt, yaw=0))


def fig_hemi_cone(r, h, slant=None):
    lab = [('r', 1, cm(r)), ('h', 0, cm(h))] + ([('l', 0, cm(slant))] if slant else [])
    return fig_round([{'t': 'cone_down', 'r': r, 'h': h}, {'t': 'hemi', 'r': r}], labels=lab)
