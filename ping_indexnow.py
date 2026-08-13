#!/usr/bin/env python3
"""Submit changed URLs to IndexNow (Bing, Yandex, and other participants).

Usage:
    python3 ping_indexnow.py             # submit only what changed since the last successful ping
    python3 ping_indexnow.py --all       # force a full submit of every sitemap URL
    python3 ping_indexnow.py --dry-run   # show what would be submitted, send nothing

Why diff-driven: IndexNow expects the URLs you actually changed. Resubmitting the whole
site on every deploy is noise at best, and participants may discount a source that does it.

State lives in .indexnow-state.json (gitignored — the last commit whose changes were
accepted). It is only advanced after a successful submission, so a failed ping is retried
on the next run rather than silently skipped. With no state file, it falls back to a full
submit, which is always safe.
"""
import json
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

SITE = "https://pixelislands.app"
ENDPOINT = "https://api.indexnow.org/indexnow"
ROOT = pathlib.Path(__file__).parent
STATE = ROOT / ".indexnow-state.json"
KEY_RE = re.compile(r"^[0-9a-f]{32}$")

# A page's URL only changes meaning when its own HTML changes. Styling, build scripts and
# docs touch or accompany every page without changing content, so they must not trigger a submit.
IGNORED_FILES = {"sitemap.xml", "robots.txt", "llms.txt", "styles.css", ".gitignore"}
IGNORED_PREFIXES = ("docs/", "assets/")


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def find_key() -> str:
    """The IndexNow key is the root .txt file whose name and contents match."""
    for f in ROOT.glob("*.txt"):
        if KEY_RE.match(f.stem) and f.read_text().strip() == f.stem:
            return f.stem
    sys.exit("No IndexNow key file at site root (expected <32-hex>.txt containing its own name)")


def sitemap_urls() -> set:
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return set(re.findall(r"<loc>([^<]+)</loc>", xml))


def path_to_url(rel: str):
    """'de/guides/x/index.html' -> 'https://pixelislands.app/de/guides/x/'"""
    if not rel.endswith("index.html"):
        return None
    return f"{SITE}/{rel[: -len('index.html')]}"


def changed_urls(since: str, live: set):
    """URLs whose own page changed between `since` and HEAD, plus any deleted pages."""
    out, skipped = set(), []
    raw = git("diff", "--name-status", f"{since}..HEAD")
    for line in raw.splitlines():
        parts = line.split("\t")
        status, rel = parts[0], parts[-1]
        if (rel in IGNORED_FILES or rel.endswith(".py")
                or rel.startswith(IGNORED_PREFIXES)):
            continue
        url = path_to_url(rel)
        if url is None:
            skipped.append(rel)
        elif status.startswith("D"):
            out.add(url)          # signal removal so engines recrawl and see the 404
        elif url in live:
            out.add(url)
        else:
            skipped.append(f"{rel} (not in sitemap)")
    return out, skipped


def submit(urls, key, dry) -> bool:
    if dry:
        print(f"[dry-run] would POST {len(urls)} URLs")
        return True
    payload = {"host": SITE.split("//")[1], "key": key, "urlList": sorted(urls)}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow accepted {len(urls)} URL(s) (HTTP {r.status})")
            return True
    except urllib.error.HTTPError as e:
        print(f"IndexNow rejected the submission: HTTP {e.code} {e.reason}")
    except Exception as e:                      # noqa: BLE001 — report, keep state, retry next run
        print(f"IndexNow submission failed: {e}")
    return False


def main():
    force_all = "--all" in sys.argv
    dry = "--dry-run" in sys.argv
    key, live, head = find_key(), sitemap_urls(), git("rev-parse", "HEAD")

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    since = state.get("last_commit")

    if force_all or not since:
        urls = live
        why = "forced full submit" if force_all else "no previous state — full submit"
    else:
        urls, skipped = changed_urls(since, live)
        why = f"changed since {since[:7]}"
        for s in skipped[:10]:
            print(f"  ignored: {s}")

    if not urls:
        print(f"Nothing to submit ({why}). State unchanged.")
        return

    print(f"Submitting {len(urls)} URL(s) — {why}")
    for u in sorted(urls)[:10]:
        print(f"  {u}")
    if len(urls) > 10:
        print(f"  … and {len(urls) - 10} more")

    if submit(urls, key, dry) and not dry:
        STATE.write_text(json.dumps({"last_commit": head}, indent=1) + "\n")
        print(f"State advanced to {head[:7]}")


if __name__ == "__main__":
    main()
