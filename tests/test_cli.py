from expects import expect, contain

import pytest

from grue.__main__ import main


def test_grue_startup_banner(capsys, zork1_z3) -> None:
    """Provides a minimal banner on startup."""

    from grue import __version__

    main([str(zork1_z3)])

    captured = capsys.readouterr()
    result = captured.out

    banner_text = f"Grue Z-Machine Interpreter (Version: {__version__})"
    expect(result).to(contain(banner_text))


def test_no_program_provided(capsys) -> None:
    """Indicates when a program has not been provided."""

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    result = captured.err

    error_text = "the following arguments are required: program"
    expect(result).to(contain(error_text))


def test_handle_invalid_arguments(capsys, zork1_z3) -> None:
    """Indicates when an invalid argument is provided."""

    with pytest.raises(SystemExit):
        main([str(zork1_z3), "--invalid"])

    captured = capsys.readouterr()
    result = captured.err

    error_text = "unrecognized arguments: --invalid"
    expect(result).to(contain(error_text))


def test_unable_to_locate_program() -> None:
    """Raises an exception when a program can't be located."""

    from grue.program import UnableToLocateProgramError

    with pytest.raises(UnableToLocateProgramError) as exc_info:
        main(["program.z5"])

    error_text = "Unable to locate the program: program.z5"
    expect(str(exc_info.value)).to(contain(error_text))


def test_handle_invalid_log_level(capsys) -> None:
    """Indicates when an invalid log level is specified."""

    with pytest.raises(SystemExit):
        main(["--log", "LOTS"])

    captured = capsys.readouterr()
    result = captured.err

    error_text = "invalid choice: 'LOTS'"
    expect(result).to(contain(error_text))
