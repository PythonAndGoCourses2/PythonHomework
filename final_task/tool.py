import config


def arithmetic(a, b, token):
    return config.characters[token](a, b)


def functions(token, *args):
    return config.all_functions[token](*args)


def constants_calculation(token):
    return config.constants[token]


def comparison_calculation(a, b, token):
    return config.comparison[token](a, b)
