# Écosystèmes technologiques + fiches machines / matières structurées (chargé par build.py)

# ---------------------------------------------------------------- données de la page « Machines & Matières »
NAME2SLUG = {
 "SuperMaker 3D 1518": "supermaker-sls1518", "SuperMaker 3D 3540": "supermaker-sls3540-pro",
 "Rilsan PA11": "pa11-rilsan", "Nylon PA12 (série)": "sls-nylon-pa12-serie", "Nylon PA12 (gris)": "sls-nylon-pa12-gris",
 "PA11": "sls-ultrasint-pa11", "PA11 CF": "sls-ultrasint-pa11-cf", "PA11 ESD": "sls-ultrasint-pa11-esd",
 "PA12 - GF (Glass Fiber)": "sls-pa12-charge-verre", "PA2210 FR": "sls-pa2210-fr", "PA12 (Grade alimentaire)": "sls-pa12-grade-alimentaire",
 "TPU 88A": "sls-ultrasint-tpu-88a", "Bambu Lab X1C": "bambu-lab-x1c", "Bambu Lab H2C": "bambu-lab-h2c", "Modix Big Meter": "modix-big-meter",
 "Prusa Core one": "prusa-core-one", "INTAMSYS Funmat HT": "intamsys-funmat-ht", "PLA": "pla", "PETG": "petg", "TPU": "tpu", "ABS": "abs", "ASA": "asa",
 "PA12-CF (Nylon fibre de carbone)": "pa12-cf", "PA12-GF (Nylon fibre de verre)": "pa12-gf", "PP (Polypropylène)": "pp", "PPS-CF": "pps-cf",
 "PEEK/CF-GF": "peek", "PEKK/CF-GF": "pekk", "ULTEM": "ultem-pei", "Carvera Ultimate Makera": "makera-carvera", "xTool F1": "xtool-f1",
 "Anycubic Photon Mono M7 Max": "anycubic-photon-m7-max", "SMS 3DeVOK MT": "scanner-3devok-mt"}
HUBDATA = {}
def _parse_hub():
    cur = None; mode = None
    for b in BY["machines-materiaux"]["native"]:
        t, v = b["t"], b.get("v")
        if t == "h2" and v in NAME2SLUG:
            cur = HUBDATA.setdefault(NAME2SLUG[v], {"name": v, "tag": None, "specs": [], "feat": [], "adv": [], "lim": []}); mode = None; continue
        if cur is None: continue
        if t in ("h2", "h3", "p") and isinstance(v, str):
            if "Avantages" in v: mode = "adv"; continue
            if "Limites" in v: mode = "lim"; continue
            if v.startswith("NOS ") or v.startswith("LE COMPARATIF"): cur = None; continue
            if not cur["tag"]: cur["tag"] = v.rstrip(" :")
            continue
        if t == "ul":
            if mode in ("adv", "lim"): cur[mode] += v; mode = None; continue
            for x in v:
                if " : " in x or ": " in x:
                    k, _, val = x.partition(":"); cur["specs"].append((k.strip(), val.strip()))
                else: cur["feat"].append(x)
_parse_hub()

