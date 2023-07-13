class Memory:
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data
        self.version: int = self.read_byte(0x00)

    def read_byte(self, offset: int) -> int:
        return self.data[offset]
