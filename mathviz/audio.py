"""Audio synthesis utilities."""

from __future__ import annotations

import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .sampling import AudioConfig, generate_audio_signal


@dataclass(frozen=True)
class AudioResult:
    samples: np.ndarray
    sample_rate: int


def synthesize_audio(evaluator, config: AudioConfig) -> AudioResult:
    """Generate audio samples from a mathematical evaluator."""

    samples = generate_audio_signal(evaluator, config)
    return AudioResult(samples=samples, sample_rate=config.sample_rate)


def write_wav(path: str | Path, audio: AudioResult) -> Path:
    """Write a mono WAV file to disk."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    samples = np.clip(audio.samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)

    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(audio.sample_rate)
        wav_file.writeframes(int_samples.tobytes())

    return output_path
