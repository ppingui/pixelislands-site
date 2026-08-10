#!/usr/bin/env python3
"""Regenerate sitemap.xml by walking the site directory.

Usage: python3 build_sitemap.py

Every directory containing an index.html becomes a URL, so newly added pages are
picked up automatically. Priorities are derived from path shape.
"""
import pathlib
import subprocess

SITE = "https://pixelislands.app"

# lastmod is derived per-file from git rather than hardcoded: a stale global date
# understates freshness to crawlers, and every content edit already goes through git.
_MTIME_CACHE = {}


def lastmod_for(idx: pathlib.Path) -> str:
    key = str(idx)
    if key not in _MTIME_CACHE:
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", key],
                           capture_output=True, text=True, cwd=str(ROOT))
        _MTIME_CACHE[key] = r.stdout.strip() or "2026-07-22"
    return _MTIME_CACHE[key]
LOCALES = {"de", "fr", "es", "ja", "pt-br", "ru", "uk"}
SKIP_DIRS = {".git", "assets", "node_modules"}

ROOT = pathlib.Path(__file__).parent


def classify(parts):
    """parts: URL path segments, e.g. ('de', 'guides', 'slug'). -> (changefreq, priority)"""
    loc = parts[0] in LOCALES if parts else False
    rest = parts[1:] if loc else parts

    if not rest:                                    # homepage
        return ("weekly", "0.9" if loc else "1.0")
    if rest == ("guides",):                         # guides hub
        return ("weekly", "0.7" if loc else "0.8")
    if rest[0] == "guides":                         # article
        return ("monthly", "0.7" if loc else "0.8")
    if rest == ("support",):
        return ("monthly", "0.5")
    if rest == ("privacy",):
        return ("yearly", "0.3")
    return ("monthly", "0.5")


def discover():
    urls = []
    for idx in sorted(ROOT.rglob("index.html")):
        rel = idx.relative_to(ROOT).parent
        parts = rel.parts
        if any(p in SKIP_DIRS or p.startswith(".") for p in parts):
            continue
        path = "/" + ("/".join(parts) + "/" if parts else "")
        cf, pr = classify(parts)
        urls.append((path, cf, pr, lastmod_for(idx)))
    # homepage first, then by priority desc, then alphabetically
    urls.sort(key=lambda u: (u[0] != "/", -float(u[2]), u[0]))
    return urls


if __name__ == "__main__":
    urls = discover()
    body = "\n".join(
        f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{lm}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for p, cf, pr, lm in urls
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{body}\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml written with {len(urls)} URLs")
    for p, _, pr, lm in urls:
        print(f"  {pr}  {lm}  {p}")
