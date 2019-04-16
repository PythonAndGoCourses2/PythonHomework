import readline
import calculator as calc


def readline_configure():
    readline.parse_and_bind('tab: complete')


def main():
    help_msg = \
        "This is calculator for basic math expressions.\n\
Input correct expression and press <ENTER>.\n\
Press 'q <Enter>' to exit."
    readline_configure()

    c = calc.Calculator()

    while True:
        user_input = r'> '
        if user_input == 'h':
            print(help_msg)
        elif user_input == 'q':
            break
        else:
            try:
                result = c.calculate("".join(user_input))
            except (calc.parser.ParseError,
                    calc.converter.ConvertError,
                    calc.converter.ConvertError,
                    calc.evaluator.EvaluateError,
                    ArithmeticError,
                    ValueError) as e:
                print("Error: " + str(e))
            else:
                print("= " + str(result))
