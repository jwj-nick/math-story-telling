import re, sys, pathlib
# concept.css/js?v= 캐시버전을 한 값으로 통일 (바이트 단위, 줄끝 보존)
root = pathlib.Path(sys.argv[1]); ver = sys.argv[2].encode()
pat = re.compile(rb'concept\.(css|js)\?v=[0-9a-z]*')
changed = 0; seen = set()
for f in sorted(root.glob('*.html')):
    b = f.read_bytes()
    nb = pat.sub(lambda m: b'concept.' + m.group(1) + b'?v=' + ver, b)
    if nb != b:
        f.write_bytes(nb); changed += 1
    for m in pat.finditer(nb): seen.add(m.group(0).decode())
print('changed', changed, 'files; versions now:', sorted(seen))
