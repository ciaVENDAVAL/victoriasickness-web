# victoriasickness-web

Website and promoter material of **cia. Victoria Sickness** — contemporary circus, travesti body, queer memory.

- Live (staging): https://ciavendaval.github.io/victoriasickness-web/ → victoriasickness.com once the domain moves
- 8 languages: ES CA EU EN FR IT PT DE
- Rules for editing: `CLAUDE.md` · step by step: `UPDATING.md` · short links for emails: `LINKS.txt`

```
victoriasickness-web/
├── build.py           builds the site into docs/
├── content/
│   ├── i18n/<lang>.json   all website texts, one file per language
│   ├── data.json          shows, credits, photos, downloads, redirects
│   └── facts.json         spellings, contact data, banned words (for the checker)
├── src/               page.html (Jinja2) + social/a11y/cursor partials, style.css, site.js, smoke.js
├── dossiers/
│   ├── invocaciones-compacto/   template.html + <lang>.json + build.py  (4 p)
│   └── invocaciones-largo/      es.html + img/ + build.py              (7 p, ES only)
├── static/            favicon, og/ preview image, video/, pdf/ (built PDFs)
├── source-images/     original public photos (never cropped)
├── tools/check.py     cross-check → CHECK-REPORT.md
└── docs/              GENERATED — served by GitHub Pages (main, /docs)
```

Setup: `pip install jinja2 pillow pypdf playwright && playwright install chromium`
