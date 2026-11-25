#!/usr/bin/env python3
"""Render the 24 Nov 2026 world-news infographic (1024x1024 PNG).

v1: newspaper layout — masthead, 2x3 story panels, footer ticker.
All facts from web research on 24 Nov 2026 (Just Security Early Edition,
Principia, The Global Eye, Reuters diary, Medium brief).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 24, 39)
NAVY = (13, 42, 84)
RED = (178, 34, 34)
MUTED = (90, 90, 90)
PANEL = (255, 255, 255)
LINE = (200, 196, 186)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 26)
F_TAG = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans-Bold.ttf", 17)

STORIES = [
    ("TECH", "NVIDIA BRINGS BACK JENSEN HUANG",
     "Reinstated as CEO and chair less than two weeks after he resigned. "
     "Trump says he pressed the board. Shares surge."),
    ("JUSTICE", "14 NATIONS BACK ICJ ROHINGYA RULING",
     "UK, Spain, Canada, Australia and 10 more endorse the court's genocide "
     "finding against Myanmar. UK sanctions five generals."),
    ("SPACE", "NATO VOWS TO DEFEND SPACE",
     "Chief Mark Rutte warns Russia after reports Moscow may launch a "
     "nuclear-armed satellite as soon as next month."),
    ("ENERGY", "TANKERS HIT BY MINES IN HORMUZ",
     "Iran says three oil tankers struck mines and caught fire in the strait, "
     "as Tehran vows to confront the US naval blockade."),
    ("MIDDLE EAST", "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
     "Airstrikes in Gaza kill Naeem Abu Nahel and six others, including two "
     "police officers, medics say."),
    ("UKRAINE", "RUSSIAN STRIKE HITS ZAPORIZHZHIA FLATS",
     "Overnight attack kills two and wounds 40, including four children, "
     "after hitting an apartment building."),
]

FOOTER_LINES = [
    "ALSO:  UN climate summit ends without a deal  •  US loses measles "
    "elimination status",
    "Sanofi to buy Insmed for $41bn  •  47,000 women killed by "
    "partners or relatives in 2025",
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 148], fill=NAVY)
    title = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, 22),
           title, font=F_TITLE, fill=(255, 255, 255))
    date = "TUESDAY  •  24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 96),
           date, font=F_DATE, fill=(255, 209, 102))
    d.rectangle([0, 148, W, 152], fill=RED)

    # --- Story grid: 2 cols x 3 rows ---
    gx, gy, gap = 28, 172, 20
    pw = (W - 2 * gx - gap) // 2
    ph = 240
    for i, (tag, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                            fill=PANEL, outline=LINE, width=2)
        # red tag bar + tag
        d.rectangle([x, y, x + 8, y + ph], fill=RED)
        tx = x + 24
        d.text((tx, y + 16), tag, font=F_TAG, fill=RED)
        d.line([tx, y + 46, x + pw - 24, y + 46], fill=LINE, width=2)
        # headline (max 3 lines)
        lines = wrap(d, head, F_HEAD, pw - 48)[:3]
        hy = y + 58
        for ln in lines:
            d.text((tx, hy), ln, font=F_HEAD, fill=INK)
            hy += 33
        # body (max 4 lines)
        blines = wrap(d, body, F_BODY, pw - 48)[:4]
        by = hy + 8
        for ln in blines:
            d.text((tx, by), ln, font=F_BODY, fill=(55, 55, 55))
            by += 27

    # --- Footer ticker (two lines so nothing is cut off) ---
    fy = H - 76
    d.rectangle([0, fy, W, H], fill=INK)
    d.text((28, fy + 10), FOOTER_LINES[0], font=F_FOOT, fill=(255, 255, 255))
    d.text((28, fy + 40), FOOTER_LINES[1], font=F_FOOT, fill=(200, 200, 200))

    img.save("news.png", optimize=True)
    print("saved news.png", img.size)


if __name__ == "__main__":
    main()
