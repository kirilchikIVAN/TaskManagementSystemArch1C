from exceptions.base import ServiceExceptionBase


class ObjectNotFoundError(ServiceExceptionBase):
    status_code: int = 404

    def __init__(
        self,
        field: str,
        value: str,
        object_name: str | None = None,
        status_message: str | None = None,
        error_message: str | None = None,
    ) -> None:
        if object_name:
            self.object_name = object_name
        if not status_message:
            status_message = f"{self.object_name} is not found"
        if error_message is None:
            error_message = f"{self.object_name} with {field}={value} is not found"
        super().__init__(
            status_code=self.status_code,
            status_message=status_message,
            error_message=error_message,
        )
