"""Encode a folder of finished WAV notes into a pack in the house format (mono 44.1 kHz 192 kbps MP3), with no
further processing, then decode each MP3 back and write manifest.csv from the decoded artifact.

Used for electric-gretsch-od/: the WAVs are already rendered and levelled (NAM amp capture + cab IR, see CREDITS.md),
so this only encodes and measures. MIDI numbers come from the clean pack's manifest, which uses the same file names.

    python tools/encode_wav_pack.py <wav_dir> <out_dir> <reference_manifest.csv>
"""
import csv, subprocess, sys
from pathlib import Path
import numpy as np

SR = 44100
WAV, OUT, REF = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
midi_of = {r["file"]: int(r["midi"]) for r in csv.DictReader(open(REF, newline=""))}

def ff(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def onset(x):
    return int(np.argmax(np.abs(x) > np.abs(x).max() * 0.05))

def rms_db(x):
    s = x[onset(x):][: int(1.5 * SR)]
    return 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-12)

def pitch_cents(x, midi):
    """Deviation from equal temperament, measured on the steady part (0.3-1.0 s after onset)."""
    f0 = 440 * 2 ** ((midi - 69) / 12)
    a = onset(x); seg = x[a + int(0.3 * SR): a + int(1.0 * SR)].astype(np.float64)
    seg -= seg.mean()
    ac = np.correlate(seg, seg, "full")[len(seg) - 1:]
    lo, hi = int(SR / (f0 * 2 ** (1.5 / 12))), int(SR / (f0 * 2 ** (-1.5 / 12))) + 1
    k = lo + int(np.argmax(ac[lo:hi]))
    y0, y1, y2 = ac[k - 1], ac[k], ac[k + 1]
    lag = k + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    return 1200 * np.log2((SR / lag) / f0)

wavs = sorted(WAV.glob("*.wav"))
assert len(wavs) == len(midi_of), f"{len(wavs)} WAVs vs {len(midi_of)} reference notes"
rows = []
for w in wavs:
    name = w.stem + ".mp3"
    midi = midi_of[name]
    out = OUT / name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(w), "-ac", "1", "-ar", str(SR),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(out)], check=True)
    v = ff(out)  # verify the artifact itself, not the WAV we meant to encode
    rows.append(dict(file=name, midi=midi, source=w.name, out_cents=round(pitch_cents(v, midi), 1),
                     rms_db=round(rms_db(v), 1), peak_db=round(20 * np.log10(np.abs(v).max()), 2),
                     length_s=round(len(v) / SR, 2), onset_ms=round(onset(v) / SR * 1000, 1)))

with open(OUT / "manifest.csv", "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)

oc = np.array([r["out_cents"] for r in rows]); rm = np.array([r["rms_db"] for r in rows])
pk = np.array([r["peak_db"] for r in rows]); ln = np.array([r["length_s"] for r in rows])
print(f"{len(rows)} files | pitch error max {np.abs(oc).max():.1f} cents | RMS {rm.min():.1f}..{rm.max():.1f} dB"
      f" | peak max {pk.max():.2f} dB | length {ln.min():.2f}..{ln.max():.2f} s")
