"""Pipeline orchestration for MathViz."""

from __future__ import annotations

from dataclasses import dataclass

from .analysis import ExpressionAnalysis, analyze_expression
from .audio import AudioResult, synthesize_audio, write_wav
from .parsing import ParsedExpression, build_vectorized_evaluator, parse_expression
from .sampling import AudioConfig, SampleConfig
from .visualization import AnimationResult, animate_expression


@dataclass
class PipelineResult:
    parsed: ParsedExpression
    analysis: ExpressionAnalysis
    animation: AnimationResult
    audio: AudioResult | None


class Pipeline:
    """High-level interface for parsing, analysis, visualization, and audio."""

    def __init__(self, sample_config: SampleConfig | None = None):
        self.sample_config = sample_config or SampleConfig()

    def run(
        self,
        expression: str,
        audio_config: AudioConfig | None = None,
        audio_output: str | None = None,
    ) -> PipelineResult:
        parsed = parse_expression(expression)
        analysis = analyze_expression(parsed)
        evaluator = build_vectorized_evaluator(parsed)

        if analysis.expression_type != "single_variable":
            raise ValueError("Only single-variable expressions are supported in this version.")

        animation = animate_expression(evaluator, self.sample_config)

        audio = None
        if audio_config:
            audio = synthesize_audio(evaluator, audio_config)
            if audio_output:
                write_wav(audio_output, audio)

        return PipelineResult(
            parsed=parsed,
            analysis=analysis,
            animation=animation,
            audio=audio,
        )
