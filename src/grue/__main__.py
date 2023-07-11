import sys
from typing import Optional

from grue import __version__


def main(args: Optional[list] = None) -> int:
    print(f"\nGrue Z-Machine Interpreter (Version: {__version__})\n")

    if not args:
        args = sys.argv[1:]

    return 0


if __name__ == "__main__":
    sys.exit(main())
