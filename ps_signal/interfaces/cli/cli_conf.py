"""Module that contains various functions that initialize the cli interface.
"""
import argparse
import ps_signal as init
from . import strings as s


def initialize_args_parser() -> argparse.ArgumentParser:
    """Function that initialize the argparse. Adding all the arguments
    that should be available as well as configure them appropriately.
    Is using :mod:`.strings` for all the help strings for each argument.

    Returns:
        argparse.ArgumentParser: Returns an argparse object that can be
        invoked to run the initialized cli interface.
    """
    parser = argparse.ArgumentParser(description=s.welcome,
                                     prog="ps_signal")

    parser.add_argument("file", metavar="file", help=s.file)

    parser.add_argument("-i", metavar=("lower", "upper"), nargs=2,
                        required=False, type=int, help=s.interval)

    parser.add_argument("-fft", action="store_true", required=False,
                        help=s.fft)

    parser.add_argument("-lp", metavar="cutoff", required=False, type=float,
                        help=s.lowpass)

    parser.add_argument("-hp", metavar="cutoff", required=False, type=float,
                        help=s.highpass)

    parser.add_argument("-bs", metavar=("lower", "upper"), nargs=2,
                        required=False, type=float, help=s.bandstop)

    parser.add_argument("-bp", metavar=("lower", "upper"), nargs=2,
                        required=False, type=float, help=s.bandpass)

    parser.add_argument("-o", metavar="dir", required=False, type=int,
                        help=s.output)

    parser.add_argument("-t", metavar="title", required=False, type=str,
                        help=s.title)

    parser.add_argument('--version', action='version',
                        version=init.__version__, help=s.version)

    return parser


def parse_args() -> argparse.Namespace:
    """Function that executes the CLI interface and returns the name space aquired.

    Returns:
        argparse.Namespace: A list with all by the the user choosen arguments.
    """
    parser = initialize_args_parser()
    return parser.parse_args()
