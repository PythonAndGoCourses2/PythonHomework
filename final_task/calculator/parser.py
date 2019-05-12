import argparse

def parse_query():
    """
    Convert argument strings to objects and assign them as attributes of the namespace.

    Returns:
        Namespace: got data from command line.
    """
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('expr', metavar='EXPRESSION', help='expression string to evaluate')
    parser.add_argument('-m',
                        '--use-modules',
                        default=[],
                        dest='modules',
                        metavar='MODULE',
                        nargs='+',
                        help='additional modules to use')

    return parser.parse_args()
