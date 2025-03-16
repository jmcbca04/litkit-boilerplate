"""
Theme management for LitKit UI components.
This module provides functions for consistent styling across the application.
"""

import streamlit as st


# Color palette
PRIMARY_COLOR = "#FF4B4B"
SECONDARY_COLOR = "#0068C9"
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#262730"
GRAY_COLOR = "#F0F2F6"

# Font settings
FONT_FAMILY = "sans-serif"
HEADING_FONT_SIZE = "2rem"
SUBHEADING_FONT_SIZE = "1.5rem"
BODY_FONT_SIZE = "1rem"
SMALL_FONT_SIZE = "0.875rem"

# Spacing
SPACING_XS = "0.25rem"
SPACING_SM = "0.5rem"
SPACING_MD = "1rem"
SPACING_LG = "1.5rem"
SPACING_XL = "2rem"

# Border radius
BORDER_RADIUS_SM = "0.25rem"
BORDER_RADIUS_MD = "0.5rem"
BORDER_RADIUS_LG = "1rem"


def apply_theme():
    """Apply the LitKit theme to the current Streamlit app."""
    st.markdown(
        f"""
        <style>
        /* Global styles */
        .stApp {{
            font-family: {FONT_FAMILY};
            color: {TEXT_COLOR};
        }}
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {FONT_FAMILY};
            font-weight: bold;
        }}
        
        /* Hero section text color overrides */
        [class*="hero-container"] h1,
        [class*="hero-container"] p,
        [class*="hero-container"] div,
        [class*="hero-heading"],
        [class*="hero-subheading"] {{
            color: white !important;
        }}
        
        /* Custom button styles */
        .litkit-button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            padding: {SPACING_SM} {SPACING_MD};
            border-radius: {BORDER_RADIUS_SM};
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }}
        
        .litkit-button:hover {{
            background-color: {SECONDARY_COLOR};
            cursor: pointer;
        }}
        
        /* Card styles */
        .litkit-card {{
            background-color: white;
            border-radius: {BORDER_RADIUS_MD};
            padding: {SPACING_MD};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_theme():
    """Return a dictionary of theme variables."""
    return {
        "colors": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "background": BACKGROUND_COLOR,
            "text": TEXT_COLOR,
            "gray": GRAY_COLOR,
        },
        "fonts": {
            "family": FONT_FAMILY,
            "sizes": {
                "heading": HEADING_FONT_SIZE,
                "subheading": SUBHEADING_FONT_SIZE,
                "body": BODY_FONT_SIZE,
                "small": SMALL_FONT_SIZE,
            },
        },
        "spacing": {
            "xs": SPACING_XS,
            "sm": SPACING_SM,
            "md": SPACING_MD,
            "lg": SPACING_LG,
            "xl": SPACING_XL,
        },
        "borders": {
            "radius_sm": BORDER_RADIUS_SM,
            "radius_md": BORDER_RADIUS_MD,
            "radius_lg": BORDER_RADIUS_LG,
        },
    }
