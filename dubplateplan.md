# DUBPLATE — a jungle / drum & bass tracker for mobile web

Working title: **Dubplate**. (A dubplate is the one-off acetate junglists cut to test tunes.)
Backup names: Rinse, Rollout, Junglizm.

## 1. The goal

Make a mobile web app that lets one person write a jungle tune in ten minutes.
The core loop: chop a break, roll a sub, drop a Reese, stab a chord, arrange, export.
The feel: Amiga ProTracker meets a pirate-radio studio. Fast, gritty, hex numbers, no menus.

## 2. Ground rules

- One `index.html`. Vanilla JS. No build step. No runtime dependencies.
- Works offline on iPad and iPhone Safari. Add-to-home-screen meta tags.
- All default sounds are **synthesized** in code. Ship zero copyrighted audio.
- User can import their own break WAVs. The app treats imports as first-class. Every import gets a slice map and lands in a LIBRARY that all projects share.
- Canvas UI with a bitmap font. Skin: **Amiga Workbench** (decided). Copy rules in section 6b.
- Audio: Web Audio API only. No AudioWorklet needed for v1.
- Keep it a repo with one HTML file plus a `CLAUDE.md`, like the nes-tracker project.

## 3. Prior art (what to steal)

| Program | What it proves | What to take |
|---|---|---|
| BassoonTracker (web) | A full ProTracker clone runs in plain JS in mobile Safari | The 9xx sample-offset chop command; in-app sample slicing; MOD effect vocabulary |
| LSDJ / LittleGPTracker | Trackers work on tiny screens with almost no buttons | One channel per screen; short reusable patterns; song = grid of pattern IDs |
| Koala Sampler | The modern mobile jungle workflow | Auto-chop; pads; resampling; "Retro" timestretch mode |
| ReCycle / REX files | Slice a loop once, play it at any tempo | Transient slicing; slices become notes; spread-to-sequence |
| ProTracker (Amiga) | The original jungle tool | 4-channel mindset; hex everywhere; sample-first design |
| Polyend Tracker / M8 | Modern hardware tracker UX | Screen-per-task navigation; big playhead; instant audition |

Links at the bottom.

## 4. Sound set

### 4a. Breaks (the heart of it)

Ship these as **pattern presets**: groove data that plays the built-in synth kit in the style of each break. Rhythms are not recordings. This is legally clean.
When the user imports a real break, the same presets act as chop maps.

| Preset name | Source record | Year | Character |
|---|---|---|---|
| AMEN | The Winstons — "Amen, Brother" | 1969 | The one. Frantic, scratchy ride, ghost snares |
| THINK | Lyn Collins — "Think (About It)" | 1972 | Crunchy shuffle, whip-crack snare, tambourine |
| FUNKY | James Brown — "Funky Drummer" | 1970 | Loose, rolling, hi-hat 16ths |
| APACHE | Incredible Bongo Band — "Apache" | 1973 | Bongos, airy, the "intelligent" choice |
| HOTPANTS | Bobby Byrd — "Hot Pants" | 1971 | Tight, dry, funky |
| COLDSWEAT | James Brown — "Cold Sweat" | 1967 | Sparse, heavy backbeat |
| SESAME | Blowfly — "Sesame Street" | 1974 | Bouncy, ragga-jungle staple |
| ASSEMBLY | Commodores — "Assembly Line" | 1974 | Rolling toms, tearout favorite |

Default tempo 170 BPM. Range 120–200. Classic jungle sits 155–175.

### 4b. Drum one-shots (synthesized)

- 808-style kick: sine with fast pitch drop, plus click transient.
- 808 sub boom: long sine, 50–60 Hz.
- Break-style kick: shorter, mid-punchy.
- Snare: tone burst (180–220 Hz) plus band-passed noise. Two flavors: tight and trashy.
- Rimshot, closed hat, open hat, ride, crash: shaped metallic noise.
- Shaker and tambourine: high-passed noise bursts.

Add a **CRUSH** control on every channel: sample-rate reduce to 22/11 kHz and 8–12 bits. This fakes the Akai S950 / Amiga grit that defines the era.

### 4c. Bass

- **SUB**: pure sine, mono, glide, optional 40 ms pitch drop. The jungle low end.
- **REESE**: two saws detuned ±20–40 cents, 24 dB lowpass at 300–1200 Hz, slow chorus, soft clip. Named for Kevin Saunderson's 1988 track "Just Want Another Chance"; jungle adopted it after Renegade's "Terrorist" sampled it in 1994. Give it glide for the classic sliding line.
- **WOBBLE** (stretch goal): Reese with an LFO on the filter.

### 4d. Synths and FX

- **HOOVER STAB**: detuned saw/pulse stack, downward pitch sweep on attack, PWM movement. The Mentasm rave sound.
- **CHORD STAB**: one trigger plays a minor or minor-7 chord through a pluck envelope. The M1-style rave stab.
- **PAD**: soft detuned saws, slow attack, dark filter. For the deep tunes.
- **DUB SIREN**: square wave, pitch LFO, into the delay. Pure fun, fully legal.
- Vocal chops: do not ship any. User imports go to the FX channel.

