class LibraryError(Exception):
    """Base exception for library application errors."""


class ValidationError(LibraryError):
    """Raised when user or application data is invalid."""


class StudentNotFoundError(LibraryError):
    """Raised when a student does not exist."""


class BookNotFoundError(LibraryError):
    """Raised when a book does not exist."""


class BookUnavailableError(LibraryError):
    """Raised when no copy of a book is available."""


class DuplicateRecordError(LibraryError):
    """Raised when a duplicate record is not allowed."""


class BorrowLimitError(LibraryError):
    """Raised when a student reaches the borrowing limit."""


class PersistenceError(LibraryError):
    """Raised when JSON data cannot be loaded or saved."""