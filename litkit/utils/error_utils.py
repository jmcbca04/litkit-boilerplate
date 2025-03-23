"""
Error utility functions for LitKit.

This module combines error handling, logging, and UI components into
a comprehensive error management system.
"""

from typing import Optional, Dict, Any, Callable, TypeVar, ParamSpec

from .error_handling import handle_error
from .logging import app_logger as logger
from ..ui.error_display import show_error, show_error_and_stop

# Type variables for decorator
P = ParamSpec('P')
R = TypeVar('R')


def log_and_display_error(
    exception: Exception,
    user_message: Optional[str] = None,
    show_ui: bool = True,
    critical: bool = False,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Process an exception by logging it and optionally displaying a UI message.

    Args:
        exception: The caught exception
        user_message: Optional user-friendly message (defaults to exception message)
        show_ui: Whether to show a UI message
        critical: Whether this is a critical error that should stop execution
        details: Additional details to include in the error display
    """
    # Get error message and details using our handler
    display_message, error_details = handle_error(exception, user_message)

    # Add any additional details
    if details:
        error_details.update(details)

    # Log the error
    if critical:
        logger.critical(f"{display_message} - {str(exception)}")
    else:
        logger.error(f"{display_message} - {str(exception)}")

    logger.debug(f"Error details: {error_details}")

    # Display UI message if requested
    if show_ui:
        if critical:
            show_error_and_stop(display_message, details=error_details)
        else:
            show_error(display_message, details=error_details)


def try_except_decorator(
    error_message: Optional[str] = None,
    show_ui: bool = True,
    critical: bool = False
) -> Callable[[Callable[P, R]], Callable[P, Optional[R]]]:
    """
    Decorator that wraps a function in a try-except block.

    Args:
        error_message: Optional error message to display
        show_ui: Whether to show a UI message
        critical: Whether this is a critical error that should stop execution

    Returns:
        Decorated function
    """
    def decorator(func: Callable[P, R]) -> Callable[P, Optional[R]]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Optional[R]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get appropriate message
                message = error_message or f"Error in {func.__name__}: {str(e)}"

                # Process the exception
                log_and_display_error(
                    e, message, show_ui=show_ui, critical=critical
                )

                # Return None for non-critical errors
                if not critical:
                    return None

        return wrapper
    return decorator
