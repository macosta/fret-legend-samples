# Overdriven electric guitar samples

Drop overdriven / lightly distorted electric guitar MP3s here, one per fretted pitch.

## File naming

`eN-FF.mp3` where:
- `N` = string number (1=high E, 2=B, 3=G, 4=D, 5=A, 6=low E)
- `FF` = fret number, zero-padded (`00` = open string, `01` = first fret, etc.)

Example: `e6-00.mp3` is the open low-E string. `e1-12.mp3` is the high-E string at the 12th fret.

## Pitch mapping

Same as `public/samples/acoustic/README.md` — see that file for the full table.

## Minimum required set

49 files (same as acoustic):

- `e1-00.mp3` … `e1-24.mp3` (25 files)
- `e2-00.mp3` … `e2-04.mp3` (5 files)
- `e3-00.mp3` … `e3-03.mp3` (4 files)
- `e4-00.mp3` … `e4-04.mp3` (5 files)
- `e5-00.mp3` … `e5-04.mp3` (5 files)
- `e6-00.mp3` … `e6-04.mp3` (5 files)

## Audio specs

- Format: MP3, CBR, 192 kbps, 44.1 kHz, mono or consistent stereo
- Each file: 3–5 seconds, single isolated note, natural decay
- Consistent volume across the set (apply loudness normalization if needed)
- No external reverb / delay — the only "effect" should be the amp/cabinet character baked into the recording
- No other instruments

## Recommended sources (in order of preference)

1. **Karoryfer Lascivious free sample packs** — https://www.karoryfer.com/karoryfer-samples
   Look for distorted / overdriven electric guitar. CC-BY licensed (credit required).

2. **Freesound.org** — https://freesound.org/
   Search: `"overdriven electric guitar" single note CC` — filter by Creative Commons license.

3. **Pianobook community packs** — https://www.pianobook.co.uk/
   Some uploaded SFZ / WAV electric guitar packs.

Convert WAV → MP3 with:

```
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k -ar 44100 -ac 1 output.mp3
```

## Tone target

"Edge of breakup" tube amp — light overdrive, not metal-distortion. Should sound musical and cleaned-up enough that chords stay legible, while single notes have warmth and harmonic richness. Avoid scooped-mid metal tones, chuggy palm-mute dry, or heavy gain.

## Status

**Currently empty.** The Overdrive preset is configured to fall back to the clean electric samples in `public/samples/electric/`, so the button works but plays the same tone as Clean. To make Overdrive sound distinct, either:

1. Drop a dedicated overdriven-electric sample pack here following the same `eN-FF.mp3` convention, OR
2. Drop a guitar-cabinet impulse response WAV here (e.g. `cab.wav`) and the audio chain will be wired to apply waveshaper distortion + convolution against this IR — see `src/hooks/useGuitarTone.ts`.

## Attribution

(Add source / license attribution here once samples are placed.)
