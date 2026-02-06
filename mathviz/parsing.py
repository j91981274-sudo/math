"""Expression parsing and safe evaluation utilities."""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np

ALLOWED_FUNCTIONS = {
    name: getattr(math, name)
    for name in (
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sinh",
        "cosh",
        "tanh",
        "exp",
        "log",
        "log10",
        "sqrt",
        "fabs",
    )
}

ALLOWED_NAMES = {
    "pi": math.pi,
    "e": math.e,
}

ALLOWED_NODE_TYPES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
)


@dataclass(frozen=True)
class ParsedExpression:
    """Represents a parsed mathematical expression."""

    raw: str
    variables: tuple[str, ...]
    evaluator: Callable[[np.ndarray], np.ndarray]


def _validate_ast(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODE_TYPES):
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function calls are allowed.")
            if node.func.id not in ALLOWED_FUNCTIONS:
                raise ValueError(f"Function '{node.func.id}' is not allowed.")
        if isinstance(node, ast.Name):
            if node.id in ALLOWED_NAMES:
                continue
            if node.id != "x":
                raise ValueError(f"Unknown variable '{node.id}'.")


def _collect_variables(tree: ast.AST) -> tuple[str, ...]:
    variables = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    variables.difference_update(ALLOWED_NAMES.keys())
    return tuple(sorted(variables))


def parse_expression(raw: str) -> ParsedExpression:
    """Parse a raw expression string into a safe, callable object."""

    tree = ast.parse(raw, mode="eval")
    _validate_ast(tree)
    variables = _collect_variables(tree)
    compiled = compile(tree, filename="<expression>", mode="eval")

    def evaluator(x: np.ndarray) -> np.ndarray:
        env = {"x": x}
        env.update(ALLOWED_FUNCTIONS)
        env.update(ALLOWED_NAMES)
        return eval(compiled, {"__builtins__": {}}, env)

    return ParsedExpression(raw=raw, variables=variables, evaluator=evaluator)


def build_vectorized_evaluator(parsed: ParsedExpression) -> Callable[[np.ndarray], np.ndarray]:
    """Ensure the evaluator is numpy-aware for vectorized input."""

    def vectorized(x: np.ndarray) -> np.ndarray:
        return np.asarray(parsed.evaluator(x), dtype=float)

    return vectorized


def supported_functions() -> Iterable[str]:
    return sorted(ALLOWED_FUNCTIONS.keys())
