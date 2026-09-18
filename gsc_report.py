#!/usr/bin/env python3
"""Pull Search Console data for pixelislands.app and surface actionable buckets.

Usage:
    python3 gsc_report.py                      # last 28 days, quick-wins report
    python3 gsc_report.py --days 90
    python3 gsc_report.py --raw queries        # dump top queries as TSV
    python3 gsc_report.py --raw pages
    python3 gsc_report.py --key /path/to/sa.json

Auth: a Google Cloud service-account JSON key whose client_email has been added as a
user on the Search Console property. Default location is ~/.gsc-service-account.json
(deliberately OUTSIDE this repo — never commit the key).

No third-party HTTP/Google libraries: signs the JWT with `cryptography` (already present)
and talks to the REST API over urllib.
"""
import argparse
import base64
import datetime as dt
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

SITE = "sc-domain:pixelislands.app"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
DEFAULT_KEY = pathlib.Path.home() / ".gsc-service-account.json"


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def access_token(key_path: pathlib.Path) -> str:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    sa = json.loads(key_path.read_text())
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    claims = {"iss": sa["client_email"], "scope": SCOPE, "aud": TOKEN_URL,
              "iat": now, "exp": now + 3600}
    signing_input = f"{_b64(json.dumps(header).encode())}.{_b64(json.dumps(claims).encode())}".encode()
    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    sig = key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    assertion = f"{signing_input.decode()}.{_b64(sig)}"

    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": assertion}).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=30) as r:
        return json.load(r)["access_token"]


def query(token, start, end, dimensions, row_limit=1000, dimension_filters=None):
    payload = {"startDate": start, "endDate": end, "dimensions": dimensions,
               "rowLimit": row_limit, "dataState": "final"}
    if dimension_filters:
        payload["dimensionFilterGroups"] = [{"filters": dimension_filters}]
    req = urllib.request.Request(
        API.format(site=urllib.parse.quote(SITE, safe="")),
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r).get("rows", [])


def fmt(rows, dims):
    out = []
    for r in rows:
        d = dict(zip(dims, r["keys"]))
        d.update(clicks=r["clicks"], impressions=r["impressions"],
                 ctr=r["ctr"] * 100, position=r["position"])
        out.append(d)
    return out


def quick_wins(token, start, end):
    """The four buckets that actually suggest an action."""
    q = fmt(query(token, start, end, ["query"]), ["query"])
    qp = fmt(query(token, start, end, ["query", "page"]), ["query", "page"])

    striking = [r for r in q if 5 <= r["position"] <= 15 and r["impressions"] >= 20]
    low_ctr = [r for r in q if r["impressions"] >= 50 and r["ctr"] < 3]
    page2 = [r for r in q if 11 <= r["position"] <= 20 and r["impressions"] >= 10]

    by_query = defaultdict(set)
    for r in qp:
        by_query[r["query"]].add(r["page"])
    cannibal = {k: v for k, v in by_query.items() if len(v) > 1}

    def table(title, rows, note):
        print(f"\n{title}  ({len(rows)})")
        print(f"  {note}")
        if not rows:
            print("    — nothing yet")
            return
        rows = sorted(rows, key=lambda r: -r["impressions"])[:15]
        print(f"    {'query':<44} {'pos':>6} {'impr':>7} {'clicks':>7} {'ctr':>7}")
        for r in rows:
            print(f"    {r['query'][:44]:<44} {r['position']:>6.1f} "
                  f"{r['impressions']:>7.0f} {r['clicks']:>7.0f} {r['ctr']:>6.1f}%")

    tot_i = sum(r["impressions"] for r in q)
    tot_c = sum(r["clicks"] for r in q)
    print(f"=== pixelislands.app — Search Console {start} → {end} ===")
    print(f"  {len(q)} queries | {tot_i:.0f} impressions | {tot_c:.0f} clicks "
          f"| {100*tot_c/tot_i if tot_i else 0:.1f}% CTR")

    table("A. STRIKING DISTANCE", striking,
          "pos 5-15 with real impressions — small on-page edits can move these to page 1 top")
    table("B. LOW CTR", low_ctr,
          "ranking but not clicked — rewrite <title> and meta description")
    table("C. PAGE TWO", page2,
          "pos 11-20 — expand the content or add internal links")

    print(f"\nD. CANNIBALIZATION  ({len(cannibal)})")
    print("  one query, multiple of our pages competing")
    if not cannibal:
        print("    — none")
    else:
        for kq, pages in sorted(cannibal.items(), key=lambda x: -len(x[1]))[:10]:
            print(f"    {kq[:50]}")
            for p in sorted(pages):
                print(f"        {p.replace('https://pixelislands.app','')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--key", type=pathlib.Path, default=DEFAULT_KEY)
    ap.add_argument("--raw", choices=["queries", "pages", "countries"])
    a = ap.parse_args()

    if not a.key.exists():
        sys.exit(f"No service-account key at {a.key}\n"
                 f"Create one in Google Cloud, enable the Search Console API, then add its\n"
                 f"client_email as a user on the {SITE} property in Search Console.")

    # GSC finalizes data with ~2-3 days lag; ending today would show a misleading dip.
    end = dt.date.today() - dt.timedelta(days=3)
    start = end - dt.timedelta(days=a.days)
    token = access_token(a.key)

    if a.raw:
        dims = {"queries": ["query"], "pages": ["page"], "countries": ["country"]}[a.raw]
        rows = fmt(query(token, str(start), str(end), dims), dims)
        rows.sort(key=lambda r: -r["impressions"])
        print("\t".join(dims + ["clicks", "impressions", "ctr", "position"]))
        for r in rows:
            print("\t".join([str(r[d]) for d in dims] +
                            [f"{r['clicks']:.0f}", f"{r['impressions']:.0f}",
                             f"{r['ctr']:.2f}", f"{r['position']:.1f}"]))
    else:
        quick_wins(token, str(start), str(end))


if __name__ == "__main__":
    main()
