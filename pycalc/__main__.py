import argparse
from pycalc.pycalc import myresult


def main():
    try:
        parser = argparse.ArgumentParser(
            'pycalc', description="Command-line calculator.",
            usage='pycalc [-h] EXPRESSION')
        parser.add_argument('EXPRESSION', type=str, help='Input string to evaluate', )
        exp = parser.parse_args()
        exp = exp.EXPRESSION
        print(myresult(exp))
    except Exception as exp:
        print(f'ERROR: {exp}')


if __name__ == '__main__':
    main()
