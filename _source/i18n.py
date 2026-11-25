# Post-traitement multilingue : génère /en/, /de/, /nl/ à partir des pages FR de dist/
# Dictionnaires : i18n/<lang>.json  { "texte FR": "traduction" }
# Une page n'est publiée dans une langue que si >= SEUIL de son texte est traduit.
import json, re, posixpath, html, pathlib, sys, urllib.parse, collections

ROOT = pathlib.Path(__file__).parent
D = ROOT / "dist"
SITE = "https://www.od3d.be/"
LANGS = {"en": ("English", "en_GB"), "de": ("Deutsch", "de_BE"), "nl": ("Nederlands", "nl_BE")}
ALL = [("fr", "FR", "Français")] + [(l, l.upper(), n) for l, (n, _) in LANGS.items()]
SEUIL = 0.97
HAS_LETTER = re.compile(r"[A-Za-zÀ-ÿ]")
SCRIPT = re.compile(r"(<(script|style)\b[\s\S]*?</\2>)")
TEXT = re.compile(r">([^<>]+)<")
ATTR = re.compile(r'\b(alt|placeholder|aria-label|title|data-label)="([^"]*)"')
META = re.compile(r'(<meta (?:name="description"|property="og:(?:title|description)") content=")([^"]*)(")')

def key(s): return " ".join(html.unescape(s).split())

def strings(t):
    t = SCRIPT.sub("", t)
    out = [key(s) for s in TEXT.findall(t)] + [key(v) for _, v in ATTR.findall(t)] + [key(m[1]) for m in META.findall(t)]
    return [s for s in out if len(s) > 1 and HAS_LETTER.search(s)]

def pages():
    for f in sorted(D.rglob("index.html")):
        rel = f.parent.relative_to(D).as_posix()
        rel = "" if rel == "." else rel
        if rel.split("/")[0] in LANGS: continue
        yield rel, f

def load(lang):
    p = ROOT / "i18n" / f"{lang}.json"
    return {key(k): v for k, v in json.load(open(p, encoding="utf-8")).items()} if p.exists() else {}

def tr_text(s, dic):
    k = key(s)
    if not k or not HAS_LETTER.search(k) or k not in dic: return s
    lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
    return lead + html.escape(dic[k], quote=False) + trail

RICH = re.compile(r"(<(p|h1|h2|h3|li|span|a)\b[^>]*>)((?:[^<]|<(?:strong|b|em|i|br|span)\b[^>]*>|</(?:strong|b|em|i|span)>)*?)(</\2>)")
def translate(t, dic):
    t = RICH.sub(lambda m: m.group(1) + dic["§" + key(m.group(3))] + m.group(4) if ("§" + key(m.group(3))) in dic else m.group(0), t)
    pieces = re.split(r"(<(?:script|style)\b[\s\S]*?</(?:script|style)>)", t)
    for i in range(0, len(pieces), 2):
        seg = pieces[i]
        seg = TEXT.sub(lambda m: ">" + tr_text(m.group(1), dic) + "<", seg)
        seg = ATTR.sub(lambda m: f'{m.group(1)}="{html.escape(dic.get(key(m.group(2)), html.unescape(m.group(2))))}"', seg)
        seg = META.sub(lambda m: m.group(1) + html.escape(dic.get(key(m.group(2)), html.unescape(m.group(2)))) + m.group(3), seg)
        pieces[i] = seg
    return "".join(pieces)

def url_of(lang, rel):
    return SITE + (f"{lang}/" if lang != "fr" else "") + urllib.parse.quote(rel)

