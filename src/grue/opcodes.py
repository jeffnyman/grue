"""Module for holding opcode definitions."""

from dataclasses import dataclass


@dataclass
class Opcodes:
    """Represents data values to identify unique opcodes."""

    def __init__(
        self, name: str, versions: list, value: tuple, store: bool = False
    ) -> None:
        self.name = name
        self.versions = versions
        self.value = value
        self.store = store

    def matches(self, version: int, byte: int, number: int) -> bool:
        """Checks for matching Opcode data class based on parameters."""

        return version in self.versions and (byte, number) == self.value


opcodes = [
    Opcodes(name="call", versions=[1, 2, 3], value=(224, 0), store=True),
    Opcodes(name="call_vs", versions=[5, 6, 7, 8], value=(224, 0), store=True),
]
