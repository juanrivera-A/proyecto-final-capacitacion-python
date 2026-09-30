class DomainError(Exception):
    """Base exception for domain layer errors."""


class EmptyOrderError(DomainError):
    """Raised when an order is created without items."""

    def __init__(
        self, message: str = "An order must contain at least one item."
    ) -> None:
        super().__init__(message)


class InvalidOrderStateError(DomainError):
    """Raised when an operation is invalid for the current order state."""

    def __init__(
        self, message: str = "Invalid action for current order status."
    ) -> None:
        super().__init__(message)
