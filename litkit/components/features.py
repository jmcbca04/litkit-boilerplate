"""
Feature sections component for LitKit.
Displays feature cards in a grid layout.
"""

import streamlit as st
from typing import List, Dict, Optional

from litkit.components.base import BaseComponent


class Features(BaseComponent):
    """Features section component for displaying product features."""

    def __init__(
        self,
        title: str,
        features: List[Dict[str, str]],
        columns: int = 2,
        background_color: Optional[str] = None,
        text_color: str = "white",
        key: Optional[str] = None,
    ):
        """Initialize features component.

        Args:
            title: Section title
            features: List of feature dictionaries with keys:
                     - "icon": Emoji or icon text
                     - "title": Feature title
                     - "description": Feature description
            columns: Number of columns to display (1-4)
            background_color: Background color of the section
            text_color: Text color for the section
            key: Unique component key
        """
        super().__init__(key)
        self.title = title
        self.features = features
        # Ensure columns is between 1 and 4
        self.columns = min(max(columns, 1), 4)
        self.background_color = (
            background_color or self.theme["colors"]["background"]
        )
        self.text_color = text_color

    def render(self) -> None:
        """Render the features component."""
        # Apply base styling
        st.markdown(
            f"""
            <style>
            .features-title {{
                color: {self.text_color} !important;
                font-size: 2rem !important;
                font-weight: bold !important;
                margin-bottom: 30px;
                text-align: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        # Section title
        st.markdown(
            f'<h2 class="features-title">{self.title}</h2>',
            unsafe_allow_html=True
        )

        # Create columns for features
        cols = st.columns(self.columns)

        # Apply card container styling - using direct CSS for container div
        card_css = """
        <style>
        .element-container div[data-testid="stVerticalBlock"] > div {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }
        </style>
        """
        st.markdown(card_css, unsafe_allow_html=True)

        # Distribute features across columns - using container for each card
        for i, feature in enumerate(self.features):
            col_idx = i % self.columns

            with cols[col_idx]:
                # Create a container for each feature card with manual styling
                with st.container():
                    # Apply direct styling to this specific container
                    st.markdown(
                        """
                        <style>
                        div.stContainer {
                            background-color: rgba(255, 255, 255, 0.1);
                            border-radius: 8px;
                            padding: 16px;
                            margin-bottom: 16px;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    # Feature content
                    icon = feature.get('icon', '✨')
                    title = feature.get('title', '')
                    description = feature.get('description', '')

                    # Container for the feature card with forced styling
                    st.markdown(
                        f"""
                        <div style="background-color: rgba(255, 255, 255, 0.1); 
                                 border-radius: 8px; padding: 16px; margin-bottom: 10px;">
                            <div style="font-size: 2rem; margin-bottom: 10px;">
                                {icon}
                            </div>
                            <h3 style="color: {self.text_color}; font-size: 1.3rem; 
                                      font-weight: bold; margin-bottom: 10px;">
                                {title}
                            </h3>
                            <p style="color: {self.text_color}; opacity: 0.9;">
                                {description}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
