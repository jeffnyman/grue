import pytest
from expects import expect, equal, contain


def test_package_version() -> None:
    """Current version is exposed on the package."""

    from grue import __version__

    expect(__version__).to(equal("0.1.0"))


def test_grue_startup_banner(capsys) -> None:
    """Provides a minimal banner on startup."""

    from grue.__main__ import main
    from grue import __version__

    main(["zork1.z3"])

    captured = capsys.readouterr()
    result = captured.out

    banner_text = f"Grue Z-Machine Interpreter (Version: {__version__})"
    expect(result).to(contain(banner_text))


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


def test_handle_invalid_log_level(capsys) -> None:
    """Indicates when an invalid log level is specified."""

    from grue.__main__ import main

    with pytest.raises(SystemExit):
        main(["--log", "LOTS"])

    captured = capsys.readouterr()
    result = captured.err

    error_text = "invalid choice: 'LOTS'"
    expect(result).to(contain(error_text))


def test_generate_logs(caplog) -> None:
    """Displays logs based on log levels."""

    import logging
    from grue.startup import setup_logging, display_arguments

    with caplog.at_level(logging.DEBUG):
        setup_logging("DEBUG")
        display_arguments({"log": "DEBUG"})

    expect(caplog.text).to(contain("Argument count", "Parsed arguments"))


def test_no_program_provided(capsys) -> None:
    """Indicates when a program has not been provided."""

    from grue.__main__ import main

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    result = captured.err

    error_text = "the following arguments are required: program"
    expect(result).to(contain(error_text))
