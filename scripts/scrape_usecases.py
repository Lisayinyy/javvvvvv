"""Scrape madewithjev.com use-case categories; extract X-sourced builds."""
import re, html, json, sys, concurrent.futures as cf, urllib.request, time
UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://madewithjev.com"
CATS = {"agents-and-browsers": "agents-browsers", "games-and-real-time": "games-realtime", "triage-and-routing": "triage-routing",
        "trading-and-markets": "trading-markets", "content-and-growth": "content-growth", "research-and-data": "research-data",
        "robotics-and-devices": "robotics-devices", "tools-and-apps": "tools-apps"}
def get(u, tries=3):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode("utf-8", "ignore")
        except Exception as e:
            time.sleep(2 * (i + 1))
    return ""
def strip(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
def parse_build(slug, cat):
    t = get(f"{BASE}/builds/{slug}")
    if not t: return None
    links = list(re.finditer(r'href="(https://x\.com/([A-Za-z0-9_]+)/status/(\d+))"', t))
    x = links[0] if links else None
    cut = links[1].start() if len(links) > 1 else len(t)
    head = t[:cut]
    gh = re.search(r'href="(https://github\.com/[^"?#]+)"', t)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', t)
    author = re.search(r'"author":\{"@type":"Person","name":"([^"]+)"', t)
    date = re.search(r'"datePublished":"([^"]+)"', t)
    likes = re.search(r"([\d.,]+[KM]?)<!-- --> likes", t)
    views = re.search(r"([\d.,]+[KM]?)<!-- --> views", t)
    media = re.search(r'<img src="(https://pbs\.twimg\.com/(?:amplify_video_thumb|media|ext_tw_video_thumb)/[^"]+)"', head)
    card = re.search(r'@<!-- -->[A-Za-z0-9_]+</p>.*?</div>\s*(?:<svg.*?</svg>)?\s*</div>\s*<p[^>]*>(.*?)</p>', head, re.S)
    body = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
    para = re.findall(r"<p[^>]*>(.*?)</p>", body.group(1) if body else t, re.S)
    tags = re.findall(r'href="/tags/([^"]+)"', t)
    metrics = [(k, v) for k, v in re.findall(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>', head, re.S) if strip(k) not in ("Author", "Use case", "Added")]
    return {"slug": slug, "category": cat, "title": strip(h1.group(1)) if h1 else slug, "summary": strip(desc.group(1)) if desc else "",
            "author": author.group(1) if author else None, "date": date.group(1) if date else "",
            "x": x.group(1) if x else None, "handle": x.group(2) if x else None, "tweet_id": x.group(3) if x else None,
            "github": gh.group(1) if gh else None, "likes": likes.group(1) if likes else None, "views": views.group(1) if views else None,
            "media": html.unescape(media.group(1)) if media else None, "post": strip(card.group(1)) if card else "",
            "tags": sorted(set(tags))[:8], "metrics": {strip(k): strip(v) for k, v in metrics[:6]}}
def main():
    slugs = {}
    for c, ours in CATS.items():
        t = get(f"{BASE}/categories/{c}")
        for s in sorted(set(re.findall(r'href="/builds/([^"]+)"', t))): slugs.setdefault(s, ours)
    print("builds:", len(slugs), file=sys.stderr)
    with cf.ThreadPoolExecutor(8) as ex:
        res = [r for r in ex.map(lambda kv: parse_build(*kv), slugs.items()) if r]
    json.dump(res, open("mwj_builds.json", "w"), ensure_ascii=False, indent=1)
    xs = [r for r in res if r["x"]]
    print("parsed", len(res), "with X", len(xs), "with likes", sum(1 for r in xs if r["likes"]), "with views", sum(1 for r in xs if r["views"]), file=sys.stderr)
main()
