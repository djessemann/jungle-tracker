# DUBPLATE

A jungle / drum & bass box for mobile web. One file, no build step, no
dependencies. Started from `dubplateplan.md` (a ProTracker style tracker) and
was then deliberately stripped back: the tracker was too much on a phone, so
the pattern grid, song arranger, hex effect column and instrument parameter
pages are gone. What is left is a step sequencer you paint with your thumb.
The audio engine, the break presets and the import pipeline are unchanged.

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
- Copy rules: one-word labels, all caps, messages of three words or fewer, no
  helper text, no onboarding, no exclamation points.
- **Nothing on screen may need explaining.** A control that only applies
  sometimes is hidden the rest of the time — see the break screen, which shows
  slicing controls only for a sampled break.
- Minimum hit target ~44 css px. `touch-action: none`. First touch anywhere
  resumes the AudioContext.

## The shape of the app

Three tabs and one transport bar. That is the whole surface.

- **BEAT** — four lanes (BREAK BASS STAB FX) of sixteen steps, a palette of
  sounds for the selected lane, and three faders. Pick from the palette, tap
  steps. Tapping a step that already holds that exact value clears it; holding
  a step always clears it. REV and ROLL are sticky brushes: arm one and the
  steps you paint carry the flag.
- **BREAK** — the library. Browse presets and your imports, LOAD more, slice
  8/16/32 or AUTO (transients), drag markers, FILL BEAT.
- **SAVE** — save, load, name, render, and the machine line.

Scenes A B C D live in the transport bar. Tapping one while stopped switches
immediately; while playing it queues and lands on the next bar (the pending
scene shows orange). CHN plays the scenes that have something in them, in
order, forever.

## Layout of index.html

Read it top to bottom; the sections are in dependency order.

| Section | What it holds |
|---|---|
| FONT | `FONTDATA` — 5x7 glyphs in a 6x8 cell, rows base32 encoded, bit 16 leftmost. Codes 32-95 are ASCII (uppercase only), 96-111 are icons. `buildFont()` renders one atlas canvas per palette colour. |
| GFX | `resize()` places and sizes the canvas, then picks `PIX` (device pixels per app pixel) so the app grid is ~250 px wide on phones, ~400 on tablets. All drawing is in app pixels. Immediate-mode widgets push hit `regions` each frame; pointer events pick the topmost. `insets()` is the safe area (see below). |
| AUDIO | `createEngine(ac)` builds the whole graph and is called for both the live context and the `OfflineAudioContext` renderer. Master: gain → soft-clip waveshaper → compressor. Sends: tempo-synced dub delay with a lowpass in the feedback loop, and a convolver reverb with a generated dark impulse. Four channel strips, one per lane. |
| INSTRUMENTS | `trigger(E,o)` dispatches by `inst.t`. `monoVoice` handles the bass with voice steal and glide. `INSTDEF` still describes every parameter; the app now picks fixed values in `buildInst()` instead of exposing them. |
| BREAKS | `PRESETS` — eight breaks, each a 16-slice map over the synth kit plus a 32 step groove. `LIB` holds presets first, then imports. Preset and sampled breaks are interchangeable: a step just holds a slice number. |
| MODEL | Lanes, steps, scenes. `scheduleStep()` is the only place a step turns into sound. `fillBreak()` lays a break onto the grid. Lookahead scheduler on a 25 ms `setInterval` scheduling 140 ms ahead. |
| SAMPLES | Import pipeline: trim → snap to first transient → `analyzeTempo` → bars/BPM → slice. `findOnsets` is amplitude-flux with an adaptive threshold; `analyzeTempo` autocorrelates that flux and then snaps to a whole number of bars. |
| STORE | IndexedDB (`projects`, `library`), JSON export with the break embedded as base64 WAV, `renderWAV()` offline render. |
| UI / SCREENS | Transport, tabs, widgets, then `drawBeat` / `drawBreak` / `drawSave`. |
| DEMO / BOOT | `demoProject()` builds the two scenes that play on first load. `BAKED` is the starter-bank hook (see below). |

## Data model

```json
{ "name":"UNTITLED", "bpm":170, "swing":14, "master":0.85, "key":0,
  "brk":"p0", "chain":true, "ver":2,
  "lane":[{"vol":0.85,"tone":1,"fx":0.08,"mute":false}],
  "scenes":[ [ [ {"v":5,"r":0,"o":1}, null ] ] ],
  "breaks":[{"id":"u…","sid":"s…","slices":[{"t":0.0,"p":0,"r":0,"g":1}],"wav":"<base64>"}] }
```

- `scenes[scene][lane][step]`, four scenes, four lanes, sixteen steps.
- A step is `null` or `{v,r,o}` — palette value, reverse, roll.
- `v` means a slice number 1-16 on the BREAK lane, and an index into `SCALE`,
  `STABROOT` or `FXPAD` on the others. Notes never leave the scale, so the
  palette cannot produce a wrong note.
- Two adjacent bass steps glide into each other. That is the only hidden rule
  in the app, and it is what makes the sub slide.

## Working on this

- Build/run: open `index.html`. There is nothing to install.
- Test with a headless browser: check for zero page errors, then render a few
  bars through an `OfflineAudioContext` and assert the peak is non-zero. Silence
  and thrown scheduler exceptions are the two failure modes that matter, and
  both are invisible in a screenshot.
- Every path must work in the offline renderer too. Anything that reaches for
  the live `ac` or `E` inside `trigger`/`kitVoice`/`playBreak` will break WAV
  export.
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
  (`gestureBar()`). A real reported inset always wins.
- **Stale copy.** iOS keeps the HTML it installed. `var BUILD` at the top of the
  file is the stamp; `checkUpdate()` fetches the page once per session with
  `cache:"reload"`, compares the stamp and reloads if it changed (guarded by
  `sessionStorage` so it can never loop). **Bump `BUILD` on every deploy.**

The SAVE screen prints `B<build> T<top> B<bottom> <screen> <grid> SA` along the
bottom. Ask for that line first when a layout bug is reported from a phone.

## Starter bank

`index.html` has a `/* BAKE:START */ … /* BAKE:END */` block holding
`var BAKED = []`. `python3 bake.py` base64-embeds every WAV in `breaks/` into
that block; the app decodes them at boot and puts them in the library, analysed
and sliced. `breaks/` is gitignored and the committed build ships the mechanism
empty — that is deliberate, keep it that way.

## Not done yet

Per-scene copy/paste, step probability, resample-a-channel, `.mod` export, zip
kit export (currently one WAV plus a JSON slice map), pattern-share URLs.
