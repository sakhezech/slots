import argparse
import sys
from typing import NoReturn, Sequence

from . import Slots
from .__version__ import __version__
from .column import Column
from .predefined_charsets import _charsets


def print_and_exit(*values, exit_code: int = 1) -> NoReturn:
    print(*values, file=sys.stderr)
    sys.exit(exit_code)


def make_user_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser('slots')
    rand_rig_group = parser.add_mutually_exclusive_group()

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
    )
    rand_rig_group.add_argument(
        '--seed',
        default=None,
        help='random seed (defaults to None)',
    )
    rand_rig_group.add_argument(
        '-r',
        '--rig',
        metavar='VAL',
        nargs='+',
        help="""
        list of roll values, number of values must match number of columns
        """,
    )
    parser.add_argument(
        '-T',
        '--period',
        type=float,
        default=0.05,
        help='interval between frames in seconds (defaults to 0.05)',
    )

    return parser


def make_cli_parser() -> argparse.ArgumentParser:
    parser = make_user_parser()

    parser.add_argument(
        '-c',
        '--chars',
        default='small_nums',
        choices=_charsets.keys(),
        help='charset (defaults to small_nums)',
    )
    parser.add_argument(
        'columns',
        type=int,
        help='number of columns',
    )

    return parser


def cli(argv: Sequence[str] | None = None) -> None:
    parser = make_cli_parser()
    args = parser.parse_args(argv)
    if args.columns <= 0:
        print_and_exit(
            f'number of columns must be greater than 0: {args.columns}'
        )
    chars = [(str(value), char) for value, char in _charsets[args.chars]]
    slots = Slots([Column(chars) for _ in range(args.columns)])
    run_slots(slots, args)


def user_cli(slots: Slots, argv: Sequence[str] | None = None) -> None:
    parser = make_user_parser()
    args = parser.parse_args(argv)
    run_slots(slots, args)


def run_slots(slots: Slots, args) -> None:
    if args.period <= 0:
        print_and_exit(f'period must be greater than 0: {args.period}')
    if args.rig:
        slots.rig_values(args.rig)
    else:
        slots.randomize(args.seed)
    slots.spin(args.period)


if __name__ == '__main__':
    cli(None)
