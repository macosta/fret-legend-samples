# Acoustic guitar samples

Drop steel-string acoustic guitar MP3s here, one per fretted pitch.

## File naming

`eN-FF.mp3` where:
- `N` = string number (1=high E, 2=B, 3=G, 4=D, 5=A, 6=low E)
- `FF` = fret number, zero-padded (`00` = open string, `01` = first fret, etc.)

Example: `e6-00.mp3` is the open low-E string. `e1-12.mp3` is the high-E string at the 12th fret.

## Pitch mapping (which pitch each filename should contain)

| String 1 (high E) | String 2 (B) | String 3 (G) | String 4 (D) | String 5 (A) | String 6 (low E) |
|---|---|---|---|---|---|
| `e1-00` = E4 | `e2-00` = B3 | `e3-00` = G3 | `e4-00` = D3 | `e5-00` = A2 | `e6-00` = E2 |
| `e1-01` = F4 | `e2-01` = C4 | `e3-01` = G#3 | `e4-01` = D#3 | `e5-01` = A#2 | `e6-01` = F2 |
| `e1-02` = F#4 | `e2-02` = C#4 | `e3-02` = A3 | `e4-02` = E3 | `e5-02` = B2 | `e6-02` = F#2 |
| ... up to `e1-24` = E6 | `e2-04` = D#4 | `e3-03` = A#3 | `e4-04` = F#3 | `e5-04` = C#3 | `e6-04` = G#2 |

## Minimum required set

49 files cover the whole fretboard (Tone.js pitch-shifts between samples):

- `e1-00.mp3` … `e1-24.mp3` (25 files for the high-E string — covers the upper register)
- `e2-00.mp3` … `e2-04.mp3` (5 files)
- `e3-00.mp3` … `e3-03.mp3` (4 files)
- `e4-00.mp3` … `e4-04.mp3` (5 files)
- `e5-00.mp3` … `e5-04.mp3` (5 files)
- `e6-00.mp3` … `e6-04.mp3` (5 files)

## Audio specs

- Format: MP3, CBR, 192 kbps, 44.1 kHz, mono or consistent stereo
- Each file: 3–5 seconds, single isolated note, natural decay
- Consistent volume across the set (apply loudness normalization if needed)
- No reverb, no delay, no other instruments

## Attribution

Samples derived from **MDM Acoustic Guitar v1.0 F** by Mića de Mijatović, downloaded from Pianobook (https://www.pianobook.co.uk/profile/demijatovic/). Pianobook community packs are typically licensed under Creative Commons; users of this app credit Mića de Mijatović as the recording artist.

Source files are FLAC (lossless), `MDMAG Sustain Pick` articulation, velocity layer 076. Each MIDI pitch from MIDI 40 (E2, low E open) through MIDI 84 (C6) is converted to MP3 (192 kbps, 44.1 kHz, mono) and renamed per the `eN-FF.mp3` convention. Pitches above MIDI 84 (top 4 frets of the high-E string) are pitch-shifted by Tone.Sampler from the C6 sample.
