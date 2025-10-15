from datetime import datetime, timedelta, timezone
from typing import Dict

from app.core.environment import settings

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to check against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    """
    Create a JWT access token for a given user ID.

    Args:
        user_id (int): The unique identifier of the user for whom the token is generated.

    Returns:
        str: A JWT access token as a string containing the user ID and expiration timestamp.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, object] = {'sub': str(user_id),'exp': int(expire.timestamp())}
    token: str = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token