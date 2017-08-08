

class CredentialsNotFoundError(ValueError):
    """Raised when api key or repo id not found"""

class InsufficientInformationError(BaseException):
    """Base class used when necessary parameters not provided"""

class InsufficientSearchParametersError(InsufficientInformationError):
    """Raised when not all values given to search endpoint"""
