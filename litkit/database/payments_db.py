"""
Payment and subscription database operations.

This module provides functions for managing payment and subscription data in Supabase.
"""

from typing import Dict, Any, Optional, List
import streamlit as st
from datetime import datetime, timezone
from ..auth.client import supabase_client


def get_user_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get the subscription details for a user from the database.

    Args:
        user_id: Supabase user ID

    Returns:
        Optional[Dict[str, Any]]: Subscription details or None if not found
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return None

    try:
        # Query the subscriptions table for the user's subscription
        response = supabase_client.table("subscriptions").select(
            "*").eq("user_id", user_id).execute()

        # Return the most recent subscription (if any)
        subs = response.data
        if subs and len(subs) > 0:
            # Sort by created_at descending to get the most recent
            return sorted(subs, key=lambda x: x.get("created_at", ""), reverse=True)[0]

        return None
    except Exception as e:
        st.error(f"Error fetching subscription: {str(e)}")
        return None


def create_subscription(
    user_id: str,
    stripe_customer_id: str,
    stripe_subscription_id: str,
    status: str,
    price_id: str,
    current_period_start: datetime,
    current_period_end: datetime
) -> Optional[Dict[str, Any]]:
    """
    Create a new subscription record in the database.

    Args:
        user_id: Supabase user ID
        stripe_customer_id: Stripe customer ID
        stripe_subscription_id: Stripe subscription ID
        status: Subscription status (active, canceled, etc.)
        price_id: Stripe price ID
        current_period_start: Start date of the current period
        current_period_end: End date of the current period

    Returns:
        Optional[Dict[str, Any]]: Created subscription record or None on error
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return None

    try:
        # Format dates as ISO strings
        period_start = current_period_start.isoformat()
        period_end = current_period_end.isoformat()

        # Create the subscription record
        data = {
            "user_id": user_id,
            "stripe_customer_id": stripe_customer_id,
            "stripe_subscription_id": stripe_subscription_id,
            "status": status,
            "price_id": price_id,
            "current_period_start": period_start,
            "current_period_end": period_end,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        response = supabase_client.table(
            "subscriptions").insert(data).execute()

        if response.data and len(response.data) > 0:
            return response.data[0]

        return None
    except Exception as e:
        st.error(f"Error creating subscription: {str(e)}")
        return None


def update_subscription_status(
    subscription_id: str,
    status: str,
    current_period_end: Optional[datetime] = None
) -> bool:
    """
    Update the status of a subscription.

    Args:
        subscription_id: Stripe subscription ID
        status: New subscription status
        current_period_end: New end date of the current period

    Returns:
        bool: True if update was successful, False otherwise
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return False

    try:
        # Prepare the update data
        data = {
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        # Add current_period_end if provided
        if current_period_end:
            data["current_period_end"] = current_period_end.isoformat()

        # Update the subscription
        response = supabase_client.table("subscriptions") \
            .update(data) \
            .eq("stripe_subscription_id", subscription_id) \
            .execute()

        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error updating subscription: {str(e)}")
        return False


def cancel_subscription(subscription_id: str) -> bool:
    """
    Mark a subscription as canceled in the database.

    Args:
        subscription_id: Stripe subscription ID

    Returns:
        bool: True if cancellation was successful, False otherwise
    """
    return update_subscription_status(subscription_id, "canceled")


def has_active_subscription(user_id: str) -> bool:
    """
    Check if a user has an active subscription.

    Args:
        user_id: Supabase user ID

    Returns:
        bool: True if the user has an active subscription, False otherwise
    """
    subscription = get_user_subscription(user_id)
    if not subscription:
        return False

    # Check if status is active
    if subscription.get("status") != "active":
        return False

    # Check if subscription has expired
    current_period_end = subscription.get("current_period_end")
    if current_period_end:
        try:
            end_date = datetime.fromisoformat(
                current_period_end.replace("Z", "+00:00"))
            return end_date > datetime.now(timezone.utc)
        except (ValueError, TypeError):
            # If we can't parse the date, assume it's not active
            return False

    return True


# Credit system functions (if using a credit-based model)

def get_user_credits(user_id: str) -> int:
    """
    Get the current credit balance for a user.

    Args:
        user_id: Supabase user ID

    Returns:
        int: Number of credits available, or 0 if error or no credits
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return 0

    try:
        # Query the credits table for the user
        response = supabase_client.table("credits").select(
            "amount").eq("user_id", user_id).execute()

        credits = response.data
        if credits and len(credits) > 0:
            return credits[0].get("amount", 0)

        # If no record exists, create one with 0 credits
        create_data = {
            "user_id": user_id,
            "amount": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        supabase_client.table("credits").insert(create_data).execute()

        return 0
    except Exception as e:
        st.error(f"Error getting credits: {str(e)}")
        return 0


def add_credits(user_id: str, amount: int) -> int:
    """
    Add credits to a user's account.

    Args:
        user_id: Supabase user ID
        amount: Number of credits to add

    Returns:
        int: New credit balance, or -1 on error
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return -1

    try:
        # Get current credits
        current_credits = get_user_credits(user_id)

        # Calculate new amount
        new_amount = current_credits + amount

        # Update the credits record
        data = {
            "amount": new_amount,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        response = supabase_client.table("credits") \
            .update(data) \
            .eq("user_id", user_id) \
            .execute()

        if response.data and len(response.data) > 0:
            return response.data[0].get("amount", 0)

        return -1
    except Exception as e:
        st.error(f"Error adding credits: {str(e)}")
        return -1


def use_credits(user_id: str, amount: int) -> bool:
    """
    Use credits from a user's account if they have enough.

    Args:
        user_id: Supabase user ID
        amount: Number of credits to use

    Returns:
        bool: True if credits were successfully used, False otherwise
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return False

    try:
        # Get current credits
        current_credits = get_user_credits(user_id)

        # Check if user has enough credits
        if current_credits < amount:
            return False

        # Calculate new amount
        new_amount = current_credits - amount

        # Update the credits record
        data = {
            "amount": new_amount,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        response = supabase_client.table("credits") \
            .update(data) \
            .eq("user_id", user_id) \
            .execute()

        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error using credits: {str(e)}")
        return False


def create_payment_record(
    user_id: str,
    stripe_checkout_id: str,
    amount: int,
    currency: str,
    status: str,
    payment_type: str = "one-time"
) -> Optional[Dict[str, Any]]:
    """
    Create a payment record in the database.

    Args:
        user_id: Supabase user ID
        stripe_checkout_id: Stripe checkout session ID
        amount: Payment amount (in cents)
        currency: Currency code (e.g., "usd")
        status: Payment status (e.g., "succeeded", "failed")
        payment_type: Type of payment ("one-time" or "subscription")

    Returns:
        Optional[Dict[str, Any]]: Created payment record or None on error
    """
    if not supabase_client:
        st.warning("Supabase client is not configured.")
        return None

    try:
        # Create the payment record
        data = {
            "user_id": user_id,
            "stripe_checkout_id": stripe_checkout_id,
            "amount": amount,
            "currency": currency,
            "status": status,
            "payment_type": payment_type,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        response = supabase_client.table("payments").insert(data).execute()

        if response.data and len(response.data) > 0:
            return response.data[0]

        return None
    except Exception as e:
        st.error(f"Error creating payment record: {str(e)}")
        return None
