#!/bin/bash
# 단원 검증: srv 재구성 → 새 포트 서버 → 콘솔 0 (u/g/p/d/index) → 하네스(flow, reduced-motion 스크롤/모션 분기) → 스크린샷
# 사용: bash run_unit.sh <N> [port]
set -u
N=${1:?unit}; PORT=${2:-8571}
S="/c/Users/admin/AppData/Local/Temp/claude/C--Kids-math-story-telling/0804986b-c22c-428e-9e94-ad94a24ef9f9/scratchpad"
R="/c/Kids/math-story-telling"
C="/c/Program Files/Google/Chrome/Application/chrome.exe"
rm -rf "$S/srv" "$S/out"; mkdir -p "$S/srv/mid3/print" "$S/out"
cp "$R"/40_grades/middle/math3/app3/*.{html,js,css} "$S/srv/mid3/"
cp "$R"/40_grades/middle/math3/print/index.html "$S/srv/mid3/print/"
cp "$S/_h.html" "$S/srv/mid3/_h.html"
cd "$S" || exit 1
python -m http.server $PORT --bind 127.0.0.1 --directory "$S/srv" > "$S/out/server.log" 2>&1 &
SPID=$!
python -c "import time;time.sleep(1.2)"
B="http://127.0.0.1:$PORT/mid3"
run(){ # name url budget extra...
  local name=$1 url=$2 budget=$3; shift 3
  rm -rf "$S/prof_$name"
  "$C" --headless --disable-gpu --no-sandbox --disable-extensions --user-data-dir="$S/prof_$name" \
       --enable-logging=stderr --v=0 --virtual-time-budget=$budget --window-size=1000,1400 "$@" \
       "$url" > "$S/out/$name.html" 2> "$S/out/$name.err"
  echo "== $name: console=$(grep -c CONSOLE "$S/out/$name.err") dom=$(wc -c < "$S/out/$name.html")"
  grep CONSOLE "$S/out/$name.err" | head -5
}
for k in u g p d; do run "$k$N" "$B/$k$N.html" 3000 --dump-dom; done
run index "$B/index.html" 3000 --dump-dom
run print "$B/print/index.html" 3000 --dump-dom
if [ "${HARNESS:-1}" = "1" ]; then
  run h_flow "$B/_h.html#flow" 30000 --dump-dom --force-prefers-reduced-motion
  run h_stamp "$B/_h.html#stamp" 8000 --dump-dom
  run h_retry "$B/_h.html#retry" 6000 --dump-dom
  for n in h_flow h_stamp h_retry; do
    echo "---- $n"; PYTHONIOENCODING=utf-8 python -c "import re,html,sys;t=open(sys.argv[1],encoding='utf-8').read();m=re.search(r'<div id=\"log\">(.*?)</div>',t,re.S);sys.stdout.buffer.write((html.unescape(m.group(1)) if m else 'NO LOG').encode('utf-8'))" "$S/out/$n.html"; echo
  done
fi
# 스크린샷: u(상단), p(상단), stamp 상태
shot(){ local name=$1 url=$2 h=$3; shift 3; rm -rf "$S/prof_s_$name"
  "$C" --headless --disable-gpu --no-sandbox --disable-extensions --user-data-dir="$S/prof_s_$name" --enable-logging=stderr --v=0 \
       --virtual-time-budget=5000 --window-size=1000,$h "$@" --screenshot="$S/out/$name.png" "$url" 2>/dev/null; }
shot "u$N" "$B/u$N.html" 1500
shot "p$N" "$B/p$N.html" 1500
shot "g$N" "$B/g$N.html" 1500
shot "d$N" "$B/d$N.html" 1700
if [ "${HARNESS:-1}" = "1" ]; then shot stamp "$B/_h.html?tall=1#stamp" 4400; fi
kill $SPID 2>/dev/null
echo "server non-200:"; grep -v " 200 " "$S/out/server.log" | grep GET | grep -v favicon | head
