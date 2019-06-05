"""
Initialize a calculator and calculate
an expression from a command line argument.
"""

import sys

from pycalc.args import get_args
from pycalc.calculator import calculator, CalculatorError

ERROR_MSG_PREFIX = 'ERROR: '


class Cli:
    """Command line interface for a calculator."""

    def __init__(self):
        self.args = get_args()
        self.calculator = None

    def run(self):
        """Initialize a calculator and make a calculation."""

        modules = self.args.modules
        self.init_calculator(modules)

        expression = self.args.expression
        self.calculate(expression)

    def init_calculator(self, modules):
        """Initialize a calculator."""

        try:
            self.calculator = calculator(modules)
            return

        except CalculatorError as exc:
            err_msg = exc.err_msg
            self.on_error(err_msg)

    def calculate(self, expression):
        """Make a calculation."""

        assert callable(
            self.calculator.calculate), 'calculate is not a callable'

        try:
            result = self.calculator.calculate(expression)
            self.on_success(result)
            return

        except CalculatorError as exc:
            err_msg = exc.err_msg

        except Exception as exc:
            err_msg = str(exc)

        self.on_error(err_msg)

    def on_success(self, result):
        """Run if a calculation was succesfull."""

        self.exit(result)

    def on_error(self, err_msg):
        """Run if there were initialization or calculation errors."""

        message = self.prefix_err_msg(err_msg)
        self.exit(message, is_error=True)

    def exit(self, message, is_error=False):
        """Print a message and exit."""

        print(message)

        if is_error:
            sys.exit(1)

        sys.exit()

    def prefix_err_msg(self, msg):
        """Return an error message with an error prefix."""

        return f'{ERROR_MSG_PREFIX}{msg}'


if __name__ == "__main__":
    Cli().run()