### 4e. Sends and master

- Tempo-synced dub delay (3/16 default) with a lowpass in the feedback loop.
- Dark reverb: convolver with a generated noise impulse. No IR files.
- Master: soft-clip waveshaper into a limiter-style compressor.

## 5. The sequencer

- **6 channels**: BRK1, BRK2, SUB, REESE, STAB, FX.
- **Patterns are per-channel.** 32 rows = 2 bars of 16ths. Ticks per row: 6 (ProTracker heritage; gives retrigger resolution).
- **Song screen** = grid. Columns are channels. Rows are time slots. Each cell holds a pattern ID in hex. Patterns repeat anywhere. This is the LSDJ/LGPT model and it is the right one for a phone.
- Note column: `C-2`–`B-5` for synths; `S01`–`S32` slice numbers for break channels.
- Swing control per song (0–75%).

### Effect commands (one per row, two hex digits)

| Cmd | Name | Why it matters |
|---|---|---|
| `9xx` | Sample offset | THE jungle chop command since ProTracker |
| `Rxx` | Retrigger every xx ticks | Snare rushes, edits |
| `Bxx` | Reverse | Backwards slices |
| `Pxx` | Pitch offset, signed semitones | Pitched chops |
| `Gxx` | Glide time | Sliding Reese and sub lines |
| `Cxx` | Filter cutoff | Per-row filter moves |
| `Txx` | Timestretch grain | Fake Akai "cyclic" stretch artifacts |
| `Vxx` | Volume | Ghost notes |

## 6. UI: screens

Portrait-first. One task per screen. Swipe or tab between screens. Transport bar always visible: play, stop, rec, BPM, pattern ID, save dot.

1. **SONG** — the pattern-ID grid. Tap a cell to assign. Double-tap to clone. Channel mute/solo on the header.
2. **PATTERN** — one channel at a time, 32 big rows. Swipe left/right to change channel. Tap a row to place the last-used note. Long-press opens the edit drawer: note picker or slice pads, instrument, effect, value. Two thumbs, no typing.
3. **PADS** — 16 pads = the current break's slices. Finger-drum. REC quantizes hits into the pattern. This is the Koala move inside a tracker.
4. **CHOP** — the ReCycle move. Waveform with slice markers. Slice modes: equal 8/16/32, or TRANS (onset detection on the amplitude envelope). Markers drag, and snap to the nearest detected transient. Per-slice pitch/reverse/gain, CRUSH knob, audition on tap. **SPREAD** writes all slices in order into the current pattern at 16th intervals — the break now plays at song tempo with no pitch change, exactly like a REX loop. Then rearrange the notes.
5. **INST** — parameters for the selected instrument type.
6. **MIX** — 6 faders, per-channel filter and crush, delay and reverb sends, master level.

Landscape iPad bonus (later): classic all-channels tracker view, BassoonTracker style.

### Break import pipeline

IMPORT accepts many files at once (iOS gives no standing folder access, so import once and the LIBRARY keeps them). Each break runs five steps:

1. Trim silence from both ends.
2. Snap the start to the first transient — the downbeat.
3. Guess the length: 1, 2, or 4 bars. Compute the break's own BPM from the guess. Show both. One tap corrects a wrong guess.
4. Slice: 16 equal by default; TRANS for loose grooves.
5. Save to the LIBRARY with the slice map.

After SPREAD, slices sit on grid steps and the grid runs at song tempo. The break is on beat by construction. No timestretching. If the tempo gap is wide, slices leave gaps or overlap. The period-correct fixes: pitch the sample up, or lean on `Txx` grain stretch.

### 6a. Look: old-school computer UI

The whole app looks like software from 1987–1992. Not "retro-inspired". Period-correct.
**Skin decision: A. WORKBENCH.** Build only A. Keep colors and metrics in one token block so B and C can come later. Mockups in `dubplate-mockups.html`.

| Skin | Reference | Palette | Notes |
|---|---|---|---|
| **A. WORKBENCH** (chosen) | Amiga Workbench 1.3 | Blue `#0055AA`, white, black, orange `#FF8800` | Beveled gadgets. Jungle's home machine. This is the build |
| B. SYSTEM 7 | Classic Mac, 1-bit | Black on white, dither patterns | Pinstripe title bar, inverted playhead. Cleanest |
| C. TEXT MODE | DOS / Norton-era PC | `#0000AA` blue, gray `#AAAAAA`, yellow `#FFFF55` | Box-drawing borders. Cheapest to build |

Skin rules:

- One pixel font, no anti-aliasing. Integer scaling only.
- No rounded corners over 2 px. No shadows. No gradients. No transparency.
- Every control looks like the period drew it: bevels (A), 1-px outlines (B), or character cells (C).
- The playhead row inverts. That is the only animation the grid needs.

