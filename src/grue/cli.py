import argparse

import grue.__version__

log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def process_arguments(args: list) -> dict:
    parser = argparse.ArgumentParser(
        prog="quendor",
        description="Execute a zcode program on the Z-Machine",
        epilog="Watch out for Grues!",
    )

    parser.add_argument(
        "--log",
        default="ERROR",
        const="ERROR",
        nargs="?",
        metavar="LEVEL",
        choices=log_levels,
        help="level of logging to display (default: %(default)s). Levels: "
        + ", ".join(log_levels),
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"Version: {grue.__version__}"
    )

    return vars(parser.parse_args(args))
