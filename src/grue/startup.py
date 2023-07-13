import sys
import logging
from typing import Optional

from grue import __version__
from grue.cli import process_arguments
from grue.program import Program
from grue.memory import Memory


def main(args: Optional[list] = None) -> int:
    print(f"\nGrue Z-Machine Interpreter (Version: {__version__})\n")

    check_python_version()

    if not args:
        args = sys.argv[1:]

    cli = process_arguments(args)
    setup_logging(cli["log"])
    display_arguments(cli)
    setup_grue(cli)

    return 0


def setup_grue(cli: dict) -> None:
    program = Program(cli["program"])
    logging.info(program.file.name)

    memory = Memory(program.data)
    memory.details()


def check_python_version() -> None:
    python_version = (
        f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
    )

    if sys.version_info < (3, 8, 2):
        sys.stderr.write("\nGrue requires Python 3.8.2 or later.\n")
        sys.stderr.write(f"Your current version is {python_version}\n\n")
        sys.exit(1)


def setup_logging(log_level: str) -> None:
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )


def display_arguments(args: dict) -> None:
    logging.debug(f"Argument count: {'':>4}" + str(len(args)))

    for i, arg in enumerate(args):
        logging.debug(f"Argument {i}: {'':>8}" + arg)

    logging.debug(f"Parsed arguments: {'':>2}" + f"{args}")
