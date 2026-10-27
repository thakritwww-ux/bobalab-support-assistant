class ServiceError(Exception):
    def __init__(self, code, message, status=503):
        self.code, self.message, self.status = code, message, status
        super().__init__(message)


class Conflict(ServiceError):
    def __init__(self):
        super().__init__(
            "version_conflict",
            "The prompt changed during editing. Retry against the current version.",
            409,
        )