TECH = {
 "sls": {"name": "SLS", "long": "Frittage laser sélectif", "url": "services/impression-3d-sls",
   "machines": ["supermaker-sls1518", "supermaker-sls3540-pro"],
   "mats": ["sls-nylon-pa12-gris", "sls-nylon-pa12-serie", "pa11-rilsan", "sls-ultrasint-pa11", "sls-ultrasint-pa11-cf", "sls-ultrasint-pa11-esd",
            "sls-pa12-charge-verre", "sls-pa2210-fr", "sls-pa12-grade-alimentaire", "sls-ultrasint-tpu-88a"],
   "steps": [("Une couche de poudre", "Une fine couche de poudre de nylon est étalée dans la chambre de la machine."),
             ("Le laser dessine", "Un laser fait fondre la poudre uniquement là où la pièce doit exister."),
             ("Couche après couche", "On recommence jusqu'en haut. La poudre non fondue soutient la pièce : aucun support à retirer.")],
   "ideal": ["Pièces fonctionnelles et mécaniques", "Formes complexes, canaux internes, charnières intégrées", "Petites séries : des dizaines de pièces par cycle", "Pièces résistantes aux chocs et à l'usure"],
   "limits": ["Surface légèrement granuleuse (finitions possibles)", "Couleurs limitées : blanc, gris ou noir selon la poudre", "Volume max. 350 × 350 × 430 mm"],
   "comp": ["comparateur-materiaux/fdm-sls-resine", "comparateur-materiaux/pa12cf-pa12gf"]},
 "fdm": {"name": "FDM", "long": "Dépôt de fil fondu", "url": "services/impression-3d-fdm",
   "machines": ["bambu-lab-h2c", "bambu-lab-x1c", "prusa-core-one", "modix-big-meter", "intamsys-funmat-ht"],
   "mats": ["pla", "petg", "abs", "asa", "tpu", "pp", "pa12-cf", "pa12-gf", "pps-cf", "peek", "pekk", "ultem-pei"],
   "steps": [("Le fil fond", "Une bobine de plastique alimente une buse chauffée qui fait fondre la matière."),
             ("La buse trace", "La buse dépose la matière ligne par ligne, comme un stylo 3D piloté par ordinateur."),
             ("Couche après couche", "La pièce monte couche par couche, du PLA économique jusqu'au PEEK haute performance.")],
   "ideal": ["Prototypes rapides et économiques", "Très grand choix de matières, du PLA au PEEK et à l'ULTEM", "Grandes pièces (Modix Big Meter)", "Pièces multi-couleurs et multi-matières"],
   "limits": ["Lignes de couche visibles", "Résistance plus faible entre les couches : l'orientation compte", "Supports nécessaires pour les parties en surplomb"],
   "comp": ["comparateur-materiaux/fdm-sls-resine", "comparateur-materiaux/pla-petg", "comparateur-materiaux/abs-asa", "comparateur-materiaux/pa12cf-pa12gf",
            "comparateur-materiaux/comparateur-ppa-cf-vs-pps-cf", "comparateur-materiaux/peek-pekk-ultem"]},
 "resine": {"name": "Résine", "long": "Photopolymérisation (MSLA)", "url": "services/impression-3d-resine",
   "machines": ["anycubic-photon-m7-max"], "mats": [],
   "steps": [("Une cuve de résine", "La pièce est fabriquée dans une cuve de résine liquide."),
             ("La lumière durcit", "Un écran UV durcit une couche entière d'un seul coup, avec une très grande finesse."),
             ("Lavage et cuisson", "La pièce est lavée puis post-polymérisée pour atteindre ses propriétés finales.")],
   "ideal": ["Détails très fins", "Surfaces lisses dès la sortie de machine", "Maquettes, figurines, prototypes d'aspect", "Masters pour moulage"],
   "limits": ["Plus fragile que le nylon ou les filaments techniques", "Sensible aux UV sur la durée", "Volume max. 298 × 300 × 164 mm"],
   "comp": ["comparateur-materiaux/fdm-sls-resine"]},
 "cnc": {"name": "CNC", "long": "Usinage à commande numérique", "url": "services/usinage-cnc",
   "machines": ["tooldance-x1-cnc"],
   "mats": ["cnc-aluminium", "cnc-laiton", "cnc-bronze", "cnc-titane", "cnc-pom", "cnc-ertalon"],
   "steps": [("Un bloc de matière", "On part d'un bloc brut : aluminium, laiton, plastique technique…"),
             ("La fraise enlève", "Une fraise tournant à grande vitesse retire la matière en suivant votre fichier 3D."),
             ("Une pièce dans la masse", "On obtient une pièce pleine, précise, avec un bel état de surface.")],
   "ideal": ["Pièces en métal", "Ajustements et alésages précis", "Pièces mécaniques soumises à l'usure ou à la chaleur", "Plaques, supports, petites séries"],
   "limits": ["Certaines formes internes sont impossibles (réservées à l'impression 3D)", "Plus de chutes de matière qu'en impression 3D", "Taille limitée par le plateau de la machine"],
   "comp": []},
}
OTHER_MACH = ["scanner-3devok-mt", "xtool-f1"]
def tech_of(slug):
    for k, t in TECH.items():
        if slug in t["machines"] or slug in t["mats"]: return k
    return None

