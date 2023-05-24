"""Tests for Grue execution."""

from expects import be_a, contain, equal, expect
import pytest


def test_load_zcode_program(zork1_z3, monkeypatch, capsys) -> None:
    """Grue loads a zcode program as a sequence of bytes."""

    from grue.__main__ import Loader, main

    monkeypatch.setattr("sys.argv", ["grue", str(zork1_z3)])

    main()

    captured_output = capsys.readouterr().out

    expect(captured_output).to(contain("GRUE Z-Machine Interpreter"))
    expect(Loader.load(zork1_z3)).to(be_a(bytes))


def test_read_byte(zork1_z3) -> None:
    """Grue reads byte addresses from memory."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z3))

    memory = Memory(data)

    expect(memory.read_byte(0)).to(equal(3))


def test_read_word(zork1_z3) -> None:
    """Grue reads word addresses from memory."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z3))

    memory = Memory(data)

    expect(memory.read_word(0x0E)).to(equal(memory.static))
    expect(memory.read_word(0x04)).to(equal(memory.high))


def test_determine_zcode_version(zork1_z3) -> None:
    """Grue reads the zcode version from memory."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z3))

    memory = Memory(data)

    expect(memory.version).to(equal(3))


def test_determine_zcode_release_number(zork1_z3) -> None:
    """Grue reads the zcode release number from memory."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z3))

    memory = Memory(data)

    expect(memory.release_number).to(equal(88))


def test_determine_zcode_serial_code(zork1_z3) -> None:
    """Grue reads the zcode serial code from memory."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z3))

    memory = Memory(data)

    expect(int(memory.serial_code.decode("utf-8"))).to(equal(840726))


def test_invalid_version_not_allowed(invalid_version_zcode_file) -> None:
    """Grue raises an an error for unsupported versions."""

    from grue.__main__ import Memory

    with open(invalid_version_zcode_file, "rb") as file:
        zcode_data = file.read()

    with pytest.raises(RuntimeError) as exc_info:
        Memory(zcode_data)

    expect(str(exc_info.value)).to(contain("unsupported Z-Machine version of 9 found"))


def test_determine_starting_address(zork1_z3) -> None:
    """Grue reads starting address for zcode execution (versions 1 to 5)."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z3))

    memory = Memory(data)

    expect(hex(memory.pc)).to(equal(hex(0x4F05)))


def test_determine_starting_main_routine(zork1_z6) -> None:
    """Grue reads starting main routine for zcode execution (version 6)."""

    from grue.__main__ import Loader, Memory

    data = Loader.load(str(zork1_z6))

    memory = Memory(data)

    expect(hex(memory.pc)).to(equal(hex(0x7AA4)))
