"""Tests for Grue execution."""

from expects import be_a, contain, equal, expect


def test_load_zcode_program(sample_zcode_file, monkeypatch, capsys) -> None:
    """Grue loads a zcode program as a sequence of bytes."""

    from grue.__main__ import Loader, main

    monkeypatch.setattr("sys.argv", ["program.z3", str(sample_zcode_file)])

    main()

    captured_output = capsys.readouterr().out

    expect(captured_output).to(contain("GRUE Z-Machine Interpreter"))
    expect(Loader.load(sample_zcode_file)).to(be_a(bytes))


def test_read_byte(sample_memory, monkeypatch) -> None:
    """Grue reads byte addresses from memory."""

    monkeypatch.setattr(sample_memory, "data", bytes([0x11, 0x22, 0x33]))

    expect(sample_memory.read_byte(0)).to(equal(0x11))
    expect(sample_memory.read_byte(1)).to(equal(0x22))
    expect(sample_memory.read_byte(2)).to(equal(0x33))


def test_read_word(sample_memory, monkeypatch) -> None:
    """Grue reads word addresses from memory."""

    monkeypatch.setattr(sample_memory, "data", bytes([0x11, 0x22, 0x33, 0x44, 0x55]))

    expect(sample_memory.read_word(0)).to(equal(0x1122))
    expect(sample_memory.read_word(1)).to(equal(0x2233))
    expect(sample_memory.read_word(2)).to(equal(0x3344))
    expect(sample_memory.read_word(3)).to(equal(0x4455))
