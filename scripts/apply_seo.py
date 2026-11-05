#!/usr/bin/env python3
"""
AI Code Study 全站 SEO 头部批量处理脚本
功能：为每个 HTML 页面注入 canonical、Open Graph、Twitter Card、JSON-LD Schema。
注意：请先把 SITE_URL 替换为真实域名后再运行。
"""
import os
import re
from datetime import datetime, timezone

# ==================== 用户配置 ====================
SITE_URL = "https://ai-code-study.chiguashentan.com"   # <-- 替换为你的真实域名
SITE_NAME = "AI Code Study"
SITE_DESCRIPTION = "21 门中文 AI 编程教程，覆盖 AI 基础、编码 Agent、开源模型、机器学习框架与视觉自动化。"
AUTHOR_NAME = "AI Code Study"
OG_IMAGE = "assets/og.png"             # 相对于站点根目录

# 百度统计脚本（从 assets/config.js 读取 baiduId，实现独立 JS 配置）
ANALYTICS_BLOCK = """<!-- BAIDU-ANALYTICS-START -->
<script src="assets/config.js"></script>
<script>
(function(){
  var cfg = window.ACS_CONFIG || {};
  if (!cfg.baiduId) return;
  var _hmt = _hmt || [];
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?" + cfg.baiduId;
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
<!-- BAIDU-ANALYTICS-END -->"""
# =================================================

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\n", " ")).strip()

def extract_tag(html: str, tag: str, attrs: dict) -> str:
    """从 HTML 中提取第一个匹配 tag 的文本内容（忽略内嵌标签）。"""
    attr_pattern = ""
    for k, v in attrs.items():
        attr_pattern += re.escape(k) + r"=[\"']" + re.escape(v) + r"[\"']"
    pattern = re.compile(rf"<{tag}(?:[^>]*){attr_pattern}[^>]*>(.*?)</{tag}>", re.S | re.I)
    m = pattern.search(html)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()

def extract_meta(html: str, name: str) -> str:
    """提取 <meta name="..." content="..."> 的 content 值。"""
    pattern = re.compile(
        rf"<meta\s+[^>]*(?:name|property)=[\"']{re.escape(name)}[\"'][^>]*content=[\"']([^\"']*)[\"']",
        re.I | re.S,
    )
    m = pattern.search(html)
    if m:
        return m.group(1).strip()
    # 属性顺序可能相反
    pattern2 = re.compile(
        rf"<meta\s+[^>]*content=[\"']([^\"']*)[\"'][^>]*(?:name|property)=[\"']{re.escape(name)}[\"']",
        re.I | re.S,
    )
    m2 = pattern2.search(html)
    return m2.group(1).strip() if m2 else ""

def extract_h1_text(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if not m:
        return ""
    return clean_text(re.sub(r"<[^>]+>", "", m.group(1)))

def file_mtime_iso(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")

def build_seo_block(filename: str, title: str, description: str, page_type: str, h1: str, mtime: str) -> str:
    canonical = f"{SITE_URL}/{filename}"
    og_image_url = f"{SITE_URL}/{OG_IMAGE}"
    safe_title = title.replace("\"", "&quot;")
    safe_desc = description.replace("\"", "&quot;")

    og_type = "website" if page_type == "website" else "article"

    # Open Graph & Twitter
    social = f"""<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{safe_title}">
<meta property="og:description" content="{safe_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image_url}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{safe_title}">
<meta name="twitter:description" content="{safe_desc}">
<meta name="twitter:image" content="{og_image_url}">"""

    # Canonical
    canonical_tag = f'<link rel="canonical" href="{canonical}">'

    # JSON-LD Schema
    if page_type == "website":
        schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{SITE_NAME}",
  "url": "{SITE_URL}/",
  "description": "{safe_desc}",
  "potentialAction": {{
    "@type": "SearchAction",
    "target": "{SITE_URL}/?q={{search_term_string}}",
    "query-input": "required name=search_term_string"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{SITE_NAME}",
  "url": "{SITE_URL}/"
}}
</script>"""
    else:
        headline = h1 or title
        schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{headline.replace('"', '\\"')}",
  "description": "{safe_desc}",
  "author": {{"@type": "Organization", "name": "{AUTHOR_NAME}"}},
  "dateModified": "{mtime}",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "{canonical}"}}
}}
</script>"""

    return f"""<!-- SEO-HEAD-START -->
{canonical_tag}
{social}
{schema}
<!-- SEO-HEAD-END -->"""

def process_file(path: str) -> str:
    filename = os.path.basename(path)
    html = open(path, encoding="utf-8").read()

    title = extract_tag(html, "title", {})
    description = extract_meta(html, "description")

    # 旧版 Kimi 页面：指向新页面的 canonical，不输出额外 OG/Schema
    if filename == "Kimi-Code-CLI-本地上手指南.html":
        new_canonical = f"{SITE_URL}/kimi-code.html"
        block = f"""<!-- SEO-HEAD-START -->
<link rel="canonical" href="kimi-code.html">
<meta name="robots" content="noindex, follow">
<!-- SEO-HEAD-END -->"""
        # 如果没 description，补一个
        if not description:
            desc_tag = '<meta name="description" content="本页已迁移至 Kimi Code CLI 教程，请点击跳转查看最新内容。">'
            html = re.sub(r"(<meta[^>]*description[^>]*>)", desc_tag, html, count=1, flags=re.I)
        html = replace_or_insert(html, block)
        return apply_analytics(html)

    if not title:
        title = SITE_NAME
    if not description:
        description = SITE_DESCRIPTION

    page_type = "website" if filename == "index.html" else "article"
    h1 = extract_h1_text(html)
    mtime = file_mtime_iso(path)

    block = build_seo_block(filename, title, description, page_type, h1, mtime)
    html = replace_or_insert(html, block)
    return apply_analytics(html)

def replace_or_insert(html: str, block: str) -> str:
    # 如果已有 SEO-HEAD 标记，替换；否则插入到 description meta 之后
    if "<!-- SEO-HEAD-START -->" in html:
        html = re.sub(
            r"<!-- SEO-HEAD-START -->.*?<!-- SEO-HEAD-END -->",
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        # 尝试插在 description meta 后面
        pattern = re.compile(r"(<meta\s+[^>]*name=[\"']description[\"'][^>]*>)", re.I | re.S)
        m = pattern.search(html)
        if m:
            insert_pos = m.end()
            html = html[:insert_pos] + "\n" + block + html[insert_pos:]
        else:
            # 没有 description，插在 </title> 后面
            html = re.sub(r"(</title>)", r"\1\n" + block, html, count=1, flags=re.I)
    return html

def apply_analytics(html: str) -> str:
    """在百度统计标记存在时替换，否则插入到 </head> 前。"""
    if "<!-- BAIDU-ANALYTICS-START -->" in html:
        html = re.sub(
            r"<!-- BAIDU-ANALYTICS-START -->.*?<!-- BAIDU-ANALYTICS-END -->",
            ANALYTICS_BLOCK,
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = re.sub(r"(</head>)", r"\n" + ANALYTICS_BLOCK + r"\n\1", html, count=1, flags=re.I)
    return html

def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    for filename in files:
        path = os.path.join(ROOT, filename)
        new_html = process_file(path)
        open(path, "w", encoding="utf-8").write(new_html)
        print(f"✓ {filename}")
    print(f"\n完成。请将 SITE_URL 替换为真实域名后重新运行，并生成 sitemap。")

if __name__ == "__main__":
    main()
