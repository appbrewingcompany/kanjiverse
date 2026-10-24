#!/usr/bin/env python3
"""Render the Kanjiverse hero-ad animatic (draft cut, no captures).

Produces brand-derived mock frames per beat, assembles them with ffmpeg into
export/animatic.mp4 (1080x1920@30fps, captions burned from captions.ass).
The final cut replaces these frames with real device captures via assemble.sh.

Deps: rsvg-convert, ffmpeg; fonts Noto Sans JP + Roboto (see discord pack README).
"""

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))  # repo root
BUILD = os.path.join(HERE, "..", "build")
EXPORT = os.path.join(HERE, "..", "export")

W, H = 1080, 1920
BG = "#141218"
CARD = "#211E26"
CARD_HI = "#2B2731"
INK = "#FFFFFF"
INK_2 = "#E6E0E9"
DIM = 0.62

VIVID = ["#3F51B5", "#673AB7", "#9C27B0", "#E91E63", "#F44336"]
DEFAULT = ["#303F9F", "#512DA8", "#7B1FA2", "#AF1781", "#D32F2F"]
PASTEL = ["#7986CB", "#9575CD", "#BA68C8", "#F06292", "#E57373"]

TIER_GRAD = ",".join(VIVID)
TIER_GRAD_DEF = ",".join(DEFAULT)


def svg(body, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">{extra_defs}{body}</svg>'
    )


def tier_gradient(gid, colors, x2="100%", y2="100%"):
    stops = "".join(
        f'<stop offset="{i / (len(colors) - 1) * 100:.0f}%" stop-color="{c}"/>'
        for i, c in enumerate(colors)
    )
    return (
        f'<defs><linearGradient id="{gid}" x1="0%" y1="0%" x2="{x2}" y2="{y2}">'
        f"{stops}</linearGradient></defs>"
    )


def render(svg_text, out_png):
    p = subprocess.run(
        ["rsvg-convert", "-w", str(W), "-h", str(H), "-o", out_png, "-"],
        input=svg_text.encode(), check=True, capture_output=True)
    return p


def kanji(x, y, text, size, fill, weight=900, anchor="middle"):
    return (
        f'<text x="{x}" y="{y}" font-family="Noto Sans JP" font-weight="{weight}" '
        f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
        f'dominant-baseline="central">{text}</text>'
    )


def latin(x, y, text, size, fill, weight=500, anchor="middle", spacing=None, opacity=None):
    op = f' fill-opacity="{opacity}"' if opacity else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x}" y="{y}" font-family="Roboto" font-weight="{weight}" '
        f'font-size="{size}" fill="{fill}" text-anchor="{anchor}"{sp}{op} '
        f'dominant-baseline="central">{text}</text>'
    )


def card(x, y, w, h, fill=CARD, r=28):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'


# ---------------------------------------------------------------- hook frames
def hook_frame(i, n):
    """Frames 0..n: kanji 漢 ink-reveal (first half) then tier-color sweep."""
    t = i / (n - 1)
    half = t < 0.5
    defs = tier_gradient("tiers", VIVID)
    # ink reveal mask: soft-edged band sweeping down-right
    edge = -300 + t * 2 * (W + 700) if half else W + 500
    defs += (
        '<linearGradient id="soft" x1="0%" y1="0%" x2="100%" y2="0%">'
        '<stop offset="0%" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="45%" stop-color="#fff"/>'
        '<stop offset="100%" stop-color="#fff"/></linearGradient>'
        f'<mask id="reveal"><rect x="-400" y="0" width="{edge + 400:.0f}" '
        'height="1920" fill="url(#soft)"/></mask>'
    )
    glyph = kanji(W / 2, 880, "漢", 880, INK)
    body = f'<rect width="{W}" height="{H}" fill="{BG}"/>' + glyph
    if half:
        body = (
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            f'<g mask="url(#reveal)">{glyph}</g>'
        )
    else:
        t2 = (t - 0.5) * 2  # 0..1 across second half
        defs += (
            '<linearGradient id="soft2" x1="0%" y1="0%" x2="100%" y2="0%">'
            '<stop offset="0%" stop-color="#fff"/>'
            '<stop offset="70%" stop-color="#fff"/>'
            '<stop offset="100%" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="sweep"><rect x="0" y="0" width="{t2 * (W + 300):.0f}" '
            'height="1920" fill="url(#soft2)"/></mask>'
        )
        colored = kanji(W / 2, 880, "漢", 880, "url(#tiers)")
        body = (
            f'<rect width="{W}" height="{H}" fill="{BG}"/>' + glyph +
            f'<g mask="url(#sweep)">{colored}</g>'
        )
    return svg(body, defs)


