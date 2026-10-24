# 60s vertical hero ad — production

In-house, $0: beat script → real device/emulator captures → motion-graphics
assembly (ffmpeg). 9:16, 1080×1920, 60s, captions burned in, licensed-free
music. Showcase anchors: kanji dictionary + themes only; dictionary-first hook
(no AI in hook, title card, or captions) — epic kanjiverse#427 decisions.

- Beat script: [beats.md](beats.md)
- Draft cut: `export/animatic.mp4` — a motion-graphics animatic (brand-derived
  mock frames, real beat timing, real captions) produced by
  `tools/make_animatic.py`. It exists so the beat rhythm, caption voice, and
  look can be approved before the capture day; it is NOT the final cut.
- Final cut: `assemble.sh` composes the real capture segments + captions +
  music into `export/hero-ad.mp4`.

Everything derives from [the creative direction](../creative-direction.md).

## Capture runbook (final cut)

Same emulator recipe as the store screenshots (kanjiverse_app#1099 capture
plan): Pixel_10_CI AVD from the shared image, current staging build installed,
`adb shell wm size 1080x1920`.

Per beat, drive the app and record:

```
adb shell screenrecord --time-limit 12 --bit-rate 12000000 \
  /sdcard/beat<N>.mp4 && adb pull /sdcard/beat<N>.mp4 captures/
```

| Beat | Drive | Duration target |
|------|-------|-----------------|
| 3 lookup | Open search sheet, input みず (adb `input text`/IME), let results settle, slow scroll | 7s usable |
| 4 decompose | Open 漢 detail → formula card → glyph graph | 8s usable |
| 5 stroke order | Stroke-order card, animation speed 1.5×, one full pass | 7s usable |
| 6 read | Sentence of the day → tap one word → word card | 8s usable |
| 7 themes | Frequency palette settings: default → vivid → pastel with a populated list behind | 8s usable |
| 8 type | Japanese font setting cycling 3–4 faces + light/dark toggle | 6s usable |

Trim each segment to its beat length in `assemble.sh` (`-ss/-t`), scale-crop
to 1080×1920 (`scale=1080:1920:force_original_aspect_ratio=increase,crop=`),
and cut on the beat grid (see beats.md).

## Music

Slot-based: drop any licensed-free track as `audio/track.mp3` (not committed).
Selection criteria (owner pick): instrumental lo-fi/beat, 96–104 BPM, no
vocals, warm, resolves cleanly at 0:60. Sources: YouTube Audio Library
(royalty-free with attribution where required), Pixabay Music (license-free).
Record the chosen track + license line in this file when picked:

> track: TBD — source/license:

## Assembly

```
# animatic (draft, no captures needed):
tools/make_animatic.py              # → export/animatic.mp4

# final cut:
./assemble.sh                       # reads captures/*.mp4, audio/track.mp3,
                                     # captions.ass → export/hero-ad.mp4
```

Dependencies: ffmpeg, rsvg-convert, ImageMagick, Noto Sans JP + Roboto in
500/700/900 (see `marketing/discord/README.md` for the fetch recipe).

## Captions

`captions.ass` — burned by both pipelines (`subtitles=` filter, or
`ffmpeg -vf "ass=captions.ass"`). Keywords carry frequency-tier colors.
Keep every line inside the bottom-third safe area; max ~7 words per line.

## Publication

Final cut approval is Siri's; publishing rides kanjiverse_app#1089 channels,
sequenced as the first social beat AFTER the revival announcement (#417).
