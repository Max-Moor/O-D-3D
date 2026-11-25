"""Génère le site O&D (design futuriste) avec la même arborescence d'URL que od3d.be.
Usage : python3 build.py [--prod]   (--prod = indexable, sans bandeau maquette)"""
import json, re, sys, shutil, html, pathlib, urllib.parse
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "dist"
STATIC = ROOT / "static" if (ROOT / "static").exists() else ROOT.parent / "static"
PROD = "--prod" in sys.argv
BASE = "/" if PROD else "/O-D-3D/"
SITE = "https://www.od3d.be"
E = html.escape

P = json.load(open(ROOT / "content/pages.json", encoding="utf-8"))
P = [p for p in P if p["path"] not in ("donate", "donation-thank-you-page")]
BY = {p["path"]: p for p in P}
MEDIA = json.load(open(ROOT / "content/media.json", encoding="utf-8"))
IMG = MEDIA["img"]; LOGOS = MEDIA["logos"]
def pic(depth, path, alt, cls="", lazy=True):
    if path not in IMG: return ""
    base, (w, h) = IMG[path]; pre = "../" * depth
    return (f'<picture class="{cls}"><source srcset="{pre}{base}.webp" type="image/webp"><img src="{pre}{base}.png" alt="{E(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + '></picture>')

MACHINES = ["supermaker-sls1518", "supermaker-sls3540-pro", "bambu-lab-h2c", "bambu-lab-x1c", "modix-big-meter", "prusa-core-one",
            "intamsys-funmat-ht", "anycubic-photon-m7-max", "tooldance-x1-cnc", "xtool-f1", "scanner-3devok-mt"]
def kids(prefix): return [p for p in P if p["path"].startswith(prefix + "/")]
SERVICES = kids("services")
MACH = [BY["machines-materiaux/" + m] for m in MACHINES if "machines-materiaux/" + m in BY]
MATS = [p for p in kids("machines-materiaux") if p not in MACH]
COMP = kids("comparateur-materiaux")
ZONES = kids("a-propos")
REAL = kids("réalisations")
POSTS = [p for p in P if p.get("blog")]

def label(p):
    t = p["title"].split(" | ")[0]
    t = re.sub(r"^(Impression 3D|Filament)\s+", "", t) if p["path"].startswith("machines-materiaux/") else t
    return t.split(" – ")[0].split(" : ")[0].strip()

# ---------------------------------------------------------------- utilitaires
def rel(depth, path):
    pre = "../" * depth
    return (pre or "./") if path in ("", "/") else pre + path.strip("/") + "/"
ICON = {
 "home": '<path d="M3 11l9-7 9 7v9H4z"/><path d="M10 20v-6h4v6"/>',
 "serv": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
 "mach": '<path d="M4 20h16M6 20V8h12v12M9 8V4h6v4"/><path d="M12 12v4"/>',
 "comp": '<path d="M12 3v18M5 7h14M5 7l-3 7h6zM19 7l-3 7h6z"/>',
 "real": '<path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/>',
 "about": '<circle cx="12" cy="10" r="3"/><path d="M12 21s-7-6.5-7-11a7 7 0 0114 0c0 4.5-7 11-7 11z"/>',
 "blog": '<path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h8M8 17h5"/>',
 "mail": '<path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/>',
}
RAIL = [("", "Accueil", "home"), ("services", "Services", "serv"), ("machines-materiaux", "Parc", "mach"), ("comparateur-materiaux", "Comparer", "comp"),
        ("réalisations", "Projets", "real"), ("a-propos", "À propos", "about"), ("actualites", "Blog", "blog"), ("contact", "Contact", "mail")]

def section_of(path):
    first = path.split("/")[0]
    return "actualites" if first == "post" else first

def head(p, depth, title, desc, extra_ld=()):
    url = SITE + "/" + (p.strip("/") + ("/" if p else "")) if False else SITE + ("/" + urllib.parse.quote(p) if p else "/")
    ld = [{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#od3d", "name": "O&D Impression 3D", "url": SITE + "/",
           "logo": SITE + "/static/img/icon-512.png", "foundingDate": "2021",
           "address": {"@type": "PostalAddress", "streetAddress": "Rue Trois Bourdons 52E", "postalCode": "4840", "addressLocality": "Welkenraedt", "addressRegion": "Liège", "addressCountry": "BE"}}]
    if p:
        parts = p.split("/"); items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"}]
        for i in range(len(parts)):
            sub = "/".join(parts[:i + 1]); pp = BY.get(sub)
            items.append({"@type": "ListItem", "position": i + 2, "name": label(pp) if pp else parts[i], "item": SITE + "/" + urllib.parse.quote(sub)})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    ld += list(extra_ld)
    pre = "../" * depth
    robots = "index, follow" if PROD else "noindex, nofollow"
    return f'''<!DOCTYPE html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="O&amp;D Impression 3D">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/static/img/og-image.jpg"><meta property="og:locale" content="fr_BE">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#020407">
<link rel="icon" href="{pre}static/img/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{pre}static/img/apple-touch-icon.png">
<link rel="preload" href="{pre}static/fonts/chakra-petch-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}static/css/od3d.css">
{chr(10).join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)}
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<div class="bgfx" aria-hidden="true"></div>
'''

def chrome(p, depth):
    cur = section_of(p)
    rail = "".join(f'<a href="{rel(depth, h)}"{" aria-current=\"page\"" if cur == h else ""}><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5">{ICON[i]}</svg>{t}</a>' for h, t, i in RAIL)
    def col(t, hub, items):
        lis = "".join(f'<li><a href="{rel(depth, x["path"])}">{E(label(x))}</a></li>' for x in items)
        return f'<div><h2 class="h4"><a href="{rel(depth, hub)}">{t} →</a></h2><ul>{lis}</ul></div>'
    over = f'''<div class="overlay" id="menu"><div class="cols">
{col("Services", "services", SERVICES)}
<div>{col("Machines", "machines-materiaux", MACH)[5:-6]}{col("Comparatifs", "comparateur-materiaux", COMP)[5:-6]}</div>
{col("Matériaux", "machines-materiaux", MATS)}
{col("Réalisations", "réalisations", REAL)}
<div>{col("À propos & zones", "a-propos", ZONES)[5:-6]}<h2 class="h4"><a href="{rel(depth,"technologies-materiaux-impression-3d")}">Guide matériaux →</a></h2><h2 class="h4"><a href="{rel(depth,"quiz-technologie-impression-3d")}">Quiz technologie →</a></h2><h2 class="h4"><a href="{rel(depth,"devis-instantane")}">Devis instantané →</a></h2></div>
<div><h2 class="h4"><a href="{rel(depth,"actualites")}">Blog →</a></h2><h2 class="h4"><a href="{rel(depth,"faq")}">FAQ →</a></h2><h2 class="h4"><a href="{rel(depth,"contact")}">Contact →</a></h2></div>
</div></div>'''
    pre = "../" * depth
    mock = "" if PROD else '<div class="mock">Maquette · non officielle</div>'
    return f'''<aside class="rail"><a class="logo" href="{rel(depth, "")}" aria-label="Accueil O&amp;D Impression 3D"><img src="{pre}static/img/logo-od.png" alt="O&amp;D" width="60" height="32"></a><nav aria-label="Navigation principale">{rail}</nav><div class="coord">50.65°N · 5.97°E — WELKENRAEDT</div></aside>
<header class="top"><a class="brand" href="{rel(depth, "")}"><img src="{pre}static/img/logo-od.png" alt="O&amp;D" width="56" height="30"><span>Impression 3D</span></a>
<div class="status"><b>Atelier en ligne</b><span>SLS · FDM · SLA · CNC · Scan 3D</span><span>Depuis 2021</span></div>
<div class="top-actions"><a class="btn btn-p" href="{rel(depth, "devis-instantane")}">Devis instantané <span class="a">→</span></a><button class="menu-btn" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><i></i></button></div></header>
{over}{mock}
<main id="main">
'''

def footer(depth):
    pre = "../" * depth
    def ul(items): return "".join(f'<li><a href="{rel(depth, x["path"])}">{E(label(x))}</a></li>' for x in items)
    return f'''</main>
<footer class="foot"><div class="wrap">
<div class="big"><div><img src="{pre}static/img/logo-od-large.png" alt="O&amp;D Impression 3D" width="180" height="97" loading="lazy"><p style="margin-top:1rem">Fabrication additive et usinage pour l'industrie. Rue Trois Bourdons 52E, 4840 Welkenraedt, Belgique. Depuis 2021.</p></div>
<div class="map"><div><h2 class="h4">Services</h2><ul>{ul(SERVICES)}</ul></div><div><h2 class="h4">Machines</h2><ul>{ul(MACH)}</ul><h2 class="h4" style="margin-top:1.4rem">Comparatifs</h2><ul>{ul(COMP)}</ul></div>
<div><h2 class="h4">Matériaux</h2><ul>{ul(MATS)}</ul></div><div><h2 class="h4">Réalisations</h2><ul>{ul(REAL)}</ul><h2 class="h4" style="margin-top:1.4rem">Zones</h2><ul>{ul(ZONES)}</ul></div></div></div>
<div class="base"><span>© <span data-year>2026</span> O&amp;D Impression 3D</span><span><a href="{rel(depth,"mentions-légales")}">Mentions légales</a> · <a href="{rel(depth,"politique-de-confidentialité")}">Confidentialité</a> · <a href="{rel(depth,"politique-de-cookies")}">Cookies</a> · <a href="{rel(depth,"faq")}">FAQ</a></span></div>
</div></footer>
<div class="dock"><a class="btn btn-p" href="{rel(depth, "devis-instantane")}">Devis instantané <span class="a">→</span></a></div>
<script src="{pre}static/js/od3d.js" defer></script>
</body></html>
'''

def crumbs(p, depth):
    parts = p.split("/"); out = [f'<a href="{rel(depth, "")}">Accueil</a>']
    for i in range(len(parts)):
        sub = "/".join(parts[:i + 1]); pp = BY.get(sub)
        name = "Blog" if sub == "post" else (label(pp) if pp else parts[i])
        href = rel(depth, "actualites" if sub == "post" else sub)
        out.append(f'<a href="{href}">{E(name)}</a>' if i < len(parts) - 1 else f'<span>{E(name)}</span>')
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">' + " <i>/</i> ".join(out) + "</nav>"

def cta(depth, title="Votre pièce, <span class='glow'>fabriquée.</span>", text="Envoyez votre fichier 3D ou décrivez votre besoin : devis instantané avec fichier, devis personnalisé sous 24 h."):
    return f'''<section style="padding-top:20px"><div class="wrap"><div class="panel hot cta rv"><div><div class="hud eyebrow">Prochaine étape</div><h2>{title}</h2><p class="lead" style="margin:0">{text}</p></div>
<div class="cta-row" style="flex-direction:column"><a class="btn btn-p" href="{rel(depth,"devis-instantane")}">Devis instantané <span class="a">→</span></a><a class="btn btn-g" href="{rel(depth,"contact")}">Demande personnalisée <span class="a">→</span></a></div></div></div></section>'''

# ---------------------------------------------------------------- rendu générique
DROP = re.compile(r"^(Autres articles|Plus de détails|Lire plus|En savoir plus|O&D Impression 3D ·.*|O&D 3D|Contactez-nous|Demander un devis|Lancer mon projet|Voir .*)$", re.I)
CTA_SEC = re.compile(r"(parlons-en|un projet \?|passez à l'action|demandez votre devis|prêt à|contactez-nous)", re.I)
LABEL = re.compile(r"^(Matériaux disponibles|Avantages( & limites)?|Limites|Inconvénients|Points forts|Points faibles|Idéal pour|À éviter|Applications?|Cas d'usage.*|Usages?|Points clés|Atouts?)$", re.I)
NEG = re.compile(r"^(Limites|Inconvénients|Points faibles|À éviter)$", re.I)

def is_item(t): return len(t) < 75 and not t.endswith((".", ":", "?")) or (len(t) < 75 and t.count(" ") < 9)

ORPHAN = re.compile(r"^(Styles nécessaires.*|STYLES NÉCESSAIRES.*|Besoin d.aide pour choisir.*|BESOIN D.AIDE POUR CHOISIR.*|\d{1,2}|0\d|GROUPE\s*\d.*|STEP\s*\d.*|HEADER|FOOTER|SPECS|SELECTOR|HERO|RÉALISATION\s*\d+|/\w+|\d+ — [A-ZÉ0-9 ]+|LIGNE|Structure HTML.*|ESPACE DESTINÉ.*|.*injectés par JS.*|VS|CTA|POPULAR COMBOS|Choisissez vos deux matériaux|Comparaisons populaires|PROS / CONS|cube|gear|bolt|layers|```.*|.*id=\"[a-z0-9]+\".*)$", re.I)
KVTAIL = re.compile(r"^(.{1,40}?) (Matériaux?|Quantité|Client|Format|Secteur|Méthode|Dimensions|Délai|Durée|Technologie|Finition|Pièces)$")
TEXTFIX = [("FDM vs SLS vs Résine", "FDM vs SLS vs SLA"), ("O&D Impression 3D a Baelen", "O&D Impression 3D à Welkenraedt"), ("à Baelen", "à Welkenraedt"), (" a Baelen", " à Welkenraedt"), ("Usinage CNC — Makera Carvera", "Usinage CNC"), ("Notre Makera Carvera permet", "Notre fraiseuse CNC permet"), ("Makera Carvera", "fraiseuse CNC"), ("Carvera", "fraiseuse CNC")]
def _fix(v):
    if isinstance(v, str):
        for a, b in TEXTFIX: v = v.replace(a, b)
    elif isinstance(v, list): v = [_fix(x) for x in v]
    return v
def short(s, n=150):
    s = s or ""
    if len(s) <= n: return s
    c = s[:n].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return c + "…"
def normalize(blocks, page_h1=None):
    conv = []
    blocks = [{k: _fix(x) for k, x in b.items()} for b in blocks]
    for b in blocks:
        if b["t"] == "txt" and KVTAIL.match(b["v"]):
            v, k = KVTAIL.match(b["v"]).groups(); conv.append({"t": "kv", "k": k, "v": v})
        else: conv.append(b)
    blocks = [dict(b, v=re.sub(r"^/[a-z]+\s+", "", b["v"])) if isinstance(b.get("v"), str) else b for b in conv]
    # étiquettes en double (« Conception » à côté de « … : CONCEPTION »)
    keep = []
    for i, b in enumerate(blocks):
        if b["t"] == "txt" and len(b["v"]) < 30:
            near = [x.get("v", "") for x in blocks[max(0, i - 3):i + 4] if x is not b and isinstance(x.get("v"), str)]
            if any(b["v"].casefold() != n.casefold() and b["v"].casefold() in n.casefold() and len(n) < 40 for n in near): continue
        keep.append(b)
    blocks = [b for b in keep if not (b["t"] in ("txt", "p", "h2", "h3") and isinstance(b.get("v"), str) and ORPHAN.match(b["v"]))]
    out = []
    for b in blocks:
        v = b.get("v")
        if b["t"] == "link": continue
        if b["t"] == "kv" and b["k"] == b["v"]: continue
        if isinstance(v, str) and DROP.match(v): continue
        if b["t"] in ("txt", "p") and v and v.startswith("© "): continue
        out.append(dict(b))
    return out

def build_model(p):
    blocks = normalize(p["native"] + p["embed"])
    title = None; eyebrow = None; lead = None; stats = []; i = 0
    # hero
    toks = {w.lower() for w in re.findall(r"[\wÀ-ÿ]{3,}", label(p) + " " + p["path"].replace("-", " "))}
    for j, b in enumerate(blocks[:14]):
        if b["t"] == "h1":
            if toks & {w.lower() for w in re.findall(r"[\wÀ-ÿ]{3,}", b["v"])}:
                title = b["v"]; i = j + 1
                if j and blocks[j - 1]["t"] == "txt": eyebrow = blocks[j - 1]["v"]
            break
    if not title:
        title = label(p)
    while i < len(blocks) and blocks[i]["t"] in ("p", "txt") and not lead:
        if len(blocks[i]["v"]) > 60: lead = blocks[i]["v"]
        i += 1
    rest = blocks[i:] if lead or title else blocks
    # stats : kv avant le premier h2
    k = 0
    while k < len(rest) and rest[k]["t"] in ("kv", "txt") and len(stats) < 8:
        if rest[k]["t"] == "kv" and len(rest[k]["k"]) < 22: stats.append((rest[k]["k"], rest[k]["v"]))
        elif rest[k]["t"] == "txt" and k + 1 < len(rest) and rest[k + 1]["t"] in ("h2", "h1"): break
        elif rest[k]["t"] == "txt" and len(rest[k]["v"]) < 25 and stats is not None and k + 1 < len(rest) and rest[k+1]["t"] == "txt" and len(rest[k+1]["v"]) < 25:
            stats.append((rest[k]["v"], rest[k + 1]["v"])); k += 1
        else: break
        k += 1
    rest = rest[k:]
    # sections
    secs = []; cur = {"eyebrow": None, "title": None, "items": []}
    def flush():
        if cur["title"] or cur["items"]: secs.append(dict(cur))
    for j, b in enumerate(rest):
        t = b["t"]
        if t in ("h1", "h2"):
            if b["v"] == title or b["v"] in ("​",): continue
            flush()
            eb = None
            if cur["items"] and cur["items"][-1]["t"] == "txt" and len(cur["items"][-1]["v"]) < 40:
                eb = cur["items"].pop()["v"]
                if secs and secs[-1] is not None and not cur["items"]: pass
            cur = {"eyebrow": eb, "title": b["v"], "items": []}
            if secs and secs[-1]["items"] and secs[-1]["items"][-1]["t"] == "txt" and len(secs[-1]["items"][-1]["v"]) < 40 and not eb:
                cur["eyebrow"] = secs[-1]["items"].pop()["v"]
        else:
            cur["items"].append(b)
    flush()
    return {"title": title, "eyebrow": eyebrow, "lead": lead, "stats": stats, "sections": [s for s in secs if not (s["title"] and CTA_SEC.search(s["title"]))]}

PCT = re.compile(r"^\d{1,3}\s?%$")
def _istxt(x, short=60): return x["t"] == "txt" and len(x["v"]) <= short
def try_bars(items, i):
    n = len(items); j = i; title = None
    def pair(k): return k + 1 < n and _istxt(items[k]) and not PCT.match(items[k]["v"]) and _istxt(items[k + 1]) and PCT.match(items[k + 1]["v"])
    if not pair(j):
        if _istxt(items[j]) and pair(j + 1): title = items[j]["v"]; j += 1
        else: return None, i
    rows = []
    while pair(j): rows.append((items[j]["v"], int(re.sub(r"\D", "", items[j + 1]["v"])))); j += 2
    if len(rows) < 3: return None, i
    summ = ""
    if j < n and items[j]["t"] == "p": summ = f'<p style="margin-top:1rem">{E(items[j]["v"])}</p>'; j += 1
    bars = "".join(f'<div class="bar"><span>{E(a)}</span><i><b style="width:{v}%"></b></i><em>{v}%</em></div>' for a, v in rows)
    return f'<div class="panel rv bars">{f"<h3>{E(title)}</h3>" if title else ""}{bars}{summ}</div>', j

def try_tcards(items, i):
    """txt (nom) + p (description) + txt court (étiquette) répétés -> cartes"""
    n = len(items); cards = []; j = i
    while j + 1 < n and _istxt(items[j], 45) and not PCT.match(items[j]["v"]) and items[j + 1]["t"] == "p" and len(items[j + 1]["v"]) > 40:
        tag = None
        if j + 2 < n and _istxt(items[j + 2], 24) and not (j + 3 < n and items[j + 3]["t"] == "p"): tag = items[j + 2]["v"]; k = j + 3
        elif j + 2 < n and _istxt(items[j + 2], 24) and j + 3 < n and items[j + 3]["t"] == "p" and j + 4 < n and _istxt(items[j + 4], 24): tag = items[j + 2]["v"]; k = j + 3
        else: k = j + 2
        cards.append((items[j]["v"], items[j + 1]["v"], tag)); j = k
    if len(cards) < 2: return None, i
    h = "".join(f'<article class="panel spot card rv"><span class="k">{E(tg) if tg else "Fiche"}</span><h3>{E(a)}</h3><p>{E(b)}</p></article>' for a, b, tg in cards)
    return f'<div class="grid {"g3" if len(cards) >= 3 else "g2"}">{h}</div>', j

def render_items(items):
    out = []; i = 0; n = len(items)
    while i < n:
        b = items[i]; t = b["t"]
        if t == "txt":
            group = []
            while i < n:
                h_, j = try_bars(items, i)
                if not h_: break
                group.append(h_); i = j
            if group:
                out.append(f'<div class="grid {"g3" if len(group) >= 3 else "g2" if len(group) == 2 else ""}">' + "".join(group) + "</div>"); continue
            h_, j = try_tcards(items, i)
            if h_: out.append(h_); i = j; continue
        if t in ("h3", "h4") or (t == "txt" and i + 1 < n and items[i + 1]["t"] in ("h3",) and len(b["v"]) < 45):
            cards = []
            while i < n and (items[i]["t"] in ("h3", "h4") or (items[i]["t"] == "txt" and i + 1 < n and items[i + 1]["t"] == "h3" and len(items[i]["v"]) < 45)):
                kick = None
                if items[i]["t"] == "txt": kick = items[i]["v"]; i += 1
                c = {"k": kick, "h": items[i]["v"], "body": [], "chips": [], "list": [], "kv": []}; i += 1
                while i < n and items[i]["t"] in ("p", "txt", "ul", "kv") and not (items[i]["t"] == "txt" and i + 1 < n and items[i + 1]["t"] == "h3" and len(items[i]["v"]) < 45):
                    x = items[i]
                    if x["t"] == "ul": c["list"] += x["v"]
                    elif x["t"] == "kv": c["kv"].append((x["k"], x["v"]))
                    elif x["v"].startswith("✓"): c["chips"] += [s.strip() for s in x["v"].lstrip("✓ ").split("·")]
                    elif x["t"] == "txt" and c["body"] and len(x["v"]) < 70: c["chips"].append(x["v"])
                    else: c["body"].append(x["v"])
                    i += 1
                cards.append(c)
            cls = "g3" if len(cards) >= 3 and len(cards) != 4 else "g2" if len(cards) != 4 else "g4"
            h = []
            for ix, c in enumerate(cards, 1):
                body = "".join(f"<p>{E(x)}</p>" for x in c["body"])
                lst = ('<ul class="list" style="margin-top:.8rem">' + "".join(f"<li>{E(x)}</li>" for x in c["list"]) + "</ul>") if c["list"] else ""
                kv = ('<table class="specs" style="margin-top:.6rem">' + "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in c["kv"]) + "</table>") if c["kv"] else ""
                chips = ('<div class="chips">' + "".join((f'<span class="chip tech">{E(x)}</span>' if x.startswith("→") else f'<span class="chip">{E(x)}</span>') for x in c["chips"] if x) + "</div>") if c["chips"] else ""
                h.append(f'<article class="panel spot card rv"><span class="k">{E(c["k"]) if c["k"] else f"[ {ix:02d} ]"}</span><h3>{E(c["h"])}</h3>{body}{lst}{kv}{chips}</article>')
            out.append(f'<div class="grid {cls}">' + "".join(h) + "</div>")
            continue
        if t == "kv":
            rows = []
            while i < n and items[i]["t"] == "kv": rows.append((items[i]["k"], items[i]["v"])); i += 1
            out.append('<div class="panel rv tscroll"><table class="specs">' + "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in rows) + "</table></div>")
            continue
        if t == "faq":
            qs = []
            while i < n and items[i]["t"] == "faq": qs.append(items[i]); i += 1
            out.append('<div class="faq rv">' + "".join(f"<details><summary>{E(q['q'])}</summary><p>{E(q['a'])}</p></details>" for q in qs) + "</div>")
            continue
        if t == "table":
            rows = b["v"]; hd = rows[0]; body = [r for r in rows[1:] if any(str(c).strip() for c in r[1:])]
            out.append('<div class="panel rv tscroll"><table class="specs wide"><thead><tr>' + "".join(f"<th>{E(c)}</th>" for c in hd) + "</tr></thead><tbody>" +
                       "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
            i += 1; continue
        if t == "ul":
            out.append('<ul class="list two rv">' + "".join(f"<li>{E(x)}</li>" for x in b["v"]) + "</ul>"); i += 1; continue
        if t in ("txt", "p"):
            run = []
            while i < n and items[i]["t"] in ("txt", "p"):
                if items[i]["t"] == "txt" and i + 1 < n and items[i + 1]["t"] == "h3" and len(items[i]["v"]) < 45 and run: break
                if run and items[i]["t"] == "txt" and (try_tcards(items, i)[0] or try_bars(items, i)[0]): break
                run.append(items[i]["v"]); i += 1
            # découpe en sous-listes étiquetées / listes / paragraphes
            groups = []; buf = []; lab = None
            def push():
                if buf or lab: groups.append((lab, list(buf)))
            for x in run:
                if LABEL.match(x):
                    push(); lab = x; buf = []
                else: buf.append(x)
            push()
            labeled = [g for g in groups if g[0]]
            if labeled:
                cols = []
                for lab_, items_ in groups:
                    if not lab_:
                        out.append("".join(f"<p>{E(x)}</p>" for x in items_)); continue
                    if not items_: continue
                    cls = "list neg" if NEG.match(lab_) else "list"
                    cols.append(f'<div class="panel rv"><div class="hud" style="margin-bottom:1rem">{E(lab_)}</div><ul class="{cls}">' + "".join(f"<li>{E(x)}</li>" for x in items_) + "</ul></div>")
                if cols: out.append(f'<div class="grid {"g2" if len(cols) > 1 else ""}">' + "".join(cols) + "</div>")
                continue
            if len(run) <= 4 and all(len(x) < 40 for x in run) and not any(x.endswith(".") for x in run):
                out.append('<div class="chips rv" style="margin:0">' + "".join(f'<span class="chip">{E(x)}</span>' for x in run) + "</div>"); continue
            longs = [x for x in run if len(x) > 80]
            if longs and len(run) > len(longs):
                html_ = []; k = 0
                while k < len(run):
                    x = run[k]
                    if x.endswith("?") and len(x) < 160 and k + 1 < len(run) and len(run[k + 1]) > 60 and not run[k + 1].endswith("?"):
                        qa = []
                        while k + 1 < len(run) and run[k].endswith("?") and len(run[k + 1]) > 60 and not run[k + 1].endswith("?"):
                            qa.append((run[k], run[k + 1])); k += 2
                        html_.append('<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in qa) + "</div>"); continue
                    if len(x) > 80 or (len(x) > 40 and x.endswith((".", "!", "?"))):
                        html_.append(f"<p>{E(x)}</p>"); k += 1; continue
                    seg = []
                    while k < len(run) and not (len(run[k]) > 80 or (len(run[k]) > 40 and run[k].endswith((".", "!", "?")))): seg.append(run[k]); k += 1
                    nxt_long = k < len(run)
                    if len(seg) == 1:
                        if nxt_long: html_.append(f'<div class="stars">{E(seg[0])}</div>' if set(seg[0]) <= set("★☆ ") else f'<h3 style="margin-top:.6rem">{E(seg[0])}</h3>')
                        continue
                    lab = None
                    NAME = re.compile(r"^[A-ZÉÈ][a-zéèëï\-]+ [A-ZÉÈ\-]{2,}$")
                    names = [ix for ix, y in enumerate(seg) if NAME.match(y)]
                    if names:
                        head_ = seg[:names[0]]; team = []
                        for a, ix in enumerate(names):
                            end = names[a + 1] if a + 1 < len(names) else len(seg)
                            team.append((seg[ix], seg[ix + 1:min(end, ix + 2)]))
                        extra = seg[names[-1] + 2:]
                        html_.append("".join(f'<div class="hud" style="margin:.6rem 0">{E(h)}</div>' for h in head_) + '<div class="grid g2" style="margin-bottom:1rem">' +
                                     "".join(f'<div class="panel team">{team_photo(1, nm)}<div><span class="k hud">Fondateur</span><h3>{E(nm)}</h3>' + "".join(f"<p>{E(r)}</p>" for r in roles) + "</div></div>" for nm, roles in team) + "</div>" + "".join(f'<h3 style="margin-top:1.2rem">{E(x)}</h3>' for x in extra))
                        continue
                    if re.search(r"(disponibles|typiques|:)$", seg[0], re.I) or seg[0].endswith(":"): lab = seg.pop(0)
                    elif nxt_long and len(seg) == 2: html_.append(f'<h3 style="margin-top:.6rem">{E(seg[-1])}</h3>'); seg = seg[:-1]
                    if seg: html_.append((f'<div class="hud" style="margin:.4rem 0 .6rem">{E(lab)}</div>' if lab else "") + '<div class="chips" style="margin:0 0 .8rem">' + "".join(f'<span class="chip">{E(y)}</span>' for y in seg) + "</div>")
                out.append('<div class="intro rv">' + "".join(html_) + "</div>"); continue
            short = [x for x in run if is_item(x)]
            if len(run) >= 3 and len(short) == len(run):
                out.append('<ul class="list two rv">' + "".join(f"<li>{E(x)}</li>" for x in run) + "</ul>")
            else:
                out.append('<div class="intro rv">' + "".join(f"<p>{E(x)}</p>" for x in run) + "</div>")
            continue
        i += 1
    return "\n".join(out)

def faq_ld(p):
    qs = [b for b in p["native"] + p["embed"] if b["t"] == "faq"]
    if not qs: return []
    return [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in qs]}]

def render_sections(m, start=1):
    h = []
    for ix, s in enumerate(m["sections"], start):
        body = render_items(s["items"])
        if not s["title"] and not body.strip(): continue
        head_ = ""
        if s["title"]:
            head_ = f'<div class="sec-no">[ {ix:02d} ]{(" · " + E(s["eyebrow"])) if s["eyebrow"] else ""}</div><h2 class="rv{" long" if len(s["title"]) > 60 else ""}">{E(s["title"])}</h2>'
        h.append(f'<section><div class="wrap">{head_}<div class="flow">{body}</div></div></section>')
    return "\n".join(h)

def page_hero(p, depth, m, after=""):
    stats = ""
    if m["stats"]:
        stats = '<div class="stats">' + "".join(f'<div class="stat"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in m["stats"][:4]) + "</div>"
    eb = f'<div class="hud eyebrow">{E(m["eyebrow"])}</div>' if m["eyebrow"] else ""
    lead = f'<p class="lead">{E(m["lead"])}</p>' if m["lead"] else (f'<p class="lead">{E(p["desc"])}</p>' if p.get("desc") else "")
    img = pic(depth, p["path"], m["title"], "pimg", lazy=False)
    if img:
        return (f'<section class="phero has-img"><div class="wrap">{crumbs(p["path"], depth)}<div class="split"><div>{eb}<h1>{E(m["title"])}</h1>{lead}{stats}{after}</div>'
                f'<div class="pvis"><div class="halo"></div>{img}<span class="hud dim tagl">Réf. {E(p["path"].split("/")[-1].upper())}</span></div></div></div></section>')
    return f'<section class="phero"><div class="wrap">{crumbs(p["path"], depth)}{eb}<h1>{E(m["title"])}</h1>{lead}{stats}{after}</div></section>'

def hub_grid(depth, items, kind):
    cards = []
    for ix, x in enumerate(items, 1):
        d = x.get("desc", "")
        th = pic(depth, x["path"], label(x), "thumb")
        cards.append(f'<a class="panel spot lcard rv{" with-img" if th else ""}" href="{rel(depth, x["path"])}">{th}<span class="k">{kind} · {ix:02d}</span><h3>{E(label(x))}</h3><p>{E(short(d, 150))}</p><span class="go">Ouvrir la fiche →</span></a>')
    return '<div class="grid g3">' + "".join(cards) + "</div>"

def write(path, html_):
    d = OUT / path if path else OUT
    d.mkdir(parents=True, exist_ok=True)
    if "Nos techniciens vous conseillent</h2>" in html_:
        up = "../" * (len(path.split("/")) if path else 0)
        html_ = re.sub(r"(Nos techniciens vous conseillent</h2>[\s\S]*?</p>)", lambda m: m.group(1) +
                       f'<p style="margin-top:1.4rem;display:flex;gap:.8rem;flex-wrap:wrap"><a class="btn btn-p" href="{up}contact/">Demander conseil <span class="a">→</span></a><a class="btn btn-g" href="{up}comparateur-materiaux/">Comparateur interactif <span class="a">→</span></a></p>', html_, count=1)
    html_ = html_.replace('a-propos/ou/"', 'a-propos/impression-3d-ville-liege/"') if path != "a-propos/ou" else html_
    (d / "index.html").write_text(html_, encoding="utf-8")

def depth_of(path): return len(path.split("/")) if path else 0

# ---------------------------------------------------------------- pages
HUBS = {"services": (SERVICES, "Service"), "machines-materiaux": (None, None), "comparateur-materiaux": (COMP, "Comparatif"),
        "réalisations": (REAL, "Projet"), "a-propos": (ZONES, "Zone")}

def gen_generic(p):
    d = depth_of(p["path"]); m = build_model(p)
    if p["path"] == "réalisations" and m["stats"]: m["stats"][0] = (str(len(REAL)), m["stats"][0][1])
    hub = ""
    if p["path"] == "machines-materiaux":
        hub = (f'<section><div class="wrap"><div class="sec-no">[ PARC MACHINES ]</div><h2 class="rv">Nos machines</h2>{hub_grid(d, MACH, "Machine")}</div></section>'
               f'<section><div class="wrap"><div class="sec-no">[ BIBLIOTHÈQUE ]</div><h2 class="rv">Nos matériaux</h2>{hub_grid(d, MATS, "Matériau")}</div></section>')
    elif p["path"] in HUBS:
        items, kind = HUBS[p["path"]]
        hub = f'<section><div class="wrap"><div class="sec-no">[ INDEX ]</div><h2 class="rv">{"Nos villes et zones" if p["path"]=="a-propos" else "Toutes les fiches"}</h2>{hub_grid(d, items, kind)}</div></section>'
    # liens vers pages sœurs (maillage interne)
    sib = ""
    parent = p["path"].rsplit("/", 1)[0] if "/" in p["path"] else None
    if parent and parent != "post":
        pool = MACH if p in MACH else MATS if p in MATS else kids(parent)
        others = [x for x in pool if x["path"] != p["path"]][:6]
        if others:
            sib = f'<section style="padding-top:30px"><div class="wrap"><div class="sec-no">[ À VOIR AUSSI ]</div>{hub_grid(d, others, "Fiche")}</div></section>'
    body = page_hero(p, d, m) + hub + render_sections(m) + (events_section(d) if p["path"] == "a-propos" else "") + sib + cta(d)
    write(p["path"], head(p["path"], d, p["title"], p["desc"], faq_ld(p)) + chrome(p["path"], d) + body + footer(d))

def gen_post(p):
    d = depth_of(p["path"]); m = build_model(p)
    date = p.get("date", "")[:10]
    content = []
    for b in normalize(p["native"]):
        t = b["t"]
        if t in ("h1",) and b["v"] == m["title"]: continue
        if t in ("h1", "h2"): content.append(f"<h2>{E(b['v'])}</h2>")
        elif t in ("h3", "h4"): content.append(f"<h3>{E(b['v'])}</h3>")
        elif t == "ul": content.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in b["v"]) + "</ul>")
        elif t in ("p", "txt"): content.append(f"<p>{E(b['v'])}</p>")
        elif t == "faq": content.append(f"<h3>{E(b['q'])}</h3><p>{E(b['a'])}</p>")
    ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["title"], "datePublished": p.get("date", ""), "author": {"@type": "Organization", "name": "O&D Impression 3D"}, "publisher": {"@id": SITE + "/#od3d"}}]
    title = p["title"].split(" | ")[0]
    cov = next((rp for rp, (src, *_x) in NEW_REAL.items() if src == p["path"]), None)
    covimg = (f'<div class="post-cover">{rimg(d, REALIMG[cov][0][0], REALIMG[cov][0][1], title, lazy=False)}</div><p><a class="btn btn-g" href="{rel(d, cov)}">Voir la réalisation en photos <span class="a">→</span></a></p>') if cov and REALIMG.get(cov) else ""
    hero = f'<section class="phero"><div class="wrap">{crumbs(p["path"], d)}<div class="post-meta">Article · {date}</div><h1 style="text-transform:none;font-size:clamp(2rem,4.6vw,3.6rem)">{E(title)}</h1><p class="lead">{E(p["desc"])}</p>{covimg}</div></section>'
    body = hero + f'<section><div class="wrap"><article class="prose">{"".join(content)}</article></div></section>' + cta(d)
    write(p["path"], head(p["path"], d, p["title"], p["desc"], ld) + chrome(p["path"], d) + body + footer(d))

