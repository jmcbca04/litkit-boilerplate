"""
Stripe client configuration.

This module sets up the connection to Stripe for payment processing.
"""

import os
from typing import Optional
import streamlit as st
from dotenv import load_dotenv

# Try to import stripe, with graceful fallback if not installed
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

# Load environment variables
load_dotenv()

# Load Stripe credentials from environment variables or Streamlit secrets


def get_stripe_key() -> Optional[str]:
    """
    Get the appropriate Stripe API key based on mode.

    Returns:
        Optional[str]: Stripe API key or None if not configured
    """
    # First try to get from Streamlit secrets
    if hasattr(st, "secrets") and "stripe" in st.secrets:
        # Check if we're in test mode
        if st.secrets.get("stripe", {}).get("PAYMENT_MODE", "test") == "test":
            return st.secrets.get("stripe", {}).get("API_KEY_TEST")
        else:
            return st.secrets.get("stripe", {}).get("API_KEY")

    # Fallback to environment variables
    payment_mode = os.getenv("STRIPE_PAYMENT_MODE", "test")
    if payment_mode == "test":
        return os.getenv("STRIPE_API_KEY_TEST")
    else:
        return os.getenv("STRIPE_API_KEY")


def initialize_stripe() -> bool:
    """
    Initialize the Stripe client with the appropriate API key.

    Returns:
        bool: True if Stripe was initialized successfully, False otherwise
    """
    if not STRIPE_AVAILABLE:
        print("Warning: Stripe Python package not installed.")
        print("Please install it with: pip install stripe")
        return False

    api_key = get_stripe_key()
    if not api_key:
        print("Warning: Stripe API key not found in environment variables or Streamlit secrets.")
        print("Please set STRIPE_API_KEY_TEST or STRIPE_API_KEY in your .env file or Streamlit secrets.")
        return False

    try:
        stripe.api_key = api_key
        return True
    except Exception as e:
        print(f"Error initializing Stripe client: {e}")
        return False


def check_stripe_configured() -> bool:
    """
    Check if Stripe is properly configured with credentials.

    Returns:
        bool: True if Stripe is configured, False otherwise
    """
    if not STRIPE_AVAILABLE:
        return False

    return get_stripe_key() is not None


def get_stripe_setup_instructions() -> str:
    """
    Get instructions for setting up Stripe for this project.

    Returns:
        str: Setup instructions
    """
    return """
    # Setting Up Stripe for LitKit
    
    ## Step 1: Create a Stripe Account
    1. Go to https://stripe.com and sign up
    2. Verify your email and complete basic account setup
    
    ## Step 2: Get API Credentials
    1. Go to the Stripe Dashboard > Developers > API keys
    2. Get your test API key (starts with 'sk_test_')
    3. Add these to your .env file or Streamlit secrets:
       ```
       STRIPE_API_KEY_TEST=sk_test_your_test_key
       STRIPE_PUBLISHABLE_KEY_TEST=pk_test_your_test_key
       STRIPE_PAYMENT_MODE=test
       ```
    
    ## Step 3: Create a Product and Price
    1. Go to Products > Create product
    2. Enter a name and description for your product
    3. Add pricing information
    4. Copy the Price ID (starts with 'price_')
    5. Add to your environment variables:
       ```
       STRIPE_PRICE_ID=price_your_price_id
       ```
    
    ## Step 4: Set up Webhook
    Instructions for setting up webhooks will be provided separately.
    """
