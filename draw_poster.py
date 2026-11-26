#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news poster (1024x1024, deterministic).

Pure PIL, no network, no external images. Run: python3 draw_poster.py
Writes entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---
NAVY_TOP = (10, 14, 42)
NAVY_BOT = (22, 30, 82)
CARD = (27, 35, 80)
CARD_EDGE = (58, 70, 130)
WHITE = (255, 255, 255)
YELLOW = (255, 210, 63)
RED = (255, 59, 48)
ORANGE = (255, 122, 26)
TEAL = (25, 194, 184)
BLUE = (80, 160, 255)
GREEN = (70, 210, 120)
MUTED = (201, 207, 232)
GOLD = (242, 183, 5)
GLOBE = (14, 90, 99)
GLOBE_LAND = (242, 183, 5)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def flame(draw, cx, base_y, w, h, colors):
    """Simple teardrop flame: outer, mid, inner stacked polygons."""
    pts_outer = [
        (cx, base_y - h),
        (cx + w * 0.42, base_y - h * 0.55),
        (cx + w * 0.5, base_y - h * 0.28),
        (cx + w * 0.28, base_y),
        (cx - w * 0.28, base_y),
        (cx - w * 0.5, base_y - h * 0.28),
        (cx - w * 0.42, base_y - h * 0.55),
    ]
    draw.polygon(pts_outer, fill=colors[0])
    pts_mid = [
        (cx, base_y - h * 0.62),
        (cx + w * 0.26, base_y - h * 0.32),
        (cx + w * 0.3, base_y - h * 0.12),
        (cx + w * 0.16, base_y),
        (cx - w * 0.16, base_y),
        (cx - w * 0.3, base_y - h * 0.12),
        (cx - w * 0.26, base_y - h * 0.32),
    ]
    draw.polygon(pts_mid, fill=colors[1])
    pts_in = [
        (cx, base_y - h * 0.38),
        (cx + w * 0.15, base_y - h * 0.16),
        (cx + w * 0.12, base_y),
        (cx - w * 0.12, base_y),
        (cx - w * 0.15, base_y - h * 0.16),
    ]
    draw.polygon(pts_in, fill=colors[2])


