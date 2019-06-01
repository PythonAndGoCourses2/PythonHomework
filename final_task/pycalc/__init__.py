"""Module to group all other modules"""
from pycalc import parser
from pycalc import tokenizer
from pycalc import translator
from pycalc import calculator
from pycalc.library import Library


def main():
    """Call of all needed methods and return result"""
    try:
        infix_string = parser.parse_arguments()
        if isinstance(infix_string, tuple):
            process_modules(infix_string[0])
            infix_string = infix_string[1]
        tokens = tokenizer.tokenize(infix_string)
        postfix_string = translator.get_postfix(tokens)
        res = calculator.calculate(postfix_string)
        print(res)
    except Exception as ex:
        print(f'ERROR: {ex}')
        exit(1)


def process_modules(module_names):
    for name in module_names:
        Library().read_user_module(name)


if __name__ == "__main__":
    main()
