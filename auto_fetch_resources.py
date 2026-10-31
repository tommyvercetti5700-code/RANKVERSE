#!/usr/bin/env python3
"""
100% Legal Automated Study Material & One-Shot Video Fetcher
For JEE (Main & Advanced), NEET UG, CUET, and NDA Aspirants.
"""
import json
import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

OFFICIAL_CHANNELS = [
    {"name": "NCERT Official", "channel_id": "UCT0s92hGjqLX6p7qY9BBrSA", "exam": "JEE & NEET"},
    {"name": "SWAYAM IIT PAL", "channel_id": "UC3c132831e9B6a6P8C7A09w", "exam": "JEE & NEET"}
]

AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "rankverse-21")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
DATA_FILE = os.path.join(os.path.dirname(__file__), "resources_data.json")

def fetch_youtube_rss(channel_id: str, exam_label: str, max_items: int = 5):
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    discovered = []
    try:
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0 (StudyBot/1.0)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
        for entry in root.findall("atom:entry", ns)[:max_items]:
            video_id_el = entry.find("yt:videoId", ns)
            title_el = entry.find("atom:title", ns)
            published_el = entry.find("atom:published", ns)
            author_el = entry.find("atom:author/atom:name", ns)
            if video_id_el is not None and title_el is not None:
                vid = video_id_el.text
                discovered.append({
                    "id": f"yt-{vid}",
                    "title": title_el.text,
                    "channel": author_el.text if author_el is not None else "Official Channel",
                    "exam": exam_label,
                    "type": "One-Shot Video",
                    "video_id": vid,
                    "embed_url": f"https://www.youtube.com/embed/{vid}",
                    "watch_url": f"https://www.youtube.com/watch?v={vid}",
                    "published_at": published_el.text if published_el is not None else datetime.now(timezone.utc).isoformat(),
                    "legal_basis": "Official YouTube IFrame API Embed"
                })
    except Exception as exc:
        print(f"[WARN] RSS fetch skipped for {channel_id}: {exc}")
    return discovered

def main():
    videos = []
    for ch in OFFICIAL_CHANNELS:
        videos.extend(fetch_youtube_rss(ch["channel_id"], ch["exam"]))
    payload = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "affiliate_tag": AFFILIATE_TAG,
        "videos": videos
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print("Saved", len(videos), "items to", DATA_FILE)

if __name__ == "__main__":
    main()

    # Auto-update sitemap.xml for Google Search Console
    base_url = "https://tommyvercetti5700-code.github.io/RANKVERSE"
    urls = [f"  <url><loc>{base_url}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"]
    if os.path.exists(NOTES_DIR):
        for fn in sorted(os.listdir(NOTES_DIR)):
            if fn.endswith(".html"):
                urls.append(f"  <url><loc>{base_url}/{NOTES_DIR}/{fn}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    with open("sitemap.xml", "w", encoding="utf-8") as sf:
        sf.write(sitemap_content)
    print(f"[AUTO-BOT] Updated sitemap.xml with {len(urls)} URLs for Google Search Console.")

