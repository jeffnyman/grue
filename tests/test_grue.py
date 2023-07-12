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

    main()

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
