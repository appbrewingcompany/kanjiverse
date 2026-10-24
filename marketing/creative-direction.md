# Kanjiverse creative direction

The single brand source for every marketing surface: the site (kanjiverse_site),
the store screenshots (kanjiverse_app#1099), the hero ad (#429), the Discord pack
(#430), and the social style guide (kanjiverse_app#1089). Everything here is
derived from the app's live design system — `kanjiverse_models` themes,
`kanjiverse_app/kanjiverse/lib/app/theme.dart` — so marketing and product move
together.

## Positioning

**Kanjiverse is a deep Japanese dictionary you can make yours.** Look up any
kanji, word, or sentence; color-coding shows what is actually worth learning;
themes and fonts let every learner shape the app into their own study space.

Two showcase anchors, in this order:

1. **The dictionary** — kanji, words, sentences, decomposition, stroke order.
2. **The themes** — frequency palettes, light/dark, nine Japanese typefaces.

AI features appear only as supporting detail in feature lists — never in a
hook, tagline, thumbnail, or video opener. The hook is always a dictionary
moment: a glyph, a lookup, a color reveal.

## Voice

Plain, warm, learner-to-learner. Short sentences. Concrete verbs. English by
default, Japanese terms in Japanese where the product uses them (kanji,
furigana, JLPT).

- Say "look up", "see", "learn" — not "unlock the power of", "revolutionize",
  "supercharge".
- Frequency is the signature claim: **"instantly see what is worth learning."**
- Confidence without hype: the product is deep; the copy doesn't need to shout.
- One exclamation mark per surface, maximum. Usually zero.

Reference copy: the refreshed store listing (kanjiverse_app fastlane metadata)
is the canonical voice sample — "Japanese learner's dictionary: kanji, words and
sentences in one app."

## Color

The brand palette IS the app's frequency color-coding. Six tiers, named after
how often a word is actually used:

| Tier | Meaning (usage percentile) | Default (700) | Vivid (500) | Pastel (300) |
|---|---|---|---|---|
| Common | top 80% most used | `#303F9F` indigo | `#3F51B5` | `#7986CB` |
| Uncommon | 20% least used | `#512DA8` deep purple | `#673AB7` | `#9575CD` |
| Rare | 5% least used | `#7B1FA2` purple | `#9C27B0` | `#BA68C8` |
| Epic | 1% least used | `#AF1781` magenta | `#E91E63` | `#F06292` |
| Legendary | 0.1% least used | `#D32F2F` red | `#F44336` | `#E57373` |
| (Unclassified) | unknown | `#E64A19` deep orange | `#FF5722` | `#FFB74D` |

**Uncommon — deep purple — is the brand primary.** It is the app's default
scheme seed and the through-line of the interface; every CTA, logo lockup, and
link color sits in the deep-purple family (`#512DA8` for text and accents,
`#673AB7` for large fills on light surfaces).

Rules:

- **The brand gradient** is the tier sequence itself:
  `linear-gradient(90deg, #303F9F, #512DA8, #7B1FA2, #AF1781, #D32F2F)`.
  Use it as the hero sweep — headline fills, section underlines, the ad's
  progress bar. Never as a full-bleed background behind body text.
- Use **default (700)** for type, icons, and accents on white; **vivid (500)**
  for large fills, gradients, and dark-on-dark moments; **pastel (300)** only
  inside light pastel surfaces or as tints/fills of chips.
- Tier colors are semantic — they always mean frequency. Never recolor the
  sequence for decoration; never use one tier's hue as a neutral.
- Surfaces follow Material 3 tonal neutrals: near-white `#FFFFFF`/`#F7F2FA`
  in light, `#141218`-family dark surfaces with `#E6E0E9`-family text in dark.
  Dark mode is a first-class look — at least one dark surface appears in every
  multi-shot asset set.
- White space is the frame. Screenshots, glyphs, and headline words float on
  flat surfaces — no drop shadows heavier than M3 elevation, no stock-photo
  backgrounds, no clutter.

## Typography

- **Latin/UI: Roboto** (Medium for headings, Regular for body). Tight tracking
  on display sizes (−1% at 48px+), generous leading on body (150%).
- **Japanese: Noto Sans JP** is the default face; it is also the marketing
  default for Japanese strings. The other eight learner-selectable families —
  M PLUS 1p, M PLUS Rounded 1c, Kosugi, Kosugi Maru, Sawarabi Mincho,
  Sawarabi Gothic, Hachi Maru Pop, Yusei Magic — are a showcase surface: use
  them (labeled) when the asset is about customizing the look, never mix more
  than two in one frame.
- **The kanji glyph is the hero object.** Display glyphs run huge (a single
  漢字 can fill a 9:16 frame), set in the kanji display face, colored by its
  frequency tier or in the brand gradient. Latin copy around glyphs stays
  small and quiet.
- Furigana (ruby) over kanji is a signature texture — use real, correct
  pairings when showing reading UI; wrong furigana is a brand defect.

## Shape & texture

Material 3 geometry: sheets and dialogs at 28dp top corners, buttons pill-shaped
(24dp+ radius), cards on `surfaceContainer` tones with hairline separation, not
hard borders. Glyph-graph nodes are circles with 2dp tier-colored rings. The
look is soft, layered, print-calm — closer to a well-set textbook than a game.

## Motion

The app feels like pages easing forward, never sliding sideways.

- **Signature move: stroke order.** A kanji draws itself stroke by stroke —
  this is the brand's motion metaphor and the hero-ad opener. Use the
  draw-on reveal whenever a glyph enters a frame.
- Transitions are **fade-forward** (M3): incoming content rises slightly and
  fades in (~300ms, standard easing). Tab switches crossfade; nothing slides
  horizontally.
- Color reveals (a list flipping to frequency colors, a theme switch) ease
  over ~250ms — color change itself is the event; don't mask it with movement.
- In video: cuts on the beat, motion between cuts calm and few — one idea per
  shot. Screen content is the animation; overlay graphics stay minimal.

## Surface rules

- **Site (kanjiverse.com):** one page, dictionary-first hero ("Learn kanji.
  Build your vocabulary. Read real Japanese." lineage), frequency gradient as
  the section rhythm, real app screens over mockups, dark-mode section
  included, store badges as terminal CTAs.
- **Store screenshots:** branded frames, tier-colored caption bars, one
  feature per frame, dictionary beats first, themes beat last, no AI frame in
  the first three slots.
- **Hero ad (60s, 9:16):** hook = a glyph drawing itself + "The Japanese
  dictionary that shows what's worth learning." → dictionary beats → theme
  aesthetic → CTA. Burned captions in Roboto, tier-colored keywords.
- **Discord:** icon = the Kanjiverse mark (deep purple on gradient or
  reverse), banner = gradient sweep with hero glyphs; welcome copy in the
  voice above.
- **Never:** AI in a hook; rainbow gradients unrelated to the tier sequence;
  katakana-English decoration ("スゴイ!!" bursts); before/after shame frames;
  stock photos of students.

## Tokens (machine-readable)

```yaml
primary: "#512DA8"
primary_fill: "#673AB7"
on_primary: "#FFFFFF"
surface_light: "#FFFFFF"
surface_light_alt: "#F7F2FA"
surface_dark: "#141218"
on_surface_dark: "#E6E0E9"
tiers:
  common:    { default: "#303F9F", vivid: "#3F51B5", pastel: "#7986CB" }
  uncommon:  { default: "#512DA8", vivid: "#673AB7", pastel: "#9575CD" }
  rare:      { default: "#7B1FA2", vivid: "#9C27B0", pastel: "#BA68C8" }
  epic:      { default: "#AF1781", vivid: "#E91E63", pastel: "#F06292" }
  legendary: { default: "#D32F2F", vivid: "#F44336", pastel: "#E57373" }
  unclassified: { default: "#E64A19", vivid: "#FF5722", pastel: "#FFB74D" }
brand_gradient: "linear-gradient(90deg,#303F9F,#512DA8,#7B1FA2,#AF1781,#D32F2F)"
font_latin: "Roboto"
font_japanese: "Noto Sans JP"
radius_dialog: 28
radius_button: 24
```
