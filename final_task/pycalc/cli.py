import argparse
import calculator


def create_parser():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument('EXPRESSION', help='iExpr string to evaluate',)
    args = parser.parse_args()
    iExpr = args.EXPRESSION
    return iExpr

def main():
    try:
        iExpr = create_parser()
        if iExpr:
            calc = calculator.Calculator()
            print(calc.calculate(iExpr))
        else:
            raise Exception('empty expression')
    except Exception as error:
        print("ERROR: " + str(error))
if __name__ == '__main__':
    main()