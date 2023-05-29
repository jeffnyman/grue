"""Module to represent a zcode instruction."""

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grue.memory import Memory

from grue.logging import log
from grue.opcodes import opcodes


FORMAT = Enum("Format", "UNKNOWN EXTENDED VARIABLE SHORT LONG")
OP_COUNT = Enum("OpCount", "UNKNOWN OP0 OP1 OP2 VAR")
OP_TYPE = Enum("OpType", "UNKNOWN Variable Large Small")


class Instruction:
    """Stores the information related to an instruction."""

    def __init__(self, memory: "Memory") -> None:
        self.memory: "Memory" = memory

        self.current_byte: int

        self.opcode_byte: int
        self.opcode_name: str
        self.opcode_number: int
        self.format: FORMAT = FORMAT.UNKNOWN
        self.operand_count: OP_COUNT = OP_COUNT.UNKNOWN
        self.operand_types: list = []
        self.operand_values: list = []

    def details(self) -> None:
        """Display information of instruction parts."""

        log(f"Opcode Byte: {self.opcode_byte} ({hex(self.opcode_byte)})")
        log(f"Opocde Name: {self.opcode_name}")
        log(f"Format: {self.format.name}")
        log(f"Operand Count: {self.operand_count.name}")
        log(f"Opcode Number: {self.opcode_number} ({hex(self.opcode_number)})")
        log(f"Operand Types: {self.operand_types}")

        values = [hex(num)[2:].rjust(4, "0") for num in self.operand_values]
        log(f"Operand Values: {values}")

    def decode(self) -> None:
        """Determine all details of an instruction."""

        log("\n----------------------------------------------")
        log(f"Reading instruction at {hex(self.memory.pc)}")
        log("----------------------------------------------\n")

        # Reading a new instruction always takes place at the location
        # where the program counter is pointing.

        self.current_byte = self.memory.pc

        # Grab the operation byte from the current byte.
        self.opcode_byte = self.memory.read_byte(self.memory.pc)

        self._determine_format()

        # With the format known, it's possible to get the opcode number.
        # This number will be part of the current byte unless it's the
        # case that the opcode byte is 190. In that case, the opcode
        # number will be in the second byte. Either way, the current
        # byte can be moved forward.

        self.current_byte += 1

        # Now we read the opcode number. The opcode byte determines
        # the opcode number, so it's okay that the current byte has been
        # moved forward since the method below does not rely on it.

        self._determine_opcode_number()

        # If we're dealing with opcode byte 190, then the above attempt
        # to get the opcode number was effectively useless. Instead we
        # we have to read the opcode number from the current byte, which
        # has been moved to the second byte, per above. We then have to
        # move the current byte forward yet again.

        if self.memory.version >= 5 and self.opcode_byte == 0xBE:
            self.opcode_number = self.memory.read_byte(self.current_byte)
            self.current_byte += 1

        self._determine_opcode_name()

        self._determine_operand_count()

        if self.operand_count != OP_COUNT.OP0:
            if self.format in [FORMAT.VARIABLE, FORMAT.EXTENDED]:
                self._determine_operand_types()

                # It's necessary to move to the next next byte after getting
                # the operand types in these formats. This is not needed for
                # the other formats.
                self.current_byte += 1

                # There is a special circumstance of "double-variable" opcodes.
                # In this case, another set of operands needs to be read in and
                # then the current byte has to be incremented past those.
                if self.opcode_name in ["call_vs2", "call_vn2"]:
                    self._determine_operand_types()
                    self.current_byte += 1
            else:
                self._determine_operand_types()

        self._determine_operand_values()

    def _determine_operand_values(self) -> None:
        """Read operand value based on operand type."""

        for operand_type in self.operand_types:
            if operand_type == OP_TYPE.Large:
                self.operand_values.append(self.memory.read_word(self.current_byte))
                self.current_byte += 2

            if operand_type in [OP_TYPE.Small, OP_TYPE.Variable]:
                self.operand_values.append(self.memory.read_byte(self.current_byte))
                self.current_byte += 1

    def _determine_operand_types(self) -> None:
        """Determine operand type from the byte being read."""

        value = self.memory.read_byte(self.current_byte)

        if self.format == FORMAT.SHORT:
            if self.opcode_byte & 0b00100000 == 0b00100000:
                self.operand_types = [OP_TYPE.Variable]
            elif self.opcode_byte & 0b00010000 == 0b00010000:
                self.operand_types = [OP_TYPE.Small]
            elif self.opcode_byte & 0b00000000 == 0b00000000:
                self.operand_types = [OP_TYPE.Large]

        if self.format == FORMAT.LONG:
            # Check first operand
            if self.opcode_byte & 0b01000000 == 0b01000000:
                self.operand_types.append(OP_TYPE.Variable)
            else:
                self.operand_types.append(OP_TYPE.Small)

            # Check second operand
            if self.opcode_byte & 0b00100000 == 0b00100000:
                self.operand_types.append(OP_TYPE.Variable)
            else:
                self.operand_types.append(OP_TYPE.Small)

        if self.format in [FORMAT.VARIABLE, FORMAT.EXTENDED]:
            # First field
            if value & 0b11000000 == 0b11000000:
                return
            else:
                self.operand_types.append(self._type_from_bits(value >> 6))

            # Second field
            if value & 0b00110000 == 0b00110000:
                return
            else:
                self.operand_types.append(self._type_from_bits((value & 0b00110000) >> 4))

            # Third field
            if value & 0b00001100 == 0b00001100:
                return
            else:
                self.operand_types.append(self._type_from_bits((value & 0b00001100) >> 2))

            # Fourth field
            if value & 0b00000011 == 0b00000011:
                return
            else:
                self.operand_types.append(self._type_from_bits(value & 0b00000011))

    def _determine_opcode_name(self) -> None:
        """Determine mnemonic for opcode."""

        version = self.memory.version
        byte = self.opcode_byte
        number = self.opcode_number

        for opcode in opcodes:
            if opcode.matches(version=version, byte=byte, number=number):
                self.opcode_name = opcode.name

    def _determine_opcode_number(self) -> None:
        """Determine opcode number from format and operation byte."""

        if self.format in [FORMAT.LONG, FORMAT.VARIABLE]:
            self.opcode_number = self.opcode_byte & 0b00011111

        if self.format in [FORMAT.SHORT]:
            self.opcode_number = self.opcode_byte & 0b00001111

    def _determine_operand_count(self) -> None:
        """Determine operand count from the format and operation byte."""

        if self.format == FORMAT.SHORT:
            if self.opcode_byte & 0b00110000 == 0b00110000:
                self.operand_count = OP_COUNT.OP0
            else:
                self.operand_count = OP_COUNT.OP1

        if self.format == FORMAT.LONG:
            self.operand_count = OP_COUNT.OP2

        if self.format == FORMAT.VARIABLE:
            if self.opcode_byte & 0b00100000 == 0b00100000:
                self.operand_count = OP_COUNT.VAR
            else:
                self.operand_count = OP_COUNT.OP2

        if self.format == FORMAT.EXTENDED:
            self.operand_count = OP_COUNT.VAR

        if self.operand_count.name == "UNKNOWN":
            raise RuntimeError("Operand Count is unknown.")

    def _determine_format(self) -> None:
        """Determine instruction format from opcode byte."""

        if self.memory.version >= 5 and self.opcode_byte == 0xBE:
            self.format = FORMAT.EXTENDED
        elif self.opcode_byte & 0b11000000 == 0b11000000:
            self.format = FORMAT.VARIABLE
        elif self.opcode_byte & 0b10000000 == 0b10000000:
            self.format = FORMAT.SHORT
        else:
            self.format = FORMAT.LONG

        if self.format.name == "UNKNOWN":
            raise RuntimeError("Instruction format is unknown.")

    def _type_from_bits(self, value: int) -> OP_TYPE:
        """Determine operand type by binary digits."""

        if value == 0:
            return OP_TYPE.Large

        if value == 1:
            return OP_TYPE.Small

        return OP_TYPE.Variable
