# Page À propos (refonte) + fusion des pages Liège
LIEGE_MAIN, LIEGE_OLD = "a-propos/impression-3d-ville-liege", "a-propos/ou"
ZONES[:] = [z for z in ZONES if z["path"] != LIEGE_OLD]
if LIEGE_MAIN in BY:
    BY[LIEGE_MAIN]["title"] = "Impression 3D à Liège et en province de Liège | O&D Impression 3D"
    NICE[LIEGE_MAIN] = "Impression 3D à Liège & province"

FOUNDERS = [
 ("O", "Owen Schimmenti", "Owen SCHIMMENTI", "Co-fondateur · CNC Specialist & Programming",
  "Owen pilote la programmation des machines, l'usinage CNC et l'impression 3D. C'est lui qui transforme un fichier en pièce : réglages, matière, orientation, finition.",
  ["Usinage CNC", "Programmation", "Impression 3D"]),
 ("D", "Donovan Waucomont", "Donovan WAUCOMONT", "Co-fondateur · 3D Printing Specialist & Project Manager",
  "Donovan suit les projets de A à Z et s'occupe du dessin 3D : il écoute le besoin, modélise la pièce, la fait valider et reste votre interlocuteur jusqu'à la livraison.",
  ["Gestion de projet", "Dessin & modélisation 3D", "Impression 3D"]),
]
TEAM_MORE = []

TIMELINE = [
 ("2019", "Origines", "La passion avant tout", "Un projet personnel autour des motos 50 cm³ : les premiers pas dans la fabrication.", False),
 ("2021", "Fondation", "Naissance d'O&D Impression 3D", "Création officielle à Baelen, premières machines et premiers projets, depuis un garage.", False),
 ("2022", "Croissance", "Atelier à la maison, premiers clients industriels", "Une pièce reconvertie en atelier pour gagner en confort et en capacité.", False),
 ("2025", "Premier local", "Un vrai espace professionnel", "Trois pièces dédiées à l'activité. Arrivée du scan 3D et de l'usinage CNC.", False),
 ("2026", "Déménagement", "Installation à Welkenraedt", "Déménagement dans notre nouvel atelier de Welkenraedt et arrivée des SuperMaker SLS 1518 et 3540 Pro.", False),
 ("Demain", "La suite", "Le prochain chapitre", "La suite s'écrit avec vos projets.", True),
]

STRENGTHS = [
 ("Réactifs & rapides", "Une demande de devis est analysée rapidement et vous recevez une réponse claire, avec un service rapide et compétitif."),
 ("La bonne matière", "Nous sélectionnons la matière la plus adaptée aux contraintes de votre projet, au meilleur prix."),
 ("Pièces en série", "Un parc de machines toujours prêtes : nous produisons et livrons vos séries au plus vite."),
 ("Modélisation 3D", "Notre dessinateur redessine la pièce dont vous avez besoin : rapide, fiable, abordable. Rien n'est imprimé sans votre validation."),
 ("Proches de vous", "Vous êtes les bienvenus à l'atelier pour parler de vos projets. Une relation directe, sans intermédiaire."),
]

PROCESS = [
 ("Conception", [
   ("Prise de contact", "Partagez votre idée, votre besoin ou votre projet, par e-mail, téléphone ou formulaire. On vous répond rapidement pour vous orienter.", "Gratuit & sans engagement", False),
   ("Dessin & modélisation", "Vous avez un fichier 3D ? Parfait. Sinon, nous modélisons la pièce pour votre besoin fonctionnel ou esthétique.", "STL · STEP · OBJ · F3D", False),
   ("Validation du dessin", "Vous vérifiez dimensions, forme et tolérances. Rien ne démarre sans votre accord.", "Votre accord requis", True)]),
 ("Prototypage", [
   ("Impression du prototype", "Une première pièce de test dans la matière convenue, pour valider que tout est conforme avant la série.", "24 à 72 h selon complexité", False),
   ("Validation du prototype", "Vous testez assemblage, dimensions, aspect et fonction. Les ajustements sont intégrés avant la production.", "Votre accord requis", True)]),
 ("Production & livraison", [
   ("Acompte pour les séries", "Pour les grandes quantités, un acompte sécurise la commande et l'approvisionnement des matières.", "Grandes quantités uniquement", False),
   ("Impression en série", "Les machines tournent pour respecter vos délais, avec le même soin que le prototype validé.", "Contrôle qualité à chaque lot", False),
   ("Paiement du solde", "La facture finale est envoyée quand les pièces sont prêtes ; le solde est réglé avant l'envoi.", "Virement · Carte · PayPal", False),
   ("Envoi du colis", "Pièces emballées et protégées, transporteurs fiables, numéro de suivi dès l'expédition.", "Belgique & Europe", False),
   ("Réception", "Vos pièces sont entre vos mains — souvent le début d'une collaboration durable.", "✦ Projet réalisé", True)]),
]

