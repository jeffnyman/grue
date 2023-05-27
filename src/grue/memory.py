"""Module for the interpreter memory."""

from enum import Enum

from grue.logging import log

FORMAT = Enum("Format", "UNKNOWN VARIABLE")
OP_COUNT = Enum("OpCount", "UNKNOWN VAR")
OP_TYPE = Enum("OpType", "UNKNOWN Variable Large Small")


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

        self.opcode_byte: int
        self.opcode_number: int
        self.format: FORMAT = FORMAT.UNKNOWN
        self.operand_count: OP_COUNT = OP_COUNT.UNKNOWN
        self.operand_types: list = []

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
        self.opcode_byte: int = self.read_byte(self.pc)
        log(f"Opcode byte: {self.opcode_byte} ({hex(self.opcode_byte)})")

        # Immediately move to the next byte. This will be necessary
        # to begin looking at operands.

        current_byte += 1

        self._determine_instruction_format()
        self._determine_operand_count()
        self._determine_opcode_number()

        # Need to determine the operand types.
        value = self.read_byte(current_byte)

        if self.format == FORMAT.VARIABLE:
            # First field
            if value & 0b11000000 == 0b11000000:
                print("First Field: Omitted")
            else:
                self.operand_types.append(self._type_from_bits(value >> 6))

            # Second field
            if value & 0b00110000 == 0b00110000:
                print("Second Field: Omitted")
            else:
                self.operand_types.append(self._type_from_bits((value & 0b00110000) >> 4))

            # Third field
            if value & 0b00001100 == 0b00001100:
                print("Third Field: Omitted")
            else:
                self.operand_types.append(self._type_from_bits((value & 0b00001100) >> 2))

            # Fourth field
            if value & 0b00000011 == 0b00000011:
                print("Fourth Field: Omitted")
            else:
                self.operand_types.append(self._type_from_bits(value & 0b00000011))

        print(f"Operand Types: {self.operand_types}")

    def read_byte(self, address: int) -> int:
        """Reads a byte from the specified memory address."""

        return self.data[address]

    def read_bytes(self, address: int, length: int) -> bytes:
        """Reads a series of bytes starting at a memory address."""

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

    def _determine_opcode_number(self) -> None:
        """Determine opcode number from format and operation byte."""

        if self.format == FORMAT.VARIABLE:
            self.opcode_number = self.opcode_byte & 0b00011111
            log(f"Opcode Number: {self.opcode_number} ({hex(self.opcode_number)})")

    def _determine_operand_count(self) -> None:
        """Determine operand count from the format and operation byte."""

        if self.format == FORMAT.VARIABLE:
            if self.opcode_byte & 0b00100000 == 0b00100000:
                self.operand_count = OP_COUNT.VAR
                log(f"Operand Count: {self.operand_count.name}")
            else:
                raise RuntimeError("IMP: Handle non-VAR operand count for VARIABLE.")
        else:
            raise RuntimeError("Operand Count is unknown.")

    def _determine_instruction_format(self) -> None:
        """Determine instruction format from opcode byte."""

        if self.version >= 5 and self.opcode_byte == 0xBE:
            raise RuntimeError("IMP: Handle EXTENDED Format")
        elif self.opcode_byte & 0b11000000 == 0b11000000:
            self.format = FORMAT.VARIABLE
        elif self.opcode_byte & 0b10000000 == 0b10000000:
            raise RuntimeError("IMP: Handle SHORT Format")
        else:
            raise RuntimeError("IMP: Handle LONG Format")

        if self.format.name == "UNKNOWN":
            raise RuntimeError("Instruction format is unknown.")
        else:
            log(f"Format: {self.format.name}")

    def _type_from_bits(self, value: int) -> OP_TYPE:
        """Determine operand type by binary digits."""

        if value == 0:
            return OP_TYPE.Large
        elif value == 1:
            return OP_TYPE.Small
        else:
            return OP_TYPE.Variable

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
