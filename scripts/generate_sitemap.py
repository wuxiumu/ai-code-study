#!/usr/bin/env python3
"""生成 sitemap.xml，排除旧版迁移页。"""
import os
from datetime import datetime, timezone

SITE_URL = "https://ai-code-study.chiguashentan.com"  # <-- 替换为真实域名
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE = {"Kimi-Code-CLI-本地上手指南.html", "404.html"}

def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html") and f not in EXCLUDE)
    urls = []
    for filename in files:
        path = os.path.join(ROOT, filename)
        mtime = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc).strftime("%Y-%m-%d")
        priority = "1.0" if filename == "index.html" else "0.8"
        urls.append(f"""  <url>
    <loc>{SITE_URL}/{filename}</loc>
    <lastmod>{mtime}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    out = os.path.join(ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"✓ 已生成 {out}，共 {len(urls)} 个 URL")

if __name__ == "__main__":
    main()
