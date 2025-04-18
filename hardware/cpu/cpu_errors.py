class InvalidInstructionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidRegisterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)