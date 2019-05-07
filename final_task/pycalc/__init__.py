import Parser
import Tokenizer


def main():
    """The main routine    ."""
    infix_string = Parser.parse_console()
    tokens = Tokenizer.tokenize(infix_string)
    print(tokens)


if __name__ == "__main__":
    main()