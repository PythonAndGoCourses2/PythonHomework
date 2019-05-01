import sys
import argparse


def main(args=None):
    """The main routine."""
    stringToParse = parse_console()
    print(stringToParse)


def parse_console():
    """Parse args from console and give it to main"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    return parser.parse_args().EXPRESSION
    

if __name__ == "__main__":
    main()