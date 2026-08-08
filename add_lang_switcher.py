#!/usr/bin/env python3
"""Add a visible language switcher to guide articles and guide hubs.

Usage: python3 add_lang_switcher.py

hreflang tells Google which translations exist, but it is a weak crawl signal on
its own. Real <a> links give every localized page inbound links from the site's
strongest pages, which is what "Discovered - currently not indexed" needs.

The link set is derived from each page's own hreflang block, so this can never
point at a translation that doesn't exist. Idempotent.
"""
import pathlib
import re

NAME = {"en": "English", "de": "Deutsch", "fr": "Français", "es": "Español",
        "ja": "日本語", "pt-BR": "Português", "ru": "Русский", "uk": "Українська"}
ORDER = ["en", "de", "fr", "es", "ja", "pt-BR", "ru", "uk"]
SITE = "https://pixelislands.app"

ROOT = pathlib.Path(__file__).parent
HREFLANG = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">')


def relative(from_path, to_path):
    """Both are absolute site paths like '/de/guides/slug/'. Return a relative href."""
    depth = len([s for s in from_path.split("/") if s])
    return "../" * depth + to_path.lstrip("/")


changed, skipped = [], []
targets = sorted(ROOT.rglob("guides/**/index.html")) + sorted(ROOT.rglob("guides/index.html"))
for idx in sorted(set(targets)):
    html = idx.read_text(encoding="utf-8")
    if 'class="wrap lang-row"' in html:
        skipped.append((idx, "already has switcher")); continue

    alts = [(l, u) for l, u in HREFLANG.findall(html) if l != "x-default"]
    if len(alts) < 2:
        skipped.append((idx, "no hreflang set")); continue

    cur = "/" + str(idx.parent.relative_to(ROOT)) + "/"
    by_lang = {l: u.replace(SITE, "") for l, u in alts}
    # which locale is this page? the alternate whose URL equals our own path
    self_lang = next((l for l, p in by_lang.items() if p == cur), None)
    if self_lang is None:
        skipped.append((idx, f"self not in hreflang ({cur})")); continue

    parts = []
    for lang in ORDER:
        if lang not in by_lang:
            continue
        if lang == self_lang:
            parts.append(f'<strong style="color:#fff">{NAME[lang]}</strong>')
        else:
            parts.append(f'<a href="{relative(cur, by_lang[lang])}">{NAME[lang]}</a>')
    row = '    <div class="wrap lang-row">' + " · ".join(parts) + "</div>\n"

    if "</footer>" not in html:
        skipped.append((idx, "no footer")); continue
    html = html.replace("</footer>", row + "</footer>", 1)
    idx.write_text(html, encoding="utf-8")
    changed.append(idx)

print(f"added language switcher to {len(changed)} pages")
for p, why in skipped:
    print(f"  skipped ({why}): {p.relative_to(ROOT)}")
