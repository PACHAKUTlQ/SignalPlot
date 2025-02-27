import code
import os
from .evaluator import define_function
from .plotter import parse_and_plot
from .functions import *
import numpy as np
import matplotlib.pyplot as plt


def show_help():
    """Display help information."""
    help_text = """
Function Plotter Interactive Shell

Available functions:
  define_function(name, expression) - Define a function.
      Example: define_function("x", "t + 2")

  parse_and_plot(expression, t_min=-5, t_max=5, num_points=1000) - Plot.
      Example: parse_and_plot("x(t)")
      Example: parse_and_plot("sin(t)", -10, 10)

  rect(x), u(x), sin(x), cos(x), tan(x), exp(x), log(x), ln(x), sqrt(x), abs(x)

  Derivatives: d(expression)/d(t)
      Example: parse_and_plot("d(sin(t))/d(t)")

  help() - Show this help message
  show_help() - Show this help message
  exit() - Exit

Examples:
  define_function("x", "(t+2)*rect(t+3/2)-t*rect(t+1/2)+t*rect(t-1/2)+u(t-1)")
  parse_and_plot("x(t)")
  parse_and_plot("d(sin(t))/d(t)")
  parse_and_plot("x(-t)")
  parse_and_plot("1/2*(x(t)+x(-t))")
  parse_and_plot("x(2*t+1)")
"""
    print(help_text)


def setup_interactive_shell():
    """Set up the interactive shell."""
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

    # Regular tab completion and history
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

    # Try bpython, ptpython, then IPython, falling back to standard REPL
    for shell_type in ["bpython", "ptpython", "IPython", "standard"]:
        try:
            if shell_type == "bpython":
                from bpython import embed

                print("Starting enhanced shell (bpython)...")
                print("Type show_help() for commands and examples.")
                embed(locals_=namespace)
                return
            elif shell_type == "ptpython":
                from ptpython.repl import embed

                print("Starting enhanced shell (ptpython)...")
                print("Type help() for commands and examples.")
                embed(
                    globals=namespace,
                    vi_mode=True,
                    history_filename=os.path.expanduser("~/.pythonhist"),
                )
                return
            elif shell_type == "IPython":
                from IPython import embed

                print("Starting enhanced shell (IPython)...")
                print("Type help() for commands and examples.")
                embed(user_ns=namespace)
                return
        except ImportError:
            pass

    print(
        "Syntax highlighting not available. Install 'bpython', 'ptpython', or 'IPython'."
    )
    code.interact(local=namespace, banner="")
