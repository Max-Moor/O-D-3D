# O&D Impression 3D — maquette du nouveau site

Maquette non officielle, non indexée. En ligne : https://max-moor.github.io/O-D-3D/

Mise à jour : remplacer tout le contenu du dépôt par le contenu de ce dossier, puis Commit + Push.

- Mêmes URL que od3d.be + écosystèmes SLS / FDM / Résine / CNC, matières CNC, Makera Carvera, devis instantané, FAQ complète.
- Design : `static/css/od3d.css` · Animations : `static/js/od3d.js` · Photos : `static/img/`
- Régénérer (avancé) : `python3 _source/build.py` (`--prod` = version indexable pour le lancement).

## Langues (FR · EN · DE · NL)
- Le français reste à la racine ; les traductions sont générées dans `/en/`, `/de/`, `/nl/` par `_source/i18n.py` (lancé automatiquement à la fin de `build.py`).
- Les traductions vivent dans `_source/i18n/en.json`, `de.json`, `nl.json` : `"texte français": "traduction"`. Corriger une traduction = modifier la valeur, puis relancer `python3 build.py`.
- Une page n'est publiée dans une langue que si 97 % de son texte est traduit ; sinon le bouton de langue renvoie vers l'accueil de cette langue.
- Liste des textes manquants d'une page : `python3 i18n.py --missing en contact`.
- Balises `hreflang` + sitemap multilingue ajoutés automatiquement.
