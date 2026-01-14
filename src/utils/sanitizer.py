import html
import re
from typing import Union, List, Dict, Any


def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent XSS and other injection attacks
    """
    if not isinstance(text, str):
        return ""

    # Remove potentially dangerous characters/sequences
    sanitized = html.escape(text)

    # Remove any potential script tags (case-insensitive)
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'<iframe[^>]*>.*?</iframe>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'<object[^>]*>.*?</object>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'<embed[^>]*>.*?</embed>', '', sanitized, flags=re.IGNORECASE)

    # Remove javascript: and data: URIs
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'data:', '', sanitized, flags=re.IGNORECASE)

    return sanitized.strip()


def sanitize_keywords(keywords: List[str]) -> List[str]:
    """
    Sanitize a list of keywords
    """
    if not isinstance(keywords, list):
        return []

    sanitized_keywords = []
    for keyword in keywords:
        if isinstance(keyword, str):
            sanitized_keyword = sanitize_input(keyword)
            if sanitized_keyword:  # Only add non-empty keywords
                sanitized_keywords.append(sanitized_keyword)

    return sanitized_keywords


def sanitize_content(content: str) -> str:
    """
    Sanitize generated content to prevent XSS
    """
    return sanitize_input(content)


def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively sanitize dictionary values
    """
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized_data[key] = sanitize_input(value)
        elif isinstance(value, list):
            # Handle list of strings
            if all(isinstance(item, str) for item in value):
                sanitized_data[key] = sanitize_keywords(value)
            else:
                sanitized_data[key] = value  # Leave other types as-is
        elif isinstance(value, dict):
            sanitized_data[key] = sanitize_dict(value)
        else:
            sanitized_data[key] = value

    return sanitized_data


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing
    """
    if not isinstance(text, str):
        return ""

    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing
    """
    if not isinstance(text, str):
        return ""

    # Clean the text first
    cleaned = clean_text(text)

    # Additional normalization can be added here
    return cleaned