# Réalisations avec photos, équipe, salons (chargé par build.py après eco.py)
REALIMG = MEDIA.get("real", {}); TEAM = MEDIA.get("team", {}); EVENTS = MEDIA.get("events", [])

NEW_REAL = {
 "réalisations/walibi-wagons-loup-garou": ("post/200-wagons-miniatures-imprimés-en-3d-pour-l-attraction-loup-garou-de-walibi",
   "200 wagons miniatures pour Walibi Belgium | O&D Impression 3D", "Wagons Loup-Garou — Walibi",
   "200 wagons miniatures imprimés en 3D pour l'attraction Loup-Garou de Walibi Belgium : 100 bleus, 100 rouges, numérotés et montés sur plaques."),
 "réalisations/faucon-bas-relief-jean-pierre-craninx": ("post/un-faucon-en-bas-relief-imprimé-en-3d-pour-l-artiste-jean-pierre-craninx",
   "Faucon en bas-relief pour Jean-Pierre Craninx | O&D Impression 3D", "Faucon — J-P Craninx",
   "Un faucon en bas-relief imprimé en 3D pour l'artiste Jean-Pierre Craninx, exposé à Saint-Jean-Cap-Ferrat."),
}
for path, (src, title, lab, desc) in NEW_REAL.items():
    s_ = BY.get(src, {"native": []})
    np_ = {"path": path, "title": title, "desc": desc, "native": s_["native"], "embed": [], "new": True, "from_post": src}
    P.append(np_); BY[path] = np_; NICE[path] = lab
REAL[:] = [x for x in REAL if x["path"] not in NEW_REAL] + [BY[p] for p in NEW_REAL]
RDATA = json.load(open(ROOT / "content" / "realisations.json", encoding="utf-8"))

def rimg(depth, base, size, alt, cls="", lazy=True, sizes=""):
    pre = "../" * depth; w, h = size
    return (f'<picture class="{cls}"><source srcset="{pre}{base}.webp" type="image/webp"><img src="{pre}{base}.jpg" alt="{E(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + "></picture>")

def photo_thumb(depth, path, alt):
    if path not in REALIMG or not REALIMG[path]: return ""
    base, size = REALIMG[path][0]
    return f'<span class="thumb photo">{rimg(depth, base, size, alt)}</span>'

_hub_grid_orig = hub_grid
def hub_grid(depth, items, kind):
    cards = []
    for ix, x in enumerate(items, 1):
        th = photo_thumb(depth, x["path"], label(x)) or pic(depth, x["path"], label(x), "thumb")
        cards.append(f'<a class="panel spot lcard rv{" with-img" if th else ""}" href="{rel(depth, x["path"])}">{th}<span class="k">{kind} · {ix:02d}</span><h3>{E(label(x))}</h3><p>{E(short(x.get("desc", ""), 150))}</p><span class="go">Ouvrir la fiche →</span></a>')
    return '<div class="grid g3">' + "".join(cards) + "</div>"

def gallery(depth, path, alt, caps=None):
    imgs = REALIMG.get(path, [])
    if not imgs: return ""
    caps = caps or []
    out = []
    for i, (b, s) in enumerate(imgs, 1):
        c = caps[i - 1] if i <= len(caps) else ""
        out.append(f'<figure class="gal-f rv"><a class="gal-i" href="{"../" * depth}{b}.jpg" data-full="{"../" * depth}{b}.jpg">{rimg(depth, b, s, c or f"{alt} — photo {i}")}</a>'
                   + (f'<figcaption>{E(c)}</figcaption>' if c else "") + "</figure>")
    return f'<div class="gallery g{min(len(imgs), 4)}">{"".join(out)}</div>'

def real_section(n, s):
    body = "".join(f"<p>{E(x)}</p>" for x in s.get("paras", []))
    body += "".join(f'<div class="hl panel">{E(x)}</div>' for x in s.get("hl", []))
    if s.get("specs"):
        body += '<div class="rspecs">' + "".join(f'<div class="rspec panel"><span class="hud">{E(k)}</span><b>{E(v)}</b></div>' for k, v in s["specs"]) + "</div>"
    if s.get("machines"):
        body += '<div class="rmach">' + "".join(f'<div class="panel rm"><span class="hud">{E(m.get("tag", ""))}</span><h3>{E(m["name"])}</h3><p>{E(m.get("detail", ""))}</p></div>' for m in s["machines"]) + "</div>"
    if s.get("comm"):
        body += '<blockquote class="comm panel">' + "".join(f"<p>{E(x)}</p>" for x in s["comm"]) + "</blockquote>"
    return sec(f"{n:02d}", E(s["h2"]), f'<div class="rbody prose">{body}</div>', s.get("tag"))

def gen_real(p):
    d = depth_of(p["path"]); name = label(p)
    R = RDATA.get(p["path"])
    if not R:
        m = build_model(p)
        R = {"ey": "Réalisation client", "h1": m["title"], "lead": m["lead"] or p["desc"], "captions": [], "sections": [], "nda": "", "_m": m}
    cover = ""
    if REALIMG.get(p["path"]):
        b, s = REALIMG[p["path"]][0]
        cover = f'<div class="pvis photo-hero"><div class="frame">{rimg(d, b, s, R["h1"], lazy=False)}</div></div>'
    out = (f'<section class="phero has-img"><div class="wrap">{crumbs(p["path"], d)}<div class="split"><div><div class="hud eyebrow">{E(R["ey"])}</div>'
           f'<h1>{E(R["h1"])}</h1><p class="lead">{E(R["lead"])}</p></div>{cover}</div></div></section>')
    g = gallery(d, p["path"], name, R.get("captions"))
    n = 1
    if g:
        out += sec(f"{n:02d}", E(R.get("photo_title") or "Le projet en images"), g, R.get("photo_tag") or "Photos du projet"); n += 1
    for s_ in R["sections"]:
        out += real_section(n, s_); n += 1
    if R.get("_m"): out += render_sections(R["_m"], start=n)
    if R.get("nda"):
        out += f'<section class="tight"><div class="wrap"><p class="nda hud">{E(R["nda"])}</p></div></section>'
    others = [x for x in REAL if x["path"] != p["path"]][:6]
    out += sec("→", "D'autres projets", hub_grid(d, others, "Projet"))
    out += cta(d, "Un projet <span class='glow'>similaire ?</span>", "Envoyez-nous votre pièce, votre fichier ou une simple photo : réponse sous 24 h.")
    write(p["path"], head(p["path"], d, p["title"], p["desc"]) + chrome(p["path"], d) + out + footer(d))

def events_section(depth, no="◆"):
    if not EVENTS: return ""
    items = "".join(f'<figure class="ev rv">{rimg(depth, b, s, c)}<figcaption class="hud">{E(c)}</figcaption></figure>' for b, s, c in EVENTS)
    return sec(no, "Sur le <span class='glow'>terrain.</span>", f'<div class="events">{items}</div>', "Salons & événements",
               right='<p class="lead">On va à la rencontre de l\'industrie : Euronaval pour le naval et la défense, Formnext pour la fabrication additive, Batibouw pour la construction.</p>')

def team_photo(depth, name):
    if name not in TEAM: return ""
    b, s = TEAM[name]
    return f'<div class="avatar">{rimg(depth, b, s, name)}</div>'
