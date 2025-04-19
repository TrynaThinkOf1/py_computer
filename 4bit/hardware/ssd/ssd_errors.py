class StorageFullError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DirectoryAlreadyExistsError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DirectoryNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class FileAlreadyExistsError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class FileNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)