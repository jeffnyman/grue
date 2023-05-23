"""Configuration file for providing test fixtures."""

from pathlib import Path
import pytest

from grue.__main__ import Memory


@pytest.fixture()
def sample_zcode_file(tmp_path: Path) -> Path:
    """Create a sample zcode file for testing."""

    zcode_data = b"Sample Zcode Data"
    file_path = tmp_path / "sample.zcode"

    with open(file_path, "wb") as file:
        file.write(zcode_data)

    return file_path


@pytest.fixture()
def sample_memory() -> Memory:
    """Create a sample Memory instance for testing."""

    data = bytes([0x11, 0x22, 0x33, 0x44, 0x55])
    return Memory(data)
