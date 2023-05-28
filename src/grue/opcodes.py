"""Module for holding opcode definitions."""

from dataclasses import dataclass


@dataclass
class Opcodes:
    """Represents data values to identify unique opcodes."""

    def __init__(self, name: str, versions: list, id: tuple) -> None:
        self.name = name
        self.versions = versions
        self.id = id

    def matches(self, version: int, byte: int, number: int) -> bool:
        result = version in self.versions and (byte, number) == self.id
        return result


opcodes = [
    Opcodes(name="call", versions=[1, 2, 3], id=(224, 0)),
    Opcodes(name="call_vs", versions=[5, 6, 7, 8], id=(224, 0)),
]
