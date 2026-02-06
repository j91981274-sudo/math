"""Analyze parsed expressions to determine visualization strategy."""

from __future__ import annotations

from dataclasses import dataclass

from .parsing import ParsedExpression


@dataclass(frozen=True)
class ExpressionAnalysis:
    """Metadata about an expression to guide visualization and audio."""

    variables: tuple[str, ...]
    expression_type: str
    visualization: str


def analyze_expression(parsed: ParsedExpression) -> ExpressionAnalysis:
    """Determine the expression type and visualization strategy."""

    if parsed.variables == ("x",):
        expression_type = "single_variable"
        visualization = "animated_line"
    elif not parsed.variables:
        expression_type = "scalar"
        visualization = "oscillating_point"
    else:
        expression_type = "unsupported"
        visualization = "none"

    return ExpressionAnalysis(
        variables=parsed.variables,
        expression_type=expression_type,
        visualization=visualization,
    )
