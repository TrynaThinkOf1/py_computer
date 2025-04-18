class MemoryNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class OutOfMemoryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)