#!/usr/bin/env python3
"""生成 1200×630 的 Open Graph 图片。"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "og.png")

# macOS 常见中文字体，按需修改
FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
]

def find_font(size: int):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    # 兜底
    return ImageFont.load_default()

def main():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#0E1A16")
    draw = ImageDraw.Draw(img)

    # 装饰色块
    draw.rectangle([(0, H - 8), (W, H)], fill="#59C99B")

    title_font = find_font(90)
    sub_font = find_font(36)
    small_font = find_font(24)

    title = "AI Code Study"
    subtitle = "21 门中文 AI 编程教程"
    tag = "ai-code-study.chiguashentan.com"

    # 居中绘制
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 200), title, font=title_font, fill="#DCE9E2")

    bbox2 = draw.textbbox((0, 0), subtitle, font=sub_font)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) / 2, 330), subtitle, font=sub_font, fill="#9AA8A2")

    bbox3 = draw.textbbox((0, 0), tag, font=small_font)
    rw = bbox3[2] - bbox3[0]
    draw.text(((W - rw) / 2, 460), tag, font=small_font, fill="#59C99B")

    img.save(OUT, "PNG")
    print(f"✓ 已生成 {OUT}")

if __name__ == "__main__":
    main()
