# 🔥 LitKit - The Ultimate Streamlit Boilerplate

LitKit is a comprehensive boilerplate for Streamlit applications. It enables users to build and launch Streamlit apps quickly with pre-built functionalities like authentication, payments, and UI components.

## Features

- **User Authentication** - OAuth integration with Supabase
- **UI Component Library** - Ready-to-use Streamlit components
- **Database Integration** - Built-in Supabase connection
- **Payment Processing** - Stripe integration (coming soon)

## Getting Started

### Prerequisites

- Python 3.8+
- Supabase account
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
# Edit .env file with your Supabase credentials
```

5. Run the application:

```bash
streamlit run Home.py
```

## Project Structure

```
litkit-boilerplate/
├── litkit/                     # Core package
│   ├── auth/                   # Authentication functions
│   ├── database/               # Database connectors
│   ├── ui/                     # UI utilities
│   ├── components/             # UI components
│   └── utils/                  # Utility functions
├── examples/                   # Example applications
├── docs/                       # Documentation
└── tests/                      # Test suite
```

## Acknowledgments

- Inspired by [ShipFast](https://shipfa.st/)
- Built with [Streamlit](https://streamlit.io/)
