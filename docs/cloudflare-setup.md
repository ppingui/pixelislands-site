# Putting Cloudflare in front of pixelislands.app

**Why:** GitHub Pages serves every asset with `Cache-Control: max-age=600` and gives you no way
to change it, and it gives you no server logs at all. Cloudflare fixes both — you control cache
headers (fonts and images cached for a year instead of 10 minutes) and you get request-level
visibility including AI crawlers like `GPTBot` and `ChatGPT-User`, which is currently unmeasurable.

**Cost:** free plan is enough for everything here.
**Risk level:** this is a nameserver change — the highest-risk operation performed on this domain
so far. It is fully reversible, but not instantly. Read "Rollback" before starting.
**Time:** ~20 minutes, plus up to a few hours of nameserver propagation.

---

## Pre-flight: the exact records that must survive

Captured 2026-08-10. Cloudflare will scan and import these automatically, but **verify every
line against this list before switching nameservers.** A missed record is the only real failure mode.

| Type | Name | Value | Purpose | Proxy |
|---|---|---|---|---|
| A | `@` | `185.199.108.153` | GitHub Pages | Proxied |
| A | `@` | `185.199.109.153` | GitHub Pages | Proxied |
| A | `@` | `185.199.110.153` | GitHub Pages | Proxied |
| A | `@` | `185.199.111.153` | GitHub Pages | Proxied |
| CNAME | `www` | `ppingui.github.io` | www → apex redirect | Proxied |
| TXT | `@` | `google-site-verification=PcFRQbmx34juEEOhvNI15pBI4ogfTgBwVpAiVUHOYt4` | Search Console | n/a |
| TXT | `@` | `yandex-verification: 1fca23d62d3a0f51` | Yandex Webmaster | n/a |

Also present at the site root and unrelated to DNS (do not delete):
`6a36bd11c03ac2c8e661b4d3a00a841e.txt` — the IndexNow key.

**Not configured, and correctly so:** no MX records (no email on this domain), no AAAA, no CAA.
The absence of MX is what makes this migration low-risk — the usual disaster in a nameserver
move is silently breaking email, and there is no email to break.

**Losing either TXT record costs you Search Console and Yandex verification.** Both would need
re-verifying from scratch. Check them twice.

---

## Steps

### 1. Create the Cloudflare account and add the site
Sign up at [dash.cloudflare.com](https://dash.cloudflare.com), choose **Add a site**, enter
`pixelislands.app`, and select the **Free** plan.

### 2. Verify the imported records
Cloudflare scans your existing DNS and shows what it found. Compare against the table above.
Add anything missing by hand. Set the four A records and the `www` CNAME to **Proxied**
(orange cloud) — grey cloud means DNS-only and you get none of the benefits.

### 3. Set SSL/TLS mode BEFORE switching nameservers
**SSL/TLS → Overview → Full (strict).**

This matters more than anything else on this page. GitHub Pages force-redirects HTTP to HTTPS.
If Cloudflare is set to **Flexible**, it talks to GitHub over HTTP, GitHub redirects to HTTPS,
Cloudflare follows it back to itself — **infinite redirect loop, site down.** Full (strict) is
correct because GitHub already serves a valid Let's Encrypt certificate for this domain
(issuer `Let's Encrypt CN=YR2`, currently valid to 2026-10-20).

### 4. Change nameservers at Porkbun
Cloudflare assigns you two nameservers. In
[Porkbun → Domain Management → pixelislands.app → Authoritative Nameservers](https://porkbun.com/account/domainsSpeedy),
replace the four current ones:

```
curitiba.ns.porkbun.com
fortaleza.ns.porkbun.com
maceio.ns.porkbun.com
salvador.ns.porkbun.com
```

with the two Cloudflare gives you. Propagation is usually minutes, occasionally hours.
The site keeps serving from Porkbun's DNS until it flips, so there is no gap.

### 5. Cache rules — the actual point of this exercise
**Caching → Cache Rules → Create rule.**

Rule name: `Long-cache static assets`
- **If** — `URI Path` `starts with` `/assets/`
- **Then** — Cache eligibility: *Eligible for cache*; Edge TTL: *Override origin*, **1 year**;
  Browser TTL: *Override origin*, **1 year**

Safe because every filename in `/assets/` is content-stable — changing an image means writing a
new file, not mutating one. Do **not** apply this to HTML: pages must stay short-cached so
content edits go live immediately. The default (honour origin's 10 minutes) is right for HTML.

### 6. Confirm it worked
```bash
curl -sI https://pixelislands.app/assets/hero.webp | grep -iE 'cache-control|cf-cache-status|server'
```
Expect `cache-control: max-age=31536000` and a `cf-cache-status` header. Before the change it
reads `max-age=600` with no Cloudflare headers.

### 7. AI crawler visibility
Once traffic flows through Cloudflare, the dashboard's **Analytics** and bot/AI-crawler sections
show requests by user agent — this is where `GPTBot`, `OAI-SearchBot`, `ClaudeBot`,
`PerplexityBot` and `ChatGPT-User` become countable. Cloudflare's UI for this has moved around
between releases, so look under Analytics and under Security rather than trusting a fixed menu path.

**Leave AI crawlers allowed.** Cloudflare offers one-click blocking of AI bots; blocking them is
the exact opposite of the GEO strategy this site is built around. `robots.txt` already welcomes
them explicitly.

---

## Known interaction: GitHub's certificate renewal

GitHub renews the Pages certificate via an HTTP challenge on your domain. With Cloudflare
proxying, that challenge can be intercepted, so renewal may fail.

- Current certificate expires **2026-10-20**, so this first becomes relevant in October.
- If GitHub's cert lapses while you are on **Full (strict)**, the origin connection fails and the
  site goes down.
- **Mitigation:** around renewal time, check GitHub Pages settings still shows the certificate as
  valid. If renewal fails, temporarily set the four A records and `www` to **DNS-only** (grey
  cloud), let GitHub renew, then re-enable proxying.
- **Lower-risk alternative:** run **Full** instead of Full (strict). It still encrypts to the
  origin but tolerates a lapsed/invalid origin certificate, so a failed renewal degrades quietly
  instead of taking the site down.

---

## Rollback

If anything breaks, revert the nameservers at Porkbun to the four `*.ns.porkbun.com` entries
above and re-add the records from the pre-flight table. The GitHub Pages configuration itself is
untouched by any of this — the repo still holds `CNAME` containing `pixelislands.app`, and
`https_enforced` is already true — so the site returns to exactly its current state once DNS
propagates back.

For a fast partial rollback without touching nameservers, switch the proxied records to
**DNS-only** (grey cloud). That takes Cloudflare out of the request path in seconds while
leaving DNS hosted there.
