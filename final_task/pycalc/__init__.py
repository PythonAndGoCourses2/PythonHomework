from . import Parser
from . import Tokenizer
from . import Translator
from . import Calculator


def main():
    """Call of all needed methods and return result"""
    infix_string = Parser.parse_console()
    tokens = Tokenizer.tokenize(infix_string)
    postfix_string = Translator.get_postfix(tokens)
    res = Calculator.calc(postfix_string)
    print(res)


if __name__ == "__main__":
    main()