import argparse
import pycalc.main as Main


def main():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator")
    parser.add_argument("EXPRESSION", type=str, help='expression string to evaluate')
    parser.add_argument('-m MODULE[MODULE...]', '--use-modules MODULE[MODULE...]', nargs='*',
                        help='additional modules to use', dest='modules', type=str, default=['math'])
    args = parser.parse_args(["1+2*3=="])

    answer = Main.pycalc(args.EXPRESSION, args.modules)
    if type(answer) == float or type(answer) == int:
        if answer % 1 == 0:
            return int(answer)
        else:
            return answer
    else:
        return answer
