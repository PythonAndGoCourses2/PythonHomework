import argparse


def create_parser():
    parser = argparse.ArgumentParser(prog='pycalc', description="Pure-python command-line calculator.")
    parser.add_argument('EXPRESSION', help='expression string to evaluate', type=str)
    print(parser.parse_args())
    return parser.parse_args()

# Создать оформление справки и ошибок
