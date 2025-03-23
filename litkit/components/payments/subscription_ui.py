"""
Subscription UI components.

This module provides UI components for displaying subscription status.
"""

import streamlit as st
from typing import Optional
from ...payments.subscription import (
    has_active_subscription,
    add_subscription as check_subscription
)
from ...auth.auth import is_authenticated, get_user


def subscription_status(use_sidebar: bool = False):
    """
    Display the current subscription status.

    Args:
        use_sidebar: If True, display in the sidebar
    """
    if not is_authenticated():
        container = st.sidebar if use_sidebar else st
        container.warning("Please log in to view subscription status.")
        return

    user = get_user()
    if not user:
        return

    container = st.sidebar if use_sidebar else st

    # Check subscription status (placeholder implementation)
    is_subscribed = has_active_subscription(user.get("id", ""))

    if is_subscribed:
        container.success("✅ You have an active subscription.")
    else:
        container.warning("⚠️ You don't have an active subscription.")
        container.info("Subscribe to access premium features.")


def subscription_required(
    required_text: str = "This feature requires a subscription",
    button_text: str = "Subscribe Now",
    button_color: str = "#FF4B4B",
    use_sidebar: bool = False
):
    """
    Check if the user has an active subscription and display appropriate UI.
    This is a decorator-like function that can be used to protect content.

    Args:
        required_text: Text to display if subscription is required
        button_text: Text for the subscription button
        button_color: Color for the subscription button
        use_sidebar: If True, display in the sidebar
    """
    return check_subscription(
        required=True,
        redirect_button_text=button_text,
        button_color=button_color,
        use_sidebar=use_sidebar
    )


def subscription_upsell(
    upsell_text: str = "Upgrade to access more features",
    button_text: str = "Upgrade Now",
    button_color: str = "#4CAF50",
    use_sidebar: bool = False
):
    """
    Display a non-blocking upsell message for subscriptions.

    Args:
        upsell_text: Text to display for the upsell
        button_text: Text for the upgrade button
        button_color: Color for the upgrade button
        use_sidebar: If True, display in the sidebar
    """
    # This is similar to subscription_required but doesn't block execution
    return check_subscription(
        required=False,
        redirect_button_text=button_text,
        button_color=button_color,
        use_sidebar=use_sidebar
    )
