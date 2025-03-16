"""
LitKit main application.
Demonstrates the UI components and features of the boilerplate.
"""

import streamlit as st

from litkit.ui.theme import apply_theme
from litkit.components import Header, Hero

# Set page configuration
st.set_page_config(
    page_title="LitKit Boilerplate",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the LitKit theme
apply_theme()


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

    # Content below the hero
    st.markdown('<h1 style="color: white;">Features</h1>', unsafe_allow_html=True)

    # Feature columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 style="color: white;">🔐 Authentication</h3>', unsafe_allow_html=True)
        st.write("""
        Secure user authentication with Supabase, including social 
        login options. Easily manage user sessions and profiles.
        """)

        st.markdown('<h3 style="color: white;">🎨 UI Components</h3>', unsafe_allow_html=True)
        st.write("""
        Beautiful, responsive UI components designed specifically 
        for Streamlit. Customizable and easy to use.
        """)

    with col2:
        st.markdown('<h3 style="color: white;">💾 Database Integration</h3>', unsafe_allow_html=True)
        st.write("""
        Built-in Supabase database integration for storing and 
        managing your data. Simple CRUD operations and data models.
        """)

        st.markdown('<h3 style="color: white;">💰 Payments</h3>', unsafe_allow_html=True)
        st.write("""
        Stripe integration for handling payments and subscriptions.
        Coming soon!
        """)

    # Component showcase
    st.markdown('<h2 style="color: white;">Component Showcase</h2>', unsafe_allow_html=True)
    st.write(
        "LitKit includes a variety of UI components to help you build "
        "beautiful Streamlit apps quickly."
    )

    st.markdown('<h3 style="color: white;">Current Components</h3>', unsafe_allow_html=True)
    components = [
        "✅ Header/Navigation",
        "✅ Hero Section",
        "⏳ Feature Sections",
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
