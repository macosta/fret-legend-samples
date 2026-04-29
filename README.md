# Fret Legend — guitar sample packs

CDN-served sample packs for [Fret Legend](https://github.com/macosta/fret-legend-v1).

The application repo loads these via jsDelivr:

```
https://cdn.jsdelivr.net/gh/macosta/fret-legend-samples@main/<preset>/<file>
```

## Layout

| Directory | Preset | Source |
|---|---|---|
| `electric/` | Clean | MDM Strat v1.0 F (Pick Position 0, vel 077) |
| `acoustic/` | Acoustic | MDM Acoustic Guitar v1.0 F (Sustain Pick, vel 076) |
| `overdrive/` | Overdrive | _empty placeholder_ — code falls back to `electric/` |

## Filename convention

`eN-FF.mp3` — `N` = string number 1–6 (1=high E, 6=low E), `FF` = fret 00–24.

Each pack covers from the open low-E (MIDI 40 = E2) up through whatever pitch the source library tops out at. Tone.js Sampler pitch-shifts up from the highest available sample for any notes beyond that.

| Pack | Top pitch on disk |
|---|---|
| `electric/` | MIDI 86 (D6 — high E string fret 22) |
| `acoustic/` | MIDI 84 (C6 — high E string fret 20) |

## Audio specs

- MP3, CBR 192 kbps, 44.1 kHz, mono
- Each file: 11–18 s, single isolated note, natural decay, no effects
- Source FLACs at single velocity layer per pack (077 for Strat, 076 for acoustic)

## Attribution

Both packs by **Mića de Mijatović** — https://www.pianobook.co.uk/profile/demijatovic/

Pianobook community packs are typically licensed under Creative Commons; users of Fret Legend credit Mića de Mijatović as the recording artist.
