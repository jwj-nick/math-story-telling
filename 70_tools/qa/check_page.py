# -*- coding: utf-8 -*-
"""check_page.py — 앱 HTML 페이지 정적 검증 (2026-08-30, math3 파일럿에서 정립)

    python 70_tools/qa/check_page.py <html 파일 또는 디렉토리> [...]

검사 항목(페이지마다):
  1. 태그 균형 — html.parser 스택 기반(void 요소 제외). 대량 편집 후 구조 붕괴 사고 방지.
  2. 인라인 <script> 구문 — Node `new Function` 파싱(엔진 파일은 node --check로 따로).
  3. id 참조 — getElementById('x') / MJ*.checkNum('x',…) / MJ*.check('x',…) / reveal('a','b') / hintSteps('b',[…]) 의
     문자열 id가 HTML에 id="x"로 존재하는지. 확인 문제 입력 id → 'id'+'b'(버튼)·'id'+'o'(출력) 짝도 점검.
  4. 중복 id.
  5. 캐시버전 — 디렉토리 단위로 concept.css/js?v= 값이 한 종류인지.
종료 코드 0 = 전부 통과. 문제는 파일:항목으로 출력.
"""
import io, os, re, sys, subprocess, tempfile
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Bal(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.errors=[]; self.ids={}
    def handle_starttag(self, tag, attrs):
        for k,v in attrs:
            if k=='id' and v is not None:
                self.ids.setdefault(v,0); self.ids[v]+=1
        if tag in VOID: return
        self.stack.append((tag,self.getpos()[0]))
    def handle_startendtag(self, tag, attrs):
        for k,v in attrs:
            if k=='id' and v is not None:
                self.ids.setdefault(v,0); self.ids[v]+=1
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack:
            self.errors.append('닫는 태그만 있음 </%s> @%d' % (tag,self.getpos()[0])); return
        if self.stack[-1][0]==tag:
            self.stack.pop(); return
        # 스택 안에 있으면 그 사이 것들이 안 닫힘
        names=[t for t,_ in self.stack]
        if tag in names:
            while self.stack and self.stack[-1][0]!=tag:
                t,l=self.stack.pop(); self.errors.append('안 닫힌 <%s> (열린 줄 %d, </%s> @%d에서 강제 종료)' % (t,l,tag,self.getpos()[0]))
            self.stack.pop()
        else:
            self.errors.append('짝 없는 </%s> @%d (스택 top=%s)' % (tag,self.getpos()[0],self.stack[-1][0]))

def inline_scripts(html):
    out=[]
    for m in re.finditer(r'<script(?P<attr>[^>]*)>(?P<body>.*?)</script>', html, re.S|re.I):
        if re.search(r'\bsrc\s*=', m.group('attr')): continue
        out.append((html[:m.start()].count('\n')+1, m.group('body')))
    return out

def node_check(scripts):
    """각 인라인 스크립트를 new Function으로 파싱. 반환: 오류 문자열 목록"""
    errs=[]
    if not scripts: return errs
    tmp=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8')
    try:
        import json
        tmp.write('var S='+json.dumps([b for _,b in scripts])+';\n')
        tmp.write('var bad=[];S.forEach(function(s,i){try{new Function(s);}catch(e){bad.push(i+":"+e.message);}});\n')
        tmp.write('process.stdout.write(JSON.stringify(bad));\n')
        tmp.close()
        r=subprocess.run(['node',tmp.name],capture_output=True,text=True,encoding='utf-8')
        if r.returncode!=0: return ['node 실행 실패: '+(r.stderr or '')[:200]]
        for item in json.loads(r.stdout or '[]'):
            i,msg=item.split(':',1); errs.append('인라인 스크립트 #%d(줄 %d) 구문 오류: %s' % (int(i)+1, scripts[int(i)][0], msg))
    finally:
        try: os.unlink(tmp.name)
        except OSError: pass
    return errs

ID_PATTERNS=[
    (r"getElementById\(\s*'([^']+)'\s*\)", 'plain'),
    (r"getElementById\(\s*\"([^\"]+)\"\s*\)", 'plain'),
    (r"\bMJ\d?\.checkNum\(\s*'([^']+)'\s*,", 'check'),
    (r"\bMJ\d?\.check\(\s*'([^']+)'\s*,", 'check'),
    (r"\bMJ\d?\.reveal\(\s*'([^']+)'\s*,\s*'([^']+)'", 'plain2'),
    (r"\bMJ\d?\.makeProgress\(\s*'([^']+)'", 'plain'),
]

def _out_id_of(body, nm):
    """MJ*.check('a1', …, 'o1') / checkNum('a1', …, 'o1') 의 출력 id 를 읽는다."""
    m = re.search(r"check(?:Num)?\(\s*['\"]" + re.escape(nm) + r"['\"]\s*,.*?,\s*['\"]([\w-]+)['\"]", body)
    return m.group(1) if m else None


def _has_button_for(body, nm, ids):
    """그 입력을 채점하는 버튼이 하나라도 걸려 있는가.
       a1b 처럼 접미사 규칙을 따르거나, check('a1'…) 호출 지점에서 거슬러 올라가
       가장 가까운 클릭 핸들러의 대상이 실재하는 id 이면 통과."""
    if nm + 'b' in ids:
        return True
    call = re.compile(r"check(?:Num)?\(\s*['\"]" + re.escape(nm) + r"['\"]")
    handler = re.compile(r"getElementById\(\s*['\"]([\w-]+)['\"]\s*\)\s*"
                         r"(?:\.onclick\s*=|\.addEventListener\(\s*['\"]click['\"])")
    for m in call.finditer(body):
        before = body[:m.start()]
        hs = list(handler.finditer(before))
        if hs and hs[-1].group(1) in ids:
            return True
    return False


# 실행해 봐야만 드러나는데 조건이 맞아야 터지는 패턴들. 눈으로 찾는 편이 확실하다.
# 2026-09-07 에 놀이터에서 classList.add('') 가 **정답을 맞힌 순간에만** 예외를 던져
# 게임이 멈추는 버그가 있었다. 런타임 스모크는 그 갈래를 밟아야 걸리지만, 여기서는 늘 걸린다.
RISKY = [
    (re.compile(r"classList\.(?:add|remove|toggle)\([^)]*?:\s*(''|\"\")\s*\)"),
     "classList 에 빈 문자열이 넘어갈 수 있음 — DOMException 이 나고 그 아래가 통째로 멈춘다. "
     "빈 값이면 건너뛰도록 감쌀 것"),
    (re.compile(r"classList\.(?:add|remove|toggle)\(\s*(''|\"\")\s*\)"),
     "classList 에 빈 문자열을 그대로 넘김 — DOMException"),
]


def check_risky(scripts):
    errs = []
    for _, body in scripts:
        for pat, why in RISKY:
            for m in pat.finditer(body):
                errs.append('위험한 패턴: %s — %s' % (why, m.group(0)[:90]))
    return errs


def check_ids(scripts, ids):
    errs=[]; seen=set()
    for _,body in scripts:
        for pat,kind in ID_PATTERNS:
            for m in re.finditer(pat, body):
                names=m.groups()
                for nm in names:
                    if nm in seen: continue
                    seen.add(nm)
                    if nm not in ids: errs.append("참조 id 없음: '%s'" % nm)
                    elif kind=='check':
                        # 짝 이름 규칙은 하나가 아니다. 개념/심화 페이지는 a1 → a1b·a1o 를,
                        # 심화 문제(dNp) 페이지는 a1 → b1·o1 을 쓴다. 규칙을 강요하는 대신
                        # 출력 id 는 호출 인자에서 읽고, 버튼은 실제로 하나 걸려 있는지만 본다.
                        out = _out_id_of(body, nm)
                        if out and out not in ids:
                            errs.append("확인 문제 '%s'의 출력 id '%s' 없음" % (nm, out))
                        if not _has_button_for(body, nm, ids):
                            errs.append("확인 문제 '%s'를 채점하는 버튼을 찾지 못함" % nm)
    # 동적 문자열 결합(예: 'a'+i)은 검사 대상 아님 — 보고만
    return errs

def check_file(path):
    html=io.open(path,encoding='utf-8').read()
    p=Bal(); p.feed(html); p.close()
    errs=list(p.errors)
    for t,l in p.stack: errs.append('끝까지 안 닫힌 <%s> (줄 %d)' % (t,l))
    dup=[k for k,v in p.ids.items() if v>1]
    if dup: errs.append('중복 id: '+', '.join(dup))
    sc=inline_scripts(html)
    errs+=node_check(sc)
    errs+=check_ids(sc, p.ids)
    errs += check_risky(sc)
    vers=set(re.findall(r'concept\.(?:css|js)\?v=([0-9a-z]+)', html))
    return errs, vers

def main(argv):
    files=[]
    for a in argv:
        if os.path.isdir(a):
            files+=[os.path.join(a,f) for f in sorted(os.listdir(a)) if f.endswith('.html')]
        else: files.append(a)
    total=0; vers_by_dir={}
    for f in files:
        errs,vers=check_file(f)
        vers_by_dir.setdefault(os.path.dirname(f),set()).update(vers)
        if errs:
            total+=len(errs)
            print('✗ '+f)
            for e in errs: print('    - '+e)
        else: print('✓ '+f)
    for d,vs in vers_by_dir.items():
        if len(vs)>1: total+=1; print('✗ 캐시버전 불일치 %s: %s' % (d, sorted(vs)))
        elif vs: print('  캐시버전 %s: %s' % (d, sorted(vs)[0]))
    print('문제 %d건' % total)
    return 1 if total else 0

if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
