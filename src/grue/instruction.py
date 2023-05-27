"""Module to represent a zcode instruction."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grue.memory import Memory


class Instruction:
    """Stores the information related to an instruction."""

    def __init__(self, memory: "Memory") -> None:
        self.memory: "Memory" = memory

    def decode(self) -> None:
        """Determine all details of an instruction."""
