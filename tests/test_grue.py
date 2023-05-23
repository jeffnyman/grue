"""Tests for Grue execution."""

from expects import be_a, contain, equal, expect


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
