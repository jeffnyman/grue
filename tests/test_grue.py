"""Tests for Grue execution."""

from expects import be_a, contain, equal, expect
import pytest


def test_load_zcode_program(zork1_z3, monkeypatch, capsys) -> None:
    """Grue loads a zcode program as a sequence of bytes."""

    from grue.__main__ import main
    from grue.loader import Loader

    monkeypatch.setattr("sys.argv", ["grue", str(zork1_z3)])

    main()

    captured_output = capsys.readouterr().out

    expect(captured_output).to(contain("GRUE Z-Machine Interpreter"))
    expect(Loader.load(zork1_z3)).to(be_a(bytes))


def test_read_byte(zork1_z3_program) -> None:
    """Grue reads byte addresses from memory."""

    memory = zork1_z3_program

    expect(memory.read_byte(0)).to(equal(3))


def test_read_word(zork1_z3_program) -> None:
    """Grue reads word addresses from memory."""

    memory = zork1_z3_program

    expect(memory.read_word(0x0E)).to(equal(memory.static))
    expect(memory.read_word(0x04)).to(equal(memory.high))


def test_determine_zcode_version(zork1_z3_program) -> None:
    """Grue reads the zcode version from memory."""

    memory = zork1_z3_program

    expect(memory.version).to(equal(3))


def test_determine_zcode_release_number(zork1_z3_program) -> None:
    """Grue reads the zcode release number from memory."""

    memory = zork1_z3_program

    expect(memory.release_number).to(equal(88))


def test_determine_zcode_serial_code(zork1_z3_program) -> None:
    """Grue reads the zcode serial code from memory."""

    memory = zork1_z3_program

    expect(int(memory.serial_code.decode("utf-8"))).to(equal(840726))


def test_invalid_version_not_allowed(invalid_version_zcode_file) -> None:
    """Grue raises an an error for unsupported versions."""

    from grue.memory import Memory

    with open(invalid_version_zcode_file, "rb") as file:
        zcode_data = file.read()

    with pytest.raises(RuntimeError) as exc_info:
        Memory(zcode_data)

    expect(str(exc_info.value)).to(contain("unsupported Z-Machine version of 9 found"))


def test_determine_starting_address(zork1_z3_program) -> None:
    """Grue reads starting address for zcode execution (versions 1 to 5)."""

    memory = zork1_z3_program

    expect(hex(memory.pc)).to(equal(hex(0x4F05)))


def test_determine_starting_main_routine(zork1_z6) -> None:
    """Grue reads starting main routine for zcode execution (version 6)."""

    from grue.loader import Loader
    from grue.memory import Memory

    data = Loader.load(str(zork1_z6))

    memory = Memory(data)

    expect(hex(memory.pc)).to(equal(hex(0x7AA4)))


def test_get_the_first_instruction_operation_byte(zork1_z3_program) -> None:
    """Grue reads the operation byte from an instruction."""

    memory = zork1_z3_program
    memory.read_instruction()

    expect(hex(memory.read_byte(memory.pc))).to(equal(hex(0xE0)))
    expect(hex(memory.opcode_byte)).to(equal(hex(0xE0)))


def test_get_the_first_instruction_format(zork1_z3_program) -> None:
    """Grue reads the format of an instruction."""

    memory = zork1_z3_program
    memory.read_instruction()

    expect(memory.format.name).to(equal("VARIABLE"))


def test_report_unknown_instruction_format(zork1_z3_program) -> None:
    """Grue raises an error when the instruction format is unknown."""

    from grue.memory import FORMAT

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
    memory.read_instruction()

    expect(memory.operand_count.name).to(equal("VAR"))


def test_report_unknown_operand_count(zork1_z3_program) -> None:
    """Grue raises an error when the operand count is unknown."""

    from grue.memory import FORMAT, OP_COUNT

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
    memory.read_instruction()

    expect(memory.opcode_number).to(equal(0))


def test_get_the_first_instruction_operand_types(zork1_z3_program) -> None:
    """Grue determines the operand types of an instruction."""

    memory = zork1_z3_program
    memory.read_instruction()

    expect(len(memory.operand_types)).to(equal(3))
    expect(memory.operand_types[0].name).to(equal("Large"))
    expect(memory.operand_types[1].name).to(equal("Large"))
    expect(memory.operand_types[2].name).to(equal("Large"))
