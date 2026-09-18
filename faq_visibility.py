#!/usr/bin/env python3
"""Keep FAQPage schema and visible page text in sync across every guide.

Google requires FAQ rich-result content to be visible to the user on the page.
Schema whose questions and answers appear nowhere in the rendered text is a
structured-data policy violation, so this script is both the fixer and the guard.

    python3 faq_visibility.py            # check every guide, exit 1 on a mismatch
    python3 faq_visibility.py --fix      # append the missing visible sections
    python3 faq_visibility.py --fix --dry-run

The schema is the source of truth: --fix renders the existing Q&A into a
"Common questions" section before </main>, escaping only &, < and > so the
rendered text is character-identical to the JSON. It never edits the schema and
never touches a page whose Q&As are already visible.
"""
import argparse
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent

# Heading used by the guides that already render their FAQ, per locale.
HEADING = {
    "en": "Common questions",
    "de": "Häufige Fragen",
    "fr": "Questions fréquentes",
    "es": "Preguntas frecuentes",
    "ja": "よくある質問",
    "pt-br": "Perguntas frequentes",
    "ru": "Частые вопросы",
    "uk": "Часті запитання",
}


def locale_of(path: pathlib.Path) -> str:
    """Locale from the path: guides/<slug>/ is English, <loc>/guides/<slug>/ is not."""
    rel = path.relative_to(ROOT).parts
    return "en" if rel[0] == "guides" else rel[0]


def visible_text(page: str) -> str:
    """Approximate what a reader (and a crawler) sees inside <main>."""
    m = re.search(r"<main.*?</main>", page, re.S)
    body = m.group(0) if m else page
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()


def faq_entries(page: str):
    """The Q&A pairs from the page's FAQPage block, or None if it has none."""
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        if '"FAQPage"' not in block:
            continue
        data = json.loads(block)
        return [(e["name"], e["acceptedAnswer"]["text"]) for e in data["mainEntity"]]
    return None


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def missing(entries, seen: str):
    """Q&A pairs whose text is not present in the visible page text."""
    return [(q, a) for q, a in entries if norm(q) not in seen or norm(a) not in seen]


def esc(text: str) -> str:
    """Escape only what HTML requires, so the rendered text matches the JSON exactly."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def section(entries, locale: str) -> str:
    lines = [f"\n  <h2>{esc(HEADING[locale])}</h2>"]
    for q, a in entries:
        lines.append(f"  <h3>{esc(q)}</h3>")
        lines.append(f"  <p>{esc(a)}</p>")
    return "\n".join(lines) + "\n"


def guides():
    return sorted(ROOT.glob("*/guides/*/index.html")) + sorted(ROOT.glob("guides/*/index.html"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="append the missing visible sections")
    ap.add_argument("--dry-run", action="store_true", help="with --fix, report without writing")
    args = ap.parse_args()

    broken, fixed, skipped = [], [], []

    for path in guides():
        page = path.read_text(encoding="utf-8")
        entries = faq_entries(page)
        if not entries:
            continue
        gaps = missing(entries, visible_text(page))
        if not gaps:
            continue

        rel = path.relative_to(ROOT).parent
        broken.append((rel, len(gaps), len(entries)))

        if not args.fix:
            continue

        # Only append when the whole block is absent. A partial mismatch means the
        # page has its own wording that drifted, and appending would duplicate text.
        if len(gaps) != len(entries):
            skipped.append(rel)
            continue

        locale = locale_of(path)
        if locale not in HEADING:
            skipped.append(rel)
            continue

        updated = page.replace("</main>", section(entries, locale) + "</main>", 1)
        if updated == page:
            skipped.append(rel)
            continue

        if not args.dry_run:
            path.write_text(updated, encoding="utf-8")
            # Re-read and re-check rather than trusting the write.
            if missing(entries, visible_text(path.read_text(encoding="utf-8"))):
                print(f"  !! still mismatched after fix: {rel}", file=sys.stderr)
                return 2
        fixed.append(rel)

    if not broken:
        print("All guides: FAQ schema text is visible on the page.")
        return 0

    if args.fix:
        verb = "would fix" if args.dry_run else "fixed"
        print(f"{verb} {len(fixed)} page(s):")
        for rel in fixed:
            print(f"  + {rel}")
        if skipped:
            print(f"\nskipped {len(skipped)} page(s) needing manual review:")
            for rel in skipped:
                print(f"  ? {rel}")
        return 1 if skipped else 0

    print(f"{len(broken)} page(s) have FAQ schema text that is not visible:")
    for rel, gaps, total in broken:
        print(f"  x {rel}  ({gaps}/{total} Q&A missing)")
    print("\nRun: python3 faq_visibility.py --fix")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
