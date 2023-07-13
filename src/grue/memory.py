class Memory:
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data

    def read_byte(self, offset: int) -> int:
        return self.data[offset]