def founder_card(d, letter, name, key, role, bio, skills):
    ph = TEAM.get(key)
    img = (f'<picture><source srcset="{"../" * d}{ph[0]}.webp" type="image/webp"><img src="{"../" * d}{ph[0]}.jpg" alt="{E(name)}, {E(role)}" width="{ph[1][0]}" height="{ph[1][1]}" loading="lazy"></picture>') if ph else ""
    first, last = name.split(" ", 1)
    return (f'<article class="fcard rv"><div class="f-photo">{img}<span class="f-lan">O&amp;D · ACCÈS ATELIER</span></div>'
            f'<div class="f-body"><span class="f-letter" aria-hidden="true">{letter}</span><div class="hud f-role">{E(role)}</div><h3><span>{E(first)}</span> {E(last)}</h3><p>{E(bio)}</p>'
            f'<div class="chips">' + "".join(f'<span class="chip">{E(s)}</span>' for s in skills) + "</div></div></article>")

def gen_about():
    p = BY["a-propos"]; d = 1
    hero = (f'<section class="phero ab-hero"><div class="wrap">{crumbs("a-propos", d)}<div class="hud eyebrow">À propos · Depuis 2021</div>'
            f'<h1>Deux passionnés,<br>un atelier,<br><span class="glow">une obsession : la pièce qui fonctionne.</span></h1>'
            f'<p class="lead">O&amp;D Impression 3D est née en 2021 à Baelen, dans la province de Liège, avant de s\'installer à Welkenraedt en 2026. '
            f'Le nom vient de ses deux fondateurs, <strong>Owen</strong> et <strong>Donovan</strong>, qui ont transformé une passion pour la fabrication numérique en un atelier professionnel au service des entreprises, des collectivités et des créateurs.</p>'
            f'<div class="stats"><div class="stat"><b>2021</b><span>Création de l\'atelier</span></div><div class="stat"><b>6</b><span>Technologies</span></div>'
            f'<div class="stat"><b>{len(MATS)}</b><span>Matières</span></div><div class="stat"><b>100 %</b><span>Fabriqué en Belgique</span></div></div></div></section>')
    founders = '<div class="fgrid">' + "".join(founder_card(d, *f) for f in FOUNDERS) + "</div>"
    if TEAM_MORE: founders += '<div class="fmore">' + "".join(f'<div class="panel"><span class="hud">L\'équipe</span><b>{E(n)}</b><span>{E(r)}</span></div>' for n, r in TEAM_MORE) + "</div>"
    out = hero + sec("01", "O &amp; D, <span class='glow'>ce sont eux.</span>", founders, "Les fondateurs",
                     right='<p class="lead">Owen + Donovan = O&amp;D. Deux profils complémentaires : la machine et le projet.</p>')
    tl = '<div class="tline">' + "".join(
        f'<div class="tl-it{" fut" if fut else ""} {"up" if i % 2 == 0 else "down"} rv" style="--i:{i}"><div class="tl-card"><span class="tl-badge">{E(b)}</span><h3>{E(t)}</h3><p>{E(x)}</p></div>'
        f'<div class="tl-node"><i></i><b>{E(y)}</b></div></div>' for i, (y, b, t, x, fut) in enumerate(TIMELINE)) + "</div>"
    out += sec("02", "Notre histoire", tl, "De 2019 à aujourd'hui")
    mission = [b["v"] for b in p["native"] if b["t"] == "p" and len(b["v"]) > 90][:5]
    if mission:
        out += sec("03", "Notre mission", '<div class="ab-mission"><blockquote class="panel">Un partenaire technique engagé aux côtés des entreprises pour transformer leurs idées en solutions concrètes et performantes.</blockquote>'
                   '<div class="prose rbody">' + "".join(f"<p>{E(x)}</p>" for x in mission[:4]) + "</div></div>", "Pourquoi on fait ça")
    st = '<div class="strengths">' + "".join(f'<div class="panel rv sg"><span class="hud">{i:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(STRENGTHS, 1)) + "</div>"
    out += sec("04", "La force d'O&amp;D", st, "Nos engagements")
    n = 0; cols = []
    for g, steps in PROCESS:
        items = []
        for (t, x, badge, imp) in steps:
            n += 1
            items.append(f'<div class="ps rv"><div class="ps-n">{n:02d}</div><div><h3 class="ps-t">{E(t)}</h3><p>{E(x)}</p><span class="ps-b{" imp" if imp else ""}">{E(badge)}</span></div></div>')
        cols.append(f'<div class="pcol"><div class="pg hud">{E(g)}</div>{"".join(items)}</div>')
    out += sec("05", "De l'idée à la pièce <span class='glow'>entre vos mains.</span>", '<div class="process">' + "".join(cols) + "</div>", "Notre processus",
               right='<p class="lead">Un accompagnement complet, de la première prise de contact jusqu\'à la livraison. Transparent, simple, professionnel.</p>')
    out += events_section(d, "06")
    zones = [z for z in ZONES if z["path"] != LIEGE_OLD]
    zones.sort(key=lambda z: 0 if z["path"] == LIEGE_MAIN else 1)
    zl = '<div class="zones">' + "".join(f'<a class="zone{" main" if z["path"] == LIEGE_MAIN else ""}" href="{rel(d, z["path"])}"><span class="hud">Zone</span><b>{E(label(z))}</b><span class="go">→</span></a>' for z in zones) + "</div>"
    zl += ('<div class="ab-addr panel"><div><span class="hud">Atelier</span><b>Rue Trois Bourdons 52E, 4840 Welkenraedt</b><span>Province de Liège · Belgique · Visites sur rendez-vous</span></div>'
           f'<a class="btn btn-g" href="{rel(d, "contact")}">Nous rendre visite <span class="a">→</span></a></div>')
    out += sec("07", "Où nous trouver", zl, "Zones desservies")
    out += cta(d)
    write("a-propos", head("a-propos", d, p["title"], p["desc"]) + chrome("a-propos", d) + out + footer(d))

def gen_liege():
    pm, po = BY[LIEGE_MAIN], BY[LIEGE_OLD]; d = depth_of(LIEGE_MAIN)
    m1, m2 = build_model(pm), build_model(po)
    def pick(m, key):
        return next((s for s in m["sections"] if s["title"] and key.lower() in s["title"].lower()), None)
    order = [(m1, "pourquoi nous choisir"), (m2, "Ce que nous faisons"), (m1, "Communes desservies"), (m2, "dans votre ville"),
             (m2, "Projets réalisés"), (m2, "disent nos clients"), (m1, "Pourquoi O&")]
    secs = [s for s in (pick(m, k) for m, k in order) if s]
    fa, fb = pick(m1, "Questions fréquentes"), pick(m2, "Tout ce que vous voulez savoir")
    if fa or fb:
        seen, items = set(), []
        for s in (fa, fb):
            for it in (s["items"] if s else []):
                q = it.get("q", "").strip().lower() if it.get("t") == "faq" else None
                if q and q in seen: continue
                if q: seen.add(q)
                items.append(it)
        secs.append({"eyebrow": "Questions fréquentes", "title": "Impression 3D à Liège et en province : vos questions", "items": items})
    m = {"title": "Impression 3D à Liège et en province de Liège", "eyebrow": "Liège · Verviers · Spa · Seraing · Huy · Eupen",
         "lead": m1["lead"] or pm["desc"], "stats": [], "sections": secs}
    desc = "Impression 3D à Liège et dans toute la province : prototypes, pièces techniques, scan 3D et modélisation depuis notre atelier de Welkenraedt. Devis sous 24 h."
    out = page_hero(pm, d, m) + render_sections(m, start=2) + cta(d)
    write(LIEGE_MAIN, head(LIEGE_MAIN, d, pm["title"], desc) + chrome(LIEGE_MAIN, d) + out + footer(d))
    # ancienne URL : redirection vers la page fusionnée (à remplacer par une 301 lors du passage sur Wix)
    url = "../" * depth_of(LIEGE_OLD) + LIEGE_MAIN + "/"
    write(LIEGE_OLD, f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Impression 3D à Liège et en province de Liège</title>'
          f'<meta name="robots" content="noindex"><link rel="canonical" href="https://www.od3d.be/{LIEGE_MAIN}"><meta http-equiv="refresh" content="0; url={url}"></head>'
          f'<body><p>Cette page a été fusionnée : <a href="{url}">Impression 3D à Liège et en province de Liège</a>.</p></body></html>')
