import numpy as np
import matplotlib.pyplot as plt
import re
import code
import os
import sys


def rect(x):
    """Rectangular function: 1 for |x| <= 0.5, 0 elsewhere"""
    return np.where(np.abs(x) <= 0.5, 1.0, 0.0)


def u(x):
    """Unit step function: 1 for x >= 0, 0 elsewhere"""
    return np.where(x >= 0, 1.0, 0.0)


def sin(x):
    """Sine function"""
    return np.sin(x)


def cos(x):
    """Cosine function"""
    return np.cos(x)


def tan(x):
    """Tangent function"""
    return np.tan(x)


def exp(x):
    """Exponential function"""
    return np.exp(x)


def log(x):
    """Natural logarithm function"""
    return np.log(x)


def ln(x):
    """Natural logarithm function"""
    return np.log(x)


def sqrt(x):
    """Square root function"""
    return np.sqrt(x)


def abs(x):
    """Absolute value function"""
    return np.abs(x)


def compute_derivative(func_values, t_values):
    """Compute numerical derivative of a function using central differences"""
    dt = t_values[1] - t_values[0]  # Assuming uniform spacing
    derivative = np.gradient(func_values, dt)
    return derivative


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

    # Get the original function expression
    func_expr = function_definitions[func_name]

    # Create t values based on the provided expression (e.g., -t, 2*t+1)
    t_modified = eval(
        t_expr.replace("t", "t_values"),
        {"__builtins__": {}},
        {"t_values": t_values, "np": np},
    )

    # Evaluate the function with the modified t values
    # We need to evaluate the original expression each time
    # rather than storing pre-computed values
    result = evaluate_expression(func_expr, t_modified)

    return result


def evaluate_expression(expr, t_values):
    """Evaluate a mathematical expression with the given t values"""
    # Check for derivative notation d(expression)/d(t)
    derivative_pattern = r"d\((.*?)\)/d\(t\)"
    derivative_matches = re.findall(derivative_pattern, expr)

    # Replace derivatives with their computed values
    for inner_expr in derivative_matches:
        # Evaluate the inner expression
        inner_result = evaluate_expression(inner_expr, t_values)

        if inner_result is not None:
            # Compute the derivative
            derivative = compute_derivative(inner_result, t_values)

            # Create a unique placeholder to avoid nested pattern conflicts
            placeholder = f"__DERIVATIVE_RESULT_{hash(inner_expr)}_"
            expr = expr.replace(f"d({inner_expr})/d(t)", placeholder)

            # Store for later substitution
            globals()[placeholder] = derivative

    # Process the expression (same as before)
    processed_expr = process_rect_expressions(expr)

    # Check for function calls like x(t), x(-t), x(2*t+1)
    func_pattern = r"([a-zA-Z]+)\(([^()]+)\)"

    def replace_func_call(match):
        func_name = match.group(1)
        t_expr = match.group(2)

        if func_name in function_definitions:
            # This is a placeholder - we'll handle the actual evaluation later
            return f"evaluate_function('{func_name}', '{t_expr}', t)"

        return match.group(0)

    # Replace all function calls
    processed_expr = re.sub(func_pattern, replace_func_call, processed_expr)

    try:
        # Create namespace with available functions and variables
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

        # Add derivative placeholders to namespace
        for key, value in globals().items():
            if key.startswith("__DERIVATIVE_RESULT_"):
                namespace[key] = value

        # Evaluate the expression
        result = eval(processed_expr, {"__builtins__": {}}, namespace)

        # Clean up derivative placeholders
        for key in list(globals().keys()):
            if key.startswith("__DERIVATIVE_RESULT_"):
                del globals()[key]
        # print(f"Debug - expression to evaluate: {processed_expr}")
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None


def process_rect_expressions(expr):
    """Process rect expressions in the given string"""
    # Create a modified version of the expression that can be evaluated with numpy
    processed = expr

    # Replace rect((t-a)/b) format
    pattern_rect = (
        r"rect\(\s*\(\s*t\s*([+-])\s*(\d+(?:\.\d+)?)\s*\)\s*/\s*(\d+(?:\.\d+)?)\s*\)"
    )

    # Process once instead of using a while loop to avoid infinite recursion
    matches = list(re.finditer(pattern_rect, processed))

    # Process in reverse order to preserve indices
    for match in reversed(matches):
        sign, a, b = match.groups()
        a = float(a)
        b = float(b)
        if sign == "-":
            center = a
        else:
            center = -a

        # Create a normalized replacement that won't match the pattern again
        replacement = f"rect((t-{center})/{b})"

        processed = processed[: match.start()] + replacement + processed[match.end() :]

    # Replace rect(t-a) with rect((t-a)/1) format
    pattern_rect_simple = r"rect\(\s*t\s*([+-])\s*(\d+(?:\.\d+)?)\s*\)"

    # Process once instead of using a while loop
    matches = list(re.finditer(pattern_rect_simple, processed))

    # Process in reverse order to preserve indices
    for match in reversed(matches):
        sign, a = match.groups()
        a = float(a)
        if sign == "-":
            center = a
        else:
            center = -a

        replacement = f"rect((t-{center})/1)"
        processed = processed[: match.start()] + replacement + processed[match.end() :]

    return processed


