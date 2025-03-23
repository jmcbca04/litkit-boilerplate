"""
Authentication UI components.

This module provides Streamlit UI components for authentication.
"""

import streamlit as st
from ..auth.auth import (
    sign_in,
    sign_up,
    sign_out,
    reset_password,
    social_sign_in,
    is_authenticated,
    get_user
)


def login_form():
    """
    Display a login form with email and password inputs.

    Returns:
        bool: True if login was successful, False otherwise.
    """
    with st.form("login_form"):
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")

        if submit:
            if email and password:
                success, message = sign_in(email, password)
                if success:
                    st.success(message)
                    return True
                else:
                    st.error(message)
            else:
                st.error("Please provide both email and password")

    return False


def signup_form():
    """
    Display a signup form with email and password inputs.

    Returns:
        bool: True if signup was successful, False otherwise.
    """
    with st.form("signup_form"):
        st.subheader("Create an Account")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input(
            "Password", type="password", key="signup_password")
        password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_password_confirm"
        )
        submit = st.form_submit_button("Sign Up")

        if submit:
            if not email or not password:
                st.error("Please provide both email and password")
                return False

            if password != password_confirm:
                st.error("Passwords do not match")
                return False

            success, message = sign_up(email, password)
            if success:
                st.success(message)
                return True
            else:
                st.error(message)
                return False

    return False


def reset_password_form():
    """
    Display a password reset form with email input.

    Returns:
        bool: True if password reset request was successful, False otherwise.
    """
    with st.form("reset_password_form"):
        st.subheader("Reset Password")
        email = st.text_input("Email", key="reset_email")
        submit = st.form_submit_button("Send Reset Link")

        if submit:
            if email:
                success, message = reset_password(email)
                if success:
                    st.success(message)
                    return True
                else:
                    st.error(message)
            else:
                st.error("Please provide your email")

    return False


def social_login_buttons():
    """
    Display social login buttons for various providers.

    Returns:
        bool: True if social login was successful, False otherwise.
    """
    st.subheader("Or sign in with")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Google", key="google_login"):
            success, message = social_sign_in("google")
            if success:
                st.info(message)
            else:
                st.error(message)

    with col2:
        if st.button("GitHub", key="github_login"):
            success, message = social_sign_in("github")
            if success:
                st.info(message)
            else:
                st.error(message)

    return False


def user_profile():
    """
    Display the user profile if authenticated.
    """
    if not is_authenticated():
        st.warning("You are not logged in")
        return

    user = get_user()
    if not user:
        return

    st.subheader("Your Profile")
    st.write(f"Email: {user.get('email', 'Unknown')}")

    if user.get('user_metadata') and user['user_metadata'].get('name'):
        st.write(f"Name: {user['user_metadata']['name']}")

    if st.button("Sign Out"):
        sign_out()
        st.experimental_rerun()


def auth_required(func):
    """
    Decorator to require authentication for a function.
    Shows a login form if the user is not authenticated.

    Args:
        func: The function to wrap

    Returns:
        Function: The wrapped function
    """
    def wrapper(*args, **kwargs):
        if is_authenticated():
            return func(*args, **kwargs)
        else:
            st.warning("Please log in to access this content")
            login_form()
            return None

    return wrapper
