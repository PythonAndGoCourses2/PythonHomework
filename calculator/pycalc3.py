import sys
import argparse as a
import calculator.logic as c
import importlib as imp
import inspect


def create_parser():
    parser = a.ArgumentParser(description="Pure-python command line calculator")
    parser.add_argument("EXPRESSION", metavar='EXPRESSION', help="expression string to evaluate", type=str, nargs='+')
    parser.add_argument("-m", "--user-modules", help="additional modules to use", type=str, nargs='*')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    solve = ""
    for key, list in args._get_kwargs():
        if key == "EXPRESSION":
            solve = "".join(list)
        if key == "user_modules":
            if list is None:
                break
            else:
                for module in list:
                    imported_module = imp.import_module(module)
                    for func in inspect.getmembers(imported_module, inspect.isfunction):
                        c.func_dictionary[func[0]] = func[1]
    try:
        print(c.solve(solve))
    except Exception as err:
        print("ERROR: {}".format(err))


if __name__ == "__main__":
    main()
