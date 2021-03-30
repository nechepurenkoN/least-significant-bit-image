class EncoderTooLongMessageException(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidPixelChannelException(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)
