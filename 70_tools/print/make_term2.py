"""make_term2.py — 세트 빌드 → PDF 인쇄 → 쪽 그림(PNG) + 잉크 추정을 한 번에.

사용: python make_term2.py <png 폴더> <세트이름> [<세트이름> ...]
PNG 는 <png 폴더>/<pdf 이름>_p<쪽>.png 로 저장된다(화면 검사용).
"""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import build_term2  # noqa: E402


def main():
    png_dir = sys.argv[1]
    pdfs = []
    for name in sys.argv[2:]:
        build_term2.build(name)
        mod = __import__(name)
        plan = build_term2.HTML_DIR / (mod.META['id'] + '_pdfplan.json')
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                            str(HERE / 'print_pdf.ps1'), '-Plan', str(plan)],
                           capture_output=True, text=True, encoding='cp949', errors='replace')
        print(r.stdout.strip())
        pdfs += [it['pdf'] for it in json.loads(plan.read_text(encoding='utf-8'))]
    subprocess.run([sys.executable, str(HERE / 'ink_check.py'), png_dir] + pdfs)


if __name__ == '__main__':
    main()
