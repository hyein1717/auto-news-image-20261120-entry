#!/usr/bin/env python3
"""World news of Friday 20 November 2026, summed up in one image.

Builds a 1024x1024 newspaper front page: a generated cyclone artwork as
the hero (Cyclone Akvan's landfall on India's Odisha coast), the date
named in the masthead, and three further verified stories of the day
below it. Deterministic: same bytes on every run, no network, no input.

Stories verified against live reporting on 20 November 2026:
  1. Cyclone Akvan makes landfall near Gopalpur, Odisha, around noon
     IST, winds 90-100 km/h gusting to 110, 100,000+ people evacuated
     (India Meteorological Department, via India Today / PTI).
  2. India vs New Zealand, 1st Test, Day 1 in Wellington: New Zealand
     243/5 at stumps, Henry Nicholls 113 not out (Times of India).
  3. US President Donald Trump to brief the press on Friday about his
     China trip, after Thursday's first-ever Trump-Xi-Putin trilateral
     summit in Shenzhen (CBS).
  4. World Children's Day, marked around the world on 20 November
     (United Nations observance).
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
FONTS = ASSETS / "fonts"

SIZE = 1024
PAPER = (250, 247, 240)      # warm newsprint white
INK = (15, 27, 45)           # deep navy ink
GREY = (84, 92, 104)         # secondary text
RED = (178, 34, 34)          # masthead / kicker red
RULE = (196, 190, 178)       # hairline rules
CARD_BG = (255, 255, 255)    # story card fill
CARD_LINE = (214, 209, 198)  # story card border

DATE_LINE = "20 NOVEMBER 2026"
MASTHEAD_TOP = "FRIDAY  •  THE WORLD IN ONE DAY"
HEADLINE = "CYCLONE AKVAN HITS ODISHA"
SUBLINE = "Landfall near Gopalpur at noon  •  100 km/h winds  •  100,000 evacuated"
FOOTER = "FRIDAY 20 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE IMAGE"

# (kicker, headline, subline, icon) for the three story cards.
CARDS = [
    (
        "CRICKET  •  WELLINGTON",
        "NICHOLLS 113* AS NZ REACH 243/5",
        "Day 1 of the 1st Test vs India",
        "cricket",
    ),
    (
        "USA  •  CHINA TRIP",
        "TRUMP TO BRIEF ON CHINA TRIP",
        "After the first three-way summit",
        "podium",
    ),
    (
        "AROUND THE WORLD",
        "WORLD CHILDREN'S DAY",
        "Marked across the globe today",
        "sun",
    ),
]


def font(name, size):
    """Load a bundled DejaVu font; fall back to PIL's default font."""
    path = FONTS / name
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def fit_font(draw, text, name, start_size, max_width, min_size=10):
    """Largest font size at which `text` fits within `max_width`."""
    size = start_size
    while size > min_size:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(name, min_size)


