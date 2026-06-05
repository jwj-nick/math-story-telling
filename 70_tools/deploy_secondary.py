#!/usr/bin/env python3
# deploy_secondary.py — 완성된 secondary 영상을 배포(mid1)에 올리고 2인 chooser 페이지 생성.
# - 8-final.mp4 → mid1/story/_video/unitNN-<slug>.mp4 (faststart) + poster jpg
# - story/unitNN/index.html 을 primary+secondary 2인 chooser 로 교체
# primary 정보(이름/한단어/기존 mp4)는 현 배포 페이지에서 읽음.
import subprocess, re, pathlib, sys

SRC = pathlib.Path(r"C:\Kids\math-story-telling\50_channel")
DEPLOY = pathlib.Path(r"C:\Nick\30_Apps\jwj-nick.github.io\mid1\story")

# nn: (season, sec_slug_dir, sec_filekey, sec_ko, sec_word, sec_desc, prim_desc, wrapnote_html)
DATA = {
 "03": ("season-1-ancient","viete","viete","비에트","기호","기호 대수 발명","대수를 말로 풀다",
   "같은 <b>문자와 식</b>을 두 눈으로 봐요.<br>알콰리즈미는 말로 설명하는 대수(균형), 비에트는 수를 <b>문자 기호</b>로 적는 발명 — 기호는 약속이에요."),
 "05": ("season-1-ancient","fermat","fermat","페르마","번역","식 → 그림","그림 → 식",
   "같은 <b>좌표</b>를 두 방향으로 봐요.<br>데카르트는 그림을 식으로, 페르마는 <b>식을 그림으로</b> — 좌표는 둘 사이의 번역기."),
 "07": ("season-2-geometry","thales","thales","탈레스","그림자","닮음 · 비례","공준 · 증명",
   "같은 <b>도형</b>을 두 눈으로 봐요.<br>유클리드는 증명의 규칙, 탈레스는 <b>그림자</b>로 피라미드 높이를 잰 닮음·비례."),
 "08": ("season-2-geometry","gauss","gauss","가우스","가능","작도가능성의 경계","자·컴퍼스 작도",
   "같은 <b>작도</b>를 두 눈으로 봐요.<br>유클리드는 '어떻게 그리나'(규칙), 가우스는 '<b>어디까지 가능한가</b>' — 정17각형."),
 "10": ("season-2-geometry","liu-hui","liu-hui","유휘","더 잘게","할원술 · 3072각형","96각형으로 가두다",
   "같은 <b>π</b>를 두 눈으로 봐요.<br>아르키메데스는 96각형으로 가두고, 유휘는 <b>더 잘게</b> 쪼개 3.14159에 닿았어요."),
 "12": ("season-2-geometry","cavalieri","cavalieri","카발리에리","단면","단면을 쌓는 부피","구·원기둥 2:3",
   "같은 <b>부피</b>를 두 눈으로 봐요.<br>아르키메데스는 결과의 비(2:3), 카발리에리는 <b>단면</b>을 쌓는 적분의 직관."),
 "13": ("season-3-statistics","playfair","playfair","플레이페어","그림","그래프의 발명","coxcomb로 설득",
   "같은 <b>자료</b>를 두 눈으로 봐요.<br>플레이페어는 <b>그래프라는 그림</b>을 발명했고, 나이팅게일은 그 그림으로 세상을 설득했어요."),
}

