# O&D Impression 3D — maquette du nouveau site (design futuriste)

Maquette **non officielle**, non indexée par Google (`noindex` + `robots.txt` bloquant). Le site officiel reste od3d.be sur Wix.

## Mettre en ligne sur GitHub Pages
1. Crée un dépôt **public** nommé `od3d-maquette` sur github.com (sans README).
2. Envoie le contenu : le site compte plus de 100 fichiers, au-delà de la limite d'envoi du navigateur GitHub. Deux options :
   - **le plus simple** : dis à Claude que le dépôt existe, il pousse tout lui-même ;
   - ou avec **GitHub Desktop** (gratuit) : *Clone* le dépôt, copie tout ce dossier dedans, *Commit* puis *Push*.
3. *Settings → Pages* → Source : **Deploy from a branch** → branche `main`, dossier `/ (root)` → *Save*.
4. Après 1 à 2 minutes : `https://max-moor.github.io/od3d-maquette/`

## Ce qu'il y a dedans
- **Même structure d'URL que od3d.be** : 82 pages + 29 articles de blog (`services/…`, `machines-materiaux/…`, `comparateur-materiaux/…`, `a-propos/…`, `réalisations/…`, `post/…`). Aucune page regroupée : tout le capital SEO/GEO est conservé.
- Contenu repris du site actuel (textes, FAQ complète, fiches techniques), photos des machines et matériaux, ruche des logos clients.
- Nouvelles pages : `devis-instantane/` (calculateur corrigé) et le quiz intégré.
- `static/` : styles (`css/od3d.css`), scripts (`js/od3d.js`), polices hébergées localement, images optimisées (WebP + PNG).

## Modifier
- **Couleurs / polices** : variables en haut de `static/css/od3d.css` (`--c` = cyan O&D).
- **Une page** : chaque page est un fichier `index.html` dans son dossier. Les textes se modifient directement.
- **Tout régénérer** (avancé) : `python3 _source/build.py` reconstruit toutes les pages à partir de `_source/content/` (nécessite Python 3). Ajoute `--prod` pour la version indexable du lancement.

## À vérifier avant le lancement
- Les affirmations du site actuel reprises telles quelles (±0,1 mm, 1000×1000×1000 mm, Ultem « certifié FAA », délais…) : voir `4-affirmations-a-verifier.md` de l'archive précédente.
- Calculateur : préciser si le prix affiché est HTVA ou TVAC (mention orange).
- La photo « Carvera » n'est utilisée nulle part (aucune page Makera Carvera sur le site actuel).
- La FAQ citait « Baelen (4837) » : remplacé par « Welkenraedt (4840) ».
- Pages Wix `donate` et `donation-thank-you-page` non reprises (pages modèles inutilisées).