def wrap_text(draw, text, f, max_width):
    """Greedy word wrap; returns a list of lines that fit `max_width`."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, y, text, f, fill, canvas_width=SIZE):
    """Draw one line of text horizontally centred at height y."""
    width = draw.textlength(text, font=f)
    draw.text(((canvas_width - width) / 2, y), text, font=f, fill=fill)


def draw_icon(draw, kind, x, y, s):
    """Small geometric pictogram for a story card, inside a s-by-s box."""
    if kind == "cricket":
        # Green pitch, three stumps, red ball.
        draw.rectangle([x, y + s * 0.55, x + s, y + s * 0.95], fill=(46, 125, 50))
        draw.rectangle([x + s * 0.30, y + s * 0.10, x + s * 0.36, y + s * 0.55],
                       fill=(212, 175, 55))
        draw.rectangle([x + s * 0.47, y + s * 0.10, x + s * 0.53, y + s * 0.55],
                       fill=(212, 175, 55))
        draw.rectangle([x + s * 0.64, y + s * 0.10, x + s * 0.70, y + s * 0.55],
                       fill=(212, 175, 55))
        draw.ellipse([x + s * 0.72, y + s * 0.28, x + s * 0.92, y + s * 0.48],
                     fill=(178, 34, 34))
    elif kind == "podium":
        # Lectern with a microphone dot.
        draw.polygon([(x + s * 0.15, y + s * 0.95), (x + s * 0.85, y + s * 0.95),
                      (x + s * 0.72, y + s * 0.45), (x + s * 0.28, y + s * 0.45)],
                     fill=(15, 27, 45))
        draw.rectangle([x + s * 0.10, y + s * 0.38, x + s * 0.90, y + s * 0.48],
                       fill=(15, 27, 45))
        draw.line([x + s * 0.62, y + s * 0.38, x + s * 0.72, y + s * 0.18],
                  fill=(15, 27, 45), width=4)
        draw.ellipse([x + s * 0.66, y + s * 0.06, x + s * 0.80, y + s * 0.20],
                     fill=(178, 34, 34))
    else:  # "sun"
        # Rising sun over a horizon, for World Children's Day.
        cx, cy, r = x + s * 0.5, y + s * 0.45, s * 0.26
        for angle in range(0, 360, 45):
            import math
            x1 = cx + (r + 4) * math.cos(math.radians(angle))
            y1 = cy + (r + 4) * math.sin(math.radians(angle))
            x2 = cx + (r + 14) * math.cos(math.radians(angle))
            y2 = cy + (r + 14) * math.sin(math.radians(angle))
            draw.line([x1, y1, x2, y2], fill=(212, 160, 32), width=4)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 184, 44))
        draw.rectangle([x, y + s * 0.82, x + s, y + s * 0.90], fill=(46, 125, 50))


def prepare_hero(width, height):
    """Crop the cyclone artwork to the hero box and sharpen it."""
    hero = Image.open(ASSETS / "hero.png").convert("RGB")
    target = width / height
    w, h = hero.size
    if w / h > target:  # too wide: trim the sides
        new_w = int(h * target)
        left = (w - new_w) // 2
        hero = hero.crop((left, 0, left + new_w, h))
    else:  # too tall: trim top and bottom, keeping the boat and palms
        new_h = int(w / target)
        top = int((h - new_h) * 0.25)
        hero = hero.crop((0, top, w, top + new_h))
    hero = hero.resize((width, height), Image.Resampling.LANCZOS)
    hero = ImageEnhance.Sharpness(hero).enhance(1.18)
    hero = ImageEnhance.Contrast(hero).enhance(1.08)
    return hero


def build():
    """Compose the front page and return the finished image."""
    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(page)

    # --- Masthead: the day, named loud and clear. ---
    draw_centered(draw, 14, MASTHEAD_TOP,
                  font("DejaVuSans.ttf", 24), GREY)
    draw_centered(draw, 40, DATE_LINE,
                  fit_font(draw, DATE_LINE, "DejaVuSans-Bold.ttf", 62, 960),
                  INK)
    draw.line([24, 108, SIZE - 24, 108], fill=RED, width=4)

    # --- Hero: the cyclone fills most of the frame. ---
    hero = prepare_hero(SIZE, 620)
    page.paste(hero, (0, 112))
    draw.rectangle([0, 112, SIZE, 732], outline=INK, width=2)

    # --- Headline and standfirst under the hero. ---
    draw_centered(draw, 744, HEADLINE,
                  fit_font(draw, HEADLINE, "DejaVuSans-Bold.ttf", 54, 980),
                  INK)
    draw_centered(draw, 800, SUBLINE,
                  fit_font(draw, SUBLINE, "DejaVuSans.ttf", 25, 980), GREY)
    draw.line([24, 836, SIZE - 24, 836], fill=RULE, width=2)

    # --- Three story cards in a row. ---
    card_w, card_h, gap, top = 320, 132, 16, 850
    for i, (kicker, headline, subline, icon) in enumerate(CARDS):
        x = gap + i * (card_w + gap)
        draw.rectangle([x, top, x + card_w, top + card_h],
                       fill=CARD_BG, outline=CARD_LINE, width=2)
        draw_icon(draw, icon, x + 14, top + 10, 44)
        draw.text((x + 66, top + 12), kicker,
                  font=font("DejaVuSans-Bold.ttf", 17), fill=RED)
        head_font = font("DejaVuSans-Bold.ttf", 23)
        lines = wrap_text(draw, headline, head_font, card_w - 28)
        y = top + 56
        for line in lines[:2]:
            draw.text((x + 14, y), line, font=head_font, fill=INK)
            y += 26
        draw.text((x + 14, top + 110), subline,
                  font=fit_font(draw, subline, "DejaVuSans.ttf", 18,
                                card_w - 28),
                  fill=GREY)

    # --- Footer repeats the date so the day is unmistakable. ---
    draw.line([24, 994, SIZE - 24, 994], fill=RULE, width=2)
    draw_centered(draw, 1002, FOOTER,
                  fit_font(draw, FOOTER, "DejaVuSans.ttf", 18, 980), GREY)
    return page


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # JPEG bytes in entry.png: the kit allows PNG or JPEG, told apart by
    # first bytes, under the same name. A photographic hero makes PNG
    # exceed the 1 MiB cap; JPEG at quality 90 with 4:4:4 subsampling
    # stays well under it while keeping the text crisp. Deterministic.
    build().convert("RGB").save(
        out_dir / "entry.png", format="JPEG", quality=90,
        subsampling=0, optimize=True,
    )


if __name__ == "__main__":
    main()
