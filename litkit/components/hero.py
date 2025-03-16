"""
Hero section component for LitKit.
A simple hero section with no buttons.
"""

import streamlit as st
from typing import Optional
import random

from litkit.components.base import BaseComponent


class Hero(BaseComponent):
    """Hero section component for landing pages."""

    def __init__(
        self,
        heading: str,
        subheading: str = "",
        image_url: Optional[str] = None,
        background_color: Optional[str] = None,
        alignment: str = "center",
        key: Optional[str] = None,
    ):
        """Initialize hero component.

        Args:
            heading: Main heading text
            subheading: Subheading text
            image_url: URL to an image to display
            background_color: Background color (defaults to theme primary)
            alignment: Text alignment ("left", "center", or "right")
            key: Unique component key
        """
        super().__init__(key)
        self.heading = heading
        self.subheading = subheading
        self.image_url = image_url
        self.background_color = (
            background_color or self.theme["colors"]["primary"]
        )
        self.alignment = alignment

    def render(self) -> None:
        """Render the hero component."""
        # Direct Streamlit components approach instead of HTML/CSS

        custom_css = f"""
        <style>
        .hero-section {{
            background-color: {self.background_color};
            padding: 160px 40px;
            min-height: 300px;
            border-radius: 8px;
            margin: 0;
            width: 100%;
            text-align: {self.alignment};
        }}
        
        .hero-section h1, 
        .hero-section p,
        .hero-section div {{
            color: white !important;
            font-weight: normal !important;
        }}
        
        .hero-heading {{
            font-size: 2.5rem !important;
            font-weight: bold !important;
            margin-bottom: 16px;
            color: white !important;
        }}
        
        .hero-subheading {{
            font-size: 1.8rem !important;
            opacity: 0.9;
            margin-bottom: 24px;
            color: white !important;
        }}
        </style>
        """

        st.markdown(custom_css, unsafe_allow_html=True)

        # Render directly without columns for full width
        st.markdown(
            f"""
            <div class="hero-section">
                <h1 class="hero-heading">
                    {self.heading}
                </h1>
                <p class="hero-subheading">
                    {self.subheading}
                </p>
                {f'<img src="{self.image_url}" alt="Hero Image" style="max-width: 100%; border-radius: 8px;">' if self.image_url else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