# ------------------------------------------------------------------- scenes
def scene_lookup():
    rows = [
        ("水", "みず", "water", VIVID[0]),
        ("水曜日", "すいようび", "Wednesday", VIVID[0]),
        ("水泳", "すいえい", "swimming", VIVID[1]),
        ("水素", "すいそ", "hydrogen", VIVID[2]),
    ]
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(card(48, 120, W - 96, 128, CARD_HI, 64))
    b.append(f'<circle cx="140" cy="184" r="26" stroke="{INK_2}" stroke-width="6" fill="none"/>')
    b.append(f'<line x1="160" y1="204" x2="182" y2="226" stroke="{INK_2}" stroke-width="6"/>')
    b.append(kanji(230, 186, "みず", 56, INK, 700, "start"))
    y = 320
    for word, kana, gloss, color in rows:
        b.append(card(48, y, W - 96, 300))
        b.append(kanji(130, y + 120, kana, 40, INK_2, 500, "start"))
        b.append(kanji(130, y + 210, word, 96, color, 900, "start"))
        b.append(latin(W - 130, y + 210, gloss, 44, INK_2, 400, "end"))
        y += 344
    return svg("".join(b))


def scene_decompose():
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(latin(W / 2, 220, "decomposition", 46, INK_2, 500, "middle", 6, DIM))
    for cx, r, color, ch in ((240, 130, VIVID[0], "氵"), (840, 130, VIVID[1], "感")):
        b.append(f'<circle cx="{cx}" cy="560" r="150" fill="none" stroke="{color}" stroke-width="10"/>')
        b.append(kanji(cx, 560, ch, 170, INK))
    b.append(latin(540, 560, "+", 110, INK_2, 300))
    b.append(latin(540, 830, "=", 110, INK_2, 300))
    b.append(kanji(540, 1120, "漢", 420, "url(#tiers)"))
    b.append(kanji(540, 1450, "カン", 54, INK_2, 500))
    b.append(latin(540, 1540, "China-style · Sino-", 40, INK_2, 400, "middle", 2, DIM))
    return svg("".join(b), tier_gradient("tiers", VIVID))


