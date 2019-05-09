import argparse

PARSER = {
    'description': 'Pure-python command-line calculator.'
}

EXPRESSION = {
    'name_or_flags': ['expression'],
    'keyword_arguments': {
        'metavar': 'EXPRESSION',
        'type': str,
        'help': 'expression string to evaluate'
    }
}

MODULE = {
    'name_or_flags': ['-m', '--use-modules'],
    'keyword_arguments': {
        'metavar': 'MODULE',
        'type': str,
        'nargs': '+',
        'help': 'additional modules to use',
        'dest': 'modules'
    }
}

ARGUMENTS = [
    EXPRESSION,
    MODULE,
]

parser = argparse.ArgumentParser(**PARSER)

for arg in ARGUMENTS:
    parser.add_argument(*arg['name_or_flags'], **arg['keyword_arguments'])

args = parser.parse_args()