def main():
    dics = {l: load(l) for l in LANGS}
    src = {rel: f.read_text(encoding="utf-8") for rel, f in pages()}
    done = collections.defaultdict(set)
    for l, dic in dics.items():
        for rel, t in src.items():
            ss = strings(t); tot = sum(map(len, ss)) or 1
            ok = sum(len(s) for s in ss if s in dic)
            if ok / tot >= SEUIL: done[l].add(rel)
    avail = lambda rel: [l for l in LANGS if rel in done[l]]

    def switcher(cur, rel, depth):
        # depth = profondeur du fichier dans dist (préfixe langue compris)
        up = "../" * depth
        items = []
        for l, code, name in ALL:
            if l == "fr": href = up + (urllib.parse.quote(rel) + "/" if rel else "")
            elif rel in done[l]: href = up + f"{l}/" + (urllib.parse.quote(rel) + "/" if rel else "")
            elif "" in done[l]: href = up + f"{l}/"
            else: href = up + (urllib.parse.quote(rel) + "/" if rel else "")
            cls = ' aria-current="true"' if l == cur else ""
            items.append(f'<a href="{href}" hreflang="{l}" lang="{l}"{cls}><b>{code}</b> {name}</a>')
        return (f'<details class="lang-sw"><summary aria-label="Langue / Language"><span>{cur.upper()}</span></summary>'
                f'<div class="lang-pop">{"".join(items)}</div></details>')

    def alternates(rel):
        ls = ["fr"] + avail(rel)
        if len(ls) == 1: return ""
        h = "".join(f'<link rel="alternate" hreflang="{l}" href="{url_of(l, rel)}">' for l in ls)
        return h + f'<link rel="alternate" hreflang="x-default" href="{url_of("fr", rel)}">'

    def inject(t, cur, rel, depth):
        t = t.replace('<div class="top-actions">', '<div class="top-actions">' + switcher(cur, rel, depth), 1)
        t = t.replace("</head>", alternates(rel) + "</head>", 1)
        return t

    # FR : on ajoute le sélecteur + hreflang
    for rel, t in src.items():
        depth = len(rel.split("/")) if rel else 0
        (D / rel / "index.html").write_text(inject(t, "fr", rel, depth), encoding="utf-8")

    # Langues
    for l, dic in dics.items():
        for rel in done[l]:
            t = src[rel]
            depth_fr = len(rel.split("/")) if rel else 0
            base = pathlib.PurePosixPath("/" + rel + "/") if rel else pathlib.PurePosixPath("/")

            def fix(m):
                attr, u = m.group(1), m.group(2)
                if re.match(r"(https?:|mailto:|tel:|data:|javascript:|#)", u) or u.startswith("/"): return m.group(0)
                parts = u.split()
                p = parts[0]; path, _, frag = p.partition("#")
                tgt = urllib.parse.unquote(path)
                full = (pathlib.PurePosixPath(str(base)) / tgt).as_posix()
                full = posixpath.normpath(full).lstrip("/")
                full = "" if full == "." else full
                is_page = (D / full / "index.html").exists() if full else True
                if is_page and full in done[l] and (not path or path.endswith("/") or path in ("..", ".")):
                    newp = p
                else:
                    newp = "../" + p
                parts[0] = newp
                return f'{attr}="{" ".join(parts)}"'

            out = re.sub(r'\b(href|src|data-full|poster)="([^"]*)"', fix, t)
            out = re.sub(r'\bsrcset="([^"]*)"', lambda m: 'srcset="' + ", ".join(
                ("../" + x.strip() if not re.match(r"(https?:|data:|/)", x.strip()) else x.strip()) for x in m.group(1).split(",")) + '"', out)
            out = translate(out, dic)
            out = out.replace('<html lang="fr"', f'<html lang="{l}"', 1)
            out = out.replace('content="fr_BE"', f'content="{LANGS[l][1]}"')
            out = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url_of(l, rel), out, count=1)
            out = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url_of(l, rel), out, count=1)
            out = inject(out, l, rel, depth_fr + 1)
            dst = D / l / rel / "index.html"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(out, encoding="utf-8")

    # sitemap
    sm = D / "sitemap.xml"
    if sm.exists():
        extra = "".join(f"<url><loc>{url_of(l, rel)}</loc></url>" for l in LANGS for rel in sorted(done[l]))
        sm.write_text(sm.read_text(encoding="utf-8").replace("</urlset>", extra + "</urlset>"), encoding="utf-8")

    for l in LANGS: print(l, len(done[l]), "pages /", len(src))

if __name__ == "__main__":
    if "--missing" in sys.argv:
        # liste les chaînes manquantes pour des pages données : python3 i18n.py --missing en page1 page2 ...
        l = sys.argv[2]; dic = load(l); want = sys.argv[3:]
        seen = []
        for rel, f in pages():
            if want and rel not in want: continue
            for s in strings(f.read_text(encoding="utf-8")):
                if s not in dic and s not in seen: seen.append(s)
        print(json.dumps(seen, ensure_ascii=False, indent=0))
    else:
        main()
