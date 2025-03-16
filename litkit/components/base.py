"""
Base component class for LitKit UI components.
All UI components should inherit from this class.
"""

import streamlit as st
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from litkit.ui.theme import get_theme


class BaseComponent(ABC):
    """Base class for all LitKit UI components."""

    def __init__(self, key: Optional[str] = None):
        """Initialize the component with a unique key.

        Args:
            key: Unique key for the component. If None, a random key will be generated.
        """
        # Increment component count in session state
        if "component_count" not in st.session_state:
            st.session_state.component_count = 0
        st.session_state.component_count += 1

        # Generate key using component count as string
        component_count_str = str(st.session_state.component_count)
        self.key = key or f"{self.__class__.__name__}_{component_count_str}"
        self.theme = get_theme()

    @abstractmethod
    def render(self) -> Any:
        """Render the component. Must be implemented by subclasses."""
        pass

    def get_html_tag(self, tag: str, content: str, attributes: Dict[str, str] = None) -> str:
        """Generate an HTML tag with attributes.

        Args:
            tag: The HTML tag name (e.g., 'div', 'span').
            content: The content inside the tag.
            attributes: Dictionary of HTML attributes.

        Returns:
            A string with the HTML tag.
        """
        attributes = attributes or {}
        attrs_str = " ".join([f'{k}="{v}"' for k, v in attributes.items()])
        return f"<{tag} {attrs_str}>{content}</{tag}>"

    def custom_html(self, html: str) -> None:
        """Render custom HTML with the component's key.

        Args:
            html: The HTML string to render.
        """
        # st.markdown doesn't support key parameter
        st.markdown(html, unsafe_allow_html=True)

    def apply_custom_css(self, css: str) -> None:
        """Apply custom CSS for the component.

        Args:
            css: The CSS string to apply.
        """
        # st.markdown doesn't support key parameter
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
