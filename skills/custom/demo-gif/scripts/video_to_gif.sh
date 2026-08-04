#!/usr/bin/env bash
# Convert a screen/browser recording (.webm/.mp4/.mov) into an optimized GIF.
#
# Stack-agnostic: works with any video produced by Playwright, Puppeteer, screen
# recorders, or terminal tools that emit video. Uses a two-pass ffmpeg palette
# (palettegen / paletteuse) for clean colors, plus a configurable speed-up to
# trim dead air. If a caption banner PNG is provided, it is overlaid onto an
# added top margin (works even when the ffmpeg build lacks the drawtext filter).
#
# Usage:
#   scripts/video_to_gif.sh [INPUT_VIDEO] [OUTPUT_GIF]
#
# Defaults:
#   INPUT_VIDEO   recording.webm
#   OUTPUT_GIF    demo.gif
#
# Environment:
#   GIF_FPS      Output frames per second (default 10)
#   GIF_WIDTH    Output width in px, height auto (default 820)
#   GIF_SPEED    Playback speed multiplier, >1 is faster (default 2.5)
#   CAPTION_IMG  Banner PNG to overlay onto a top margin. "none" (default)
#                disables the banner. Its height is read via ffprobe.
set -euo pipefail

INPUT="${1:-recording.webm}"
OUTPUT="${2:-demo.gif}"
FPS="${GIF_FPS:-10}"
WIDTH="${GIF_WIDTH:-820}"
SPEED="${GIF_SPEED:-2.5}"
CAPTION_IMG="${CAPTION_IMG:-none}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found. Install it (e.g. 'brew install ffmpeg')." >&2
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Input video not found: $INPUT" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"

PALETTE="$(mktemp -t demo-gif-palette).png"
trap 'rm -f "$PALETTE"' EXIT

# Common time/scale filter applied in both passes.
VF_BASE="setpts=PTS/${SPEED},fps=${FPS},scale=${WIDTH}:-1:flags=lanczos"

USE_CAPTION=0
if [ "$CAPTION_IMG" != "none" ] && [ -f "$CAPTION_IMG" ]; then
  USE_CAPTION=1
  BAR_H="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$CAPTION_IMG")"
fi

if [ "$USE_CAPTION" = "1" ]; then
  echo "[video_to_gif] Banner: ${CAPTION_IMG} (h=${BAR_H}px)  speed=${SPEED}x fps=${FPS} width=${WIDTH}"
  # Pad a top margin, overlay the banner image, then speed/scale. [v] feeds both passes.
  CHAIN="[0:v]pad=iw:ih+${BAR_H}:0:${BAR_H}:color=0x000000[vp];[vp][1:v]overlay=0:0[bn];[bn]${VF_BASE}[v]"
  echo "[video_to_gif] Generating palette"
  ffmpeg -y -loglevel error -i "$INPUT" -i "$CAPTION_IMG" \
    -filter_complex "${CHAIN};[v]palettegen=stats_mode=diff[p]" -map "[p]" "$PALETTE"
  echo "[video_to_gif] Encoding GIF -> ${OUTPUT}"
  ffmpeg -y -loglevel error -i "$INPUT" -i "$CAPTION_IMG" -i "$PALETTE" \
    -filter_complex "${CHAIN};[v][2:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[o]" \
    -map "[o]" "$OUTPUT"
else
  echo "[video_to_gif] No banner  speed=${SPEED}x fps=${FPS} width=${WIDTH}"
  CHAIN="[0:v]${VF_BASE}[v]"
  echo "[video_to_gif] Generating palette"
  ffmpeg -y -loglevel error -i "$INPUT" \
    -filter_complex "${CHAIN};[v]palettegen=stats_mode=diff[p]" -map "[p]" "$PALETTE"
  echo "[video_to_gif] Encoding GIF -> ${OUTPUT}"
  ffmpeg -y -loglevel error -i "$INPUT" -i "$PALETTE" \
    -filter_complex "${CHAIN};[v][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[o]" \
    -map "[o]" "$OUTPUT"
fi

SIZE="$(du -h "$OUTPUT" | cut -f1)"
echo "[video_to_gif] Wrote ${OUTPUT} (${SIZE})"
