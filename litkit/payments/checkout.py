"""
Stripe checkout session management.

This module provides functions for creating and managing Stripe checkout sessions.
"""

import os
from typing import Dict, Any, Optional
import streamlit as st
from .stripe_client import check_stripe_configured, initialize_stripe

# Try to import stripe, with graceful fallback if not installed
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None


def get_checkout_settings() -> Dict[str, Any]:
    """
    Get the checkout settings from environment variables or Streamlit secrets.

    Returns:
        Dict[str, Any]: Dictionary of checkout settings
    """
    settings = {}

    # First try to get from Streamlit secrets
    if hasattr(st, "secrets") and "stripe" in st.secrets:
        secrets = st.secrets.get("stripe", {})
        settings["price_id"] = secrets.get("PRICE_ID")
        settings["success_url"] = secrets.get("SUCCESS_URL")
        settings["cancel_url"] = secrets.get("CANCEL_URL")

    # Fallback to environment variables
    if "price_id" not in settings or not settings["price_id"]:
        settings["price_id"] = os.getenv("STRIPE_PRICE_ID")
    if "success_url" not in settings or not settings["success_url"]:
        settings["success_url"] = os.getenv(
            "STRIPE_SUCCESS_URL", "http://localhost:8501")
    if "cancel_url" not in settings or not settings["cancel_url"]:
        settings["cancel_url"] = os.getenv(
            "STRIPE_CANCEL_URL", "http://localhost:8501")

    return settings


def create_checkout_session(
    user_email: Optional[str] = None,
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
    price_id: Optional[str] = None,
    quantity: int = 1,
    mode: str = "subscription"
) -> Optional[str]:
    """
    Create a Stripe checkout session.

    Args:
        user_email: Email of the user making the purchase
        success_url: URL to redirect to after successful payment
        cancel_url: URL to redirect to after cancelled payment
        price_id: Stripe Price ID for the subscription or product
        quantity: Quantity to purchase (default: 1)
        mode: 'subscription' or 'payment' (one-time)

    Returns:
        Optional[str]: URL for the checkout session or None if creation failed
    """
    if not check_stripe_configured() or not initialize_stripe():
        st.error(
            "Stripe is not properly configured. Please set up your Stripe credentials.")
        return None

    # Get settings with provided values or defaults
    settings = get_checkout_settings()

    # Override defaults with provided values
    if success_url:
        settings["success_url"] = success_url
    if cancel_url:
        settings["cancel_url"] = cancel_url
    if price_id:
        settings["price_id"] = price_id

    # Validate required settings
    if not settings.get("price_id"):
        st.error(
            "No Stripe Price ID found. Please set STRIPE_PRICE_ID in your environment variables.")
        return None

    if not settings.get("success_url"):
        st.error(
            "No success URL found. Please set STRIPE_SUCCESS_URL in your environment variables.")
        return None

    if not settings.get("cancel_url"):
        st.error(
            "No cancel URL found. Please set STRIPE_CANCEL_URL in your environment variables.")
        return None

    try:
        # Create the checkout session with Stripe
        checkout_params = {
            "line_items": [
                {
                    "price": settings["price_id"],
                    "quantity": quantity,
                }
            ],
            "mode": mode,
            "success_url": settings["success_url"],
            "cancel_url": settings["cancel_url"],
        }

        # Add customer email if provided
        if user_email:
            checkout_params["customer_email"] = user_email

        # Create the checkout session
        checkout_session = stripe.checkout.Session.create(**checkout_params)

        return checkout_session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None
