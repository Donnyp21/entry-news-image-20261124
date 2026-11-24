"""Paint the news-image-20261124 front page: one picture that sums up
Tuesday 24 November 2026.

This file only runs at build time (here, with Pillow). The graded
program is main.py, which hands the finished art.jpg to the output
folder. Everything on the page is drawn with PIL primitives -- shapes
and text, no photos, no borrowed artwork -- so every headline reads
exactly as spelled below.

The day's stories, verified against reporting dated 24 Nov 2026
by web search this run:

  LEAD: Ukraine says its naval drones sank the Russian corvette
  Merkury at the Benghazi naval base in Libya on 23 Nov -- the
  Black Sea fight reaching the Mediterranean. Libya demands
  explanations from Kyiv; the UN seeks a probe.
  1. Russia is testing Article 5: 25 airspace violations against
  NATO members in 2026, four times the 2024 total; two missiles
  and a drone crashed in Poland on 20 Nov. Putin is reportedly
  open to Article 5-style security guarantees for Ukraine if no
  NATO troops deploy.
  2. The ICJ Rohingya ruling: 14 countries (the UK, Spain, Canada,
  Australia and 10 more) recognise the court's ruling that Myanmar
  committed genocide against the Rohingya.
  3. Markets surge on Nvidia reinstating Jensen Huang after Trump
  intervened: Kospi +6-7%, Nikkei +3.91%, Nasdaq +6.51%,
  S&P 500 +4.73%.
  4. The US Treasury sanctions two dozen-plus Iranian exchange
  houses; Hormuz mines and Gulf strike tensions run high, and
  Iran rules out negotiation until Washington meets 7 conditions.
  Also today: COP31 collapsed in Antalya over fossil-fuel wording
  (first COP failure since 2009; COP32 goes to Addis Ababa) --
  yesterday's lead, a strip item here; a 5.6 quake in Nepal near
  the China border; a factory fire in Cikande, Indonesia, with
  casualties; a 9th measles death in Pennsylvania.
"""

import math

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
MARGIN = 36
RIGHT = SIDE - MARGIN

