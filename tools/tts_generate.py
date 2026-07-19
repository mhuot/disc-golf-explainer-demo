"""Generate generic per-scene explainer narration WAVs with Kokoro.

After its model files are cached, Kokoro-82M inference runs locally without a
network connection. This template writes one 24 kHz WAV per scene plus a
``durations.json`` manifest from which composition timing can be derived.

Replace every placeholder in ``SCENE_NARRATIONS`` before running. Budget
approximately 2.55 words/second at speed 1.1. Spell out or space acronyms as
needed for pronunciation; on-screen text can retain its normal spelling.
"""

import json
from pathlib import Path

import numpy as np
import soundfile
from kokoro import KPipeline

OUTPUT_DIRECTORY = (
    Path(__file__).resolve().parent.parent / "production" / "assets" / "audio"
)
SAMPLE_RATE_HZ = 24_000
VOICE_NAME = "af_heart"
SPEECH_SPEED = 1.1

# Explainer arc: hook → context → steps 1..3 → what it means → recap.
SCENE_NARRATIONS: list[tuple[str, str]] = [
    (
        "s1_hook",
        "No clubs. No ball. Just a disc, a chain basket, and open air. "
        "How does a flying disc become a full round of golf?",
    ),
    (
        "s2_context",
        "Disc golf is played like traditional golf, but every shot is a "
        "throw. More than nine thousand eight hundred courses exist "
        "worldwide, winding through parks, woods, and hillsides.",
    ),
    (
        "s3_step1",
        "Every hole starts at a tee. The target is an elevated metal "
        "basket, with hanging chains that catch the disc and drop it in.",
    ),
    (
        "s4_step2",
        "Wherever your disc lands becomes your lie. The next throw starts "
        "exactly there. The hole is finished when your disc comes to rest "
        "in the basket.",
    ),
    (
        "s5_step3",
        "Different discs do different jobs. Drivers have sharp rims that "
        "cut through the air for distance. Mid ranges fly straight and "
        "predictable. Putters are blunt and stable, built to drop in and "
        "stay.",
    ),
    (
        "s6_meaning",
        "Scoring stays simple: count every throw. Most holes are par "
        "three, and the fewest total throws across nine or eighteen holes "
        "wins.",
    ),
    (
        "s7_recap",
        "That's disc golf. Tee, lie, basket. Count the throws. Most "
        "players start with just a putter and a mid range.",
    ),
]


def synthesize_scene(pipeline: KPipeline, scene_id: str, narration_text: str) -> float:
    """Synthesize one scene's narration; return its duration in seconds."""
    narration_text = narration_text.strip()
    if not narration_text:
        raise ValueError(f"narration is empty for {scene_id}")
    if narration_text.startswith("<") and narration_text.endswith(">"):
        raise ValueError(f"replace the narration placeholder for {scene_id}")

    audio_chunks = [
        chunk_audio
        for _graphemes, _phonemes, chunk_audio in pipeline(
            narration_text, voice=VOICE_NAME, speed=SPEECH_SPEED
        )
    ]
    if not audio_chunks:
        raise RuntimeError(f"Kokoro produced no audio for {scene_id}")

    scene_audio = np.concatenate([np.asarray(chunk) for chunk in audio_chunks])
    output_path = OUTPUT_DIRECTORY / f"{scene_id}.wav"
    soundfile.write(output_path, scene_audio, SAMPLE_RATE_HZ)
    duration_seconds = len(scene_audio) / SAMPLE_RATE_HZ
    print(f"{scene_id}: {duration_seconds:.2f}s -> {output_path.name}")
    return duration_seconds


def main() -> None:
    """Generate all scene WAVs and the durations manifest."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    scene_durations = {
        scene_id: synthesize_scene(pipeline, scene_id, narration_text)
        for scene_id, narration_text in SCENE_NARRATIONS
    }
    manifest_path = OUTPUT_DIRECTORY / "durations.json"
    manifest_path.write_text(
        json.dumps(scene_durations, indent=2) + "\n", encoding="utf-8"
    )
    total_seconds = sum(scene_durations.values())
    print(f"total narration: {total_seconds:.2f}s -> {manifest_path}")


if __name__ == "__main__":
    main()
