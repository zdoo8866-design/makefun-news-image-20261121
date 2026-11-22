#!/usr/bin/env python3
"""Compose entry.png for news-image-20261121: a 1024x1024 newspaper front
page in the style of the competition's winning pages -- masthead, region
tally, the day in numbers, 13 drawn story cards, a where-it-happened map,
21 one-line briefs and a date-check box. Every element is drawn in code;
all type is set programmatically so every word and figure is exact."""
import os
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFont

W = H = 1024
WORK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(WORK, "..", "entry.png")
sys.path.insert(0, WORK)
from worldmap_data import POLYS_HQ

NOTO = "/usr/share/fonts/truetype/noto"
SERIF_B = f"{NOTO}/NotoSerif-Bold.ttf"
SERIF_I = f"{NOTO}/NotoSerif-Italic.ttf"
SANS_B = f"{NOTO}/NotoSans-Bold.ttf"
SANS_SB = f"{NOTO}/NotoSans-SemiBold.ttf"
SANS_R = f"{NOTO}/NotoSans-Regular.ttf"
SANS_I = f"{NOTO}/NotoSans-Italic.ttf"

PAPER = (243, 234, 214)
INK = (26, 38, 52)
NAVY = (24, 42, 66)
RED = (168, 30, 30)
DARKRED = (142, 26, 26)
SOFT = (88, 94, 92)
CARD = (255, 254, 248)
BORDER = (178, 168, 142)
GOLD = (232, 190, 92)
GREEN = (56, 116, 62)
AMBER = (172, 116, 28)
STEEL = (64, 98, 138)

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def fit(d, text, path, size, maxw, floor=10):
    """Shrink a one-line font until the text fits maxw."""
    while size > floor and d.textlength(text, font=F(path, size)) > maxw:
        size -= 1
    return F(path, size)

