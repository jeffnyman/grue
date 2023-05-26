"""Zcode loader module for Grue."""


class Loader:
    """Handles loading a file from the command line and reading it as binary."""

    @staticmethod
    def load(program_file: str) -> bytes:
        """Load the specified program file and return its content as bytes."""

        zcode_file = open(program_file, "rb")
        return zcode_file.read()