def draw_globe(img, size=270):
    """Stylised globe on its own layer, clipped to a circle."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, size - 1, size - 1], fill=255)
    land = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(land)
    ld.ellipse([0, 0, size - 1, size - 1], fill=GLOBE + (255,))
    # rough continents (gold blobs)
    ld.polygon([(52, 78), (96, 58), (128, 84), (112, 122), (78, 128), (48, 108)], fill=GOLD + (255,))
    ld.polygon([(150, 66), (196, 52), (232, 78), (214, 112), (168, 118), (146, 96)], fill=GOLD + (255,))
    ld.polygon([(120, 150), (168, 140), (196, 168), (176, 208), (138, 212), (112, 182)], fill=GOLD + (255,))
    ld.polygon([(212, 160), (252, 150), (268, 182), (240, 210), (210, 196)], fill=GOLD + (255,))
    ld.polygon([(66, 196), (104, 188), (118, 218), (88, 240), (58, 224)], fill=GOLD + (255,))
    # latitude / longitude arcs
    for frac, col in ((0.30, (120, 220, 220)), (0.5, (120, 220, 220)), (0.70, (120, 220, 220))):
        y = int(size * frac)
        d.ellipse([-40, y - 26, size + 40, y + 26], outline=col + (180,), width=3)
    d.ellipse([size // 2 - 46, -30, size // 2 + 46, size + 30], outline=(120, 220, 220, 180), width=3)
    d.ellipse([size // 2 - 96, -60, size // 2 + 96, size + 60], outline=(120, 220, 220, 120), width=3)
    layer.paste(land, (0, 0), mask)
    d2 = ImageDraw.Draw(layer)
    d2.ellipse([0, 0, size - 1, size - 1], outline=YELLOW + (255,), width=9)
    return layer


def draw_rocket(d, x, y, scale=1.0):
    """Small rocket angled up-right, with flame trail."""
    # flame trail (behind body)
    flame(d, int(x - 34 * scale), int(y + 52 * scale), int(30 * scale), int(52 * scale),
          (ORANGE, YELLOW, WHITE))
    # body: pointed nose, straight sides, fins
    body = [
        (x, y - 78 * scale),
        (x + 26 * scale, y - 18 * scale),
        (x + 26 * scale, y + 34 * scale),
        (x - 26 * scale, y + 34 * scale),
        (x - 26 * scale, y - 18 * scale),
    ]
    d.polygon(body, fill=WHITE)
    d.polygon([(x - 26 * scale, y + 10 * scale), (x - 52 * scale, y + 46 * scale),
               (x - 26 * scale, y + 34 * scale)], fill=RED)
    d.polygon([(x + 26 * scale, y + 10 * scale), (x + 52 * scale, y + 46 * scale),
               (x + 26 * scale, y + 34 * scale)], fill=RED)
    d.ellipse([x - 13 * scale, y - 52 * scale, x + 13 * scale, y - 26 * scale],
              fill=TEAL, outline=NAVY_TOP, width=3)
    d.rectangle([x - 26 * scale, y + 34 * scale, x + 26 * scale, y + 42 * scale], fill=RED)


def bars_icon(d, x, y, color, w=54, h=40):
    xs = [x, x + 19, x + 38]
    hs = [16, 28, 40]
    for bx, bh in zip(xs, hs):
        d.rectangle([bx, y + h - bh, bx + 13, y + h], fill=color)
    # rising arrow
    d.line([x - 2, y + h - 14, x + w - 2, y - 6], fill=color, width=5)
    d.polygon([(x + w - 2, y - 6), (x + w - 16, y - 4), (x + w - 4, y + 8)], fill=color)


def shield_icon(d, x, y, color):
    pts = [(x + 27, y), (x + 54, y + 10), (x + 54, y + 28), (x + 27, y + 52),
           (x, y + 28), (x, y + 10)]
    d.polygon(pts, outline=color, width=5)
    d.polygon([(x + 27, y + 12), (x + 35, y + 24), (x + 27, y + 40),
               (x + 19, y + 24)], fill=color)


def peace_icon(d, x, y, color):
    d.ellipse([x, y, x + 52, y + 52], outline=color, width=5)
    d.line([x + 26, y + 2, x + 26, y + 50], fill=color, width=5)
    d.line([x + 26, y + 26, x + 6, y + 46], fill=color, width=5)
    d.line([x + 26, y + 26, x + 46, y + 46], fill=color, width=5)


def main():
    img = Image.new("RGB", (W, H), NAVY_TOP)
    d = ImageDraw.Draw(img)
    # vertical gradient
    for yy in range(H):
        t = yy / (H - 1)
        r = int(NAVY_TOP[0] + (NAVY_BOT[0] - NAVY_TOP[0]) * t)
        g = int(NAVY_TOP[1] + (NAVY_BOT[1] - NAVY_TOP[1]) * t)
        b = int(NAVY_TOP[2] + (NAVY_BOT[2] - NAVY_TOP[2]) * t)
        d.line([(0, yy), (W, yy)], fill=(r, g, b))
    # diagonal sunburst rays from top-right
    ray = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ray)
    for i, ang in enumerate(range(-78, -10, 12)):
        import math
        a = math.radians(ang)
        x2 = 1024 + int(1400 * math.cos(a))
        y2 = -40 + int(1400 * math.sin(a))
        rd.polygon([(1024, -40), (x2, y2),
                    (1024 + int(1400 * math.cos(math.radians(ang + 5))),
                     -40 + int(1400 * math.sin(math.radians(ang + 5))))],
                   fill=(255, 255, 255, 14 if i % 2 == 0 else 0))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ray).convert("RGB"), (0, 0))

    # ---- header ----
    f_kick = font(BOLD, 30)
    f_day = font(BOLD, 108)
    f_date = font(BOLD, 76)
    d.text((48, 30), "THE WORLD IN ONE DAY", font=f_kick, fill=YELLOW)
    d.text((46, 62), "THURSDAY", font=f_day, fill=WHITE)
    d.text((48, 168), "26 NOVEMBER 2026", font=f_date, fill=YELLOW)
    d.rectangle([48, 258, 976, 266], fill=RED)

    # ---- hero: globe + rocket + tariff bars ----
    globe = draw_globe(img, size=270)
    img.paste(globe, (96, 292), globe)
    d = ImageDraw.Draw(img)
    # red orbit ring around globe (tilted ellipse arc)
    d.arc([66, 296, 392, 546], start=200, end=340, fill=RED, width=7)
    d.arc([66, 296, 392, 546], start=20, end=160, fill=RED, width=7)
    # rocket launching up-right of the globe
    draw_rocket(d, 700, 390, scale=1.0)
    # motion dots trailing the rocket
    for i, (dx, dy, r) in enumerate([(648, 482, 7), (612, 510, 5), (582, 534, 4)]):
        d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=(255, 255, 255, 255) if i == 0 else YELLOW)
    # tariff bars motif, bottom-right of hero
    bars_icon(d, 830, 452, RED, w=110, h=64)
    d.text((806, 522), "TARIFFS UP", font=font(BOLD, 24), fill=RED)

    # ---- story tiles ----
    stories = [
        ("TARIFFS", RED, "bars",
         "US unveils 'Thanksgiving tariffs'",
         "14 partners hit \u2014 China up to 40%"),
        ("OIL", ORANGE, "flame",
         "Houthis claim refinery strike",
         "Brent crude jumps past $94 a barrel"),
        ("UKRAINE", BLUE, "peace",
         "Geneva talks end, no breakthrough",
         "Next round promised; Europe's role open"),
        ("SPACE", TEAL, "rocket",
         "First Pakistani astronaut in orbit",
         "Shenzhou-24 docks at Tiangong station"),
        ("CAIRO", YELLOW, "flame",
         "Tanker fire kills 30+ near Cairo",
         "Ring Road blaze engulfs dozens of cars"),
        ("POLAND", GREEN, "shield",
         "Poland plans border no-fly zone",
         "Seeks NATO role against incursions"),
    ]
    tile_w, tile_h = 316, 196
    gap = 14
    x0, y0 = 16, 585
    f_tag = font(BOLD, 22)
    f_title = font(BOLD, 25)
    f_sub = font(REG, 19)
    for i, (tag, color, icon, title, sub) in enumerate(stories):
        col, row = i % 3, i // 3
        x = x0 + col * (tile_w + gap)
        y = y0 + row * (tile_h + gap)
        d.rounded_rectangle([x, y, x + tile_w, y + tile_h], radius=18,
                            fill=CARD, outline=CARD_EDGE, width=2)
        d.rectangle([x + 18, y, x + tile_w - 18, y + 7], fill=color)
        # icon
        ix, iy = x + 20, y + 26
        if icon == "bars":
            bars_icon(d, ix, iy, color)
        elif icon == "flame":
            flame(d, ix + 26, iy + 50, 44, 52, (color, YELLOW, WHITE))
        elif icon == "peace":
            peace_icon(d, ix, iy, color)
        elif icon == "rocket":
            draw_rocket(d, ix + 26, iy + 26, scale=0.42)
        elif icon == "shield":
            shield_icon(d, ix, iy, color)
        # tag
        d.text((x + 86, y + 30), tag, font=f_tag, fill=color)
        # title (max 2 lines)
        lines = wrap(d, title, f_title, tile_w - 36)
        ty = y + 84
        for ln in lines[:2]:
            d.text((x + 18, ty), ln, font=f_title, fill=WHITE)
            ty += 30
        # sub (max 2 lines)
        slines = wrap(d, sub, f_sub, tile_w - 36)
        sy = y + 84 + 30 * min(len(lines), 2) + 4
        for ln in slines[:2]:
            d.text((x + 18, sy), ln, font=f_sub, fill=MUTED)
            sy += 23

    # ---- footer ----
    d.rectangle([48, 997, 976, 999], fill=CARD_EDGE)
    f_foot = font(BOLD, 22)
    foot = "6 STORIES  \u00b7  ONE DAY  \u00b7  THURSDAY 26 NOVEMBER 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 1001), foot, font=f_foot, fill=YELLOW)

    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
