"""
Supabase client configuration.

This module sets up the connection to Supabase for authentication and database access.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Load Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Optional[Client]:
    """
    Create and return a Supabase client instance.

    Returns:
        Optional[Client]: A Supabase client instance or None if credentials are missing.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Warning: Supabase credentials not found in environment variables.")
        print("Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
        return None

    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None


# Singleton client instance
supabase_client = get_supabase_client()
