"""
Stripe checkout UI components.

This module provides UI components for Stripe checkout.
"""

import streamlit as st
from typing import Optional, Callable
from ...payments.checkout import create_checkout_session
from ...payments.subscription import get_subscription_plans
from ...auth.auth import is_authenticated, get_user


def checkout_button(
    text: str = "Subscribe Now",
    price_id: Optional[str] = None,
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
    mode: str = "subscription",
    quantity: int = 1,
    button_type: str = "primary",
    use_container_width: bool = True,
    color: Optional[str] = None,
    on_click: Optional[Callable] = None,
    key: Optional[str] = None
) -> bool:
    """
    Display a button that redirects to Stripe checkout.

    Args:
        text: Button text
        price_id: Stripe Price ID (optional, will use env var if not provided)
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect after cancelled payment
        mode: 'subscription' or 'payment'
        quantity: Number of items to purchase
        button_type: Streamlit button type ('primary', 'secondary')
        use_container_width: Whether to use the full container width
        color: Custom button color
        on_click: Function to call when button is clicked
        key: Unique key for the button

    Returns:
        bool: True if button was clicked
    """
    # Check if user is authenticated
    if not is_authenticated():
        st.warning("Please log in to subscribe.")
        return False

    # Get user email for checkout
    user = get_user()
    user_email = user.get("email") if user else None

    # Add custom CSS for button if color is provided
    if color:
        button_style = f"""
        <style>
        div[data-testid="stButton"] > button[kind="{button_type}"] {{
            background-color: {color};
            border-color: {color};
        }}
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)

    # Display the button
    button_clicked = st.button(
        text,
        type=button_type,
        on_click=on_click,
        use_container_width=use_container_width,
        key=key or "stripe_checkout_button"
    )

    if button_clicked:
        # Create checkout session
        checkout_url = create_checkout_session(
            user_email=user_email,
            success_url=success_url,
            cancel_url=cancel_url,
            price_id=price_id,
            quantity=quantity,
            mode=mode
        )

        if checkout_url:
            # Redirect to checkout
            st.markdown(
                f'<meta http-equiv="refresh" content="0;URL=\'{checkout_url}\'">', unsafe_allow_html=True)
            st.info(f"Redirecting to Stripe checkout...")

    return button_clicked


def pricing_table(
    show_checkout_buttons: bool = True,
    button_text: str = "Subscribe",
    highlight_color: str = "#FF4B4B"
):
    """
    Display a pricing table with subscription options.

    Args:
        show_checkout_buttons: Whether to show checkout buttons
        button_text: Text for checkout buttons
        highlight_color: Color for highlighted plan and buttons
    """
    plans = get_subscription_plans()

    # Display the plans in columns
    cols = st.columns(len(plans))

    for i, plan in enumerate(plans):
        with cols[i]:
            # Apply highlighting styles
            if plan.get("highlighted", False):
                st.markdown(f"""
                <div style="
                    border: 2px solid {highlight_color};
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    height: 100%;
                ">
                    <h3>{plan['name']}</h3>
                    <p>{plan['description']}</p>
                    <h2>{plan['price']}</h2>
                    <ul style="text-align: left;">
                        {''.join([f'<li>{feature}</li>' for feature in plan['features']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    height: 100%;
                ">
                    <h3>{plan['name']}</h3>
                    <p>{plan['description']}</p>
                    <h2>{plan['price']}</h2>
                    <ul style="text-align: left;">
                        {''.join([f'<li>{feature}</li>' for feature in plan['features']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # Add checkout button if enabled
            if show_checkout_buttons:
                checkout_button(
                    text=button_text,
                    price_id=plan.get('price_id'),
                    color=highlight_color if plan.get(
                        "highlighted", False) else None,
                    key=f"checkout_button_{plan['id']}"
                )
