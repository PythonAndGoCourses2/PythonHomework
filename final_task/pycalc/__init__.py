from myParser import parse_console


def main():
    """The main routine."""
    infixstring = parse_console()
    print(infixstring)


def is_number(s):
    return s.isdigit()


if __name__ == "__main__":
    main()
