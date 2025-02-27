# SignalPlot

A Python tool designed for plotting and analyzing mathematical signals with an interactive shell interface.

## Overview

SignalPlot provides a user-friendly environment for defining, evaluating, and visualizing signal functions. It's particularly useful for signal processing, electrical engineering, and mathematical analysis of time-varying functions.

## Features

- **Interactive Shell**: Enhanced Python REPL with syntax highlighting (supports bpython, ptpython, and IPython)
- **Function Definition**: Define custom functions that can be reused
- **Plotting**: Easily visualize signal functions with customizable plotting parameters
- **Built-in Functions**:
  - Basic mathematical functions: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`
  - Signal processing functions: `rect` (rectangular function), `u` (unit step function)
- **Derivatives**: Automatically calculate and plot derivatives of functions
- **Signal Transformations**: Easily visualize time-scaling, time-shifting, and other transformations

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/PACHAKUTlQ/SignalPlot.git
    cd SignalPlot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    By default both [bpython](https://github.com/bpython/bpython) and [ptpython](https://github.com/prompt-toolkit/ptpython) interactive shells are installed. bpython only works on Unix-like systems. It will automatically fall back to ptpython if fails with bpython.

## Usage

Run the application:

```shell
python main.py
```

### Basic Examples

In the interactive shell:

```python
# Define a function
define_function("x", "sin(t) * exp(-0.2*t)")

# Plot the function
parse_and_plot("x(t)")

# Plot with custom range
parse_and_plot("x(t)", t_min=-10, t_max=10)

# Plot derivative
parse_and_plot("d(x(t))/d(t)")

# Plot time-scaled function
parse_and_plot("x(2*t)")

# Plot time-shifted function
parse_and_plot("x(t-2)")
```

### Advanced Examples

```python
# Define a complex rectangular pulse signal
define_function("x", "(t+2)*rect(t+3/2)-t*rect(t+1/2)+t*rect(t-1/2)+u(t-1)")

# Plot the function
parse_and_plot("x(t)")

# Even and odd components
parse_and_plot("1/2*(x(t)+x(-t))")  # Even component
parse_and_plot("1/2*(x(t)-x(-t))")  # Odd component

# Define netted functions
define_function("x", "d(sin(t))/d(t)")
define_function("y", "x(2*t)*u(t)+rect(-2*t-1)")
define_function("z", "cos(x(2*t))*u(t)+rect(-2*t-1)")

parse_and_plot("z(t)")

# Plot netted derivative
parse_and_plot("d(z(t))/d(t)")
```

## Available Functions

- [x] `define_function(name, expression)`: Define a custom function
- [x] `parse_and_plot(expression, t_min=-5, t_max=5, num_points=1000)`: Plot a function
- [x] Signal functions: `rect(x)`, `u(x)`
- [x] Mathematical functions: `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`, `log(x)`, `ln(x)`, `sqrt(x)`, `abs(x)`
- [x] Derivative notation over `t`: `d(func)/d(t)`
- [ ] Derivative notation: `diff(func)`
- [ ] Integration notation: `integral(func, x_min, x_max)`
- [ ] Derivative and integration over variables other than `t`
- [ ] Convolution: `conv(func_1, func_2)`

## Dependencies

- **NumPy**: Numerical computing
- **Matplotlib**: Plotting library
- **SymPy**: Symbolic mathematics
- Optional (for enhanced shell):
  - **bpython**: Most user-friendly enhanced Python REPL, only supports Unix-like systems
  - **ptpython**: Enhanced Python REPL
  - **IPython**: Enhanced Python REPL


## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.