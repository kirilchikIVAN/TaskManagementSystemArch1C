from starlette import status


class ServiceExceptionBase(Exception):
    """
    Generic class to handle services API exceptions
    """

    status_code: int = status.HTTP_400_BAD_REQUEST

    status_message: str = "Error"
    error_message: str | None = None

    def __init__(
        self,
        status_code: int | None = None,
        status_message: str | None = None,
        error_message: str | None = None,
    ) -> None:
        if status_code is not None:
            self.status_code = status_code
        if status_message is not None:
            self.status_message = status_message
        if error_message is not None:
            self.error_message = error_message
        super().__init__()
