#!/usr/bin/env python3
# deploy_videos_to_mid1.py — 1차 배포: 13편 영상을 jwj-nick.github.io/mid1/story 에 올리고
# story/unitNN 를 영상 플레이어로 교체(옛 애니는 anim.html 보존) + story/index 갤러리.
import os, re, glob, shutil, html

SRC = "C:/Kids/math-story-telling/50_channel"
DST = "C:/Nick/30_Apps/jwj-nick.github.io/mid1"
VID = os.path.join(DST, "story", "_video")
os.makedirs(VID, exist_ok=True)

# unit -> (인물, 한 단어, 단원명)  (인물·단어=신 narrative 기준 / 단원명=교과 단원)
META = {
 1:("에라토스테네스","정리","소인수분해"),
 2:("브라마굽타","발명","정수와 유리수"),
 3:("알콰리즈미","균형","문자와 식"),
 4:("디오판토스","수수께끼","일차방정식"),
 5:("데카르트","만남","좌표와 그래프"),
 6:("케플러","조화","정비례와 반비례"),
 7:("유클리드","약속","기본도형"),
 8:("유클리드","규칙","작도와 합동"),
 9:("피타고라스","수","다각형"),
 10:("아르키메데스","π","원과 부채꼴"),
 11:("플라톤","다섯","다면체와 회전체"),
 12:("아르키메데스","쌓기","입체도형의 겉넓이와 부피"),
 13:("나이팅게일","그림","자료의 정리와 해석"),
}

# unit -> source folder
src_map={}
for f in glob.glob(os.path.join(SRC,"*","unit-*")):
    m=re.search(r"unit-(\d+)-", f.replace("\\","/"))
    if m: src_map[int(m.group(1))]=f

def copy_assets():
    for n,folder in sorted(src_map.items()):
        for ext,dst in (("8-final.mp4",f"unit{n:02d}.mp4"),("8-poster.jpg",f"unit{n:02d}.jpg")):
            s=os.path.join(folder,ext); d=os.path.join(VID,dst)
            if os.path.exists(s):
                shutil.copy2(s,d); print(f"  copy u{n:02d} {ext} -> {dst} ({os.path.getsize(d)//1048576}MB)")

PAGE='''﻿<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>{person} — Unit {nn} — {chapter}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Nanum+Myeongjo:wght@700;800&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Noto Sans KR',sans-serif;background:#14110d;color:#f3ead9;
    min-height:100vh;display:flex;flex-direction:column;align-items:center;
    padding:max(16px,env(safe-area-inset-top)) 16px max(20px,env(safe-area-inset-bottom));}}
  .top{{width:100%;max-width:880px;display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}}
  .back{{color:#c9a14a;text-decoration:none;font-size:14px}}
  .word{{font-family:'Nanum Myeongjo',serif;color:#D9A441;font-weight:800;font-size:15px;
    border:1px solid #6b5a2e;border-radius:999px;padding:4px 14px}}
  h1{{font-family:'Nanum Myeongjo',serif;font-size:clamp(22px,5vw,30px);margin:6px 0 2px;text-align:center}}
  .sub{{color:#a99b80;font-size:14px;margin-bottom:16px;text-align:center}}
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
    <span class="word">한 단어 · {word}</span>
  </div>
  <h1>{person}</h1>
  <div class="sub">Unit {nn} · {chapter}</div>
  <div class="player">
    <video controls playsinline preload="metadata" poster="../_video/unit{nn}.jpg">
      <source src="../_video/unit{nn}.mp4" type="video/mp4" />
      이 브라우저는 영상을 지원하지 않습니다.
    </video>
  </div>
  <div class="foot">
    <a href="anim.html">🎞 예전 애니메이션 버전</a>
    <a href="../../math1/index.html">📐 수학 단원 앱</a>
  </div>
</body>
</html>
'''

def build_pages():
    for n,(person,word,chapter) in META.items():
        d=os.path.join(DST,"story",f"unit{n:02d}")
        idx=os.path.join(d,"index.html"); anim=os.path.join(d,"anim.html")
        if not os.path.exists(anim) and os.path.exists(idx):
            os.rename(idx,anim); print(f"  u{n:02d} index.html -> anim.html (옛 애니 보존)")
        with open(idx,"w",encoding="utf-8") as fp:
            fp.write(PAGE.format(person=html.escape(person),word=html.escape(word),
                                 nn=f"{n:02d}",chapter=html.escape(chapter)))
        print(f"  u{n:02d} new video page written")

GAL_HEAD='''﻿<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>수학자 이야기 — 중1 수학</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Nanum+Myeongjo:wght@700;800&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Noto Sans KR',sans-serif;background:#14110d;color:#f3ead9;
    padding:max(20px,env(safe-area-inset-top)) 16px max(28px,env(safe-area-inset-bottom))}
  header{max-width:980px;margin:0 auto 22px;text-align:center}
  .back{display:inline-block;color:#c9a14a;text-decoration:none;font-size:14px;margin-bottom:10px}
  h1{font-family:'Nanum Myeongjo',serif;font-size:clamp(24px,6vw,34px)}
  .lead{color:#a99b80;font-size:14px;margin-top:8px}
  .grid{max-width:980px;margin:0 auto;display:grid;
    grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
  a.card{display:block;text-decoration:none;color:inherit;background:#1d1812;
    border:1px solid #322a1c;border-radius:14px;overflow:hidden;transition:.15s}
  a.card:hover{border-color:#c9a14a;transform:translateY(-2px)}
  .thumb{position:relative;aspect-ratio:16/9;background:#000;overflow:hidden}
  .thumb img{width:100%;height:100%;object-fit:cover;display:block}
  .play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
    font-size:34px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.7)}
  .meta{padding:11px 13px}
  .u{color:#c9a14a;font-size:12px;font-weight:700}
  .p{font-family:'Nanum Myeongjo',serif;font-size:18px;margin:2px 0}
  .c{color:#a99b80;font-size:13px}
  .w{float:right;color:#D9A441;font-family:'Nanum Myeongjo',serif;font-weight:800;font-size:13px}
</style>
</head>
<body>
<header>
  <a class="back" href="../index.html">← 중1 수학</a>
  <h1>수학자 이야기</h1>
  <div class="lead">13단원, 13명의 수학자 — 각 영상이 남기는 한 단어. 카드를 누르면 영상이 열립니다.</div>
</header>
<div class="grid">
'''

def build_gallery():
    cards=[]
    for n,(person,word,chapter) in META.items():
        cards.append(f'''  <a class="card" href="unit{n:02d}/index.html">
    <div class="thumb"><img src="_video/unit{n:02d}.jpg" alt="{html.escape(person)}" loading="lazy"><div class="play">▶</div></div>
    <div class="meta"><span class="w">{html.escape(word)}</span><div class="u">UNIT {n:02d}</div>
      <div class="p">{html.escape(person)}</div><div class="c">{html.escape(chapter)}</div></div>
  </a>''')
    with open(os.path.join(DST,"story","index.html"),"w",encoding="utf-8") as fp:
        fp.write(GAL_HEAD+"\n".join(cards)+"\n</div>\n</body>\n</html>\n")
    print("  story/index.html gallery written")

if __name__=="__main__":
    print("== copy assets =="); copy_assets()
    print("== build unit pages =="); build_pages()
    print("== build gallery =="); build_gallery()
    print("== DONE ==")
