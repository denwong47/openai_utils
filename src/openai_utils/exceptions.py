class OpenAIUtilsException(Exception):
    def __bool__(self):
        return False
    __nonzero__ = __bool__

class OpenAIRequestFailed(RuntimeError, OpenAIUtilsException):
    pass

class LocalFileSystemError(OSError, OpenAIUtilsException):
    pass