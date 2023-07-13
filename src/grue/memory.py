import logging


class Memory:
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data
        self.version: int = self.read_byte(0x00)
        self.pc: int = 0

        self._read_starting_location()

    def details(self) -> None:
        logging.info(f"zcode version: {self.version}")
        logging.info(f"Starting location: {hex(self.pc)}")

    def read_byte(self, offset: int) -> int:
        return self.data[offset]

    def read_word(self, offset: int) -> int:
        return (self.data[offset] << 8) | self.data[offset + 1]

    def _read_starting_location(self) -> None:
        if self.version != 6:
            self.pc = self.read_word(0x06)
        else:
            raise Exception("IMP: Read v6 starting location")
