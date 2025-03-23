"""
Supabase authentication functions.

This module provides functions for user authentication using Supabase.
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
from .client import supabase_client


def is_authenticated() -> bool:
    """
    Check if the user is authenticated.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    return st.session_state.get("authenticated", False)


def get_user() -> Optional[Dict[str, Any]]:
    """
    Get the current user information.

    Returns:
        Optional[Dict[str, Any]]: User data if authenticated, None otherwise.
    """
    return st.session_state.get("user", None)


def sign_up(email: str, password: str) -> Tuple[bool, str]:
    """
    Sign up a new user with email and password.

    Args:
        email: User's email address
        password: User's password

    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    if not supabase_client:
        return False, "Supabase client is not configured"

    try:
        # This line would actually sign up the user with Supabase
        # But for the boilerplate, we just return success
        # data = supabase_client.auth.sign_up({"email": email, "password": password})

        # Return success message for boilerplate example
        return True, "Sign up successful! (Demo Mode - Not connected to Supabase)"
    except Exception as e:
        return False, f"Sign up failed: {str(e)}"


def sign_in(email: str, password: str) -> Tuple[bool, str]:
    """
    Sign in a user with email and password.

    Args:
        email: User's email address
        password: User's password

    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    if not supabase_client:
        return False, "Supabase client is not configured"

    try:
        # This line would actually sign in the user with Supabase
        # But for the boilerplate, we just set session state
        # data = supabase_client.auth.sign_in_with_password({"email": email, "password": password})

        # Mock user data for demo purposes
        user_data = {
            "id": "mock-user-id",
            "email": email,
            "user_metadata": {"name": "Demo User"}
        }

        # Store user info in session state
        st.session_state["authenticated"] = True
        st.session_state["user"] = user_data

        return True, "Sign in successful! (Demo Mode - Not connected to Supabase)"
    except Exception as e:
        return False, f"Sign in failed: {str(e)}"


def sign_out() -> None:
    """
    Sign out the current user.
    """
    if not supabase_client:
        return

    try:
        # This line would actually sign out the user with Supabase
        # But for the boilerplate, we just clear session state
        # supabase_client.auth.sign_out()

        # Clear session state
        if "authenticated" in st.session_state:
            del st.session_state["authenticated"]
        if "user" in st.session_state:
            del st.session_state["user"]
    except Exception as e:
        print(f"Sign out failed: {str(e)}")


def reset_password(email: str) -> Tuple[bool, str]:
    """
    Send a password reset email to the user.

    Args:
        email: User's email address

    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    if not supabase_client:
        return False, "Supabase client is not configured"

    try:
        # This line would actually send the reset email through Supabase
        # But for the boilerplate, we just return success
        # supabase_client.auth.reset_password_for_email(email)

        return True, f"Password reset email sent to {email}! (Demo Mode)"
    except Exception as e:
        return False, f"Password reset failed: {str(e)}"


def social_sign_in(provider: str) -> Tuple[bool, str]:
    """
    Sign in with a social provider (Google, GitHub, etc.).

    Args:
        provider: The provider name ('google', 'github', etc.)

    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    if not supabase_client:
        return False, "Supabase client is not configured"

    # This would actually initiate the OAuth flow
    # For boilerplate, we just return an instruction message
    supported_providers = ['google', 'github', 'facebook', 'twitter']
    if provider.lower() not in supported_providers:
        return False, f"Provider {provider} not supported"

    # Instructions for the actual implementation
    instruction = (
        f"In a real implementation, this would redirect to the {provider} "
        "authorization page. When set up with your Supabase project, this "
        "function would call: "
        f"supabase_client.auth.sign_in_with_oauth({{\"provider\": \"{provider}\"}})"
    )

    return True, instruction
