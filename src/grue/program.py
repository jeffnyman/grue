import os
import logging
from pathlib import Path


class UnableToAccessProgramError(Exception):
    """Raise for a zcode program file that cannot be opened or read from."""


class UnableToLocateProgramError(Exception):
    """Raise for a zcode program file that cannot be located."""


class Program:
    def __init__(self, program: str) -> None:
        self._program: str = program
        self.file: Path
        self.data: bytes = b""

        self._locate()
        self._read_data()

    def _read_data(self) -> None:
        try:
            self.data = self.file.read_bytes()
        except OSError:
            raise UnableToAccessProgramError(
                f"\nUnable to access the program: {self.file.name}"
                f"\nFile location: {self.file.parent}"
            )

    def _locate(self) -> None:
        paths = [
            Path.cwd(),
            Path.cwd() / "zcode",
            Path.home() / "zcode",
            Path(os.path.expandvars("$ZCODE_PATH")),
            Path(os.path.expandvars("$QUENDOR_PATH")),
        ]

        paths = [Path(path) for path in paths]

        for path in paths:
            logging.info(f"Checking: {Path(path).joinpath(self._program)}")

            file_path = path.joinpath(self._program)

            if file_path.is_file():
                self.file = file_path
                return

        checked_paths = "\n\t".join([a.as_posix() for a in paths])

        raise UnableToLocateProgramError(
            f"\nUnable to locate the program: {self._program}"
            f"\n\nChecked in:\n\t{checked_paths}"
        )
