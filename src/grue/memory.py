import logging


class Memory:
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data
        self.version: int = self.read_byte(0x00)

    def details(self) -> None:
        logging.info(f"zcode version: {self.version}")

    def read_byte(self, offset: int) -> int:
        return self.data[offset]