TEMPLATE = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>Unit {nn} — {unit_title} — {prim_ko} · {sec_ko}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Nanum+Myeongjo:wght@700;800&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Noto Sans KR',sans-serif;background:#14110d;color:#f3ead9;
    min-height:100vh;display:flex;flex-direction:column;align-items:center;
    padding:max(16px,env(safe-area-inset-top)) 16px max(20px,env(safe-area-inset-bottom));}}
  .top{{width:100%;max-width:880px;display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}}
  .back{{color:#c9a14a;text-decoration:none;font-size:14px}}
  h1{{font-family:'Nanum Myeongjo',serif;font-size:clamp(20px,5vw,28px);margin:4px 0 2px;text-align:center}}
  .sub{{color:#a99b80;font-size:14px;margin-bottom:6px;text-align:center}}
  .wrap-note{{max-width:620px;color:#b7a884;font-size:13.5px;line-height:1.6;text-align:center;margin:2px 0 16px}}
  .picker{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:16px}}
  .p{{display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;
    background:#1d1812;border:1px solid #3a3324;border-radius:13px;padding:11px 18px;min-width:128px;transition:.15s}}
  .p:hover{{border-color:#6b5a2e}}
  .p[data-on="1"]{{border-color:#c9a14a;background:#241d15}}
  .p .nm{{font-family:'Nanum Myeongjo',serif;font-weight:800;font-size:17px;color:#f3ead9}}
  .p .wd{{font-size:12px;color:#D9A441}}
  .p .ds{{font-size:11.5px;color:#9a8d72}}
  .player{{width:100%;max-width:880px;border-radius:14px;overflow:hidden;
    box-shadow:0 10px 40px rgba(0,0,0,.55);background:#000}}
  video{{width:100%;height:auto;display:block}}
  .foot{{margin-top:18px;display:flex;gap:14px;flex-wrap:wrap;justify-content:center}}
  .foot a{{color:#cdbf9c;text-decoration:none;font-size:14px;border:1px solid #3a3324;
    border-radius:10px;padding:9px 16px}}
  .foot a:hover{{border-color:#c9a14a;color:#f3ead9}}
</style>
</head>
<body>
  <div class="top">
    <a class="back" href="../index.html">← 이야기 목록</a>
    <span style="font-family:'Nanum Myeongjo',serif;color:#D9A441;font-weight:800;font-size:14px;border:1px solid #6b5a2e;border-radius:999px;padding:4px 13px">Unit {nn} · {unit_title}</span>
  </div>
  <h1 id="ttl">{prim_ko}</h1>
  <div class="sub" id="sub">{prim_desc}</div>
  <div class="wrap-note">{wrapnote}</div>

  <div class="picker">
    <div class="p" data-on="1" onclick="pick('p1')">
      <span class="nm">{prim_ko}</span><span class="wd">한 단어 · {prim_word}</span><span class="ds">{prim_desc}</span>
    </div>
    <div class="p" data-on="0" onclick="pick('p2')">
      <span class="nm">{sec_ko}</span><span class="wd">한 단어 · {sec_word}</span><span class="ds">{sec_desc}</span>
    </div>
  </div>

  <div class="player">
    <video id="vid" controls playsinline preload="metadata" poster="../_video/unit{nn}.jpg">
      <source id="vsrc" src="../_video/unit{nn}.mp4" type="video/mp4" />
      이 브라우저는 영상을 지원하지 않습니다.
    </video>
  </div>

  <div class="foot">
    <a href="anim.html">🎞 예전 애니메이션 버전</a>
    <a href="../../math1/index.html">📐 수학 단원 앱</a>
  </div>

<script>
const DATA = {{
  p1: {{ttl:"{prim_ko}", sub:"{prim_desc}", mp4:"../_video/unit{nn}.mp4",            jpg:"../_video/unit{nn}.jpg"}},
  p2: {{ttl:"{sec_ko}",  sub:"{sec_desc}",  mp4:"../_video/unit{nn}-{sec_filekey}.mp4", jpg:"../_video/unit{nn}-{sec_filekey}.jpg"}}
}};
function pick(who){{
  const d=DATA[who], v=document.getElementById("vid"), s=document.getElementById("vsrc");
  document.getElementById("ttl").textContent=d.ttl;
  document.getElementById("sub").textContent=d.sub;
  v.pause(); s.src=d.mp4; v.setAttribute("poster",d.jpg); v.load();
  document.querySelectorAll(".p").forEach((p,i)=>p.dataset.on=(["p1","p2"][i]===who)?"1":"0");
}}
</script>
</body>
</html>
'''

def ffdur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)],capture_output=True,text=True).stdout.strip())

def read_primary(nn):
    idx = DEPLOY/f"unit{nn}"/"index.html"
    t = idx.read_text(encoding="utf-8")
    ko = re.search(r"<h1[^>]*>([^<]+)</h1>", t).group(1).strip()
    wm = re.search(r"한 단어 · ([^<]+)<", t)
    word = wm.group(1).strip() if wm else ""
    tm = re.search(r"Unit \d+ · ([^<\"]+)", t) or re.search(r"— ([^<—]+)</title>", t)
    title = (tm.group(1).strip() if tm else "")
    return ko, word, title

def main():
    only = sys.argv[1:] if len(sys.argv)>1 else list(DATA.keys())
    vid_dir = DEPLOY/"_video"
    for nn in only:
        season, slug, fk, sec_ko, sec_word, sec_desc, prim_desc, wrap = DATA[nn]
        src = SRC/season/f"unit-{nn}"/slug/"8-final.mp4"
        if not src.exists():
            print(f"  SKIP u{nn}: {src} 없음"); continue
        prim_ko, prim_word, title = read_primary(nn)
        # 영상 faststart 복사 + poster
        out = vid_dir/f"unit{nn}-{fk}.mp4"
        subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-i",str(src),
            "-c","copy","-movflags","+faststart",str(out)], check=True)
        poster = src.parent/"8-poster.jpg"
        if poster.exists(): (vid_dir/f"unit{nn}-{fk}.jpg").write_bytes(poster.read_bytes())
        # chooser html
        html = TEMPLATE.format(nn=nn, unit_title=title, prim_ko=prim_ko, prim_word=prim_word,
            prim_desc=prim_desc, sec_ko=sec_ko, sec_word=sec_word, sec_desc=sec_desc,
            sec_filekey=fk, wrapnote=wrap)
        (DEPLOY/f"unit{nn}"/"index.html").write_text(html, encoding="utf-8")
        print(f"  OK u{nn}: {prim_ko}+{sec_ko}  {ffdur(out):.0f}s  ({title})")
    print("== deploy 완료 ==")

if __name__ == "__main__":
    main()
