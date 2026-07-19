# How disc golf works — explainer video

A 66-second narrated explainer of how disc golf works: tee → lie → basket,
the three disc types, and how scoring counts every throw. The entire video
is source code: every scene, word, color, and timing is a small edit
followed by a ~45-second re-render.

**Watch:** [`YouTube Video`](https://youtu.be/Qi3Vx8kRgMc) [`production/renders/disc-golf-explainer-v1.mp4`](production/renders/disc-golf-explainer-v1.mp4)

This repo is both a demo of the
[explainer-video-skill](https://github.com/mhuot/explainer-video-skill)
and a **teaching repo for editing a video after initial creation** — see
the [exercises](#teaching-exercises-edit-this-video) below.

## How it was made

Produced with the
[mhuot/explainer-video-skill](https://github.com/mhuot/explainer-video-skill)
workflow (Kokoro TTS + HyperFrames + FFmpeg, fully local after setup), using
the skill's Claude Design component library (title/hook card, step chips,
flow-diagram grammar, recap card, light token set). That repo documents the
method, toolchain installation, composition rules, and production gates;
this repo is one video produced by it.

## Repo layout

```
production/
  research/research-brief.md      # every scripted claim, source-mapped (PDGA etc.)
  proposal.md                     # narrative arc, scene list, theme
  script/script.md                # locked narration
  scene_plan/scene-plan.md        # derived timing table + per-scene visual notes
  checkpoints/decision-log.json   # append-only production decisions
  checkpoints/self-review.md      # post-render QA evidence
  checkpoints/frames/             # reviewed encoded stills
  assets/audio/                   # Kokoro WAVs + measured durations.json
  renders/disc-golf-explainer-v1.mp4  # the deliverable
tools/tts_generate.py             # narration synthesis (edit SCENE_NARRATIONS)
video/index.html                  # THE VIDEO — 7 scenes, one GSAP timeline
video/assets/                     # vendored gsap + scene audio
```

## Updating the video

Prerequisites (Node ≥ 22, bun, FFmpeg with libx264, a HyperFrames build,
Python 3.12 + Kokoro) are covered by the skill repo's
[environment bootstrap](https://github.com/mhuot/explainer-video-skill).
Below, `CLI` means `node "$HYPERFRAMES_DIR/packages/cli/dist/cli.js"`.

**The one rule that governs everything:** the script locks first, and every
timing number downstream is *derived from measured narration audio* — never
guessed. If you change any words, you must re-measure and re-derive.

### Changing the script (narration)

1. Edit `SCENE_NARRATIONS` in `tools/tts_generate.py`. Write numbers and
   acronyms as the TTS should say them ("nine thousand eight hundred");
   on-screen text keeps real spelling. Budget ≈2.55 words/second.
2. Synthesize and measure:

   ```bash
   uv venv --python 3.12 .venv
   uv pip install --python .venv/bin/python "kokoro>=0.9.4,<1" numpy soundfile
   PYTORCH_ENABLE_MPS_FALLBACK=1 .venv/bin/python tools/tts_generate.py
   ```

   This writes one WAV per scene plus
   `production/assets/audio/durations.json` with measured durations.
3. Re-derive the timing table (current one in
   `production/scene_plan/scene-plan.md`):

   ```
   n_start[0]     = 0.5                       # first narration starts at 0.5 s
   n_start[i+1]   = n_start[i] + dur[i] + 0.5 # breathing gap
   scene_start[i] = n_start[i] - 0.3          # visuals lead narration slightly
   TOTAL          = last n_end + ~0.9         # fade-out room
   ```

4. Apply the derived numbers to **all three timing surfaces** in
   `video/index.html` — they must agree exactly:
   - each `<section>`'s `data-start` / `data-duration`
   - each `<audio>`'s `data-start` / `data-duration`
   - the JS scene constants (`S1`…`S7`) and the root `data-duration`

   Also nudge any GSAP beats inside the changed scene so elements land on
   the new narration phrasing.
5. Copy audio into the composition:

   ```bash
   cp production/assets/audio/*.wav video/assets/audio/
   ```

   (This video has no music bed — a logged decision; the skill docs have
   the deterministic recipe if you want to add one.)

### Changing visuals only

Edit `video/index.html` directly — no audio or timing work needed. Theme
lives in the `:root` CSS variables (one accent color); scene layouts are
plain absolutely-positioned HTML/SVG. Respect the composition rules from
the skill docs, chiefly: entrances are GSAP `fromTo` (never CSS transform
initial states), media elements keep explicit unique `id`s, and animate
only transforms/opacity (+ `strokeDashoffset` for SVG draws).

### Validate, render, QA (every change)

```bash
cd video
$CLI lint                      # structural rules
$CLI check                     # runtime, layout, WCAG AA contrast
$CLI snapshot --at <seconds>   # then actually LOOK at the changed scenes
$CLI render --quality high --output ../production/renders/disc-golf-explainer.mp4

ffprobe -show_entries format=duration ../production/renders/disc-golf-explainer.mp4
ffmpeg -i ../production/renders/disc-golf-explainer.mp4 -af volumedetect -f null -
```

Pass criteria: 0 lint/check errors, duration within ±0.1 s of the derived
`TOTAL`, `max_volume` below 0 dB, and extracted frames matching the scene
plan. Record what you verified in `production/checkpoints/self-review.md`,
and log any decision changes in `production/checkpoints/decision-log.json`
(append-only).

## Teaching exercises: edit this video

Graded from a one-line change to a full timing re-derivation. Each ends
with the same validate → render → QA loop above.

1. **Re-skin (5 lines, no timing).** Swap the `:root` tokens in
   `video/index.html` for the dark set from the skill's design system —
   ground `#141c24`, panel `#1d2833`, ink `#e8eef4`, ink-dim `#9db0c0`,
   accent `#1e8fe0`, hairline `#2e3d4d` — and re-render. `check` will
   re-verify every contrast pair on the new surface.
2. **Move a visual beat (one number, no audio).** In scene 5, the putter
   card lands at `S5 + 8.7`, timed to the word "putters." Say the video
   should tease it earlier: change it and watch the result feel wrong —
   then put it back where the narration says it belongs. The point:
   beats belong to the measured audio, not to taste.
3. **Change one scene's words (scoped re-derive).** Edit `s7_recap` in
   `tools/tts_generate.py` (it is the last scene, so only its own numbers
   and `TOTAL` change). Re-run TTS, read the new duration from
   `durations.json`, update scene 7's `data-duration`, `aud-s7`'s
   `data-duration`, and the root `data-duration` (= new `n_end + 0.9`).
4. **Change an early scene's words (full re-derive).** Edit `s2_context`
   — now every downstream `n_start`, scene start, JS constant, and GSAP
   beat shifts. Walk the derivation formula through all seven scenes.
   This is the exercise that teaches why the skill measures instead of
   guessing.

## Sources

Script claims are source-mapped in
[`production/research/research-brief.md`](production/research/research-brief.md)
(PDGA rules and introduction; disc-type guides). The narration is
synthetic (Kokoro); assess platform disclosure per the skill docs before
publishing.

## License

MIT — see [LICENSE](LICENSE). Method credit: Idan Shimon.
