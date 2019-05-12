"""Module to group all other modules"""
from . import Parser
from . import Tokenizer
from . import Translator
from . import Calculator
from . import Exeptions


def main():
    """Call of all needed methods and return result"""
    try:
        infix_string = Parser.parse_console()
        tokens = Tokenizer.tokenize(infix_string)
        postfix_string = Translator.get_postfix(tokens)
        res = Calculator.calc(postfix_string)
        print(res)
    except Exeptions.GeneralError:
        print('ERROR: empty input')
        exit(1)
    except Exeptions.InvalidStringError:
        print('ERROR: invalid string input')
        exit(1)
    except Exeptions.BracketsError:
        print('ERROR: brackets are not balanced')
        exit(1)
    except Exeptions.UnknownFunctionError as ex:
        print(f'ERROR: no such function or operator: \'{ex.token}\'')
        exit(1)
    except Exception:
        print('ERROR: something went wrong')
        exit(1)


if __name__ == "__main__":
    main()
