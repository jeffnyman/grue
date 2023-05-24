"""Package entry point for Grue."""

import sys


class Memory:
    """Handles the private interpreter memory implementation."""

    def __init__(self, data: bytes) -> None:
        self.data = data

        self.version: int = self.read_byte(0x00)

        self.dynamic: int = 0
        self.static: int = self.read_word(0x0E)
        self.high: int = self.read_word(0x04)

        self._version_check()
        self._memory_checks()

    def details(self) -> None:
        print(f"zcode version: {self.version}")
        print(f"Static memory: {hex(self.static)}")
        print(f"High memory: {hex(self.high)}")

    def read_byte(self, address: int) -> int:
        """Reads a byte from the specified memory address."""

        return self.data[address]

    def read_word(self, address: int) -> int:
        """Reads a word (2 bytes) from the specified memory address."""

        return (self.data[address] << 8) | self.data[address + 1]

    def _version_check(self) -> None:
        if self.version not in range(1, 9):
            raise RuntimeError(f"unsupported Z-Machine version of {self.version} found")

    def _memory_checks(self) -> None:
        header_size: int = 64

        # There is a minimum size to a zcode program in that it must be able
        # to accommodate a 64 byte header.

        if len(self.data) < header_size:
            raise RuntimeError("dynamic memory is below required 64 bytes")

        # The specification indicates that dynamic memory must contain at
        # least 64 bytes to accommodate the header.

        if self.static < header_size:
            raise RuntimeError("static memory begins before byte 64")

        # The specification indicates that the total of dynamic plus static
        # memory must not exceed 64K minus 2 bytes.

        dynamic_size: int = self.static - 1 - self.dynamic + 1

        if (dynamic_size + self.static) > 65534:
            raise RuntimeError("memory exceeds addressable memory space")


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
    memory = Memory(data)
    memory.details()

    return 0


if __name__ == "__main__":
    sys.exit(main())
