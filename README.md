# DUBPLATE

A jungle / drum & bass tracker that runs in a phone browser.

**→ https://djessemann.github.io/jungle-tracker/**

Chop a break, roll a sub, drop a Reese, stab a chord, arrange, export. One
`index.html`, vanilla JS, no build step, no dependencies, works offline once
loaded. Add it to your home screen and it runs full screen.

![DUBPLATE](https://img.shields.io/badge/one-file-FF8800) ![](https://img.shields.io/badge/no-dependencies-0055AA)

## Screens

`SONG` grid of pattern IDs, one column per channel · `PTN` one channel of 32
rows, or every channel at once in landscape · `PAD` 16 slice pads, finger-drum
with quantised record · `CHOP` waveform, slice markers, transient detection,
SPREAD · `INST` synth parameters · `MIX` faders, filter, crush, sends ·
disk icon for save / load / export.

Six channels: **BRK1 BRK2 SUB REESE STAB FX**. 32 rows per pattern, 2 bars of
16ths, 6 ticks per row. Default 170 BPM.

## Sound

Everything is synthesized in code — nothing sampled ships here.

- **Breaks** — AMEN, THINK, FUNKY, APACHE, HOTPANTS, COLDSWEAT, SESAME,
  ASSEMBLY. These are groove data: a 16-slice map over the synth drum kit plus
  the bar-and-a-half of chops that make each one sound like itself. They are
  rhythms, not recordings.
- **Bass** — SUB (sine, pitch drop, glide), REESE (detuned saws, 24 dB lowpass,
  slow chorus, soft clip), WOBBLE.
- **Synths** — HOOVER stab, CHORD stab, PAD, DUB SIREN.
- **Kit** — 808 kick and boom, break kick, two snares, ghost, rim, clap, hats,
  ride, crash, shaker, tambourine, toms, bongo, conga, sticks.
- **CRUSH** on every channel for the S950 / Amiga grit, tempo-synced dub delay
  with a lowpass in the feedback loop, dark convolver reverb, soft-clip and
  compressor on the master.

## Your own breaks

`IMP` on the CHOP screen takes as many files as you can select. Each one gets
trimmed, snapped to its first transient, tempo-analysed, told how many bars it
is, sliced 16 to the bar and filed in the LIBRARY, which is shared by every
project. `TRANS` re-slices on detected transients; drag a marker and it snaps to
the nearest one. `SPREAD` writes the slices onto the grid at the positions they
occupy in the break, so it plays back in time at the song tempo with no
timestretch — then you rearrange the notes. That is the whole point.

## Effects

One per row, two hex digits.

| | | | |
|---|---|---|---|
| `9xx` sample offset | `Rxx` retrigger every xx ticks | `Bxx` reverse | `Pxx` pitch, signed semitones |
| `Gxx` glide time | `Cxx` filter cutoff | `Txx` grain stretch | `Vxx` volume (`80` = 100%) |

## Saving

Autosaves to IndexedDB every 30 seconds and when the tab goes away. `EXP` writes
a `.json` with any imported breaks embedded, so the file stands alone; `IMP`
reads it back. `WAV` renders the song offline and downloads it. `KIT` exports the
current break as a WAV plus a JSON slice map.

## Samples and the law

The famous breaks are copyrighted recordings and the drummers who played them
were never paid. None of them are in here. What ships is a synth kit and the
grooves. Import whatever you have the right to use — royalty-free break packs
are easy to find, and those licences cover making music, not redistribution, so
they stay out of this file too.

`bake.py` embeds WAVs from `breaks/` into your **local** copy of `index.html` as
a starter bank. The folder is gitignored and the published build ships empty.

## Files

`index.html` — the whole app · `CLAUDE.md` — how it is built · `bake.py` — the
starter-bank baker · `dubplateplan.md` — the spec it was built to.
