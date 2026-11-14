# victoriasickness-web (PUBLIC)

Website victoriasickness.com and all promoter material of cia. Victoria Sickness (show dossiers, riders, photos).
**This repo is public:** never add fees, budgets, tax IDs (NIF), personal data (team phones, IDs, addresses) or application answers — not in text, PDFs or commit messages. Those go in the private repo `ciaVENDAVAL/victoriasickness-docs` (its `INDEX.md` lists where every document lives).

- **Facts:** Project doc `master/VICTORIA SICKNESS master fact sheet.md` (claude.ai Project "Cia. Victoria Sickness"). Newest info wins; update it and every language when a fact changes. Read it right before writing it (parallel sessions overwrite each other).
- **How to update:** `UPDATING.md`. Check before pushing: `python3 tools/check.py` (writes CHECK-REPORT.md).
- **Build:** `python3 build.py` (site → `docs/`, never edit `docs/` by hand) · `python3 dossiers/invocaciones-compacto/build.py [langs]` · `python3 dossiers/invocaciones-largo/build.py` (ES only, first version).
- **Push:** build, check, commit (author `cia. Victoria Sickness <victoriasickness@gmail.com>`), `git fetch origin main && git rebase origin/main && git push origin HEAD:main`. If a rebase conflicts only in `docs/`, take ours, rebuild, `git add -A`, continue. GitHub Pages serves `docs/` (branch main, folder /docs).
- **Languages:** ES (default) CA EU EN FR IT PT DE — kept consistent. A language is live when `content/i18n/<lang>.json` exists and it is in `content/data.json → languages`. No Esperanto, no Japanese. EU FR IT PT DE need a native check (fact sheet ⚠13).
- **Domain:** while `site.domain_live` is false, links and previews use the GitHub address. To move victoriasickness.com: at the DNS provider set A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` and `www` CNAME → `ciavendaval.github.io`; then set `domain_live` true, rebuild, push (adds docs/CNAME), and in Settings → Pages enter the domain and tick Enforce HTTPS.
- **Transition:** the root `index.html` forwards to `docs/` only while Pages still serves the repo root. Once Pages serves `/docs`, delete the root `index.html` and `.nojekyll`.

## House style
- Name: cia. Victoria Sickness (⚠ spelling cia./Cia. to confirm) · Vic Heredero · tyle fernández lowercase. Spellings in `content/facts.json → names`.
- Never crop photos (resize only; the Cyr wheel must be visible). Credit every photographer (`data.json → photos.credits`).
- Prices never public.
- In print: web link always **victoriasickness.com**; socials as logos only; links, not QR codes; contact on the last content page.
- Dossiers: A4 landscape, website style (pages 1–3 black, last page white with a bold red contact band), ≤ 3 MB. ES design first, other languages after approval. Must have team + credits, technical contact, recommended age, duration.
- Website: no "Hablemos", no "Hecho con purpurina y rueda Cyr" (banned in facts.json). Footer right (accessibility button is bottom-left).
