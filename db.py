from supabase import create_client, Client
from typing import Optional

supabase: Optional[Client] = None  # Declare at module level

def load(supabase_url: str, supabase_key: str) -> None:
    """Load the database connection."""
    global supabase
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("Supabase client initialized.")
    except Exception as e:
        print(f"Failed to initialize Supabase: {e}")
        supabase = None

def get_email() -> Optional[list[str]]:
    """Get the emails from the database."""
    if not supabase:
        print("Supabase client is not initialized.")
        return None

    try:
        response = supabase.table("newsletter_subscriptions").select("email").execute()
        if response.data:
            return [entry["email"] for entry in response.data]
    except Exception as e:
        print(f"Error fetching emails: {e}")
    return None

def set_email(email: str) -> None:
    """Set the email in the database."""
    if not supabase:
        print("Supabase client is not initialized.")
        return

    try:
        supabase.table("newsletter_subscriptions").insert({"email": email}).execute()
        print(f"Email '{email}' inserted successfully.")
    except Exception as e:
        print(f"Error inserting email: {e}")
