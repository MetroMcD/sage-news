#!/usr/bin/env python3
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from html import escape
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'posts'
MANIFEST_PATH = ROOT / 'posts-manifest.json'
INDEX_PATH = ROOT / 'index.html'
APP_SRC_PATH = ROOT / 'src' / 'app.jsx'
CATEGORY_DIR = ROOT / 'kategorie'
SITEMAP_PATH = ROOT / 'sitemap.xml'
FEED_PATH = ROOT / 'feed.xml'
SITE = 'https://sage-news.de'
AUTHOR = 'René Münz'
EXCLUDE_DIRS = {'assets', 'posts', 'uploads', 'datenschutz', 'impressum', '.git', '.github', '.state', 'scripts', 'node_modules', 'kategorie', 'src'}
# Statische Seiten, die neben Startseite und Beiträgen in die Sitemap gehören.
# Cloudflare normalisiert /foo.html -> /foo, deshalb steht systemcheck ohne Endung hier.
STATIC_URLS = ['/impressum/', '/datenschutz/', '/systemcheck']
# Ab diesem Alter wandert ein Beitrag von der Kategorieseite in deren Archiv.
# Stichtag ist der Build-Tag, der Build ist damit bewusst datumsabhaengig.
ARCHIVE_AFTER_MONTHS = 24
CATEGORY_META = {
    'Sage 100': {'color': '#0a3b93', 'bg': '#dceeff'},
    'Sage X3': {'color': '#1a6b3a', 'bg': '#d4f0e0'},
    'Sage Operations': {'color': '#7b3a00', 'bg': '#fde8cc'},
    'Sage Intact': {'color': '#5a1d8a', 'bg': '#ede0f8'},
}
# Eigene URLs für die Kategorien. Das Präfix /kategorie/ ist zwingend:
# "sage-operations" ist bereits der Slug eines Beitrags.
CATEGORY_SLUGS = {
    'Sage 100': 'sage-100',
    'Sage X3': 'sage-x3',
    'Sage Operations': 'sage-operations',
    'Sage Intact': 'sage-intact',
}
CATEGORY_INTRO = {
    'Sage 100': 'Alle Meldungen zu Sage 100: LiveUpdates, Service Packs, Systemvoraussetzungen und Hinweise zum laufenden Betrieb.',
    'Sage X3': 'Meldungen rund um Sage X3.',
    'Sage Operations': 'Alle Meldungen zu Sage Operations: Produktupdates, API-Änderungen und Neuerungen der Plattform.',
    'Sage Intact': 'Meldungen rund um Sage Intacct.',
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
SOURCE_SUFFIX = '(zusammengefasst mit KI für Sage-News.de)'
SOURCE_BLOCK_RE = re.compile(r'\n\s*---\s*\n(Quelle:[^\n]+)\s*$')
ALLOWED_CATEGORIES = {'Sage 100', 'Sage X3', 'Sage Operations', 'Sage Intact'}
ALLOWED_TAGS = {'Release', 'Neu', 'KI', 'Cloud', 'Compliance', 'Perspektive', 'News'}
DATE_RE = re.compile(r'^\d{1,2}\.\s+[A-Za-zÄÖÜäöü]+\s+\d{4}$')
READTIME_RE = re.compile(r'^\d+\s+min$')
ISO_DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-')

# Kopf- und Fusszeile teilen sich Artikel- und Kategorieseiten. Root-absolute
# Pfade, damit derselbe Baustein in /slug/ und /kategorie/slug/ funktioniert.
SITE_HEADER = '<header style="background:var(--sn-blue-950);border-bottom:1.5px solid rgba(255,255,255,0.08)"><div style="max-width:1140px;margin:0 auto;padding:0 16px"><div style="display:flex;align-items:center;height:64px;gap:16px"><a href="/" title="Zur Startseite" style="background:none;border:none;cursor:pointer;padding:0;flex-shrink:0;line-height:0;text-decoration:none"><img src="/assets/sage-news_logo_3.png" alt="sage news" style="height:52px;width:auto;display:block;mix-blend-mode:lighten"></a><div class="sn-nav-divider" style="width:1px;height:28px;background:rgba(255,255,255,0.12);flex-shrink:0"></div><nav class="sn-desktop-nav" style="display:flex;gap:2px;align-items:center;flex:1;overflow:hidden"><a href="/" style="background:#ffd22e;color:#07172f;font-weight:700;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Alle News</a><a href="/kategorie/sage-100/" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Sage 100</a><a href="/kategorie/sage-x3/" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Sage X3</a><a href="/kategorie/sage-operations/" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Sage Operations</a><a href="/systemcheck" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Systemcheck</a><a href="/#info" style="color:rgba(255,255,255,0.72);font-weight:500;font-size:13.5px;padding:7px 13px;border-radius:8px;text-decoration:none;white-space:nowrap">Info</a></nav><div style="margin-left:auto;flex-shrink:0;display:flex;align-items:center;gap:10px"><span style="background:#ffd22e;color:#07172f;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;letter-spacing:.04em">BETA</span><a class="sn-backlink-mobile" href="/" style="display:none;font-size:14px;font-weight:600;color:rgba(255,255,255,0.85);text-decoration:none;white-space:nowrap">← Zur Übersicht</a></div></div></div><style>@media (max-width:680px){.sn-nav-divider,.sn-desktop-nav{display:none !important}.sn-backlink-mobile{display:inline-block !important}}</style></header>'
SITE_FOOTER = '<footer class="footer"><div class="footer-inner"><div>© 2026 René Münz</div><a href="/">Zurück zu sage news</a></div></footer>'

# Lokale Inter-Schnitte statt fonts.googleapis.com: identische Schrift,
# aber kein render-blockierender Fremdzugriff.
FONT_FACE_CSS = ''.join(
    f"@font-face{{font-family:'Inter';font-style:normal;font-weight:{w};"
    f"font-display:swap;src:url('/assets/fonts/Inter-{w}.ttf') format('truetype');}}"
    for w in (400, 500, 600, 700, 800, 900)
)


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
            item_text = re.sub(r'^-\s+', '', stripped)
            html_lines.append(f'<li>{render_inline(item_text)}</li>')
            continue
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    return ''.join(html_lines)


def split_source(body: str) -> tuple[str, str]:
    """Trennt die Quellen-Fußzeile vom Fließtext ab."""
    match = SOURCE_BLOCK_RE.search(body)
    if not match:
        return body, ''
    return body[:match.start()].rstrip(), match.group(1).strip()


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
        source = split_source(post.body)[1]
        if not source:
            raise ValueError(f'{post.source_path.name}: Quellen-Fußzeile fehlt am Textende')
        if not source.endswith(SOURCE_SUFFIX):
            raise ValueError(f'{post.source_path.name}: Quellen-Fußzeile ohne KI-Hinweis {SOURCE_SUFFIX}')


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


def iso_date(post: Post) -> str:
    """ISO-Datum aus dem Dateinamen. Das Frontmatter-Feld `date` ist deutscher
    Fließtext ("27. Juli 2026") und für Maschinen unbrauchbar."""
    match = ISO_DATE_RE.match(post.file_stem)
    if not match:
        raise ValueError(f'{post.file_stem}: kein ISO-Datum am Dateinamen-Anfang')
    return match.group(1)


def category_path(category: str) -> str:
    return f'/kategorie/{CATEGORY_SLUGS[category]}/'


def render_card(post: Post) -> str:
    """Kartenmarkup mit exakt den Inline-Styles aus PostCard (src/app.jsx).
    React ersetzt das auf der Startseite beim Mount; auf den Kategorieseiten
    ist es die finale Darstellung."""
    cat = CATEGORY_META.get(post.meta['category'], {'bg': '#dceeff', 'color': '#0a3b93'})
    tag = post.meta['tag']
    tag_meta = TAG_COLORS.get(tag, {'bg': '#f0f0f0', 'color': '#374151'})
    return (
        f'<a href="/{post.slug}/" style="display:block;text-decoration:none;background:white;'
        # Keine color-Angabe: der Titel erbt wie auf der Startseite das Blau aus
        # der a-Regel. Sonst weicht die Kartenoptik vom React-Rendering ab.
        'border:1.5px solid var(--sn-border);border-radius:14px;padding:22px;'
        'box-shadow:0 1px 4px rgba(6,27,73,0.05)">'
        '<div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap">'
        f'<span style="display:inline-block;background:{cat["bg"]};color:{cat["color"]};font-weight:700;'
        'font-size:11px;letter-spacing:0.03em;padding:2px 8px;border-radius:999px;white-space:nowrap">'
        f'{escape(post.meta["category"])}</span>'
        f'<span style="display:inline-block;background:{tag_meta["bg"]};color:{tag_meta["color"]};'
        'font-weight:600;font-size:11px;padding:2px 8px;border-radius:999px;white-space:nowrap">'
        f'{escape(tag)}</span>'
        '</div>'
        '<h3 style="font-size:15px;font-weight:700;line-height:1.35;margin:0 0 8px">'
        f'{escape(post.meta["title"])}</h3>'
        '<p style="font-size:13px;color:var(--sn-muted);line-height:1.6;margin:0 0 14px">'
        f'{escape(post.meta["summary"])}</p>'
        '<div style="display:flex;gap:10px;align-items:center">'
        f'<time datetime="{iso_date(post)}" style="font-size:12px;color:var(--sn-muted)">'
        f'{escape(post.meta["date"])}</time>'
        f'<span style="font-size:12px;color:var(--sn-muted)">· {escape(post.meta["readTime"])}</span>'
        '<span style="margin-left:auto;font-size:12px;font-weight:700;color:var(--sn-blue-600)">'
        'Weiterlesen →</span>'
        '</div></a>'
    )


def render_card_grid(posts: list[Post]) -> str:
    cards = ''.join(render_card(post) for post in posts)
    return (
        '<div class="post-grid-regular" style="display:grid;'
        f'grid-template-columns:repeat(2, 1fr);gap:16px">{cards}</div>'
    )


def build_home_prerender(posts: list[Post], limit: int = 8) -> str:
    """Inhalt für #root. React leert den Container beim Mount (createRoot, nicht
    hydrateRoot) — das hier ist also reine Crawler-Nahrung und kann die finale
    Darstellung nicht verändern. Umfang = was React auch zeigt (postsPerPage)."""
    cat_links = ''.join(
        f'<a href="{category_path(name)}">{escape(name)}</a> '
        for name in CATEGORY_SLUGS
    )
    return (
        '<div style="max-width:1140px;margin:0 auto;padding:24px 20px 64px">'
        '<h1>sage news – Neuigkeiten zu Sage 100, Sage X3 und Sage Operations</h1>'
        f'<nav>{cat_links}</nav>'
        f'{render_card_grid(posts[:limit])}'
        '</div>'
    )


def article_jsonld(post: Post) -> str:
    url = f'{SITE}/{post.slug}/'
    category = post.meta['category']
    blocks = [
        {
            '@context': 'https://schema.org',
            '@type': 'NewsArticle',
            'headline': post.meta['title'],
            'description': post.meta['summary'],
            'datePublished': iso_date(post),
            'dateModified': iso_date(post),
            'inLanguage': 'de-DE',
            'articleSection': category,
            'author': {'@type': 'Person', 'name': AUTHOR},
            'publisher': {
                '@type': 'Organization',
                'name': 'sage news',
                'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/sage-news_logo_3.png'},
            },
            'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        },
        {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': category,
                 'item': SITE + category_path(category)},
                {'@type': 'ListItem', 'position': 3, 'name': post.meta['title'], 'item': url},
            ],
        },
    ]
    return ''.join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>\n'
        for b in blocks
    )


