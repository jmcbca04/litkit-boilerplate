"""
💳 Subscription Example

This page demonstrates how to implement Stripe subscriptions in your application.
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import litkit modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Try to import the litkit modules
try:
    from litkit.components.auth_ui import login_form
    from litkit.auth.auth import is_authenticated, get_user
    from litkit.components.payments.checkout_ui import checkout_button, pricing_table
    from litkit.components.payments.subscription_ui import (
        subscription_status,
        subscription_required,
        subscription_upsell
    )
    from litkit.payments.stripe_client import (
        check_stripe_configured,
        get_stripe_setup_instructions
    )
    MODULES_LOADED = True
except ImportError as e:
    print(f"Import error: {e}")
    MODULES_LOADED = False

# Set page config
st.set_page_config(
    page_title="LitKit - Subscription Example",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Subscription Example")
st.write("This example demonstrates how to implement Stripe subscriptions in your app")

# Show Stripe configuration status
if MODULES_LOADED:
    with st.expander("Stripe Configuration Status"):
        if check_stripe_configured():
            st.success("✅ Stripe is properly configured!")
        else:
            st.error("❌ Stripe is not configured.")
            st.markdown(get_stripe_setup_instructions())

        # Add webhook setup instructions
        st.subheader("Webhook Setup")
        st.markdown("""
        Webhooks are necessary to receive events from Stripe (like successful payments or subscription updates).
        
        **Follow these steps to set up webhooks:**
        
        1. **Deploy the webhook handler**:
           ```bash
           # Install Supabase CLI if not already installed
           npm install -g supabase
           
           # Login to Supabase
           supabase login
           
           # Link your project
           supabase link --project-ref your-project-ref
           
           # Deploy the webhook function
           supabase functions deploy stripe-webhook --no-verify-jwt
           ```
        
        2. **Configure Stripe webhook endpoint**:
           - In Stripe Dashboard > Developers > Webhooks
           - Add your webhook URL: `https://[your-project-id].supabase.co/functions/v1/stripe-webhook`
           - Add events to listen for: `checkout.session.completed`, `customer.subscription.updated`, etc.
           - Save the webhook signing secret
        
        3. **Set environment variables for the Edge Function**:
           ```bash
           supabase secrets set STRIPE_API_KEY=sk_test_your_key
           supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
           ```
        
        For more details, see the full integration guide in `docs/stripe_integration_guide.md`.
        """)
else:
    st.warning(
        "⚠️ Stripe modules not loaded. This is a simplified example.")

st.markdown("---")

# Authentication section
st.subheader("1. Authentication")
st.write("First, a user needs to be authenticated:")

if not is_authenticated():
    login_form()
else:
    user = get_user()
    st.success(f"👋 Hello, {user.get('email', 'User')}!")

    # Subscription status
    st.subheader("2. Subscription Status")
    subscription_status()

    # Subscription plans
    st.subheader("3. Subscription Plans")
    st.write("Choose a subscription plan:")
    pricing_table()

    # Protected content example
    st.markdown("---")
    st.subheader("4. Protected Content Example")

    tab1, tab2 = st.tabs(["Free Content", "Premium Content"])

    with tab1:
        st.write("This content is freely available to all users.")
        st.info("Free features are limited but still useful.")

    with tab2:
        # This content is only shown if the user has an active subscription
        if subscription_required():
            st.write("Welcome to the premium content!")
            st.success(
                "You're seeing this because you have an active subscription.")
            st.balloons()

    # Non-blocking upsell example
    st.markdown("---")
    st.subheader("5. Non-Blocking Upsell Example")
    st.write("This section shows an upsell message but doesn't block access:")

    subscription_upsell(upsell_text="Upgrade to unlock advanced features!")
    st.write(
        "This content is visible regardless of subscription status, but users are encouraged to upgrade.")

st.info("""
**Note:** This example demonstrates the payment integration scaffolding.

When properly configured with Stripe, this would connect to a real payment system.
""")

# Add a button to go back to home
if st.button("Return to Home"):
    st.switch_page("Home.py")
