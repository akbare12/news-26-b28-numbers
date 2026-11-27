#!/usr/bin/env python3
"""news-26 b28 — layout V26: heroes stacked LEFT 45%, cards 2x5 RIGHT 55%
top, bottom band full-width (map 40% + ALSO 3 cols 60%). 50 stories.
Render with PIL at build time. main.py copies this output stdlib-only.
"""
import hashlib
import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_R = lambda s: font("DejaVuSans.ttf", s)

PAPER = (247, 243, 232)
INK = (20, 20, 20)
MUT = (90, 86, 76)
RED = (176, 30, 36)
BLUE = (29, 78, 137)
GOLD = (176, 132, 24)
LINE = (180, 172, 150)
CARD_BG = (255, 255, 255)
HERO_BG = (255, 255, 255)
SEA = (198, 222, 232)
LAND = (226, 214, 178)

STOP = set("""the a an of to in on at for and as by with after over from its is
are was be up down no per off near into set hit hits say says than then
all two one first new us""".split())

def tokens(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)  # drop [C]/[CL] tags before comparing
    return [t for t in re.findall(r"[a-z0-9]+", s.lower())
            if t not in STOP and len(t) >= 2]

def wrap(draw, text, fnt, maxw):
    """Greedy wrap; returns list of lines, each measured to fit maxw."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        assert draw.textlength(ln, font=fnt) <= maxw, f"LINE TOO WIDE: {ln!r}"
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)

# ---------------------------------------------------------------- data
HEROES = [
    dict(city="NEW YORK", tag="[C]", num="1",
         head="MACY'S 100TH PARADE POSTPONED",
         deck="A huge East Coast storm forces the first weather delay in the "
              "parade's 100-year history.",
         why="Thanksgiving's most iconic parade, in its centenary year, is "
             "delayed for the first time ever by weather, not war.",
         stat="100TH PARADE  ·  FIRST WEATHER DELAY EVER  ·  SAT 28 NOV 08:30 ET",
         art="parade"),
    dict(city="HORMUZ", tag="[CL]", num="2",
         head="IRGC CLAIMS 2 TANKERS HIT BY MINES",
         deck="Iran's Revolutionary Guard says two tankers, one a supertanker "
              "carrying over 2M barrels, exploded and burned near Khasab. "
              "The claim is unverified.",
         why="The claim lands as the Iran war widens at sea, pushing oil "
             "higher and putting the world's busiest oil chokepoint on edge.",
         stat="2M BARRELS  ·  2 TANKERS CLAIMED  ·  BRENT +0.9% THU",
         art="tanker"),
    dict(city="GLOBAL MARKETS", tag="[C]", num="3",
         head="TRUMP TARIFFS: MARKETS REBOUND",
         deck="Europe and Asia rally as the new tariff salvo on 14 partners "
              "looks milder than feared and will not stack on July tariffs.",
         why="The market verdict softens the biggest trade shock of the year, "
             "with China facing the top rate of 20%.",
         stat="14 PARTNERS  ·  STOXX +1.6%  ·  20% CHINA",
         art="market"),
]

CARDS = [
    ("GAZA", "[C]", "Hamas education deputy killed in Gaza strike",
     "Israeli strike on a Deir al-Balah flat kills Hamas deputy education "
     "minister Khaled Abu Nada and his wife; 9 Palestinians killed overnight."),
    ("KYIV", "[C]", "Russian missiles hit Kyiv mall; 7 wounded",
     "Ballistic missiles and 113 drones hit Kyiv overnight; a mall in the "
     "Desnianskyi district is struck and 7 are wounded."),
    ("BOGOR", "[C]", "Flooded illegal gold mine: 13 dead, 13 missing",
     "An illegal gold mine floods in Bogor, Indonesia; 13 dead and 13 missing "
     "about 100 metres underground after heavy rain."),
    ("JERUSALEM", "[C]", "Judge urges bribery charge against Netanyahu dropped",
     "A judge urges prosecutors to drop Case 4000, the only bribery charge "
     "against PM Benjamin Netanyahu."),
    ("PYONGYANG", "[C]", "Kim tours nuclear plant, pushes tactical nukes",
     "Kim Jong Un tours a nuclear-material plant and urges wider use of "
     "tactical nuclear weapons."),
    ("WASHINGTON", "[C]", "FCC clears SpaceX 1M-satellite data centres",
     "The FCC clears SpaceX to launch up to 1M orbital data-centre satellites, "
     "approved Nov 25; a first US approval of its kind."),
    ("LONDON", "[C]", "UK net migration falls to 77,000",
     "UK net migration falls to 77,000 in the year to June 2026, the lowest "
     "since 1997 outside the pandemic."),
    ("MOSCOW", "[C]", "Russia approves record post-Soviet military budget",
     "Russia approves a record post-Soviet military budget as the war in "
     "Ukraine grinds on."),
    ("BANGKOK", "[C]", "Blast at Bangkok oil depot injures 7",
     "A blast at a Bangkok oil depot injures 7 and triggers evacuation "
     "warnings; the fire is controlled in about 30 minutes."),
    ("COLOGNE", "[C]", "2 held over plot to attack synagogue",
     "Germany arrests 2 Iraqi suspects in Cologne and Heidelberg over a plot "
     "to attack a synagogue."),
]

ALSO = [
    "Philadelphia parade cancelled over weather [C]",
    "NBC airs 2025 parade Thu; 2026 live on Sat [C]",
    "Mamdani to miss Sat parade after foot surgery [C]",
    "Balloons inflated Wed, then deflated again [C]",
    "UKMTO: blast near tanker off Dubai, crew safe [C]",
    "Tanker hit 18 nm off Khasab, 25 Nov [C]",
    "Houthis claim Ras Tanura refinery strike, 25 Nov [CL]",
    "Saudi air defence downs 2 missiles bound for Riyadh, 25 Nov [C]",
    "OPEC+ meets 29 Nov on 2027 output [C]",
    "Brent $93.8 Thu; WTI $83.32 [C]",
    "Gold $3,572/oz, down 8% in a month [C]",
    "Nvidia ends -3.91% at $149.30 [C]",
    "S&P futures +0.5%; Wall St shut for Thanksgiving [C]",
    "MSCI global index +0.4% Thu [C]",
    "Dollar flat at 103.71 [C]",
    "Eisenkot clinches first Israeli coalition deal [C]",
    "Merz warns Russia's ambitions go beyond Ukraine [C]",
    "UK on alert over drone threat to airbases [C]",
    "Norse Atlantic suspends all flights, warns of bankruptcy [C]",
    "Poundland enters administration; 11,000 jobs at risk [C]",
    "Malaysia sues Google for $146m over harmful content [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Belarus offers to fly Zelensky to Moscow; he refuses [C]",
    "Kushner calls Putin a \u201cgrandmaster of politics\u201d [C]",
    "Estonia decides to close its border [C]",
    "Copernicus confirms longest stretch above 2\u00b0C warming [C]",
    "Nvidia halts AI server shipments to 4 countries [C]",
    "US bitcoin funds hit record $4.94bn [C]",
    "UN rights chief warns of atrocity-crime risk in Gaza [C]",
    "Ukraine drones damage 5 jets at Savasleyka base [C]",
    "Ukraine hits pump station 1,300 km inside Russia [C]",
    "Kharkiv couple aged 37 and 38 die in apartment hit [C]",
    "18 wounded in Kryvyi Rih strike [C]",
    "NYC gusts to 60 mph; wind warning from 10:00 Thu [C]",
    "Balloons grounded if sustained wind tops 23 mph [C]",
    "Tariff hearing set 25 Jan; in force Feb/Mar [C]",
    "IRGC claim names no ships, flags or casualties [CL]",
]

TOTAL = len(HEROES) + len(CARDS) + len(ALSO)
assert TOTAL == 50, f"TOTAL stories {TOTAL} != 50"
assert len(ALSO) == 37, f"ALSO {len(ALSO)} != 37"

# ------------------------------------------------------- duplicate scan
def dup_scan():
    items = []
    for h in HEROES:
        items.append(("hero" + h["num"], h["head"] + " " + h["deck"] + " "
                      + h["why"] + " " + h["stat"]))
    for i, (c, _t, hd, dk) in enumerate(CARDS):
        items.append((f"card{i+1}", c + " " + hd + " " + dk))
    for i, a in enumerate(ALSO):
        items.append((f"also{i+1}", a))
    flags = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            shared = set(tokens(items[i][1])) & set(tokens(items[j][1]))
            if len(shared) >= 3:
                flags.append((items[i][0], items[j][0], sorted(shared)))
    return flags

# ------------------------------------------------------------ hero art
def hero_art(kind, w, h):
    """Art drawn on its own layer exactly box-sized, then pasted."""
    layer = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(layer)
    if kind == "parade":
        for y in range(h):  # storm sky
            t = y / max(h - 1, 1)
            d.line([(0, y), (w, y)], fill=(int(70 + 60 * t), int(90 + 70 * t),
                                            int(120 + 80 * t)))
        d.rectangle([0, h - 26, w, h], fill=(52, 52, 58))  # street
        for bx in range(30, w - 20, 46):  # skyline
            bh = 26 + ((bx * 7) % 30)
            d.rectangle([bx, h - 26 - bh, bx + 34, h - 26], fill=(38, 40, 48))
        # giant balloons, netted
        d.ellipse([28, 6, 108, 52], fill=(176, 30, 36))
        d.ellipse([120, 2, 196, 46], fill=(232, 176, 40))
        d.ellipse([206, 8, 268, 50], fill=(29, 78, 137))
        for x in range(0, w, 14):  # net
            d.line([(x, 0), (x, 58)], fill=(240, 240, 230), width=1)
        for x in range(0, w, 12):  # rain
            d.line([(x, 60), (x - 5, h - 28)], fill=(210, 220, 235), width=1)
        d.text((w - 118, h - 24), "100TH", font=F_B(13), fill=(255, 255, 255))
    elif kind == "tanker":
        for y in range(h):  # dusk sea sky
            t = y / max(h - 1, 1)
            d.line([(0, y), (w, y)], fill=(int(200 - 90 * t), int(120 - 20 * t),
                                            int(60 + 40 * t)))
        d.rectangle([0, h - 34, w, h], fill=(24, 52, 72))  # sea
        d.rectangle([52, h - 62, 268, h - 34], fill=(28, 28, 30))  # hull
        d.rectangle([210, h - 84, 244, h - 62], fill=(200, 60, 30))
        d.rectangle([60, h - 84, 96, h - 62], fill=(60, 60, 64))
        for fx, fy, r, c in [(150, 18, 20, (255, 190, 40)),
                             (168, 30, 13, (255, 110, 20)),
                             (136, 32, 10, (255, 220, 90))]:
            d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=c)
        for mx, my in [(300, 22), (322, 34), (288, 40)]:  # mines
            d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 20, 20))
            d.line([(mx - 10, my), (mx + 10, my)], fill=(20, 20, 20), width=2)
            d.line([(mx, my - 10), (mx, my + 10)], fill=(20, 20, 20), width=2)
        d.text((10, h - 30), "2M BARRELS", font=F_B(13), fill=(255, 255, 255))
    else:  # market
        d.rectangle([0, 0, w, h], fill=(16, 42, 66))
        for i, (gx, gh, c) in enumerate([(20, 26, (90, 140, 190)),
                                         (52, 40, (90, 140, 190)),
                                         (84, 30, (90, 140, 190)),
                                         (116, 52, (120, 170, 210)),
                                         (148, 44, (120, 170, 210))]):
            d.rectangle([gx, h - 18 - gh, gx + 24, h - 18], fill=c)
        pts = [(10, h - 30), (70, h - 52), (130, h - 40), (190, h - 62),
               (250, h - 70), (310, h - 44)]
        d.line(pts, fill=(255, 190, 40), width=4)
        for px, py in pts:
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 220, 90))
        d.rectangle([250, 6, 306, 22], fill=(176, 30, 36))
        d.text((254, 7), "+1.6%", font=F_B(11), fill=(255, 255, 255))
    return layer

def card_strip(i, w, h):
    """Small art strip for a card, drawn on its own layer."""
    layer = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(layer)
    palette = [(29, 78, 137), (176, 30, 36), (24, 110, 70), (120, 70, 140),
               (176, 132, 24), (40, 90, 110), (90, 60, 30), (70, 70, 90),
               (150, 60, 20), (30, 100, 90)]
    base = palette[i % len(palette)]
    d.rectangle([0, 0, w, h], fill=base)
    for k in range(6):  # skyline ticks
        bx = 8 + k * (w // 6)
        d.rectangle([bx, h - 10 - (k % 3) * 4, bx + 10, h - 8], fill=(255, 255, 255))
    d.ellipse([w - 30, 3, w - 8, 25], fill=(255, 220, 90))
    return layer

# ------------------------------------------------------------- world map
# rough equirectangular continent outlines (lon, lat)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-117, 33), (-125, 49), (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -8), (-35, -18), (-45, -28),
     (-55, -35), (-65, -45), (-70, -55), (-75, -40), (-80, -20), (-80, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 55), (12, 58), (20, 60),
     (28, 60), (30, 55), (28, 45), (20, 40), (12, 38), (3, 38), (-10, 36)],
    [(-6, 35), (10, 37), (20, 32), (32, 31), (43, 12), (51, 11), (48, 0),
     (40, -10), (35, -20), (28, -33), (18, -35), (12, -18), (8, 4),
     (-8, 5), (-17, 15), (-6, 35)],
    [(30, 70), (50, 70), (70, 73), (100, 76), (140, 72), (170, 66),
     (162, 60), (158, 52), (140, 40), (127, 38), (120, 30), (108, 12),
     (100, 8), (92, 16), (80, 8), (72, 20), (60, 25), (48, 29), (43, 36),
     (30, 36), (30, 70)],
    [(114, -22), (124, -14), (136, -12), (142, -11), (150, -23), (153, -28),
     (146, -39), (140, -38), (130, -32), (116, -35), (114, -22)],
]
# (label, lon, lat, nudge dx, dy)
PINS = [
    ("1 NYC", -74, 40.7, 0, -8), ("2 HORMUZ", 56.2, 26.2, 0, 8),
    ("3 WASHINGTON", -77, 38.9, -14, 10), ("4 GAZA", 34.5, 31.5, 0, -10),
    ("5 KYIV", 30.5, 50.4, 8, -8), ("6 BOGOR", 106.8, -6.6, 0, 8),
    ("7 JERUSALEM", 35.2, 31.8, 12, 8), ("8 PYONGYANG", 125.8, 39.0, -30, -8),
    ("9 LONDON", -0.1, 51.5, -10, -8), ("10 MOSCOW", 37.6, 55.8, 0, -8),
    ("11 BANGKOK", 100.5, 13.8, 0, 8), ("12 COLOGNE", 7.0, 50.9, 12, 6),
]

def draw_map(d, x0, y0, mw, mh):
    d.rectangle([x0, y0, x0 + mw, y0 + mh], fill=SEA, outline=LINE)
    def px(lon, lat):
        return (x0 + (lon + 180) / 360.0 * mw,
                y0 + (75 - lat) / 130.0 * mh)
    for poly in CONTINENTS:
        d.polygon([px(lo, la) for lo, la in poly], fill=LAND,
                  outline=(150, 135, 100))
    for label, lon, lat, dx, dy in PINS:
        px0, py0 = px(lon, lat)
        lx, ly = px0 + dx, py0 + dy
        if dx or dy:
            d.line([(px0, py0), (lx, ly)], fill=INK, width=1)
        d.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=RED,
                  outline=(255, 255, 255))
        d.text((lx + 6, ly - 5), label, font=F_B(8), fill=INK)

# ---------------------------------------------------------------- render
def main():
    flags = dup_scan()
    assert not flags, f"DUPLICATE FLAGS: {flags}"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead y 0-48
    d.rectangle([0, 0, W, 48], fill=(20, 20, 20))
    d.text((10, 4), "THE WORLD IN ONE PAGE", font=F_SERIF_B(24), fill=(247, 243, 232))
    d.text((10, 31), "THURSDAY 26 NOVEMBER 2026", font=F_B(11), fill=(232, 176, 40))
    badge = "50 STORIES"
    bw = text_w(d, badge, F_B(14)) + 18
    d.rectangle([W - 10 - bw, 10, W - 10, 32], fill=RED)
    d.text((W - 10 - bw + 9, 13), badge, font=F_B(14), fill=(255, 255, 255))
    d.text((W - 10 - bw - 8 - text_w(d, "MAKE.FUN DAILY IMAGE", F_B(10)),
            15), "MAKE.FUN DAILY IMAGE", font=F_B(10), fill=(180, 180, 170))

    # ---- date check strip y 48-76 (2 lines)
    d.rectangle([0, 48, W, 76], fill=(232, 224, 200))
    dc1 = "DATE CHECK: Every story below is verified for Thu 26 Nov 2026."
    dc2 = "Events from 25 Nov are dated in the text.  [C] = confirmed  ·  [CL] = claim, not independently confirmed"
    assert text_w(d, dc1, F_B(12)) <= W - 20 and text_w(d, dc2, F_R(11)) <= W - 20
    d.text((10, 50), dc1, font=F_B(12), fill=INK)
    d.text((10, 64), dc2, font=F_R(11), fill=MUT)

    # ---- main zone y 76-628: heroes left x8-460, cards right x468-1016
    LX, LW = 8, 452
    RX, RW = 468, 548
    HY, HH, HGAP = 76, 180, 6
    for i, h in enumerate(HEROES):
        y0 = HY + i * (HH + HGAP)
        d.rectangle([LX, y0, LX + LW, y0 + HH], fill=HERO_BG, outline=LINE)
        art = hero_art(h["art"], LW - 2, 66)
        img.paste(art, (LX + 1, y0 + 1))
        # number badge circle, solid, on the art band
        cx, cy = LX + 18, y0 + 16
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)
        d.text((cx - 4, cy - 8), h["num"], font=F_B(13), fill=(255, 255, 255))
        tx = LX + 10
        by = y0 + 70
        city = h["city"] + "  " + h["tag"]
        assert text_w(d, city, F_B(11)) <= LW - 20
        d.text((tx, by), city, font=F_B(11), fill=RED)
        head = wrap(d, h["head"], F_B(16), LW - 20)
        assert len(head) <= 1, f"hero head too long: {head}"
        by = draw_lines(d, head, tx, by + 13, F_B(16), INK, 17)
        deck = wrap(d, h["deck"], F_R(11), LW - 20)
        assert len(deck) <= 2, f"hero deck too long: {deck}"
        by = draw_lines(d, deck, tx, by + 2, F_R(11), INK, 13)
        why = wrap(d, "WHY IT MATTERS: " + h["why"], F_R(10), LW - 20)
        assert len(why) <= 2, f"hero why too long: {why}"
        why_bottom = draw_lines(d, why, tx, by + 2, F_R(10), MUT, 11)
        stat_top = y0 + HH - 20
        assert stat_top - why_bottom >= 6, (
            f"hero {h['num']} why/stat gap {stat_top - why_bottom}")
        d.rectangle([LX + 1, stat_top - 2, LX + LW - 1, y0 + HH - 1],
                    fill=(20, 20, 20))
        st = h["stat"]
        assert text_w(d, st, F_B(10)) <= LW - 16, f"hero stat too wide: {st}"
        d.text((tx, stat_top + 2), st, font=F_B(10), fill=(232, 176, 40))

    # ---- cards 2x5, right column
    CW = (RW - 6) // 2
    CHH, CGAP = 106, 5
    for i, (city, tag, head, deck) in enumerate(CARDS):
        r, c = divmod(i, 2)
        x0 = RX + c * (CW + 6)
        y0 = HY + r * (CHH + CGAP)
        d.rectangle([x0, y0, x0 + CW, y0 + CHH], fill=CARD_BG, outline=LINE)
        strip = card_strip(i, CW - 2, 24)
        img.paste(strip, (x0 + 1, y0 + 1))
        nx = x0 + 14
        d.ellipse([nx - 11, y0 + 13, nx + 11, y0 + 35], fill=BLUE)
        d.text((nx - 4, y0 + 16), str(i + 1), font=F_B(12),
               fill=(255, 255, 255))
        lab = city + "  " + tag
        assert text_w(d, lab, F_B(10)) <= CW - 40, f"card label wide: {lab}"
        d.text((x0 + 30, y0 + 17), lab, font=F_B(10), fill=RED)
        hl = wrap(d, head, F_B(12), CW - 16)
        assert len(hl) <= 2, f"card head too long: {hl}"
        cy = draw_lines(d, hl, x0 + 8, y0 + 40, F_B(12), INK, 13)
        dk = wrap(d, deck, F_R(10), CW - 16)
        assert len(dk) <= 3, f"card deck too long: {dk}"
        dend = draw_lines(d, dk, x0 + 8, cy + 2, F_R(10), MUT, 11)
        assert dend <= y0 + CHH - 2, f"card {i+1} overflow"

    # ---- bottom band y 634-995: map left 40%, ALSO right 60%
    BY0, BY1 = 634, 995
    d.rectangle([0, BY0 - 4, W, BY0 - 4], fill=LINE)
    MX, MW = 8, 396
    d.text((MX, BY0), "WORLD MAP  ·  WHERE IT HAPPENED", font=F_B(12), fill=INK)
    draw_map(d, MX, BY0 + 20, MW, 250)
    leg = ["1 NYC  2 HORMUZ  3 WASHINGTON  4 GAZA  5 KYIV  6 BOGOR",
           "7 JERUSALEM  8 PYONGYANG  9 LONDON  10 MOSCOW  11 BANGKOK",
           "12 COLOGNE"]
    ly = BY0 + 276
    for ln in leg:
        assert text_w(d, ln, F_R(10)) <= MW
        d.text((MX, ly), ln, font=F_R(10), fill=MUT)
        ly += 13

    AX, AW = 412, 604
    d.text((AX, BY0), "ALSO TODAY  ·  37 MORE STORIES", font=F_B(12), fill=INK)
    d.line([(AX, BY0 + 17), (AX + AW, BY0 + 17)], fill=RED, width=2)
    colw = (AW - 12) // 3
    cols = [ALSO[0:13], ALSO[13:25], ALSO[25:37]]
    for ci, col in enumerate(cols):
        cx = AX + ci * (colw + 6)
        iy = BY0 + 24
        for j, item in enumerate(col):
            n = ci * 13 + j + 1 if ci == 0 else (13 + (ci - 1) * 12 + j + 1)
            lines = wrap(d, item, F_R(10), colw)
            assert len(lines) <= 2, f"ALSO too long: {item!r} -> {lines}"
            iy = draw_lines(d, lines, cx, iy, F_R(10), INK, 12)
            iy += 1
        assert iy <= BY1, f"ALSO col {ci} overflow {iy} > {BY1}"

    # ---- timeline strip + footer
    tl = ("25 NOV: Tariffs unveiled  ·  FCC clears Starmind  ·  Ras Tanura hit  "
          ">>  26 NOV: Macy's postponed  ·  IRGC mine claim  ·  Markets rebound  "
          ">>  28 NOV: Parade rescheduled  ·  29 NOV: OPEC+ meets")
    assert text_w(d, tl, F_R(10)) <= W - 20, "timeline too wide"
    d.text((10, 999), tl, font=F_R(10), fill=MUT)
    ft = "Sources: Reuters  ·  AP  ·  BBC  ·  CNN  ·  NPR  ·  UKMTO  ·  ONS  ·  KCNA   |   All stories verified for Thu 26 Nov 2026"
    assert text_w(d, ft, F_R(9)) <= W - 20, "footer too wide"
    d.text((10, 1013), ft, font=F_R(9), fill=MUT)

    img.save(OUT)
    raw = open(OUT, "rb").read()
    print("stories:", TOTAL, "heroes:", len(HEROES), "cards:", len(CARDS),
          "also:", len(ALSO))
    print("size:", img.size, "bytes:", len(raw))
    print("sha256:", hashlib.sha256(raw).hexdigest())

if __name__ == "__main__":
    main()
