import sys
import argparse


def main(args=None):
    """The main routine."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Turn on verbosity', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        print('Verbosity turned on')


if __name__ == "__main__":
    main()