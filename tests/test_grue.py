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
