"""
User data management with Supabase.

This module provides functions for user data operations using Supabase.
"""

from typing import Dict, Any, List, Optional
from ..auth.client import supabase_client


def get_user_data(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user's data from the database.

    Args:
        user_id: The user's ID

    Returns:
        Optional[Dict[str, Any]]: User data if found, None otherwise
    """
    if not supabase_client:
        print("Supabase client is not configured")
        return None

    try:
        # This would actually query the user data from Supabase
        # For the boilerplate, we just return a mock data object
        # response = supabase_client.from_("users").select("*").eq("id", user_id).execute()
        # return response.data[0] if response.data else None

        # Mock user data
        return {
            "id": user_id,
            "email": "demo@example.com",
            "name": "Demo User",
            "created_at": "2023-01-01T00:00:00Z",
            "preferences": {
                "theme": "light",
                "notifications": True
            }
        }
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return None


def update_user_data(user_id: str, data: Dict[str, Any]) -> bool:
    """
    Update a user's data in the database.

    Args:
        user_id: The user's ID
        data: The data to update

    Returns:
        bool: True if update was successful, False otherwise
    """
    if not supabase_client:
        print("Supabase client is not configured")
        return False

    try:
        # This would actually update the user data in Supabase
        # For the boilerplate, we just return success
        # supabase_client.from_("users").update(data).eq("id", user_id).execute()

        print(f"Would update user {user_id} with data: {data}")
        return True
    except Exception as e:
        print(f"Error updating user data: {str(e)}")
        return False


def get_all_users() -> List[Dict[str, Any]]:
    """
    Get all users from the database (admin only).

    Returns:
        List[Dict[str, Any]]: List of all users
    """
    if not supabase_client:
        print("Supabase client is not configured")
        return []

    try:
        # This would actually query all users from Supabase
        # For the boilerplate, we just return mock data
        # response = supabase_client.from_("users").select("*").execute()
        # return response.data if response.data else []

        # Mock users data
        return [
            {
                "id": "user-1",
                "email": "user1@example.com",
                "name": "User One",
                "created_at": "2023-01-01T00:00:00Z"
            },
            {
                "id": "user-2",
                "email": "user2@example.com",
                "name": "User Two",
                "created_at": "2023-01-02T00:00:00Z"
            }
        ]
    except Exception as e:
        print(f"Error fetching all users: {str(e)}")
        return []


def delete_user(user_id: str) -> bool:
    """
    Delete a user from the database.

    Args:
        user_id: The user's ID

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    if not supabase_client:
        print("Supabase client is not configured")
        return False

    try:
        # This would actually delete the user from Supabase
        # For the boilerplate, we just return success
        # supabase_client.from_("users").delete().eq("id", user_id).execute()

        print(f"Would delete user {user_id}")
        return True
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return False
