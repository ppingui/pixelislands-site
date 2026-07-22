#!/usr/bin/env python3
"""Regenerate sitemap.xml from the actual set of pages. Run after adding pages."""
import pathlib

SITE = "https://pixelislands.app"
LASTMOD = "2026-07-22"  # bump when content changes materially
LOCALES = ["de", "fr", "es", "ja", "pt-br", "ru", "uk"]
SLUGS = ["best-walking-games-iphone", "how-to-make-walking-fun", "how-many-steps-a-day"]

entries = []  # (path, changefreq, priority)
entries.append(("/", "weekly", "1.0"))
for l in LOCALES:
    entries.append((f"/{l}/", "weekly", "0.9"))
for s in SLUGS:
    entries.append((f"/guides/{s}/", "monthly", "0.8"))
for l in LOCALES:
    for s in SLUGS:
        entries.append((f"/{l}/guides/{s}/", "monthly", "0.7"))
entries.append(("/support/", "monthly", "0.5"))
entries.append(("/privacy/", "yearly", "0.3"))

root = pathlib.Path(__file__).parent
missing = [p for p, _, _ in entries if not (root / p.lstrip("/") / "index.html").exists()]
if missing:
    raise SystemExit(f"Refusing to write sitemap; missing pages: {missing}")

urls = "\n".join(
    f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n"
    f"    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
    for p, c, pr in entries
)
xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
(root / "sitemap.xml").write_text(xml)
print(f"sitemap.xml written with {len(entries)} URLs")
