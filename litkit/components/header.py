"""
Header/Navigation component for LitKit.
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple, Union

from litkit.components.base import BaseComponent


class Header(BaseComponent):
    """Header component with navigation links."""

    def __init__(
        self,
        title: str,
        logo_url: Optional[str] = None,
        nav_items: Optional[List[Dict[str, str]]] = None,
        is_sticky: bool = True,
        key: Optional[str] = None,
    ):
        """Initialize header component.

        Args:
            title: The title to display in the header
            logo_url: Optional URL to a logo image
            nav_items: List of navigation items [{"label": "Home", "url": "#"}]
            is_sticky: Whether the header should stick to the top when scrolling
            key: Unique component key
        """
        super().__init__(key)
        self.title = title
        self.logo_url = logo_url
        self.nav_items = nav_items or []
        self.is_sticky = is_sticky

    def render(self) -> None:
        """Render the header component."""
        # CSS for the header
        header_css = f"""
        .litkit-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: {self.theme["spacing"]["md"]};
            background-color: white;
            border-bottom: 1px solid {self.theme["colors"]["gray"]};
            margin-bottom: {self.theme["spacing"]["md"]};
        }}
        
        .litkit-header-sticky {{
            position: sticky;
            top: 0;
            z-index: 999;
        }}
        
        .litkit-logo-title {{
            display: flex;
            align-items: center;
            gap: {self.theme["spacing"]["sm"]};
        }}
        
        .litkit-nav {{
            display: flex;
            gap: {self.theme["spacing"]["md"]};
        }}
        
        .litkit-nav-item {{
            text-decoration: none;
            color: {self.theme["colors"]["text"]};
            padding: {self.theme["spacing"]["xs"]} {self.theme["spacing"]["sm"]};
            border-radius: {self.theme["borders"]["radius_sm"]};
            transition: all 0.2s;
        }}
        
        .litkit-nav-item:hover {{
            background-color: {self.theme["colors"]["gray"]};
        }}
        
        /* Mobile responsive styles */
        @media (max-width: 768px) {{
            .litkit-header {{
                flex-direction: column;
                gap: {self.theme["spacing"]["sm"]};
            }}
            
            .litkit-nav {{
                flex-wrap: wrap;
                justify-content: center;
            }}
        }}
        """

        # Apply the CSS
        self.apply_custom_css(header_css)

        # Build header HTML
        header_class = "litkit-header"
        if self.is_sticky:
            header_class += " litkit-header-sticky"

        # Logo and title section
        logo_title_html = ""
        if self.logo_url:
            logo_title_html += f'<img src="{self.logo_url}" alt="Logo" height="32px">'

        logo_title_html += f'<h2 style="margin: 0; font-size: 1.5rem;">{self.title}</h2>'

        # Navigation items
        nav_items_html = ""
        for item in self.nav_items:
            nav_items_html += f'<a href="{item.get("url", "#")}" class="litkit-nav-item">{item.get("label", "")}</a>'

        # Complete header HTML
        header_html = f"""
        <div class="{header_class}">
            <div class="litkit-logo-title">
                {logo_title_html}
            </div>
            <div class="litkit-nav">
                {nav_items_html}
            </div>
        </div>
        """

        # Render the header
        self.custom_html(header_html)

        # Add some spacing after the header
        st.markdown("")
