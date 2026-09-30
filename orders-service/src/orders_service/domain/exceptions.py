class DomainError(Exception):
    """Base exception for domain layer errors."""


class EmptyOrderError(DomainError):
    """Raised when an order is created without items."""

    def __init__(
        self, message: str = "An order must contain at least one item."
    ) -> None:
        super().__init__(message)
