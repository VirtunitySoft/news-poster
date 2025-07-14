import dotenv
import os
from typing import Optional

def load(file_path: Optional[str] = None) -> bool:
    """Load environment variables from a .env file."""
    try:
        return dotenv.load_dotenv(dotenv_path=file_path)
    except Exception as e:
        print(f"Failed to load .env file: {e}")
        return False

@staticmethod
def get(key: str) -> any:
    """Get an environment variable, returning a default value if not found."""
    return dotenv.get_key(dotenv.find_dotenv(), key_to_get=key)
    
@staticmethod
def set(key: str, value: str) -> None:
    """Set an environment variable."""
    dotenv.set_key(dotenv.find_dotenv(), key, value)
