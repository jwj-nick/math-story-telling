"""그림 함수 시험용 갤러리 (인쇄물 아님)."""
import figgen as F

META = {'id': 'm1-term2-gallery', 'title': '그림 함수 갤러리', 'subtitle': '시험용', 'kind': 'practice',
        'folder': '_gallery', 'file': 'gallery'}
SECTIONS = {'g': ('갤러리', '모든 그림 함수')}


def _p(i, fig, note):
    return {'id': 'g%02d' % i, 'sec': 'g', 'format': 'short', 'level': 'L', 'topic': note, 'stem_print': note,
            'figure': fig, 'answer_print': '-', 'hint': '-', 'solution': '-', 'work_mm': 5}


P = F.polygon_by_angles([60, 80, 40], [4])
Q = F.polygon_by_angles([100, 110, 70, 80], [4, 3])
figs = [
    (F.fig_polygon(P, angles={0: '60°', 1: '80°'}, ext={2: '140°'}, names='ABC'), '삼각형 외각'),
    (F.fig_polygon(Q, angles={0: '100°', 1: '110°', 2: '70°'}, unknown={3: F.X_ITAL}, fill='m'), '사각형 x'),
    (F.fig_regular_polygon(7, diag_from=0), '칠각형 대각선'),
    (F.fig_regular_polygon(6, all_diag=True, fill='g'), '육각형 모든 대각선'),
    (F.fig_star([30, 40, 35, 45, 30], ['30°', '40°', '35°', '45°', F.X_ITAL]), '별'),
    (F.fig_circle_parts(3, {'A': 200, 'B': 250, 'C': 330, 'D': 60}, radii='ABCD',
                        angles=[('A', 'B', '50°'), ('C', 'D', F.X_ITAL)],
                        arc_labels=[('A', 'B', '5cm'), ('C', 'D', '9cm')], shade=[('C', 'D', 'c')]), '원 부채꼴'),
    (F.fig_sector(6, 150, r_label='6cm', theta_label='150°', fill='p'), '부채꼴'),
    (F.fig_sector_band(6, 3, 120, fill='o'), '띠'),
    (F.fig_square_quarter(6, 'outside'), '정사각형-사분원'),
    (F.fig_square_quarter(6, 'lens', fill='m'), '렌즈'),
    (F.fig_semicircles(4, 6), '반원 3개'),
    (F.fig_polyhedron(*F.box(4, 2.5, 3), labels=[((2, 0, 0), '4cm', (0, -10)), ((4, 0, 1.25), '2.5cm', (22, -4)),
                                                  ((0, 1.5, 0), '3cm', (-18, 0))]), '직육면체'),
    (F.fig_polyhedron(*F.prism(F.reg_base(3, 2, 90), 4), fill='g'), '삼각기둥'),
    (F.fig_polyhedron(*F.pyramid(F.reg_base(4, 2.4, 45), 4), fill='y'), '사각뿔'),
    (F.fig_polyhedron(*F.frustum(F.reg_base(6, 3, 0), 0.5, 3), fill='p'), '육각뿔대'),
    (F.fig_polyhedron(*F.tetrahedron(4), fill='m', view=F.View(tilt=12, yaw=10)), '정사면체'),
    (F.fig_polyhedron(*F.octahedron(3.5), fill='c', view=F.View(tilt=15, yaw=20)), '정팔면체'),
    (F.fig_polyhedron(*F.cube(3), fill='o'), '정육면체'),
    (F.fig_round([{'t': 'cyl', 'r': 3, 'h': 5}], labels=[('r', 1, '3cm'), ('hs', 0, '5cm')]), '원기둥'),
    (F.fig_round([{'t': 'cone', 'r': 3, 'h': 4}], labels=[('r', 0, '3cm'), ('h', 0, '4cm'), ('l', 0, '5cm')]), '원뿔'),
    (F.fig_round([{'t': 'frustum', 'r1': 4, 'r2': 2, 'h': 3}], labels=[('r', 0, '4cm'), ('r', 1, '2cm')]), '원뿔대'),
    (F.fig_round([{'t': 'sphere', 'r': 3}], labels=[('r', 0, '3cm')]), '구'),
    (F.fig_round([{'t': 'hemi_down', 'r': 3}], labels=[('r', 1, '3cm')]), '반구 그릇'),
    (F.fig_round([{'t': 'cyl', 'r': 3, 'h': 4}, {'t': 'cone', 'r': 3, 'h': 3}],
                 labels=[('r', 0, '3cm'), ('hs', 0, '4cm'), ('h', 1, '3cm')]), '원기둥+원뿔'),
    (F.fig_round([{'t': 'cyl', 'r': 2, 'h': 4}, {'t': 'hemi', 'r': 2}], labels=[('r', 1, '2cm'), ('hs', 0, '4cm')]), '원기둥+반구'),
    (F.fig_hemi_cone(3, 4, 5), '아이스크림'),
    (F.fig_net_cylinder(3, 5, r_label='3cm', h_label='5cm', w_label='?'), '원기둥 전개도'),
    (F.fig_net_cone(10, 216, 6, l_label='10cm', theta_label='216°', r_label='6cm'), '원뿔 전개도'),
    (F.fig_net(*F.cube_net([(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)], letters='ABCDEF')), '정육면체 전개도'),
    (F.fig_rotation_trapezoid(2, 4, 3), '회전 사다리꼴'),
    (F.fig_rotation([(0, 0), (3, 0), (0, 4)], labels=[((1.5, 0), '3cm', (0, -10)), ((0, 2), '4cm', (-20, 0))],
                    right=[((0, 0), 0, 90)], fill='c'), '회전 삼각형'),
    (F.fig_rotation([(1, 0), (3, 0), (3, 3), (1, 3)], labels=[((2, 0), '2cm', (0, -10)), ((0.5, 0), '1cm', (0, -10)),
                                                              ((3, 1.5), '3cm', (18, 0))], fill='g'), '회전 떨어진 사각형'),
    (F.fig_rotation_trapezoid(2, 4, 3, mirror=True), '회전 단면 해설'),
    (F.fig_regular_turn(6), '외각 따라 돌기'),
]
PROBLEMS = [_p(i, f, n) for i, (f, n) in enumerate(figs)]


def check():
    pass
