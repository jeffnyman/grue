"""Configuration file for providing test fixtures."""

import os
import shutil
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture()
def zork1_z3(pytestconfig) -> Path:
    """Provides a Z-Machine version 3 Zork program."""

    tests_dir = pytestconfig.rootdir / "tests"
    fixtures_dir = tests_dir / "fixtures"
    return fixtures_dir / "zork1.z3"


@pytest.fixture()
def invalid_version_zcode_file(pytestconfig) -> Generator[Path, None, None]:
    """Provides a mock zcode file for testing."""

    original_file_path = pytestconfig.rootdir / "tests" / "fixtures" / "zork1.z3"
    temp_file_path = pytestconfig.rootdir / "tests" / "fixtures" / "mock.z3"

    shutil.copyfile(original_file_path, temp_file_path)

    with open(temp_file_path, "r+b") as file:
        file.seek(0)
        file.write(bytes([9]))

    yield temp_file_path

    os.remove(temp_file_path)
