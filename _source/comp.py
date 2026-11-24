# Comparateur de matériaux interactif (données reprises de l'outil Wix d'origine : content/comparateur.json)
CMP = json.load(open(ROOT / "content" / "comparateur.json", encoding="utf-8"))
CMP_MACH = {"Bambu Lab X1C": "bambu-lab-x1c", "Bambu Lab H2C": "bambu-lab-h2c", "Prusa Core One": "prusa-core-one", "Modix Big Meter": "modix-big-meter",
            "INTAMSYS Funmat HT": "intamsys-funmat-ht", "SuperMaker SLS 1518": "supermaker-sls1518", "SuperMaker SLS 3540 Pro": "supermaker-sls3540-pro",
            "Anycubic Photon M7 Max": "anycubic-photon-m7-max"}
CMP_FICHE = {"PLA": "pla", "PETG": "petg", "ABS": "abs", "ASA": "asa", "TPU": "tpu", "PP": "pp", "PA12-CF": "pa12-cf", "PA12-GF": "pa12-gf",
             "PPS-CF": "pps-cf", "PEEK": "peek", "PEKK": "pekk", "Ultem": "ultem-pei", "SLS-PA12": "sls-nylon-pa12-gris",
             "SLS-PA11": "sls-ultrasint-pa11", "SLS-TPU": "sls-ultrasint-tpu-88a"}
CMP_LABELS = {"impression": "Facilité d'impression", "mecanique": "Résistance mécanique", "thermique": "Résistance thermique",
              "chimique": "Résistance chimique", "uv": "Résistance aux UV", "surface": "Qualité de surface", "flexibilite": "Flexibilité"}
CMP_QUICK = [("PLA", "PETG"), ("PETG", "ABS"), ("ABS", "ASA"), ("PA12-CF", "PA12-GF"), ("PEEK", "PEKK"), ("PEEK", "Ultem"),
             ("SLS-PA12", "PA12-GF"), ("Resine-Std", "PLA"), ("TPU", "SLS-TPU"), ("PPA-CF", "PPS-CF")]
CMP_PAIRS = {"comparateur-materiaux/fdm-sls-resine": ("FDM", "SLS", "Résine"), "comparateur-materiaux/pla-petg": ("PLA", "PETG"),
             "comparateur-materiaux/abs-asa": ("ABS", "ASA"), "comparateur-materiaux/pa12cf-pa12gf": ("PA12-CF", "PA12-GF"),
             "comparateur-materiaux/comparateur-ppa-cf-vs-pps-cf": ("PPA-CF", "PPS-CF"), "comparateur-materiaux/peek-pekk-ultem": ("PEEK", "PEKK", "Ultem")}

def comp_cards(d):
    out = []
    for i, x in enumerate(COMP, 1):
        parts = CMP_PAIRS.get(x["path"], tuple(label(x).split(" vs ")))
        vs = '<span class="vs">vs</span>'.join(f'<b>{E(s)}</b>' for s in parts)
        out.append(f'<a class="panel spot ccard rv" href="{rel(d, x["path"])}"><span class="hud k">Fiche comparative · {i:02d}</span>'
                   f'<div class="cvs">{vs}</div><p>{E(short(x.get("desc", ""), 120))}</p><span class="go">Lire le comparatif →</span></a>')
    return '<div class="grid g3 ccards">' + "".join(out) + "</div>"