def build_article_html(post: Post) -> str:
    cat = CATEGORY_META.get(post.meta['category'], {'bg': '#dceeff', 'color': '#0a3b93'})
    tags = split_tags(post.meta['tag'])
    tag_html = ''.join(
        f'<span class="badge badge-tag" style="background:{TAG_COLORS.get(tag, {"bg":"#f0f0f0","color":"#374151"})["bg"]};color:{TAG_COLORS.get(tag, {"bg":"#f0f0f0","color":"#374151"})["color"]}">{escape(tag)}</span>'
        for tag in tags
    )
    body_text, source_text = split_source(post.body)
    article_html = markdown_to_html(body_text)
    if source_text:
        article_html += f'<hr><p class="article-source">{render_inline(source_text)}</p>'
    title = escape(post.meta['title'])
    summary = escape(post.meta['summary'])
    iso = iso_date(post)
    category = escape(post.meta['category'])
    cat_href = category_path(post.meta['category'])
    jsonld = article_jsonld(post)
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
<link rel="alternate" type="application/atom+xml" title="sage news" href="/feed.xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="sage news">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{summary}">
<meta property="og:url" content="https://sage-news.de/{post.slug}/">
<meta property="og:image" content="https://sage-news.de/assets/sage-news_logo_3.png">
<meta property="article:published_time" content="{iso}">
<meta property="article:section" content="{category}">
<meta property="article:author" content="{AUTHOR}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{summary}">
<meta name="twitter:image" content="https://sage-news.de/assets/sage-news_logo_3.png">
{jsonld}<style>
{FONT_FACE_CSS}
:root {{--sn-blue-950:#061b49;--sn-blue-900:#082b6f;--sn-blue-800:#0a3b93;--sn-blue-600:#0d6ecf;--sn-blue-100:#e8f7ff;--sn-ink:#07172f;--sn-muted:#5f728a;--sn-border:#d6e9f8;--sn-bg:#f4f9fe;}}
*,*::before,*::after{{box-sizing:border-box}} body{{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--sn-bg);color:var(--sn-ink);-webkit-font-smoothing:antialiased}}
a{{color:var(--sn-blue-600);text-decoration:none}}a:hover{{text-decoration:underline}}.container{{max-width:860px;margin:0 auto;padding:24px 20px 64px}}.hero{{margin-top:24px;background:linear-gradient(135deg,var(--sn-blue-950),var(--sn-blue-800));color:white;border-radius:16px;padding:32px}}.badges{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}.badge{{display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:700}}.badge-category{{background:{cat['bg']};color:{cat['color']};text-decoration:none}}.badge-category:hover{{text-decoration:underline}}h1{{margin:0 0 12px;font-size:32px;line-height:1.2}}.meta{{font-size:13px;color:rgba(255,255,255,.72)}}.article{{margin-top:24px;background:#fff;border:1.5px solid var(--sn-border);border-radius:16px;padding:32px}}.summary{{background:var(--sn-blue-100);border-left:3px solid var(--sn-blue-600);border-radius:10px;padding:16px 20px;margin-bottom:24px}}.summary-label{{font-size:11px;font-weight:800;color:var(--sn-blue-800);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}}.prose{{font-size:16px;line-height:1.8}}.prose h2{{font-size:22px;line-height:1.3;margin:1.6em 0 .6em;padding-bottom:8px;border-bottom:1.5px solid var(--sn-border)}}.prose h3{{font-size:18px;line-height:1.35;margin:1.35em 0 .55em}}.prose p{{margin:0 0 1em}}.prose ul{{margin:0 0 1em 1.2em;padding:0}}.prose li{{margin:0 0 .5em}}.prose strong{{color:var(--sn-ink)}}.prose code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#eef6ff;padding:2px 6px;border-radius:5px;font-size:.92em}}.prose hr{{border:none;border-top:1.5px solid var(--sn-border);margin:1.5em 0}}.prose .article-source{{color:var(--sn-muted);font-size:14px;font-style:italic;margin-bottom:0}}.footer{{border-top:1.5px solid var(--sn-border);background:#fff}}.footer-inner{{max-width:1140px;margin:0 auto;padding:18px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px;color:var(--sn-muted);font-size:12px}}@media (max-width:700px){{h1{{font-size:26px}}.hero,.article{{padding:22px}}.topbar-inner,.footer-inner{{flex-direction:column;align-items:flex-start}}}}
</style>
</head>
<body>
{SITE_HEADER}
<main class="container">
<section class="hero"><div class="badges"><a class="badge badge-category" href="{cat_href}">{category}</a>{tag_html}</div><h1>{title}</h1><div class="meta"><time datetime="{iso}">{escape(post.meta['date'])}</time> · {escape(post.meta['readTime'])} Lesezeit</div></section>
<article class="article"><div class="summary"><div class="summary-label">Kurzfazit</div><div>{summary}</div></div><div class="prose">{article_html}</div></article>
</main>
{SITE_FOOTER}
</body>
</html>
'''


BASE_CSS = (
    ':root{--sn-blue-950:#061b49;--sn-blue-900:#082b6f;--sn-blue-800:#0a3b93;'
    '--sn-blue-600:#0d6ecf;--sn-blue-100:#e8f7ff;--sn-ink:#07172f;--sn-muted:#5f728a;'
    '--sn-border:#d6e9f8;--sn-bg:#f4f9fe;}'
    '*,*::before,*::after{box-sizing:border-box}'
    "body{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;"
    'background:var(--sn-bg);color:var(--sn-ink);-webkit-font-smoothing:antialiased}'
    'a{color:var(--sn-blue-600);text-decoration:none}a:hover{text-decoration:underline}'
    '.footer{border-top:1.5px solid var(--sn-border);background:#fff}'
    '.footer-inner{max-width:1140px;margin:0 auto;padding:18px 20px;display:flex;'
    'justify-content:space-between;align-items:center;gap:12px;color:var(--sn-muted);font-size:12px}'
    '@media (max-width:700px){.footer-inner{flex-direction:column;align-items:flex-start}}'
    '@media (max-width:760px){.post-grid-regular{grid-template-columns:1fr !important}}'
)


# Nur ausgeliefert, wenn die Seite tatsaechlich einen Archiv- oder Ruecklink hat.
LISTING_LINK_CSS = (
    '.listing-link{display:inline-block;margin-top:28px;background:#fff;'
    'border:1.5px solid var(--sn-border);border-radius:12px;padding:14px 20px;'
    'font-size:14px;font-weight:700;color:var(--sn-blue-600);text-decoration:none;'
    'box-shadow:0 1px 4px rgba(6,27,73,0.05)}'
    '.listing-link:hover{border-color:var(--sn-blue-600);text-decoration:none}'
)


def render_listing_page(*, head_title: str, og_title: str, description: str, url: str,
                        jsonld: list[dict], hero_title: str, count_line: str,
                        posts: list[Post], tail: str = '') -> str:
    """Gemeinsames Geruest fuer Kategorie- und Archivseiten: identischer Kopf,
    identisches Kartenraster, nur Texte und der Link am Fuss unterscheiden sich."""
    jsonld_html = ''.join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>\n'
        for b in jsonld
    )
    extra_css = f'\n{LISTING_LINK_CSS}' if tail else ''
    blocks = [
        f'<section class="cat-hero"><h1>{hero_title}</h1><p>{escape(description)}</p></section>',
        f'<p class="cat-count">{count_line}</p>',
    ]
    if posts:
        blocks.append(render_card_grid(posts))
    if tail:
        blocks.append(tail)
    main_body = '\n'.join(blocks)
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{head_title}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/favicon.png">
<link rel="alternate" type="application/atom+xml" title="sage news" href="/feed.xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="sage news">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/sage-news_logo_3.png">
<meta name="twitter:card" content="summary_large_image">
{jsonld_html}<style>
{FONT_FACE_CSS}
{BASE_CSS}
.wrap{{max-width:1140px;margin:0 auto;padding:24px 20px 64px}}
.cat-hero{{margin-top:24px;background:linear-gradient(135deg,var(--sn-blue-950),var(--sn-blue-800));color:#fff;border-radius:16px;padding:32px}}
.cat-hero h1{{margin:0 0 10px;font-size:32px;line-height:1.2}}
.cat-hero p{{margin:0;font-size:15px;line-height:1.6;color:rgba(255,255,255,.78);max-width:60ch}}
.cat-count{{margin:24px 0 12px;font-size:13px;color:var(--sn-muted)}}
@media (max-width:700px){{.cat-hero{{padding:22px}}.cat-hero h1{{font-size:26px}}}}{extra_css}
</style>
</head>
<body>
{SITE_HEADER}
<main class="wrap">
{main_body}
</main>
{SITE_FOOTER}
</body>
</html>
'''


def collection_jsonld(name: str, description: str, url: str, posts: list[Post]) -> dict:
    return {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        'name': name,
        'description': description,
        'url': url,
        'inLanguage': 'de-DE',
        'hasPart': [
            {'@type': 'NewsArticle', 'headline': p.meta['title'],
             'datePublished': iso_date(p), 'url': f'{SITE}/{p.slug}/'}
            for p in posts
        ],
    }


def build_category_html(category: str, posts: list[Post], archived: list[Post]) -> str:
    slug = CATEGORY_SLUGS[category]
    url = f'{SITE}/kategorie/{slug}/'
    intro = CATEGORY_INTRO[category]
    name = escape(category)
    count = len(posts)
    plural = 'Beitrag' if count == 1 else 'Beiträge'
    # Ohne diesen Fall stuende auf einem eingeschlafenen Bereich "0 Beiträge",
    # obwohl das Archiv voll ist.
    count_line = f'{count} {plural}' if count else 'Alle Beiträge liegen im Archiv'
    tail = ''
    if archived:
        older = len(archived)
        tail = (f'<a class="listing-link" href="archiv/">Ältere Beiträge '
                f'({older}) →</a>')
    jsonld = [
        collection_jsonld(f'{category} – Neuigkeiten', intro, url, posts),
        {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': category, 'item': url},
            ],
        },
    ]
    return render_listing_page(
        head_title=f'{name} – Neuigkeiten und Updates | sage news',
        og_title=f'{name} – Neuigkeiten und Updates',
        description=intro,
        url=url,
        jsonld=jsonld,
        hero_title=name,
        count_line=count_line,
        posts=posts,
        tail=tail,
    )


def build_archive_html(category: str, archived: list[Post]) -> str:
    slug = CATEGORY_SLUGS[category]
    cat_url = f'{SITE}/kategorie/{slug}/'
    url = f'{cat_url}archiv/'
    name = escape(category)
    count = len(archived)
    plural = 'Beitrag' if count == 1 else 'Beiträge'
    intro = (f'Ältere {category}-Meldungen von sage news: alles, was mehr als '
             f'{ARCHIVE_AFTER_MONTHS} Monate zurückliegt.')
    jsonld = [
        collection_jsonld(f'Archiv – {category}', intro, url, archived),
        {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': category, 'item': cat_url},
                {'@type': 'ListItem', 'position': 3, 'name': 'Archiv', 'item': url},
            ],
        },
    ]
    return render_listing_page(
        head_title=f'Archiv – {name} | sage news',
        og_title=f'Archiv – {name}',
        description=intro,
        url=url,
        jsonld=jsonld,
        hero_title=f'Archiv – {name}',
        count_line=f'{count} {plural} im Archiv',
        posts=archived,
        tail=f'<a class="listing-link" href="../">← Zurück zu {name}</a>',
    )


def build_sitemap(posts: list[Post], cutoff: str) -> str:
    newest = max((iso_date(p) for p in posts), default='')
    entries = [(f'{SITE}/', newest, '1.0')]
    for category, slug in CATEGORY_SLUGS.items():
        in_cat = [p for p in posts if p.meta['category'] == category]
        if not in_cat:
            continue
        entries.append((f'{SITE}/kategorie/{slug}/', max(iso_date(p) for p in in_cat), '0.8'))
        _, archived = split_archive(in_cat, cutoff)
        if archived:
            entries.append((f'{SITE}/kategorie/{slug}/archiv/',
                            max(iso_date(p) for p in archived), '0.4'))
    entries += [(f'{SITE}/{p.slug}/', iso_date(p), '0.7') for p in posts]
    entries += [(f'{SITE}{path}', newest, '0.3') for path in STATIC_URLS]
    body = ''.join(
        f'  <url><loc>{escape(loc, quote=True)}</loc>'
        f'<lastmod>{lastmod}</lastmod><priority>{prio}</priority></url>\n'
        for loc, lastmod, prio in entries
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'{body}</urlset>\n')


def build_feed(posts: list[Post]) -> str:
    newest = max((iso_date(p) for p in posts), default='1970-01-01')
    items = ''.join(
        f'  <entry>\n'
        f'    <title>{escape(p.meta["title"])}</title>\n'
        f'    <link href="{SITE}/{p.slug}/"/>\n'
        f'    <id>{SITE}/{p.slug}/</id>\n'
        f'    <updated>{iso_date(p)}T00:00:00Z</updated>\n'
        f'    <category term="{escape(p.meta["category"], quote=True)}"/>\n'
        f'    <summary>{escape(p.meta["summary"])}</summary>\n'
        f'  </entry>\n'
        for p in posts
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de">\n'
        '  <title>sage news</title>\n'
        '  <subtitle>Neuigkeiten zu Sage 100, Sage X3 und Sage Operations</subtitle>\n'
        f'  <link href="{SITE}/"/>\n'
        f'  <link rel="self" href="{SITE}/feed.xml"/>\n'
        f'  <id>{SITE}/</id>\n'
        f'  <updated>{newest}T00:00:00Z</updated>\n'
        f'  <author><name>{AUTHOR}</name></author>\n'
        f'{items}</feed>\n'
    )


def sync_home_prerender(posts: list[Post]) -> None:
    """Schreibt das vorgerenderte Markup zwischen die SSG-Marker in #root."""
    begin, end = '<!--SSG:HOME-->', '<!--/SSG:HOME-->'
    text = INDEX_PATH.read_text(encoding='utf-8')
    if begin not in text or end not in text:
        raise ValueError('SSG-Marker fehlen in index.html')
    start = text.index(begin) + len(begin)
    stop = text.index(end)
    INDEX_PATH.write_text(
        text[:start] + build_home_prerender(posts) + text[stop:], encoding='utf-8')


def sync_index_loader() -> None:
    """Der App-Code liegt seit der Vorkompilierung in src/app.jsx, nicht mehr
    inline in index.html."""
    text = APP_SRC_PATH.read_text(encoding='utf-8')
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
    APP_SRC_PATH.write_text(text, encoding='utf-8')


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


JS_SOURCES = ['tweaks-panel.jsx', 'app.jsx']
FINGERPRINT_PATH = ROOT / 'assets' / 'js' / '.sources.sha256'


def js_fingerprint() -> str:
    """Hash der JSX-Quellen. Damit faellt auf, wenn assets/js/*.js nicht zu
    src/*.jsx passt — sonst wuerde ein veraltetes Bundle unbemerkt deployt."""
    digest = hashlib.sha256()
    for name in JS_SOURCES:
        digest.update((ROOT / 'src' / name).read_bytes())
    return digest.hexdigest()


def write_fingerprint() -> None:
    FINGERPRINT_PATH.write_text(js_fingerprint() + '\n', encoding='utf-8')
    print('JS-Fingerprint geschrieben.')


def check_fingerprint() -> None:
    if not FINGERPRINT_PATH.exists():
        raise ValueError(
            'assets/js/.sources.sha256 fehlt — bitte "npm run build:js" ausfuehren')
    if FINGERPRINT_PATH.read_text(encoding='utf-8').strip() != js_fingerprint():
        raise ValueError(
            'assets/js/*.js passt nicht zu src/*.jsx — bitte "npm run build:js" ausfuehren')


ESBUILD_VERSION = '0.24.0'
ESBUILD_ARGS = [
    'src/tweaks-panel.jsx', 'src/app.jsx',
    '--outdir=assets/js',
    '--jsx-factory=React.createElement',
    '--jsx-fragment=React.Fragment',
    '--target=es2019',
    '--minify-whitespace', '--minify-syntax',
]


def esbuild_command() -> list[str] | None:
    """Lokale Installation bevorzugen, sonst npx mit fester Version."""
    local = ROOT / 'node_modules' / '.bin' / 'esbuild'
    if local.exists():
        return [str(local)]
    if shutil.which('npx'):
        return ['npx', '--yes', f'esbuild@{ESBUILD_VERSION}']
    return None


def compile_js() -> None:
    """JSX vorkompilieren. Laeuft als Teil von build(), damit es garantiert nach
    sync_index_loader() passiert — sonst koennte das Bundle veralten."""
    if FINGERPRINT_PATH.exists() and FINGERPRINT_PATH.read_text(encoding='utf-8').strip() == js_fingerprint():
        print('JS unveraendert, kein Neubau noetig.')
        return
    command = esbuild_command()
    if command is None:
        raise ValueError(
            'src/*.jsx hat sich geaendert, aber esbuild ist nicht verfuegbar. '
            'Bitte Node installieren und "npm run build:js" ausfuehren.')
    subprocess.run(command + ESBUILD_ARGS, cwd=ROOT, check=True)
    write_fingerprint()


def cleanup_category_dirs(valid_slugs: set[str], dry_run: bool = False) -> list[str]:
    """Verwaiste Kategorieordner entfernen, z. B. nach einer Umbenennung."""
    removed: list[str] = []
    if not CATEGORY_DIR.exists():
        return removed
    for child in CATEGORY_DIR.iterdir():
        if not child.is_dir() or child.name in valid_slugs:
            continue
        removed.append(child.name)
        if not dry_run:
            shutil.rmtree(child)
    return sorted(removed)


def categories_with_posts(posts: list[Post]) -> dict[str, list[Post]]:
    grouped: dict[str, list[Post]] = {}
    for category in CATEGORY_SLUGS:
        in_cat = [p for p in posts if p.meta['category'] == category]
        if in_cat:
            grouped[category] = in_cat
    return grouped


def archive_cutoff(today: date | None = None) -> str:
    """ISO-Stichtag: alles davor gehoert ins Archiv. Gerechnet wird ab dem
    Build-Tag, nicht ab dem neuesten Beitrag — ein Bereich, in dem nichts mehr
    erscheint, soll mit der Zeit vollstaendig ins Archiv wandern."""
    today = today or date.today()
    months = today.year * 12 + (today.month - 1) - ARCHIVE_AFTER_MONTHS
    year, month = divmod(months, 12)
    month += 1
    day = min(today.day, calendar.monthrange(year, month)[1])
    return date(year, month, day).isoformat()


def split_archive(posts: list[Post], cutoff: str) -> tuple[list[Post], list[Post]]:
    """Teilt eine Kategorieliste in (aktuell, Archiv). Die Reihenfolge bleibt
    neueste-zuerst, weil load_posts() bereits sortiert liefert."""
    recent = [p for p in posts if iso_date(p) >= cutoff]
    archived = [p for p in posts if iso_date(p) < cutoff]
    return recent, archived


def check_slug_collisions(posts: list[Post]) -> None:
    """/kategorie/ darf nie mit einem Beitrags-Slug kollidieren — sonst wäre ein
    Bericht nicht mehr erreichbar."""
    slugs = {post.slug for post in posts}
    if 'kategorie' in slugs:
        raise ValueError('Beitrags-Slug "kategorie" kollidiert mit den Kategorie-URLs')


def build() -> None:
    posts = load_posts()
    validate_posts(posts)
    check_slug_collisions(posts)
    manifest = build_manifest(posts)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    sync_index_loader()
    compile_js()
    sync_home_prerender(posts)
    valid_slugs = {post.slug for post in posts}
    cleanup_generated_dirs(valid_slugs)
    for post in posts:
        target = ROOT / post.slug
        target.mkdir(exist_ok=True)
        (target / 'index.html').write_text(build_article_html(post), encoding='utf-8')

    grouped = categories_with_posts(posts)
    cleanup_category_dirs({CATEGORY_SLUGS[c] for c in grouped})
    CATEGORY_DIR.mkdir(exist_ok=True)
    cutoff = archive_cutoff()
    archives = 0
    for category, in_cat in grouped.items():
        recent, archived = split_archive(in_cat, cutoff)
        target = CATEGORY_DIR / CATEGORY_SLUGS[category]
        target.mkdir(exist_ok=True)
        (target / 'index.html').write_text(
            build_category_html(category, recent, archived), encoding='utf-8')
        archive_dir = target / 'archiv'
        if archived:
            archive_dir.mkdir(exist_ok=True)
            (archive_dir / 'index.html').write_text(
                build_archive_html(category, archived), encoding='utf-8')
            archives += 1
        elif archive_dir.exists():
            # Kann auftreten, wenn ein Beitrag geloescht oder die Schwelle
            # angehoben wird — sonst bliebe eine verwaiste Seite online.
            shutil.rmtree(archive_dir)

    SITEMAP_PATH.write_text(build_sitemap(posts, cutoff), encoding='utf-8')
    FEED_PATH.write_text(build_feed(posts), encoding='utf-8')
    print(f'Built {len(posts)} posts, {len(grouped)} category pages, '
          f'{archives} archive pages, sitemap and feed.')


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
    app_text = APP_SRC_PATH.read_text(encoding='utf-8')
    if 'api.github.com' in app_text or 'raw.githubusercontent.com' in app_text:
        raise ValueError('src/app.jsx nutzt noch den alten GitHub-Runtime-Loader')
    stale_dirs = cleanup_generated_dirs(set(expected_slugs), dry_run=True)
    if stale_dirs:
        raise ValueError('Verwaiste Artikelordner gefunden: ' + ', '.join(stale_dirs))

    check_slug_collisions(posts)
    index_text = INDEX_PATH.read_text(encoding='utf-8')
    for host in ('unpkg.com', 'cdn.jsdelivr.net', 'fonts.googleapis.com'):
        if host in index_text:
            raise ValueError(f'index.html laedt noch von {host}')
    # Das Vorrendering ist der Kern der Auffindbarkeit — leer heisst kaputt.
    prerender = index_text.split('<!--SSG:HOME-->')[1].split('<!--/SSG:HOME-->')[0]
    if f'href="/{posts[0].slug}/"' not in prerender:
        raise ValueError('Vorgerendertes Markup in index.html fehlt oder ist veraltet')

    grouped = categories_with_posts(posts)
    cutoff = archive_cutoff()
    archives = 0
    for category, in_cat in grouped.items():
        cat_dir = CATEGORY_DIR / CATEGORY_SLUGS[category]
        cat_path = cat_dir / 'index.html'
        if not cat_path.exists():
            raise ValueError(f'Fehlende Kategorieseite: {cat_path.relative_to(ROOT)}')
        cat_html = cat_path.read_text(encoding='utf-8')
        archive_path = cat_dir / 'archiv' / 'index.html'
        _, archived = split_archive(in_cat, cutoff)
        if archived:
            if not archive_path.exists():
                raise ValueError(f'Fehlende Archivseite: {archive_path.relative_to(ROOT)}')
            # Ein Beitrag darf auf der Kategorie- ODER der Archivseite stehen,
            # aber er darf nirgends verschwinden.
            cat_html += archive_path.read_text(encoding='utf-8')
            archives += 1
        elif archive_path.exists():
            raise ValueError(f'Verwaiste Archivseite: {archive_path.relative_to(ROOT)}')
        missing = [p.slug for p in in_cat if f'href="/{p.slug}/"' not in cat_html]
        if missing:
            raise ValueError(f'Kategorieseite {category} verlinkt nicht: {", ".join(missing)}')
    stale_cats = cleanup_category_dirs({CATEGORY_SLUGS[c] for c in grouped}, dry_run=True)
    if stale_cats:
        raise ValueError('Verwaiste Kategorieordner: ' + ', '.join(stale_cats))

    if not SITEMAP_PATH.exists():
        raise ValueError('sitemap.xml fehlt')
    sitemap = SITEMAP_PATH.read_text(encoding='utf-8')
    expected_urls = 1 + len(grouped) + archives + len(posts) + len(STATIC_URLS)
    found_urls = sitemap.count('<loc>')
    if found_urls != expected_urls:
        raise ValueError(f'sitemap.xml hat {found_urls} URLs, erwartet {expected_urls}')
    for post in posts:
        if f'<loc>{SITE}/{post.slug}/</loc>' not in sitemap:
            raise ValueError(f'sitemap.xml fehlt Beitrag: {post.slug}')
    if not FEED_PATH.exists():
        raise ValueError('feed.xml fehlt')
    check_fingerprint()

    print(f'Validated {len(posts)} posts, {len(grouped)} category pages, '
          f'{archives} archive pages, {found_urls} sitemap URLs.')


def main() -> None:
    parser = argparse.ArgumentParser(description='Build and validate sage-news posts.')
    parser.add_argument('command', nargs='?', default='build',
                        choices=['build', 'validate', 'fingerprint'])
    args = parser.parse_args()
    if args.command == 'build':
        build()
    elif args.command == 'fingerprint':
        write_fingerprint()
    else:
        validate()


if __name__ == '__main__':
    main()
