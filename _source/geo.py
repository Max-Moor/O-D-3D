"""Optimisation GEO (moteurs de réponse IA) — post-traitement de dist/ après build + i18n.
- Graphe schema.org par page : WebSite, WebPage (dateModified, speakable), Service, CreativeWork, VideoObject
- llms.txt + llms-full.txt (résumé machine-lisible du site, format llmstxt.org)
- sitemap avec lastmod + alternates de langue ; robots.txt de production ouvert aux robots IA
Usage : python3 geo.py [--prod]"""
import json, re, sys, html, datetime, pathlib, urllib.parse, posixpath
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "dist"
PROD = "--prod" in sys.argv
SITE = "https://www.od3d.be"
ORG = SITE + "/#od3d"
WEBSITE = SITE + "/#website"
TODAY = datetime.date.today().isoformat()
LANGS = ("en", "de", "nl")
INLANG = {"fr": "fr-BE", "en": "en", "de": "de-BE", "nl": "nl-BE"}
AREA = [{"@type": "AdministrativeArea", "name": "Province de Liège"}, {"@type": "Country", "name": "Belgique"}]
TECHS = {"impression-3d-sls": "Impression 3D SLS", "impression-3d-fdm": "Impression 3D FDM", "impression-3d-resine": "Impression 3D SLA",
         "usinage-cnc": "Usinage CNC", "scan-3d": "Scan 3D"}

