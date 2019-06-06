import argparse
import calc


def main():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument("EXPRESSION", help="Please, enter an expression for calculating", type=str)
    args = parser.parse_args()
    result = calc.pols_not(calc.tran_in_pol_not(args.EXPRESSION))
    print(result)


if __name__ == '__main__':
    main()