# 🔥 LitKit - The Ultimate Streamlit Boilerplate

LitKit is a comprehensive boilerplate for Streamlit applications. It enables users to build and launch Streamlit apps quickly with pre-built functionalities like authentication, payments, and UI components.

## Features

- **User Authentication** - OAuth integration with Supabase
- **UI Component Library** - Ready-to-use Streamlit components
- **Database Integration** - Built-in Supabase connection
- **Payment Processing** - Stripe integration for subscriptions and payments

## Getting Started

### Prerequisites

- Python 3.8+
- [Supabase](https://supabase.com) account (for authentication & database)
- [Stripe](https://stripe.com) account (for payment processing)
- Streamlit Community Cloud account (optional for deployment)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/jmcbca04/litkit-boilerplate.git
cd litkit-boilerplate
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env file with your credentials
```

5. Run the application:

```bash
streamlit run Home.py
```

## Setting Up Your Own Project

### 1. Configure Authentication (Supabase)

1. Create an account on [Supabase](https://supabase.com)
2. Create a new project
3. Get your API URL and API Key from Project Settings > API
4. Add these credentials to your `.env` file:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```
5. Enable the authentication providers you want in Supabase dashboard (Email, Google, GitHub, etc.)

### 2. Configure Database (Supabase)

1. In your Supabase project, create any tables you need for your application
2. The boilerplate already includes database connections and basic CRUD operations
3. Modify the database models in `litkit/database/` to match your schema

### 3. Configure Payments (Stripe)

1. Create an account on [Stripe](https://stripe.com)
2. Get your API keys from the Stripe Dashboard
3. Add these credentials to your `.env` file:
   ```
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   ```
4. Create your products and price plans in the Stripe Dashboard
5. Update the pricing plans in the app to match your Stripe products

### 4. Customize the UI

1. Modify `Home.py` to update the landing page content
2. Add your own pages in the `pages/` directory
3. Update styles and branding to match your project
4. Look at the example pages to understand the structure

### 5. Deploy Your App

1. Push your code to GitHub
2. Sign up for [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Set up your environment variables
5. Deploy!

## Limitations and Known Issues

- Error handling is minimal - you may want to add more robust error handling for production
- Security features are basic - add additional security measures for sensitive applications
- Performance optimization may be needed for large-scale applications

## Project Structure

```
litkit-boilerplate/
├── Home.py                     # Main landing page
├── pages/                      # Additional pages
│   ├── Auth_Example.py         # Authentication demo
│   ├── Private_Page.py         # Role-based access example
│   ├── Profile_Page_Example.py # User profile example
│   └── Subscription_Example.py # Payment integration example
├── litkit/                     # Core package
│   ├── auth/                   # Authentication functions
│   ├── database/               # Database connectors
│   ├── ui/                     # UI utilities
│   ├── components/             # UI components
│   └── utils/                  # Utility functions
└── .env.example                # Example environment variables
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- Inspired by [ShipFast](https://shipfa.st/)
- Built with [Streamlit](https://streamlit.io/)