def scene_strokes():
    # stroke-order player mock: glyph + progress indicator + replay control
    # (no faked stroke positions — the real cut captures the app's animation)
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(latin(540, 240, "stroke order", 46, INK_2, 500, "middle", 6, DIM))
    b.append(kanji(540, 880, "漢", 820, INK))
    b.append(card(120, 1420, 840, 150, CARD_HI, 75))
    x = 165
    for n in range(1, 14):
        on = n <= 8  # mid-animation progress
        fill = f'url(#tiers)' if on else "none"
        stroke = "none" if on else INK_2
        b.append(f'<rect x="{x}" y="1452" width="44" height="86" rx="16" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        b.append(latin(x + 22, 1497, str(n), 30, INK if on else INK_2, 700))
        x += 60
    b.append(f'<circle cx="540" cy="1700" r="52" fill="{VIVID[1]}"/>')
    b.append(f'<path d="M 522 1672 L 568 1700 L 522 1728 Z" fill="{INK}"/>')
    return svg("".join(b), tier_gradient("tiers", VIVID))


def scene_read():
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(latin(540, 240, "reading view", 46, INK_2, 500, "middle", 6, DIM))
    # highlight behind 読んで (char centers 602/694/786, ruby included)
    b.append(f'<rect x="548" y="656" width="304" height="226" rx="28" '
             f'fill="{VIVID[1]}" fill-opacity="0.28"/>')
    for x, ch, kana in ((246, "日本語", "にほんご"), (418, "を", None), (510, "読", "よ"),
                        (602, "ん", None), (694, "で", None), (786, "み", None),
                        (878, "よう", None)):
        b.append(kanji(x, 800, ch, 88, INK))
        if kana:
            b.append(kanji(x, 700, kana, 36, INK_2, 500))
    b.append(card(150, 1120, 780, 360))
    b.append(kanji(230, 1230, "よむ", 40, INK_2, 500, "start"))
    b.append(kanji(230, 1330, "読む", 100, VIVID[1], 900, "start"))
    b.append(latin(830, 1330, "to read", 46, INK_2, 400, "end"))
    b.append(latin(540, 1440, "tap any word for its card", 38, INK_2, 400, "middle", 2, DIM))
    return svg("".join(b))


def scene_palettes():
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(latin(540, 240, "frequency palettes", 46, INK_2, 500, "middle", 6, DIM))
    y = 380
    for name, palette in (("Default", DEFAULT), ("Vivid", VIVID), ("Pastel", PASTEL)):
        b.append(card(90, y, W - 180, 380))
        b.append(latin(190, y + 110, name, 48, INK, 700, "start"))
        x = 190
        for color in palette:
            b.append(f'<circle cx="{x + 40}" cy="{y + 250}" r="44" fill="{color}"/>')
            x += 120
        b.append(kanji(x + 60, y + 250, "水曜日", 92, palette[0], 900, "start"))
        y += 440
    return svg("".join(b))


def scene_fonts():
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(latin(540, 240, "9 learner fonts", 46, INK_2, 500, "middle", 6, DIM))
    rows = [
        ("Noto Sans JP", "漢字", "Noto Sans JP", 900),
        ("M PLUS Rounded 1c", "漢字", "Hiragino Maru Gothic ProN", 400),
        ("Sawarabi Mincho", "漢字", "Hiragino Mincho ProN", 400),
    ]
    y = 400
    for label, glyph, family, weight in rows:
        b.append(card(90, y, W - 180, 360))
        b.append(kanji(240, y + 180, glyph, 150, VIVID[1], weight, "middle"))
        b.append(latin(860, y + 150, label, 40, INK, 500, "end"))
        y += 420
    b.append(latin(540, 1700, "animatic uses system stand-ins", 30, INK_2, 400, "middle", 2, 0.4))
    return svg("".join(b))


def cta_frame(i, n, mark_group):
    t = min(1.0, i / (n * 0.35))          # underline draw over first 35%
    fade = min(1.0, i / (n * 0.12))       # badges fade over first 12%
    defs = tier_gradient("tiers", VIVID)
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(mark_group)
    b.append(latin(540, 760, "Kanjiverse", 130, INK, 900, "middle", -1))
    b.append(f'<rect x="200" y="830" width="{int(680 * t)}" height="16" rx="8" fill="url(#tiers)"/>')
    b.append(latin(540, 980, "The Japanese dictionary that shows", 44, INK_2, 400))
    b.append(latin(540, 1040, "what's worth learning.", 44, INK_2, 400))
    badge_alpha = 0.25 + 0.75 * fade
    for x, label in ((190, "App Store"), (560, "Google Play")):
        b.append(f'<rect x="{x}" y="1240" width="330" height="104" rx="52" '
                 f'fill="none" stroke="{INK}" stroke-width="4" stroke-opacity="{badge_alpha:.2f}"/>')
        b.append(f'<text x="{x + 165}" y="1296" font-family="Roboto" font-weight="500" '
                 f'font-size="40" fill="{INK}" fill-opacity="{badge_alpha:.2f}" '
                 f'text-anchor="middle" dominant-baseline="central">{label}</text>')
    return svg("".join(b), defs)


# ------------------------------------------------------------------- pipeline
def run(cmd):
    subprocess.run(cmd, check=True)


def build(segments_only=False):
    shutil.rmtree(BUILD, ignore_errors=True)
    os.makedirs(os.path.join(BUILD, "hook"), exist_ok=True)
    os.makedirs(os.path.join(BUILD, "cta"), exist_ok=True)
    os.makedirs(EXPORT, exist_ok=True)

    # hook frames: 6s (180)
    for i in range(180):
        render(hook_frame(i, 180), f"{BUILD}/hook/f{i:04d}.png")

    # cta frames: 10s (300); mark = the canonical extraction from the
    # Discord pack (PR carrying it may not be merged yet) → gradient
    # monogram fallback keeps the animatic self-sufficient.
    mark_file = os.path.join(ROOT, "marketing", "discord", "src", "mark.svg")
    if os.path.exists(mark_file):
        d = re.search(r'd="(.*?)"', open(mark_file).read()).group(1)
        mark_group = (f'<g transform="translate(430,470) scale(9.17)">'
                      f'<path fill="{INK}" d="{d}"/></g>')
    else:
        mark_group = (f'<circle cx="540" cy="570" r="110" fill="url(#tiers)"/>'
                      + kanji(540, 572, "漢", 130, INK))
    for i in range(300):
        render(cta_frame(i, 300, mark_group), f"{BUILD}/cta/f{i:04d}.png")

    # motion segments (shared with the final-cut assembly)
    for name in ("hook", "cta"):
        run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30",
             "-i", f"{BUILD}/{name}/f%04d.png", "-vf", "format=yuv420p",
             "-c:v", "libx264", "-crf", "22", f"{BUILD}/{name}.mp4"])
    if segments_only:
        print(f"ok: hook/cta segments in {BUILD}")
        return 0

    # static scenes
    for name, fn in (("s3", scene_lookup), ("s4", scene_decompose),
                     ("s5", scene_strokes), ("s6", scene_read),
                     ("s7", scene_palettes), ("s8", scene_fonts)):
        render(fn(), f"{BUILD}/{name}.png")

    segs = [
        ("hook", None), ("s3", 7), ("s4", 8), ("s5", 7),
        ("s6", 8), ("s7", 8), ("s8", 6), ("cta", None),
    ]
    for name, dur in segs:
        if dur:  # static: loop one frame
            run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t",
                 str(dur), "-i", f"{BUILD}/{name}.png",
                 "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "22",
                 f"{BUILD}/{name}.mp4"])
    with open(f"{BUILD}/concat.txt", "w") as f:
        for name, _ in segs:
            f.write(f"file '{name}.mp4'\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", f"{BUILD}/concat.txt", "-c", "copy", f"{BUILD}/joined.mp4"])
    # libass-free caption burn (tools/burn_captions.py reads captions.ass)
    run(["python3", os.path.join(HERE, "burn_captions.py"),
         f"{BUILD}/joined.mp4", os.path.join(EXPORT, "animatic.mp4")])
    print(f"ok: {os.path.join(EXPORT, 'animatic.mp4')}")


if __name__ == "__main__":
    sys.exit(build("--segments-only" in sys.argv))
