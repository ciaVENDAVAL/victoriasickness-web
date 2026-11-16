# victoriasickness-web (PUBLIC)

Website victoriasickness.com and all promoter material of Cia. Victoria Sickness (show dossiers, riders, photos).
**This repo is public:** never add fees, budgets, tax IDs (NIF), personal data (team phones, IDs, addresses) or application answers — not in text, PDFs or commit messages. Those go in the private repo `ciaVENDAVAL/victoriasickness-docs` (its `INDEX.md` lists where every document lives).

- **Facts:** Project doc `master/VICTORIA SICKNESS master fact sheet.md` (claude.ai Project "Cia. Victoria Sickness"). Newest info wins; update it and every language when a fact changes. Read it right before writing it (parallel sessions overwrite each other).
- **How to update:** `UPDATING.md`. Check before pushing: `python3 tools/check.py` (writes CHECK-REPORT.md).
- **Editing without code (La Senyal model):** admin `https://ciavendaval.github.io/victoriasickness-admin/` (Sveltia forms, repo victoriasickness-admin) and `…/victoriasickness-web/es/#edit` (on-page editor, `src/edit.js`). Both commit straight to `main`. The workflow `.github/workflows/site.yml` then translates texts changed in one language (`tools/translate.py`, Softcatalà, via CA) and rebuilds `docs/`. **Always pull before working** (the editors and the bot commit too). After changing a content file's shape or adding text keys, regenerate the admin forms: `python3 scripts/make_config.py ../victoriasickness-web web/config.yml` in victoriasickness-admin.
- **No Google, no Amazon:** fonts are served from `static/fonts/` (OFL); no Google Fonts, no YouTube thumbnails; videos preferably on PeerTube (a show's `video` accepts a PeerTube or YouTube link). No DeepL / Google Translate.
- **Build:** `python3 build.py` (site → `docs/`, never edit `docs/` by hand) · `python3 dossiers/invocaciones-compacto/build.py [langs]` · `python3 dossiers/invocaciones-largo/build.py` (ES only, first version) · `python3 tools/og.py` (link-preview image).
- **Push:** build, check, commit (author `Cia. Victoria Sickness <victoriasickness@gmail.com>`), `git fetch origin main && git rebase origin/main && git push origin HEAD:main`. If a rebase conflicts only in `docs/`, take ours, rebuild, `git add -A`, continue. GitHub Pages serves `docs/` (branch main, folder /docs).
- **Languages:** ES (default) CA EU EN FR IT PT DE — kept consistent. A language is live when `content/i18n/<lang>.json` exists and it is in `content/site.json → languages`. No Esperanto, no Japanese. EU FR IT PT DE need a native check (fact sheet ⚠13).
- **Domain:** while `site.domain_live` is false, links and previews use the GitHub address. To move victoriasickness.com: at the DNS provider set A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` and `www` CNAME → `ciavendaval.github.io`; then set `domain_live` true, rebuild, push (adds docs/CNAME), and in Settings → Pages enter the domain and tick Enforce HTTPS.

## House style
- Name: **Cia. Victoria Sickness** (capital C, confirmed by tyle 14 Nov 2026) · Vic Heredero · tyle fernández lowercase. Spellings in `content/facts.json → names`.
- **Pronouns for Vic / Victoria: neutral** — EN they/them/their · ES elle (le, -e endings) · CA elli (le, -e endings, no personal article before the name) · EU no gender · FR IT PT DE: rephrase around the name. Never she/her, ella, la Victoria. Rules in `content/facts.json → pronouns`; the checker flags old forms.
- Never crop photos (resize only; the Cyr wheel must be visible). Credit every photographer (`content/photos.json → credits`).
- Prices never public.
- In print: web link always **victoriasickness.com**; socials as logos only; links, not QR codes; contact on the last content page.
- Dossiers: A4 landscape, website style (pages 1–3 black, last page white with a bold red contact band), ≤ 3 MB. ES design first, other languages after approval. Must have team + credits, technical contact, recommended age, duration.
- Website: no "Hablemos", no "Hecho con purpurina y rueda Cyr" (banned in facts.json). Footer right (accessibility button is bottom-left).
