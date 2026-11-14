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
| Shows, credits, supporters, videos, photos, downloads, old-URL redirects | `content/data.json` |
| Compact dossier texts | `dossiers/invocaciones-compacto/<lang>.json` (credits and supporters come from data.json) |
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
Put the original in `source-images/` (never cropped), add `"<slug>": "<file name>"` to `data.json → photos.originals`, add the photographer to `photos.credits`, then use the slug in a show's `images`. `build.py` makes `img/sm` (820 px) and `img/lg` (1800 px).

## 6. New PDF
Name: `static/pdf/VictoriaSickness-<Show>_<LANG>_<kind>_<yyyy-mm>.pdf`. Register it in `data.json → downloads` (`"draft": true` keeps it off the website buttons but still gives it a short link). Short links in `LINKS.txt`; emails use those, never attachments.

## 7. Publish
Look at the pages (phone + computer) → commit → push (see CLAUDE.md) → one line in the fact sheet's session log → update `master/VICTORIA SICKNESS email templates.md` if links changed.
