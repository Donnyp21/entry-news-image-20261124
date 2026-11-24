"""Paint the front page for Tuesday 24 November 2026.

Build-time artwork generator (Pillow). Every shape and line of text
below is drawn by this script -- no photographs, no outside artwork.
The page it paints is saved next to this file as art.jpg, a
1024x1024 JPEG, and main.py later checks and ships that file.

The stories are the day's verified headlines:

  lead   Ukraine's sea drones sank the Russian corvette Merkury at
         the Benghazi naval base in Libya on 23 Nov; Libya wants
         answers from Kyiv and the UN wants a probe.
  one    25 Russian airspace violations against NATO members in
         2026, four times the 2024 total; missiles and a drone
         came down in Poland on 20 Nov.
  two    Fourteen countries recognise the ICJ ruling that Myanmar
         committed genocide against the Rohingya.
  three  Markets surged as Nvidia reinstated Jensen Huang after
         Trump intervened: Kospi, Nikkei, Nasdaq, S&P all up hard.
  four   US Treasury sanctions on two dozen Iranian exchange
         houses, against a backdrop of Hormuz tension.
  strip  Putin reportedly open to Article 5-style guarantees for
         Ukraine if no NATO troops are deployed.
  foot   COP31 collapsed in Antalya; a 5.6 quake in Nepal; a
         factory fire in Cikande, Indonesia; a ninth measles
         death in Pennsylvania.

Run:  python3 gen_image.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
HERE = Path(__file__).resolve().parent
TARGET = HERE / "art.jpg"

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF_BOLD = str(FONT_DIR / "dejavu" / "DejaVuSerif-Bold.ttf")
SANS = str(FONT_DIR / "dejavu" / "DejaVuSans.ttf")
SANS_BOLD = str(FONT_DIR / "dejavu" / "DejaVuSans-Bold.ttf")
SANS_OBLIQUE = str(FONT_DIR / "liberation" / "LiberationSans-Italic.ttf")

PAPER = (247, 242, 231)
INK = (26, 25, 23)
BODY = (52, 50, 46)
MUTED = (96, 90, 78)
RED = (158, 30, 38)
RULE = (60, 56, 48)
SKY = (197, 218, 233)
SEA_LIGHT = (52, 102, 143)
SEA_DARK = (22, 58, 96)
HULL = (84, 90, 99)
HULL_DARK = (52, 57, 65)
SMOKE = (150, 148, 144)
SUN = (243, 197, 84)
WHITE = (250, 250, 248)


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Split text into lines that fit width, on word boundaries."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def block(draw, x, y, text, font, fill, width, leading):
    """Draw wrapped text at (x, y); return the y below it."""
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centered(draw, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text(((SIDE - w) / 2, y), text, font=font, fill=fill)


def sea_battle(draw, box):
    """The lead picture: a corvette under sea-drone attack."""
    x0, y0, x1, y1 = box
    horizon = y0 + int((y1 - y0) * 0.46)
    draw.rectangle([x0, y0, x1, horizon], fill=SKY)
    draw.rectangle([x0, horizon, x1, y1], fill=SEA_DARK)
    # lighter swells rolling toward the viewer, clipped to the box
    yy, band = horizon + 10, 0
    while yy + 11 <= y1:
        if band % 2 == 0:
            draw.rectangle([x0, yy, x1, yy + 11], fill=SEA_LIGHT)
        yy += 22
        band += 1
    # sun, low over the water
    cx, cy, r = x1 - 84, y0 + 52, 26
    draw.ellipse([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9],
                 fill=(250, 224, 150))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN)
    # the corvette, side-on, bow to the right
    base = horizon + 50
    draw.polygon([(x0 + 56, base + 10), (x0 + 84, base - 20),
                  (x0 + 330, base - 20), (x0 + 356, base + 10)], fill=HULL)
    draw.rectangle([x0 + 150, base - 44, x0 + 240, base - 20], fill=HULL)
    draw.rectangle([x0 + 172, base - 60, x0 + 218, base - 44],
                   fill=HULL_DARK)
    draw.line([x0 + 195, base - 60, x0 + 195, base - 86],
              fill=HULL_DARK, width=4)
    draw.line([x0 + 176, base - 80, x0 + 214, base - 80],
              fill=HULL_DARK, width=3)
    draw.rectangle([x0 + 286, base - 34, x0 + 318, base - 20], fill=HULL_DARK)
    # smoke from a hit amidships, kept inside the frame
    for dx, dy, rr in [(0, 0, 11), (13, -15, 14), (28, -29, 16),
                       (44, -42, 18), (60, -52, 19)]:
        px, py = x0 + 205 + dx, base - 64 + dy
        draw.ellipse([px - rr, py - rr, px + rr, py + rr], fill=SMOKE)
    # two sea drones closing in, wakes behind them
    for dx, dy in [(404, 40), (330, 82)]:
        px, py = x0 + dx, horizon + dy
        draw.polygon([(px, py), (px + 56, py + 6), (px + 48, py + 16),
                      (px + 8, py + 15)], fill=(30, 32, 36))
        draw.polygon([(px + 10, py), (px + 18, py - 11), (px + 26, py)],
                     fill=(30, 32, 36))
        for k in range(3):
            draw.line([px - 14 - k * 18, py + 8 + k * 2, px - 2 - k * 18,
                       py + 8 + k * 2], fill=WHITE, width=2)
    # spray where the first drone struck, at the bow
    for dx in range(-6, 26, 8):
        draw.line([x0 + 348 + dx, base + 6, x0 + 340 + dx, base - 16],
                  fill=WHITE, width=3)
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def story(draw, x, y, width, number, head, body, head_font, body_font):
    draw.ellipse([x, y + 2, x + 30, y + 32], fill=RED)
    num_w = draw.textlength(number, font=body_font)
    draw.text((x + (30 - num_w) / 2, y + 5), number, font=body_font,
              fill=WHITE)
    y = block(draw, x + 42, y, head, head_font, INK, width - 42, 27)
    block(draw, x + 42, y + 2, body, body_font, BODY, width - 42, 23)


def paint():
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    draw = ImageDraw.Draw(img)
    margin = 36
    right = SIDE - margin

    # masthead
    centered(draw, 22, "THE DAILY RECORD", load(SERIF_BOLD, 57), INK)
    draw.line([margin, 96, right, 96], fill=RULE, width=3)
    draw.line([margin, 101, right, 101], fill=RULE, width=1)
    centered(draw, 110, "TUESDAY 24 NOVEMBER 2026", load(SANS_BOLD, 30), RED)
    centered(draw, 146, "The world's news of one day, in one picture",
             load(SANS_OBLIQUE, 19), MUTED)
    draw.line([margin, 176, right, 176], fill=RULE, width=1)

    # lead story
    draw.text((margin, 188), "LEAD STORY · THE MEDITERRANEAN",
              font=load(SANS_BOLD, 19), fill=RED)
    y = block(draw, margin, 214,
              "Ukraine's sea drones sink a Russian corvette off Libya",
              load(SERIF_BOLD, 43), INK, right - margin, 50)
    sea_battle(draw, (margin, y + 10, 596, y + 218))
    lead_x = 620
    ly = y + 14
    ly = block(draw, lead_x, ly,
               "Sea drones sank the corvette Merkury at the Benghazi "
               "naval base on 23 November — the Black Sea war reaches "
               "the Mediterranean.", load(SANS, 21), BODY,
               right - lead_x, 27)
    block(draw, lead_x, ly + 10,
          "Libya is demanding explanations from Kyiv, and the United "
          "Nations is seeking a probe into the strike.",
          load(SANS, 21), BODY, right - lead_x, 27)
    cap_y = y + 226
    draw.text((margin, cap_y), "A corvette burns as naval drones close in.",
              font=load(SANS_OBLIQUE, 17), fill=MUTED)
    draw.line([margin, cap_y + 28, right, cap_y + 28], fill=RULE, width=1)

    # four more stories, two by two
    head_font, body_font = load(SANS_BOLD, 23), load(SANS, 19)
    top = cap_y + 42
    col_w = (right - margin - 28) // 2
    story(draw, margin, top, col_w, "1", "Russia tests NATO skies",
          "25 airspace violations against NATO members in 2026 — four "
          "times the 2024 total. Two missiles and a drone crashed in "
          "Poland on 20 Nov.", head_font, body_font)
    story(draw, margin + col_w + 28, top, col_w, "2",
          "14 nations back the Rohingya ruling",
          "Britain, Spain, Canada, Australia and ten more recognise "
          "the ICJ ruling that Myanmar committed genocide against "
          "the Rohingya.", head_font, body_font)
    second = top + 126
    story(draw, margin, second, col_w, "3", "Markets surge on Nvidia U-turn",
          "Huang reinstated after Trump intervened: Kospi +6–7%, "
          "Nikkei +3.9%, Nasdaq +6.5%, S&P 500 +4.7%.",
          head_font, body_font)
    story(draw, margin + col_w + 28, second, col_w, "4",
          "US sanctions Iran money houses",
          "The Treasury sanctions two dozen Iranian exchange houses "
          "amid Hormuz tensions; Tehran sets 7 conditions.",
          head_font, body_font)

    # wire strip
    strip_y = second + 124
    draw.rectangle([margin, strip_y, right, strip_y + 54], fill=INK)
    block(draw, margin + 14, strip_y + 6,
          "PUTIN 'OPEN TO ARTICLE 5-STYLE GUARANTEES FOR UKRAINE' "
          "— NO NATO TROOPS, REPORTS SAY",
          load(SANS_BOLD, 18), WHITE, right - margin - 28, 23)

    # footline: the rest of the day in brief
    foot_y = strip_y + 70
    draw.line([margin, foot_y, right, foot_y], fill=RULE, width=1)
    block(draw, margin, foot_y + 12,
          "ALSO TODAY — COP31 collapses in Antalya over fossil-fuel "
          "wording, the first failure since 2009; COP32 goes to "
          "Addis Ababa · Nepal: 5.6 earthquake near the China "
          "border · Factory fire in Cikande, Indonesia, with "
          "casualties · Ninth measles death in Pennsylvania",
          load(SANS, 18), BODY, right - margin, 24)

    img.save(TARGET, "JPEG", quality=88)
    print(f"painted {TARGET} ({TARGET.stat().st_size} bytes)")


if __name__ == "__main__":
    paint()