# ---------------------------------------------------------------- nouvelles pages (CNC + machine Carvera + écosystèmes)
CNC_MATS = {
 "cnc-aluminium": ("Aluminium", "Léger · Usinable · Polyvalent", "Le métal le plus utilisé en usinage : léger, facile à travailler et naturellement résistant à la corrosion.",
   [("Densité", "≈ 2,7 g/cm³"), ("Usinabilité", "Excellente"), ("Résistance à la corrosion", "Bonne (anodisation possible)"), ("Conductivité", "Thermique et électrique élevées")],
   ["Léger : environ trois fois moins dense que l'acier", "Facile et rapide à usiner", "Bonne résistance à la corrosion", "Anodisable (couleurs, protection)"],
   ["Moins dur que l'acier", "Rayable sans traitement de surface"], ["Supports et platines", "Boîtiers", "Pièces de machines", "Prototypes métalliques"], "Al"),
 "cnc-laiton": ("Laiton", "Usinable · Esthétique · Conducteur", "Alliage cuivre-zinc très agréable à usiner, au bel aspect doré.",
   [("Densité", "≈ 8,5 g/cm³"), ("Usinabilité", "Excellente"), ("Aspect", "Doré, polissable"), ("Frottement", "Faible")],
   ["Usinage très précis et propre", "Bel aspect décoratif", "Bonne conductivité électrique", "Faible frottement"], ["Lourd", "S'oxyde (ternit) sans protection"],
   ["Raccords et inserts", "Pièces décoratives", "Contacts électriques", "Petites pièces mécaniques"], "CuZn"),
 "cnc-bronze": ("Bronze", "Anti-usure · Autolubrifiant · Durable", "Alliage cuivre-étain apprécié pour les pièces qui frottent.",
   [("Densité", "≈ 8,8 g/cm³"), ("Frottement", "Très faible"), ("Résistance à l'usure", "Élevée")],
   ["Excellente résistance à l'usure", "Faible coefficient de frottement", "Bonne résistance à la corrosion"], ["Lourd", "Plus coûteux que le laiton"],
   ["Bagues et coussinets", "Paliers", "Pièces de friction"], "CuSn"),
 "cnc-titane": ("Titane", "Ultra-résistant · Léger · Biocompatible", "Rapport résistance / poids exceptionnel, pour les applications les plus exigeantes.",
   [("Densité", "≈ 4,5 g/cm³"), ("Résistance mécanique", "Très élevée"), ("Corrosion", "Excellente"), ("Biocompatibilité", "Oui")],
   ["Rapport résistance / poids exceptionnel", "Excellente résistance à la corrosion", "Biocompatible"], ["Difficile à usiner", "Matière coûteuse"],
   ["Aéronautique et sport", "Médical", "Pièces légères très sollicitées"], "Ti"),
 "cnc-pom": ("POM (Delrin®)", "Glissant · Stable · Précis", "Plastique technique rigide et glissant, idéal pour les pièces mécaniques en mouvement.",
   [("Densité", "≈ 1,4 g/cm³"), ("Frottement", "Très faible"), ("Stabilité dimensionnelle", "Excellente"), ("Absorption d'eau", "Très faible")],
   ["Très faible frottement", "Excellente stabilité dimensionnelle", "Usinage très précis", "Bonne résistance à l'usure"], ["Difficile à coller", "Sensible aux UV en extérieur"],
   ["Engrenages", "Glissières et guides", "Bagues", "Pièces de précision"], "POM"),
 "cnc-ertalon": ("Ertalon® (PA6)", "Tenace · Anti-usure · Amortissant", "Polyamide technique usinable, tenace et résistant à l'usure.",
   [("Famille", "Polyamide 6 (nylon)"), ("Densité", "≈ 1,15 g/cm³"), ("Résistance à l'usure", "Élevée"), ("Ténacité", "Élevée")],
   ["Très tenace et résistant aux chocs", "Bonne résistance à l'usure", "Amortit les vibrations"], ["Absorbe l'humidité (cotes qui varient)", "Moins stable que le POM"],
   ["Rouleaux et poulies", "Pièces d'usure", "Patins et guides"], "PA6"),
}
for slug, (name, tag, intro, *_r) in CNC_MATS.items():
    P.append({"path": "machines-materiaux/" + slug, "title": f"Usinage CNC {name} | O&D Impression 3D",
              "desc": f"{name} usiné en CNC à Welkenraedt (Liège) : {intro[0].lower() + intro[1:]}", "native": [], "embed": [], "new": True})
