#!/usr/bin/env bash
# Assemble the Kanjiverse 60s hero ad FINAL cut from real captures.
# Inputs:  captures/beat3.mp4 .. beat8.mp4 (see README capture runbook)
#          audio/track.mp3    (licensed-free track slot — see README)
#          captions.ass       (burned captions)
# Output:  export/hero-ad.mp4 (1080x1920, 30fps, 60s)
set -euo pipefail
cd "$(dirname "$0")"

FPS=30
V="-c:v libx264 -crf 22 -pix_fmt yuv420p -r $FPS"

# beat -> source segment, in-point, duration (see beats.md cut list)
declare -a BEATS=(
  "beat3.mp4 0.0 7.0"
  "beat4.mp4 0.0 8.0"
  "beat5.mp4 0.0 7.0"
  "beat6.mp4 0.0 8.0"
  "beat7.mp4 0.0 8.0"
  "beat8.mp4 0.0 6.0"
)

mkdir -p build export
i=0
for beat in "${BEATS[@]}"; do
  read -r file ss dur <<<"$beat"
  [ -f "captures/$file" ] || { echo "missing captures/$file — see README runbook" >&2; exit 1; }
  ffmpeg -y -loglevel error -ss "$ss" -i "captures/$file" -t "$dur" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=$FPS" \
    $V "build/seg$i.mp4"
  i=$((i+1))
done

# hook + CTA motion-graphics segments from the animatic generator
tools/make_animatic.py --segments-only || true
[ -f build/hook.mp4 ] || { echo "animatic hook/cta segments missing" >&2; exit 1; }

: > build/concat.txt
echo "file 'hook.mp4'" >> build/concat.txt
for ((j=0; j<i; j++)); do echo "file 'seg$j.mp4'" >> build/concat.txt; done
echo "file 'cta.mp4'" >> build/concat.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i build/concat.txt -c copy build/joined.mp4

if [ -f audio/track.mp3 ]; then
  python3 tools/burn_captions.py build/joined.mp4 build/captioned.mp4
  ffmpeg -y -loglevel error -i build/captioned.mp4 -i audio/track.mp3 \
    -shortest $V -c:a aac -b:a 192k -movflags +faststart export/hero-ad.mp4
else
  echo "no audio/track.mp3 — rendering silent cut" >&2
  python3 tools/burn_captions.py build/joined.mp4 export/hero-ad.mp4
fi
echo "ok: export/hero-ad.mp4"
