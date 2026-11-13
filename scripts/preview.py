"""Minimal local preview without Ruby: renders the Jekyll layouts with python-liquid into ./preview.
   pip install python-liquid pyyaml   ·   python scripts/preview.py   ·   python -m http.server -d preview
   (GitHub Pages builds the real site with Jekyll; this is only for quick checks.)"""
import datetime, pathlib, re, shutil, yaml
from liquid import Environment, FileSystemLoader

root = pathlib.Path(__file__).resolve().parent.parent
out = root / "preview"
cfg = yaml.safe_load((root / "_config.yml").read_text())
data = {"shows": yaml.safe_load((root / "_data/shows.yml").read_text()), "about": yaml.safe_load((root / "_data/about.yml").read_text()),
        "i18n": {p.stem: yaml.safe_load(p.read_text()) for p in (root / "_data/i18n").glob("*.yml")}}
site = {**cfg, "data": data, "time": datetime.datetime.now()}

env = Environment(loader=FileSystemLoader(root / "_includes"))
env.filters["relative_url"] = lambda _ctx, s: s if re.match(r"https?://", str(s)) else cfg.get("baseurl", "") + str(s)
layout = re.sub(r"{% include ([\w.-]+) %}", r"{% include '\1' %}", (root / "_layouts/home.html").read_text())

shutil.rmtree(out, ignore_errors=True)
out = out / cfg.get("baseurl", "").strip("/")  # mirror the GitHub Pages sub-path
shutil.copytree(root / "assets", out / "assets")
for lang in cfg["languages"]:
    html = env.parse(layout).render({"site": site, "page": {"lang": lang["code"], "url": lang["path"]}})
    dest = out / lang["path"].strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print("✓", dest.relative_to(root))
print("serve: python -m http.server -d preview  →  http://localhost:8000" + cfg.get("baseurl", "") + "/")