def gen_blog_index():
    p = BY["actualites"]; d = 1
    cards = "".join(f'<a class="panel spot lcard rv" href="{rel(d, x["path"])}"><span class="k">{x.get("date","")[:10] or "Article"}</span><h3>{E(x["title"].split(" | ")[0])}</h3><p>{E(short(x["desc"], 140))}</p><span class="go">Lire →</span></a>'
                    for x in sorted(POSTS, key=lambda x: x.get("date", ""), reverse=True))
    m = {"title": "Actualités & blog", "eyebrow": "Journal de l'atelier", "lead": p["desc"], "stats": []}
    body = page_hero(p, d, m) + f'<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>' + cta(d)
    write("actualites", head("actualites", d, p["title"], p["desc"]) + chrome("actualites", d) + body + footer(d))

HIVE = [["BEMAC", "Ville de Verviers", "PJK Precision Mechanics", "4M Engineering"], ["Gühring", "Walibi Belgium", "Ville de Spa"],
        ["Commune de Welkenraedt", "Joris Ide", "Solucalc", "CHC Groupe Santé"]]
def hive():
    L = {l[0]: l for l in LOGOS}
    alt = {"CHC Groupe Santé": "CHC Mont Légia", "Commune de Welkenraedt": "Welkenraedt"}
    rows = "".join('<div class="hive-row">' + "".join(
        f'<div class="hex"><img src="{L[n][1][:-4]}.webp" alt="{E(alt.get(n, n))}" width="{L[n][2][0]}" height="{L[n][2][1]}" loading="lazy"></div>' for n in r if n in L) + "</div>" for r in HIVE)
    return f'<div class="hive rv" id="hive">{rows}</div>'

