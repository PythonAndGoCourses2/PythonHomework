"""Module to group all other modules"""
from . import parser
from . import tokenizer
from . import translator
from . import calculator
from . import exeptions


def main():
    """Call of all needed methods and return result"""
    try:
        infix_string = parser.parse_console()
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
    # except Exception:
    #     print('ERROR: something went wrong')
    #     exit(1)


if __name__ == "__main__":
    main()
