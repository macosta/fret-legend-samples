# Credits and licences

## `electric-gretsch/`

- **Source:** Karoryfer Black And Green Guitars, "green" (Gretsch Anniversary), `ord` articulation, mf layer.
  Recorded by Brian Wood / Karoryfer Samples. https://github.com/sfzinstruments/karoryfer.black-and-green-guitars
- **Licence:** CC0-1.0 (public domain dedication). No attribution is required; we give it anyway.
- **Our processing** (`tools/build_pack.py`): one round-robin chosen per pitch, tuning corrected to within a few
  cents, pre-roll trimmed, light EQ (high-pass 70 Hz, -3 dB at 250 Hz, +3 dB at 3 kHz), spectral noise reduction
  against a fixed hiss profile plus a 24 dB/oct low-pass at 7 kHz (the source takes carry steady hiss above 4 kHz),
  transient-only peak limiting, levelled to match the old pack, encoded as mono 44.1 kHz 192 kbps MP3. `manifest.csv` records the source file and
  the measured pitch, level and length of every output file.

## `electric-gretsch-od/`

- **Source:** the 47 notes of `electric-gretsch/` above (CC0).
- **Amp:** rendered through the Neural Amp Modeler capture "Marshall JCM 800 2203 - Crunch" by @sarcobe on TONE3000
  (https://www.tone3000.com/tones/marshall-jcm-800-2203-86089). Its T3K licence lets users publish the resulting outputs
  without royalties or restrictions; the capture file itself is not redistributed and is not in this repo.
- **Cab:** the Marshall 1960 impulse response from MIT JS Rocks (MIT licence), the same IR the app already ships.
- **Our processing:** input -12 dB into the capture, cab IR, onset aligned to the clean note, 0.25 s tail fade, pack
  normalised to -1 dBFS peak; encoded by `tools/encode_wav_pack.py` as mono 44.1 kHz 192 kbps MP3. `manifest.csv`
  records the measured pitch, level and length of every output file.

## `riffs/v1/` and `riffs/v2/`

`v2` holds the two licks cut to 8 beats (two whole bars), from the same sources and chain as `v1`.

- **Source:** Karoryfer Black And Green Guitars, "green" (Gretsch), `ord` and `stac` articulations, f layer (CC0-1.0),
  https://github.com/sfzinstruments/karoryfer.black-and-green-guitars. The riffs and licks are original, written for Sustain Six.
- **Amps:** Neural Amp Modeler captures on TONE3000, "Diezel VH4 ch3" by @petrc blended with "EVH 5150III 100W CH Red"
  by @ripper. Their T3K licence lets users publish the resulting outputs; the capture files are not redistributed and
  are not in this repo.
- **Cab:** the Mesa 4x12 impulse response from MIT JS Rocks (MIT licence), which the app already ships.
- **Our processing:** `scripts/tone/render_library.py` in the app repo (preset `tight_metal`): own-code boost, EQ,
  compressor, delay and Pedalboard reverb; levelled to -16 LUFS; folded to one exact loop per file.

- **Style catalog (2026-11-02):** files named `*_seventies_rock_*`, `*_classic_crunch_*` and `*_clean_spring_*` in
  `riffs/v1/` use other captures, each T3K (outputs publishable, capture files not redistributed, not in this repo):
  seventies_rock = "Marshall Plexi Super Lead 1959 EL34" by @ripper
  (https://www.tone3000.com/tones/marshall-plexi-super-lead-1959-el34-40971) through the Marshall 1960 IR (MIT JS Rocks);
  classic_crunch = "Marshall JCM 800 2203 - Crunch 2" by @sarcobe
  (https://www.tone3000.com/tones/marshall-jcm-800-2203-86089) through the same IR; clean_spring = "Fender 68 Custom
  Deluxe Reverb - Full Rig" by @tannerc (https://www.tone3000.com/tones/fender-68-custom-deluxe-reverb-full-rig-64712),
  which includes its own miked cabinet, so no IR. The app repo's `scripts/tone/sources.json` logs each licence and the
  date it was read.

## `electric/` and `acoustic/`

- **Source:** MDM Strat v1.0 F and MDM Acoustic Guitar v1.0 F by Mića de Mijatović, published on Pianobook.
  https://www.pianobook.co.uk/profile/demijatovic/
- **Licence:** the Pianobook end-user licence (https://www.pianobook.co.uk/terms-conditions), not Creative Commons.