def un(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
def grab(h, pat):
    m = re.search(pat, h, re.S); return un(m.group(1)) if m else ""
def url_of(rel):
    return SITE + ("/" + urllib.parse.quote(rel) if rel else "/")

def page_kind(fr):
    if fr == "": return "home"
    top = fr.split("/")[0]
    if fr in ("services", "machines-materiaux", "comparateur-materiaux", "réalisations", "actualites", "a-propos"): return "hub"
    if top == "services": return "service"
    if top == "réalisations": return "real"
    if top == "post": return "post"
    if top == "machines-materiaux": return "mat"
    if top == "a-propos": return "zone"
    if top == "comparateur-materiaux": return "comp"
    if fr == "contact": return "contact"
    if fr == "faq": return "faq"
    return "page"

TYPE = {"home": "WebPage", "hub": "CollectionPage", "contact": "ContactPage", "faq": "FAQPage", "zone": "WebPage", "post": "WebPage"}
MACHINES = {"supermaker-sls1518", "supermaker-sls3540-pro", "bambu-lab-h2c", "bambu-lab-x1c", "modix-big-meter", "prusa-core-one",
            "intamsys-funmat-ht", "anycubic-photon-m7-max", "tooldance-x1-cnc", "xtool-f1", "scanner-3devok-mt"}

pages = []
for f in sorted(OUT.rglob("index.html")):
    rel = f.parent.relative_to(OUT).as_posix(); rel = "" if rel == "." else rel
    h = f.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in h: continue
    lang = rel.split("/")[0] if rel.split("/")[0] in LANGS else "fr"
    alts = {l: urllib.parse.unquote(u).replace(SITE, "").strip("/") for l, u in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', h)}
    fr = alts.get("x-default", rel) if lang != "fr" else rel
    pages.append(dict(f=f, rel=rel, fr=fr, lang=lang, h=h, alts=alts))
langs_of = {}; locs = {}
for p in pages:
    langs_of.setdefault(p["fr"], set()).add(p["lang"]); locs[(p["lang"], p["fr"])] = p["rel"]

def loc(lang, fr):
    r = locs.get((lang, fr), fr)
    return url_of(r) + ("/" if r in LANGS else "")
for p in pages:
    h = p["h"]; url = url_of(p["rel"]) + ("/" if p["rel"] in LANGS else ""); kind = page_kind(p["fr"])
    title = grab(h, r"<title>(.*?)</title>"); desc = grab(h, r'<meta name="description" content="(.*?)"')
    main = h[h.find("<main"):] if "<main" in h else h
    h1 = grab(main, r"<h1[^>]*>(.*?)</h1>") or title.split(" | ")[0]
    img = re.search(r'<img[^>]+src="([^"]+\.(?:png|jpe?g|webp))"', main)
    image = SITE + "/" + re.sub(r"^(\.\./)+|^\./", "", img.group(1)) if img else SITE + "/static/img/og-image.jpg"
    g = [{"@type": "WebSite", "@id": WEBSITE, "url": SITE + "/", "name": "O&D Impression 3D", "publisher": {"@id": ORG},
          "inLanguage": ["fr-BE", "en", "de-BE", "nl-BE"]}]
    wp = {"@type": TYPE.get(kind, "WebPage"), "@id": url + "#webpage", "url": url, "name": title, "description": desc,
          "inLanguage": INLANG[p["lang"]], "isPartOf": {"@id": WEBSITE}, "publisher": {"@id": ORG}, "about": {"@id": ORG},
          "dateModified": TODAY, "primaryImageOfPage": {"@type": "ImageObject", "url": image},
          "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".lead"]}}
    if kind == "faq": wp["@type"] = "WebPage"  # FAQPage déjà présent dans la page
    g.append(wp)
    slug = p["fr"].split("/")[-1]
    if kind == "service" or (kind == "mat" and slug not in MACHINES):
        svc = {"@type": "Service", "@id": url + "#service", "name": h1, "description": desc, "url": url, "provider": {"@id": ORG},
               "areaServed": AREA, "mainEntityOfPage": {"@id": url + "#webpage"}, "image": image,
               "serviceType": TECHS.get(slug) or ("Impression 3D et usinage sur mesure" if kind == "mat" else h1),
               "offers": {"@type": "Offer", "url": loc(p["lang"], "devis-instantane") if p["lang"] in langs_of.get("devis-instantane", ()) else url_of("devis-instantane"),
                          "availability": "https://schema.org/InStock", "seller": {"@id": ORG}}}
        g.append(svc); wp["mainEntity"] = {"@id": url + "#service"}
    elif kind == "mat":  # fiche machine
        g.append({"@type": "Thing", "@id": url + "#machine", "name": h1, "description": desc, "image": image, "category": "Machine de l'atelier O&D"})
        wp["about"] = {"@id": url + "#machine"}
    elif kind == "real":
        g.append({"@type": "CreativeWork", "@id": url + "#projet", "name": h1, "headline": h1, "description": desc, "image": image,
                  "creator": {"@id": ORG}, "url": url, "inLanguage": INLANG[p["lang"]], "genre": "Étude de cas"})
        wp["mainEntity"] = {"@id": url + "#projet"}
    elif kind == "home":
        g.append({"@type": "VideoObject", "@id": SITE + "/#video-atelier", "name": "L'atelier O&D Impression 3D en vidéo",
                  "description": "Visite de l'atelier O&D Impression 3D à Welkenraedt : impression 3D SLS, FDM et SLA et usinage CNC.",
                  "thumbnailUrl": SITE + "/static/video/atelier-od3d-poster.jpg", "contentUrl": SITE + "/static/video/atelier-od3d.mp4",
                  "embedUrl": "https://www.youtube.com/embed/kWaspuGcDJc", "duration": "PT37S", "publisher": {"@id": ORG}})
        g.append({"@id": ORG, "@type": "LocalBusiness", "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services O&D Impression 3D",
                  "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": url_of("services/" + s)}} for s, n in TECHS.items()]}})
    elif kind == "post" and "\"dateModified\"" not in h:
        h = h.replace('"@type": "BlogPosting", ', f'"@type": "BlogPosting", "mainEntityOfPage": {{"@id": "{url}#webpage"}}, "image": "{image}", "dateModified": "{TODAY}", "inLanguage": "{INLANG[p["lang"]]}", ', 1)
    block = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + "</script>\n"
    h = re.sub(r'<script data-geo [^>]*>.*?</script>\n', "", h, flags=re.S)
    h = h.replace("</head>", block.replace("<script ", "<script data-geo ", 1) + "</head>", 1)
    p["h"] = h; p["title"] = title; p["desc"] = desc; p["h1"] = h1; p["kind"] = kind
    p["f"].write_text(h, encoding="utf-8")

# ------------------------------------------------------------- sitemap (lastmod + hreflang)
HL = {"fr": "fr", "en": "en", "de": "de", "nl": "nl"}
seen = []
for p in sorted(pages, key=lambda p: p["fr"] != ""):
    if p["lang"] == "fr" and p["fr"] not in seen and p["fr"] not in ("merci",): seen.append(p["fr"])
