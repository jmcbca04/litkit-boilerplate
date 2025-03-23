"""
Error handling utilities for LitKit.

This module provides custom exception classes and error handling functions
to standardize error management across the application.
"""

import traceback
from typing import Dict, Any, Optional, Tuple


class LitKitError(Exception):
    """Base exception class for all LitKit-specific errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Initialize the exception with a message and optional details.

        Args:
            message: Human-readable error message
            details: Additional context about the error (optional)
        """
        self.message = message
        self.details = details or {}
        super().__init__(message)


class AuthError(LitKitError):
    """Exception raised for authentication and authorization errors."""
    pass


class DatabaseError(LitKitError):
    """Exception raised for database operation failures."""
    pass


class PaymentError(LitKitError):
    """Exception raised for payment processing issues."""
    pass


def handle_error(
    exception: Exception,
    user_message: Optional[str] = None,
    log_traceback: bool = True
) -> Tuple[str, Dict[str, Any]]:
    """
    Process an exception and return a standardized error response.

    Args:
        exception: The caught exception
        user_message: An optional user-friendly message to display
        log_traceback: Whether to include a traceback in the logs

    Returns:
        A tuple of (user-friendly message, error details dictionary)
    """
    # Default error message if none provided
    if user_message is None:
        if isinstance(exception, LitKitError):
            user_message = exception.message
        else:
            user_message = "An unexpected error occurred. Please try again later."

    # Capture error details
    error_type = type(exception).__name__
    error_details = {
        "type": error_type,
        "message": str(exception),
    }

    # Add traceback for internal errors if requested
    if log_traceback:
        error_details["traceback"] = traceback.format_exc()

    # Add any custom details for LitKitError types
    if isinstance(exception, LitKitError) and exception.details:
        error_details.update(exception.details)

    return user_message, error_details
