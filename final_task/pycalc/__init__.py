import Parser
import Tokenizer
import Translator
import Calculator


def main():
    """The main routine    ."""
    infix_string = Parser.parse_console()
    tokens = Tokenizer.tokenize(infix_string)
    postfix_string = Translator.get_postfix(tokens)
    res = Calculator.calc(postfix_string)
    print(res)


if __name__ == "__main__":
    main()