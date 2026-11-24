# fusionne un lot : python3 i18n/merge.py <lot_fr.json> <lang> <fichier idx|trad>
# les index absents du fichier = texte identique (noms propres, codes)
import json, sys, pathlib
src = json.load(open(sys.argv[1], encoding="utf-8")); lang = sys.argv[2]
tr = {}
for line in open(sys.argv[3], encoding="utf-8"):
    line = line.rstrip("\n")
    if "|" not in line: continue
    i, t = line.split("|", 1); tr[int(i)] = t
out = pathlib.Path(__file__).parent / f"{lang}.json"
d = json.load(open(out, encoding="utf-8")) if out.exists() else {}
same = []
for i, s in enumerate(src):
    if i in tr: d[s] = tr[i]
    else: d[s] = s; same.append(s)
json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(lang, len(d), "entrées ; identiques :", same)
