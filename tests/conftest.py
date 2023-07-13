from pathlib import Path

import pytest


@pytest.fixture()
def zork1_z3(pytestconfig) -> Path:
    return pytestconfig.rootdir / "tests" / "fixtures" / "zork1.z3"


@pytest.fixture()
def zork1_z3_data(zork1_z3: Path) -> bytes:
    return Path(zork1_z3).read_bytes()
