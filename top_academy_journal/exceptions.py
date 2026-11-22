class JournalException(Exception):
    ...

class ClientException(Exception):
    ...

class InvalidCredentials(JournalException):
    def __init__(self):
       super().__init__("Invalid login or password")

class ArgsValidationError(ClientException, ValueError):
    pass