### 6b. Copy rules

No claudespeak. The interface reads like a tool, not a tour guide.

- If position or a symbol makes a control clear, it gets **no label**.
- Labels are one word, all caps: `SONG PTN PAD CHOP INST MIX BPM REC`.
- Symbols beat words: `▶ ■ ● + − ◂ ▸`.
- Numbers stay hex where trackers use hex.
- No helper text. No onboarding. No tooltips. No empty-state prose. No exclamation points.
- Messages are three words or fewer: `SAVED` · `NO ROOM` · `RENDERING…` · `DELETE? Y/N`.
- Never: "Let's get started", "Welcome to", "Oops", "Successfully", or any sentence that sells.

### Touch rules

- Minimum hit target 44 px.
- `touch-action: none` on the grid. Kill double-tap zoom.
- First touch anywhere resumes the AudioContext (iOS requires a gesture).
- Every edit auditions instantly at low latency.

## 7. Audio engine

- Lookahead scheduler: `setInterval` 25 ms, schedule 120 ms ahead against `audioContext.currentTime`. UI playhead reads the schedule via `requestAnimationFrame`.
- Voices: one `AudioBufferSourceNode` per sample trigger; oscillator graphs per synth voice; mono voice-steal for SUB and REESE.
- Graph per channel: voice → gain → biquad lowpass → crush (waveshaper or scripted decimate) → dry out + two send gains.
- Render to file: mirror the graph in an `OfflineAudioContext`, encode 16-bit WAV, download as a Blob.

## 8. Data model

```json
{
  "name": "untitled", "bpm": 170, "swing": 0,
  "instruments": [{ "type": "reese", "params": {} }],
  "samples": [{ "name": "mybreak", "wav": "<base64>", "slices": [0, 4410] }],
  "patterns": [{ "channel": 0, "rows": [{ "note": "S01", "inst": 1, "fx": "9", "val": "20" }] }],
  "song": [["00", "01", "02", "03", "--", "04"]]
}
```

- Autosave to IndexedDB every 30 s and on blur. Two stores: PROJECTS, and LIBRARY (breaks plus slice maps, shared across projects). Projects reference library breaks by id.
- Export/import the whole project as one `.json` (referenced breaks embedded as base64 copies, so the file stands alone).
- Export audio as `.wav`.

## 9. Legal plan for samples

- The famous breaks are copyrighted recordings. The Winstons' drummer never saw royalties. Do not embed them.
- Ship: synthesized kit + groove presets (clean). Support: user imports (their responsibility).
- Point users at royalty-free sources for practice material: Sample Focus has free Amen-style breaks; free-sample-packs.com and Circles Drum Samples offer played-in, royalty-free break packs. Note: those licenses allow use in music, not redistribution inside an app. So even those stay out of the shipped file.
- **Starter bank, for your own copy**: a `breaks/` folder and a tiny bake script that base64-embeds any WAVs there into `index.html`, pre-chopped and named. The public build ships the mechanism empty. You fill your local one.

## 10. Milestones (for Claude Code)

Each one runs and makes sound.

1. **Boot** — audio unlock, transport, master chain, metronome.
2. **Noise** — synth drum kit + hardcoded AMEN preset pattern playing at 170. Jungle in the room on day one.
3. **Edit** — PATTERN screen, canvas grid, place/erase notes, SONG screen.
4. **Low end** — SUB and REESE instruments, glide, INST screen.
5. **Chop** — multi-file import, auto-trim, bar and BPM guess, LIBRARY, CHOP screen with equal and TRANS slicing, SPREAD, slices in the note column, 9xx.
6. **Commands** — R/B/P/C/T/V effects, sends, MIX screen.
7. **Keep it** — IndexedDB autosave, JSON export/import.
8. **Ship it** — WAV render, PADS screen, skin polish, iPad landscape pass.

## 11. Stretch goals

- Resample a channel to a new sample (Koala-style).
- EXPORT KIT: a `.zip` with one WAV per slice plus a JSON slice map. The open replacement for REX export. Drops into Koala or any sampler.
- WebMIDI input. `.mod` export. Sensitivity slider for transient slicing (full ReCycle style).
- Per-channel swing. Share patterns by URL hash (no samples).

## 12. Reference links

- BassoonTracker: https://www.stef.be/bassoontracker/ · https://github.com/steffest/bassoontracker
- LittleGPTracker: https://github.com/djdiskmachine/LittleGPTracker
- Koala Sampler: https://www.koalasampler.com/
- Break history: https://allcrew.uk/gimme-a-break/ · https://www.whosampled.com/news/2015/03/05/top-10-iconic-drum-bass-jungle-breakbeats/
- Reese deep dive: https://www.attackmagazine.com/technique/tutorials/reese-bass-redux/
- Free breaks: https://samplefocus.com/categories/breakbeat · https://free-sample-packs.com/breakbeat/ · https://www.circlesdrumsamples.com/breakbeatsvol1
