import argparse

import grue.__version__


def process_arguments(args: list) -> None:
    parser = argparse.ArgumentParser(
        prog="quendor",
        description="Execute a zcode program on the Z-Machine",
        epilog="Watch out for Grues!",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"Version: {grue.__version__}"
    )

    parser.parse_args(args)
