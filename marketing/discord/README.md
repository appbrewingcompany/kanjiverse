# Kanjiverse Discord asset pack

Server look derived from the [creative direction](../creative-direction.md).
Application is owner-side (Siri); this pack is the look, not the posting —
announcement and ad posts ride #417 and kanjiverse_app#1089.

Server: discord.com/invite/YbmXmAGfdf (linked from the landing page and the
app's social buttons).

## Files

| File | Use | Spec |
|---|---|---|
| `icon.png` | Server icon | 1024×1024 PNG (Discord minimum 512) |
| `banner.png` | Server banner | 960×540 PNG |
| `src/icon.svg`, `src/banner.svg` | Editable sources | Self-contained SVG |
| `src/mark.svg` | The Kanjiverse mark (canonical extraction from the site logo) | 24×24 viewBox, single path, `currentColor` |

Banner display is boost-gated on Discord (historically Level 2 for static
banners; the boosting model changed in 2026 — check the server's current perks
at apply time). The banner ships regardless; if display is gated, the pack
leans on icon + server description + welcome copy.

## Server description (settings → overview, ≤120 chars)

> The Japanese learner's dictionary — kanji, words & sentences, color-coded by frequency. Look it up. Learn what matters.

(119 characters.)

## Welcome channel copy

> **ようこそ！ Welcome to Kanjiverse** — the home of the Japanese learner's
> dictionary that shows what's worth learning.
>
> - **#support** — stuck on a lookup or a setting? Ask here.
> - **#feature-talk** — ideas, wishes, thing you wish the dictionary did.
> - **#release-notes** — what's new; the app is back in active development.
> - **#show-your-setup** — your themes, fonts, and study lists.
>
> Be kind, stay on topic, and keep it learner-friendly. 日本語 OK!

## About channel copy

> **Kanjiverse** is a Japanese learner's dictionary for phone, tablet, and
> browser — kanji, words, and example sentences in one place, everything
> color-coded by frequency so you instantly see what is actually worth
> learning.
>
> - Download: iOS & Android — kanjiverse.com
> - Also in your browser: app.kanjiverse.com
> - Feedback goes straight to the team from inside the app.
>
> This server is the community room: study talk, feature discussion, release
> news, and the people building it.

## Apply (owner steps)

1. Server Settings → Overview → upload `icon.png`.
2. Server Settings → Overview → Server Banner → upload `banner.png` (if the
   perk is available; otherwise keep it for when it is).
3. Server Settings → Overview → Server Description → paste above.
4. `#welcome` / `#about` channels → paste copy, adjust channel names to the
   server's actual layout.

## Regenerating the assets

Fonts: Noto Sans JP (400/500/700/900) and Roboto (500/700/900) must be
installed (Google Fonts, OFL/Apache-2.0). Render with:

```
rsvg-convert -w 1024 -h 1024 src/icon.svg -o icon.png
rsvg-convert -w 960 -h 540 src/banner.svg -o banner.png
```

After editing `src/mark.svg`, re-inline its path into `icon.svg` and
`banner.svg` (replace the `<path d="…">` inside the `<g transform>` groups) —
the two render sources are kept self-contained on purpose.
