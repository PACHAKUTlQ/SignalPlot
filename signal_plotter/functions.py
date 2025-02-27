import numpy as np


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
    """Natural logarithm function (alias for log)"""
    return np.log(x)


def sqrt(x):
    """Square root function"""
    return np.sqrt(x)


def abs(x):
    """Absolute value function"""
    return np.abs(x)


def compute_derivative(func_values, t_values):
    """Compute numerical derivative using central differences"""
    dt = t_values[1] - t_values[0]  # Assuming uniform spacing
    derivative = np.gradient(func_values, dt)
    return derivative
