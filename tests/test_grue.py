"""Tests for Grue execution."""

from expects import be_a, contain, expect


def test_load_zcode_program(sample_zcode_file, monkeypatch, capsys) -> None:
    """Grue loads a zcode program as a sequence of bytes."""

    from grue.__main__ import Loader, main

    monkeypatch.setattr("sys.argv", ["program.z3", str(sample_zcode_file)])

    main()

    captured_output = capsys.readouterr().out

    expect(captured_output).to(contain("GRUE Z-Machine Interpreter"))
    expect(Loader.load(sample_zcode_file)).to(be_a(bytes))
