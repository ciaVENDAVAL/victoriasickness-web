# victoriasickness-web

Website for **cia. Victoria Sickness**, built for **GitHub Pages** (plain Jekyll, no plugins, nothing to install).

**Staging address:** https://ciavendaval.github.io/victoriasickness-web/
PDFs (dossiers, riders) go in the sister repo **victoriasickness-docs**.

## What's in it

- **8 languages:** ES at `/`, then `/ca/ /eu/ /en/ /fr/ /it/ /pt/ /de/`, with `hreflang` tags and a ✦ language menu.
- **Photos and the hero video are local** (`assets/img/sm` = thumbnails, `assets/img/lg` = full size, `assets/video/hero.mp4`).
- **Galleries:** a mosaic per show plus a photo strip in "about". Click a photo to open it full size; use the arrows, keyboard ← → or swipe, and Esc to close.
- **Old WordPress URLs** (`/en/home/`, `/ca/inici/`, `/sobre-mi/`, `/contacto/`) redirect to the new pages.
- **Menu:** the round button at the top right opens a full-screen menu with the sections, both shows, the email and social icons.
- **Accessibility:** the Cyr-wheel button at the bottom left has options to stop animations, switch dark/light, raise contrast, underline links, add line spacing, use the normal cursor, and change the text size (80–160%). The choices are remembered in that browser.
- **Sage smoke:** every tap or click lets a thin curl of sage smoke with a tiny ember rise from that spot (`assets/js/smoke.js`). It's off with reduced motion or the "stop animations" option.
- **Cursor:** a lacquer dot. **Press and hold** (mouse or finger, about 0.45 s) and the back of a hand appears and gets its nails painted, a different colour each time. A long press never triggers the link underneath, and starting to scroll cancels it on phones.

## Edit content

| What | Where |
|---|---|
| All texts, per language | `_data/i18n/<lang>.yml` (same keys in every file) |
| Shows: credits, links, supporters, photos, YouTube, dossier PDF | `_data/shows.yml` |
| Photos in "about" | `_data/about.yml` |
| Email, socials, languages, URLs | `_config.yml` |
| Look & feel | `assets/css/main.css` (colours and fonts at the top) |
| Cursor / manicure | `_includes/cursor.html` (SVG), `assets/js/main.js` |
| Accessibility panel, social icons | `_includes/a11y.html`, `_includes/social.html` |

**Add photos:** save a thumbnail (about 820 px on the long side) in `assets/img/sm/` and a large version (about 1800 px) with the **same name** in `assets/img/lg/`. Then list it in `_data/shows.yml` with `o: p` (portrait) or `o: l` (landscape). The order sets the mosaic.

**Add a show:** add an entry to `_data/shows.yml` with a new `id`, then add `shows.<id>` to every language file.

**Add a language:** copy `_data/i18n/en.yml` to `<code>.yml` and translate it, add it under `languages:` in `_config.yml`, and create `<code>/index.html` with `layout: home`, `lang: <code>`, `permalink: /<code>/`.

**Link a dossier:** upload the PDF to `victoriasickness-docs/pdf/`, then set `dossier: <file>.pdf` on the show.

## Switch the domain to victoriasickness.com (when ready to leave WordPress)

1. In `_config.yml`: `url: https://victoriasickness.com` and `baseurl: ""`.
2. Add a file named `CNAME` containing `victoriasickness.com`.
3. At your DNS provider, point the apex to GitHub with A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and set `www` as a CNAME to `ciavendaval.github.io`.
4. In the repo, open **Settings → Pages**, enter the custom domain, and tick **Enforce HTTPS**.

## Local preview

- With Ruby: `bundle install && bundle exec jekyll serve`
- Without Ruby: `pip install python-liquid pyyaml && python scripts/preview.py && python -m http.server -d preview`, then open http://localhost:8000/victoriasickness-web/
