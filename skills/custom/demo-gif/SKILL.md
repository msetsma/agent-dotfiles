---
name: demo-gif
description: Create a polished visual demo (usually an animated GIF or short screencast) of an application, choosing the right recording approach for the app type — terminal recorder for CLI/TUI apps, headless browser for web/GUI apps, and a driven-request or generated view for backend-only services. Use when the user wants to record, generate, regenerate, or tune a demo GIF, screencast, or animated preview of an app, mentions "demo gif", "screencast", "record a demo", "show off the app", asciinema/vhs/terminalizer, Playwright/Puppeteer recording, or webm/mp4 to GIF conversion.
---

# Record a Demo GIF

Produce a clean, self-running visual of an app — no manual clicking. The right
capture method depends on the app's interface, so **first classify the app, then
pick a track**. All tracks converge on the same finishing step: convert the raw
capture to an optimized, optionally captioned GIF.

## Step 1 — Classify the app

Inspect the project (entry point, framework, how a user actually interacts) and
pick the interface type. If unclear, ask the user.

| Interface | Examples | Track |
|-----------|----------|-------|
| CLI / TUI | argparse/click, cobra, ink, ratatui, REPL | **A. Terminal** |
| Web / GUI | React/Vue/Svelte SPA, server-rendered pages, Electron | **B. Browser** |
| Backend only | REST/gRPC API, worker, library, daemon | **C. Backend** |

## Step 2 — Capture (choose one track)

### A. Terminal (CLI / TUI)
Use a purpose-built terminal recorder — never screen-record a window.
- **vhs** (recommended): write a `.tape` script of keystrokes → renders GIF/MP4
  directly and deterministically. Best for scripted, repeatable demos.
- **asciinema** + **agg**: record a real session to a cast, convert to GIF.
- **terminalizer**: record + render, config-driven theming.
Drive the app with a fixed sequence of commands/inputs so the run is repeatable.

### B. Browser (Web / GUI)
Use a headless-browser driver (**Playwright** recommended, or Puppeteer) to:
1. Launch the app, wait for a readiness signal (health endpoint / element).
2. Drive the real UI through a scripted flow, recording to `.webm`/`.mp4`.
3. Prefer **adaptive driving** for stateful/AI apps: after each step read app
   state (an API/DOM signal) to decide the next input, so the demo survives
   reordering or dynamic follow-ups. Use a fixed sequence for simple UIs.

### C. Backend only (no UI)
There is nothing to "watch", so **synthesize** a view — think about what best
communicates the behavior, then record it as a Terminal (Track A) capture:
- Scripted request/response walkthrough (`curl`/`httpie`/`grpcurl`) showing
  input → output, ideally with pretty-printed JSON.
- A short client script that exercises the API and prints results/timings.
- A live log/metrics stream during a representative operation.
- If a demo UI adds real value, stand up a minimal one (e.g. the API's built-in
  Swagger/OpenAPI page) and switch to Track B.
Ask the user which framing they want if more than one fits.

## Step 3 — Finish: optimize to GIF

For any **video** capture (Tracks B/C-recorded), convert with a bundled helper
that uses a two-pass ffmpeg palette for clean colors plus speed/size controls:

```bash
scripts/video_to_gif.sh INPUT.webm OUTPUT.gif
```

Tune via env vars: `GIF_SPEED` (default `2.5`, trims dead air), `GIF_FPS`
(`10`), `GIF_WIDTH` (`820`), and `CAPTION_IMG` (a PNG banner to overlay; `none`
to skip). Terminal recorders that emit GIF directly can skip this step, or emit
video and pass it through the helper for consistent sizing.

## Techniques that make a demo good

- **Deterministic & scripted** — repeatable inputs; no live hand-driving.
- **Show the logic, not just the UI** — for evaluative/AI flows, seed a weak
  input so the app pushes back, then a strong one it accepts, making the
  decision loop visible.
- **Caption banner** — a one-line overlay stating what to notice. Render it as an
  image (perfect fonts/emoji) and overlay via ffmpeg; works even when ffmpeg
  lacks `drawtext`.
- **Speed up** to cut latency/dead air; keep width/fps modest for small files.

## Details

Per-track tooling, install commands, a Playwright driver skeleton, and the
caption-overlay recipe are in [REFERENCE.md](REFERENCE.md). The finishing
converter is bundled at [scripts/video_to_gif.sh](scripts/video_to_gif.sh).
