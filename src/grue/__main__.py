"""Package entry point for Grue."""

import sys


class Memory:
    """Handles the private interpreter memory implementation."""

    def __init__(self, data: bytes) -> None:
        self.data = data

        self.dynamic = 0
        self.static: int = self.read_word(0x0E)
        self.high: int = self.read_word(0x04)

    def read_byte(self, address: int) -> int:
        """Reads a byte from the specified memory address."""

        return self.data[address]

    def read_word(self, address: int) -> int:
        """Reads a word (2 bytes) from the specified memory address."""

        return (self.data[address] << 8) | self.data[address + 1]


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
