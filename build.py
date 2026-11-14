#!/usr/bin/env python3
"""Build the Cia. Victoria Sickness website into docs/ (served by GitHub Pages, branch main, folder /docs).

Texts:   content/i18n/<lang>.json   (one file per language; a language is live when its file exists
                                     AND it is listed in content/data.json → languages)
Facts:   content/data.json          (shows, credits, photos, downloads, redirects)
Layout:  src/page.html (+ social.html, a11y.html, cursor.html), src/style.css, src/site.js, src/smoke.js
Static:  static/ (favicon, preview image, video, PDFs) is copied as is.
Photos:  originals in source-images/ (never cropped). Web sizes are generated once into docs/img/sm|lg/<slug>.jpg.

Pages:        /<lang>/            (root / picks the visitor's language, default from data.json)
Short links:  /dossier/<short>/<lang>/  ·  /dossier/<short>/  (opens in the reader's language)
Run:  pip install jinja2 pillow && python3 build.py
"""
import datetime, json, pathlib, shutil
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).parent
SRC, OUT, CONTENT, STATIC, IMGSRC = ROOT/'src', ROOT/'docs', ROOT/'content', ROOT/'static', ROOT/'source-images'
data = json.loads((CONTENT/'data.json').read_text(encoding='utf-8'))
SITE_URL = 'https://' + data['site']['domain'] if data['site'].get('domain_live') else data['site']['preview_url']
langs = [l for l in data['languages'] if (CONTENT/'i18n'/f'{l}.json').exists()]
i18n = {l: json.loads((CONTENT/'i18n'/f'{l}.json').read_text(encoding='utf-8')) for l in langs}
DEFAULT = data['site']['default_lang']
today = datetime.date.today()
version = datetime.datetime.now().strftime('%Y%m%d%H%M')
SIZES = {'sm': 820, 'lg': 1800}

# ---------- static files and images
def build_static():
    if OUT.exists():
        for p in OUT.iterdir():
            if p.name != 'img': (shutil.rmtree if p.is_dir() else pathlib.Path.unlink)(p)
    shutil.copytree(STATIC, OUT, dirs_exist_ok=True)
    (OUT/'assets').mkdir(exist_ok=True)
    for f in ('style.css', 'site.js', 'smoke.js'): shutil.copy(SRC/f, OUT/'assets'/f)
    for slug, name in data['photos']['originals'].items():
        src = IMGSRC/name
        if not src.exists(): print(f'  ! missing original {name} for {slug}'); continue
        for d, size in SIZES.items():
            out = OUT/'img'/d/f'{slug}.jpg'
            if out.exists() and out.stat().st_mtime >= src.stat().st_mtime: continue
            out.parent.mkdir(parents=True, exist_ok=True)
            im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
            im.thumbnail((size, size), Image.LANCZOS)           # resize only, never crop
            im.save(out, 'JPEG', quality=82 if d == 'lg' else 78, optimize=True, progressive=True)

# ---------- downloads (PDFs live in static/pdf/)
def avail(key):
    return {l: u for l, u in data['downloads'][key]['files'].items() if (OUT/u).exists()}

def make_dlfile(lang):
    def dlfile(key):
        d = data['downloads'].get(key)
        if not d or d.get('draft'): return None
        fs = avail(key)
        if not fs: return None
        for l in (lang, DEFAULT, 'en', 'ca'):
            if l in fs: return {'url': fs[l], 'lang': l}
        l = next(iter(fs)); return {'url': fs[l], 'lang': l}
    return dlfile

def redirect_html(target):
    return (f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={target}"><a href="{target}">{target}</a>\n')

def build_links():
    lines = []
    for key, d in data['downloads'].items():
        fs = avail(key)
        if not fs: print(f'  ! no PDF yet for download "{key}"'); continue
        base = OUT/d['kind']/d['short']
        for l in langs:                                     # every site language gets a link (fallback: default language)
            u = fs.get(l) or fs.get(DEFAULT) or next(iter(fs.values()))
            (base/l).mkdir(parents=True, exist_ok=True)
            (base/l/'index.html').write_text(redirect_html('../../../' + u))
            lines.append(f'{SITE_URL}/{d["kind"]}/{d["short"]}/{l}/' + ('' if l in fs else f'   (→ {u.split("_")[1]})'))
        js = json.dumps(fs)
        (base/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<script>var f={js},n=(navigator.languages||[navigator.language||"{DEFAULT}"]).map(function(x){{return x.slice(0,2)}}),'
            f'k=n.find(function(x){{return f[x]}})||(f["{DEFAULT}"]?"{DEFAULT}":Object.keys(f)[0]);location.replace("../../"+f[k]);</script>\n')
        lines.append(f'{SITE_URL}/{d["kind"]}/{d["short"]}/   (opens in the reader\'s language)' + ('   DRAFT' if d.get('draft') else ''))
    (ROOT/'LINKS.txt').write_text('\n'.join(lines) + '\n')

# ---------- pages
def render():
    env = Environment(loader=FileSystemLoader(SRC), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    tpl = env.get_template('page.html')
    urls = []
    for lang in langs:
        ctx = dict(data, site_url=SITE_URL, t=i18n[lang], lang=lang, langs=langs, i18n=i18n, R='../',
                   version=version, year=today.year, dlfile=make_dlfile(lang))
        out = OUT/lang/'index.html'; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(tpl.render(**ctx), encoding='utf-8')
        urls.append(f'{SITE_URL}/{lang}/')
    # root: pick the visitor's language
    codes = json.dumps(langs)
    links = ' · '.join(f'<a href="{l}/">{i18n[l]["lang_name"]}</a>' for l in langs)
    (OUT/'index.html').write_text(f'''<!doctype html><html lang="{DEFAULT}"><meta charset="utf-8"><title>{data["site"]["name"]}</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{data["site"]["name"]}"><meta property="og:image" content="{SITE_URL}/og/victoria-sickness.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<script>var L={codes},n=(navigator.languages||[navigator.language||"{DEFAULT}"]).map(function(x){{return x.slice(0,2).toLowerCase()}}),k=n.find(function(x){{return L.indexOf(x)>=0}})||"{DEFAULT}";location.replace(k+"/"+location.hash);</script>
<p>{links}</p></html>
''')
    (OUT/'404.html').write_text(f'''<!doctype html><html><meta charset="utf-8"><title>404 · {data["site"]["name"]}</title><meta name="viewport" content="width=device-width, initial-scale=1">
<body style="background:#120d11;color:#f4eee6;font-family:system-ui;padding:3rem"><h1>404</h1><p>{links.replace('href="', 'href="' + SITE_URL + '/')}</p></body></html>
''')
    # old WordPress addresses
    for old, new in data.get('redirects', {}).items():
        p = OUT/old/'index.html'; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(redirect_html('../' * old.count('/') + new))
    if data['site'].get('domain_live'): (OUT/'CNAME').write_text(data['site']['domain'] + '\n')
    (OUT/'.nojekyll').write_text('')
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'<url><loc>{u}</loc><lastmod>{today.isoformat()}</lastmod></url>\n' for u in urls) + '</urlset>\n')

def check():
    def keys(d, p=''):
        return {p + k for k in d} | {x for k, v in d.items() if isinstance(v, dict) for x in keys(v, p + k + '.')}
    ref = keys(i18n[DEFAULT])
    for l in langs:
        miss = ref - keys(i18n[l])
        if miss: print(f'  ! {l}: missing {sorted(miss)[:8]}')

if __name__ == '__main__':
    build_static(); build_links(); render(); check()
    print(f'built {len(langs)} languages → docs/  ({SITE_URL})')
