"""Package entry point for Grue."""

import sys

from grue.loader import Loader
from grue.logging import setup_logging
from grue.memory import Memory


def main() -> int:
    """Entry point function for Grue."""

    print("GRUE Z-Machine Interpreter")

    setup_logging("log.txt")

    data = Loader.load(sys.argv[1])
    memory = Memory(data)
    memory.details()

    memory.read_instruction()

    return 0


if __name__ == "__main__":
    sys.exit(main())
