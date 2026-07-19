# Self-review — disc-golf-explainer-v1.mp4 (2026-07-19)

## Timing integrity

All timing derived from measured `durations.json` (total narration 61.73 s).
The three timing surfaces (scene `data-start/duration`, `<audio data-start>`,
JS scene constants) were authored from the same derivation: scenes at 0 /
8.175 / 19.70 / 27.95 / 36.80 / 49.175 / 58.20, narration starts at 0.5 /
8.475 / 20.00 / 28.25 / 37.10 / 49.475 / 58.50, total 66.1 s.

## Validation ladder

- `lint`: 0 errors, 1 style warning (`timeline_track_too_dense`, accepted —
  single-file composition by design, precedent in the skill's own demo).
- `check`: passed; 36/36 text checks WCAG AA; 0 motion errors.
- Snapshots at all 7 scene midpoints reviewed against the QA checklist:
  contrast ✓, no overlap/clipping ✓, composition ✓ (staggered card/tile
  states at midpoints are correct — entrances land on narration beats).

## Render measurements

- Master: H.264 1920×1080 30 fps + AAC 48 kHz stereo, 3.6 MB.
- Duration: 66.133 s (plan 66.1 s — within ±0.1 s). ✓
- volumedetect: mean −29.1 dB, max −7.2 dB (below 0 dB). ✓
- Encoded QA frames at 4 / 24 / 43 / 62 s reviewed — match preview
  snapshots; no black frames, no missing assets, narration-beat states
  correct.

## Sources honored

Script claims map to production/research/research-brief.md (PDGA rules and
introduction; disc-type guides). "Free to play" claim deliberately omitted
as unsourced.

## Music

None (decision logged) — narration only.
