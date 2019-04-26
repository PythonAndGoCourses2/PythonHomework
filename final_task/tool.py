import config
import sys


def arithmetic(a, b, token):
    return config.characters[token](a, b)


def functions(token, *args):
    try:
        return config.all_functions[token](*args)
    except KeyError:
        sys.exit('ERROR: this function is not supported.!')
    except TypeError:
        sys.exit('ERROR: invalid number of arguments!')


def constants_calculation(token):
    return config.constants[token]


def comparison_calculation(a, b, token):
    return config.comparison[token](a, b)
