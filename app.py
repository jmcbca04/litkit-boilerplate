import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="LitKit Boilerplate",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app layout


def main():
    st.title("🔥 LitKit - Streamlit Boilerplate")
    st.write(
        "Welcome to LitKit! The comprehensive boilerplate for Streamlit applications.")

    st.markdown("""
    ## Features
    - Authentication with Supabase
    - UI Component Library
    - Database Integration
    - And much more!
    """)

    st.info(
        "This is a placeholder. The content will be updated as development progresses.")


if __name__ == "__main__":
    main()
