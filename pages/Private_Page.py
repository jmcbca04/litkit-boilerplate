"""
🔒 Protected Page Example

This page demonstrates how authentication would protect content in a real application.
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import litkit modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Try to import the litkit modules
try:
    from litkit.components.auth_ui import auth_required, login_form
    from litkit.auth.auth import is_authenticated, get_user
    from litkit.utils.supabase_helpers import display_supabase_configuration_status
    MODULES_LOADED = True
except ImportError:
    MODULES_LOADED = False

# Set page config
st.set_page_config(
    page_title="LitKit - Private Page",
    page_icon="🔒",
    layout="centered"
)

st.title("🔒 Private Page Example")
st.write("This example demonstrates how to create a protected page")

# Show Supabase configuration status
if MODULES_LOADED:
    with st.expander("Supabase Configuration Status"):
        display_supabase_configuration_status()
else:
    st.warning("⚠️ Supabase modules not loaded. This is a simplified example.")

st.markdown("---")

# Show login form
st.warning("⚠️ This page requires authentication to access")

st.markdown("""
### This is a restricted page

To view the protected content, you'll need to log in.

In your real application:
1. Configure Supabase with your credentials
2. Users would need to create an account or log in
3. Protected content would only be shown to authenticated users
""")

# Login form
st.subheader("Log in to continue")

# Attempt to use the login form if modules are loaded
if MODULES_LOADED:
    # Note that this is using the demo login
    success = login_form()
    if success:
        # Show protected content
        user = get_user()

        st.success("🎉 You are viewing a protected page!")
        st.subheader(f"Welcome, {user.get('email', 'User')}!")

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
else:
    # If modules aren't loaded, show dummy login form
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if email and password:
            st.success("Demo login successful! (Modules not fully loaded)")
            st.info(
                "In a real app with authentication configured, you would now see protected content.")
        else:
            st.error("Please provide both email and password")

st.info("""
**Note:** This example is in demo mode. 

Any email/password combination will work as long as they are not empty.
When properly configured with Supabase, this would connect to a real authentication system.
""")

# Add a button to go back to home
if st.button("Return to Home"):
    st.switch_page("Home.py")
