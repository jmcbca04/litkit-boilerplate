# Supabase Authentication Guide for LitKit

This guide explains how to set up and use Supabase authentication with your LitKit application.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Supabase Project Setup](#supabase-project-setup)
4. [Configuration](#configuration)
5. [Using Authentication](#using-authentication)
6. [Social Logins](#social-logins)
7. [Protected Content](#protected-content)
8. [Database Integration](#database-integration)
9. [Troubleshooting](#troubleshooting)

## Introduction

LitKit includes built-in support for user authentication using [Supabase](https://supabase.com), an open-source Firebase alternative. The authentication system in LitKit allows you to:

- Register and login users with email/password
- Implement social logins (Google, GitHub, etc.)
- Reset passwords
- Protect content based on authentication status
- Store and retrieve user data

## Prerequisites

- A Supabase account (free tier is sufficient to start)
- LitKit boilerplate installed and running
- Basic understanding of Python and Streamlit

## Supabase Project Setup

1. **Create a Supabase Account**

   - Go to [https://supabase.com](https://supabase.com) and sign up or log in

2. **Create a New Project**

   - Click "New Project"
   - Enter a name for your project
   - Set a secure database password
   - Choose a region close to your users
   - Click "Create Project"

3. **Get API Credentials**
   - Once your project is created, go to Project Settings > API
   - Copy the "Project URL" and "anon/public" key

## Configuration

1. **Environment Variables**

   - Create a `.env` file in your project root (or copy from `.env.example`)
   - Add your Supabase credentials:

   ```
   SUPABASE_URL=your-project-url
   SUPABASE_KEY=your-anon-key
   ```

2. **Authentication Settings**

   - In your Supabase dashboard, go to Authentication > Settings
   - Under "Site URL," enter your application URL (e.g., http://localhost:8501)
   - Under "Redirect URLs," add your redirect URL (e.g., http://localhost:8501)
   - Save changes

3. **Database Setup**
   - The profiles table is created automatically when users sign up
   - You can add additional tables as needed for your application

## Using Authentication

LitKit provides several functions and components for authentication:

### Basic Authentication Flow

```python
from litkit.components.auth_ui import login_form, signup_form
from litkit.auth.auth import is_authenticated, get_user

# Check if user is authenticated
if is_authenticated():
    user = get_user()
    st.write(f"Welcome, {user['email']}!")
else:
    # Show login form
    if login_form():
        st.experimental_rerun()  # Refresh the page after login
```

### Sign Up

```python
from litkit.components.auth_ui import signup_form

if signup_form():
    st.success("Account created! You can now log in.")
```

### Password Reset

```python
from litkit.components.auth_ui import reset_password_form

reset_password_form()
```

### Sign Out

```python
from litkit.auth.auth import sign_out

if st.button("Sign Out"):
    sign_out()
    st.experimental_rerun()  # Refresh the page after logout
```

## Social Logins

To enable social logins:

1. In your Supabase dashboard, go to Authentication > Providers
2. Enable and configure the providers you want (Google, GitHub, etc.)
3. Add the OAuth client ID and secret for each provider
4. Use the social login buttons component:

```python
from litkit.components.auth_ui import social_login_buttons

social_login_buttons()
```

## Protected Content

You can protect content using the `auth_required` decorator or by checking `is_authenticated()`:

```python
from litkit.components.auth_ui import auth_required
from litkit.auth.auth import is_authenticated

# Using decorator
@auth_required
def protected_content():
    st.write("This content is only visible to logged-in users.")

# Using conditional check
if is_authenticated():
    st.write("This content is only visible to logged-in users.")
else:
    st.warning("Please log in to view this content.")
```

## Database Integration

LitKit includes functions for working with user data in the database:

```python
from litkit.database.users import get_user_data, update_user_data

# Get user data
user_id = get_user()["id"]
user_data = get_user_data(user_id)

# Update user data
update_user_data(user_id, {"name": "New Name"})
```

## Troubleshooting

### Common Issues

1. **Authentication not working**

   - Check your environment variables
   - Verify Supabase project settings
   - Check redirect URLs in Supabase dashboard

2. **Social logins fail**

   - Verify OAuth credentials
   - Check callback URLs

3. **User data not saving**
   - Check database permissions
   - Verify table structure

### Checking Configuration

Use the Supabase configuration status tool to check your setup:

```python
from litkit.utils.supabase_helpers import display_supabase_configuration_status

display_supabase_configuration_status()
```

### Example Application

Refer to the `examples/auth_example.py` file for a complete implementation of authentication. Run it with:

```bash
streamlit run examples/auth_example.py
```

---

This guide covers the basics of working with Supabase authentication in LitKit. For more advanced use cases, refer to the [Supabase documentation](https://supabase.com/docs) and the [Streamlit documentation](https://docs.streamlit.io/).
