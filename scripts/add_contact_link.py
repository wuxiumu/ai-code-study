#!/usr/bin/env python3
"""为全站内层导航添加“联系我们”入口（若不存在则添加）。"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = re.compile(
    r'(<nav\s+aria-label=["\']全站导航["\']>.*?)((?:\s*)</nav>)',
    re.S | re.I,
)

def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    for filename in files:
        path = os.path.join(ROOT, filename)
        html = open(path, encoding="utf-8").read()
        if 'href="contact.html"' in html:
            print(f"- {filename} 已存在")
            continue
        new_html, n = PATTERN.subn(r'\1      <a href="contact.html">联系我们</a>\2', html, count=1)
        if n:
            open(path, "w", encoding="utf-8").write(new_html)
            print(f"✓ {filename}")
        else:
            print(f"? {filename} 未匹配到导航")

if __name__ == "__main__":
    main()
