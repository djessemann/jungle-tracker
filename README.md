# DUBPLATE

A jungle / drum & bass box that runs in a phone browser.

**→ https://djessemann.github.io/jungle-tracker/**

Press play and it is already making a tune. Then chop your own break into it.
One `index.html`, vanilla JS, no build step, no dependencies.

![DUBPLATE](https://img.shields.io/badge/one-file-FF8800) ![](https://img.shields.io/badge/no-dependencies-0055AA)

## How it works

Three tabs.

**BEAT** — four lanes of sixteen steps: BREAK, BASS, STAB, FX. Pick a sound
from the pads at the bottom, then tap the steps you want it on. Tap a step
again to clear it, hold it to clear it whatever is in it. Tap a lane name to
work on that lane, hold it to mute. VOL, TONE and FX are that lane's mix.

**REV** and **ROLL** are brushes: arm one and the steps you paint come out
backwards, or as a three-hit roll. That is the jungle in two buttons.

**BREAK** — eight built-in breaks, plus everything you import. LOAD takes as
many files as you can select. Slice at 8, 16, 32 or AUTO (transient detection),
drag any marker, then FILL BEAT to lay the break across the grid.

**SAVE** — save, load, rename, render to WAV, send the whole thing as a `.json`.

**?** — the manual, in plain words, on a page inside the app.

**A B C D** in the top bar are four scenes. Tap one while stopped and you jump
there; tap while playing and it lands on the next bar. CHN chains whatever
scenes have something in them.

## Your own breaks

LOAD takes any audio your phone can read. Each file gets trimmed, snapped to
its first transient, tempo-analysed, told how many bars it is and sliced 16 to
the bar. FILL BEAT then lays the slices onto the grid at the positions they
occupy in the break, so it plays back in time at your tempo with no
timestretch — a two bar break fills scenes A and B and chains. Then move the
steps around, and it is your break now, not the drummer's.

## Sound

Everything is synthesized — nothing sampled ships here.

- **Breaks** — AMEN, THINK, FUNKY, APACHE, HOTPANTS, COLDSWEAT, SESAME,
  ASSEMBLY. These are groove data: a 16-slice map over a synth drum kit plus
  the chops that make each one sound like itself. Rhythms, not recordings.
- **Bass** — sine sub with a pitch drop and glide. Two steps next to each other
  slide into one another.
- **Stab** — chord stabs, locked to the key.
- **FX** — siren, hoover, crash, rise, drop, clap, rim, and your break played
  backwards.
- Tempo-synced dub delay with a lowpass in the feedback loop, dark convolver
  reverb, bit crush on the break, soft clip and compressor on the master.

## Saving

Autosaves to IndexedDB every 30 seconds and when the tab goes away. SEND writes
a `.json` with your break embedded, so the file stands alone. WAV renders the
chain offline and downloads it.

## Samples and the law

The famous breaks are copyrighted recordings and the drummers who played them
were never paid. None of them are in here. What ships is a synth kit and the
grooves. Import whatever you have the right to use.

`bake.py` embeds WAVs from `breaks/` into your **local** copy of `index.html`
as a starter bank. The folder is gitignored and the published build ships empty.

## Files

`index.html` — the whole app · `HOWTO.md` — the manual, same words as the **?**
page in the app · `CLAUDE.md` — how it is built · `bake.py` — the starter-bank
baker · `dubplateplan.md` — the original tracker spec this grew out of, before
it was stripped back for the phone.
