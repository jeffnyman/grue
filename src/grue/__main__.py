import sys

from grue import __version__


def main() -> int:
    print(f"\nGrue Z-Machine Interpreter (Version: {__version__})\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
