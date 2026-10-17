"""Build the Sustain Six clean-electric pack from Karoryfer Black And Green (green = Gretsch Anniversary), CC0.

One file per pitch, MIDI 40-86, named exactly as the app's buildSamplerUrls expects (eN-FF.mp3), so no code change.
Per note: pick the most typical round-robin of the mf layer, correct tuning, trim pre-roll, shape tone, match the
current pack's level (RMS of the first 1.5 s), encode in the house format (mono 44.1 kHz 192 kbps MP3), then decode
the MP3 back and verify pitch, level, peak and length. Writes manifest.csv beside the pack.

Tone shaping is deliberately light and dry: the app adds compression, EQ (+2.5 dB @150 low shelf, +2.5 dB @280,
-2 dB @800, +1.5 dB @8k shelf) and reverb on top, all tuned for the old Strat. So: high-pass 70 Hz (rumble below
low E), -3 dB @250 Hz (the Gretsch is ~6-12 dB fuller below 300 Hz than the Strat; the app's body boost would make it
boomy), +3 dB @3 kHz (the Gretsch is ~10 dB darker at 2.5-5 kHz; restores pick definition).

Usage: python -I build_pack.py <green_ord_dir> <out_dir> [--raw]   (--raw skips the EQ, for A/B comparison)
"""
import csv, re, subprocess, sys, pathlib
import numpy as np

SR = 44100
SRC, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
RAW = "--raw" in sys.argv
PACK = OUT / "electric"
PACK.mkdir(parents=True, exist_ok=True)

TARGET_RMS_DB = -14.5    # current pack: -12.7 .. -14.8 dB RMS over the first 1.5 s
PEAK_CAP_DB = -0.5       # current pack peaks at -0.3; leave headroom for MP3 overshoot
EQ = "highpass=f=70:poles=2,equalizer=f=250:t=q:w=0.9:g=-3,equalizer=f=3000:t=q:w=0.8:g=3"

# --- the app's file map (mirror of buildSamplerUrls in src/hooks/useGuitarTone.ts) ---
OPEN = [40, 45, 50, 55, 59, 64]; PREFIX = ['e6', 'e5', 'e4', 'e3', 'e2', 'e1']; BASE_MAX = [4, 4, 4, 3, 4, 24]
MAX_MIDI = 86
files = {}
for i in range(6):
    for fret in range(min(BASE_MAX[i], MAX_MIDI - OPEN[i]) + 1):
        files.setdefault(OPEN[i] + fret, f"{PREFIX[i]}-{fret:02d}.mp3")
assert sorted(files) == list(range(40, 87)), "file map must cover MIDI 40-86 once each"

# --- source index: Black And Green names octaves one high (twang_f3 has pitch_keycenter=41) ---
PC = {'c': 0, 'db': 1, 'd': 2, 'eb': 3, 'e': 4, 'f': 5, 'gb': 6, 'g': 7, 'ab': 8, 'a': 9, 'bb': 10, 'b': 11}
src = {}
for p in sorted(SRC.glob("twang_*_mf_rr*.wav")):
    m = re.match(r"twang_([a-g]b?)(\d)_mf_rr\d\.wav$", p.name)
    src.setdefault(12 * int(m.group(2)) + PC[m.group(1)], []).append(p)
missing = [m for m in files if m not in src]
assert not missing, f"no mf sample for MIDI {missing}"

def ff(path, af="anull"):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-af", af, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
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

def centroid(x):
    s = x[onset(x):][: int(1.5 * SR)]
    X = np.abs(np.fft.rfft(s)); f = np.fft.rfftfreq(len(s), 1 / SR)
    return (X * f).sum() / X.sum()

def limit(x, cap):
    """Look-ahead peak limiter: gain is held at the lowest value needed within +/-5 ms, then smoothed over 5 ms,
    so only the pick transient is reduced. Block-wise (1 ms) so it stays fast in plain numpy."""
    need = np.minimum(1.0, cap / np.maximum(np.abs(x), 1e-9))
    blk = 44; n = -(-len(x) // blk)
    b = np.pad(need, (0, n * blk - len(need)), constant_values=1.0).reshape(n, blk).min(1)
    b = np.lib.stride_tricks.sliding_window_view(np.pad(b, 5, constant_values=1.0), 11).min(1)
    g = np.interp(np.arange(len(x)), np.arange(n) * blk + blk / 2, b)
    w = np.hanning(221); g = np.convolve(g, w / w.sum(), "same")
    y = (x * g).astype(np.float32)
    over = np.abs(y).max() / cap
    return y / over if over > 1 else y

rows = []
for midi in sorted(files):
    name = files[midi]
    # most typical round-robin: closest to the median level and brightness of its takes
    takes = [(p, ff(p)) for p in src[midi]]
    feats = np.array([[rms_db(x), centroid(x)] for _, x in takes])
    z = np.abs(feats - np.median(feats, 0)) / (feats.std(0) + 1e-9)
    path, x = takes[int(np.argmin(z.sum(1)))]

    cents = pitch_cents(x, midi)
    tune = f"asetrate={SR * 2 ** (-cents / 1200):.3f},aresample={SR}," if abs(cents) > 3 else ""
    start = max(0.0, onset(x) / SR - 0.003)
    af = f"{tune}atrim=start={start:.5f},asetpts=PTS-STARTPTS,afade=t=in:d=0.002" + ("" if RAW else "," + EQ)
    y = ff(path, af)

    # re-trim after EQ (it moves the onset), keep the natural decay, end on a short fade
    y = y[max(0, onset(y) - int(0.003 * SR)):].copy()
    fade = int(0.1 * SR); y[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
    # level: reach the target RMS, letting a gentle peak limiter shave the pick transient instead of turning the
    # whole note down (31 of 47 notes were peak-capped without it, up to 3.8 dB short of target)
    for _ in range(3):
        y *= 10 ** ((TARGET_RMS_DB - rms_db(y)) / 20)
        y = limit(y, 10 ** (PEAK_CAP_DB / 20))
    limited_db = TARGET_RMS_DB - rms_db(y)  # >0 only if the limiter could not get there

    out = PACK / name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(out)], input=y.tobytes(), check=True)

    # verify the artifact itself, not the buffer we meant to write
    v = ff(out)
    rows.append(dict(file=name, midi=midi, source=path.name, src_cents=round(cents, 1),
                     out_cents=round(pitch_cents(v, midi), 1), rms_db=round(rms_db(v), 1),
                     peak_db=round(20 * np.log10(np.abs(v).max()), 2), length_s=round(len(v) / SR, 2),
                     onset_ms=round(onset(v) / SR * 1000, 1), short_of_target_db=round(limited_db, 1)))
    print(rows[-1])

with open(OUT / "manifest.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

oc = np.array([r["out_cents"] for r in rows]); rm = np.array([r["rms_db"] for r in rows])
pk = np.array([r["peak_db"] for r in rows]); ln = np.array([r["length_s"] for r in rows])
print(f"\n{len(rows)} files | out pitch error max {np.abs(oc).max():.1f} cents | RMS {rm.min():.1f}..{rm.max():.1f} dB"
      f" | peak max {pk.max():.2f} dB | length {ln.min():.2f}..{ln.max():.2f} s")
