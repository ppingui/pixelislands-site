#!/usr/bin/env python3
"""Ensure every guide article has a 'Guides' link in its header nav.

Usage: python3 add_guides_nav.py

Idempotent: files that already link the hub are left untouched. The hub is always
one level up from an article, so the href is "../" in every locale.
"""
import pathlib
import re

LABEL = {"": "Guides", "de": "Guides", "fr": "Guides", "es": "Guías",
         "ja": "ガイド", "pt-br": "Guias", "ru": "Гайды", "uk": "Гайди"}

ROOT = pathlib.Path(__file__).parent
FEATURES_LINK = re.compile(r'(<a href="\.\./\.\./#features">[^<]*</a>)')

changed, skipped = [], []
for idx in sorted(ROOT.rglob("guides/*/index.html")):
    parts = idx.relative_to(ROOT).parts
    loc = parts[0] if parts[0] != "guides" else ""
    html = idx.read_text(encoding="utf-8")
    nav = re.search(r"<nav>.*?</nav>", html, re.S)
    if not nav:
        skipped.append((idx, "no nav")); continue
    if 'href="../"' in nav.group(0):
        skipped.append((idx, "already linked")); continue
    m = FEATURES_LINK.search(nav.group(0))
    if not m:
        skipped.append((idx, "no features link")); continue
    new_nav = nav.group(0).replace(
        m.group(1), f'{m.group(1)}\n      <a href="../">{LABEL[loc]}</a>', 1)
    idx.write_text(html.replace(nav.group(0), new_nav, 1), encoding="utf-8")
    changed.append(idx)

print(f"added Guides nav link to {len(changed)} files")
for p, why in skipped:
    print(f"  skipped ({why}): {p.relative_to(ROOT)}")
