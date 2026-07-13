#!/usr/bin/env python3
"""Inject scraped stats + manual stats into index.html (KOL_DATA / MANUAL_STATS)."""
import json, re, sys

def esc(s): return str(s or '').replace('\\','\\\\').replace("'","\\'")

def main():
    scrape_file = sys.argv[1] if len(sys.argv) > 1 else 'scrape_results.json'
    html_file   = sys.argv[2] if len(sys.argv) > 2 else 'index.html'

    meta = json.load(open('kol_meta.json', encoding='utf-8'))['kols']
    try:    scraped = json.load(open(scrape_file, encoding='utf-8'))
    except Exception: scraped = {}
    try:    manual = json.load(open('manual_stats.json', encoding='utf-8'))
    except Exception: manual = {"reach_by_group": {}, "fb_posts": {}}

    html = open(html_file, encoding='utf-8').read()

    # preserve actual use
    m = re.search(r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*([\d.]+)', html)
    actual_use = m.group(1) if m else '0'

    # preserve existing stats when a scrape fails
    prev = {}
    for e in re.finditer(r"\{ username: '([^']+)'[^}]*?views: (\d+), likes: (\d+), shares: (\d+), comments: (\d+), saves: (\d+)", html):
        prev[e.group(1)] = dict(views=int(e.group(2)), likes=int(e.group(3)),
                                shares=int(e.group(4)), comments=int(e.group(5)), saves=int(e.group(6)))

    entries = []
    for u, mm in meta.items():
        s = scraped.get(u) or prev.get(u) or {}
        views = s.get('views', 0); likes = s.get('likes', 0)
        shares = s.get('shares', 0); comments = s.get('comments', 0); saves = s.get('saves', 0)
        link = mm.get('link', '')
        posted = bool(link) or views > 0
        followers = (scraped.get(u, {}) or {}).get('followers') or mm.get('followers', 0)
        entries.append(
            f"  {{ username: '{esc(u)}', displayName: '{esc(mm['displayName'])}', "
            f"tier: '{esc(mm['tier'])}', platform: '{esc(mm['platform'])}', "
            f"category: '{esc(mm['category'])}', angle: '{esc(mm['angle'])}', gender: '-', "
            f"followers: {followers}, views: {views}, likes: {likes}, shares: {shares}, "
            f"comments: {comments}, saves: {saves}, posts: {1 if posted else 0}, "
            f"kpi_views: {views}, posted: {'true' if posted else 'false'}, "
            f"link: '{esc(link)}', budget: {mm.get('budget',0)} }}")

    html = re.sub(r'const KOL_DATA = \[[\s\S]*?\];',
                  'const KOL_DATA = [\n' + ',\n'.join(entries) + '\n];', html, count=1)
    html = re.sub(r'const\s+MANUAL_STATS\s*=\s*\{[\s\S]*?\};',
                  'const MANUAL_STATS = ' + json.dumps(manual, ensure_ascii=False) + ';', html, count=1)
    html = re.sub(r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*[\d.]+',
                  f'const CAMPAIGN_ACTUAL_USE_DEFAULT = {actual_use}', html)

    open(html_file, 'w', encoding='utf-8').write(html)
    print(f"Updated {html_file}: {len(entries)} KOLs · scraped {len(scraped)}")

if __name__ == '__main__':
    main()
