"""
👤 Profile Page Example

This page demonstrates a comprehensive user profile page for a SaaS application.
"""

import streamlit as st
import sys
import os
import datetime
import random

# Add parent directory to path to import litkit modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Try to import the litkit modules
try:
    from litkit.components.auth_ui import login_form
    from litkit.auth.auth import is_authenticated, get_user, sign_out
    from litkit.components.payments.subscription_ui import subscription_status
    MODULES_LOADED = True
except ImportError:
    MODULES_LOADED = False

# Set page config
st.set_page_config(
    page_title="LitKit - Profile Page Example",
    page_icon="👤",
    layout="centered"
)

# Development mode - set to True to always show profile content with mock data
# This will be helpful for demonstration purposes
DEV_MODE = True

st.title("👤 Profile Page Example")
st.write("This example demonstrates a comprehensive user profile page for a SaaS app")

st.markdown("---")

# Authentication check - bypass if in development mode
if MODULES_LOADED and not is_authenticated() and not DEV_MODE:
    # Only show login form if modules are loaded, user isn't authenticated, and not in dev mode
    st.warning("Please log in to view your profile")
    login_form()
else:
    # Get user data - either real data if authenticated or mock data
    if MODULES_LOADED and is_authenticated():
        user = get_user()
        email = user.get('email', 'user@example.com')
        name = user.get('user_metadata', {}).get('name', 'Demo User')
    else:
        # Mock user data for demo/development
        user = {
            "id": "user123",
            "email": "demo@example.com",
            "created_at": "2023-01-15T12:00:00Z",
            "last_sign_in_at": "2023-05-20T09:30:00Z"
        }
        email = user["email"]
        name = "Demo User"

        # Show a notice that this is demo data
        st.info("🔍 Viewing profile page in demo mode with mock data")

    # Profile header section with avatar
    col1, col2 = st.columns([1, 3])

    with col1:
        # Profile image
        st.image(
            "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=150", width=120)

    with col2:
        st.subheader(name)
        st.write(f"📧 {email}")
        member_since = datetime.datetime.now() - datetime.timedelta(
            days=random.randint(30, 365))
        st.write(f"🗓️ Member since {member_since.strftime('%B %d, %Y')}")

        # Profile completion indicator
        completion = random.randint(70, 95)
        st.progress(completion/100, text=f"Profile {completion}% complete")

    # Main profile content with tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Account Settings",
        "Subscription",
        "Activity",
        "Preferences"
    ])

    # Tab 1: Account Settings
    with tab1:
        st.subheader("Account Information")

        # Personal information section
        with st.expander("Personal Information", expanded=True):
            with st.form("update_personal_info"):
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("First Name", value="Demo")
                with col2:
                    st.text_input("Last Name", value="User")

                st.text_input("Email Address", value=email)
                st.text_input("Phone Number", value="+1 (555) 123-4567")

                # Profile picture upload
                st.file_uploader("Update Profile Picture",
                                 type=["jpg", "jpeg", "png"])

                st.form_submit_button("Save Changes")

        # Security settings section
        with st.expander("Security Settings"):
            with st.form("update_password"):
                st.text_input("Current Password", type="password")
                st.text_input("New Password", type="password")
                st.text_input("Confirm New Password", type="password")
                st.form_submit_button("Update Password")

            # Security settings for 2FA
            st.subheader("Two-Factor Authentication")
            st.toggle("Enable Two-Factor Authentication", value=True)
            if st.button("Setup 2FA"):
                st.info("In a real app, this would initiate the 2FA setup process.")

            st.subheader("Login Sessions")
            st.markdown("""
            | Device | Location | Last Active |
            | ------ | -------- | ----------- |
            | 🖥️ Windows PC | New York, USA | Just now |
            | 📱 iPhone 14 | New York, USA | 2 days ago |
            """)

            if st.button("Log Out All Devices"):
                st.info("This would log you out of all devices except this one.")

        # Danger zone
        with st.expander("Danger Zone"):
            st.warning("These actions cannot be undone!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Account"):
                    st.error("This would permanently delete your account.")
            with col2:
                if st.button("Download My Data"):
                    st.info("This would download all your data in JSON format.")

    # Tab 2: Subscription Information
    with tab2:
        st.subheader("Your Subscription")

        if MODULES_LOADED:
            # Use actual subscription component if available
            subscription_status()
        else:
            # Mockup subscription display
            st.info("Current Plan: **Premium**")
            st.progress(0.7, text="Next billing cycle: 21 days remaining")

            st.subheader("Billing Information")
            st.markdown("""
            **Payment Method:** Visa ending in 4242
            
            **Billing Address:**  
            123 Main Street  
            New York, NY 10001  
            United States
            """)

            # Billing history
            st.subheader("Billing History")
            st.dataframe({
                "Date": ["2023-05-01", "2023-04-01", "2023-03-01"],
                "Description": ["Premium Plan - Monthly",
                                "Premium Plan - Monthly",
                                "Premium Plan - Monthly"],
                "Amount": ["$70.00", "$70.00", "$70.00"],
                "Status": ["Paid", "Paid", "Paid"]
            })

            col1, col2 = st.columns(2)
            with col1:
                st.button("Upgrade Plan")
            with col2:
                st.button("Cancel Subscription")

    # Tab 3: Activity History
    with tab3:
        st.subheader("Recent Activity")

        # Activity filters
        col1, col2 = st.columns([3, 1])
        with col1:
            st.selectbox("Activity Type", [
                         "All Activities", "Logins", "Data Updates", "Payments", "Settings Changes"])
        with col2:
            st.date_input("From Date", datetime.datetime.now() -
                          datetime.timedelta(days=30))

        # Activity timeline
        activities = [
            {"date": "Today", "time": "09:45 AM", "type": "Login",
             "message": "Logged in from New York, USA"},
            {"date": "Today", "time": "09:47 AM", "type": "Settings",
             "message": "Updated notification preferences"},
            {"date": "Yesterday", "time": "03:12 PM", "type": "Data",
             "message": "Exported project data"},
            {"date": "Yesterday", "time": "11:30 AM", "type": "Payment",
             "message": "Monthly subscription payment processed"},
            {"date": "May 18, 2023", "time": "02:20 PM", "type": "Login",
             "message": "Logged in from new device"},
            {"date": "May 17, 2023", "time": "10:15 AM", "type": "Data",
             "message": "Created new project 'Marketing Campaign'"},
        ]

        for activity in activities:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{activity['date']}**")
                st.write(activity['time'])
            with col2:
                icon = "🔑" if activity['type'] == "Login" else "⚙️" if activity[
                    'type'] == "Settings" else "💾" if activity['type'] == "Data" else "💰"
                st.write(
                    f"{icon} **{activity['type']}**: {activity['message']}")
            st.divider()

        if st.button("Load More Activities"):
            st.info("In a real app, this would load more activities.")

    # Tab 4: Preferences
    with tab4:
        st.subheader("Application Preferences")

        # UI preferences
        with st.expander("Display Settings", expanded=True):
            st.selectbox("Theme", ["Light", "Dark", "System Default"])
            st.selectbox("Default Dashboard View", [
                         "Overview", "Analytics", "Projects", "Custom"])
            st.slider("Items per page", min_value=10,
                      max_value=100, value=25, step=5)

        # Notification settings
        with st.expander("Notification Preferences"):
            st.toggle("Email Notifications", value=True)
            st.toggle("Browser Notifications", value=True)
            st.toggle("Mobile Push Notifications", value=False)

            st.subheader("Notification Types")
            st.checkbox("Account updates", value=True)
            st.checkbox("Security alerts", value=True)
            st.checkbox("Payment reminders", value=True)
            st.checkbox("Product updates", value=True)
            st.checkbox("Marketing emails", value=False)

            if st.button("Save Notification Settings"):
                st.success("Notification preferences saved")

        # Regional settings
        with st.expander("Regional Settings"):
            st.selectbox("Language", [
                         "English (US)", "Spanish", "French", "German", "Japanese", "Chinese (Simplified)"])
            st.selectbox("Time Zone", ["UTC-8 (Pacific Time)", "UTC-5 (Eastern Time)",
                         "UTC+0 (London)", "UTC+1 (Paris)", "UTC+8 (Singapore)"])
            st.selectbox("Date Format", [
                         "MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
            st.selectbox(
                "Currency", ["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)", "CAD (C$)"])

    # Sign out button at bottom
    st.markdown("---")
    if st.button("Sign Out"):
        if MODULES_LOADED and is_authenticated() and not DEV_MODE:
            sign_out()
            st.experimental_rerun()
        else:
            if DEV_MODE:
                st.info("In development mode - sign out functionality is simulated")
            else:
                st.info("In a real app with authentication, this would sign you out")

# Add a button to go back to home
st.markdown("---")
if st.button("Return to Home"):
    st.switch_page("Home.py")
