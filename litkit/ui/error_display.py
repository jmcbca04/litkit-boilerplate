"""
UI components for displaying error messages in Streamlit.

This module provides utilities for displaying user-friendly error messages
in the Streamlit UI.
"""

import streamlit as st
from typing import Optional, Dict, Any


def show_error(
    message: str,
    title: Optional[str] = "Error",
    icon: str = "❌",
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Display an error message to the user.

    Args:
        message: The error message to display
        title: Optional title for the error box
        icon: Icon to display next to the title
        details: Optional technical details (shown in expander)
    """
    # Create an error box with custom styling
    st.markdown(
        f"""
        <div style="
            background-color: #FFEBEE; 
            padding: 1rem; 
            border-radius: 0.5rem; 
            border-left: 5px solid #F44336;
            margin-bottom: 1rem;
        ">
            <h3 style="color: #D32F2F; margin-top: 0;">{icon} {title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show technical details in an expander if provided
    if details:
        with st.expander("Technical Details"):
            for key, value in details.items():
                st.text(f"{key}: {value}")


def show_warning(
    message: str,
    title: Optional[str] = "Warning",
    icon: str = "⚠️"
) -> None:
    """
    Display a warning message to the user.

    Args:
        message: The warning message to display
        title: Optional title for the warning box
        icon: Icon to display next to the title
    """
    # Create a warning box with custom styling
    st.markdown(
        f"""
        <div style="
            background-color: #FFF8E1; 
            padding: 1rem; 
            border-radius: 0.5rem; 
            border-left: 5px solid #FFC107;
            margin-bottom: 1rem;
        ">
            <h3 style="color: #FF8F00; margin-top: 0;">{icon} {title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_error_and_stop(
    message: str,
    title: Optional[str] = "Error",
    icon: str = "🛑",
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Display an error message and stop execution with st.stop().

    This is useful for critical errors where the application cannot continue.

    Args:
        message: The error message to display
        title: Optional title for the error box
        icon: Icon to display next to the title
        details: Optional technical details (shown in expander)
    """
    show_error(message, title, icon, details)
    st.stop()
