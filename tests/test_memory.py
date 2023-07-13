from expects import expect, equal

from grue.memory import Memory


def test_read_byte(zork1_z3_data) -> None:
    """Reads a byte address from memory."""

    memory = Memory(zork1_z3_data)

    expect(memory.read_byte(0)).to(equal(3))


def test_read_word(zork1_z3_data) -> None:
    """Reads a two-byte address from memory."""

    memory = Memory(zork1_z3_data)

    expect(memory.read_word(0x06)).to(equal(0x4F05))


def test_read_zcode_version(zork1_z3_data) -> None:
    """Reads the zcode version from memory."""

    memory = Memory(zork1_z3_data)

    expect(memory.version).to(equal(3))


def test_read_starting_location(zork1_z3_data) -> None:
    """Reads starting address for zcode execution (version 3)."""

    memory = Memory(zork1_z3_data)

    expect(memory.pc).to(equal(0x4F05))
