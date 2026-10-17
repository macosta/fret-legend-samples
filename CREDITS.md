# Credits and licences

## `electric-gretsch/`

- **Source:** Karoryfer Black And Green Guitars, "green" (Gretsch Anniversary), `ord` articulation, mf layer.
  Recorded by Brian Wood / Karoryfer Samples. https://github.com/sfzinstruments/karoryfer.black-and-green-guitars
- **Licence:** CC0-1.0 (public domain dedication). No attribution is required; we give it anyway.
- **Our processing** (`tools/build_pack.py`): one round-robin chosen per pitch, tuning corrected to within a few
  cents, pre-roll trimmed, light EQ (high-pass 70 Hz, -3 dB at 250 Hz, +3 dB at 3 kHz), transient-only peak limiting,
  levelled to match the old pack, encoded as mono 44.1 kHz 192 kbps MP3. `manifest.csv` records the source file and
  the measured pitch, level and length of every output file.

## `electric/` and `acoustic/`

- **Source:** MDM Strat v1.0 F and MDM Acoustic Guitar v1.0 F by Mića de Mijatović, published on Pianobook.
  https://www.pianobook.co.uk/profile/demijatovic/
- **Licence:** the Pianobook end-user licence (https://www.pianobook.co.uk/terms-conditions), not Creative Commons.
