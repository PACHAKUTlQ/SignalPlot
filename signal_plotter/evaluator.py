import numpy as np
import re
from .functions import (
    rect,
    u,
    sin,
    cos,
    tan,
    exp,
    log,
    ln,
    sqrt,
    abs,
    compute_derivative,
)

# Store function definitions
function_definitions = {}


def define_function(name, expr):
    """Store a function definition for later use"""
    function_definitions[name] = expr
    print(f"Function {name} defined as {expr}")


def evaluate_function(func_name, t_expr, t_values):
    """Evaluate a defined function with a transformed time variable"""
    if func_name not in function_definitions:
        raise ValueError(f"Function '{func_name}' is not defined")

    func_expr = function_definitions[func_name]
    t_modified = eval(
        t_expr.replace("t", "t_values"),
        {"__builtins__": {}},
        {"t_values": t_values, "np": np},
    )
    return evaluate_expression(func_expr, t_modified)


def evaluate_expression(expr, t_values):
    """Evaluate a mathematical expression with given t values."""

    derivative_pattern = r"d\((.*?)\)/d\(t\)"
    derivative_matches = re.findall(derivative_pattern, expr)

    for inner_expr in derivative_matches:
        inner_result = evaluate_expression(inner_expr, t_values)
        if inner_result is not None:
            derivative = compute_derivative(inner_result, t_values)
            placeholder = f"__DERIVATIVE_RESULT_{hash(inner_expr)}_"
            expr = expr.replace(f"d({inner_expr})/d(t)", placeholder)
            globals()[placeholder] = derivative

    processed_expr = process_rect_expressions(expr)
    func_pattern = r"([a-zA-Z]+)\(([^()]+)\)"

    def replace_func_call(match):
        func_name = match.group(1)
        t_expr = match.group(2)
        if func_name in function_definitions:
            return f"evaluate_function('{func_name}', '{t_expr}', t)"
        return match.group(0)

    processed_expr = re.sub(func_pattern, replace_func_call, processed_expr)

    try:
        namespace = {
            "t": t_values,
            "rect": rect,
            "u": u,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "exp": exp,
            "log": log,
            "ln": ln,
            "sqrt": sqrt,
            "abs": abs,
            "np": np,
            "compute_derivative": compute_derivative,
            "evaluate_function": evaluate_function,
        }

        for key, value in globals().items():
            if key.startswith("__DERIVATIVE_RESULT_"):
                namespace[key] = value

        result = eval(processed_expr, {"__builtins__": {}}, namespace)

        for key in list(globals().keys()):
            if key.startswith("__DERIVATIVE_RESULT_"):
                del globals()[key]
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None


def process_rect_expressions(expr):
    """Process rect expressions, handling both rect((t-a)/b) and rect(t-a)."""
    processed = expr

    # rect((t-a)/b)
    pattern_rect = (
        r"rect\(\s*\(\s*t\s*([+-])\s*(\d+(?:\.\d+)?)\s*\)\s*/\s*(\d+(?:\.\d+)?)\s*\)"
    )
    matches = list(re.finditer(pattern_rect, processed))
    for match in reversed(matches):
        sign, a, b = match.groups()
        center = -float(a) if sign == "+" else float(a)
        replacement = f"rect((t-{center})/{b})"
        processed = processed[: match.start()] + replacement + processed[match.end() :]

    # rect(t-a)
    pattern_rect_simple = r"rect\(\s*t\s*([+-])\s*(\d+(?:\.\d+)?)\s*\)"
    matches = list(re.finditer(pattern_rect_simple, processed))
    for match in reversed(matches):
        sign, a = match.groups()
        center = -float(a) if sign == "+" else float(a)
        replacement = f"rect((t-{center})/1)"
        processed = processed[: match.start()] + replacement + processed[match.end() :]

    return processed