P.append({"path": "services/impression-3d-fdm", "title": "Impression 3D FDM en Belgique | O&D Impression 3D",
          "desc": "Impression 3D FDM à Welkenraedt (Liège) : prototypes, pièces techniques et grandes pièces, du PLA au PEEK et à l'ULTEM. Devis sous 24 h.", "native": [], "embed": [], "new": True})
P.append({"path": "services/usinage-cnc", "title": "Usinage CNC aluminium, laiton & plastiques | O&D Impression 3D",
          "desc": "Usinage CNC à Welkenraedt (Liège) : aluminium, laiton, bronze, titane, POM, Ertalon. Pièces précises à l'unité ou en petite série.", "native": [], "embed": [], "new": True})
for p in P[-9:]: BY[p["path"]] = p
SERVICES[:] = [p for p in P if p["path"].startswith("services/")]
ALLM = [m for t in TECH.values() for m in t["machines"]] + OTHER_MACH
MACH[:] = [BY["machines-materiaux/" + s] for s in ALLM if "machines-materiaux/" + s in BY]
ALLT = [m for t in TECH.values() for m in t["mats"]]
MATS[:] = [BY["machines-materiaux/" + s] for s in ALLT if "machines-materiaux/" + s in BY]


NICE = {"supermaker-sls1518": "Supermaker SLS1518", "supermaker-sls3540-pro": "Supermaker SLS3540 Pro", "sls-nylon-pa12-gris": "Nylon PA12 gris",
        "sls-nylon-pa12-serie": "Nylon PA12 série", "pa11-rilsan": "Rilsan PA11", "sls-ultrasint-pa11": "PA11", "sls-ultrasint-pa11-cf": "PA11 CF",
        "sls-ultrasint-pa11-esd": "PA11 ESD", "sls-pa12-charge-verre": "PA12 chargé verre", "sls-pa2210-fr": "PA2210 FR", "sls-pa12-grade-alimentaire": "PA12 alimentaire",
        "sls-ultrasint-tpu-88a": "TPU 88A", "pa12-cf": "PA12-CF", "pa12-gf": "PA12-GF", "pps-cf": "PPS-CF", "peek": "PEEK", "pekk": "PEKK", "ultem-pei": "ULTEM (PEI)",
        "pla": "PLA", "petg": "PETG", "abs": "ABS", "asa": "ASA", "tpu": "TPU", "pp": "PP", "bambu-lab-h2c": "Bambu Lab H2C", "bambu-lab-x1c": "Bambu Lab X1C",
        "prusa-core-one": "Prusa Core One", "modix-big-meter": "Modix Big Meter", "intamsys-funmat-ht": "INTAMSYS Funmat HT", "anycubic-photon-m7-max": "Anycubic Photon M7 Max",
        "makera-carvera": "Makera Carvera", "tooldance-x1-cnc": "ToolDance X1", "scanner-3devok-mt": "Scanner 3DeVOK MT", "xtool-f1": "xTool F1",
        "services/impression-3d-sls": "Impression 3D SLS", "services/impression-3d-fdm": "Impression 3D FDM", "services/impression-3d-resine": "Impression 3D résine", "services/usinage-cnc": "Usinage CNC"}
_old_label = label
def label(p):
    s = p["path"].split("/", 1)[-1]
    if s in NICE: return NICE[s]
    if p["path"] in NICE: return NICE[p["path"]]
    if s in CNC_MATS: return CNC_MATS[s][0]
    return _old_label(p)

