#!/usr/bin/env python3
# build_connections.py — 연결망 SSOT 생성기 (A2)
#
# 입력: 30_content/units/*/meta.json  (단원 메타 — key-concepts, persons)
# 출력: 30_content/graph/connections.json  (nav app A3 의 데이터 소스)
#
# 노드 = 단원(unit) + 개념(concept, parent=unit) + 상위학년(future, 예고 stub)
# 엣지 = same-person(단원-단원) + concept-prereq(개념 학습 선후) + forward(상위 학년)
#
# 링크 경로는 배포 사이트(mid1/) 기준 상대경로 (nav app = mid1/map/index.html):
#   video : ../story/unit{NN}/index.html
#   app   : ../math1/{NN}_{slug-en}/index.html
#
# 확장 가능: 중2~고1·과목 간 노드는 같은 스키마로 추가. future 노드를 실제 단원으로 승격하면 됨.
# 실행:  PYTHONIOENCODING=utf-8 python 70_tools/build_connections.py
import json, glob, re, io
from collections import defaultdict, Counter

units = {}
for d in sorted(glob.glob("30_content/units/*/meta.json")):
    m = json.load(open(d, encoding="utf-8"))
    units[m["id"]] = m

ERA = {"era-ancient": "고대", "era-medieval": "중세", "era-renaissance": "르네상스",
       "era-early-modern": "근대초", "era-modern": "근대", "era-victorian": "근대"}
PERSON_KO = {"eratosthenes": "에라토스테네스", "brahmagupta": "브라마굽타", "al-khwarizmi": "알콰리즈미",
             "viete": "비에트", "diophantus": "디오판토스", "descartes": "데카르트", "fermat": "페르마",
             "kepler": "케플러", "boyle": "보일", "euclid": "유클리드", "thales": "탈레스",
             "gauss": "가우스", "pythagoras": "피타고라스", "archimedes": "아르키메데스",
             "liu-hui": "유휘", "plato": "플라톤", "cavalieri": "카발리에리",
             "nightingale": "나이팅게일", "playfair": "플레이페어"}
WORD = {"01": "정리", "02": "발명", "03": "균형", "04": "수수께끼", "05": "만남", "06": "조화",
        "07": "약속", "08": "규칙", "09": "수", "10": "π", "11": "다섯", "12": "쌓기", "13": "그림"}

# 배포 사이트(mid1/math1/)의 실제 디렉터리명 — meta slug-en 과 다를 수 있어 검증본 고정 (2026-06-01 확인).
MID1_DIR = {"01": "01_prime-factorization", "02": "02_integers-rationals",
            "03": "03_variables-expressions", "04": "04_linear-equations",
            "05": "05_coordinates-graphs", "06": "06_proportionality",
            "07": "07_basic-geometry", "08": "08_construction-congruence",
            "09": "09_polygons", "10": "10_circles-sectors",
            "11": "11_polyhedra-solids", "12": "12_solid-geometry",
            "13": "13_data-statistics"}

def short(c):  # '소수 (prime number)' -> '소수'
    return re.split(r"[ (（—\-]", c.strip())[0].strip()

nodes = []
concept_index = {}
for uid, m in units.items():
    persons = m.get("persons", [])
    prim = persons[0] if persons else {}
    era = ERA.get(prim.get("era-palette", ""), "")
    pnames = [PERSON_KO.get(p["ref"], p["ref"]) for p in persons]
    slug = m.get("slug-en", "")
    nodes.append({
        "id": f"u{uid}", "level": "unit", "grade": "mid1", "chapter": m.get("chapter"),
        "title": m["title-ko"], "slug-en": slug,
        "persons": pnames, "primary-person": pnames[0] if pnames else None,
        "era": era, "word": WORD.get(uid, ""),
        "links": {
            "video": f"../story/unit{uid}/index.html",
            "app": f"../math1/{MID1_DIR[uid]}/index.html",
        },
    })
    concept_index[uid] = []
    for i, c in enumerate(m.get("key-concepts", []), 1):
        cid = f"u{uid}-c{i:02d}"
        nodes.append({"id": cid, "level": "concept", "parent": f"u{uid}",
                      "label": short(c), "full": c})
        concept_index[uid].append((cid, short(c), c))

def cref(uid, kw):
    for cid, sh, full in concept_index.get(uid, []):
        if kw in full or kw in sh:
            return cid
    return f"u{uid}"

edges = []
def E(frm, to, etype, label):
    edges.append({"from": frm, "to": to, "type": etype, "label": label})

# 1) same-person (단원-단원) — persons 교차에서 자동 도출
byperson = defaultdict(list)
for uid, m in units.items():
    for p in m.get("persons", []):
        byperson[p["ref"]].append(uid)
for ref, uids in byperson.items():
    if len(uids) > 1:
        ko = PERSON_KO.get(ref, ref)
        for a, b in zip(uids, uids[1:]):
            E(f"u{a}", f"u{b}", "same-person", ko)

# 2) concept-prereq (개념 학습 선후) — 큐레이션
PRE = [
    ("01", "소인수분해", "02", "정수", "수의 확장: 자연수→정수·유리수"),
    ("02", "유리수", "03", "문자", "수를 문자로 일반화"),
    ("03", "일차식", "04", "일차방정식", "식 → 등식 풀기"),
    ("03", "문자", "06", "정비례", "문자식 y=ax"),
    ("05", "좌표평면", "06", "정비례", "좌표 위에 그래프"),
    ("04", "일차방정식", "05", "그래프", "해를 좌표로 보기"),
    ("07", "각", "08", "작도", "각·길이 → 작도"),
    ("07", "평행", "09", "다각형", "평행선·각 → 내각합"),
    ("08", "합동", "09", "다각형", "합동 → 다각형 성질"),
    ("09", "다각형", "11", "다면체", "평면도형 → 입체"),
    ("10", "넓이", "12", "구", "원의 넓이 → 구·원뿔 부피"),
    ("11", "회전체", "12", "회전체", "회전체 → 겉넓이·부피"),
    ("05", "그래프", "13", "히스토그램", "그래프 읽기 → 통계 그래프"),
]
for fu, fk, tu, tk, lab in PRE:
    E(cref(fu, fk), cref(tu, tk), "concept-prereq", lab)

# 3) forward (상위 학년 예고) — stub 노드
FWD = [
    ("u06", "future:중2-일차함수", "정비례·반비례 → 일차함수 y=ax+b"),
    ("u04", "future:중2-연립방정식", "일차방정식 → 미지수 2개"),
    ("u09", "future:중2-삼각형의성질", "다각형 → 삼각형 닮음·성질"),
    ("u01", "future:중3-제곱근", "소인수분해 → 제곱근·무리수"),
    ("u13", "future:중2-확률", "자료 정리 → 확률"),
]
for frm, to, lab in FWD:
    E(frm, to, "forward", lab)
    nodes.append({"id": to, "level": "future", "label": to.split(":")[1]})

graph = {
    "$schema-note": ("math-story-telling 연결망 SSOT. 노드=단원(unit)+개념(concept)+상위학년(future). "
                     "확장 가능(중2~고1·과목 간). 생성: 70_tools/build_connections.py (meta.json 기반)."),
    "version": "0.1",
    "nodes": nodes,
    "edges": edges,
}
io.open("30_content/graph/connections.json", "w", encoding="utf-8").write(
    json.dumps(graph, ensure_ascii=False, indent=2))
print(f"nodes={len(nodes)}  edges={len(edges)}")
print("edge types:", dict(Counter(e["type"] for e in edges)))
