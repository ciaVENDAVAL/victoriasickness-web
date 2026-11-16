# victoriasickness-web

Website and promoter material of **Cia. Victoria Sickness** — contemporary circus, travesti body, queer memory.

- Live (staging): https://ciavendaval.github.io/victoriasickness-web/ → victoriasickness.com once the domain moves
- 8 languages: ES CA EU EN FR IT PT DE
- Edit without code: admin https://ciavendaval.github.io/victoriasickness-admin/ · on the page: add `#edit` to any page
- Rules for editing: `CLAUDE.md` · step by step: `UPDATING.md` · short links for emails: `LINKS.txt`

```
victoriasickness-web/
├── build.py           builds the site into docs/
├── content/
│   ├── i18n/<lang>.json   all website texts, one file per language
│   ├── shows.json · about.json · photos.json · downloads.json · theme.json   (edited in the admin)
│   ├── site.json          domain, languages, contact, PDF kinds, redirects (technical)
│   └── facts.json         spellings, pronouns, banned words, private-data patterns, names not to translate
├── src/               page.html (Jinja2) + partials, style.css, site.js, smoke.js, edit.js (edit on the page)
├── dossiers/
│   ├── invocaciones-compacto/   template.html + <lang>.json + build.py  (4 p)
│   └── invocaciones-largo/      es.html + img/ + build.py              (7 p, ES only)
├── static/            favicon, og/ preview image, video/, pdf/ (built PDFs)
├── source-images/     original public photos (never cropped)
├── tools/             check.py (→ CHECK-REPORT.md), translate.py (Softcatalà), og.py (link preview)
├── .github/workflows/site.yml   translate → build → publish after every change
└── docs/              GENERATED — served by GitHub Pages (main, /docs)
```

Setup: `pip install jinja2 pillow pypdf playwright && playwright install chromium`
