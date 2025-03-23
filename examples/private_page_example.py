"""
Example of a private page protected by authentication.

Run with:
streamlit run examples/private_page_example.py
"""

# First import standard libraries
from litkit.components.auth_ui import auth_required, login_form
import streamlit as st
import sys
import os

# Add parent directory to path to import litkit modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Now import the litkit modules

# Import the rest of required modules
try:
    from litkit.utils.supabase_helpers import display_supabase_configuration_status
    from litkit.auth.auth import is_authenticated, get_user
    MODULES_LOADED = True
except ImportError:
    MODULES_LOADED = False


def main():
    """Main function for the private page example."""
    st.set_page_config(
        page_title="LitKit - Private Page Example",
        page_icon="🔒",
        layout="centered"
    )

    st.title("🔒 LitKit Private Page Example")
    st.write("This example demonstrates how to create a protected page")

    # Show Supabase configuration status
    if MODULES_LOADED:
        with st.expander("Supabase Configuration Status"):
            display_supabase_configuration_status()
    else:
        st.warning(
            "⚠️ Supabase modules not loaded. This is a simplified example.")

    st.markdown("---")

    # Show login form directly since we may not have is_authenticated
    show_login_required()


@auth_required
def show_protected_content():
    """Content that should only be visible to authenticated users."""
    if not MODULES_LOADED:
        st.error("Authentication modules not loaded properly")
        return

    user = get_user()

    st.success("🎉 You are viewing a protected page!")

    st.subheader(f"Welcome, {user.get('email', 'User')}!")

    st.markdown("""
    ### This content is protected
    
    In a real application with authentication enabled, this page would only be 
    accessible to users who have logged in.
    
    You can use the `@auth_required` decorator on any function to protect it:
    
    ```python
    @auth_required
    def my_protected_function():
        # This will only run for authenticated users
        st.write("Secret content here!")
    ```
    
    Or check authentication manually:
    
    ```python
    if is_authenticated():
        # Show protected content
        st.write("You can see this because you're logged in")
    else:
        # Show login prompt
        st.warning("Please log in to continue")
    ```
    """)

    # Example of protected data
    st.subheader("Your Private Data")

    st.markdown("#### User Profile")
    st.json({
        "id": user.get("id", "mock-user-id"),
        "email": user.get("email", "user@example.com"),
        "name": user.get("user_metadata", {}).get("name", "Demo User"),
        "membership": "Premium",
        "joined": "2023-05-15"
    })

    st.markdown("#### Analytics")
    cols = st.columns(3)
    cols[0].metric("Projects", "12", "+2")
    cols[1].metric("Actions", "483", "+28")
    cols[2].metric("Resources", "24", "-1")

    # Fun interactive element that would be protected
    st.subheader("Protected Interactive Demo")
    selected_color = st.color_picker("Pick a color", "#1E88E5")
    st.markdown(f"""
        <div style="background-color: {selected_color}; padding: 20px; 
        border-radius: 10px; color: white; text-align: center;">
            <h3>This custom element is protected!</h3>
            <p>Only authenticated users would see this content.</p>
        </div>
    """, unsafe_allow_html=True)


def show_login_required():
    """Content shown to unauthenticated users."""
    st.warning("⚠️ This page requires authentication to access")

    st.markdown("""
    ### This is a restricted page
    
    To view the protected content, you'll need to log in.
    
    In your real application:
    1. Configure Supabase with your credentials
    2. Users would need to create an account or log in
    3. Protected content would only be shown to authenticated users
    """)

    # Demonstrate login form
    st.subheader("Log in to continue")

    # Note that this is using the demo login
    success = login_form()
    if success and MODULES_LOADED:
        show_protected_content()

    st.info("""
    **Note:** This example is in demo mode. 
    
    Any email/password combination will work as long as they are not empty.
    """)


if __name__ == "__main__":
    main()
