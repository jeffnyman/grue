import pytest
from expects import expect, equal, contain


def test_package_version() -> None:
    """Current version is exposed on the package."""

    from grue import __version__

    expect(__version__).to(equal("0.1.0"))


def test_bad_python_version(monkeypatch, capsys) -> None:
    """Checks if Python version requirement is met."""

    import sys
    from grue.startup import check_python_version

    monkeypatch.setattr(sys, "version_info", (3, 7, 9))

    with pytest.raises(SystemExit):
        check_python_version()

    captured = capsys.readouterr()
    result = captured.err

    error_text = "Grue requires Python 3.8.2 or later."
    expect(result).to(contain(error_text))


def test_grue_version_display(capsys) -> None:
    """Reports its version."""

    from grue.cli import process_arguments

    with pytest.raises(SystemExit):
        process_arguments(["-v"])

    captured = capsys.readouterr()
    result = captured.out

    verison_text = "Version: 0.1.0"
    expect(result).to(contain(verison_text))


def test_generate_logs(caplog) -> None:
    """Displays logs based on log levels."""

    import logging
    from grue.startup import setup_logging, display_arguments

    with caplog.at_level(logging.DEBUG):
        setup_logging("DEBUG")
        display_arguments({"log": "DEBUG"})

    expect(caplog.text).to(contain("Argument count", "Parsed arguments"))


def test_unable_to_access_program(tmp_path, zork1_z3) -> None:
    """Raises an eception when a program can't be accessed."""

    import shutil
    from grue.program import Program, UnableToAccessProgramError

    program = Program(zork1_z3)

    inaccessible = tmp_path / "inaccessible"
    program.file = inaccessible

    inaccessible.mkdir()

    error_text = f"Unable to access the program: {inaccessible.name}"

    with pytest.raises(UnableToAccessProgramError, match=error_text):
        program._read_data()

    shutil.rmtree(inaccessible)
