# Demo-Recording Reference

Detailed per-track tooling and recipes. Pick the track from SKILL.md Step 1.
Nothing here is tied to a specific language or framework — adapt selectors,
commands, and readiness checks to the target app.

## A. Terminal (CLI / TUI)

### vhs (recommended — scripted, deterministic)
Install: `brew install vhs` (or `go install github.com/charmbracelet/vhs@latest`).
Write a `.tape` describing the session, then `vhs demo.tape`:

```tape
Output demo.gif
Set FontSize 20
Set Width 1200
Set Height 700
Type "myapp --help"
Enter
Sleep 1s
Type "myapp run --input sample.json"
Enter
Sleep 3s
```

vhs renders GIF/MP4/WebM directly — no separate conversion needed. Prefer it for
repeatable demos because the tape is the script.

### asciinema + agg (record a real session)
```bash
asciinema rec demo.cast        # run your commands, exit to stop
agg demo.cast demo.gif         # convert cast -> GIF
```
Good when you want a genuine interactive session rather than a scripted tape.

### terminalizer
`terminalizer record demo` then `terminalizer render demo` — config-driven
frames/theme; heavier output than vhs/agg.

Tips: set an explicit terminal size, keep the font large enough to read at GIF
scale, and insert deliberate `Sleep`/pauses so viewers can follow.

## B. Browser (Web / GUI)

Install (Playwright): `npm i -D playwright && npx playwright install chromium`
(or the Python package + `playwright install chromium`).

Record by launching a context with video enabled, driving the UI, then closing
the context to flush the video. Skeleton (JS; the Python API mirrors this):

```js
const { chromium } = require('playwright');
const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1280, height: 800 },
  recordVideo: { dir: 'out/', size: { width: 1280, height: 800 } },
});
const page = await context.newPage();
await page.goto(APP_URL, { waitUntil: 'networkidle' });
// ... drive the flow: click, fill, type (with a small delay), wait for responses ...
await context.close();   // finalizes the .webm
await browser.close();
```

Readiness: poll a health endpoint or `waitForSelector` before driving. Robust
waits: `page.expect_response(...)` on the network call each action triggers,
rather than fixed sleeps.

### Adaptive driving (stateful / AI apps)
Instead of a fixed click list, loop: read app state (an API like
`GET /state/{id}`, or a DOM signal) → decide the next input from a map keyed by
the current step → send it. This survives dynamic ordering and follow-up prompts.
An answer value can be a list where early entries are intentionally weak (to
trigger a rejection/follow-up) and the last is the accepted one — this visibly
demonstrates evaluation logic.

Alternatives: Puppeteer (Chrome), or Playwright's built-in `codegen` to bootstrap
selectors. Convert the resulting `.webm`/`.mp4` with the Step 3 helper.

## C. Backend only (no UI)

Decide what best communicates behavior, then usually record it as Track A:

- **Request/response walkthrough**: script `curl`/`httpie`/`grpcurl` calls and
  pretty-print output (`| jq`). Record the terminal with vhs.
- **Client script**: a short program that calls the API and prints inputs,
  outputs, and timings in a readable sequence.
- **Log / metrics stream**: run a representative job and record the streaming
  logs or a `watch`ed metrics view.
- **Generated UI**: if the service exposes Swagger/OpenAPI or a playground,
  drive that with Track B instead.

## Step 3 — Caption banner overlay

Render the banner as an image (so fonts/emoji are exact), then overlay it onto a
padded top margin during conversion. Example: render an HTML bar to `caption.png`
(headless browser screenshot, or ImageMagick), then:

```bash
CAPTION_IMG=caption.png scripts/video_to_gif.sh in.webm out.gif
```

The bundled `scripts/video_to_gif.sh` handles both the two-pass palette and the
optional overlay; set `CAPTION_IMG=none` (default) to skip the banner.

## Troubleshooting

- **GIF too large** — lower `GIF_WIDTH`/`GIF_FPS`, raise `GIF_SPEED`, or shorten
  the script. GIF is lossless-palette; prefer MP4/WebM for long demos.
- **`ffmpeg`/`ffprobe` not found** — `brew install ffmpeg`.
- **Blank/short web video** — you must `context.close()` before reading the path;
  ensure the flow actually ran and readiness waits passed.
- **Unreadable terminal GIF** — increase font size / terminal dimensions.
- **Flaky browser timing** — replace fixed sleeps with response/selector waits.
