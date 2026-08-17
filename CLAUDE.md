# DUBPLATE

A jungle / drum & bass tracker for mobile web. One file, no build step, no
dependencies. Written to the spec in `dubplateplan.md` (Amiga ProTracker meets a
pirate-radio studio).

## Ground rules

- Everything lives in `index.html`. Vanilla JS, one `<script>`, no imports, no
  bundler, no runtime dependencies. If a change needs a build step, it is the
  wrong change.
- All default sounds are synthesized in code. **No copyrighted audio ever ships
  in the repo.** The named breaks (AMEN, THINK, …) are groove data played by the
  synth kit, not recordings.
- Canvas only. One bitmap font, no anti-aliasing, integer scaling.
- Skin is Amiga Workbench 1.3: blue `#0055AA`, white, black, orange `#FF8800`.
  Four colours, nothing else. Bevels, no rounded corners over 2px, no shadows,
  no gradients, no transparency.
- Copy rules: one-word labels, all caps, hex where trackers use hex, messages of
  three words or fewer, no helper text, no onboarding, no exclamation points.
- Minimum hit target ~44 css px. `touch-action: none`. First touch anywhere
  resumes the AudioContext.

## Layout of index.html

Read it top to bottom; the sections are in dependency order.

| Section | What it holds |
|---|---|
| FONT | `FONTDATA` — 5x7 glyphs in a 6x8 cell, rows base32 encoded, bit 16 leftmost. Codes 32-95 are ASCII (uppercase only), 96-111 are icons (`I_PLAY`, `I_STOP`, …). `buildFont()` renders one atlas canvas per palette colour. |
| GFX | `resize()` places and sizes the canvas, then picks `PIX` (device pixels per app pixel) so the app grid is ~250 px wide on phones, ~400 on tablets. All drawing is in app pixels. `rect/frame/bevel/panel/dither/text`. Immediate-mode widgets push hit `regions` each frame; pointer events pick the topmost. `insets()` is the safe area (see below). |
| AUDIO | `createEngine(ac)` builds the whole graph and is called for both the live context and the `OfflineAudioContext` renderer. Master: gain → soft-clip waveshaper → compressor. Sends: tempo-synced dub delay with a lowpass in the feedback loop, and a convolver reverb with a generated dark impulse. Six channel strips: in → lowpass → crush waveshaper → post-crush lowpass → vol → dry + 2 sends. |
| INSTRUMENTS | `INSTDEF` is the parameter schema; the INST screen renders itself from it, so adding a parameter is a one-line change. `trigger(E,o)` dispatches by `inst.t`. `monoVoice` handles SUB / REESE / WOBBLE with voice steal and glide. |
| BREAKS | `PRESETS` — eight breaks, each a 16-slice map over the synth kit plus a 32-row groove. `LIB` holds presets first, then imports. Preset and sampled breaks share the same note column (`S01`-`S32`), so any pattern plays with any break. |
| PROJECT / SEQ | Data model, `scheduleRow()` (the only place notes get turned into sound), lookahead scheduler on a 25 ms `setInterval` scheduling 140 ms ahead. `lookahead()` finds the next event on a channel to get note length and whether the next note glides. |
| SAMPLES | Import pipeline: trim → snap to first transient → `analyzeTempo` → bars/BPM → slice. `findOnsets` is amplitude-flux with an adaptive threshold; `analyzeTempo` autocorrelates that flux and then snaps to a whole number of bars. |
| STORE | IndexedDB (`projects`, `library`), JSON export with breaks embedded as base64 WAV, `renderWAV()` offline render. |
| UI / SCREENS / DRAWER | SONG, PATTERN (narrow and a landscape all-channels view), PADS, CHOP, INST, MIX, DISK. The long-press drawer is the note/instrument/effect editor. |
| DEMO / BOOT | `demoProject()` builds the tune that plays on first load. `BAKED` is the starter-bank hook (see below). |

## Data model

```json
{ "name":"UNTITLED", "bpm":170, "swing":0, "master":0.85,
  "inst":[{"t":"reese","n":"REESE","p":{}}],
  "chan":[{"inst":0,"brk":"p0","vol":0.8,"cut":1,"res":0.1,"crush":0,"dly":0,"rev":0,"mute":false,"solo":false}],
  "pat":[{"id":0,"ch":0,"rows":[{"n":"S01","i":0,"f":"9","v":32}]}],
  "song":[[0,-1,2,3,-1,-1]],
  "breaks":[{"id":"u…","sid":"s…","slices":[{"t":0.0,"p":0,"r":0,"g":1}],"wav":"<base64>"}] }
```

- Six channels: BRK1, BRK2, SUB, REESE, STAB, FX. Patterns are per channel,
  32 rows (2 bars of 16ths), 6 ticks per row.
- A song row is a slot; every channel advances together, 32 rows per slot.
- `null` in `rows` is an empty row. `"OFF"` is a note-off.
- Effects, one per row: `9` offset · `R` retrigger (ticks) · `B` reverse ·
  `P` pitch (signed byte) · `G` glide · `C` cutoff · `T` grain stretch ·
  `V` volume (`80` = 100%).

## Working on this

- Build/run: open `index.html`. There is nothing to install.
- Test with a headless browser: check for zero page errors, then render a few
  bars through an `OfflineAudioContext` and assert the peak is non-zero. Silence
  and thrown scheduler exceptions are the two failure modes that matter, and
  both are invisible in a screenshot.
- Every note path must work in the offline renderer too. Anything that reaches
  for the live `ac` or `E` inside `trigger`/`kitVoice`/`playBreak` will break
  WAV export.
- Never call `.start()` twice on an oscillator, and never pass a non-finite time
  to `.stop()`. Both throw and kill the whole scheduler tick.
- Do not shadow window globals with `var` at top level (`screen`, `stop`,
  `name`, `length`, `status`). `scrn` is named that way for this reason.

## iOS home screen

Two things bite once the app is added to the home screen, and both are handled
in code because neither can be fixed from CSS alone.

- **Safe area.** Added to the home screen, iOS reports
  `safe-area-inset-bottom: 0` while still drawing the home indicator over the
  page. `insets()` reads what iOS reports through the hidden `#sa` probe and
  then applies a floor of its own — 28 css px portrait, 16 landscape — when the
  window covers the whole screen (`coversScreen()`) on a gesture-bar phone
  (`gestureBar()`). A real reported inset always wins, so a device that says 34
  gets 34 and never doubles up. `resize()` places the canvas from those numbers;
  nothing about the layout comes from `env()` in CSS.
- **Stale copy.** iOS keeps the HTML it installed, so a deploy can go unseen for
  days. `var BUILD` at the top of the file is the stamp; `checkUpdate()` fetches
  the page once per session with `cache:"reload"`, compares the stamp and
  reloads if it changed (guarded by `sessionStorage` so it can never loop).
  **Bump `BUILD` on every deploy** or the check is useless.

The DISK screen prints `B<build> T<top> B<bottom> <screen> <grid> SA` along the
bottom. That line is the first thing to ask for when a layout bug is reported
from a phone — it says which build is running and what iOS claimed.

## Starter bank

`index.html` has a `/* BAKE:START */ … /* BAKE:END */` block holding
`var BAKED = []`. `python3 bake.py` base64-embeds every WAV in `breaks/` into
that block; the app decodes them at boot and puts them in the LIBRARY, analysed
and sliced. `breaks/` is gitignored and the committed build ships the mechanism
empty — that is deliberate, keep it that way.

## Not done yet

Resample-a-channel, `.mod` export, zip kit export (currently one WAV plus a JSON
slice map), per-channel swing, pattern-share URLs.
