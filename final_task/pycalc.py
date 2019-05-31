import argparse
import check
import core


def create_parser():
    """Parse command line options"""
    parser = argparse.ArgumentParser(prog='pycalc', description="Pure-python command-line calculator.")
    parser.add_argument('expr', metavar='EXPRESSION', help='expression string to evaluate', default='', type=str)
    parser.add_argument('-m', '--use-modules', metavar="MODULE[MODULE...]", help='additional modules to use')
    return parser.parse_args()


def main():
    try:
        expression = create_parser().expr
        comparison = check.comparison_check(expression)
        expression = check.common_check(expression)
        expression = check.replace_whitespace_and_const(expression)
        expression = check.fix_unary(expression)
        expression = check.replace_plus_minus(expression)
        if expression:
            if not comparison:
                if check.brackets_check(expression):
                    print(core.calculating(expression))
            else:
                print(check.comparison_calc(expression, comparison))
        else:
            print("ERROR: no symbols to calculate")
    except OverflowError:
        print("ERROR: numerical result out of range")
    except ZeroDivisionError:
        print("ERROR: division by zero")
    except Exception:
        print("ERROR: incorrect expression")


if __name__ == '__main__':
    main()