def cloud(shape, obj, proc, color="#00C1EA", extra="Glisser pour tourner", cls="", tilt=None):
    return (f'<div class="scan {cls}" style="--c:{color}"><div class="ring"></div><div class="ring r2"></div><canvas data-shape="{shape}" data-color="{color}"{f' data-tilt="{tilt}"' if tilt is not None else ""} aria-label="Rendu 3D interactif : {E(obj)}"></canvas>'
            f'<div class="tag t1">Objet<b>{E(obj)}</b></div><div class="tag t2">Rotation<b data-ang>000.0°</b></div><div class="tag t3">Points<b data-npts>—</b></div><div class="tag t4">{E(proc)}<b>{E(extra)}</b></div></div>')

ECO_C = {"sls": "#00C1EA", "fdm": "#FF8A3D", "resine": "#A97BFF", "cnc": "#C9D6DF"}
def mat_ring(d):
    cards = []
    for x in MATS:
        s = x["path"].split("/")[-1]; tk = None
        for k, t in TECH.items():
            if s in t["mats"]: tk = k
        if not tk: continue
        im = pic(d, x["path"], label(x), "rc-img")
        if not im:
            sym = CNC_MATS[s][7] if s in CNC_MATS else label(x).split()[0]
            im = f'<span class="rc-img sym"><b>{E(sym)}</b></span>'
        tg = HUBDATA.get(s, {}).get("tag") or (CNC_MATS[s][1] if s in CNC_MATS else "")
        cards.append(f'<a class="rcard" data-t="{tk}" style="--eco:{ECO_C[tk]}" href="{rel(d, x["path"])}" draggable="false">{im}<span class="rc-t">{E(TECH[tk]["name"])}</span><b>{E(label(x))}</b><span class="rc-g">{E(tg)}</span></a>')
    chips = '<button type="button" class="on" data-f="all">Toutes</button>' + "".join(f'<button type="button" data-f="{k}" style="--eco:{ECO_C[k]}">{E(t["name"])}</button>' for k, t in TECH.items() if t["mats"])
    return (f'<div class="mring" id="mring"><div class="mr-filters" role="group" aria-label="Filtrer par technologie">{chips}</div>'
            f'<div class="mr-box"><div class="mr-stage"><div class="mr-core">{cloud("gear", "Engrenage", "Matière", "#00C1EA", "PA12 · SLS", "mini")}</div><div class="mr-rot">{"".join(cards)}</div></div>'
            f'<button type="button" class="mr-arr l" data-nav="-1" aria-label="Matière précédente"><span>‹</span><span>‹</span></button><button type="button" class="mr-arr r" data-nav="1" aria-label="Matière suivante"><span>›</span><span>›</span></button></div>'
            f'<div class="mr-front"><span class="hud">Face à vous</span><b id="mrName">—</b><span id="mrTag"></span><a class="btn btn-g" id="mrGo" href="#">Ouvrir la fiche <span class="a">→</span></a></div></div>')

