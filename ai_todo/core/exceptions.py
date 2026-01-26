class TodoAIError(Exception):
    """Base exception for todo.ai errors."""

    pass


class TamperError(TodoAIError):
    """Raised when external modification is detected in TODO.md."""

    def __init__(self, message: str, expected_hash: str, actual_hash: str):
        self.expected_hash = expected_hash
        self.actual_hash = actual_hash
        super().__init__(message)
