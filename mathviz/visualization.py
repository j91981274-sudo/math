"""Visualization primitives for MathViz."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .sampling import SampleConfig, sample_expression


@dataclass(frozen=True)
class AnimationResult:
    animation: FuncAnimation
    figure: plt.Figure


def animate_expression(evaluator, config: SampleConfig) -> AnimationResult:
    """Create a Matplotlib animation for a single-variable expression."""

    fig, ax = plt.subplots()
    ax.set_xlim(config.x_min, config.x_max)
    ax.set_ylim(-2, 2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("MathViz: Animated Expression")

    (line,) = ax.plot([], [], lw=2)

    def init():
        line.set_data([], [])
        return (line,)

    def update(frame: int):
        phase = (frame / config.frames) * 2 * 3.14159
        x, y = sample_expression(evaluator, config, phase)
        line.set_data(x, y)
        return (line,)

    animation = FuncAnimation(
        fig,
        update,
        frames=config.frames,
        init_func=init,
        blit=True,
        interval=1000 / config.fps,
    )

    return AnimationResult(animation=animation, figure=fig)
