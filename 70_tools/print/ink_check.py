"""ink_check.py — PDF 쪽을 그림으로 바꾸고, 잉크(C·M·Y·K) 사용량을 대략 추정한다.

추정 방법: 각 픽셀 RGB를 단순 변환 K = 1 − max(R,G,B), C = (1 − R − K)/(1 − K) … 로 바꿔
채널별 덮임 합을 낸다. 실제 프린터 드라이버의 변환(UCR/GCR)과 다르므로 '비율 경향'만 본다.

사용: python ink_check.py <png 출력 폴더> <pdf> [<pdf> ...]
"""
import sys
from pathlib import Path

import pymupdf

sys.stdout.reconfigure(encoding='utf-8')


def coverage(pix):
    s = pix.samples
    n = pix.n
    tot = [0.0, 0.0, 0.0, 0.0]
    step = 3  # 3픽셀마다 하나만 본다(속도)
    cnt = 0
    for i in range(0, len(s), n * step):
        r, g, b = s[i] / 255, s[i + 1] / 255, s[i + 2] / 255
        k = 1 - max(r, g, b)
        if k < 1:
            tot[0] += (1 - r - k) / (1 - k)
            tot[1] += (1 - g - k) / (1 - k)
            tot[2] += (1 - b - k) / (1 - k)
        tot[3] += k
        cnt += 1
    return [t / cnt for t in tot]


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    grand = [0.0] * 4
    pages = 0
    for pdf in sys.argv[2:]:
        d = pymupdf.open(pdf)
        acc = [0.0] * 4
        for i, pg in enumerate(d):
            pix = pg.get_pixmap(dpi=110)
            pix.save(str(out / ('%s_p%d.png' % (Path(pdf).stem, i + 1))))
            cv = coverage(pg.get_pixmap(dpi=40))
            acc = [a + c for a, c in zip(acc, cv)]
        grand = [g + a for g, a in zip(grand, acc)]
        pages += d.page_count
        print('%s  %d쪽  C %.2f%%  M %.2f%%  Y %.2f%%  K %.2f%% (쪽 평균 덮임)' % (
            Path(pdf).name, d.page_count, *[100 * a / d.page_count for a in acc]))
    if pages:
        print('전체 %d쪽  C %.2f%%  M %.2f%%  Y %.2f%%  K %.2f%%' % (pages, *[100 * g / pages for g in grand]))


if __name__ == '__main__':
    main()
