"""Preview a sample pack the way the app's CLEAN preset plays it.

Plays one file per pitch (exactly the app's eN-FF.mp3 map, no resampling: every pitch 40-86 has a file), then runs a
copy of the clean chain in src/hooks/useGuitarTone.ts: compressor (-24 dB, 5:1, 3 ms / 100 ms, 6 dB knee) ->
low shelf 150 Hz +2.5 -> peak 280 Hz +2.5 Q0.8 -> peak 800 Hz -2 Q1.2 -> high shelf 8 kHz +1.5 ->
reverb (2.0 s decay, 30 ms pre-delay, wet 0.18) -> limiter -1 dB. Sampler release 0.5 s, as in the app.
Phrase: the comparison phrase from demo.py, then a two-octave G major scale up and down at 8th notes, 120 bpm.
Usage: python -I app_preview.py <pack_dir_with_eN-FF.mp3> <out.mp3>
"""
import subprocess, sys, pathlib
import numpy as np

SR = 44100
PACK, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
OPEN = [40, 45, 50, 55, 59, 64]; PREFIX = ['e6', 'e5', 'e4', 'e3', 'e2', 'e1']; BASE_MAX = [4, 4, 4, 3, 4, 24]
files = {}
for i in range(6):
    for fret in range(min(BASE_MAX[i], 86 - OPEN[i]) + 1):
        files.setdefault(OPEN[i] + fret, f"{PREFIX[i]}-{fret:02d}.mp3")

cache = {}
def sample(midi):
    if midi not in cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(PACK / files[midi]), "-ac", "1", "-ar", str(SR),
                              "-f", "f32le", "-"], capture_output=True, check=True).stdout
        cache[midi] = np.frombuffer(raw, dtype=np.float32)
    return cache[midi]

events = []  # (start, midi, velocity, held seconds)
t = 0.2
for m in [40, 45, 55, 64, 76]:
    events.append((t, m, 0.8, 1.1)); t += 1.2
for chord in ([40, 47, 52, 56, 59, 64], [45, 52, 57, 60, 64]):
    t += 0.3
    for k, m in enumerate(chord):
        events.append((t + k * 0.022, m, 0.7 + 0.04 * (k % 3), 2.4))
    t += 2.6
t += 0.4
g_major = [43, 45, 47, 48, 50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 67]
for m in g_major + g_major[-2::-1]:
    events.append((t, m, 0.75, 0.22)); t += 0.25
t += 1.5

dry = np.zeros(int(t * SR), dtype=np.float32)
rel = int(0.5 * SR)
for start, m, vel, held in events:
    x = sample(m); n = min(len(x), int(held * SR) + rel)
    env = np.ones(n, dtype=np.float32)
    k = int(held * SR)
    if k < n:  # Tone.Sampler release: fade over 0.5 s after the note is let go
        env[k:] = np.linspace(1, 0, n - k, dtype=np.float32)
    a = int(start * SR); dry[a:a + n] += x[:n] * env * vel

# reverb IR: noise with an exponential decay to -60 dB over 2.0 s, 30 ms pre-delay (Tone.Reverb's recipe)
rng = np.random.default_rng(7)
L = int(2.0 * SR)
ir = rng.standard_normal(L).astype(np.float32) * np.exp(-6.9 * np.arange(L) / L).astype(np.float32)
ir = np.concatenate([np.zeros(int(0.03 * SR), np.float32), ir]); ir /= np.sqrt((ir ** 2).sum())
tmp = OUT.with_suffix(".ir.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)],
               input=ir.tobytes(), check=True)

chain = ("acompressor=threshold=-24dB:ratio=5:attack=3:release=100:knee=2,"
         "bass=g=2.5:f=150,equalizer=f=280:t=q:w=0.8:g=2.5,equalizer=f=800:t=q:w=1.2:g=-2,treble=g=1.5:f=8000")
fc = (f"[0:a]{chain},asplit[d][w];[w][1:a]afir=dry=10:wet=10[r];"
      f"[d][r]amix=inputs=2:weights='0.82 0.18':normalize=0,alimiter=limit=0.891:level=false[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-i", str(tmp),
                "-filter_complex", fc, "-map", "[o]", "-b:a", "192k", str(OUT)], input=dry.tobytes(), check=True)
tmp.unlink()
print(OUT, f"{t:.1f}s")
