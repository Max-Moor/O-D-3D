# Mise en ligne : check-list SEO / GEO

1. Construire en production : `python3 build.py --prod` (retire le noindex, ouvre robots.txt aux robots IA).
2. Recréer les redirections 301 listées dans `redirects_301.csv` (anciennes URL Wix -> nouvelles).
   Les URL anglaises actuelles du site Wix (/en/machines-materials/…, /en/services/…) sont conservées
   via `i18n/slugs_en.json` ; tant qu'une page n'est pas traduite, son URL anglaise redirige vers la page FR.
3. Envoyer `sitemap.xml` dans Google Search Console.
4. Vérifier `llms.txt` et `llms-full.txt` à la racine.
5. Comparer clics / positions à J+14 et J+42 (Search Console > Performances).

Fichiers clés : `geo.py` (données structurées, llms.txt, sitemap, redirections), `content/seo.json`
(titres et descriptions), `i18n/slugs_*.json` (URL par langue), `content/redirects.json` (anciennes URL).