def gen_home():
    p = BY[""] if "" in BY else {"path": "", "title": "O&D Impression 3D", "desc": ""}
    d = 0
    tech = [("SLS", "services/impression-3d-sls", "Frittage laser", "Pièces fonctionnelles robustes en nylon, sans supports. Formes complexes et séries."),
            ("FDM", "services/impression-3d-fdm", "Dépôt de filament", "Prototypes, outillages, grandes pièces et multicolore. Du PLA au PEEK et à l'ULTEM."),
            ("SLA", "services/impression-3d-resine", "Stéréolithographie", "Très haute définition, surfaces lisses, petits détails : maquettes et pièces d'aspect."),
            ("CNC", "services/usinage-cnc", "Fraisage", "Pièces usinées précises dans la masse : aluminium, laiton, bronze, titane, plastiques techniques."),
            ("Scan 3D", "services/scan-3d", "Numérisation", "Rétro-conception, reproduction de pièces introuvables, contrôle de forme."),
            ("Laser", "machines-materiaux/xtool-f1", "Gravure laser", "Personnalisation, marquage, numérotation, découpe et signalétique.")]
    tcards = "".join(f'<a class="panel spot lcard tcard rv" href="{rel(d, u)}"><span class="k">{k}</span><h3 class="tcode">{c}</h3><p>{E(t)}</p><span class="go">Explorer →</span></a>' for c, u, k, t in tech)
    reals = "".join(f'<a class="panel spot lcard rv" href="{rel(d, x["path"])}"><span class="k">Projet · {i:02d}</span><h3>{E(label(x))}</h3><p>{E(short(x["desc"], 130))}</p><span class="go">Voir le projet →</span></a>' for i, x in enumerate(REAL, 1))
    mats = " ".join(f"<span>{E(label(x))}</span>" for x in MATS)
    tools = "".join(f'<a class="panel spot lcard rv" href="{rel(d, u)}"><span class="k">Outil</span><h3>{t}</h3><p>{s}</p><span class="go">Ouvrir →</span></a>' for u, t, s in [
        ("quiz-technologie-impression-3d", "Quiz : quelle technologie ?", "Quelques questions pour savoir quel procédé convient à votre pièce."),
        ("devis-instantane", "Devis instantané", "Déposez votre STL, choisissez la matière : estimation immédiate."),
        ("comparateur-materiaux", "Comparateur de matériaux", "PLA vs PETG, PEEK vs PEKK vs Ultem, FDM vs SLS vs SLA…"),
        ("technologies-materiaux-impression-3d", "Guide matériaux & technologies", "Le guide complet pour choisir procédé et matière.")])
    hero = f'''<section class="hero"><div class="wrap">
<div><div class="hud eyebrow">Fabrication additive &amp; usinage — Belgique</div>
<h1><span class="ln"><span>Fabriquer</span></span><span class="ln"><span>le futur,</span></span><span class="ln"><span class="glow">couche par couche.</span></span></h1>
<p class="lead">Impression 3D <strong>SLS, FDM et SLA</strong>, <strong>usinage CNC</strong> et <strong>scan 3D</strong> réunis dans un atelier à Welkenraedt. Prototypes, pièces techniques et petites séries pour l'industrie et les secteurs exigeants.</p>
<div class="cta-row"><a class="btn btn-p" href="devis-instantane/">Devis instantané <span class="a">→</span></a><a class="btn btn-g" href="services/">Nos technologies</a></div>
<div class="stats"><div class="stat"><b>2021</b><span>Atelier fondé</span></div><div class="stat"><b>6</b><span>Procédés</span></div><div class="stat"><b>{len(MATS)}</b><span>Fiches matériaux</span></div><div class="stat"><b>24 h</b><span>Devis personnalisé</span></div></div></div>
<div class="scan" aria-hidden="true"><div class="ring"></div><div class="ring r2"></div><canvas id="cloud" data-shape="flange" aria-label="Rendu 3D interactif"></canvas>
<div class="tag t1">Objet<b>Bride percée Ø80</b></div><div class="tag t2">Rotation<b id="ang" data-ang>000.0°</b></div><div class="tag t3">Points<b id="npts" data-npts>—</b></div><div class="tag t4">Scanner<b>3DeVOK MT</b></div></div>
</div></section>
<div class="ticker" aria-hidden="true"><div>{mats} {mats}</div></div>'''
    secs = f'''
<section class="vid-sec"><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ ATELIER ] · Welkenraedt</div><h2>L'atelier <span class="glow">en mouvement.</span></h2></div><p class="lead">Les machines tournent, les pièces sortent. Un aperçu de notre atelier de Welkenraedt et de l'équipe au travail.</p></div>
<figure class="vframe rv"><video id="atelierVid" muted loop playsinline preload="metadata" poster="static/video/atelier-od3d-poster.jpg" aria-label="Vidéo de présentation de l'atelier O&amp;D Impression 3D"><source src="static/video/atelier-od3d.mp4" type="video/mp4"></video>
<span class="vc tl"></span><span class="vc tr"></span><span class="vc bl"></span><span class="vc br"></span><span class="vrec hud"><i></i>Atelier · Welkenraedt (BE)</span>
<div class="vctl"><button type="button" class="vbtn" data-act="play" aria-label="Lecture / pause"><span class="ic-pause">❚❚</span><span class="ic-play">▶</span></button><button type="button" class="vbtn" data-act="sound" aria-label="Activer / couper le son"><span class="ic-mute">Son coupé</span><span class="ic-snd">Son activé</span></button>
<a class="vyt" href="https://youtu.be/kWaspuGcDJc" target="_blank" rel="noopener">Voir sur YouTube ↗</a></div></figure></div></section>
<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ 01 ] · Technologies</div><h2>Six procédés.<br><span class="glow">Un interlocuteur.</span></h2></div><p class="lead">Le procédé se choisit selon votre cahier des charges : résistance, précision, état de surface, quantité, budget.</p></div><div class="grid g3">{tcards}</div></div></section>
<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ 02 ] · Parc machines</div><h2>Ce qui tourne<br>à l'atelier.</h2></div><p><a class="btn btn-g" href="machines-materiaux/">Tout le parc <span class="a">→</span></a></p></div>{hub_grid(d, MACH[:6], "Machine")}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-no">[ RÉFÉRENCES ] · Ils nous ont confié leurs pièces</div>{hive()}</div></section>
<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ BIBLIOTHÈQUE ] · Matériaux</div><h2>Du PLA<br>au <span class="glow">PEEK.</span></h2></div><p class="lead">{len(MATS)} fiches matériaux détaillées : propriétés, avantages, limites et machines compatibles.</p></div>{mat_ring(d)}<p style="margin-top:1.4rem"><a class="btn btn-g" href="machines-materiaux/">Toute la bibliothèque <span class="a">→</span></a></p></div></section>
<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ 03 ] · Méthode</div><h2>Du fichier<br>à la pièce.</h2></div></div>
<div class="steps"><div class="panel rv n"><h3>Envoyez</h3><p>Fichier STEP, STL ou 3MF, plan, croquis… ou la pièce à scanner.</p></div><div class="panel rv n"><h3>Analyse &amp; devis</h3><p>Instantané avec fichier 3D, personnalisé sous 24 h.</p></div><div class="panel rv n"><h3>Fabrication</h3><p>Procédé et matière choisis selon vos contraintes.</p></div><div class="panel rv n"><h3>Livraison</h3><p>Envoi ou retrait à l'atelier de Welkenraedt.</p></div></div></div></section>
<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ 04 ] · Réalisations</div><h2>Des projets<br><span class="glow">réels.</span></h2></div><p><a class="btn btn-g" href="réalisations/">Tous les projets <span class="a">→</span></a></p></div>{hub_grid(d, REAL[:6], "Projet")}</div></section>
{events_section(d, "05")}
<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ 06 ] · Outils</div><h2>Choisir, comparer,<br>chiffrer.</h2></div></div><div class="grid g4">{tools}</div></div></section>
'''
    m = build_model(p) if p.get("native") is not None else None
    write("", head("", d, "O&D Impression 3D | Impression 3D SLS, FDM & CNC à Liège", "Impression 3D SLS, FDM et SLA, usinage CNC et scan 3D à Welkenraedt (Liège). Prototypes, pièces techniques et petites séries. Devis sous 24 h.") + chrome("", d) + hero + secs + cta(d) + footer(d))

