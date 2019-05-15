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
        res = calculator.calc(postfix_string)
        print(res)
    except exeptions.GeneralError:
        print('ERROR: empty input')
        exit(1)
    except exeptions.InvalidStringError:
        print('ERROR: invalid string input')
        exit(1)
    except exeptions.BracketsError:
        print('ERROR: brackets are not balanced')
        exit(1)
    except exeptions.UnknownFunctionError as ex:
        print(f'ERROR: no such function or operator: \'{ex.token}\'')
        exit(1)
    except OverflowError:
        print("ERROR: numerical result out of range")
        exit(1)
    except ZeroDivisionError:
        print("ERROR: division by zero")
        exit(1)


if __name__ == "__main__":
    main()
