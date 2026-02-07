#!/usr/bin/env python3
"""
Generate simple PNG 'screenshots' for notebooks by rendering key cells as text.
This is a lightweight alternative to a true HTML->PNG render.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

NOTEBOOKS = {
    "notebooks/quickstart.ipynb": "docs/images/quickstart.png",
    "notebooks/export_visualize.ipynb": "docs/images/export_visualize.png",
    "notebooks/llm_instructions.ipynb": "docs/images/llm_instructions.png",
}

FONT_PATH = None  # use default

def extract_snippet(nb_path):
    with open(nb_path, "r", encoding="utf-8") as fh:
        nb = json.load(fh)
    md = ""
    code = ""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown" and not md:
            md = " ".join(cell.get("source", [])).strip()
        if cell.get("cell_type") == "code" and not code:
            code = "".join(cell.get("source", [])).strip()
        if md and code:
            break
    snippet = md.splitlines()[:10]
    code_snip = code.splitlines()[:10]
    lines = []
    lines.append(" / ".join(snippet[:2]))
    lines.append("")
    lines.append("Code:")
    for l in code_snip:
        lines.append(l[:80])
    return lines

def render_image(lines, out_path, size=(1200, 600), bgcolor=(255,255,255), fg=(20,20,20)):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", size, color=bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONT_PATH or "DejaVuSansMono.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    x, y = 20, 20
    # compute line height
    try:
        ascent, descent = font.getmetrics()
        line_h = ascent + descent + 6
    except Exception:
        line_h = 20
    for line in lines:
        draw.text((x, y), line, fill=fg, font=font)
        y += line_h
        if y > size[1] - 40:
            break
    img.save(out_path, optimize=True)

def main():
    for nb, out in NOTEBOOKS.items():
        if not os.path.exists(nb):
            print("Notebook not found:", nb)
            continue
        lines = extract_snippet(nb)
        render_image(lines, out)
        print("Wrote:", out)

if __name__ == "__main__":
    main()