PALETTE = {
    "paper": (247, 243, 234),
    "ink": (26, 26, 26),
    "grey": (74, 74, 74),
    "navy": (26, 42, 74),
    "red": (178, 34, 34),
    "steel": (96, 108, 124),
    "sky": (206, 224, 236),
    "gold": (196, 152, 44),
    "green": (46, 110, 62),
    "white": (252, 251, 247),
    "blue": (70, 110, 180),
    "rise": (110, 220, 130),
    "sand": (240, 205, 110),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FACES = {
    "serif_b": FONT_DIR + "DejaVuSerif-Bold.ttf",
    "serif": FONT_DIR + "DejaVuSerif.ttf",
    "sans_b": FONT_DIR + "DejaVuSans-Bold.ttf",
    "sans": FONT_DIR + "DejaVuSans.ttf",
}


def load_font(face, size):
    return ImageFont.truetype(FACES[face], size)


def fit_words(pen, body, face_font, width):
    """Greedy word wrap measured in pixels."""
    fitted, current = [], ""
    for word in body.split():
        candidate = word if current == "" else current + " " + word
        if pen.textlength(candidate, font=face_font) <= width:
            current = candidate
        elif current:
            fitted.append(current)
            current = word
        else:
            current = word
    if current:
        fitted.append(current)
    return fitted


def draw_paragraph(pen, origin, body, face_font, colour, width, spacing=1.18):
    """Draw wrapped text starting at origin; return the y below it."""
    x, y = origin
    gap = int(face_font.size * spacing)
    for row in fit_words(pen, body, face_font, width):
        pen.text((x, y), row, font=face_font, fill=colour)
        y += gap
    return y


def draw_centred(pen, middle, top, body, face_font, colour):
    span = pen.textlength(body, font=face_font)
    pen.text((middle - span / 2, top), body, font=face_font, fill=colour)


canvas = Image.new("RGB", (SIDE, SIDE), PALETTE["paper"])
pen = ImageDraw.Draw(canvas)


def masthead():
    draw_centred(pen, SIDE / 2, 26, "THE WORLD TODAY",
                 load_font("serif_b", 74), PALETTE["ink"])
    pen.line([(MARGIN, 118), (RIGHT, 118)], fill=PALETTE["ink"], width=3)
    pen.line([(MARGIN, 124), (RIGHT, 124)], fill=PALETTE["ink"], width=1)
    draw_centred(pen, SIDE / 2, 136, "TUESDAY 24 NOVEMBER 2026",
                 load_font("sans_b", 41), PALETTE["red"])
    draw_centred(pen, SIDE / 2, 188, "THE DAY'S WORLD NEWS IN ONE IMAGE",
                 load_font("sans", 19), PALETTE["grey"])
    pen.line([(MARGIN, 222), (RIGHT, 222)], fill=PALETTE["ink"], width=2)


LEAD_TOP, LEAD_BOTTOM = 238, 486
LEAD_TEXT_X = 396
LEAD_TEXT_W = RIGHT - LEAD_TEXT_X - 24


def lead_story():
    pen.rectangle([MARGIN, LEAD_TOP, RIGHT, LEAD_BOTTOM],
                  outline=PALETTE["ink"], width=2)
    # pictogram: a warship listing and sinking off Libya, a naval
    # drone above it, waves below, stamped SUNK
    pen.text((66, 258), "OFF LIBYA", font=load_font("sans_b", 19),
             fill=PALETTE["navy"])
    # sea
    for crest in (66, 130, 194, 258):
        pen.arc([crest, 396, crest + 64, 428], start=0, end=180,
                fill=PALETTE["navy"], width=3)
    # listing hull
    pen.polygon([(84, 340), (300, 372), (282, 396), (96, 372)],
                fill=PALETTE["steel"], outline=PALETTE["ink"])
    pen.rectangle([150, 322, 190, 348], fill=PALETTE["navy"])
    pen.line([(170, 296), (170, 322)], fill=PALETTE["ink"], width=3)
    pen.line([(170, 296), (196, 306)], fill=PALETTE["red"], width=3)
    # smoke from the ship (below the kicker, above the hull)
    pen.ellipse([112, 302, 140, 328], fill=PALETTE["grey"])
    pen.ellipse([96, 318, 122, 342], fill=PALETTE["grey"])
    # naval drone above
    pen.ellipse([292, 276, 308, 290], fill=PALETTE["ink"])
    pen.line([(300, 290), (300, 302)], fill=PALETTE["ink"], width=2)
    pen.line([(288, 296), (312, 296)], fill=PALETTE["ink"], width=2)
    pen.rectangle([258, 420, 360, 452], fill=PALETTE["red"])
    pen.text((268, 426), "SUNK", font=load_font("sans_b", 22),
             fill=PALETTE["white"])
    # lead words
    pen.text((LEAD_TEXT_X, 256), "BENGHAZI, LIBYA",
             font=load_font("sans_b", 19), fill=PALETTE["red"])
    after_head = draw_paragraph(
        pen, (LEAD_TEXT_X, 284), "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
        load_font("serif_b", 36), PALETTE["ink"], LEAD_TEXT_W, spacing=1.12)
    draw_paragraph(
        pen, (LEAD_TEXT_X, after_head + 8),
        "Sea drones sank the corvette Merkury at the Benghazi "
        "naval base on 23 Nov. Libya demands answers; the UN "
        "seeks a probe.",
        load_font("serif", 22), PALETTE["grey"], LEAD_TEXT_W, spacing=1.25)


PANEL_W, PANEL_H = 466, 148


def story_panel(left, top, kicker, headline, sub, painter):
    pen.rectangle([left, top, left + PANEL_W, top + PANEL_H],
                  outline=PALETTE["ink"], width=2)
    pen.text((left + 14, top + 9), kicker, font=load_font("sans_b", 15),
             fill=PALETTE["red"])
    painter(left + 14, top + 33)
    draw_paragraph(pen, (left + 120, top + 31), headline,
                   load_font("serif_b", 26), PALETTE["ink"],
                   PANEL_W - 134, spacing=1.12)
    pen.text((left + 120, top + 122), sub, font=load_font("sans", 15),
             fill=PALETTE["grey"])


def paint_jet(x, y):
    # a jet crossing a radar sweep, with a warning triangle
    pen.ellipse([x + 6, y + 8, x + 86, y + 88], outline=PALETTE["steel"],
                width=2)
    pen.line([(x + 46, y + 48), (x + 82, y + 12)], fill=PALETTE["steel"],
             width=2)
    pen.polygon([(x + 10, y + 44), (x + 62, y + 28), (x + 70, y + 36),
                 (x + 26, y + 56)], fill=PALETTE["navy"])
    pen.polygon([(x + 44, y + 30), (x + 58, y + 18), (x + 60, y + 30)],
                fill=PALETTE["navy"])
    pen.polygon([(x + 66, y + 62), (x + 84, y + 84), (x + 52, y + 84)],
                fill=PALETTE["gold"], outline=PALETTE["ink"], width=2)
    pen.text((x + 71, y + 68), "!", font=load_font("sans_b", 16),
             fill=PALETTE["ink"])


def paint_scales(x, y):
    # scales of justice
    pen.line([(x + 50, y + 6), (x + 50, y + 82)], fill=PALETTE["ink"],
             width=3)
    pen.line([(x + 14, y + 18), (x + 86, y + 18)], fill=PALETTE["ink"],
             width=3)
    pen.line([(x + 14, y + 18), (x + 14, y + 44)], fill=PALETTE["ink"],
             width=2)
    pen.line([(x + 86, y + 18), (x + 86, y + 44)], fill=PALETTE["ink"],
             width=2)
    pen.pieslice([x + 2, y + 44, x + 26, y + 62], start=0, end=180,
                 fill=PALETTE["gold"], outline=PALETTE["ink"], width=2)
    pen.pieslice([x + 74, y + 44, x + 98, y + 62], start=0, end=180,
                 fill=PALETTE["gold"], outline=PALETTE["ink"], width=2)
    pen.line([(x + 42, y + 6), (x + 58, y + 6)], fill=PALETTE["ink"],
             width=3)


def paint_chart(x, y):
    # a rising market chart with an arrowhead
    pen.line([(x + 8, y + 84), (x + 8, y + 8)], fill=PALETTE["ink"],
             width=2)
    pen.line([(x + 8, y + 84), (x + 96, y + 84)], fill=PALETTE["ink"],
             width=2)
    trend = [(x + 12, y + 70), (x + 32, y + 62), (x + 52, y + 66),
             (x + 72, y + 38), (x + 90, y + 18)]
    pen.line(trend, fill=PALETTE["green"], width=4)
    pen.polygon([(x + 90, y + 18), (x + 78, y + 20), (x + 86, y + 32)],
                fill=PALETTE["green"])


def paint_bank(x, y):
    # a bank / exchange house: pediment, columns, dollar sign
    pen.polygon([(x + 8, y + 22), (x + 52, y + 2), (x + 96, y + 22)],
                fill=PALETTE["white"], outline=PALETTE["ink"], width=2)
    pen.rectangle([x + 8, y + 26, x + 96, y + 34], fill=PALETTE["white"],
                  outline=PALETTE["ink"], width=2)
    for column in (x + 16, x + 38, x + 60, x + 82):
        pen.line([(column, y + 36), (column, y + 78)], fill=PALETTE["ink"],
                 width=3)
    pen.line([(x + 8, y + 80), (x + 96, y + 80)], fill=PALETTE["ink"],
             width=3)
    pen.text((x + 42, y + 44), "$", font=load_font("sans_b", 26),
             fill=PALETTE["red"])


STORIES = [
    (36, 500, "NATO - AIRSPACE", "RUSSIA TESTS NATO SKIES",
     "25 violations in 2026, 4x the 2024 total", paint_jet),
    (522, 500, "THE HAGUE - JUSTICE", "14 NATIONS BACK ICJ ROHINGYA RULING",
     "UK, Spain, Canada, Australia + 10 more", paint_scales),
    (36, 660, "MARKETS - STOCKS", "STOCKS SURGE AS NVIDIA REINSTATES HUANG",
     "Kospi +6-7%, Nikkei +3.9%, Nasdaq +6.5%", paint_chart),
    (522, 660, "WASHINGTON - SANCTIONS", "US SANCTIONS DOZENS OF IRAN EXCHANGE HOUSES",
     "Hormuz tension; Tehran sets 7 conditions", paint_bank),
]


STRIP_TOP, STRIP_BOTTOM = 820, 900


def guarantee_strip():
    pen.rectangle([MARGIN, STRIP_TOP, RIGHT, STRIP_BOTTOM],
                  fill=PALETTE["navy"])
    # a shield pictogram
    pen.polygon([(106, STRIP_TOP + 14), (142, STRIP_TOP + 14),
                 (142, STRIP_TOP + 48), (124, STRIP_TOP + 66),
                 (106, STRIP_TOP + 48)], fill=PALETTE["white"],
                outline=PALETTE["sand"], width=2)
    pen.text((120, STRIP_TOP + 26), "5", font=load_font("sans_b", 22),
             fill=PALETTE["navy"])
    pen.text((164, STRIP_TOP + 12),
             "PUTIN OPEN TO ARTICLE 5-STYLE GUARANTEES",
             font=load_font("serif_b", 24), fill=PALETTE["white"])
    pen.text((164, STRIP_TOP + 50),
             "for Ukraine, if no NATO troops deploy - missiles and a drone fell in Poland",
             font=load_font("sans_b", 19), fill=PALETTE["sand"])


def also_today():
    pen.line([(MARGIN, 914), (RIGHT, 914)], fill=PALETTE["ink"], width=2)
    pen.text((MARGIN, 922), "ALSO TODAY", font=load_font("sans_b", 19),
             fill=PALETTE["red"])
    draw_paragraph(
        pen, (MARGIN, 948),
        "COP31 collapsed in Antalya over fossil-fuel wording - "
        "first failure since 2009; COP32 to Addis Ababa - "
        "Nepal quake 5.6 near the China border - factory fire "
        "in Cikande, Indonesia, with casualties - 9th measles "
        "death in Pennsylvania",
        load_font("serif", 18), PALETTE["ink"], SIDE - 2 * MARGIN,
        spacing=1.15)


masthead()
lead_story()
for left, top, kicker, headline, sub, painter in STORIES:
    story_panel(left, top, kicker, headline, sub, painter)
guarantee_strip()
also_today()

canvas.save("art.jpg", quality=88)
print("wrote art.jpg", canvas.size)
