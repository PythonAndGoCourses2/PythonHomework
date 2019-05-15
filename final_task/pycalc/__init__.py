"""Module to group all other modules"""
from pycalc import parser
from pycalc import tokenizer
from pycalc import translator
from pycalc import calculator
from pycalc import exeptions


def main():
    """Call of all needed methods and return result"""
    try:
        infix_string = parser.parse_arguments()
        tokens = tokenizer.tokenize(infix_string)
        postfix_string = translator.get_postfix(tokens)
        res = calculator.calculate(postfix_string)
        print(res)
    except Exception as ex:
        print(f'ERROR: {ex}')
        exit(1)


if __name__ == "__main__":
    main()
