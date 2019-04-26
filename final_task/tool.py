import config
import sys


def arithmetic(a, b, token):
    """Simple calculation."""
    return config.characters[token](a, b)


def functions(token, *args):
    """Calculation math and trigonometry functions."""
    try:
        return config.all_functions[token](*args)
    except KeyError:
        sys.exit('ERROR: this function is not supported.!')
    except TypeError:
        sys.exit('ERROR: invalid number of arguments!')


def constants_calculation(token):
    """Return the value of a constant."""
    return config.constants[token]


def comparison_calculation(a, b, token):
    """Calculation simple logic expression."""
    return config.comparison[token](a, b)