xs = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for fr in seen:
    ls = sorted(langs_of.get(fr, {"fr"}), key=lambda l: (l != "fr", l))
    for l in ls:
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{HL[x]}" href="{loc(x, fr)}"/>' for x in ls) if len(ls) > 1 else ""
        if len(ls) > 1: alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{loc("fr", fr)}"/>'
        xs.append(f"  <url><loc>{loc(l, fr)}</loc><lastmod>{TODAY}</lastmod>{alt}</url>")
xs.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(xs) + "\n", encoding="utf-8")

# ------------------------------------------------------------- robots
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
           "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot", "DuckAssistBot", "MistralAI-User", "CCBot"]
prod_robots = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS) + "User-agent: *\nAllow: /\nDisallow: /merci/\n\nSitemap: " + SITE + "/sitemap.xml\n"
(ROOT / "robots_production.txt").write_text(prod_robots, encoding="utf-8")
(OUT / "robots.txt").write_text(prod_robots if PROD else "User-agent: *\nDisallow: /\n", encoding="utf-8")

# ------------------------------------------------------------- llms.txt / llms-full.txt
FR = {p["fr"]: p for p in pages if p["lang"] == "fr"}
def md_link(p): return f"- [{p['h1']}]({url_of(p['fr'])}): {p['desc']}"
GROUPS = [("Services", lambda k, fr: k == "service" or fr == "services"),
          ("Machines de l'atelier", lambda k, fr: k == "mat" and fr.split("/")[-1] in MACHINES),
          ("Matières (fiches techniques)", lambda k, fr: k == "mat" and fr.split("/")[-1] not in MACHINES),
          ("Comparatifs de matériaux", lambda k, fr: fr.startswith("comparateur-materiaux") or fr == "technologies-materiaux-impression-3d"),
          ("Réalisations (études de cas)", lambda k, fr: k == "real"),
          ("Zones desservies et entreprise", lambda k, fr: k == "zone" or fr == "a-propos"),
          ("Outils et contact", lambda k, fr: fr in ("devis-instantane", "quiz-technologie-impression-3d", "contact", "faq")),
          ("Articles et guides", lambda k, fr: k == "post")]
facts = """O&D Impression 3D est un atelier de fabrication belge fondé en 2021 par Owen Schimmenti et Donovan Waucomont, installé Rue Trois Bourdons 52E, 4840 Welkenraedt (province de Liège, Belgique).

- Procédés : impression 3D SLS (frittage laser sélectif), FDM (dépôt de fil fondu), SLA (résine), usinage CNC, scan 3D, rétro-conception, modélisation 3D, gravure et découpe laser.
- Production : prototypes, pièces techniques et fonctionnelles, pièces de remplacement, outillages et petites séries, de la pièce unique à la production.
- Zones servies : Liège, Verviers, Eupen, Spa, Huy, Seraing, Welkenraedt et toute la Belgique.
- Devis : instantané en ligne avec un fichier 3D (STL, STEP, 3MF), ou personnalisé sous 24 h.
- Contact : +32 471 68 66 53 · o.d3dindustrie@gmail.com · https://www.od3d.be/contact
- Langues du site : français (principal), anglais (/en/), allemand (/de/), néerlandais (/nl/)."""
lines = ["# O&D Impression 3D", "", "> Atelier d'impression 3D (SLS, FDM, SLA) et d'usinage CNC à Welkenraedt, province de Liège (Belgique) : prototypes, pièces techniques et petites séries. Devis sous 24 h.", "", facts, ""]
used = set()
for name, test in GROUPS:
    items = [p for fr, p in FR.items() if fr not in used and test(p["kind"], fr)]
    if not items: continue
    lines += [f"## {name}", ""] + [md_link(p) for p in items] + [""]
    used |= {p["fr"] for p in items}
