"""
🔐 Authentication Example

This page demonstrates how authentication would work in a real application.
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import litkit modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Try to import the litkit modules
try:
    from litkit.components.auth_ui import (
        login_form, signup_form, reset_password_form,
        social_login_buttons, user_profile, auth_required
    )
    from litkit.auth.auth import is_authenticated, sign_out
    from litkit.utils.supabase_helpers import display_supabase_configuration_status
    MODULES_LOADED = True
except ImportError:
    MODULES_LOADED = False

# Set page config
st.set_page_config(
    page_title="LitKit - Auth Example",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Authentication Example")
st.write("This page demonstrates how to use authentication in your app")

# Show Supabase configuration status
if MODULES_LOADED:
    with st.expander("Supabase Configuration Status"):
        display_supabase_configuration_status()
else:
    st.warning("⚠️ Supabase modules not loaded. This is a simplified example.")

st.markdown("---")

if MODULES_LOADED:
    # Authentication UI
    if is_authenticated():
        st.success("You are logged in!")
        user_profile()

        # Protected content
        with st.expander("Protected Content (Only visible when logged in)"):
            st.write("This content is only visible to authenticated users.")
            st.image("https://picsum.photos/800/300", caption="A random image")

            if st.button("Refresh Random Image"):
                st.experimental_rerun()
    else:
        # Authentication options via tabs
        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Reset Password"])

        with tab1:
            if login_form():
                st.experimental_rerun()
            social_login_buttons()

        with tab2:
            if signup_form():
                st.info("Account created! You can now log in.")

        with tab3:
            reset_password_form()
else:
    # Simple mockup if modules aren't loaded
    tabs = st.tabs(["Login", "Sign Up", "Reset Password"])

    with tabs[0]:
        st.text_input("Email")
        st.text_input("Password", type="password")
        if st.button("Login"):
            st.success("Demo login successful!")
            st.info("In a real app, you would now be logged in.")

    with tabs[1]:
        st.text_input("Email", key="signup_email")
        st.text_input("Password", type="password", key="signup_pass")
        st.text_input("Confirm Password", type="password",
                      key="signup_confirm")
        if st.button("Sign Up"):
            st.success("Demo signup successful!")

    with tabs[2]:
        st.text_input("Email", key="reset_email")
        if st.button("Send Reset Link"):
            st.success("Demo reset link sent!")

st.info("""
**Note:** This example is in demo mode.

When properly configured with Supabase, this would connect to a real authentication system.
""")

# Add a button to go back to home
if st.button("Return to Home"):
    st.switch_page("Home.py")
