# MathViz

MathViz is a minimal, extensible Python system for converting mathematical expressions into animated visualizations and synchronized, programmatic audio. The initial implementation focuses on single-variable expressions (e.g., `sin(x)`, `x**2`, `exp(-x) * cos(3*x)`) and provides a foundation for adding additional expression types, renderers, and sound mappings.

## Features
- **Safe expression parsing** from plain-text input
- **Structured analysis** to determine dimensionality and visualization strategy
- **Animated visualization** using time-based sampling
- **Synthetic audio generation** derived from the same mathematical representation
- **Modular architecture** for extensibility

## Quick Start

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run a demo animation with optional audio:

```bash
python -m mathviz "sin(x)" --duration 8 --audio-out output.wav
```

## Ubuntu Terminal Layout

The project is intentionally small and terminal-friendly. The expected file structure is:

```text
math/
├── README.md
├── requirements.txt
└── mathviz/
    ├── __init__.py
    ├── __main__.py
    ├── analysis.py
    ├── audio.py
    ├── cli.py
    ├── parsing.py
    ├── pipeline.py
    ├── sampling.py
    └── visualization.py
```

## Architecture Overview

- `mathviz/parsing.py` — input parsing and safe evaluation
- `mathviz/analysis.py` — expression introspection and routing decisions
- `mathviz/sampling.py` — time-based sampling of the mathematical model
- `mathviz/visualization.py` — animated rendering
- `mathviz/audio.py` — real-time-capable audio synthesis and WAV export
- `mathviz/cli.py` — command-line entry point

## Extending

Add new analysis strategies, visualization renderers, or audio mappings by registering them in the relevant modules. The core `Pipeline` wires components together without requiring changes to support new types.
