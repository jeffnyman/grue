"""Package entry point for Grue."""

import sys
from enum import Enum

from grue.logging import log, setup_logging


FORMAT = Enum("Format", "UNKNOWN VARIABLE")


class Memory:
    """Handles the private interpreter memory implementation."""

    def __init__(self, data: bytes) -> None:
        self.data = data

        self.version: int = self.read_byte(0x00)
        self.release_number: int = self.read_word(0x2)
        self.serial_code: bytes = self.read_bytes(0x12, 6)

        self.dynamic: int = 0
        self.static: int = self.read_word(0x0E)
        self.high: int = self.read_word(0x04)
        self.routine_offset: int = self.read_word(0x28)
        self.strings_offset: int = self.read_word(0x2A)

        self.pc: int = 0

        self.format: FORMAT = FORMAT.UNKNOWN

        self._version_check()
        self._memory_checks()
        self._zcode_size_checks()
        self._read_starting_address()

    def details(self) -> None:
        """Display information of initial memory configuration."""

        log(f"zcode version: {self.version}")
        log(f"Release number: {self.release_number}")
        log(f"Serial code: {self.serial_code.decode('utf-8')}")
        log(f"Static memory: {hex(self.static)}")
        log(f"High memory: {hex(self.high)}")
        log(f"Routine offset: {self.routine_offset}")
        log(f"Strings offset: {self.strings_offset}")
        log(f"Starting address: {hex(self.pc)}")

    def read_instruction(self) -> None:
        """Reads an instruction at the location of the program counter."""

        log("\n----------------------------------------------")
        log(f"Reading instruction at {hex(self.pc)}")
        log("----------------------------------------------\n")

        # Reading a new instruction always takes place at the location
        # where the program counter is pointing.

        current_byte: int = self.pc

        # Grab the operation byte from the current byte.
        opcode_byte: int = self.read_byte(self.pc)
        log(f"Opcode byte: {opcode_byte} ({hex(opcode_byte)})")

        # Immediately move to the next byte. This will be necessary
        # to begin looking at operands.

        current_byte += 1

        # Determine the instruction form.

        if self.version >= 5 and opcode_byte == 0xBE:
            raise RuntimeError("IMP: Handle EXTENDED Format")
        elif opcode_byte & 0b11000000 == 0b11000000:
            self.format = FORMAT.VARIABLE
        elif opcode_byte & 0b10000000 == 0b10000000:
            raise RuntimeError("IMP: Handle SHORT Format")
        else:
            raise RuntimeError("IMP: Handle LONG Format")

        print(f"Format: {self.format.name}")

    def read_byte(self, address: int) -> int:
        """Reads a byte from the specified memory address."""

        return self.data[address]

    def read_bytes(self, address: int, length: int) -> bytes:
        """Reeads a series of bytes starting at a memory address."""

        return self.data[address : address + length]

    def read_word(self, address: int) -> int:
        """Reads a word (2 bytes) from the specified memory address."""

        return (self.data[address] << 8) | self.data[address + 1]

    def read_packed(self, address: int, is_routine: bool) -> int:
        """Reads a packed address from memory, accounting for offsets."""

        if self.version < 4:
            return 2 * address

        if self.version < 6:
            return 4 * address

        if self.version < 8 and is_routine:
            return 4 * address + (8 * self.routine_offset)

        if self.version < 8:
            return 4 * address + (8 * self.strings_offset)

        return 8 * address

    def _read_starting_address(self) -> None:
        """Read address where zcode execution begins."""

        if self.version != 6:
            self.pc = self.read_word(0x06)
        else:
            self.pc = self.read_packed(self.read_word(0x06), True)

    def _version_check(self) -> None:
        """Checks a valid zcode program range."""

        if self.version not in range(1, 9):
            raise RuntimeError(f"unsupported Z-Machine version of {self.version} found")

    def _memory_checks(self) -> None:
        """Checks for specific memory contraints related to the memory map."""

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

    def _zcode_size_checks(self) -> None:
        """Checks for contraints related to allowed zcode program size."""

        size_limits = {
            1: 128,
            2: 128,
            3: 128,
            4: 256,
            5: 256,
            6: 512,
            7: 512,
            8: 512,
            9: 512,
        }

        total_size: int = len(self.data)
        size_limit: int = size_limits[self.version]

        if total_size > size_limit * 1024:
            raise RuntimeError(
                f"program exceeds size limit of {size_limit}KB for version {self.version}"
            )


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

    setup_logging("log.txt")

    data = Loader.load(sys.argv[1])
    memory = Memory(data)
    memory.details()

    memory.read_instruction()

    return 0


if __name__ == "__main__":
    sys.exit(main())
