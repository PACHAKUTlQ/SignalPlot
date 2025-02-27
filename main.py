import sys
from signal_plotter.shell import setup_interactive_shell


def main():
    try:
        for module in ["numpy", "matplotlib", "sympy"]:
            __import__(module)
    except ImportError as e:
        print(f"Error: Missing dependency: {e}")
        print("Please install: pip install numpy matplotlib sympy")
        print("For highlighting: pip install bpython  # or ptpython or IPython")
        sys.exit(1)

    setup_interactive_shell()


if __name__ == "__main__":
    main()
