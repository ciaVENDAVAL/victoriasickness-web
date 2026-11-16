# Cia. Victoria Sickness — how to change a fact everywhere

Goal: one change → every language, every PDF and the website say the same thing.

## 1. Record the fact once
1. In the Project doc `master/VICTORIA SICKNESS master fact sheet.md` (read → merge → write).
2. Spelling, contact detail or style rule → also `content/facts.json` (used by the checker).

## 2. Find every place that uses it
`python3 tools/check.py --find "old text"` → every source, web page and PDF that contains it.

## 3. Change the sources, all languages at once
| What | Where |
|---|---|
| Website texts | `content/i18n/<lang>.json` (es ca eu en fr it pt de) |
| Shows: title, video, credits, supporters, gallery | `content/shows.json` (admin: Espectáculos) |
| Photos of "about" · photographer credits | `content/about.json` · `content/photos.json` |
| Which PDF each language gets | `content/downloads.json` (admin: PDFs) |
| Colours, text font | `content/theme.json` (admin: Aspecto) |
| Domain, languages, contact, PDF kinds, old-URL redirects | `content/site.json` (technical, not in the admin) |
| Compact dossier texts | `dossiers/invocaciones-compacto/<lang>.json` (credits and supporters come from content/shows.json) |
| Long dossier (ES only) | `dossiers/invocaciones-largo/es.html` |
| Layout | `src/page.html`, `src/style.css`, `src/site.js`, `src/smoke.js` |
| Private documents | victoriasickness-docs (`INDEX.md`) |

Never update one language only. Unsure translation → write it anyway and add it to the native-check list (fact sheet ⚠13).

## 4. Rebuild and check
```
python3 dossiers/invocaciones-compacto/build.py [langs]   # only if its texts or data changed
python3 build.py
python3 tools/check.py                                     # → CHECK-REPORT.md
```
Don't rebuild a PDF whose text hasn't changed.

## 5. New photo
Put the original in `source-images/<name>.jpg` (never cropped; simple name, no spaces or accents) — or upload it in the admin / replace it on the page. Add the photographer to `content/photos.json → credits`, then use `/source-images/<name>.jpg` in a show's `images`. `build.py` makes `img/sm` (820 px) and `img/lg` (1800 px), and redoes them when the original's content changes.

## 6. New PDF
Name: `static/pdf/VictoriaSickness-<Show>_<LANG>_<kind>_<yyyy-mm>.pdf`. Choose it in `content/downloads.json` (admin: PDFs); a new kind also needs an entry in `content/site.json → downloads` (`"draft": true` keeps it off the website buttons but still gives it a short link). Short links in `LINKS.txt`; emails use those, never attachments.

## 7. Editors and robots
tyle edits in the admin or on the page; every Save/Publish is a commit. The workflow translates (unless `[no-translate]`) and rebuilds `docs/` in 3–5 minutes. Before working from a computer: `git pull`. Translations by Softcatalà's models must be read by a human (pronouns: fact sheet section 1).

## 8. Publish
Look at the pages (phone + computer) → commit → push (see CLAUDE.md) → one line in the fact sheet's session log → update `master/VICTORIA SICKNESS email templates.md` if links changed.
