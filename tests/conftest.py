"""Configuration file for providing test fixtures."""

from pathlib import Path
import pytest


@pytest.fixture()
def zork1_z3(pytestconfig) -> Path:
    """Provides a Z-Machine version 3 Zork program."""

    tests_dir = pytestconfig.rootdir / "tests"
    fixtures_dir = tests_dir / "fixtures"
    return fixtures_dir / "zork1.z3"
