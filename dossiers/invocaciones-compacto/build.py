#!/usr/bin/env python3
"""Build the compact Invocaciones dossier (A4 landscape, 4 pages) → static/pdf/.

Texts:   dossiers/invocaciones-compacto/<lang>.json   (one per language; copy es.json to start a new one)
Facts:   content/shows.json  (credits, supporters of the show "invocaciones")
Photos:  source-images/ (resized copies in .img/, never cropped)
Output:  static/pdf/VictoriaSickness-Invocaciones_<LANG>_dossier-compacto_<yyyy-mm>.pdf

Run:  pip install jinja2 pillow pypdf playwright && playwright install chromium
      python3 dossiers/invocaciones-compacto/build.py          # all languages with a .json
      python3 dossiers/invocaciones-compacto/build.py es ca    # only these
Set CHROME=/path/to/chrome to use an installed Chrome instead of Playwright's Chromium.
"""
import asyncio, datetime, json, os, pathlib, sys
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
data = json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
show = next(s for s in json.loads((ROOT/'content/shows.json').read_text(encoding='utf-8'))['shows'] if s['id'] == 'invocaciones')
STAMP = os.environ.get('DOSSIER_DATE', datetime.date.today().strftime('%Y-%m'))
IMAGES = ['invocaciones-cartel', 'invocaciones-1', 'invocaciones-2', 'victoria-retrato', 'circografia-4']

def images():
    d = HERE/'.img'; d.mkdir(exist_ok=True)
    for slug in IMAGES:
        out = d/f'{slug}.jpg'
        if out.exists(): continue
        im = ImageOps.exif_transpose(Image.open(ROOT/'source-images'/f'{slug}.jpg')).convert('RGB')
        im.thumbnail((1500, 1500)); im.save(out, 'JPEG', quality=78, optimize=True, progressive=True)

def cover_fade():
    """Cover image with the fade to black baked in (PDF viewers on phones draw CSS alpha gradients over images wrongly, pink).
    Same framing as CSS object-fit: cover in the 46% × 210 mm box on page 1."""
    out = HERE/'.img'/'invocaciones-cartel-fade.jpg'
    im = Image.open(HERE/'.img'/'invocaciones-cartel.jpg').convert('RGB')
    box = (297 * .46) / 210
    w, h = im.size
    if w / h > box:
        nw = round(h * box); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    w, h = im.size
    stops = [(0, 1), (.06, 1), (.16, .92), (.27, .7), (.40, .38), (.52, .12), (.62, 0), (1, 0)]
    def alpha(x):
        for (x0, a0), (x1, a1) in zip(stops, stops[1:]):
            if x <= x1: return a0 + (a1 - a0) * (x - x0) / (x1 - x0)
        return 0
    mask = Image.new('L', (w, 1)); mask.putdata([round(255 * alpha(i / (w - 1))) for i in range(w)])
    ink = Image.new('RGB', (w, h), (18, 13, 17))
    Image.composite(ink, im, mask.resize((w, h))).save(out, 'JPEG', quality=80, optimize=True, progressive=True)

async def pdf(html_path, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
        b = await p.chromium.launch(args=['--no-sandbox'], **kw)
        pg = await b.new_page()
        await pg.goto(html_path.as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(600)
        await pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
        await b.close()

def build(lang):
    t = json.loads((HERE/f'{lang}.json').read_text(encoding='utf-8'))
    env = Environment(loader=FileSystemLoader(HERE), autoescape=False)
    html = env.get_template('template.html').render(t=t, lang=lang, show=show, img='.img/')
    tmp = HERE/f'.{lang}.html'; tmp.write_text(html, encoding='utf-8')
    out = ROOT/'static/pdf'/f'VictoriaSickness-Invocaciones_{lang.upper()}_dossier-compacto_{STAMP}.pdf'
    out.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(pdf(tmp, out))
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(out); w = PdfWriter()
    for page in r.pages: w.add_page(page)
    w.add_metadata({'/Title': f'{t.get("title", "Invocaciones")} — {t["doc_title"]}', '/Author': data['site']['name'], '/Subject': t['status']})
    w.write(out)
    print(f'  ✓ {out.relative_to(ROOT)}  ({out.stat().st_size / 1e6:.1f} MB, {len(r.pages)} p)')

if __name__ == '__main__':
    images(); cover_fade()
    langs = sys.argv[1:] or sorted(p.stem for p in HERE.glob('*.json'))
    for l in langs: build(l)
