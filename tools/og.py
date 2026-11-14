#!/usr/bin/env python3
"""Link-preview image (WhatsApp, Telegram, social): tools/og.html → static/og/victoria-sickness.jpg (1200×630).
Vic's face stays inside the centre square (WhatsApp crops small previews to it).
Run: python3 tools/og.py   (CHROME=/path/to/chrome to use an installed Chrome)"""
import asyncio, os, pathlib, io
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent/'static/og/victoria-sickness.jpg'

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
        b = await p.chromium.launch(args=['--no-sandbox'], **kw)
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        await pg.goto((HERE/'og.html').as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        png = await pg.screenshot(); await b.close()
    Image.open(io.BytesIO(png)).convert('RGB').save(OUT, 'JPEG', quality=84, optimize=True, progressive=True)
    print('  ✓', OUT.relative_to(HERE.parent), f'{OUT.stat().st_size // 1024} KB')

asyncio.run(main())