def gen_comp(p):
    d = depth_of(p["path"])
    data = {"m": CMP, "labels": CMP_LABELS,
            "mach": {k: rel(d, "machines-materiaux/" + v) for k, v in CMP_MACH.items()},
            "fiche": {k: rel(d, "machines-materiaux/" + v) for k, v in CMP_FICHE.items()}}
    groups = {}
    for k, m in CMP.items(): groups.setdefault(m["group"], []).append((k, m["fullName"]))
    def sel(id_, cur):
        o = "".join(f'<optgroup label="{E(g)}">' + "".join(f'<option value="{E(k)}"{" selected" if k == cur else ""}>{E(n)}</option>' for k, n in items) + "</optgroup>" for g, items in groups.items())
        return f'<select id="{id_}" class="csel">{o}</select>'
    quick = "".join(f'<button type="button" class="chip" data-a="{E(a)}" data-b="{E(b)}">{E(a.replace("Resine-Std", "Résine"))} <i>vs</i> {E(b)}</button>' for a, b in CMP_QUICK)
    hero = (f'<section class="phero"><div class="wrap">{crumbs(p["path"], d)}<div class="hud eyebrow">Outil interactif</div>'
            f'<h1>Comparateur de matériaux</h1><p class="lead">Choisissez deux matériaux : leurs points forts, leurs limites et leurs caractéristiques s\'affichent côte à côte. '
            f'{len(CMP)} matériaux FDM, SLS et résine.</p></div></section>')
    tool = (f'<div class="cmp panel" id="cmp">'
            f'<div class="cmp-pick"><label class="pick a"><span class="hud">Matériau A</span>{sel("selA", "PLA")}</label>'
            f'<button type="button" class="swap" id="swap" aria-label="Inverser A et B">⇄</button>'
            f'<label class="pick b"><span class="hud">Matériau B</span>{sel("selB", "PETG")}</label></div>'
            f'<div class="cmp-quick"><span class="hud">Comparaisons rapides</span><div class="chips">{quick}</div></div>'
            f'<div id="cmpOut" aria-live="polite"></div></div>')
    js = """<script>(function(){var D=__DATA__,M=D.m,L=D.labels;var A=document.getElementById('selA'),B=document.getElementById('selB'),O=document.getElementById('cmpOut');
function e(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function head(k,m,side){var f=D.fiche[k]?'<a class="go" href="'+D.fiche[k]+'">Fiche matériau →</a>':'';
return '<div class="ch '+side+'"><span class="hud">'+e(m.tech)+'</span><h3>'+e(m.fullName)+'</h3><p class="pro"><b>Pour</b> '+e(m.for)+'</p><p class="con"><b>Éviter si</b> '+e(m.against)+'</p>'+f+'</div>'}
function run(){var ka=A.value,kb=B.value,a=M[ka],b=M[kb];if(!a||!b)return;var wa=0,wb=0,rows='';
Object.keys(L).forEach(function(s){var va=a.scores[s]||0,vb=b.scores[s]||0;if(va>vb)wa++;else if(vb>va)wb++;
rows+='<div class="sc"><span class="lab">'+e(L[s])+'</span><div class="duo"><div class="bar a'+(va>vb?' win':'')+'"><i style="width:'+va+'%"></i><em>'+va+'</em></div><div class="bar b'+(vb>va?' win':'')+'"><i style="width:'+vb+'%"></i><em>'+vb+'</em></div></div></div>'});
var keys=[];[a.specs,b.specs].forEach(function(o){Object.keys(o||{}).forEach(function(k){if(keys.indexOf(k)<0)keys.push(k)})});
var spec=keys.map(function(k){return '<tr><td>'+e((a.specs||{})[k]||'—')+'</td><th>'+e(k)+'</th><td>'+e((b.specs||{})[k]||'—')+'</td></tr>'}).join('');
function lst(m){return (m.usages||[]).map(function(u){return '<li>'+e(u)+'</li>'}).join('')}
function mach(m){return (m.machines||[]).map(function(x){return D.mach[x]?'<a href="'+D.mach[x]+'">'+e(x)+'</a>':'<span>'+e(x)+'</span>'}).join('')}
var n=Object.keys(L).length,verdict=wa===wb?'Égalité : '+wa+' critère'+(wa>1?'s':'')+' chacun':(wa>wb?e(ka):e(kb))+' l\\u2019emporte sur '+Math.max(wa,wb)+' critère'+(Math.max(wa,wb)>1?'s':'')+' sur '+n;
O.innerHTML='<div class="cmp-heads">'+head(ka,a,'a')+head(kb,b,'b')+'</div>'+
'<div class="cmp-block"><div class="cmp-t"><span class="hud">Scores atelier /100</span><span class="verdict">'+verdict+'</span></div><div class="legend"><span class="ca">'+e(ka)+'</span><span class="cb">'+e(kb)+'</span></div>'+rows+'</div>'+
'<div class="cmp-block"><div class="cmp-t"><span class="hud">Caractéristiques</span></div><div class="tbl"><table class="ctab"><thead><tr><td class="ca">'+e(ka)+'</td><th></th><td class="cb">'+e(kb)+'</td></tr></thead><tbody>'+spec+'</tbody></table></div></div>'+
'<div class="cmp-block two"><div><span class="hud ca">Usages · '+e(ka)+'</span><ul>'+lst(a)+'</ul><div class="mach">'+mach(a)+'</div></div><div><span class="hud cb">Usages · '+e(kb)+'</span><ul>'+lst(b)+'</ul><div class="mach">'+mach(b)+'</div></div></div>';
document.querySelectorAll('.cmp-quick .chip').forEach(function(c){c.classList.toggle('on',c.dataset.a===ka&&c.dataset.b===kb)})}
A.onchange=run;B.onchange=run;document.getElementById('swap').onclick=function(){var t=A.value;A.value=B.value;B.value=t;run()};
document.querySelectorAll('.cmp-quick .chip').forEach(function(c){c.onclick=function(){A.value=c.dataset.a;B.value=c.dataset.b;run()}});run()})();</script>""".replace("__DATA__", json.dumps(data, ensure_ascii=False))
    out = hero + sec("01", "Deux matériaux, <span class='glow'>face à face.</span>", tool, "Comparateur") + js
    out += sec("02", "Les comparatifs détaillés", comp_cards(d), "Fiches", right='<p class="lead">Six duels rédigés par l\'atelier, avec tableaux complets et recommandations.</p>')
    out += cta(d)
    write(p["path"], head(p["path"], d, p["title"], p["desc"]) + chrome(p["path"], d) + out + footer(d))
