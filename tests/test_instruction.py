"""Tests for reading instruction details."""

from expects import equal, expect
import pytest


def test_get_the_first_instruction_operation_byte(zork1_z3_program) -> None:
    """Grue reads the operation byte from an instruction."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(hex(memory.read_byte(memory.pc))).to(equal(hex(0xE0)))
    expect(hex(instruction.opcode_byte)).to(equal(hex(0xE0)))


def test_get_the_first_instruction_format(zork1_z3_program) -> None:
    """Grue reads the format of an instruction."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(instruction.format.name).to(equal("VARIABLE"))


def test_report_unknown_instruction_format(zork1_z3_program) -> None:
    """Grue raises an error when the instruction format is unknown."""

    from grue.instruction import FORMAT

    memory = zork1_z3_program

    def fake_read_instruction(self) -> None:
        self.format = FORMAT.UNKNOWN
        raise RuntimeError("Instruction format is unknown.")

    memory.read_instruction = fake_read_instruction.__get__(memory)

    with pytest.raises(RuntimeError) as exc_info:
        memory.read_instruction()

    expect(str(exc_info.value)).to(equal("Instruction format is unknown."))


def test_get_the_first_instruction_operand_count(zork1_z3_program) -> None:
    """Grue reads the operand count of an instruction."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(instruction.operand_count.name).to(equal("VAR"))


def test_report_unknown_operand_count(zork1_z3_program) -> None:
    """Grue raises an error when the operand count is unknown."""

    from grue.instruction import FORMAT, OP_COUNT

    memory = zork1_z3_program

    def fake_read_instruction(self) -> None:
        self.format = FORMAT.VARIABLE
        self.operand_count = OP_COUNT.UNKNOWN
        raise RuntimeError("Operand Count is unknown.")

    memory.read_instruction = fake_read_instruction.__get__(memory)

    with pytest.raises(RuntimeError) as exc_info:
        memory.read_instruction()

    expect(str(exc_info.value)).to(equal("Operand Count is unknown."))


def test_get_the_first_instruction_opcode_number(zork1_z3_program) -> None:
    """Grue determines the opcode number of an instruction."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(instruction.opcode_number).to(equal(0))


def test_get_the_first_instruction_operand_types(zork1_z3_program) -> None:
    """Grue determines the operand types of an instruction."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(len(instruction.operand_types)).to(equal(3))
    expect(instruction.operand_types[0].name).to(equal("Large"))
    expect(instruction.operand_types[1].name).to(equal("Large"))
    expect(instruction.operand_types[2].name).to(equal("Large"))


def test_get_the_first_instruction_operand_values(zork1_z3_program) -> None:
    """Grue determines the operand values of an instruction."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(len(instruction.operand_values)).to(equal(3))
    expect(hex(instruction.operand_values[0])).to(equal(hex(0x2A39)))
    expect(hex(instruction.operand_values[1])).to(equal(hex(0x8010)))
    expect(hex(instruction.operand_values[2])).to(equal(hex(0xFFFF)))


def test_get_the_first_instruction_opcode_name_z3(zork1_z3_program) -> None:
    """Grue estabishes the opcode name of an instruction, version 3."""

    memory = zork1_z3_program
    instruction = memory.read_instruction()

    expect(instruction.opcode_name).to(equal("call"))


def test_get_the_first_instruction_opcode_name_z5(zork1_z5_program) -> None:
    """Grue estabishes the opcode name of an instruction, version 5."""

    memory = zork1_z5_program
    instruction = memory.read_instruction()

    expect(instruction.opcode_name).to(equal("call_vs"))