# ---------------------------------------------------------------- briques de rendu
def tag_chip(depth, tk):
    t = TECH[tk]; return f'<a class="chip tech" href="{rel(depth, t["url"])}">{t["name"]} · {t["long"]}</a>'

def mini_cards(depth, slugs, kind):
    items = [BY["machines-materiaux/" + s] for s in slugs if "machines-materiaux/" + s in BY]
    cards = []
    for x in items:
        s = x["path"].split("/")[-1]; th = pic(depth, x["path"], label(x), "thumb") or symbol_tile(s)
        tagl = (HUBDATA.get(s, {}).get("tag") or (CNC_MATS[s][1] if s in CNC_MATS else "") or "")
        cards.append(f'<a class="panel spot lcard rv with-img" href="{rel(depth, x["path"])}">{th}<span class="k">{kind}</span><h3>{E(label(x))}</h3><p>{E(tagl)}</p><span class="go">Voir la fiche →</span></a>')
    return '<div class="grid g4">' + "".join(cards) + "</div>"

def symbol_tile(s):
    if s not in CNC_MATS: return ""
    return f'<span class="thumb sym"><b>{CNC_MATS[s][7]}</b></span>'

def spec_table(rows):
    return '<div class="panel tscroll"><table class="specs">' + "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in rows) + "</table></div>"

def pros_cons(adv, lim):
    if not adv and not lim: return ""
    a = '<div class="panel rv"><div class="hud" style="margin-bottom:1rem;color:var(--ok)">Avantages</div><ul class="list">' + "".join(f"<li>{E(x)}</li>" for x in adv) + "</ul></div>" if adv else ""
    l = '<div class="panel rv"><div class="hud" style="margin-bottom:1rem;color:var(--amber)">Limites</div><ul class="list neg">' + "".join(f"<li>{E(x)}</li>" for x in lim) + "</ul></div>" if lim else ""
    return f'<div class="grid g2">{a}{l}</div>'

def sec(no, title, inner, eyebrow=None, right=""):
    eb = f" — {E(eyebrow)}" if eyebrow else ""
    return f'<section><div class="wrap"><div class="sec-head"><div><div class="sec-no">[ {no} ]{eb}</div><h2 class="rv">{title}</h2></div>{right}</div>{inner}</div></section>'

def more_details(m):
    body = render_sections(m)
    if not body.strip(): return ""
    return f'<section style="padding-top:20px"><div class="wrap"><details class="more panel"><summary><span class="hud">Description détaillée</span><span>Tout savoir — cliquez pour déplier</span></summary><div class="more-in">{body}</div></details></div></section>'

def digits(s): return re.sub(r"\D", "", s)

def embed_struct(p):
    """specs kv + avantages/limites depuis le bloc HTML de la fiche."""
    kv = []; adv = []; lim = []; mode = None
    for b in p["embed"]:
        if b["t"] == "kv": kv.append((b["k"], b["v"])); continue
        v = b.get("v") if isinstance(b.get("v"), str) else None
        if v is None: continue
        if re.match(r"^Avantages$", v): mode = "adv"; continue
        if re.match(r"^(Limites|Inconvénients)$", v): mode = "lim"; continue
        if v.startswith("O&D Impression 3D") or v.isupper(): mode = None if v.startswith("O&D") else mode; continue
        if mode == "adv" and b["t"] in ("txt", "p"): adv.append(v)
        elif mode == "lim" and b["t"] in ("txt", "p"): lim.append(v)
    return kv, adv, lim

def lead_of(p):
    for b in p["native"]:
        if b["t"] == "p" and len(b["v"]) > 90: return b["v"]
    return p["desc"]

def detail_model(p):
    """modèle 'description détaillée' : contenu natif d'origine (pour le SEO), replié."""
    m = build_model({**p, "embed": []})
    return m

