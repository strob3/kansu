"""
kanji terminal glyph renderer
converts kanji characters into multi-line terminal ASCII/unicode block art.
"""

from functools import lru_cache
import os
from pathlib import Path
from typing import Optional

FONT_CANDIDATES = [
    os.environ.get("KANJI_FONT_PATH", ""),
    "/usr/share/fonts/google-droid-sans-fonts/DroidSansJapanese.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansJapanese.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "C:\\Windows\\Fonts\\msgothic.ttc",
    "C:\\Windows\\Fonts\\meiryo.ttc",
]

_CACHED_FONT_PATH: Optional[str] = None


def find_cjk_font() -> Optional[str]:
    """Finds an available CJK / Japanese TrueType font on the system."""
    global _CACHED_FONT_PATH
    if _CACHED_FONT_PATH is not None:
        return _CACHED_FONT_PATH

    for candidate in FONT_CANDIDATES:
        if candidate and Path(candidate).is_file():
            _CACHED_FONT_PATH = candidate
            return candidate

    _CACHED_FONT_PATH = None
    return None


@lru_cache(maxsize=2048)
def render_halfblock(char: str, size: int = 18) -> str:
    """
    Renders a single Kanji character into multi-line half-block characters (█, ▀, ▄).
    Default size 18 yields 8-9 terminal lines.
    Output is clean uncolored text (inherits terminal foreground theme).
    """
    if not char:
        return ""

    font_path = find_cjk_font()
    if not font_path:
        return char

    try:
        from PIL import Image, ImageDraw, ImageFont

        font = ImageFont.truetype(font_path, size)
        img = Image.new("1", (size, size), color=0)
        draw = ImageDraw.Draw(img)
        bbox = font.getbbox(char)
        if not bbox:
            return char

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((size - w) // 2 - bbox[0], (size - h) // 2 - bbox[1]), char, font=font, fill=1)

        raw_lines = []
        for y in range(0, size, 2):
            row = []
            for x in range(size):
                top = img.getpixel((x, y))
                bot = img.getpixel((x, y + 1)) if y + 1 < size else 0
                if top and bot:
                    row.append("█")
                elif top and not bot:
                    row.append("▀")
                elif not top and bot:
                    row.append("▄")
                else:
                    row.append(" ")
            raw_lines.append("".join(row))

        # Trim leading and trailing empty lines for compact 8-10 line height
        while raw_lines and not raw_lines[0].strip():
            raw_lines.pop(0)
        while raw_lines and not raw_lines[-1].strip():
            raw_lines.pop()

        if not raw_lines:
            return char

        return "\n".join(raw_lines)
    except Exception:
        return char


@lru_cache(maxsize=2048)
def render_braille(char: str, size: int = 24) -> str:
    """
    Renders a single Kanji character into Unicode 2x4 braille dot matrix.
    Yields ~6-7 terminal lines.
    """
    if not char:
        return ""

    font_path = find_cjk_font()
    if not font_path:
        return char

    try:
        from PIL import Image, ImageDraw, ImageFont

        font = ImageFont.truetype(font_path, size)
        img = Image.new("1", (size, size), color=0)
        draw = ImageDraw.Draw(img)
        bbox = font.getbbox(char)
        if not bbox:
            return char

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((size - w) // 2 - bbox[0], (size - h) // 2 - bbox[1]), char, font=font, fill=1)

        raw_lines = []
        for y in range(0, size, 4):
            row = []
            for x in range(0, size, 2):
                byte = 0
                if img.getpixel((x, y)):
                    byte |= 1
                if y + 1 < size and img.getpixel((x, y + 1)):
                    byte |= 2
                if y + 2 < size and img.getpixel((x, y + 2)):
                    byte |= 4
                if y + 3 < size and img.getpixel((x, y + 3)):
                    byte |= 64
                if x + 1 < size:
                    if img.getpixel((x + 1, y)):
                        byte |= 8
                    if y + 1 < size and img.getpixel((x + 1, y + 1)):
                        byte |= 16
                    if y + 2 < size and img.getpixel((x + 1, y + 2)):
                        byte |= 32
                    if y + 3 < size and img.getpixel((x + 1, y + 3)):
                        byte |= 128
                row.append(chr(0x2800 + byte))
            raw_lines.append("".join(row))

        while raw_lines and not raw_lines[0].strip():
            raw_lines.pop(0)
        while raw_lines and not raw_lines[-1].strip():
            raw_lines.pop()

        if not raw_lines:
            return char

        return "\n".join(raw_lines)
    except Exception:
        return char
