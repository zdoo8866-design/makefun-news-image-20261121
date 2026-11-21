#!/usr/bin/env python3
"""Compose entry.png for news-image-20261121: one 1024x1024 front page,
six panels over one shared pale backdrop. All type set programmatically."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
WORK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(WORK, "..", "entry.png")

NOTO = "/usr/share/fonts/truetype/noto"
SERIF_B = f"{NOTO}/NotoSerif-Bold.ttf"
SERIF_I = f"{NOTO}/NotoSerif-Italic.ttf"
SANS_B = f"{NOTO}/NotoSans-Bold.ttf"
SANS_SB = f"{NOTO}/NotoSans-SemiBold.ttf"
SANS_R = f"{NOTO}/NotoSans-Regular.ttf"

INK = (30, 42, 54)
SOFT = (84, 98, 110)
TAGC = (43, 92, 122)        # muted steel blue
CHIP_BG = (250, 238, 214)   # soft amber wash
CHIP_TX = (146, 96, 22)     # dark amber
CARD = (255, 255, 255)
RULE = (120, 134, 146)

def font(path, size):
    return ImageFont.truetype(path, size)

def cover(img, tw, th, focus_y=0.5):
    """Resize+crop img to exactly tw x th, keeping the focus_y band."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = int((nh - th) * focus_y)
    y = max(0, min(nh - th, y))
    return img.crop((x, y, x + tw, y + th))

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---------- canvas over the shared backdrop ----------
backdrop = Image.open(os.path.join(
    WORK, "../art/backdrop.webp")).convert("RGB")
canvas = cover(backdrop, W, H, 0.45)
# gentle white wash so type and cards sit calmly on it
wash = Image.new("RGB", (W, H), (252, 250, 245))
canvas = Image.blend(canvas, wash, 0.35)
d = ImageDraw.Draw(canvas, "RGBA")

# ---------- masthead ----------
d.text((W // 2, 30), "21 November 2026", font=font(SERIF_B, 55),
       fill=INK, anchor="ma")
d.text((W // 2, 100), "T H E   W O R L D   I N   O N E   D A Y   ·   S A T U R D A Y",
       font=font(SANS_SB, 17), fill=SOFT, anchor="ma")
d.line([(40, 138), (W - 40, 138)], fill=RULE + (200,), width=2)

# ---------- panels ----------
PANELS = [
    dict(img="../art/scene-hormuz.webp",
         focus=0.40, tag="STRAIT OF HORMUZ", chip="2 TANKERS HIT",
         head="Two tankers hit in the strait",
         fact="A second outbound tanker is struck in its engine room 50 minutes "
              "after the first, off Khasab; no casualties, UKMTO says."),
    dict(img="../art/scene-geneva.webp",
         focus=0.34, tag="GENEVA", chip="RULES BY 2028",
         head="\u2018Killer robot\u2019 talks end with a path, no pact",
         fact="Talks run past 4 a.m.: 128 states agree to spend two years "
              "drafting rules for autonomous weapons, binding or not."),
    dict(img="../art/scene-antalya.webp",
         focus=0.46, tag="ANTALYA", chip="COP32: ADDIS ABABA",
         head="COP31 runs into overtime, still no deal",
         fact="Crews pack up the venue as negotiators chase a third draft; "
              "the text still does not mention fossil fuels."),
    dict(img="../art/scene-basra.webp",
         focus=0.44, tag="BASRA", chip="800 MW OFFLINE",
         head="Power-station fire kills at least four",
         fact="The blaze at the Hartha plant breaks out around 6 a.m., spreads "
              "to nearby homes and shuts the station; 30 are injured."),
    dict(img="../art/scene-riemann.webp",
         focus=0.40, tag="CAMBRIDGE, MASS.", chip="167 YEARS OPEN",
         head="Race to verify the Riemann claim",
         fact="Independent teams compile the 17-million-line AI-assisted proof "
              "within a day; checks go on, and a human rival surfaces."),
    dict(img="../art/scene-davao.webp",
         focus=0.44, tag="DAVAO", chip="146 SAFE",
         head="Everyone walks away from flight PX19",
         fact="The Hong Kong\u2013Port Moresby 767 diverts on a fire warning in "
              "its right engine; all aboard leave by the slides."),
]

MX, GAP = 26, 18
PW = (W - 2 * MX - GAP) // 2            # 477
TOP = 154
FOOT = 46
ROWS = 3
PH = (H - TOP - FOOT - (ROWS - 1) * 14) // ROWS   # 258
SCENE_H = 148
TEXT_H = PH - SCENE_H                              # 110

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
for i, p in enumerate(PANELS):
    r, c = divmod(i, 2)
    x = MX + c * (PW + GAP)
    y = TOP + r * (PH + 14)
    sd.rounded_rectangle([x + 3, y + 5, x + PW + 3, y + PH + 5], 10, fill=(40, 55, 70, 60))
shadow = shadow.filter(ImageFilter.GaussianBlur(5))
canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow)
d = ImageDraw.Draw(canvas, "RGBA")

for i, p in enumerate(PANELS):
    r, c = divmod(i, 2)
    x = MX + c * (PW + GAP)
    y = TOP + r * (PH + 14)
    # scene
    scene = Image.open(os.path.join(WORK, p["img"])).convert("RGB")
    scene = cover(scene, PW, SCENE_H, p["focus"])
    canvas.paste(scene, (x, y))
    # white text card under the scene
    d.rectangle([x, y + SCENE_H, x + PW, y + PH], fill=CARD + (255,))
    d.line([(x, y + SCENE_H), (x + PW, y + SCENE_H)], fill=(214, 220, 224, 255), width=1)
    tx = x + 16
    ty = y + SCENE_H + 10
    # tag (left) + chip (right pill)
    d.text((tx, ty), p["tag"], font=font(SANS_B, 14), fill=TAGC)
    cf = font(SANS_B, 13)
    cw = d.textlength(p["chip"], font=cf)
    cx1 = x + PW - 16 - cw - 20
    d.rounded_rectangle([cx1, ty - 3, x + PW - 16, ty + 19], 9, fill=CHIP_BG + (255,))
    d.text((cx1 + 10, ty), p["chip"], font=cf, fill=CHIP_TX)
    # headline
    hy = ty + 26
    hf = font(SANS_B, 20)
    if d.textlength(p["head"], font=hf) > PW - 32:
        hf = font(SANS_B, 18)
    d.text((tx, hy), p["head"], font=hf, fill=INK)
    # fact, up to two lines (warn if it would need more)
    fy = hy + 30
    flines = wrap(d, p["fact"], font(SANS_R, 15), PW - 32)
    if len(flines) > 2:
        print("WARN fact too long:", p["tag"], len(flines), "lines")
    for ln in flines[:2]:
        d.text((tx, fy), ln, font=font(SANS_R, 15), fill=SOFT)
        fy += 20

# ---------- footer inventory ----------
d.text((W // 2, H - 38),
       "a strait struck \u00b7 a pact postponed \u00b7 a summit in overtime \u00b7 "
       "a fatal fire \u00b7 a proof to check \u00b7 a safe landing",
       font=font(SERIF_I, 17), fill=(70, 84, 96), anchor="ma")

canvas = canvas.convert("RGB")
canvas.save(OUT, "PNG", optimize=True)
size = os.path.getsize(OUT)
print("saved", OUT, canvas.size, size, "bytes")
if size > 1000 * 1000:
    q = canvas.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    q.save(OUT, "PNG", optimize=True)
    print("quantized ->", os.path.getsize(OUT), "bytes")
