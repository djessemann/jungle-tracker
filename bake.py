#!/usr/bin/env python3
"""Bake WAVs from breaks/ into index.html as a starter bank.

The public build ships the mechanism empty. Drop your own break WAVs in
breaks/ and run this to make a local copy that boots with them in the
LIBRARY, already trimmed, tempo-guessed and sliced by the app.

    python3 bake.py            bake breaks/*.wav into index.html
    python3 bake.py --clear    empty the bank again

File name carries the hints:   amen_2bars_136.wav  ->  name AMEN, 2 bars, 136 BPM
Bars and BPM are optional; without them the app analyses the file on load.
Baked breaks are not written to IndexedDB, so they cannot be deleted from
inside the app - remove the WAV and bake again.
"""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "index.html")
BREAKS = os.path.join(HERE, "breaks")
START = "/* BAKE:START */"
END = "/* BAKE:END */"


def parse_name(fn):
    stem = os.path.splitext(os.path.basename(fn))[0]
    bars = bpm = None
    m = re.search(r"(\d+)\s*bars?", stem, re.I)
    if m:
        bars = int(m.group(1))
    m = re.search(r"(\d{2,3})\s*(?:bpm)?$", stem, re.I)
    if m and 60 <= int(m.group(1)) <= 220:
        bpm = int(m.group(1))
    name = re.sub(r"[^A-Za-z0-9]", "", re.split(r"[_\-. ]", stem)[0]).upper()[:8]
    return name or "BREAK", bars, bpm


def main():
    if not os.path.exists(HTML):
        sys.exit("no index.html")
    html = open(HTML, encoding="utf-8").read()
    if START not in html or END not in html:
        sys.exit("no bake markers in index.html")

    entries = []
    if "--clear" not in sys.argv:
        if not os.path.isdir(BREAKS):
            sys.exit("no breaks/ folder")
        files = sorted(
            f for f in os.listdir(BREAKS)
            if f.lower().endswith((".wav", ".aif", ".aiff", ".mp3", ".m4a", ".ogg"))
        )
        if not files:
            print("breaks/ is empty, baking nothing")
        for f in files:
            path = os.path.join(BREAKS, f)
            raw = open(path, "rb").read()
            name, bars, bpm = parse_name(f)
            e = {"n": name, "wav": base64.b64encode(raw).decode("ascii")}
            if bars:
                e["bars"] = bars
            if bpm:
                e["bpm"] = bpm
            entries.append(e)
            print("%-12s %6.1f kB  bars=%s bpm=%s" % (name, len(raw) / 1024, bars, bpm))

    block = START + "\nvar BAKED = " + json.dumps(entries, separators=(",", ":")) + ";\n" + END
    html = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, html, flags=re.S)
    open(HTML, "w", encoding="utf-8").write(html)
    total = sum(len(e["wav"]) for e in entries)
    print("baked %d break(s), %.1f kB of base64 into index.html" % (len(entries), total / 1024))


if __name__ == "__main__":
    main()
