"""
LitKit main application.
Demonstrates the UI components and features of the boilerplate.
"""

import streamlit as st

from litkit.ui.theme import apply_theme
from litkit.components import Header, Hero, Features

# Set page configuration
st.set_page_config(
    page_title="LitKit Boilerplate",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the LitKit theme
apply_theme()

# Fix for unwanted red blocks
st.markdown("""
<style>
    /* Remove the unwanted red sections */
    .stApp > header {
        background-color: transparent !important;
        height: 0 !important;
    }
    
    /* Remove top padding */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Override default body background */
    .stApp {
        background-color: #0E1117 !important;
    }
    
    /* Fix for the hero section */
    .hero-section + div {
        display: none !important;
    }
    
    /* Override default Streamlit elements that might be causing red bars */
    [data-testid="stAppViewBlockContainer"] > div:first-child {
        background-color: transparent !important;
    }
    
    /* Hide any top red banners */
    .element-container:has(> div[class*="stMarkdown"]:first-child):first-child div {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Header component
    header = Header(
        title="LitKit",
        logo_url=(
            "https://cdn-icons-png.flaticon.com/512/785/785116.png"  # Fire icon
        ),
        nav_items=[
            {"label": "Home", "url": "#"},
            {"label": "Features", "url": "#features"},
            {"label": "Pricing", "url": "#pricing"},
            {"label": "Documentation", "url": "#docs"},
        ],
    )
    header.render()

    # Hero component
    hero = Hero(
        heading="Build Streamlit Apps Faster",
        subheading=(
            "The comprehensive boilerplate for Streamlit applications with "
            "authentication, payments, UI components, and more."
        ),
        background_color="#FF4B4B",
    )
    hero.render()

    # Force white text in hero section with direct CSS injection
    st.markdown("""
    <style>
    .stMarkdown h1, 
    .stMarkdown p, 
    .stMarkdown div[data-testid="stMarkdownContainer"] p,
    .stMarkdown div[data-testid="stMarkdownContainer"] h1 {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Features component
    features = Features(
        title="Features",
        features=[
            {
                "icon": "🔐",
                "title": "Authentication",
                "description": (
                    "Secure user authentication with Supabase, including social "
                    "login options. Easily manage user sessions and profiles."
                ),
            },
            {
                "icon": "🎨",
                "title": "UI Components",
                "description": (
                    "Beautiful, responsive UI components designed specifically "
                    "for Streamlit. Customizable and easy to use."
                ),
            },
            {
                "icon": "💾",
                "title": "Database Integration",
                "description": (
                    "Built-in Supabase database integration for storing and "
                    "managing your data. Simple CRUD operations and data models."
                ),
            },
            {
                "icon": "💰",
                "title": "Payments",
                "description": (
                    "Stripe integration for handling payments and subscriptions. "
                    "Coming soon!"
                ),
            },
        ],
    )
    features.render()

    # Component showcase
    st.markdown('<h2 style="color: white;">Component Showcase</h2>',
                unsafe_allow_html=True)
    st.write(
        "LitKit includes a variety of UI components to help you build "
        "beautiful Streamlit apps quickly."
    )

    st.markdown('<h3 style="color: white;">Current Components</h3>',
                unsafe_allow_html=True)
    components = [
        "✅ Header/Navigation",
        "✅ Hero Section",
        "✅ Feature Sections",
        "⏳ Pricing Tables",
        "⏳ FAQ Component",
        "⏳ Testimonials",
        "⏳ Footer",
    ]

    for component in components:
        st.markdown(component)

    st.info("More components will be added in future updates!")


if __name__ == "__main__":
    main()
