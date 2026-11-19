#!/usr/bin/env python3
"""Build the Invocaciones technical rider (A4 portrait, 1 page) → static/pdf/.

Texts:   riders/invocaciones/<lang>.json   (copy ca.json to start a new language)
Output:  static/pdf/VictoriaSickness-Invocaciones_<LANG>_rider_<yyyy-mm>.pdf
Run:     python3 riders/invocaciones/build.py [langs]      (no args = every <lang>.json)
         CHROME=/path/to/chrome to use an installed Chrome · DOSSIER_DATE=2026-11 fixes the month in the file name
Public repo: no phone numbers here (technical contact = name + company email).
"""
import asyncio, datetime, json, os, pathlib, sys
from jinja2 import Environment, FileSystemLoader

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STAMP = os.environ.get('DOSSIER_DATE', datetime.date.today().strftime('%Y-%m'))

async def pdf(html_path, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
        b = await p.chromium.launch(args=['--no-sandbox'], **kw)
        pg = await b.new_page()
        await pg.goto(html_path.as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        await pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
        await b.close()

def build(lang):
    t = json.loads((HERE/f'{lang}.json').read_text(encoding='utf-8'))
    html = Environment(loader=FileSystemLoader(HERE), autoescape=False).get_template('template.html').render(t=t, lang=lang)
    tmp = HERE/f'.{lang}.html'; tmp.write_text(html, encoding='utf-8')
    out = ROOT/'static/pdf'/f'VictoriaSickness-Invocaciones_{lang.upper()}_rider_{STAMP}.pdf'
    asyncio.run(pdf(tmp, out))
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(out); w = PdfWriter()
    for page in r.pages: w.add_page(page)
    w.add_metadata({'/Title': f'{t["title"]} — {t["doc"]}', '/Author': 'Cia. Victoria Sickness'})
    w.write(out)
    print(f'  ✓ {out.relative_to(ROOT)}  ({out.stat().st_size / 1e6:.2f} MB, {len(r.pages)} p)')

if __name__ == '__main__':
    for l in sys.argv[1:] or sorted(p.stem for p in HERE.glob('*.json')): build(l)
