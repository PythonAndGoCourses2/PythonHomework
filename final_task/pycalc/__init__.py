import parser


def main():
    """The main routine    ."""
    infix_string = parser.parse_console()
    print(infix_string)


def is_number(s):
    return s.isdigit()


if __name__ == "__main__":
    main()