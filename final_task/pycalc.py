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
        comparison = check.check_comparison(expression)
        expression = check.check_correct_whitespace(expression)
        expression = check.replace_whitespace_and_const(expression)
        expression = check.fix_unary(expression)
        expression = check.replace_plus_minus(expression)
        if check.check_brackets(expression) and check.check_unknown_func(expression) and check.check_arg_function(
                expression):
            if not comparison:
                print(core.calculating(expression))
            else:
                print(check.comparison_calc(expression, comparison))
        else:
            print("ERROR: incorrect expression")
    except OverflowError:
        print("ERROR: numerical result out of range")
    except ZeroDivisionError:
        print("ERROR: division by zero")
    except Exception:
        print("ERROR: incorrect expression")


if __name__ == '__main__':
    main()
