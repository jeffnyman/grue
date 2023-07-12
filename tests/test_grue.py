def test_package_version() -> None:
    """Current version is exposed on the package."""

    from grue import __version__

    assert __version__ == "0.1.0"


def test_grue_startup_banner(capsys) -> None:
    """Provides a minimal banner on startup."""

    from grue.__main__ import main
    from grue import __version__

    main()

    captured = capsys.readouterr()
    result = captured.out

    assert f"Grue Z-Machine Interpreter (Version: {__version__})" in result
