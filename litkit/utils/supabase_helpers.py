"""
Utility functions for Supabase operations.

This module provides helper functions for working with Supabase.
"""

import os
from typing import Dict, Any, Optional
import json
import streamlit as st
from ..auth.client import supabase_client


def check_supabase_configured() -> bool:
    """
    Check if Supabase is properly configured with credentials.

    Returns:
        bool: True if Supabase is configured, False otherwise
    """
    return (
        os.getenv("SUPABASE_URL") is not None and
        os.getenv("SUPABASE_KEY") is not None and
        supabase_client is not None
    )


def get_supabase_configuration_status() -> Dict[str, Any]:
    """
    Get the status of the Supabase configuration.

    Returns:
        Dict[str, Any]: Status information
    """
    url_configured = os.getenv("SUPABASE_URL") is not None
    key_configured = os.getenv("SUPABASE_KEY") is not None
    client_initialized = supabase_client is not None

    return {
        "url_configured": url_configured,
        "key_configured": key_configured,
        "client_initialized": client_initialized,
        "fully_configured": url_configured and key_configured and client_initialized
    }


def display_supabase_configuration_status():
    """
    Display the Supabase configuration status in Streamlit.
    """
    status = get_supabase_configuration_status()

    st.subheader("Supabase Configuration Status")

    if status["fully_configured"]:
        st.success("✅ Supabase is fully configured")
    else:
        st.error("❌ Supabase is not fully configured")

    st.write("Configuration details:")
    st.json(json.dumps({
        "URL Configured": "✅" if status["url_configured"] else "❌",
        "API Key Configured": "✅" if status["key_configured"] else "❌",
        "Client Initialized": "✅" if status["client_initialized"] else "❌"
    }))

    if not status["fully_configured"]:
        st.info("""
        To configure Supabase:
        1. Sign up at https://supabase.com
        2. Create a new project
        3. Go to Project Settings > API
        4. Copy the URL and anon/public key
        5. Add them to your .env file:
           ```
           SUPABASE_URL=your-project-url
           SUPABASE_KEY=your-anon-key
           ```
        6. Restart your application
        """)


def create_supabase_tables() -> bool:
    """
    Create the necessary tables in Supabase (for setup).
    This would typically be run once during project setup.

    Returns:
        bool: True if successful, False otherwise
    """
    if not supabase_client:
        return False

    try:
        # In a real implementation, this would create tables via SQL
        # For the boilerplate, we just print the SQL that would be executed

        users_table_sql = """
        create table public.profiles (
            id uuid references auth.users on delete cascade not null primary key,
            email text not null,
            name text,
            avatar_url text,
            created_at timestamp with time zone default now() not null,
            updated_at timestamp with time zone default now() not null
        );

        -- Set up Row Level Security (RLS)
        alter table public.profiles enable row level security;

        -- Create policies
        create policy "Users can view their own profile" 
        on public.profiles for select 
        using (auth.uid() = id);

        create policy "Users can update their own profile" 
        on public.profiles for update 
        using (auth.uid() = id);
        """

        print("Would execute SQL:")
        print(users_table_sql)

        return True
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        return False


def get_supabase_setup_instructions() -> str:
    """
    Get instructions for setting up Supabase for this project.

    Returns:
        str: Setup instructions
    """
    return """
    # Setting Up Supabase for LitKit
    
    ## Step 1: Create a Supabase Account
    1. Go to https://supabase.com and sign up
    2. Create a new organization if needed
    
    ## Step 2: Create a New Project
    1. Click 'New Project'
    2. Enter a name for your project
    3. Set a secure database password
    4. Choose a region close to your users
    5. Click 'Create Project'
    
    ## Step 3: Get API Credentials
    1. Once your project is created, go to Project Settings > API
    2. Copy the 'Project URL' and 'anon/public' key
    3. Add these to your .env file:
       ```
       SUPABASE_URL=your-project-url
       SUPABASE_KEY=your-anon-key
       ```
    
    ## Step 4: Set Up Authentication
    1. Go to Authentication > Settings
    2. Under 'Site URL', enter your application URL (e.g., http://localhost:8501)
    3. Under 'Redirect URLs', add your redirect URL (e.g., http://localhost:8501)
    4. Save changes
    
    ## Step 5: Enable Social Providers (Optional)
    1. Go to Authentication > Providers
    2. Enable and configure any providers you want (Google, GitHub, etc.)
    
    ## Step 6: Create Database Tables
    1. Go to SQL Editor
    2. Create the necessary tables using SQL or the provided utility function
    
    ## Step 7: Test the Connection
    1. Restart your LitKit application
    2. Verify the connection status shows "Fully Configured"
    """
