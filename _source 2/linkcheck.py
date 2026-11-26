import re, pathlib, urllib.parse, sys
D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dist"); bad = []
for f in D.rglob("*.html"):
    if f.name == "404.html": continue
    for u in re.findall(r'(?:href|src|srcset)="([^"#]+)', f.read_text()):
        u = u.split()[0]
        if re.match(r"(https?:|mailto:|tel:|data:|javascript:)", u) or "'+" in u: continue
        t = (f.parent / urllib.parse.unquote(u.split("?")[0])).resolve()
        if t.is_dir(): t = t / "index.html"
        if not t.exists(): bad.append((str(f.relative_to(D)), u))
print(len(bad)); [print(b) for b in bad[:15]]
