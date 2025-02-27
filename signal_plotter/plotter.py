import matplotlib.pyplot as plt
import numpy as np
import re
from .evaluator import evaluate_expression, define_function


def parse_and_plot(expression, t_min=-5, t_max=5, num_points=1000):
    """Parse and plot a function expression."""

    if "=" in expression and re.match(r"^[a-zA-Z]+\([a-zA-Z]\)\s*=", expression):
        func_name = expression.split("(")[0].strip()
        func_expr = expression.split("=", 1)[1].strip()
        define_function(func_name, func_expr)
        return  # Don't plot when defining a function

    t_values = np.linspace(t_min, t_max, num_points)
    y_values = evaluate_expression(expression, t_values)

    if y_values is None:
        return

    plt.figure(figsize=(10, 6))
    plt.plot(t_values, y_values, "b-")
    plt.grid(True)
    plt.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    plt.axvline(x=0, color="k", linestyle="-", alpha=0.3)
    plt.title(f"Plot of {expression}")
    plt.xlabel("t")
    plt.ylabel("amplitude")
    plt.show()