def gen_app(path, title, desc, h1, lead, src, height=1100):
    d = depth_of(path); p = {"path": path, "desc": desc}
    BY.setdefault(path, {"path": path, "title": title, "desc": desc, "native": [], "embed": []})
    m = {"title": h1, "eyebrow": "Outil interactif", "lead": lead, "stats": []}
    if src == "quiz.html":
        css = (STATIC / "apps" / "quiz_inline.css").read_text(encoding="utf-8").replace("border-radius: 18px;", "border-radius: 0;")
        js = (STATIC / "apps" / "quiz_inline.js").read_text(encoding="utf-8")
        body = (page_hero(p, d, m) + f'<section style="padding-top:30px"><div class="wrap"><style>{css}</style><div id="quizApp"><div class="qz-wrapper" id="quizRoot"></div></div>'
                f'<script>{js}</script></div></section>' + cta(d))
        write(path, head(path, d, title, desc) + chrome(path, d) + body + footer(d)); return
    body = page_hero(p, d, m) + f'<section style="padding-top:40px"><div class="wrap"><iframe class="app" style="min-height:{height}px" src="{"../" * d}static/apps/{src}" title="{E(h1)}" loading="lazy"></iframe></div></section>' + cta(d)
    write(path, head(path, d, title, desc) + chrome(path, d) + body + footer(d))

