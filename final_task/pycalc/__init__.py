import Parser
import Tokenizer
import Translator


def main():
    """The main routine    ."""
    infix_string = Parser.parse_console()
    tokens = Tokenizer.tokenize(infix_string)
    postfix_string = Translator.get_postfix(tokens)
    print(postfix_string)


if __name__ == "__main__":
    main()