def badge(d, cx, cy, r, num, fsize):
    # drawn on a 4x tile and downscaled: a 1x PIL ellipse is visibly
    # pixel-stepped, and these numbered badges sit on every card
    ss = 4
    R = int(round(r * ss)) + ss
    tile = Image.new("RGBA", (R * 2, R * 2), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    rr = r * ss
    td.ellipse([R - rr, R - rr, R + rr, R + rr], fill=RED + (255,))
    td.text((R, R), str(num), font=F(SANS_B, int(fsize * ss)),
            fill=(255, 255, 255, 255), anchor="mm")
    tile = tile.resize((R * 2 // ss, R * 2 // ss), Image.LANCZOS)
    canvas.paste(tile, (int(cx - R // ss), int(cy - R // ss)), tile)

def pill(d, x, y, label):
    f = F(SANS_B, 8)
    w = d.textlength(label, font=f) + 10
    col = {"REPORTED": GREEN, "CLAIM": AMBER, "FORECAST": STEEL}[label]
    d.rounded_rectangle([x, y, x + w, y + 12], 3, fill=col)
    d.text((x + 5, y + 1), label, font=f, fill=(255, 255, 255))
    return w

# ---------------------------------------------------------------- data ----
REGIONS = [  # (label, count, colour) -- real tally of the 34 stories
    ("EUROPE", 9, (43, 92, 140)),
    ("ASIA", 8, (176, 62, 40)),
    ("MIDDLE EAST", 7, (146, 118, 56)),
    ("AMERICAS", 5, (104, 74, 132)),
    ("OCEANIA", 2, (46, 118, 112)),
    ("AFRICA", 2, (86, 128, 64)),
    ("GLOBAL", 1, (58, 58, 58)),
]

STATS = [  # (big, caption)
    ("-10%", "Nasdaq's fall this week — its worst since March 2020"),
    ("$4tn", "of US stock value wiped out in the AI rout"),
    ("M6.8", "earthquake in the Banda Sea; felt in Darwin"),
    ("128", "nations to draft killer-robot rules in Geneva"),
    ("800 MW", "Basra power plant knocked offline by fire"),
    ("146", "people evacuated safely from flight PX19"),
]

HEROES = [
    dict(n=1, scene="markets", loc="NEW YORK", cat="MARKETS",
         bl="WALL STREET · NEW YORK", br="AI ROUT", tag="REPORTED",
         head="AI sell-off turns into a rout",
         body="Nasdaq's worst week since 2020: the index fell 10% as the "
              "S&P 500 slid 3.7% into correction. Nvidia tumbled 14% on "
              "a reported accounting probe.",
         src="Bloomberg · Reuters · WSJ"),
    dict(n=2, scene="geneva", loc="GENEVA", cat="ARMS CONTROL",
         bl="UN CONFERENCE · GENEVA", br="128 NATIONS", tag="REPORTED",
         head="\u2018Killer robot\u2019 talks end with a path, no pact",
         body="Talks run past 4 a.m.: 128 states agree to spend two years "
              "drafting rules for lethal autonomous weapons. Whether "
              "they will bind is left open.",
         src="Reuters · AFP"),
    dict(n=3, scene="hormuz", loc="STRAIT OF HORMUZ", cat="SECURITY",
         bl="OFF KHASAB · OMAN", br="2 TANKERS HIT", tag="REPORTED",
         head="Two tankers hit in the strait",
         body="A second outbound tanker is struck in its engine room 50 "
              "minutes after the first, off Khasab. No casualties in "
              "either incident, UKMTO says.",
         src="Reuters · UKMTO"),
]

SMALLS = [
    dict(n=4, scene="antalya", loc="ANTALYA", cat="CLIMATE", tag="REPORTED",
         band="COP31 · ANTALYA",
         head="COP31 runs into overtime, still no deal",
         body="Crews pack up as negotiators chase a third draft; "
              "COP32 to Addis Ababa.", src="AP · Reuters"),
    dict(n=5, scene="basra", loc="BASRA", cat="IRAQ", tag="REPORTED",
         band="HARTHA PLANT · BASRA",
         head="Power-station fire kills at least four",
         body="Hartha plant blaze spreads to homes, shuts the "
              "station; 30 injured.", src="Reuters · Al Jazeera"),
    dict(n=6, scene="gaza", loc="GAZA CITY", cat="WAR", tag="REPORTED",
         band="GAZA CITY · AID RUN",
         head="Strike on aid vehicle kills three",
         body="Strike hits car carrying food for World Central "
              "Kitchen, medics say.", src="Reuters"),
    dict(n=7, scene="banda", loc="BANDA SEA", cat="EARTHQUAKE", tag="REPORTED",
         band="BANDA SEA · M6.8",
         head="Magnitude 6.8 quake in the Banda Sea",
         body="Saturday-afternoon tremor 226 km NE of Dili; "
              "shaking felt in Darwin.", src="Reuters · GFZ"),
    dict(n=8, scene="kyiv", loc="KYIV", cat="POLITICS", tag="REPORTED",
         band="KYIV · ZELENSKIY",
         head="Zelenskiy relays Trump\u2019s message to Europe",
         body="Trump told Europe it spends a lot on Ukraine; "
              "Miami talks offered.", src="Reuters"),
    dict(n=9, scene="sinaloa", loc="SINALOA", cat="CRIME", tag="REPORTED",
         band="SINALOA · MEXICO",
         head="Mexico captures drug lord \u2018El Chapo Isidro\u2019",
         body="Soldiers seize Fausto Isidro Meza Flores and two "
              "other cartel leaders.", src="Reuters"),
    dict(n=10, scene="finland", loc="GULF OF FINLAND", cat="SECURITY",
         tag="CLAIM", band="GULF OF FINLAND",
         head="Russian cargo ship struck by drones",
         body="Moscow: Kaliningrad-bound vessel hit by two drones; "
              "Finland sees fire.", src="Reuters"),
    dict(n=11, scene="warsaw", loc="WARSAW", cat="NATO", tag="REPORTED",
         band="WARSAW · NATO",
         head="NATO will defend \u2018every inch\u2019 of Poland",
         body="Warsaw pledge follows Russian missiles, drone "
              "down in Poland Friday.", src="Reuters · PAP"),
    dict(n=12, scene="riemann", loc="CAMBRIDGE, MASS.", cat="SCIENCE",
         tag="REPORTED", band="CAMBRIDGE · RIEMANN",
         head="Race to verify the Riemann claim",
         body="Teams compile the 17m-line Lean proof within "
              "a day; checks go on.", src="Quanta · WSJ"),
    dict(n=13, scene="davao", loc="DAVAO", cat="AVIATION", tag="REPORTED",
         band="DAVAO · PX19",
         head="Everyone walks away from flight PX19",
         body="Hong Kong\u2013Port Moresby 767 diverts on fire "
              "warning; 146 out by slides.", src="AP · CNA"),
]

# (number, place, fact, source) -- the 21 briefs, stories 14-34
BRIEFS = [
    (14, "Port-Vila", "M4.9 quake off Vanuatu at 07:20 UTC", "USGS"),
    (15, "Rome", "Ex-police chief De Gennaro dies at 78", "Reuters"),
    (16, "Moscow", "Wildberries CEO quits after EU sanctions", "Reuters"),
    (17, "Tehran", "China, Russia back Iran nuclear doctrine", "AFP"),
    (18, "Copenhagen", "Denmark: Russian plot to kill rapper", "AP"),
    (19, "Turin", "ATP semis: Alcaraz\u2013Shelton, Zverev\u2013Medvedev", "AP"),
    (20, "Naga City", "Votes open in city-status plebiscite", "GMA"),
    (21, "Manila", "El Ni\u00f1o farm damage passes \u20b110bn", "GMA"),
    (22, "Manila", "Eala a WTA Most Improved nominee", "GMA"),
    (23, "Cox\u2019s Bazar", "UNGA chief to Rohingya: \u2018not alone\u2019", "UN News"),
    (24, "Bridgetown", "AI summit tackles safety gap", "UN News"),
    (25, "New York", "WFP to assist 91m people in 2027", "UN News"),
    (26, "West Bank", "Record settler attacks on olive harvest", "UN News"),
    (27, "Hormuz", "Pugh swims strait for wildlife", "AP"),
    (28, "Kyiv", "Russia hits bridges, rail stations", "BBC"),
    (29, "Gombe", "Soldiers fire on village: 3 dead", "Daily Trust"),
    (30, "W. Kordofan", "Shelter drone strike kills 16", "Radio Tamazuj"),
    (31, "Sydney", "Cummins keeps Test captaincy backing", "AFP"),
    (32, "Mumbai", "India lead NZ at stumps, day 3", "AFP"),
    (33, "Karachi", "Pakistan drop Rizwan, Masood", "AFP"),
    (34, "Washington", "Trump floats chief of staff for 2028", "AFP"),
]

# region of each brief; its number is drawn in the region-bar colour
BRIEF_REGION = {
    14: "OCEANIA", 15: "EUROPE", 16: "EUROPE", 17: "MIDDLE EAST", 18: "EUROPE",
    19: "EUROPE", 20: "ASIA", 21: "ASIA", 22: "ASIA", 23: "ASIA",
    24: "AMERICAS", 25: "AMERICAS", 26: "MIDDLE EAST", 27: "MIDDLE EAST",
    28: "EUROPE", 29: "AFRICA", 30: "AFRICA", 31: "OCEANIA", 32: "ASIA",
    33: "ASIA", 34: "AMERICAS",
}
REGION_COL = {name: col for name, _cnt, col in REGIONS}

# map pins for the 13 cards: (number, lon, lat)
PINS = [
    (1, -74.0, 40.7), (2, 6.1, 46.2), (3, 56.3, 26.2), (4, 30.7, 36.9),
    (5, 47.8, 30.5), (6, 34.3, 31.5), (7, 128.0, -7.0), (8, 30.5, 50.4),
    (9, -107.4, 25.0), (10, 27.5, 59.9), (11, 21.0, 52.2), (12, -71.1, 42.4),
    (13, 125.6, 7.1),
]
# dots for briefs: (lon, lat)
DOTS = [
    (167.0, -17.5), (12.5, 41.9), (37.6, 55.8), (51.4, 35.7), (12.6, 55.7),
    (7.7, 45.1), (123.2, 13.6), (121.0, 14.6), (92.0, 21.4), (-59.6, 13.1),
    (35.2, 31.9), (11.2, 10.3), (28.5, 12.5), (151.2, -33.9), (72.9, 19.1),
    (67.0, 24.9), (-77.0, 38.9), (31.5, 49.5),
]

# coarse continent polygons in (lon, lat) for the dot map
POLYS = [
    # North + Central America
    [(-168, 66), (-158, 71), (-145, 70), (-135, 69), (-125, 72), (-115, 69),
     (-105, 68), (-95, 69), (-88, 67), (-84, 66), (-80, 62), (-78, 58),
     (-72, 56), (-65, 52), (-64, 48), (-68, 45), (-70, 43), (-73, 41),
     (-74, 39), (-76, 36), (-79, 33), (-80, 31), (-81, 28), (-80, 26),
     (-82, 27), (-84, 29), (-87, 30), (-90, 29), (-93, 29), (-96, 28),
     (-97, 26), (-96, 24), (-94, 19), (-92, 15), (-88, 14), (-84, 12),
     (-80, 9), (-78, 8), (-82, 10), (-85, 12), (-88, 14), (-92, 15),
     (-96, 16), (-100, 17), (-103, 19), (-105, 21), (-107, 23), (-110, 24),
     (-112, 27), (-114, 30), (-117, 33), (-120, 35), (-122, 38), (-124, 42),
     (-124, 46), (-127, 50), (-131, 54), (-136, 58), (-145, 60), (-153, 58),
     (-158, 56), (-162, 59), (-166, 61)],
    # Greenland
    [(-45, 60), (-40, 62), (-32, 68), (-22, 70), (-20, 74), (-25, 78),
     (-35, 79), (-50, 77), (-55, 72), (-53, 66), (-50, 62)],
    # South America
    [(-78, 7), (-75, 10), (-70, 12), (-64, 10), (-60, 8), (-55, 6),
     (-51, 4), (-50, 1), (-44, -2), (-37, -5), (-35, -8), (-37, -11),
     (-39, -14), (-40, -19), (-42, -22), (-48, -25), (-52, -29), (-56, -33),
     (-58, -36), (-62, -39), (-63, -41), (-65, -44), (-66, -47),
     (-67, -50), (-68, -53), (-69, -54), (-71, -54), (-73, -51), (-74, -47),
     (-73, -43), (-73, -39), (-72, -33), (-71, -28), (-70, -22), (-70, -18),
     (-73, -15), (-76, -12), (-79, -8), (-80, -5), (-81, -2), (-80, 1),
     (-78, 4)],
    # Africa
    [(-6, 35), (-1, 35), (3, 37), (9, 37), (11, 34), (15, 32), (20, 32),
     (25, 32), (30, 31), (32, 31), (33, 29), (34, 27), (35, 24), (36, 22),
     (38, 20), (39, 17), (40, 15), (42, 12), (43, 12), (46, 11), (49, 11),
     (51, 12), (48, 8), (44, 4), (41, -1), (40, -5), (40, -10), (38, -15),
     (36, -19), (35, -22), (33, -25), (31, -28), (29, -31), (26, -33),
     (21, -34), (19, -34), (17, -32), (16, -29), (15, -26), (14, -21),
     (13, -16), (12, -12), (12, -8), (13, -4), (11, -1), (9, 2), (9, 4),
     (6, 4), (2, 6), (-3, 5), (-7, 4), (-11, 6), (-13, 8), (-15, 10),
     (-17, 12), (-17, 15), (-16, 19), (-16, 23), (-15, 27), (-13, 29),
     (-10, 31), (-8, 33)],
    # Madagascar
    [(44, -13), (47, -13), (50, -16), (49, -19), (47, -22), (45, -25),
     (44, -24), (43, -20), (43, -16)],
    # Eurasia (Europe + Asia in one landmass)
    [(-9, 37), (-9, 43), (-2, 44), (-2, 48), (0, 50), (3, 52), (6, 53),
     (8, 55), (8, 57), (12, 56), (18, 56), (21, 55), (24, 57), (23, 59),
     (25, 61), (28, 64), (30, 66), (35, 67), (45, 68), (58, 69), (70, 70),
     (82, 71), (95, 72), (108, 74), (120, 73), (132, 72), (145, 71),
     (155, 70), (165, 69), (175, 66), (179, 65), (178, 63), (170, 61),
     (162, 59), (159, 55), (156, 51), (150, 50), (144, 49), (141, 48),
     (140, 44), (138, 42), (135, 41), (132, 43), (129, 41), (126, 40),
     (122, 39), (120, 36), (121, 33), (122, 30), (120, 27), (117, 24),
     (113, 22), (109, 20), (108, 17), (108, 14), (107, 11), (105, 8),
     (103, 6), (101, 7), (99, 9), (98, 12), (97, 15), (95, 16), (93, 17),
     (91, 22), (89, 22), (87, 21), (85, 19), (82, 16), (80, 13), (78, 9),
     (77, 8), (76, 10), (74, 13), (72, 18), (70, 21), (68, 23), (66, 25),
     (63, 25), (59, 25), (56, 26), (54, 26), (52, 28), (50, 29), (49, 30),
     (50, 27), (52, 25), (55, 24), (57, 24), (59, 22), (58, 20), (55, 17),
     (53, 16), (50, 15), (48, 14), (45, 12), (43, 12), (42, 14), (41, 16),
     (39, 19), (38, 21), (36, 24), (35, 28), (34, 29), (36, 33), (33, 36),
     (30, 36), (27, 37), (23, 36), (21, 37), (19, 40), (16, 38), (15, 40),
     (12, 42), (10, 44), (8, 44), (6, 43), (3, 42), (0, 39), (-2, 37),
     (-6, 36)],
    # Indonesia / maritime SE Asia (crude single sweep)
    [(95, 5), (100, 0), (104, -4), (108, -6), (112, -6), (116, -7),
     (120, -8), (124, -9), (128, -8), (131, -3), (136, -2), (141, -3),
     (146, -5), (150, -8), (147, -10), (141, -8), (136, -4), (131, -1),
     (126, -1), (120, -1), (116, -3), (110, -2), (104, 1), (99, 3),
     (96, 5)],
    # Philippines (crude)
    [(120, 18), (122, 17), (122, 15), (121, 13), (122, 11), (124, 9),
     (123, 7), (121, 8), (120, 10), (119, 13), (120, 16)],
    # Japan (crude)
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (141, 42),
     (142, 44), (140, 44), (138, 39), (135, 35), (132, 33)],
    # Britain
    [(-5, 50), (-3, 51), (-1, 52), (-1, 54), (-2, 57), (-4, 58), (-6, 57),
     (-5, 55), (-5, 53), (-4, 51)],
    # Australia
    [(113, -22), (114, -26), (115, -31), (117, -34), (119, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (137, -35), (139, -37), (142, -38),
     (145, -38), (147, -38), (149, -37), (150, -35), (151, -33), (153, -30),
     (153, -27), (151, -24), (149, -20), (146, -19), (143, -15), (142, -11),
     (142, -13), (141, -16), (139, -18), (136, -16), (135, -12), (133, -12),
     (130, -13), (127, -14), (124, -16), (122, -17), (119, -19), (117, -20)],
    # New Zealand
    [(167, -45), (169, -43), (171, -42), (173, -41), (174, -39), (176, -38),
     (175, -40), (173, -42), (171, -44), (168, -46)],
]

# ------------------------------------------------------------- scenes -----
def _tile(w, h, bg):
    t = Image.new("RGB", (w, h), bg)
    return t, ImageDraw.Draw(t, "RGBA")
SS = 3

def vgrad(d, w, y0, y1, top, bottom):
    """Vertical gradient band drawn as 1px lines; scenes render at 3x,
    so the steps vanish in the downscale."""
    y0, y1 = int(y0), int(y1)
    span = max(1, y1 - y0)
    for yy in range(y0, y1):
        f = (yy - y0) / span
        col = tuple(int(top[i] + (bottom[i] - top[i]) * f) for i in range(3))
        d.line([(0, yy), (w, yy)], fill=col)

def render_scene(name, w, h):
    """Render a scene at 3x and downscale: smooth edges instead of
    pixel-stepped shapes, plus a whisper of grain so flat fills read
    as print rather than plastic."""
    t = SCENES[name](w * SS, h * SS).resize((w, h), Image.LANCZOS)
    noise = Image.effect_noise((w, h), 5).convert("RGB")
    return ImageChops.add(t, noise, 1, -128)

def sc_markets(w, h):
    t, d = _tile(w, h, (22, 33, 52))
    vgrad(d, w, 0, h, (30, 45, 70), (13, 19, 32))
    # skyline silhouette
    rng = [0.52, 0.66, 0.44, 0.72, 0.58, 0.8, 0.5, 0.64, 0.56, 0.7, 0.47, 0.62]
    bw = w / len(rng)
    for i, f in enumerate(rng):
        x0 = i * bw
        d.rectangle([x0 + 1, h * (1 - f * 0.62), x0 + bw - 1, h], fill=(13, 20, 33))
    # faint windows
    for i in range(26):
        x = (i * 37) % int(w)
        y = h * 0.55 + (i * 23) % int(h * 0.35)
        d.rectangle([x, y, x + 2, y + 3], fill=(240, 205, 110, 160))
    # plunging red line with arrowhead
    pts = [(w * 0.05, h * 0.16), (w * 0.3, h * 0.3), (w * 0.45, h * 0.26),
           (w * 0.62, h * 0.52), (w * 0.78, h * 0.5), (w * 0.94, h * 0.8)]
    d.line(pts, fill=(224, 60, 52), width=max(3, h // 22))
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - w * 0.07, ey - h * 0.02), (ex - w * 0.015, ey - h * 0.11)],
              fill=(224, 60, 52))
    # a few falling candles
    for i, (cx, cy, ln) in enumerate([(0.2, 0.62, 0.16), (0.52, 0.68, 0.2), (0.84, 0.34, 0.14)]):
        d.rectangle([w * cx, h * cy, w * cx + w * 0.035, h * (cy + ln)], fill=(224, 60, 52))
    return t

def sc_geneva(w, h):
    t, d = _tile(w, h, (52, 78, 92))
    vgrad(d, w, 0, h, (64, 92, 108), (40, 62, 76))
    # UN-palace columns behind
    for i in range(6):
        x = w * (0.06 + i * 0.155)
        d.rectangle([x, h * 0.18, x + w * 0.055, h * 0.96], fill=(38, 58, 72))
    d.rectangle([0, h * 0.1, w, h * 0.18], fill=(38, 58, 72))
    # robot head
    cx, cy, s = w * 0.5, h * 0.54, min(w, h)
    d.line([cx, cy - s * 0.34, cx, cy - s * 0.52], fill=(210, 216, 220), width=max(2, h // 30))
    d.ellipse([cx - s * 0.045, cy - s * 0.58, cx + s * 0.045, cy - s * 0.49], fill=(224, 60, 52))
    d.rounded_rectangle([cx - s * 0.3, cy - s * 0.34, cx + s * 0.3, cy + s * 0.3],
                        int(s * 0.09), fill=(196, 204, 210), outline=(140, 150, 158), width=2)
    for ex in (-0.15, 0.15):
        d.ellipse([cx + s * ex - s * 0.055, cy - s * 0.1, cx + s * ex + s * 0.055, cy + s * 0.01],
                  fill=(240, 176, 60))
    for i in range(4):
        gx = cx - s * 0.12 + i * s * 0.08
        d.line([gx, cy + s * 0.13, gx, cy + s * 0.22], fill=(110, 120, 128), width=max(2, h // 34))
    d.rectangle([cx - s * 0.37, cy - s * 0.14, cx - s * 0.3, cy + s * 0.12], fill=(170, 178, 186))
    d.rectangle([cx + s * 0.3, cy - s * 0.14, cx + s * 0.37, cy + s * 0.12], fill=(170, 178, 186))
    return t

def _tanker(d, x, y, s, smoke=False):
    hull = (30, 36, 44)
    d.polygon([(x, y), (x + s, y), (x + s * 0.92, y + s * 0.16), (x + s * 0.1, y + s * 0.16)],
              fill=hull)
    d.rectangle([x + s * 0.06, y - s * 0.05, x + s * 0.8, y], fill=(172, 44, 40))
    d.rectangle([x + s * 0.68, y - s * 0.2, x + s * 0.8, y - s * 0.05], fill=(226, 222, 210))
    d.rectangle([x + s * 0.71, y - s * 0.17, x + s * 0.77, y - s * 0.11], fill=(90, 130, 160))
    if smoke:
        for i, (dx, dy, r) in enumerate([(0.74, -0.34, 0.1), (0.8, -0.48, 0.14), (0.88, -0.62, 0.19)]):
            d.ellipse([x + s * dx - s * r, y + s * dy - s * r, x + s * dx + s * r, y + s * dy + s * r],
                      fill=(96, 100, 104, 200))

def sc_hormuz(w, h):
    t, d = _tile(w, h, (188, 208, 220))
    vgrad(d, w, 0, h * 0.52, (208, 226, 238), (176, 196, 212))
    vgrad(d, w, h * 0.52, h, (60, 104, 130), (32, 68, 92))
    for i in range(9):  # wave ticks
        x = (i * 53) % int(w)
        y = h * (0.62 + (i % 3) * 0.11)
        d.line([x, y, x + w * 0.05, y], fill=(120, 170, 196), width=2)
    _tanker(d, w * 0.06, h * 0.52, w * 0.34)
    _tanker(d, w * 0.56, h * 0.6, w * 0.38, smoke=True)
    # hit flash on the second tanker's engine room
    fx, fy = w * 0.9, h * 0.52
    for a in range(0, 360, 45):
        import math
        x2 = fx + math.cos(math.radians(a)) * w * 0.035
        y2 = fy + math.sin(math.radians(a)) * h * 0.07
        d.line([fx, fy, x2, y2], fill=(232, 92, 40), width=3)
    d.ellipse([fx - 4, fy - 4, fx + 4, fy + 4], fill=(246, 170, 50))
    return t

def sc_antalya(w, h):
    t, d = _tile(w, h, (236, 224, 192))
    vgrad(d, w, 0, h, (240, 230, 200), (228, 214, 176))
    # draft document sheet
    x0, y0, x1, y1 = w * 0.3, h * 0.02, w * 0.74, h * 0.86
    d.rectangle([x0 + 4, y0 + 5, x1 + 4, y1 + 5], fill=(206, 194, 164))
    d.rectangle([x0, y0, x1, y1], fill=(252, 250, 242), outline=(170, 160, 130), width=1)
    d.text(((x0 + x1) / 2, y0 + h * 0.07), "DRAFT DEAL", font=F(SANS_B, max(9, h // 9)),
           fill=INK, anchor="ma")
    for i in range(3):
        yy = y0 + h * (0.3 + i * 0.13)
        d.line([x0 + w * 0.05, yy, x1 - w * 0.05, yy], fill=(168, 168, 158), width=2)
    d.text(((x0 + x1) / 2, y0 + h * 0.60), "FOSSIL FUELS", font=F(SANS_B, max(9, h // 8)),
           fill=(60, 60, 60), anchor="ma")
    d.line([x0 + w * 0.03, y0 + h * 0.665, x1 - w * 0.03, y0 + h * 0.635], fill=RED, width=max(3, h // 22))
    # globe at left
    gx, gy, gr = w * 0.16, h * 0.42, min(w * 0.11, h * 0.3)
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(86, 140, 178))
    d.ellipse([gx - gr * 0.55, gy - gr * 0.4, gx - gr * 0.05, gy + gr * 0.1], fill=(96, 156, 96))
    d.ellipse([gx + gr * 0.15, gy + gr * 0.25, gx + gr * 0.6, gy + gr * 0.62], fill=(96, 156, 96))
    # pencil at right
    px, py = w * 0.82, h * 0.2
    d.polygon([(px, py), (px + w * 0.035, py + h * 0.5), (px + w * 0.075, py + h * 0.47),
               (px + w * 0.04, py - h * 0.03)], fill=(240, 176, 60))
    d.polygon([(px, py), (px + w * 0.035, py + h * 0.5), (px + w * 0.045, py + h * 0.42)],
              fill=(60, 60, 60))
    return t

def sc_basra(w, h):
    t, d = _tile(w, h, (206, 170, 142))
    vgrad(d, w, 0, h, (218, 184, 152), (190, 154, 124))
    base = h * 0.86
    sil = (64, 56, 52)
    # cooling tower + chimney + blocks
    d.polygon([(w * 0.1, base), (w * 0.16, h * 0.3), (w * 0.26, h * 0.3), (w * 0.32, base)], fill=sil)
    d.rectangle([w * 0.62, h * 0.14, w * 0.68, base], fill=sil)
    d.rectangle([w * 0.36, h * 0.52, w * 0.6, base], fill=sil)
    d.rectangle([w * 0.7, h * 0.6, w * 0.94, base], fill=(84, 72, 66))
    # smoke
    for (cx, cy, r) in [(0.65, 0.1, 0.09), (0.72, 0.05, 0.12), (0.2, 0.2, 0.08)]:
        d.ellipse([w * cx - w * r, h * cy - h * r, w * cx + w * r, h * cy + h * r],
                  fill=(110, 104, 100, 190))
    # flames along the base
    import math
    for i in range(9):
        fx = w * (0.08 + i * 0.1)
        fh = h * (0.24 + 0.1 * abs(math.sin(i * 1.7)))
        d.polygon([(fx - w * 0.035, base), (fx, base - fh), (fx + w * 0.035, base)],
                  fill=(226, 108, 32))
        d.polygon([(fx - w * 0.018, base), (fx, base - fh * 0.6), (fx + w * 0.018, base)],
                  fill=(246, 186, 60))
    d.rectangle([0, base, w, h], fill=(52, 46, 44))
    return t

def sc_gaza(w, h):
    t, d = _tile(w, h, (228, 210, 176))
    vgrad(d, w, 0, h, (240, 224, 190), (214, 194, 156))
    d.ellipse([w * 0.78, h * 0.08, w * 0.92, h * 0.3], fill=(246, 200, 92))  # sun
    ground = h * 0.78
    d.rectangle([0, ground, w, h], fill=(198, 176, 140))
    # aid van, side profile
    vx, vy, vw, vh = w * 0.16, ground - h * 0.42, w * 0.56, h * 0.42
    d.rounded_rectangle([vx, vy, vx + vw, vy + vh], int(h * 0.05), fill=(250, 248, 242),
                        outline=(150, 140, 120), width=2)
    d.polygon([(vx + vw, vy + vh * 0.25), (vx + vw + w * 0.13, vy + vh * 0.62),
               (vx + vw + w * 0.13, vy + vh), (vx + vw, vy + vh)], fill=(240, 236, 226),
              outline=(150, 140, 120))
    d.polygon([(vx + vw + w * 0.015, vy + vh * 0.34), (vx + vw + w * 0.1, vy + vh * 0.6),
               (vx + vw + w * 0.015, vy + vh * 0.6)], fill=(140, 180, 205))
    # heart emblem (care charity mark)
    cx, cy, r = vx + vw * 0.42, vy + vh * 0.48, vh * 0.24
    d.ellipse([cx - r, cy - r * 0.8, cx, cy + r * 0.2], fill=(206, 60, 52))
    d.ellipse([cx, cy - r * 0.8, cx + r, cy + r * 0.2], fill=(206, 60, 52))
    d.polygon([(cx - r * 0.92, cy), (cx + r * 0.92, cy), (cx, cy + r * 1.05)], fill=(206, 60, 52))
    for wx in (vx + vw * 0.18, vx + vw * 0.88):
        d.ellipse([wx - h * 0.055, ground - h * 0.1, wx + h * 0.055, ground + h * 0.01],
                  fill=(40, 40, 44))
    # stacked aid boxes behind
    for i, (bx, by) in enumerate([(0.03, 0.52), (0.03, 0.63), (0.86, 0.6)]):
        d.rectangle([w * bx, h * by, w * bx + w * 0.09, h * by + h * 0.12],
                    fill=(186, 156, 108), outline=(150, 124, 84), width=1)
    return t

def sc_vanuatu(w, h):
    t, d = _tile(w, h, (168, 202, 220))
    vgrad(d, w, 0, h * 0.55, (188, 218, 236), (156, 190, 210))
    vgrad(d, w, h * 0.55, h, (66, 124, 162), (38, 92, 126))
    # island mound
    d.polygon([(w * 0.3, h * 0.56), (w * 0.44, h * 0.34), (w * 0.56, h * 0.3),
               (w * 0.7, h * 0.56)], fill=(96, 138, 84))
    d.polygon([(w * 0.44, h * 0.34), (w * 0.56, h * 0.3), (w * 0.62, h * 0.56),
               (w * 0.48, h * 0.56)], fill=(80, 118, 70))
    # crack down the island
    d.line([(w * 0.5, h * 0.33), (w * 0.47, h * 0.42), (w * 0.53, h * 0.48), (w * 0.5, h * 0.56)],
           fill=(52, 44, 36), width=max(2, h // 26))
    # seismic rings in the sea
    cx, cy = w * 0.18, h * 0.74
    for i, r in enumerate((0.05, 0.1, 0.15)):
        d.arc([cx - w * r, cy - h * r * 1.4, cx + w * r, cy + h * r * 1.4], 300, 60,
              fill=(232, 92, 40), width=max(2, h // 30))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(232, 92, 40))
    return t

def sc_banda(w, h):
    # Banda Sea quake: same island-and-crack motif as the Vanuatu scene
    # (both are Pacific island quakes, drawn in code, not a photograph).
    return sc_vanuatu(w, h)

def sc_kyiv(w, h):
    t, d = _tile(w, h, (48, 64, 94))
    vgrad(d, w, 0, h, (58, 76, 110), (36, 50, 78))
    # flags behind: Ukraine bicolour + plain blue
    for (fx, col1, col2) in [(0.1, (74, 128, 190), (246, 206, 60)), (0.78, (36, 62, 120), (36, 62, 120))]:
        d.rectangle([w * fx, h * 0.1, w * fx + w * 0.13, h * 0.28], fill=col1)
        d.rectangle([w * fx, h * 0.28, w * fx + w * 0.13, h * 0.46], fill=col2)
        d.line([w * fx, h * 0.08, w * fx, h * 0.6], fill=(20, 26, 36), width=3)
    # figure at podium
    cx = w * 0.5
    d.ellipse([cx - w * 0.045, h * 0.3, cx + w * 0.045, h * 0.48], fill=(226, 196, 160))
    d.polygon([(cx - w * 0.11, h * 0.78), (cx - w * 0.09, h * 0.52), (cx + w * 0.09, h * 0.52),
               (cx + w * 0.11, h * 0.78)], fill=(30, 40, 34))
    d.polygon([(cx - w * 0.17, h), (cx - w * 0.1, h * 0.72), (cx + w * 0.1, h * 0.72),
               (cx + w * 0.17, h)], fill=(22, 30, 44))
    for mx in (-0.13, 0.13):
        d.line([cx + w * mx * 0.4, h * 0.72, cx + w * mx, h * 0.5], fill=(16, 20, 28),
               width=max(2, h // 30))
        d.ellipse([cx + w * mx - 4, h * 0.46, cx + w * mx + 4, h * 0.52], fill=(16, 20, 28))
    return t

def sc_sinaloa(w, h):
    t, d = _tile(w, h, (234, 202, 148))
    vgrad(d, w, 0, h * 0.8, (244, 216, 162), (226, 190, 134))
    d.ellipse([w * 0.82, h * 0.06, w * 0.96, h * 0.26], fill=(246, 190, 80))
    d.rectangle([0, h * 0.8, w, h], fill=(206, 168, 116))
    # cacti
    for (cx, s) in [(0.1, 0.5), (0.88, 0.38)]:
        gx, gy = w * cx, h * 0.82
        d.rectangle([gx - w * 0.02, gy - h * s, gx + w * 0.02, gy], fill=(74, 128, 74))
        d.rectangle([gx - w * 0.055, gy - h * s * 0.72, gx - w * 0.035, gy - h * s * 0.4],
                    fill=(74, 128, 74))
        d.rectangle([gx + w * 0.035, gy - h * s * 0.8, gx + w * 0.055, gy - h * s * 0.45],
                    fill=(74, 128, 74))
        d.rectangle([gx - w * 0.055, gy - h * s * 0.72, gx + w * 0.02, gy - h * s * 0.62],
                    fill=(74, 128, 74))
        d.rectangle([gx - w * 0.02, gy - h * s * 0.8, gx + w * 0.055, gy - h * s * 0.7],
                    fill=(74, 128, 74))
    # handcuffs, centre
    cx, cy, r = w * 0.5, h * 0.52, min(w * 0.13, h * 0.3)
    for dx in (-r * 0.95, r * 0.95):
        d.ellipse([cx + dx - r, cy - r, cx + dx + r, cy + r], outline=(110, 116, 124),
                  width=max(4, h // 16))
        d.ellipse([cx + dx - r * 0.55, cy - r * 0.55, cx + dx + r * 0.55, cy + r * 0.55],
                  outline=(150, 156, 164), width=max(2, h // 30))
    d.line([cx - r * 0.3, cy - r * 0.85, cx + r * 0.3, cy - r * 0.85], fill=(110, 116, 124),
           width=max(3, h // 22))
    return t

def sc_finland(w, h):
    t, d = _tile(w, h, (148, 166, 182))
    vgrad(d, w, 0, h * 0.58, (170, 186, 200), (136, 154, 170))
    vgrad(d, w, h * 0.58, h, (86, 112, 132), (56, 80, 100))
    # cargo ship
    sx, sy, sw = w * 0.12, h * 0.58, w * 0.52
    d.polygon([(sx, sy), (sx + sw, sy), (sx + sw * 0.9, sy + h * 0.14), (sx + sw * 0.08, sy + h * 0.14)],
              fill=(120, 52, 44))
    cols = [(52, 96, 150), (196, 120, 44), (70, 130, 84), (150, 70, 110)]
    for i in range(4):
        d.rectangle([sx + sw * (0.08 + i * 0.17), sy - h * 0.13, sx + sw * (0.23 + i * 0.17), sy],
                    fill=cols[i])
    d.rectangle([sx + sw * 0.8, sy - h * 0.26, sx + sw * 0.9, sy], fill=(228, 226, 218))
    # two drones with dotted attack lines
    import math
    for (dx, dy) in [(0.78, 0.16), (0.9, 0.3)]:
        cx, cy = w * dx, h * dy
        d.line([cx - w * 0.03, cy, cx + w * 0.03, cy], fill=(30, 34, 40), width=3)
        d.line([cx, cy - h * 0.05, cx, cy + h * 0.05], fill=(30, 34, 40), width=3)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(30, 34, 40))
        tx, ty = sx + sw * 0.55, sy - h * 0.05
        steps = 7
        for i in range(steps):
            px = cx + (tx - cx) * i / steps
            py = cy + (ty - cy) * i / steps
            d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=(200, 60, 44))
    return t

def sc_warsaw(w, h):
    t, d = _tile(w, h, (28, 48, 80))
    vgrad(d, w, 0, h, (36, 58, 96), (20, 38, 66))
    cx, cy = w * 0.5, h * 0.46
    s = min(w * 0.2, h * 0.36)
    # shield
    d.polygon([(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s * 0.3),
               (cx, cy + s * 1.25), (cx - s, cy + s * 0.3)],
              outline=(238, 240, 244), width=max(3, h // 20))
    # NATO four-point star
    d.polygon([(cx, cy - s * 0.62), (cx + s * 0.16, cy - s * 0.16), (cx + s * 0.62, cy),
               (cx + s * 0.16, cy + s * 0.16), (cx, cy + s * 0.62), (cx - s * 0.16, cy + s * 0.16),
               (cx - s * 0.62, cy), (cx - s * 0.16, cy - s * 0.16)], fill=(238, 240, 244))
    d.ellipse([cx - s * 0.13, cy - s * 0.13, cx + s * 0.13, cy + s * 0.13], fill=(28, 48, 80),
              outline=(238, 240, 244), width=2)
    # Polish white/red band at the bottom
    d.rectangle([0, h * 0.86, w, h * 0.93], fill=(240, 240, 240))
    d.rectangle([0, h * 0.93, w, h], fill=(196, 40, 52))
    return t

def sc_riemann(w, h):
    t, d = _tile(w, h, (32, 62, 52))
    vgrad(d, w, 0, h, (38, 70, 60), (26, 54, 44))
    d.text((w * 0.08, h * 0.1), "\u03b6(s) = 0", font=F(SERIF_I, max(14, h // 4)),
           fill=(240, 242, 236))
    d.text((w * 0.6, h * 0.14), "1 + 1/2\u02e2 + 1/3\u02e2 + \u2026", font=F(SERIF_I, max(9, h // 8)),
           fill=(206, 214, 206))
    for i in range(3):
        yy = h * (0.52 + i * 0.14)
        d.line([w * 0.08, yy, w * (0.5 + (i % 2) * 0.14), yy], fill=(190, 200, 190), width=2)
    # chalk check
    d.line([w * 0.68, h * 0.58, w * 0.76, h * 0.72], fill=(246, 220, 92), width=max(4, h // 14))
    d.line([w * 0.76, h * 0.72, w * 0.94, h * 0.4], fill=(246, 220, 92), width=max(4, h // 14))
    d.text((w * 0.64, h * 0.68), "17M lines", font=F(SANS_B, max(8, h // 9)), fill=(206, 214, 206))
    return t

def sc_davao(w, h):
    t, d = _tile(w, h, (70, 62, 96))
    d.rectangle([0, 0, w, h * 0.4], fill=(196, 116, 84))
    d.rectangle([0, h * 0.4, w, h * 0.68], fill=(120, 84, 96))
    d.rectangle([0, h * 0.68, w, h], fill=(36, 34, 44))  # tarmac
    d.line([0, h * 0.86, w, h * 0.86], fill=(240, 200, 90), width=2)
    # airliner side profile
    ax, ay, aw = w * 0.1, h * 0.34, w * 0.72
    d.rounded_rectangle([ax, ay, ax + aw, ay + h * 0.2], int(h * 0.05), fill=(232, 232, 228))
    d.polygon([(ax + aw * 0.86, ay - h * 0.16), (ax + aw * 0.99, ay + h * 0.02),
               (ax + aw * 0.86, ay + h * 0.04)], fill=(196, 40, 52))
    d.polygon([(ax + aw * 0.3, ay + h * 0.16), (ax + aw * 0.52, ay + h * 0.16),
               (ax + aw * 0.44, ay + h * 0.27), (ax + aw * 0.34, ay + h * 0.27)],
              fill=(200, 200, 196))
    for i in range(9):
        wx = ax + aw * (0.12 + i * 0.075)
        d.ellipse([wx, ay + h * 0.05, wx + w * 0.016, ay + h * 0.1], fill=(90, 130, 165))
    d.rectangle([ax + aw * 0.06, ay + h * 0.05, ax + aw * 0.1, ay + h * 0.13], fill=(90, 130, 165))
    # two yellow slides
    for sx in (0.2, 0.68):
        d.polygon([(ax + aw * sx, ay + h * 0.19), (ax + aw * sx + w * 0.05, ay + h * 0.19),
                   (ax + aw * sx + w * 0.13, h * 0.82), (ax + aw * sx + w * 0.07, h * 0.82)],
                  fill=(246, 200, 60))
    return t

SCENES = {
    "markets": sc_markets, "geneva": sc_geneva, "hormuz": sc_hormuz,
    "antalya": sc_antalya, "basra": sc_basra, "gaza": sc_gaza,
    "vanuatu": sc_vanuatu, "banda": sc_banda, "kyiv": sc_kyiv, "sinaloa": sc_sinaloa,
    "finland": sc_finland, "warsaw": sc_warsaw, "riemann": sc_riemann,
    "davao": sc_davao,
}

# ------------------------------------------------------- rich text --------
def rich_wrap(d, segments, maxw):
    """Wrap mixed-style segments into lines of (text, font, colour, width)."""
    tokens = []
    for text, fnt, col in segments:
        for w_ in text.split(" "):
            if w_:
                tokens.append((w_, fnt, col))
    lines, cur, curw = [], [], 0.0
    space = d.textlength(" ", font=segments[0][1])
    for w_, fnt, col in tokens:
        ww = d.textlength(w_, font=fnt)
        add = ww if not cur else ww + space
        if cur and curw + add > maxw:
            lines.append(cur)
            cur, curw = [(w_, fnt, col, ww)], ww
        else:
            cur.append((w_, fnt, col, ww))
            curw += add
    if cur:
        lines.append(cur)
    return lines

def draw_rich(d, x, y, lines, lh, space_fnt):
    space = d.textlength(" ", font=space_fnt)
    for line in lines:
        cx = x
        for w_, fnt, col, ww in line:
            d.text((cx, y), w_, font=fnt, fill=col)
            cx += ww + space
        y += lh
    return y

# ------------------------------------------------------------- canvas -----
MX = 16
CW = W - 2 * MX           # 992
canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas, "RGBA")

# kicker
d.text((MX, 11), "THE WORLD IN ONE DAY", font=F(SERIF_B, 16), fill=RED)
d.text((W - MX, 13), "34 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY",
       font=F(SANS_B, 12.5), fill=INK, anchor="ra")
d.line([(MX, 35), (W - MX, 35)], fill=INK, width=2)

# masthead
mh = fit(d, "Saturday 21 November 2026", SERIF_B, 68, CW)
d.text((MX, 38), "Saturday 21 November 2026", font=mh, fill=INK)
ink_bottom = d.textbbox((MX, 38), "Saturday 21 November 2026", font=mh)[3]

# standfirst (placed from the masthead's real ink bottom, never over it)
sf_text = ("AI rout wipes $4tn from US stocks · 128 nations chart a path "
           "to \u2018killer robot\u2019 rules · COP31 runs into overtime, still no deal")
sf = fit(d, sf_text, SERIF_I, 17, CW, floor=12)
d.text((MX, ink_bottom + 3), sf_text, font=sf, fill=DARKRED)

# region tally bar
ry, rh = 152, 22
rf = F(SANS_B, 11.5)
mins = [d.textlength(f"{n} {c}", font=rf) + 20 for n, c, _ in REGIONS]
extra = CW - sum(mins)
tot = sum(c for _, c, _ in REGIONS)
x = MX
for (name, cnt, col), mn in zip(REGIONS, mins):
    wseg = mn + extra * cnt / tot
    d.rectangle([x, ry, x + wseg, ry + rh], fill=col)
    d.text((x + wseg / 2, ry + rh / 2), f"{name} {cnt}", font=rf,
           fill=(255, 255, 255), anchor="mm")
    x += wseg

# the day in numbers
sy, sh = 178, 42
d.rectangle([MX, sy, MX + 92, sy + sh], fill=RED)
lab = wrap(d, "THE DAY IN NUMBERS", F(SANS_B, 12), 84)
ly = sy + (sh - len(lab) * 13) / 2
for ln in lab:
    d.text((MX + 46, ly), ln, font=F(SANS_B, 12), fill=(255, 255, 255), anchor="ma")
    ly += 13
sx = MX + 100
scw = (W - MX - sx) / 6
for i, (big, cap) in enumerate(STATS):
    cx = sx + i * scw
    bf = fit(d, big, SERIF_B, 23, scw - 8, floor=14)
    d.text((cx + scw / 2, sy), big, font=bf, fill=DARKRED, anchor="ma")
    cf = F(SANS_R, 9.5)
    for j, ln in enumerate(wrap(d, cap, cf, scw - 10)[:2]):
        d.text((cx + scw / 2, sy + 24 + j * 10.5), ln, font=cf, fill=SOFT, anchor="ma")
d.line([(MX, 228), (W - MX, 228)], fill=INK, width=1)

# ------------------------------------------------------------- heroes -----
HY, HH = 234, 218
HW = (CW - 2 * 13) // 3   # 322
for i, hd in enumerate(HEROES):
    x = MX + i * (HW + 13)
    y = HY
    d.rectangle([x, y, x + HW, y + HH], fill=CARD, outline=BORDER, width=1)
    tile = render_scene(hd["scene"], HW, 96)
    canvas.paste(tile, (x, y))
    by = y + 96 - 17
    d.rectangle([x, by, x + HW, y + 96], fill=NAVY + (238,))
    d.text((x + 8, by + 2.5), hd["bl"], font=F(SANS_B, 10), fill=(255, 255, 255))
    d.text((x + HW - 8, by + 2.5), hd["br"], font=F(SANS_B, 10), fill=GOLD, anchor="ra")
    ty = y + 96 + 6
    badge(d, x + 13, ty + 7, 8.5, hd["n"], 9)
    d.text((x + 27, ty + 1), f"{hd['loc']} · {hd['cat']}", font=F(SANS_B, 10.5),
           fill=DARKRED)
    pill(d, x + HW - 8 - (d.textlength(hd["tag"], font=F(SANS_B, 8)) + 10), ty + 1, hd["tag"])
    hyy = ty + 19
    hf = F(SERIF_B, 19)
    for ln in wrap(d, hd["head"], hf, HW - 20)[:2]:
        d.text((x + 10, hyy), ln, font=hf, fill=INK)
        hyy += 21
    bf = F(SANS_R, 11)
    for ln in wrap(d, hd["body"], bf, HW - 20)[:3]:
        d.text((x + 10, hyy + 1), ln, font=bf, fill=(52, 58, 60))
        hyy += 12
    d.text((x + 10, hyy + 3), hd["src"], font=F(SANS_I, 9.5), fill=SOFT)

# ------------------------------------------------------------- smalls -----
GY = HY + HH + 6
SW = (CW - 4 * 10) / 5    # 190.4
SH = 148
for i, sd_ in enumerate(SMALLS):
    r, c = divmod(i, 5)
    x = int(MX + c * (SW + 10))
    y = GY + r * (SH + 6)
    wpx = int(SW)
    d.rectangle([x, y, x + wpx, y + SH], fill=CARD, outline=BORDER, width=1)
    tile = render_scene(sd_["scene"], wpx, 68)
    canvas.paste(tile, (x, y))
    d.rectangle([x, y + 56, x + wpx, y + 68], fill=NAVY + (238,))
    d.text((x + 6, y + 57.5), sd_["band"], font=F(SANS_B, 8.5), fill=(255, 255, 255))
    ty = y + 72
    badge(d, x + 9, ty + 5, 6, sd_["n"], 7.5)
    d.text((x + 19, ty), f"{sd_['loc']} · {sd_['cat']}", font=F(SANS_B, 8), fill=DARKRED)
    tf = F(SANS_B, 7.5)
    tw = d.textlength(sd_["tag"], font=tf) + 8
    col = {"REPORTED": GREEN, "CLAIM": AMBER, "FORECAST": STEEL}[sd_["tag"]]
    d.rounded_rectangle([x + wpx - 6 - tw, ty, x + wpx - 6, ty + 11], 3, fill=col)
    d.text((x + wpx - 6 - tw + 4, ty + 1), sd_["tag"], font=tf, fill=(255, 255, 255))
    hyy = ty + 13
    hf = F(SERIF_B, 12.5)
    for ln in wrap(d, sd_["head"], hf, wpx - 14)[:2]:
        d.text((x + 7, hyy), ln, font=hf, fill=INK)
        hyy += 14.5
    segs = [(sd_["body"] + " ", F(SANS_R, 9.6), (52, 58, 60)),
            ("\u2014 " + sd_["src"], F(SANS_I, 9.6), SOFT)]
    lines = rich_wrap(d, segs, wpx - 14)[:2]
    draw_rich(d, x + 7, hyy + 1, lines, 11, F(SANS_R, 9.6))

# ------------------------------------------------------------- bottom -----
BY = GY + 2 * SH + 14
d.text((MX, BY), "WHERE IT HAPPENED", font=F(SANS_B, 12.5), fill=INK)
d.text((MX + 168, BY + 2), "numbers match the stories", font=F(SANS_I, 9.5), fill=SOFT)
d.text((428, BY), "ALSO ON SATURDAY", font=F(SANS_B, 12.5), fill=INK)
d.text((428 + 152, BY), "— 21 MORE STORIES", font=F(SANS_B, 12.5), fill=RED)
d.text((W - MX, BY + 2), "place · what happened · source", font=F(SANS_I, 9.5),
       fill=SOFT, anchor="ra")

# map: solid continents (Natural Earth 110m outlines, simplified) on a
# navy panel -- the treatment every finalist page used. Drawn on its own
# layer so antimeridian-crossing polygons clip at the panel edge.
mapx, mapy, mapw, maph = MX + 4, BY + 20, 392, 116
PANEL = (23, 38, 58)
d.rectangle([mapx - 6, mapy - 6, mapx + mapw + 6, mapy + maph + 6], fill=PANEL)
MSS = 3
mapimg = Image.new("RGB", (mapw * MSS, maph * MSS), PANEL)
md = ImageDraw.Draw(mapimg)

def proj(lon, lat):
    return ((lon + 180) / 360 * mapw * MSS, (84 - lat) / 144 * maph * MSS)

LAND = (219, 205, 170)
LAND_EDGE = (188, 170, 128)
for poly in POLYS_HQ:
    md.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
               outline=LAND_EDGE)
for lon, lat in DOTS:
    px, py = proj(lon, lat)
    md.ellipse([px - 2.6 * MSS, py - 2.6 * MSS, px + 2.6 * MSS, py + 2.6 * MSS],
               fill=(126, 200, 188))
for num, lon, lat in PINS:
    px, py = proj(lon, lat)
    md.ellipse([px - 7 * MSS, py - 7 * MSS, px + 7 * MSS, py + 7 * MSS],
               fill=RED, outline=(255, 255, 255), width=MSS)
    md.text((px, py - 0.5 * MSS), str(num), font=F(SANS_B, 8 * MSS),
            fill=(255, 255, 255), anchor="mm")
canvas.paste(mapimg.resize((mapw, maph), Image.LANCZOS), (mapx, mapy))
ly = mapy + maph + 6
d.text((MX, ly), "Red pins: the 13 stories \u00b7 teal dots + coloured numbers: the briefs, by region",
       font=F(SANS_R, 8.5), fill=SOFT)
d.text((MX, ly + 11), "Tags: REPORTED = named sources \u00b7 CLAIM = one side\u2019s account \u00b7 FORECAST = expected",
       font=F(SANS_R, 8.5), fill=SOFT)
d.text((MX, ly + 22), "UTC 03:45 Geneva ends \u00b7 05:00 tanker 1 \u00b7 05:50 tanker 2 \u00b7 09:42 Banda M6.8",
       font=F(SANS_B, 8.5), fill=INK)

# briefs, two columns -- font auto-fitted so the columns end above the
# date-check box (measured before anything is drawn)
cols = [BRIEFS[:11], BRIEFS[11:]]
colw = 284
BRIEF_TOP = BY + 22
BRIEF_BOT = 940
def brief_layout(bsize):
    lh = bsize + 1.9
    out = []
    for col in cols:
        items, total = [], 0.0
        for num, place, fact, src in col:
            segs = [(place, F(SANS_B, bsize), INK),
                    (" \u2014 " + fact + " ", F(SANS_R, bsize), (52, 58, 60)),
                    (src, F(SANS_I, bsize), SOFT)]
            lines = rich_wrap(d, segs, colw - 17)
            items.append((num, lines))
            total += len(lines) * lh + 1.4
        out.append((items, total))
    return out, lh

bsize = 9.6
layout, blh = brief_layout(bsize)
while max(t for _, t in layout) > BRIEF_BOT - BRIEF_TOP and bsize > 8.4:
    bsize -= 0.3
    layout, blh = brief_layout(bsize)
for ci, (items, _t) in enumerate(layout):
    bx = 428 + ci * (colw + 12)
    yy = BRIEF_TOP
    for num, lines in items:
        d.text((bx, yy), str(num), font=F(SANS_B, bsize),
               fill=REGION_COL[BRIEF_REGION[num]])
        yy = draw_rich(d, bx + 17, yy, lines, blh, F(SANS_R, bsize)) + 1.4

# date check box (tick drawn with lines: the serif/sans fonts lack a
# checkmark glyph)
DY = 946
d.rectangle([MX, DY, W - MX, DY + 44], outline=RED, width=2)
d.line([(MX + 12, DY + 13), (MX + 16, DY + 18)], fill=RED, width=3)
d.line([(MX + 16, DY + 18), (MX + 25, DY + 7)], fill=RED, width=3)
dc = [("DATE CHECK  ", F(SANS_B, 10), RED),
      ("Every story on this page happened, or was first reported, on Saturday "
       "21 November 2026. LEFT OUT AS OTHER DAYS\u2019 NEWS \u2014 Sat 24 Oct: Vanuatu M6.9 quake \u00b7 Thu 19 Nov: World Court "
       "rules Myanmar committed genocide \u00b7 Tbilisi gas blast kills six \u00b7 Seoul "
       "overturns ex-PM Han\u2019s sentence. Fri 20 Nov: "
       "UK\u2013EU summit deals signed \u00b7 Brazil supercell storm \u00b7 Russia\u2019s 400-drone "
       "barrage \u00b7 Gupta sentenced in New York. Tue 17 Nov: US loses measles-free "
       "status \u00b7 Senegal\u2019s PASTEF strikes off Faye. NOT YET: a binding "
       "killer-robot treaty (drafting starts now) \u00b7 COP31\u2019s final deal (talks "
       "resume Sunday).", F(SANS_R, 9.8), INK)]
lines = rich_wrap(d, dc, CW - 42)[:3]
draw_rich(d, MX + 31, DY + 6, lines, 11.5, F(SANS_R, 9.8))

# footer
foot = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Bloomberg \u00b7 WSJ \u00b7 USGS \u00b7 UN News \u00b7 "
        "GMA \u00b7 PAP \u00b7 Al Jazeera \u00b7 Quanta \u00b7 Daily Trust \u00b7 Radio Tamazuj \u00b7 GFZ \u2014 "
        "Claims are attributed, not stated as fact \u00b7 Pictures and map drawn in code, "
        "not photographs")
ff = fit(d, foot, SANS_R, 9, CW, floor=7)
d.text((W // 2, 997), foot, font=ff, fill=SOFT, anchor="ma")

canvas.save(OUT, "PNG", optimize=True)
size = os.path.getsize(OUT)
print("saved", OUT, canvas.size, size, "bytes")
if size > 1000 * 1000:
    q = canvas.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    q.save(OUT, "PNG", optimize=True)
    print("quantized ->", os.path.getsize(OUT), "bytes")
