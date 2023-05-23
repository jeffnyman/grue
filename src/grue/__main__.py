"""Package entry point for Grue."""

import sys


class Memory:
    """Handles the private interpreter memory implementation."""

    def __init__(self, data: bytes) -> None:
        self.data = data


class Loader:
    """Handles loading a file from the command line and reading it as binary."""

    @staticmethod
    def load(program_file: str) -> bytes:
        """Load the specified program file and return its content as bytes."""

        zcode_file = open(program_file, "rb")
        return zcode_file.read()


def main() -> int:
    """Entry point function for Grue."""

    print("GRUE Z-Machine Interpreter")

    data = Loader.load(sys.argv[1])
    Memory(data)

    return 0


if __name__ == "__main__":
    main()
