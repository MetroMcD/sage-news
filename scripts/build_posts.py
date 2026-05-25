#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from html import escape
import shutil

ROOT = Path('/home/rene/sage-news')
POSTS_DIR = ROOT / 'posts'
MANIFEST_PATH = ROOT / 'posts-manifest.json'
INDEX_PATH = ROOT / 'index.html'
EXCLUDE_DIRS = {'assets', 'posts', 'uploads', 'datenschutz', 'impressum', '.git', '.github', '.state', 'scripts', 'node_modules'}
CATEGORY_META = {
    'Sage 100': {'color': '#0a3b93', 'bg': '#dceeff'},
    'Sage X3': {'color': '#1a6b3a', 'bg': '#d4f0e0'},
    'Sage Operations': {'color': '#7b3a00', 'bg': '#fde8cc'},
    'Sage Intact': {'color': '#5a1d8a', 'bg': '#ede0f8'},
}
TAG_COLORS = {
    'Release': {'bg': '#e8f0fe', 'color': '#1a56db'},
    'Neu': {'bg': '#d4f0e0', 'color': '#1a6b3a'},
    'KI': {'bg': '#fde8cc', 'color': '#7b3a00'},
    'Cloud': {'bg': '#e0f0ff', 'color': '#0a5a99'},
    'Compliance': {'bg': '#fde8e8', 'color': '#9b1c1c'},
    'Perspektive': {'bg': '#ede0f8', 'color': '#5a1d8a'},
    'Tool': {'bg': '#f0f0f0', 'color': '#374151'},
    'API': {'bg': '#e8fce8', 'color': '#1a6b3a'},
    'News': {'bg': '#f0f4ff', 'color': '#3730a3'},
}
REQUIRED_META = ['title', 'date', 'category', 'tag', 'summary', 'readTime', 'featured']
ALLOWED_CATEGORIES = {'Sage 100', 'Sage X3', 'Sage Operations', 'Sage Intact'}
ALLOWED_TAGS = {'Release', 'Neu', 'KI', 'Cloud', 'Compliance', 'Perspektive', 'News'}
DATE_RE = re.compile(r'^\d{1,2}\.\s+[A-Za-zÄÖÜäöü]+\s+\d{4}$')
READTIME_RE = re.compile(r'^\d+\s+min$')


@dataclass
class Post:
    source_path: Path
    file_stem: str
    meta: dict
    body: str

    @property
    def slug(self) -> str:
        return self.meta['slug']


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$', raw)
    if not match:
        raise ValueError('Frontmatter fehlt oder ist ungültig')
    meta = {}
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    body = match.group(2).strip()
    return meta, body


def normalize_slug(value: str) -> str:
    value = value.lower()
    value = value.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-')


