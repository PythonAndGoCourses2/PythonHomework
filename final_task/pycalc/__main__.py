"""
Pure-python implementation of a command-line calculator.

Receives mathematical expression string as an argument
and prints evaluated result.
"""

from pycalc.cli import Cli


def main():
    """Pure-python implementation of a command-line calculator."""

    Cli().run()


if __name__ == "__main__":
    main()
