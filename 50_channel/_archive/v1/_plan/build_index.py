"""
build_index.py — story-master 템플릿을 단원별 데이터로 채워 index.html 생성

사용:
  python build_index.py 01

또는 일괄:
  python build_index.py all

각 단원은 90_video/unitNN/config.json 에서 데이터를 읽음.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 90_video/
TEMPLATE = ROOT / "_templates" / "story-master.html"
SYMBOLS = ROOT / "_assets" / "symbols"


def load_symbol(name: str) -> str:
    """SVG 파일을 읽어 본문만 반환 (xmlns 헤더 유지)"""
    p = SYMBOLS / f"{name}.svg"
    if not p.exists():
        raise FileNotFoundError(f"symbol not found: {p}")
    return p.read_text(encoding="utf-8").strip()


def build_unit(unit_num: str) -> Path:
    unit_dir = ROOT / f"unit{unit_num}"
    config_file = unit_dir / "config.json"

    if not config_file.exists():
        raise FileNotFoundError(f"config.json not found: {config_file}")

    cfg = json.loads(config_file.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")

    # SVG 슬롯 인라인 치환
    cfg["S2_SYMBOL"] = load_symbol(cfg["s2_symbol"])
    cfg["S3_METAPHOR"] = load_symbol(cfg["s3_symbol"])
    cfg["S4_DIAGRAM"] = load_symbol(cfg["s4_symbol"])

    # placeholder 매핑
    replacements = {
        "{{UNIT_NN}}": f"unit-{unit_num}",
        "{{COMPOSITION_ID}}": f"story-unit{unit_num}",
        "{{DURATION}}": str(cfg.get("duration", 51)),
        "{{PERSON}}": cfg["person"],
        "{{ERA}}": cfg["era"],
        "{{UNIT_TITLE}}": cfg["unit_title"],
        "{{S2_HEAD}}": cfg["s2_head"],
        "{{S2_BODY}}": cfg["s2_body"],
        "{{S2_SYMBOL}}": cfg["S2_SYMBOL"],
        "{{S3_KEYWORD}}": cfg["s3_keyword"],
        "{{S3_TEXT}}": cfg["s3_text"],
        "{{S3_METAPHOR}}": cfg["S3_METAPHOR"],
        "{{S4_HEAD}}": cfg["s4_head"],
        "{{S4_TEXT}}": cfg["s4_text"],
        "{{S4_DIAGRAM}}": cfg["S4_DIAGRAM"],
        "{{S5_TEXT}}": cfg["s5_text"],
    }

    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)

    out_file = unit_dir / "index.html"
    out_file.write_text(out, encoding="utf-8")
    return out_file


def main():
    if len(sys.argv) < 2:
        print("usage: python build_index.py <unit_num | all>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "all":
        units = sorted([
            d.name.replace("unit", "")
            for d in ROOT.iterdir()
            if d.is_dir() and d.name.startswith("unit") and (d / "config.json").exists()
        ])
        for u in units:
            try:
                out = build_unit(u)
                print(f"[OK] unit{u}: {out}")
            except Exception as e:
                print(f"[FAIL] unit{u}: {e}")
    else:
        unit_num = arg.zfill(2)
        out = build_unit(unit_num)
        print(f"[OK] unit{unit_num}: {out}")


if __name__ == "__main__":
    main()
