"""Extraction structurée (blocs ordonnés) de chaque page od3d.be -> content/*.json"""
import json, re, pathlib, urllib.parse, requests, time
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = pathlib.Path(__file__).parent
EMB = pathlib.Path("/home/claude/extract/out/embeds")
OUT = ROOT / "content"; OUT.mkdir(exist_ok=True)
RAW = ROOT / "raw"; RAW.mkdir(exist_ok=True)
SHARED = "4ea78211f6f9a8b687dd4d9623ca0d4d"
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"

BLOCKISH = {"div","section","article","header","footer","main","ul","ol","table","h1","h2","h3","h4","h5","p","details","li","figure","nav","aside","form","blockquote"}
def clean(t):
    t = t.replace("​", "").replace("\xa0", " ")
    return " ".join(t.split())
EMOJI = re.compile(r"^[^\w]{0,3}$")

def walk(node, out):
    for ch in node.children:
        if isinstance(ch, NavigableString):
            t = clean(str(ch))
            if t and not EMOJI.match(t): out.append({"t": "txt", "v": t})
            continue
        if not isinstance(ch, Tag): continue
        n = ch.name
        if n in ("script","style","svg","noscript","button","input","select","textarea","form","nav","iframe","img"):
            continue
        if n in ("h1","h2","h3","h4","h5"):
            t = clean(ch.get_text(" "))
            if t: out.append({"t": n, "v": t})
        elif n == "p":
            t = clean(ch.get_text(" "))
            if t and not EMOJI.match(t): out.append({"t": "p", "v": t})
        elif n in ("ul","ol"):
            items = [clean(li.get_text(" ")) for li in ch.find_all("li", recursive=False)]
            items = [i for i in items if i]
            if items: out.append({"t": "ul", "v": items})
        elif n == "table":
            rows = []
            for tr in ch.find_all("tr"):
                cells = [clean(c.get_text(" ")) for c in tr.find_all(["th","td"])]
                if any(cells): rows.append(cells)
            if rows: out.append({"t": "table", "v": rows})
        elif n == "details":
            s = ch.find("summary"); q = clean(s.get_text(" ")) if s else ""
            if s: s.extract()
            a = clean(ch.get_text(" "))
            if q: out.append({"t": "faq", "q": q, "a": a})
        elif n == "a":
            t = clean(ch.get_text(" "))
            if t and len(t) > 3: out.append({"t": "link", "v": t, "href": ch.get("href", "")})
        else:
            kids = [c for c in ch.children if isinstance(c, Tag) and c.name not in ("br",)]
            texts = [c for c in ch.children if isinstance(c, NavigableString) and clean(str(c))]
            # paire libellé / valeur
            if len(kids) == 2 and not texts and all(not k.find(BLOCKISH - {"div"}) and len(k.find_all("div")) == 0 for k in kids):
                a, b = clean(kids[0].get_text(" ")), clean(kids[1].get_text(" "))
                if a and b and len(a) < 45 and len(b) < 220 and not EMOJI.match(a):
                    out.append({"t": "kv", "k": a, "v": b}); continue
                if (not a or EMOJI.match(a)) and b: out.append({"t": "txt", "v": b}); continue
            walk(ch, out)

def blocks_from_html(html, selector=None):
    s = BeautifulSoup(html, "html.parser")
    roots = s.select(selector) if selector else [s.body or s]
    out = []
    for r in roots: walk(r, out)
    # dédoublonnage consécutif
    res = []
    for b in out:
        if res and b.get("v") == res[-1].get("v") and b.get("v") is not None: continue
        res.append(b)
    return res

def get(url):
    for _ in range(3):
        try:
            r = S.get(url, timeout=30)
            if r.ok: return r.text
        except Exception: pass
        time.sleep(1)
    return ""

def seo(html):
    s = BeautifulSoup(html, "html.parser")
    m = s.find("meta", attrs={"name": "description"})
    return (s.title.get_text(strip=True) if s.title else ""), (m["content"] if m else "")

pages = []
for line in open("/home/claude/extract/map.txt", encoding="utf-8"):
    path, ids = [x.strip() for x in line.split("|")]
    ids = [i for i in ids.split(",") if i and i != SHARED]
    slug = urllib.parse.unquote(path).strip("/")
    cache = RAW / ((slug.replace("/", "__") or "index") + ".html")
    if not cache.exists(): cache.write_text(get("https://www.od3d.be" + urllib.parse.quote(path)), encoding="utf-8")
    html = cache.read_text(encoding="utf-8")
    title, desc = seo(html)
    native = blocks_from_html(html, '#PAGES_CONTAINER [data-testid="richTextElement"]')
    emb = []
    for i in ids:
        emb += blocks_from_html((EMB / f"{i}.html").read_text(encoding="utf-8"))
    pages.append({"path": slug, "title": title, "desc": desc, "native": native, "embed": emb, "embeds": ids})

# Blog
sm = get("https://www.od3d.be/blog-posts-sitemap.xml")
for url in re.findall(r"<loc>([^<]+)</loc>", sm):
    slug = urllib.parse.unquote(url.split("/post/")[1])
    cache = RAW / f"post__{slug}.html"
    if not cache.exists(): cache.write_text(get(url), encoding="utf-8")
    html = cache.read_text(encoding="utf-8")
    title, desc = seo(html)
    s = BeautifulSoup(html, "html.parser")
    date = (s.find("meta", attrs={"property": "article:published_time"}) or {}).get("content", "") if s.find("meta", attrs={"property": "article:published_time"}) else ""
    img = (s.find("meta", attrs={"property": "og:image"}) or {}).get("content", "")
    body = blocks_from_html(html, '[data-hook="post-description"]') or blocks_from_html(html, "article")
    pages.append({"path": "post/" + slug, "title": title, "desc": desc, "native": body, "embed": [], "date": date, "image": img, "blog": True})

json.dump(pages, open(OUT / "pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(pages), "pages")
for p in pages[:3] + pages[-2:]:
    print(p["path"], len(p["native"]), len(p["embed"]))