FAQ = json.load(open(ROOT / "content/faq.json", encoding="utf-8"))
FIX = [("Baelen (4837)", "Welkenraedt (4840)")]
def fx(t):
    for a, b in FIX: t = t.replace(a, b)
    return t
def gen_faq():
    p = BY["faq"]; d = 1
    tabs = "".join(f'<a class="chip" href="#cat{i}">{E(c["c"])}</a>' for i, c in enumerate(FAQ))
    secs = "".join(f'<section id="cat{i}" style="padding:50px 0 10px"><div class="wrap"><div class="sec-no">[ {i+1:02d} ] · {len(c["i"])} questions</div><h2 class="rv">{E(c["c"])}</h2>'
                   + '<div class="faq rv">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(fx(a))}</p></details>" for q, a in c["i"]) + "</div></div></section>" for i, c in enumerate(FAQ))
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": fx(a)}} for c in FAQ for q, a in c["i"]]}]
    m = {"title": "Questions fréquentes", "eyebrow": "Foire aux questions", "lead": "Services, matériaux, prix, délais, fichiers : les réponses aux questions qu'on nous pose le plus souvent.", "stats": []}
    body = page_hero(p, d, m, f'<div class="chips" style="margin-top:1.6rem">{tabs}</div>') + secs + cta(d)
    write("faq", head("faq", d, p["title"], p["desc"], ld) + chrome("faq", d) + body + footer(d))

def gen_contact():
    p = BY["contact"]; d = 1; m = build_model(p)
    form = f'''<section style="padding-top:50px"><div class="wrap" style="display:grid;gap:40px">
<form class="panel form" name="devis" method="POST" action="../merci/" data-netlify="true" netlify-honeypot="bot" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="devis"><p class="sr" aria-hidden="true"><label>Ne pas remplir <input name="bot" tabindex="-1" autocomplete="off"></label></p>
<div class="field full"><label>Technologie envisagée</label><div class="opts">{"".join(f'<label><input type="checkbox" name="techno" value="{t}"><span>{t}</span></label>' for t in ["SLS","FDM","SLA","CNC","Scan 3D","Gravure laser","Je ne sais pas"])}</div></div>
<div class="field"><label for="n">Nom *</label><input id="n" name="nom" required autocomplete="name"></div>
<div class="field"><label for="s">Société</label><input id="s" name="societe" autocomplete="organization"></div>
<div class="field"><label for="e">E-mail *</label><input id="e" type="email" name="email" required autocomplete="email"></div>
<div class="field"><label for="t">Téléphone</label><input id="t" type="tel" name="tel" autocomplete="tel"></div>
<div class="field"><label for="q">Quantité</label><input id="q" name="quantite" inputmode="numeric"></div>
<div class="field"><label for="dl">Délai</label><select id="dl" name="delai"><option value="">Choisir…</option><option>Urgent</option><option>2 semaines</option><option>1 mois</option><option>Flexible</option></select></div>
<div class="field full"><label for="m">Votre projet *</label><textarea id="m" name="message" required placeholder="Usage, contraintes (température, efforts, chimie), matière, dimensions…"></textarea></div>
<div class="field full"><label for="f">Fichier 3D ou plan</label><input id="f" type="file" name="fichier" accept=".step,.stp,.stl,.3mf,.obj,.pdf,.jpg,.png"></div>
<div class="field full"><button class="btn btn-p" type="submit">Envoyer ma demande <span class="a">→</span></button></div></form>
</div></section>'''
    info = ('<section style="padding:40px 0 0"><div class="wrap"><div class="grid g4">'
            '<div class="panel rv"><span class="k hud">Atelier</span><p style="color:var(--t)">Rue Trois Bourdons 52E<br>4840 Welkenraedt, Belgique</p></div>'
            '<div class="panel rv"><span class="k hud">Téléphone</span><p><a style="color:var(--t)" href="tel:+3242901192">04 290 11 92</a></p></div>'
            '<div class="panel rv"><span class="k hud">E-mail</span><p><a style="color:var(--t)" href="mailto:o.d3dindustrie@gmail.com">o.d3dindustrie@gmail.com</a></p></div>'
            '<div class="panel rv"><span class="k hud">Horaires</span><p style="color:var(--t)">Lun–sam, 9 h–17 h<br>Visite sur rendez-vous</p></div>'
            '</div></div></section>')
    body = page_hero(p, d, m) + info + form + render_sections(m) + cta(d)
    write("contact", head("contact", d, p["title"], p["desc"]) + chrome("contact", d) + body + footer(d))

def gen_simple(path, title, h1, text):
    d = depth_of(path)
    body = f'<section class="phero" style="min-height:60vh"><div class="wrap"><div class="hud eyebrow">{E(title)}</div><h1>{h1}</h1><p class="lead">{text}</p><div class="cta-row"><a class="btn btn-p" href="{rel(d,"")}">Accueil <span class="a">→</span></a></div></div></section>'
    return head(path, d, title + " | O&D Impression 3D", text) + chrome(path, d) + body + footer(d)

exec(open(ROOT / "eco.py", encoding="utf-8").read())
exec(open(ROOT / "real.py", encoding="utf-8").read())
exec(open(ROOT / "comp.py", encoding="utf-8").read())
exec(open(ROOT / "about.py", encoding="utf-8").read())
ECO_URLS = {t["url"]: k for k, t in TECH.items()}

# ---------------------------------------------------------------- build
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(STATIC, OUT / "static")
gen_home()
for p in P:
    if p["path"] in ("", "contact", "actualites", "quiz-technologie-impression-3d", "faq"): continue
    sl = p["path"].split("/")[-1]
    if p.get("blog"): gen_post(p)
    elif p["path"] in ECO_URLS: gen_eco(ECO_URLS[p["path"]])
    elif p["path"] == "machines-materiaux": gen_parc()
    elif p["path"] == "comparateur-materiaux": gen_comp(p)
    elif p["path"] == "a-propos": gen_about()
    elif p["path"] == LIEGE_MAIN: gen_liege()
    elif p["path"] == LIEGE_OLD: pass
    elif p["path"].startswith("réalisations/"): gen_real(p)
    elif p["path"].startswith("machines-materiaux/") and sl in ALLM: gen_machine(p)
    elif p["path"].startswith("machines-materiaux/") and sl in ALLT: gen_material(p)
    else: gen_generic(p)
gen_contact(); gen_blog_index(); gen_faq()
gen_app("quiz-technologie-impression-3d", BY["quiz-technologie-impression-3d"]["title"], BY["quiz-technologie-impression-3d"]["desc"],
        "Quelle technologie pour votre pièce ?", "Répondez à quelques questions : le quiz vous recommande le procédé le plus adapté (FDM, SLS, résine ou CNC).", "quiz.html", 1000)
gen_app("devis-instantane", "Devis instantané impression 3D | O&D Impression 3D", "Déposez votre fichier STL, choisissez la matière et la quantité : estimation immédiate du prix de votre impression 3D.",
        "Devis instantané", "Déposez votre fichier STL, choisissez la matière et la quantité : estimation immédiate. Au-delà de 100 pièces, demande personnalisée.", "devis.html", 760)
(OUT / "merci").mkdir(exist_ok=True)
(OUT / "merci/index.html").write_text(gen_simple("merci", "Demande envoyée", 'Merci. <span class="glow">On s\'en occupe.</span>', "Votre demande est bien arrivée : réponse technique sous 24 h."), encoding="utf-8")
(OUT / "404.html").write_text(gen_simple("", "Page introuvable", 'Signal <span class="glow">perdu.</span>', "Cette page n'existe pas ou a été déplacée.").replace("<head>", f'<head>\n<base href="{BASE}">').replace('href="./static', 'href="' + BASE + 'static').replace('src="./static', 'src="' + BASE + 'static').replace('href="./"', 'href="' + BASE + '"'), encoding="utf-8")
# sitemap / robots
urls = [""] + [p["path"] for p in P if p["path"] and p["path"] != LIEGE_OLD] + ["devis-instantane"]
seen = []
for u in urls:
    if u not in seen: seen.append(u)
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "\n".join(f"  <url><loc>{SITE}/{urllib.parse.quote(u)}</loc></url>" for u in seen) + "\n</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(("User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n") if PROD else "User-agent: *\nDisallow: /\n", encoding="utf-8")
(OUT / ".nojekyll").write_text("")
print("pages:", len(list(OUT.rglob("index.html"))))
import subprocess; subprocess.run([sys.executable, str(ROOT / "i18n.py")], check=True)
