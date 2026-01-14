"""
Workflow Helper Utilities

This module provides utility functions for workflow management,
caching, and state management for the content generation and optimization workflows.
"""

import json
import pickle
from typing import Any, Dict, Optional, Union
from datetime import datetime, timedelta
from enum import Enum


class WorkflowStatus(Enum):
    """Enumeration of possible workflow statuses."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowCache:
    """Simple cache utility for workflow-related data."""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize the workflow cache.

        Args:
            ttl_seconds: Time-to-live in seconds for cached items
        """
        self.ttl_seconds = ttl_seconds
        self._cache = {}

    def set(self, key: str, value: Any, ttl_override: Optional[int] = None) -> bool:
        """
        Set a value in the cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl_override: Override default TTL

        Returns:
            True if successful, False otherwise
        """
        ttl = ttl_override or self.ttl_seconds
        expiry = datetime.now() + timedelta(seconds=ttl)

        try:
            # Try to serialize the value to ensure it can be cached
            serialized_value = pickle.dumps(value)
            self._cache[key] = {
                'value': serialized_value,
                'expiry': expiry
            }
            return True
        except Exception:
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            return None

        item = self._cache[key]
        if datetime.now() > item['expiry']:
            del self._cache[key]
            return None

        try:
            return pickle.loads(item['value'])
        except Exception:
            del self._cache[key]
            return None

    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear_expired(self):
        """Remove all expired items from the cache."""
        current_time = datetime.now()
        expired_keys = [
            key for key, item in self._cache.items()
            if current_time > item['expiry']
        ]

        for key in expired_keys:
            del self._cache[key]


def generate_workflow_id() -> str:
    """
    Generate a unique workflow ID.

    Returns:
        Unique workflow identifier
    """
    import uuid
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_part = str(uuid.uuid4())[:8]
    return f"wf_{timestamp}_{random_part}"


def validate_workflow_step(step_data: Dict[str, Any]) -> bool:
    """
    Validate workflow step data.

    Args:
        step_data: Dictionary containing step information

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['step_id', 'step_type', 'input_data']
    return all(field in step_data for field in required_fields)


def format_export_content(content: str, format_type: str) -> str:
    """
    Format content for specific export types.

    Args:
        content: Original content to format
        format_type: Target format ('blog', 'social_media', 'ad_campaign', etc.)

    Returns:
        Formatted content string
    """
    if format_type == 'blog':
        # Format for blog posts
        lines = content.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                # Add proper spacing for blog readability
                formatted_lines.append(line.strip())
                formatted_lines.append('')  # Add blank line between paragraphs
            else:
                formatted_lines.append('')
        return '\n'.join(formatted_lines).strip()

    elif format_type == 'social_media':
        # Format for social media (shorter, punchier)
        # Limit length and add hashtags
        content = content[:280]  # Twitter character limit
        return content

    elif format_type == 'ad_campaign':
        # Format for ad campaigns (focused headline + description)
        sentences = content.split('. ')
        if len(sentences) > 2:
            # Take first sentence as headline, rest as description
            headline = sentences[0][:150]  # Headline limit
            description = '. '.join(sentences[1:])[:300]  # Description limit
            return f"Headline: {headline}\nDescription: {description}"

    return content  # Return original if no specific formatting needed


def sanitize_content_for_platform(content: str, platform: str) -> str:
    """
    Sanitize content for specific platform requirements.

    Args:
        content: Content to sanitize
        platform: Target platform ('twitter', 'facebook', 'wordpress', etc.)

    Returns:
        Sanitized content string
    """
    if platform in ['twitter', 'linkedin']:
        # Remove potentially problematic content for social platforms
        sanitized = content.replace('@everyone', '@ everyone')  # Prevent pings
        sanitized = sanitized.replace('<script', '&lt;script')  # Prevent XSS
        return sanitized

    elif platform == 'wordpress':
        # WordPress-specific sanitization
        sanitized = content.replace('<?', '&lt;?')  # Prevent PHP execution
        sanitized = sanitized.replace('?>', '?&gt;')
        return sanitized

    return content


def calculate_workflow_progress(current_step: int, total_steps: int) -> float:
    """
    Calculate workflow progress percentage.

    Args:
        current_step: Current step number (1-indexed)
        total_steps: Total number of steps

    Returns:
        Progress percentage as float (0.0-100.0)
    """
    if total_steps <= 0:
        return 0.0
    return min(100.0, (current_step / total_steps) * 100.0)