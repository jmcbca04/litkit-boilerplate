# Stripe Integration Guide for LitKit

This guide explains how to set up and use Stripe integration with your LitKit application for subscriptions and payments.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Stripe Project Setup](#stripe-project-setup)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Webhook Setup](#webhook-setup)
7. [Integration with Your App](#integration-with-your-app)
8. [Subscription Management](#subscription-management)
9. [Credit-Based Payment System](#credit-based-payment-system)
10. [Testing](#testing)
11. [Troubleshooting](#troubleshooting)

## Introduction

LitKit includes built-in support for payment processing using [Stripe](https://stripe.com), a popular payment processing platform. The integration allows you to:

- Implement subscription-based access to your app
- Offer one-time payments for credits or products
- Securely process payments
- Track subscription status and payment history
- Implement credit-based payment systems

## Prerequisites

- A Stripe account (free to sign up, you only pay when processing real payments)
- Supabase account already set up (see Supabase Authentication Guide)
- LitKit boilerplate installed and running
- Basic understanding of Streamlit and Supabase

## Stripe Project Setup

1. **Create a Stripe Account**

   - Go to [https://stripe.com](https://stripe.com) and sign up
   - Complete the registration process

2. **Set Up Your Stripe Dashboard**

   - Navigate to the Stripe Dashboard
   - Make sure you're in Test Mode for development (toggle at the top right)

3. **Create Products and Prices**

   - Go to Products > Create Product
   - Enter a name, description, and other details
   - Add a price (either one-time or recurring subscription)
   - Copy the Price ID (starts with `price_`) for use in your app

4. **Get API Keys**
   - In the Stripe Dashboard, go to Developers > API keys
   - Copy the Publishable key and Secret key
   - Note: There are separate sets of keys for test mode and live mode

## Configuration

1. **Environment Variables**

   Add the following to your `.env` file or Streamlit secrets:

   ```
   # Stripe configuration
   STRIPE_API_KEY_TEST=sk_test_your_test_key
   STRIPE_API_KEY=sk_live_your_live_key  # Only for production
   STRIPE_PUBLISHABLE_KEY_TEST=pk_test_your_test_key
   STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key  # Only for production
   STRIPE_PRICE_ID=price_your_price_id
   STRIPE_SUCCESS_URL=http://localhost:8501/payment_success
   STRIPE_CANCEL_URL=http://localhost:8501/payment_cancel
   STRIPE_PAYMENT_MODE=test  # Change to 'live' for production
   ```

2. **Test vs. Live Mode**

   During development, always use test mode. Stripe provides test card numbers that you can use without processing actual payments. Switch to live mode only when your app is ready for production.

## Database Setup

LitKit's Stripe integration requires several tables in your Supabase database:

1. **Create the Database Tables**

   Run the SQL scripts provided in the `sql/stripe/` directory:

   - `subscriptions_table.sql` - For subscription data
   - `credits_table.sql` - For credit balances (if using credit system)
   - `payments_table.sql` - For payment history

   You can run these scripts in the Supabase SQL Editor.

2. **Database Schema**

   The integration sets up the following tables:

   - `subscriptions` - Tracks subscription status, expiration, etc.
   - `credits` - Tracks user credit balances (optional)
   - `payments` - Records payment history

## Webhook Setup

Webhooks are crucial for Stripe integration as they allow Stripe to notify your app about events (payments, subscription updates, etc.).

1. **Set Up Supabase Edge Function**

   LitKit includes a ready-to-deploy Edge Function for handling Stripe webhooks:

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

2. **Get the Webhook URL**

   After deployment, get your webhook URL from the Supabase dashboard:
   `https://[your-project-id].supabase.co/functions/v1/stripe-webhook`

3. **Configure Webhook in Stripe**

   - Go to Stripe Dashboard > Developers > Webhooks
   - Click "Add endpoint"
   - Enter your webhook URL
   - Select events to listen for (at minimum: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_succeeded`)
   - Copy the Signing Secret (starts with `whsec_`)

4. **Configure Edge Function Environment Variables**

   ```bash
   # Set the Stripe API key and webhook secret
   supabase secrets set STRIPE_API_KEY=sk_test_your_test_key
   supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
   ```

## Integration with Your App

LitKit provides several components to integrate Stripe payments into your app:

1. **Import Required Modules**

   ```python
   from litkit.components.payments.checkout_ui import checkout_button, pricing_table
   from litkit.components.payments.subscription_ui import subscription_status, subscription_required
   ```

2. **Display a Pricing Table**

   ```python
   pricing_table(
       show_checkout_buttons=True,
       button_text="Subscribe",
       highlight_color="#FF4B4B"
   )
   ```

3. **Add a Checkout Button**

   ```python
   checkout_button(
       text="Subscribe Now",
       price_id="price_your_price_id",  # Optional, will use STRIPE_PRICE_ID from env if not provided
       mode="subscription",  # or "payment" for one-time
       button_type="primary"
   )
   ```

4. **Check Subscription Status**

   ```python
   subscription_status()  # Display current subscription status
   ```

5. **Protect Content with Subscription Check**

   ```python
   if subscription_required():
       st.write("This is premium content only visible to subscribers!")
   ```

## Subscription Management

LitKit provides functions for managing subscriptions:

1. **Check Subscription Status**

   ```python
   from litkit.payments.subscription import has_active_subscription
   from litkit.auth.auth import get_user

   user = get_user()
   if has_active_subscription(user.get("id")):
       st.success("You have an active subscription!")
   ```

2. **Display Subscription Details**

   ```python
   from litkit.database.payments_db import get_user_subscription

   user = get_user()
   subscription = get_user_subscription(user.get("id"))
   if subscription:
       st.write(f"Status: {subscription.get('status')}")
       st.write(f"Renews: {subscription.get('current_period_end')}")
   ```

## Credit-Based Payment System

If you're using a credit-based system:

1. **Display User Credits**

   ```python
   from litkit.database.payments_db import get_user_credits

   user = get_user()
   credits = get_user_credits(user.get("id"))
   st.metric("Credits", str(credits))
   ```

2. **Use Credits**

   ```python
   from litkit.database.payments_db import use_credits

   user = get_user()
   if use_credits(user.get("id"), 1):  # Use 1 credit
       st.success("Credit used successfully!")
       # Perform the action that costs credits
   else:
       st.error("Not enough credits!")
   ```

3. **Sell Credits**

   ```python
   checkout_button(
       text="Buy 10 Credits",
       price_id="price_your_credits_price_id",
       mode="payment",
       quantity=1
   )
   ```

## Testing

1. **Test Cards**

   Stripe provides test card numbers for testing:

   - `4242 4242 4242 4242` - Successful payment
   - `4000 0000 0000 0002` - Card declined
   - Use any future expiration date and any 3-digit CVC

2. **Testing Webhooks Locally**

   To test webhooks during local development:

   - Use [Stripe CLI](https://stripe.com/docs/stripe-cli) to forward events
   - Or deploy your webhook handler to Supabase and use that URL

## Troubleshooting

### Common Issues

1. **Webhook Events Not Received**

   - Verify the webhook URL is correct
   - Check that you've registered for the correct events
   - Ensure the webhook secret is set correctly

2. **Subscription Status Not Updating**

   - Check webhook logs in the Supabase dashboard
   - Verify that the database tables are properly set up
   - Ensure your Edge Function has the correct permissions

3. **Payments Not Working**
   - Make sure you're using the correct API keys
   - Check that your Price IDs are correct
   - Verify the product exists in your Stripe dashboard

### Checking Configuration

You can check the configuration status in your app:

```python
from litkit.payments.stripe_client import check_stripe_configured

if check_stripe_configured():
    st.success("Stripe is properly configured!")
else:
    st.error("Stripe is not configured correctly.")
```

---

For more detailed information, refer to the [Stripe API documentation](https://stripe.com/docs/api) and [Supabase Edge Functions documentation](https://supabase.com/docs/guides/functions).
