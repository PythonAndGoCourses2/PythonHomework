from . import Parser
from . import Tokenizer
from . import Translator
from . import Calculator


def main():
    """The main routine    ."""
    infix_string = Parser.parse_console()
    tokens = Tokenizer.tokenize(infix_string)
    postfix_string = Translator.get_postfix(tokens)
    res = Calculator.calc(postfix_string)
    print(postfix_string)


if __name__ == "__main__":
    main()