def parse_and_plot(expression, t_min=-5, t_max=5, num_points=1000):
    """Parse and plot a function expression involving rect and u functions"""
    # Check if this is a function definition
    if "=" in expression and re.match(r"^[a-zA-Z]+\([a-zA-Z]\)\s*=", expression):
        func_name = expression.split("(")[0].strip()
        func_expr = expression.split("=", 1)[1].strip()
        define_function(func_name, func_expr)
        print(f"Function {func_name} defined as {func_expr}")
        return

    # Create t values for plotting
    t_values = np.linspace(t_min, t_max, num_points)

    # Evaluate the expression
    y_values = evaluate_expression(expression, t_values)

    if y_values is None:
        return

    # Plot the function
    plt.figure(figsize=(10, 6))
    plt.plot(t_values, y_values, "b-")
    plt.grid(True)
    plt.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    plt.axvline(x=0, color="k", linestyle="-", alpha=0.3)
    plt.title(f"Plot of {expression}")
    plt.xlabel("t")
    plt.ylabel("amplitude")
    plt.show()


def show_help():
    """Display help information for the interactive shell."""
    help_text = """
Function Plotter Interactive Shell

Available functions:
  define_function(name, expression) - Define a function for later use
      Example: define_function("x", "(t+2)*rect(t+3/2)+u(t-1)")

  parse_and_plot(expression, t_min=-5, t_max=5, num_points=1000) - Plot a function
      Example: parse_and_plot("x(t)")
      Example: parse_and_plot("1/2*(x(t)+x(-t))", -10, 10)

  rect(x) - Rectangular function: 1 for |x| <= 0.5, 0 elsewhere
  u(x) - Unit step function: 1 for x >= 0, 0 for x < 0
  
  Derivatives can be plotted using d(expression)/d(t) notation
      Example: parse_and_plot("d(sin(t))/d(t)")
      Example: define_function("x", "d(sin(t))/d(t)") 

  help() - Show this help message
  show_help() - Show this help message
  exit() - Exit the interactive shell

Examples:
  Define and plot a function:
    >>> define_function("x", "(t+2)*rect(t+3/2)-t*rect(t+1/2)+t*rect(t-1/2)+u(t-1)")
    >>> parse_and_plot("x(t)")
    
  Plot a derivative:
    >>> parse_and_plot("d(sin(t))/d(t)")
    >>> define_function("x", "d(sin(t))/d(t)")
    >>> parse_and_plot("x(t)")

  Plot function transformations:
    >>> parse_and_plot("x(-t)")
    >>> parse_and_plot("1/2*(x(t)+x(-t))")
    >>> parse_and_plot("x(2*t+1)")
"""
    print(help_text)


def setup_interactive_shell():
    """Set up an interactive Python shell with all functions loaded."""
    # Create namespace with all relevant functions
    namespace = {
        "np": np,
        "plt": plt,
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
        "define_function": define_function,
        "parse_and_plot": parse_and_plot,
        "help": show_help,
        "show_help": show_help,
    }

    # Regular tab completion and history setup
    try:
        import readline
        import rlcompleter

        readline.parse_and_bind("tab: complete")
        completer = rlcompleter.Completer(namespace)
        readline.set_completer(completer.complete)

        history_file = os.path.join(os.path.expanduser("~"), ".pythonhist")
        try:
            readline.read_history_file(history_file)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        import atexit

        atexit.register(readline.write_history_file, history_file)
    except (ImportError, ModuleNotFoundError):
        pass

    print("\n=== Signal Function Plotter Interactive Shell ===")

    # Try to use bpython for syntax highlighting (preferred)
    try:
        from bpython import embed

        print("Starting enhanced shell with syntax highlighting...")
        print(
            "Type show_help() for available commands and examples."
        )  # help() is a bpython builtin
        embed(locals_=namespace)
        return
    except ImportError:
        pass

    # Try to use ptpython for syntax highlighting (alternate)
    try:
        from ptpython.repl import embed

        print("Starting enhanced shell with syntax highlighting...")
        print("Type help() for available commands and examples.")
        embed(
            globals=namespace,
            vi_mode=True,
            history_filename=os.path.expanduser("~/.pythonhist"),
        )
        return
    except ImportError:
        pass

    # Try to use IPython for syntax highlighting (alternate)
    try:
        from IPython import embed

        print("Starting enhanced shell with syntax highlighting...")
        print("Type help() for available commands and examples.")
        embed(user_ns=namespace)
        return
    except ImportError:
        pass

    # Fall back to standard Python REPL
    print(
        "Syntax highlighting not available. Install 'ptpython' or 'ipython' for an enhanced experience."
    )
    code.interact(local=namespace, banner="")


if __name__ == "__main__":
    try:
        # Dependency check
        for module in ["numpy", "matplotlib", "sympy"]:
            __import__(module)
    except ImportError as e:
        print(f"Error: Missing required dependency: {e}")
        print("Please install the required packages:")
        print("pip install numpy matplotlib")
        print("\nFor syntax highlighting, also consider installing:")
        print("pip install bpython  # or ptpython or IPython")
        sys.exit(1)

    setup_interactive_shell()