def render_inline(text: str) -> str:
    placeholders: list[str] = []

    def keep_code(match: re.Match[str]) -> str:
        placeholders.append(match.group(1))
        return f'@@CODE{len(placeholders)-1}@@'

    safe = escape(text)
    safe = re.sub(r'`([^`]+)`', keep_code, safe)
    safe = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', safe)
    safe = re.sub(r'\*(.+?)\*', r'<em>\1</em>', safe)
    safe = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{escape(m.group(2), quote=True)}">{m.group(1)}</a>', safe)
    for idx, code in enumerate(placeholders):
        safe = safe.replace(f'@@CODE{idx}@@', f'<code>{escape(code)}</code>')
    return safe


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    html_lines: list[str] = []
    paragraph: list[str] = []
    in_list = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            html_lines.append(f"<p>{render_inline(' '.join(paragraph).strip())}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            html_lines.append('</ul>')
            in_list = False

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            flush_paragraph()
            close_list()
            continue
        if stripped == '---':
            flush_paragraph()
            close_list()
            html_lines.append('<hr>')
            continue
        if stripped.startswith('## '):
            flush_paragraph()
            close_list()
            html_lines.append(f'<h2>{render_inline(stripped[3:].strip())}</h2>')
            continue
        if stripped.startswith('### '):
            flush_paragraph()
            close_list()
            html_lines.append(f'<h3>{render_inline(stripped[4:].strip())}</h3>')
            continue
        if re.match(r'^-\s+', stripped):
            flush_paragraph()
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{render_inline(re.sub(r"^-\\s+", "", stripped))}</li>')
            continue
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    return ''.join(html_lines)


def load_posts() -> list[Post]:
    posts: list[Post] = []
    for path in sorted(POSTS_DIR.glob('*.md')):
        if path.name.startswith('_'):
            continue
        raw = path.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(raw)
        for key in REQUIRED_META:
            if key not in meta or meta[key] == '':
                raise ValueError(f'{path.name}: Pflichtfeld fehlt: {key}')
        derived_slug = meta.get('slug') or re.sub(r'^\d{4}-\d{2}-\d{2}-', '', path.stem)
        meta['slug'] = normalize_slug(derived_slug)
        if not meta['slug']:
            raise ValueError(f'{path.name}: slug konnte nicht abgeleitet werden')
        meta['featured'] = str(meta['featured']).lower() == 'true'
        posts.append(Post(source_path=path, file_stem=path.stem, meta=meta, body=body))
    slugs = [p.slug for p in posts]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise ValueError(f'Doppelte Slugs: {", ".join(duplicates)}')
    return sorted(posts, key=lambda p: p.file_stem, reverse=True)


def validate_posts(posts: list[Post]) -> None:
    for post in posts:
        meta = post.meta
        if meta['category'] not in ALLOWED_CATEGORIES:
            raise ValueError(f'{post.source_path.name}: Ungültige Kategorie: {meta["category"]}')
        tags = [tag.strip() for tag in meta['tag'].split(',') if tag.strip()]
        if not 1 <= len(tags) <= 2:
            raise ValueError(f'{post.source_path.name}: tag muss 1 oder 2 Werte enthalten')
        invalid_tags = [tag for tag in tags if tag not in ALLOWED_TAGS]
        if invalid_tags:
            raise ValueError(f'{post.source_path.name}: Ungültige Tags: {", ".join(invalid_tags)}')
        if not DATE_RE.match(meta['date']):
            raise ValueError(f'{post.source_path.name}: Ungültiges Datum: {meta["date"]}')
        if not READTIME_RE.match(meta['readTime']):
            raise ValueError(f'{post.source_path.name}: Ungültige readTime: {meta["readTime"]}')
        if len(meta['summary']) > 220:
            raise ValueError(f'{post.source_path.name}: summary zu lang (>220 Zeichen)')
        if len(post.slug) > 60:
            raise ValueError(f'{post.source_path.name}: slug zu lang (>60 Zeichen)')
        if 'Quelle:' not in post.body:
            raise ValueError(f'{post.source_path.name}: Quellenangabe fehlt im Body')


def build_manifest(posts: list[Post]) -> dict:
    return {
        'posts': [
            {
                'id': p.file_stem,
                'slug': p.slug,
                'permalink': p.slug,
                'title': p.meta['title'],
                'summary': p.meta['summary'],
                'category': p.meta['category'],
                'tag': p.meta['tag'],
                'date': p.meta['date'],
                'readTime': p.meta['readTime'],
                'featured': p.meta['featured'],
                'body': p.body,
            }
            for p in posts
        ]
    }


def split_tags(tag_string: str) -> list[str]:
    return [part.strip() for part in tag_string.split(',') if part.strip()]


def build_article_html(post: Post) -> str:
    cat = CATEGORY_META.get(post.meta['category'], {'bg': '#dceeff', 'color': '#0a3b93'})
    tags = split_tags(post.meta['tag'])
    tag_html = ''.join(
        f'<span class="badge badge-tag" style="background:{TAG_COLORS.get(tag, {"bg":"#f0f0f0","color":"#374151"})["bg"]};color:{TAG_COLORS.get(tag, {"bg":"#f0f0f0","color":"#374151"})["color"]}">{escape(tag)}</span>'
        for tag in tags
    )
    article_html = markdown_to_html(post.body)
    title = escape(post.meta['title'])
    summary = escape(post.meta['summary'])
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} – sage news</title>
<meta name="description" content="{summary}">
<link rel="canonical" href="https://sage-news.de/{post.slug}/">
<link rel="icon" type="image/png" href="../assets/favicon.png">
<link rel="apple-touch-icon" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {{--sn-blue-950:#061b49;--sn-blue-900:#082b6f;--sn-blue-800:#0a3b93;--sn-blue-600:#0d6ecf;--sn-blue-100:#e8f7ff;--sn-ink:#07172f;--sn-muted:#5f728a;--sn-border:#d6e9f8;--sn-bg:#f4f9fe;}}
*,*::before,*::after{{box-sizing:border-box}} body{{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--sn-bg);color:var(--sn-ink);-webkit-font-smoothing:antialiased}}
a{{color:var(--sn-blue-600);text-decoration:none}}a:hover{{text-decoration:underline}}.container{{max-width:860px;margin:0 auto;padding:24px 20px 64px}}.hero{{margin-top:24px;background:linear-gradient(135deg,var(--sn-blue-950),var(--sn-blue-800));color:white;border-radius:16px;padding:32px}}.badges{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}.badge{{display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:700}}.badge-category{{background:{cat['bg']};color:{cat['color']}}}h1{{margin:0 0 12px;font-size:32px;line-height:1.2}}.meta{{font-size:13px;color:rgba(255,255,255,.72)}}.article{{margin-top:24px;background:#fff;border:1.5px solid var(--sn-border);border-radius:16px;padding:32px}}.summary{{background:var(--sn-blue-100);border-left:3px solid var(--sn-blue-600);border-radius:10px;padding:16px 20px;margin-bottom:24px}}.summary-label{{font-size:11px;font-weight:800;color:var(--sn-blue-800);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}}.prose{{font-size:16px;line-height:1.8}}.prose h2{{font-size:22px;line-height:1.3;margin:1.6em 0 .6em;padding-bottom:8px;border-bottom:1.5px solid var(--sn-border)}}.prose h3{{font-size:18px;line-height:1.35;margin:1.35em 0 .55em}}.prose p{{margin:0 0 1em}}.prose ul{{margin:0 0 1em 1.2em;padding:0}}.prose li{{margin:0 0 .5em}}.prose strong{{color:var(--sn-ink)}}.prose code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#eef6ff;padding:2px 6px;border-radius:5px;font-size:.92em}}.prose hr{{border:none;border-top:1.5px solid var(--sn-border);margin:1.5em 0}}.footer{{border-top:1.5px solid var(--sn-border);background:#fff}}.footer-inner{{max-width:1140px;margin:0 auto;padding:18px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px;color:var(--sn-muted);font-size:12px}}@media (max-width:700px){{h1{{font-size:26px}}.hero,.article{{padding:22px}}.topbar-inner,.footer-inner{{flex-direction:column;align-items:flex-start}}}}
</style>
</head>
<body>
<header style="background:var(--sn-blue-950);border-bottom:1.5px solid rgba(255,255,255,0.08)"><div style="max-width:1140px;margin:0 auto;padding:0 16px"><div style="display:flex;align-items:center;height:64px;gap:16px"><a href="../" title="Zur Startseite" style="background:none;border:none;cursor:pointer;padding:0;flex-shrink:0;line-height:0;text-decoration:none"><img src="../assets/sage-news_logo_3.png" alt="sage news" style="height:52px;width:auto;display:block;mix-blend-mode:lighten"></a><div class="sn-nav-divider" style="width:1px;height:28px;background:rgba(255,255,255,0.12);flex-shrink:0"></div><nav class="sn-desktop-nav" style="display:flex;gap:2px;align-items:center;flex:1;overflow:hidden"><a href="../" style="background:#ffd22e;color:#07172f;font-weight:700;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Alle News</a><a href="../#sage100" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Sage 100</a><a href="../#sagex3" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Sage X3</a><a href="../#operations" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Sage Operations</a><a href="../#systemcheck" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Systemcheck</a><a href="../#info" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Info</a></nav><div style="margin-left:auto;flex-shrink:0;display:flex;align-items:center;gap:10px"><span style="background:#ffd22e;color:#07172f;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;letter-spacing:.04em">BETA</span><a class="sn-backlink-mobile" href="../" style="display:none;font-size:14px;font-weight:600;color:rgba(255,255,255,0.85);text-decoration:none;white-space:nowrap">← Zur Übersicht</a></div></div></div><style>@media (max-width:680px){{.sn-nav-divider,.sn-desktop-nav{{display:none !important}}.sn-backlink-mobile{{display:inline-block !important}}}}</style></header>
<main class="container">
<section class="hero"><div class="badges"><span class="badge badge-category">{escape(post.meta['category'])}</span>{tag_html}</div><h1>{title}</h1><div class="meta">{escape(post.meta['date'])} · {escape(post.meta['readTime'])} Lesezeit</div></section>
<article class="article"><div class="summary"><div class="summary-label">Kurzfazit</div><div>{summary}</div></div><div class="prose">{article_html}</div></article>
</main>
<footer class="footer"><div class="footer-inner"><div>© 2026 René Münz</div><a href="../">Zurück zu sage news</a></div></footer>
</body>
</html>
'''


def sync_index_loader() -> None:
    text = INDEX_PATH.read_text(encoding='utf-8')
    replacement = '''// ── POSTS MANIFEST LOADER ───────────────────────────────────────────────────
async function loadPostsFromManifest() {
  const manifestUrl = `./posts-manifest.json?v=${Date.now()}`;
  const res = await fetch(manifestUrl, { cache: "no-store" });
  if (!res.ok) throw new Error(`Manifest ${res.status}`);
  const manifest = await res.json();
  return { posts: manifest.posts || [], source: "manifest" };
}

'''
    github_marker = '// ── GITHUB LOADER ──────────────────────────────────────────────────────────'
    manifest_marker = '// ── POSTS MANIFEST LOADER ───────────────────────────────────────────────────'
    end = text.index('// ── BRAND COLORS ───────────────────────────────────────────────────────────')
    if github_marker in text:
        start = text.index(github_marker)
        text = text[:start] + replacement + text[end:]
    elif manifest_marker in text:
        start = text.index(manifest_marker)
        text = text[:start] + replacement + text[end:]
    if 'loadPostsFromGitHub(GH_CONFIG).then(({ posts: loaded, source }) => {' in text:
        text = text.replace('loadPostsFromGitHub(GH_CONFIG).then(({ posts: loaded, source }) => {', 'loadPostsFromManifest().then(({ posts: loaded, source }) => {')
    INDEX_PATH.write_text(text, encoding='utf-8')


def cleanup_generated_dirs(valid_slugs: set[str], dry_run: bool = False) -> list[str]:
    removed: list[str] = []
    for child in ROOT.iterdir():
        if not child.is_dir() or child.name in EXCLUDE_DIRS or child.name.startswith('.'):
            continue
        index_file = child / 'index.html'
        if not index_file.exists() or child.name in valid_slugs:
            continue
        removed.append(child.name)
        if not dry_run:
            shutil.rmtree(child)
    return sorted(removed)


def build() -> None:
    posts = load_posts()
    validate_posts(posts)
    manifest = build_manifest(posts)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    sync_index_loader()
    valid_slugs = {post.slug for post in posts}
    cleanup_generated_dirs(valid_slugs)
    for post in posts:
        target = ROOT / post.slug
        target.mkdir(exist_ok=True)
        (target / 'index.html').write_text(build_article_html(post), encoding='utf-8')
    print(f'Built {len(posts)} posts.')


def validate() -> None:
    posts = load_posts()
    validate_posts(posts)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8')) if MANIFEST_PATH.exists() else {'posts': []}
    manifest_posts = manifest.get('posts', [])
    manifest_slugs = [post.get('slug') for post in manifest_posts]
    expected_slugs = [post.slug for post in posts]
    if manifest_slugs != expected_slugs:
        raise ValueError('posts-manifest.json ist nicht synchron mit posts/')
    for post in posts:
        html_path = ROOT / post.slug / 'index.html'
        if not html_path.exists():
            raise ValueError(f'Fehlende HTML-Seite: {post.slug}/index.html')
        html = html_path.read_text(encoding='utf-8')
        canonical = f'https://sage-news.de/{post.slug}/'
        if canonical not in html:
            raise ValueError(f'Falscher Canonical-Link in {post.slug}/index.html')
    index_text = INDEX_PATH.read_text(encoding='utf-8')
    if 'api.github.com' in index_text or 'raw.githubusercontent.com' in index_text:
        raise ValueError('index.html nutzt noch den alten GitHub-Runtime-Loader')
    stale_dirs = cleanup_generated_dirs(set(expected_slugs), dry_run=True)
    if stale_dirs:
        raise ValueError('Verwaiste Artikelordner gefunden: ' + ', '.join(stale_dirs))
    print(f'Validated {len(posts)} posts.')


def main() -> None:
    parser = argparse.ArgumentParser(description='Build and validate sage-news posts.')
    parser.add_argument('command', nargs='?', default='build', choices=['build', 'validate'])
    args = parser.parse_args()
    if args.command == 'build':
        build()
    else:
        validate()


if __name__ == '__main__':
    main()
