"""Command-line interface for MathViz."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from .pipeline import Pipeline
from .sampling import AudioConfig, SampleConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MathViz: animated math visualization")
    parser.add_argument("expression", help="Expression to visualize, e.g. 'sin(x)'")
    parser.add_argument("--duration", type=float, default=6.0, help="Animation duration in seconds")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--audio-out", type=str, help="Optional path to write a WAV file")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    sample_config = SampleConfig(duration=args.duration, fps=args.fps)
    audio_config = None
    if args.audio_out:
        audio_config = AudioConfig(duration=args.duration)

    pipeline = Pipeline(sample_config=sample_config)
    result = pipeline.run(
        expression=args.expression,
        audio_config=audio_config,
        audio_output=args.audio_out,
    )

    result.animation.figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
