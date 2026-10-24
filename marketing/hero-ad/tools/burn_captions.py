#!/usr/bin/env python3
"""Burn captions.ass onto a video without libass (this ffmpeg build has no
`ass`/`subtitles` filter).

Renders each caption line to a transparent PNG (exact brand styling: Roboto
Medium, white with tier-colored keywords, dark outline+shadow, bottom-third)
and overlays each with an enable-window. captions.ass stays the single source.

Usage: burn_captions.py <input.mp4> <output.mp4>
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASS = os.path.join(HERE, "..", "captions.ass")
W, H = 1080, 1920

TC = re.compile(r"(\d+):(\d+):(\d+)\.(\d+)")
DIA = re.compile(
    r"Dialogue: 0,([\d:.]+),([\d:.]+),Default,,0,0,0,,(.*)$")


def tc_to_s(m):
    h, mi, s, cs = (int(g) for g in m.groups())
    return h * 3600 + mi * 60 + s + cs / 100.0


def parse_ass():
    lines = []
    for raw in open(ASS, encoding="utf-8"):
        m = DIA.match(raw.strip())
        if not m:
            continue
        start = tc_to_s(TC.fullmatch(m.group(1)))
        end = tc_to_s(TC.fullmatch(m.group(2)))
        text = m.group(3)
        runs, color, bold = [], "FFFFFF", False
        # split on override blocks; track color/bold state; drop other tags
        for part in re.split(r"(\{[^}]*\})", text):
            if part.startswith("{"):
                c = re.search(r"\\c&H([0-9A-Fa-f]{6})&", part)
                if c:
                    color = c.group(1).upper()
                if "\\b1" in part:
                    bold = True
                if "\\b0" in part:
                    bold = False
                continue
            if part:
                runs.append((part, color, bold))
        lines.append((start, end, runs))
    return lines


def bgr_to_rgb(h):
    return f"#{h[4:6]}{h[2:4]}{h[0:2]}"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def caption_svg(runs):
    spans = "".join(
        f'<tspan fill="{bgr_to_rgb(c)}" font-weight="{"900" if b else "500"}">'
        f"{esc(t)}</tspan>"
        for t, c, b in runs
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
        f'<text x="{W / 2}" y="1600" font-family="Roboto Medium" font-size="72" '
        f'text-anchor="middle" stroke="#000000" stroke-width="9" '
        f'paint-order="stroke" fill="#FFFFFF" '
        f'style="filter: drop-shadow(0 3px 6px rgba(0,0,0,0.6))">{spans}</text>'
        f"</svg>"
    )


def main(src, dst):
    caps = parse_ass()
    with tempfile.TemporaryDirectory() as td:
        pngs = []
        for i, (start, end, runs) in enumerate(caps):
            p = os.path.join(td, f"c{i:02d}.png")
            subprocess.run(
                ["rsvg-convert", "-w", str(W), "-h", str(H), "-o", p, "-"],
                input=caption_svg(runs).encode(), check=True)
            pngs.append((p, start, end))
        inputs, chain = [], []
        prev = "0:v"
        for i, (p, s, e) in enumerate(pngs):
            inputs += ["-i", p]
            out = f"v{i}"
            chain.append(
                f"[{prev}][{i + 1}:v]overlay=enable='between(t,{s:.2f},{e:.2f})'[{out}]")
            prev = out
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src]
        cmd += inputs
        cmd += ["-filter_complex", ";".join(chain), "-map", f"[{prev}]",
                "-c:v", "libx264", "-crf", "24", "-pix_fmt", "yuv420p", dst]
        subprocess.run(cmd, check=True)
    print(f"ok: {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
