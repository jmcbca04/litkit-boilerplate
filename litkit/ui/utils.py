"""
Utility functions for UI components.
"""

import streamlit as st
from typing import Dict, List, Any, Tuple


def sanitize_html(text: str) -> str:
    """Sanitize text for safe HTML rendering.

    Args:
        text: Input text to sanitize

    Returns:
        Sanitized text
    """
    if text is None:
        return ""

    # Replace HTML special characters
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text


def create_grid(columns: int = 2, gap: str = "1rem") -> List[st.columns]:
    """Create a grid layout with equal columns.

    Args:
        columns: Number of columns in the grid
        gap: CSS gap between columns (applied as padding)

    Returns:
        List of column objects
    """
    col_sizes = [1] * columns
    cols = st.columns(col_sizes)

    # Apply CSS to create gap between columns
    if gap:
        for i, col in enumerate(cols):
            # Add left padding to all but first column
            if i > 0:
                with col:
                    st.markdown(f"<style>div[data-testid='column'] {{padding-left: {gap};}}</style>",
                                unsafe_allow_html=True)

    return cols


def show_tooltip(text: str, tooltip: str, key: str = None) -> None:
    """Show text with a tooltip on hover.

    Args:
        text: The text to display
        tooltip: The tooltip text
        key: Optional unique key for the element
    """
    if key is None:
        key = f"tooltip_{text}"

    html = f"""
    <div style="position: relative; display: inline-block;" title="{sanitize_html(tooltip)}">
        {sanitize_html(text)}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True, key=key)