# ---------------------------------------------------------------- générateurs
def gen_machine(p):
    s = p["path"].split("/")[-1]; d = depth_of(p["path"]); tk = tech_of(s); hub = HUBDATA.get(s, {})
    kv, adv, lim = embed_struct(p)
    rows = list(hub.get("specs", []))
    for k, v in kv:
        if any(digits(v) and digits(v) == digits(hv) for _, hv in rows): continue
        rows.append((k, v))
    feats = hub.get("feat", [])
    chip = tag_chip(d, tk) if tk else ""
    lead = lead_of(p) if p["native"] else p["desc"]
    m = {"title": label(p), "eyebrow": None, "lead": lead, "stats": []}
    after = f'<div class="chips" style="margin-top:1.4rem">{chip}</div>'
    out = page_hero(p, d, m, after)
    if rows or feats:
        inner = (spec_table(rows) if rows else "") + (('<div class="chips" style="margin-top:1rem">' + "".join(f'<span class="chip">{E(x)}</span>' for x in feats) + "</div>") if feats else "")
        out += sec("01", "Fiche technique", inner, NICE.get(s, label(p)))
    if adv or lim: out += sec("02", "Points forts &amp; limites", pros_cons(adv, lim))
    if tk and TECH[tk]["mats"]:
        mats = TECH[tk]["mats"]
        if s == "intamsys-funmat-ht": mats = ["peek", "pekk", "ultem-pei", "pps-cf", "pa12-cf", "pa12-gf"]
        elif tk == "fdm": mats = [x for x in mats if x not in ("peek", "pekk", "ultem-pei")]
        out += sec("03", "Matériaux compatibles", mini_cards(d, mats, "Matériau " + TECH[tk]["name"]))
    if tk:
        others = [x for x in TECH[tk]["machines"] if x != s]
        if others: out += sec("04", f'Les autres machines {TECH[tk]["name"]}', mini_cards(d, others, "Machine " + TECH[tk]["name"]))
        out += sec("05", f'Tout l\'écosystème {TECH[tk]["name"]}', f'<a class="btn btn-g" href="{rel(d, TECH[tk]["url"])}">Tout savoir sur {art(TECH[tk])} : machines, matières, comparatifs <span class="a">→</span></a>')
    if p["native"]: out += more_details(detail_model(p))
    out += cta(d)
    write(p["path"], head(p["path"], d, p["title"], p["desc"]) + chrome(p["path"], d) + out + footer(d))

def gen_material(p):
    s = p["path"].split("/")[-1]; d = depth_of(p["path"]); tk = tech_of(s); hub = HUBDATA.get(s, {})
    if s in CNC_MATS:
        name, tag, intro, rows, adv, lim, apps, sym = CNC_MATS[s]
    else:
        kv, eadv, elim = embed_struct(p)
        name, tag, intro, rows = label(p), hub.get("tag", ""), p["desc"], kv
        adv, lim, apps = hub.get("adv") or eadv, hub.get("lim") or elim, []
    m = {"title": name, "eyebrow": None, "lead": intro, "stats": []}
    after = f'<div class="chips" style="margin-top:1.4rem">{tag_chip(d, tk) if tk else ""}{"<span class=chip>" + E(tag) + "</span>" if tag else ""}</div>'
    out = page_hero(p, d, m, after)
    if s in CNC_MATS and p["path"] not in IMG:
        out = out.replace('<section class="phero">', '<section class="phero has-sym">', 1)
    if rows: out += sec("01", "Fiche technique", spec_table(rows), name)
    out += sec("02", "Avantages &amp; limites", pros_cons(adv, lim)) if (adv or lim) else ""
    if apps: out += sec("03", "Applications", '<div class="chips">' + "".join(f'<span class="chip">{E(x)}</span>' for x in apps) + "</div>")
    if tk:
        ms = TECH[tk]["machines"]
        if tk == "fdm": ms = ["intamsys-funmat-ht"] if s in ("peek", "pekk", "ultem-pei") else [x for x in ms if x != "intamsys-funmat-ht"] + (["intamsys-funmat-ht"] if s in ("pps-cf", "pa12-cf", "pa12-gf") else [])
        out += sec("04", "Machines compatibles", mini_cards(d, ms, "Machine " + TECH[tk]["name"]))
        others = [x for x in TECH[tk]["mats"] if x != s][:8]
        out += sec("05", f'Autres matières {TECH[tk]["name"]}', mini_cards(d, others, "Matériau " + TECH[tk]["name"]),
                   right=f'<p><a class="btn btn-g" href="{rel(d, TECH[tk]["url"])}">Écosystème {TECH[tk]["name"]} <span class="a">→</span></a></p>')
    if p["native"]: out += more_details(detail_model(p))
    out += cta(d)
    write(p["path"], head(p["path"], d, p["title"], p["desc"]) + chrome(p["path"], d) + out + footer(d))

