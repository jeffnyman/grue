"""Module to represent a zcode instruction."""

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grue.memory import Memory

from grue.logging import log
from grue.opcodes import opcodes


FORMAT = Enum("Format", "UNKNOWN EXTENDED VARIABLE SHORT LONG")
OP_COUNT = Enum("OpCount", "UNKNOWN VAR")
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
        self._determine_operand_count()
        self._determine_opcode_number()
        self._determine_opcode_name()

        # Have to move to the next byte. This is necessary to begin
        # looking at operands.

        self.current_byte += 1

        self._determine_operand_types()

        # Have to move to the next byte after getting operand types.
        # This may differ for non-variable formats.

        self.current_byte += 1

        self._determine_operand_values()

    def _determine_operand_values(self) -> None:
        """Read operand value based on operand type."""

        for operand_type in self.operand_types:
            if operand_type == OP_TYPE.Large:
                self.operand_values.append(self.memory.read_word(self.current_byte))
                self.current_byte += 2
            if operand_type == OP_TYPE.Small:
                raise RuntimeError("IMP: Type amall operand value.")
            if operand_type == OP_TYPE.Variable:
                raise RuntimeError("IMP: Type variable operand value.")

    def _determine_operand_types(self) -> None:
        """Determine operand type from the byte being read."""

        value = self.memory.read_byte(self.current_byte)

        if self.format == FORMAT.VARIABLE:
            fields = [(6, 0b11000000), (4, 0b00110000), (2, 0b00001100), (0, 0b00000011)]

            for index, (bits, mask) in enumerate(fields):
                if value & mask == mask:
                    log(f"Field {index + 1}: Omitted")
                    return
                else:
                    self.operand_types.append(
                        self._type_from_bits((value >> bits) & 0b11)
                    )

    def _determine_opcode_name(self) -> None:
        """Determine mnemonic for opcode."""

        version = self.memory.version
        byte = self.opcode_byte
        number = self.opcode_number

        for opcode in opcodes:
            if opcode.matches(version=version, byte=byte, number=number):
                self.opcode_name = opcode.name

        return None

    def _determine_opcode_number(self) -> None:
        """Determine opcode number from format and operation byte."""

        if self.format == FORMAT.VARIABLE:
            self.opcode_number = self.opcode_byte & 0b00011111

    def _determine_operand_count(self) -> None:
        """Determine operand count from the format and operation byte."""

        if self.format == FORMAT.VARIABLE:
            if self.opcode_byte & 0b00100000 == 0b00100000:
                self.operand_count = OP_COUNT.VAR
            else:
                raise RuntimeError("IMP: Handle non-VAR operand count for VARIABLE.")
        else:
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
        elif value == 1:
            return OP_TYPE.Small
        else:
            return OP_TYPE.Variable
