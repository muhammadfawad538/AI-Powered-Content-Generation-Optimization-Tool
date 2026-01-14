from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import time
from collections import defaultdict, deque
from ..config.settings import settings


class RateLimiter:
    """Simple rate limiter to prevent abuse of the API"""

    def __init__(self):
        # Store request timestamps for each API key
        self.requests = defaultdict(deque)

    def is_allowed(self, api_key: str) -> bool:
        """
        Check if the API key is allowed to make a request

        Args:
            api_key: The API key making the request

        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()
        window_start = now - settings.rate_limit_window

        # Remove old requests outside the time window
        while self.requests[api_key] and self.requests[api_key][0] < window_start:
            self.requests[api_key].popleft()

        # Check if we've exceeded the rate limit
        if len(self.requests[api_key]) >= settings.rate_limit_requests:
            return False

        # Add the current request
        self.requests[api_key].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


class APIKeyValidator:
    """Validate API keys against stored keys"""

    def __init__(self):
        # In a real application, these would come from a secure storage
        # For now, we'll use the API keys from settings
        self.valid_keys = set()
        if settings.openai_api_key:
            self.valid_keys.add(settings.openai_api_key)
        if settings.anthropic_api_key:
            self.valid_keys.add(settings.anthropic_api_key)

    def is_valid(self, api_key: str) -> bool:
        """Check if the provided API key is valid"""
        return api_key in self.valid_keys


async def validate_api_key(credentials: HTTPAuthorizationCredentials = None):
    """
    Dependency to validate API key

    Args:
        credentials: HTTP authorization credentials

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key in Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    validator = APIKeyValidator()
    if not validator.is_valid(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check rate limit
    if not rate_limiter.is_allowed(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

    return credentials.credentials


# Initialize the security components
api_key_validator = APIKeyValidator()
bearer_scheme = HTTPBearer(auto_error=False)