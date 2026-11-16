#!/usr/bin/env python3
"""Cross-check the website and the PDFs → CHECK-REPORT.md

  python3 tools/check.py                 full report
  python3 tools/check.py --find "text"   every web page / PDF / source that contains "text"

Sections:
  1. Languages: web keys missing per language · dossiers missing per language
  2. Contact data: email and web address present and spelled right
  3. House style: banned words, wrong name spellings (content/facts.json)
  4. Files: downloads registered in data.json that have no PDF, PDFs not registered, photos without original
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((ROOT/'content/data.json').read_text(encoding='utf-8'))
facts = json.loads((ROOT/'content/facts.json').read_text(encoding='utf-8'))
LANGS = data['languages']; DEFAULT = data['site']['default_lang']

def pdf_text(p):
    try: return subprocess.run(['pdftotext', '-layout', str(p), '-'], capture_output=True, text=True).stdout
    except FileNotFoundError: return ''

def sources():
    """(label, text) for every place a fact can live."""
    for p in sorted((ROOT/'content').rglob('*.json')):
        if p.name == 'facts.json': continue
        yield str(p.relative_to(ROOT)), p.read_text(encoding='utf-8')
    for p in sorted((ROOT/'dossiers').rglob('*')):
        if p.suffix in ('.json', '.html', '.md') and not p.name.startswith('.'): yield str(p.relative_to(ROOT)), p.read_text(encoding='utf-8')
    for p in sorted((ROOT/'docs').glob('*/index.html')): yield str(p.relative_to(ROOT)), re.sub('<[^>]+>', ' ', p.read_text(encoding='utf-8'))
    for p in sorted((ROOT/'static/pdf').glob('*.pdf')): yield str(p.relative_to(ROOT)), pdf_text(p)

def keys(d, p=''):
    return {p + k for k in d if not k.startswith('_')} | {x for k, v in d.items() if isinstance(v, dict) for x in keys(v, p + k + '.')}

def main():
    if '--find' in sys.argv:
        q = sys.argv[sys.argv.index('--find') + 1].lower()
        for label, text in sources():
            n = text.lower().count(q)
            if n: print(f'{n:3}× {label}')
        return
    out = ['# CHECK-REPORT', '']
    # 1. languages
    out += ['## 1. Languages', '']
    i18n = {l: json.loads((ROOT/'content/i18n'/f'{l}.json').read_text(encoding='utf-8')) for l in LANGS if (ROOT/'content/i18n'/f'{l}.json').exists()}
    for l in LANGS:
        if l not in i18n: out.append(f'- ❌ web: no content/i18n/{l}.json')
    ref = keys(i18n[DEFAULT])
    for l, d in i18n.items():
        miss = ref - keys(d)
        if miss: out.append(f'- ❌ web {l}: missing {", ".join(sorted(miss))}')
    for folder in sorted((ROOT/'dossiers').iterdir()):
        if not folder.is_dir() or (folder/'ES-ONLY').exists(): continue
        have = {p.stem for p in folder.glob('*.json')} | {p.stem for p in folder.glob('??.html')}
        miss = [l for l in LANGS if l not in have]
        if miss: out.append(f'- ⚠ dossier {folder.name}: no {" ".join(miss)}')
    # 2-3. contact + style
    out += ['', '## 2. Contact data and 3. House style', '']
    email, web = facts['contact']['email'], facts['contact']['web']
    for label, text in sources():
        low = text.lower()
        for bad in re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text):
            if 'victoriasickness' in bad.lower() and bad.lower() != email: out.append(f'- ❌ {label}: email "{bad}" (should be {email})')
        m = re.search(r'(?:i18n/|dossiers/[^/]+/)([a-z]{2})\.(?:json|html)$|_([A-Z]{2})_', label)
        lang = (m.group(1) or m.group(2).lower()) if m else None
        for w in facts.get('banned', {}).get('*', []) + (facts.get('banned', {}).get(lang, []) if lang else []):
            if w.lower() in low: out.append(f'- ❌ {label}: banned "{w}"' + (f' (pronouns: {facts["pronouns"][lang]})' if lang and w in facts.get('banned', {}).get(lang, []) else ''))
        for right, wrongs in facts.get('names', {}).items():
            for w in wrongs:
                if re.search(r'(?<![\w])' + re.escape(w) + r'(?![\w])', text): out.append(f'- ❌ {label}: "{w}" → {right}')
        if label.startswith('static/pdf') and 'compacto' in label and web not in low:
            out.append(f'- ⚠ {label}: web address {web} not found')
    # 5. private data must never be in this public repo
    out += ['', '## 5. Private data (public repo!)', '']
    for label, text in sources():
        if 'facts.json' in label or label.startswith('static/fonts'): continue
        for rule in facts.get('private', []):
            for m in re.finditer(rule['pattern'], text):
                out.append(f'- ❌ {label}: {rule["why"]} → "{m.group(0)}"')
    # 4. files
    out += ['', '## 4. Files', '']
    downloads = json.loads((ROOT/'content/downloads.json').read_text(encoding='utf-8'))
    registered = set()
    for key, per in downloads.items():
        if key not in data['downloads']: out.append(f'- ⚠ downloads.json "{key}" has no entry in data.json → downloads')
        for l, u in per.items():
            if not u: continue
            registered.add(pathlib.Path(u).name)
            if not (ROOT/'static'/u.lstrip('/')).exists(): out.append(f'- ❌ download {key}/{l}: missing static{u}')
    for p in (ROOT/'static/pdf').glob('*.pdf'):
        if p.name not in registered: out.append(f'- ⚠ {p.name} is not in content/downloads.json')
        if p.stat().st_size > 3e6: out.append(f'- ⚠ {p.name} is {p.stat().st_size/1e6:.1f} MB (limit 3 MB)')
    have = {p.stem for p in (ROOT/'source-images').iterdir()}
    used = [i['file'] for s in data['shows'] for i in s['images']] + [s.get('video_cover') for s in data['shows']] + [data['about']['portrait']] + [i['file'] for i in data['about']['images']]
    for u in used:
        if u and pathlib.PurePosixPath(u).stem not in have: out.append(f'- ❌ photo "{u}" is used but not in source-images/')
    if not data['photos'].get('credits'): out.append('- ⚠ no photographer credits yet (data.json → photos.credits)')
    problems = sum(1 for x in out if x.startswith('- ❌'))
    out.insert(1, f'{problems} problem(s), {sum(1 for x in out if x.startswith("- ⚠"))} warning(s).\n')
    (ROOT/'CHECK-REPORT.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('\n'.join(out))

if __name__ == '__main__':
    main()