lines += ["## Optional", "", md_link(FR[""]) if "" in FR else "", f"- [Plan du site]({SITE}/sitemap.xml): toutes les pages et leurs versions linguistiques", ""]
(OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")

def main_text(h):
    m = h[h.find("<main"):h.find("</main>")] if "<main" in h else h
    m = re.split(r'<section[^>]*class="[^"]*\bcta\b', m)[0]
    m = re.sub(r"<(script|style|svg|canvas|button|nav)[^>]*>.*?</\1>", " ", m, flags=re.S)
    m = re.sub(r'<div class="crumbs.*?</div>', " ", m, flags=re.S)
    m = re.sub(r"<h([1-4])[^>]*>(.*?)</h\1>", lambda x: "\n\n" + "#" * (int(x.group(1)) + 1) + " " + un(x.group(2)) + "\n", m, flags=re.S)
    m = re.sub(r"</span>\s*<(b|p|strong)>", r": <\1>", m); m = re.sub(r"</(span|a)>", r"</\1> ", m)
    m = re.sub(r"<li[^>]*>", "\n- ", m); m = re.sub(r"<(tr)[^>]*>", "\n", m); m = re.sub(r"</t[dh]>", " | ", m)
    m = re.sub(r"<summary[^>]*>(.*?)</summary>", lambda x: "\n\n**" + un(x.group(1)) + "**\n", m, flags=re.S)
    m = re.sub(r"</(p|div|section|details|dd|dt|h\d)>", "\n", m)
    t = un(m)
    t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n\s*\n+", "\n\n", t)
    return "\n".join(x.strip() for x in t.splitlines()).strip()
full = ["# O&D Impression 3D — contenu complet", "", facts, ""]
for name, test in GROUPS[:-1]:
    for fr, p in FR.items():
        if test(p["kind"], fr) and p["kind"] != "hub":
            full += ["", "---", "", f"# {p['h1']}", f"URL : {url_of(fr)}", "", main_text(p["h"])]
(OUT / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
print(f"geo: {len(pages)} pages enrichies · llms.txt {len(lines)} lignes · llms-full.txt {sum(len(x) for x in full)//1024} Ko")

# ------------------------------------------------------------- redirections 301 (anciennes URL Wix)
RJ = json.load(open(ROOT / "content/redirects.json", encoding="utf-8"))
def is_page(rel): return (OUT / rel / "index.html").exists() if rel else True
slug_en = json.load(open(ROOT / "i18n/slugs_en.json", encoding="utf-8"))
rev_en = {v: k for k, v in slug_en.items()}
pairs = []
for a, b in RJ["fr"]: pairs.append((a.strip("/"), b.strip("/")))
for fr, s in slug_en.items():
    if fr and s != fr and is_page(fr):
        pairs.append(("en/" + fr, ("en/" + s) if is_page("en/" + s) else fr))
for fr, s in slug_en.items():  # URL anglaises du site actuel pas encore traduites -> page FR
    if s and fr and is_page(fr) and not is_page("en/" + s): pairs.append(("en/" + s, fr))
for a, b in RJ["en"]:
    b = b.strip("/"); fr_eq = rev_en.get(b, b)
    pairs.append(("en/" + a.strip("/"), ("en/" + b) if is_page("en/" + b) else fr_eq))
stub = '''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Redirection</title><meta name="robots" content="noindex">
<link rel="canonical" href="{abs}"><meta http-equiv="refresh" content="0; url={rel}"></head>
<body><p><a href="{rel}">Cette page a été déplacée.</a></p></body></html>'''
csv = ["from,to"]; made = 0; bad = []
for a, b in pairs:
    if not is_page(b) or b.startswith(("http",)):
        bad.append((a, b)); continue
    csv.append(f"/{a},/{b}")
    d = OUT / a
    if (d / "index.html").exists(): continue
    d.mkdir(parents=True, exist_ok=True)
    r = posixpath.relpath("/" + b, "/" + a) if b else posixpath.relpath("/", "/" + a)
    r = urllib.parse.quote(r) + "/"
    (d / "index.html").write_text(stub.format(abs=url_of(b), rel=r), encoding="utf-8"); made += 1
(ROOT / "redirects_301.csv").write_text("\n".join(dict.fromkeys(csv)) + "\n", encoding="utf-8")
print(f"redirections: {len(csv)-1} règles · {made} pages relais créées" + (f" · cibles absentes: {bad[:5]}" if bad else ""))