def reals_for(tk):
    keys = {"fdm": r"PLA|ASA|PAHT|polypropyl|bicolore|FDM|PETG|TPU|semelle|hachoir|coffret|Infrabel|rails", "sls": r"SLS|PA12|nylon", "resine": r"résine", "cnc": r"CNC|usin"}[tk]
    return [x for x in REAL if re.search(keys, x["title"] + " " + x["desc"], re.I)]

def art(t, cap=False):
    a = {"Résine": "la résine", "CNC": "l’usinage CNC"}.get(t["name"], "le " + t["name"])
    return a[0].upper() + a[1:] if cap else a

def gen_eco(tk):
    t = TECH[tk]; p = BY[t["url"]]; d = depth_of(t["url"])
    hero_img = {"sls": "machines-materiaux/supermaker-sls3540-pro", "fdm": "machines-materiaux/bambu-lab-h2c", "resine": "machines-materiaux/anycubic-photon-m7-max", "cnc": "machines-materiaux/tooldance-x1-cnc"}[tk]
    title = {"sls": "Impression 3D SLS", "fdm": "Impression 3D FDM", "resine": "Impression 3D résine", "cnc": "Usinage CNC"}[tk]
    lead = {"sls": "Le frittage laser transforme de la poudre de nylon en pièces solides et fonctionnelles, sans aucun support. C'est la technologie des pièces techniques et des petites séries.",
            "fdm": "La technologie d'impression 3D la plus répandue : un fil de plastique fondu, déposé couche par couche. Du prototype en PLA à la pièce aéronautique en PEEK.",
            "resine": "Une résine liquide durcie par la lumière, pour des pièces d'une finesse et d'un état de surface inégalés.",
            "cnc": "Quand la pièce doit être en métal ou d'une grande précision, on l'usine dans la masse. Complément idéal de l'impression 3D."}[tk]
    img = pic(d, hero_img, title, "pimg", lazy=False)
    nav = "".join(f'<a class="chip{" on" if k == tk else ""}" href="{rel(d, v["url"])}">{v["name"]}</a>' for k, v in TECH.items())
    hero = (f'<section class="phero has-img"><div class="wrap">{crumbs(t["url"], d)}<div class="split"><div><div class="hud eyebrow">Écosystème {t["name"]} — {t["long"]}</div>'
            f'<h1>{title}</h1><p class="lead">{lead}</p><div class="chips eco-nav" style="margin-top:1.4rem">{nav}</div>'
            f'<div class="cta-row" style="margin-top:1.6rem"><a class="btn btn-p" href="{rel(d,"devis-instantane")}">Devis instantané <span class="a">→</span></a><a class="btn btn-g" href="#machines">Machines &amp; matières</a></div></div>'
            f'<div class="pvis"><div class="halo"></div>{img}</div></div></div></section>')
    steps = '<div class="steps">' + "".join(f'<div class="panel rv n"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in t["steps"]) + '<div class="panel hot rv"><h3>Votre pièce</h3><p>Envoyez votre fichier : nous confirmons que ' + art(t) + " est le bon choix, ou nous vous orientons vers une autre technologie.</p></div></div>"
    out = hero + sec("01", f'{art(t, True)} en 3 étapes', steps, "En clair")
    out += sec("02", "Quand le choisir ?", pros_cons(t["ideal"], t["limits"]).replace(">Avantages<", ">Idéal pour<").replace(">Limites<", ">Moins adapté si<"))
    out += f'<div id="machines"></div>' + sec("03", f'Nos machines {t["name"]}', mini_cards(d, t["machines"], "Machine " + t["name"]))
    if t["mats"]: out += sec("04", f'Nos matières {t["name"]}', mini_cards(d, t["mats"], "Matériau " + t["name"]))
    comps = [BY[c] for c in t["comp"] if c in BY]
    if comps: out += sec("05", "Comparer pour mieux choisir", hub_grid(d, comps, "Comparatif"))
    rs = reals_for(tk)
    if rs: out += sec("06", "Projets réalisés", hub_grid(d, rs[:6], "Projet"))
    faqs = [b for b in p["native"] + p["embed"] if b["t"] == "faq"]
    if faqs: out += sec("07", "Questions fréquentes", '<div class="faq">' + "".join(f"<details><summary>{E(q['q'])}</summary><p>{E(q['a'])}</p></details>" for q in faqs) + "</div>")
    if p["native"] or p["embed"]:
        m = build_model(p); m["sections"] = [x for x in m["sections"] if not any(b["t"] == "faq" for b in x["items"])]
        out += more_details(m)
    out += cta(d)
    write(t["url"], head(t["url"], d, p["title"], p["desc"], faq_ld(p)) + chrome(t["url"], d) + out + footer(d))

def tech_picker(depth):
    cards = []
    for k, t in TECH.items():
        im = {"sls": "machines-materiaux/supermaker-sls3540-pro", "fdm": "machines-materiaux/bambu-lab-h2c", "resine": "machines-materiaux/anycubic-photon-m7-max", "cnc": "machines-materiaux/tooldance-x1-cnc"}[k]
        cards.append(f'<a class="panel spot lcard rv with-img" href="{rel(depth, t["url"])}">{pic(depth, im, t["name"], "thumb")}<span class="k">{t["long"]}</span><h3 style="font-size:2rem">{t["name"]}</h3>'
                     f'<p>{E(t["ideal"][0])} · {E(t["ideal"][1])}</p><span class="go">{len(t["machines"])} machine{"s" if len(t["machines"])>1 else ""}{(" · " + str(len(t["mats"])) + " matières") if t["mats"] else ""} →</span></a>')
    return '<div class="grid g4">' + "".join(cards) + "</div>"

def gen_parc():
    p = BY["machines-materiaux"]; d = 1
    m = {"title": "Machines &amp; matières", "eyebrow": "Parc machines", "lead": "Notre parc et nos matières, rangés par technologie. Choisissez une technologie pour tout comprendre, ou ouvrez directement une fiche.", "stats": []}
    m["title"] = "Machines & matières"
    out = page_hero(p, d, m, '<div class="chips eco-nav" style="margin-top:1.4rem">' + "".join(f'<a class="chip" href="#{k}">{t["name"]}</a>' for k, t in TECH.items()) + '<a class="chip" href="#autres">Scan &amp; laser</a></div>')
    out += sec("00", "Choisir une technologie", tech_picker(d))
    n = 1
    for k, t in TECH.items():
        inner = f'<div class="hud" style="margin:0 0 1rem">Machines {t["name"]}</div>' + mini_cards(d, t["machines"], "Machine " + t["name"])
        if t["mats"]: inner += f'<div class="hud" style="margin:2.4rem 0 1rem">Matières {t["name"]}</div>' + mini_cards(d, t["mats"], "Matériau " + t["name"])
        out += f'<div id="{k}"></div>' + sec(f"{n:02d}", f'{t["name"]} — {t["long"]}', inner, right=f'<p><a class="btn btn-g" href="{rel(d, t["url"])}">Découvrir l’écosystème {t["name"]} <span class="a">→</span></a></p>'); n += 1
    out += '<div id="autres"></div>' + sec(f"{n:02d}", "Scan 3D &amp; gravure laser", mini_cards(d, OTHER_MACH, "Équipement"))
    out += cta(d)
    write("machines-materiaux", head("machines-materiaux", d, p["title"], p["desc"]) + chrome("machines-materiaux", d) + out + footer(d))
