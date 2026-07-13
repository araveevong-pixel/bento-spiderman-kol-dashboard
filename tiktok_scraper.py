#!/usr/bin/env python3
"""BENTO x SPIDER-MAN — TikTok scraper (yt-dlp). Facebook = manual (manual_stats.json)."""
import json, subprocess, sys, time, random

MANUAL_OVERRIDE = {}   # ใส่ยอดเองได้ถ้า scrape ไม่ผ่าน: {"handle": {"views":0,"likes":0,...}}

def load_links():
    meta = json.load(open('kol_meta.json', encoding='utf-8'))['kols']
    return {u: m['link'] for u, m in meta.items()
            if m.get('link') and m.get('platform') == 'TikTok'}

def scrape(url, timeout=60):
    try:
        r = subprocess.run(['yt-dlp','--dump-json','--no-download','--no-warnings',url],
                           capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            r = subprocess.run(['yt-dlp','--dump-json','--no-download','--no-warnings',
                                '--age-limit','99',url], capture_output=True, text=True, timeout=timeout)
            if r.returncode != 0:
                print(f"    yt-dlp error: {r.stderr.strip()[:160]}"); return None
        i = json.loads(r.stdout)
        return {'url': i.get('webpage_url', url),
                'views': i.get('view_count') or 0, 'likes': i.get('like_count') or 0,
                'shares': i.get('repost_count') or 0, 'comments': i.get('comment_count') or 0,
                'saves': i.get('save_count') or i.get('collect_count') or i.get('favorite_count') or 0,
                'followers': i.get('channel_follower_count') or 0}
    except Exception as e:
        print(f"    error: {e}"); return None

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'scrape_results.json'
    links = load_links()
    res = {}
    print(f"Scraping {len(links)} TikTok post(s)...")
    for u, link in links.items():
        if u in MANUAL_OVERRIDE:
            res[u] = dict(MANUAL_OVERRIDE[u], url=link); print(f"  @{u} — manual"); continue
        print(f"  @{u} ...")
        d = scrape(link)
        if d:
            res[u] = d
            print(f"    views {d['views']:,} · likes {d['likes']:,} · cmt {d['comments']:,}")
        time.sleep(random.uniform(0.5, 1.5))
    json.dump(res, open(out,'w'), indent=2, ensure_ascii=False)
    print(f"Saved {len(res)}/{len(links)} -> {out}")

if __name__ == '__main__':
    main()
