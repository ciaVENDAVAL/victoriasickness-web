#!/usr/bin/env python3
"""Long Invocaciones dossier (A4 landscape, 7 pages, ES only) → static/pdf/.

Source: es.html in this folder (texts written in the HTML; photos in img/).
This is the first version; new languages are made from the compact dossier (../invocaciones-compacto).
Run:  pip install playwright pypdf && playwright install chromium
      python3 dossiers/invocaciones-largo/build.py        (CHROME=/path/to/chrome to use an installed Chrome)
"""
import asyncio, datetime, os, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STAMP = os.environ.get('DOSSIER_DATE', datetime.date.today().strftime('%Y-%m'))
OUT = ROOT/'static/pdf'/f'VictoriaSickness-Invocaciones_ES_dossier_{STAMP}.pdf'

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
        b = await p.chromium.launch(args=['--no-sandbox'], **kw)
        pg = await b.new_page()
        await pg.goto((HERE/'es.html').as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(800)
        await pg.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True)
        await b.close()
    print('  ✓', OUT.relative_to(ROOT))

asyncio.run(main())
