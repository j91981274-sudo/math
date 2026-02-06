"""Sampling utilities for time-based animation and audio."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SampleConfig:
    duration: float = 6.0
    fps: int = 30
    x_min: float = -6.0
    x_max: float = 6.0
    x_points: int = 400

    @property
    def frames(self) -> int:
        return int(self.duration * self.fps)


@dataclass(frozen=True)
class AudioConfig:
    sample_rate: int = 44100
    duration: float = 6.0
    base_frequency: float = 220.0
    frequency_range: float = 440.0
    amplitude: float = 0.3


def sample_expression(
    evaluator,
    config: SampleConfig,
    phase: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Sample an expression over x with a time-varying phase."""

    x = np.linspace(config.x_min, config.x_max, config.x_points)
    y = evaluator(x + phase)
    return x, y


def normalize(values: np.ndarray) -> np.ndarray:
    if values.size == 0:
        return values
    min_val = float(np.min(values))
    max_val = float(np.max(values))
    if max_val - min_val == 0:
        return np.zeros_like(values)
    return (values - min_val) / (max_val - min_val)


def generate_audio_signal(
    evaluator,
    config: AudioConfig,
) -> np.ndarray:
    """Generate a mono audio signal by mapping expression values to frequency."""

    total_samples = int(config.sample_rate * config.duration)
    t = np.linspace(0, config.duration, total_samples, endpoint=False)
    x = 2 * np.pi * t
    raw = evaluator(x)
    normalized = normalize(raw)
    frequency = config.base_frequency + normalized * config.frequency_range
    phase = 2 * np.pi * np.cumsum(frequency) / config.sample_rate
    audio = config.amplitude * np.sin(phase)
    return audio.astype(np.float32)
