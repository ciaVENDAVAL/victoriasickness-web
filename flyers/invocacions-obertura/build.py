#!/usr/bin/env python3
"""Build the flyer «obertura de procés» of Invocacions.

Texts:   flyers/invocacions-obertura/<lang>.json   ·   artwork: img/collage.jpg (the poster collage, never cropped)
Output:  static/pdf/VictoriaSickness-Invocaciones_<LANG>_flyer-obertura_<yyyy-mm>.pdf   (A5, print)
         static/img/VictoriaSickness-Invocaciones_<LANG>_flyer-obertura_<yyyy-mm>.jpg   (1080×1350, Instagram)
Run:     python3 flyers/invocacions-obertura/build.py [langs]   (CHROME=/path/to/chrome · DOSSIER_DATE=2026-12)
Print larger than A5 (A3 poster) only with the full-resolution collage: the current one is 1122 px wide.
"""
import asyncio, datetime, json, os, pathlib, sys
from jinja2 import Environment, FileSystemLoader

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STAMP = os.environ.get('DOSSIER_DATE', datetime.date.today().strftime('%Y-%m'))

async def render(html_a5, html_ig, pdf_out, jpg_out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
        b = await p.chromium.launch(args=['--no-sandbox'], **kw)
        pg = await b.new_page()
        await pg.goto(html_a5.as_uri(), wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        await pg.pdf(path=str(pdf_out), prefer_css_page_size=True, print_background=True)
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        await pg.goto(html_ig.as_uri(), wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(jpg_out), type='jpeg', quality=90)
        await b.close()

def build(lang):
    t = json.loads((HERE/f'{lang}.json').read_text(encoding='utf-8'))
    tpl = Environment(loader=FileSystemLoader(HERE), autoescape=False).get_template('template.html')
    paths = {}
    for fmt in ('a5', 'ig'):
        paths[fmt] = HERE/f'.{lang}-{fmt}.html'; paths[fmt].write_text(tpl.render(t=t, lang=lang, fmt=fmt), encoding='utf-8')
    name = f'VictoriaSickness-Invocaciones_{lang.upper()}_flyer-obertura_{STAMP}'
    pdf_out, jpg_out = ROOT/'static/pdf'/f'{name}.pdf', ROOT/'static/img'/f'{name}.jpg'
    jpg_out.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(render(paths['a5'], paths['ig'], pdf_out, jpg_out))
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(pdf_out); w = PdfWriter()
    for page in r.pages: w.add_page(page)
    w.add_metadata({'/Title': f'{t["title"]} — {t["kicker"]}', '/Author': 'Cia. Victoria Sickness'})
    w.write(pdf_out)
    for f in (pdf_out, jpg_out): print(f'  ✓ {f.relative_to(ROOT)}  ({f.stat().st_size / 1e6:.2f} MB)')

if __name__ == '__main__':
    for l in sys.argv[1:] or sorted(p.stem for p in HERE.glob('*.json')): build(l)
