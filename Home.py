"""
Simple Streamlit Hello World application.
"""

import streamlit as st
import base64
# Import os if you uncomment the image code below
# import os


def get_base64_of_image(image_file):
    """Get the base64 string of an image file."""
    with open(image_file, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()


def main():
    """Main application function."""
    # Set page config to name the home page
    st.set_page_config(
        page_title="LitKit - Home",
        page_icon="🔥",
        layout="centered"
    )

    # Header
    st.markdown(
        """
        <h1 style='text-align: center;'>LitKit 🔥</h1>
        """,
        unsafe_allow_html=True
    )

    # Hero Section
    # To add a background image or styling:
    # 1. Add your image file to the project directory
    # 2. Modify the CSS below to add your custom styling

    # Create a container with custom styling for the hero section
    with st.container():
        # Apply styling to the container
        st.markdown(
            """
            <style>
            [data-testid="stVerticalBlock"] > div:first-child {
                padding: 3rem;
                border-radius: 10px;
                margin-bottom: 1rem;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Hero content using native Streamlit components
        st.title("The Ultimate Streamlit Boilerplate")
        st.subheader(
            "The comprehensive boilerplate for Streamlit applications with "
            "authentication, payments, UI components, and more."
        )

    st.markdown("---")
    # Features Section
    st.markdown("## Key Features")

    # Define features as a list of dictionaries
    auth_desc_pt1 = ("Secure user authentication with Supabase, "
                     "including")
    auth_desc_pt2 = ("social login options. Easily manage user "
                     "sessions and profiles.")

    db_desc_pt1 = ("Built-in Supabase database integration for "
                   "storing and")
    db_desc_pt2 = ("managing your data. Simple CRUD operations "
                   "and data models.")

    payment_desc = "Stripe integration for payments and subscriptions."

    private_desc = "Role-based access control and content restriction options."

    features = [
        {
            "title": "🔐 Authentication",
            "description": f"{auth_desc_pt1} {auth_desc_pt2}",
            "link": "pages/Auth_Example.py"
        },
        {
            "title": "💾 Database Integration",
            "description": f"{db_desc_pt1} {db_desc_pt2}"
        },
        {
            "title": "🔒 Private Pages",
            "description": private_desc,
            "link": "pages/Private_Page.py"
        },
        {
            "title": "💰 Payments",
            "description": payment_desc,
            "link": "pages/Subscription_Example.py"
        },
        {
            "title": "👤 User Profile",
            "description": "Complete user profile page with account settings, activity tracking, and preferences.",
            "link": "pages/Profile_Page_Example.py"
        }
    ]

    # Display features
    for feature in features:
        st.subheader(feature["title"])
        st.write(feature["description"])

        # Add a page link if available
        if feature.get("link"):
            st.page_link(feature["link"],
                         label=f"View {feature['title']} Example")

        st.markdown("---")  # Divider line

    # Pricing Section
    st.header("Pricing Plans")

    # Define pricing plans
    plans = [
        {
            "name": "Starter",
            "price": "$20",
            "features": [
                "Basic UI components",
                "Documentation access",
                "Community support",
                "1 project"
            ]
        },
        {
            "name": "Pro",
            "price": "$35",
            "features": [
                "All UI components",
                "Authentication included",
                "Database integration",
                "Email support",
                "Unlimited projects"
            ]
        },
        {
            "name": "Premium",
            "price": "$70",
            "features": [
                "All Standard features",
                "Payment processing",
                "Lifetime updates"
            ]
        },
    ]

    # Display pricing plans
    cols = st.columns(len(plans))
    for col, plan in zip(cols, plans):
        with col:
            st.subheader(plan["name"])
            st.markdown(f"{plan['price']}")
            for feature in plan["features"]:
                st.write(f"- {feature}")
            st.button(f"Select {plan['name']}", key=plan["name"])

    # FAQ Section
    st.markdown("<br>", unsafe_allow_html=True)  # Add some space
    st.header("Frequently Asked Questions")

    # Define FAQs as a list of dictionaries
    faqs = [
        {
            "question": "What is LitKit?",
            "answer": "LitKit is a comprehensive boilerplate for Streamlit applications with built-in authentication, database integration, payment processing, and more. It helps you build professional web apps quickly without starting from scratch."
        },
        {
            "question": "How do I get started with LitKit?",
            "answer": "Simply clone the repository, install the requirements with `pip install -r requirements.txt`, and run the app with `streamlit run Home.py`. Detailed documentation is available in the GitHub repository."
        },
        {
            "question": "Does LitKit work with Streamlit 1.43?",
            "answer": "Yes! LitKit is built with Streamlit 1.43 and takes advantage of all the latest features, including improvements to dataframes, timezone handling, and more."
        },
        {
            "question": "Is LitKit suitable for commercial projects?",
            "answer": "Absolutely. LitKit is designed for both personal and commercial use. The pricing plans reflect the level of support and features available for each tier."
        },
        {
            "question": "Can I customize LitKit to fit my needs?",
            "answer": "Yes, LitKit is fully customizable. You can modify any part of the codebase to suit your specific requirements, or use it as a foundation to build upon."
        },
    ]

    # Display FAQs using expander
    for faq in faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])

    # Testimonial Section
    st.markdown("<br>", unsafe_allow_html=True)  # Add some space
    st.header("What Our Users Say")

    # Define testimonials as a list of dictionaries
    testimonials = [
        {
            "name": "Sarah Chen",
            "role": "Data Scientist",
            "company": "Analytics Pro",
            "testimonial": ("LitKit has revolutionized how we create data apps. "
                            "What used to take weeks now takes days.")
        },
        {
            "name": "Marcus Johnson",
            "role": "Machine Learning Engineer",
            "company": "TechSolutions",
            "testimonial": ("The pre-built components and integrations have "
                            "significantly accelerated our development process.")
        },
        {
            "name": "Priya Sharma",
            "role": "Product Manager",
            "company": "DataViz Inc",
            "testimonial": ("An essential tool for anyone building data apps. "
                            "The ROI has been incredible for our team.")
        }
    ]

    # Display testimonials
    cols = st.columns(len(testimonials))
    for col, testimonial in zip(cols, testimonials):
        with col:
            st.markdown("❝")
            st.markdown(f"*\"{testimonial['testimonial']}\"*")
            st.markdown(f"**{testimonial['name']}**")
            st.caption(f"{testimonial['role']} at {testimonial['company']}")

    # Footer
    st.markdown(
        """
        <hr>
        <p style='text-align: center;'>
        🔥 Made with Streamlit
        </p>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
