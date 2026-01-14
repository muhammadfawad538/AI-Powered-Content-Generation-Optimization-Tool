from typing import Any, Dict, List
from pydantic import ValidationError
import re


def validate_topic(topic: str) -> bool:
    """
    Validate the topic field according to specification:
    - Between 5-200 characters
    """
    if not isinstance(topic, str):
        return False
    if len(topic) < 5 or len(topic) > 200:
        return False
    return True


def validate_length(length: int) -> bool:
    """
    Validate the length field according to specification:
    - Between 100-5000 words
    """
    if not isinstance(length, int):
        return False
    if length < 100 or length > 5000:
        return False
    return True


def validate_keywords(keywords: List[str]) -> bool:
    """
    Validate the keywords field according to specification:
    - No more than 10 items
    - Each keyword must be a string
    """
    if not isinstance(keywords, list):
        return False
    if len(keywords) > 10:
        return False
    for keyword in keywords:
        if not isinstance(keyword, str):
            return False
        if len(keyword) > 50:
            return False
    return True


def validate_content_quality(content: str, quality_score: float) -> bool:
    """
    Validate content quality based on quality score
    """
    if not isinstance(content, str) or not isinstance(quality_score, (int, float)):
        return False
    if quality_score < 0.0 or quality_score > 1.0:
        return False
    return True


def validate_generation_time(generation_time: float) -> bool:
    """
    Validate generation time is positive
    """
    if not isinstance(generation_time, (int, float)):
        return False
    if generation_time <= 0:
        return False
    return True


def validate_content_generation_request(request_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate a content generation request and return any validation errors
    """
    errors = {}

    # Validate topic
    if 'topic' not in request_data:
        errors['topic'] = 'Field is required'
    elif not validate_topic(request_data['topic']):
        errors['topic'] = 'Topic must be between 5 and 200 characters'

    # Validate length
    if 'length' not in request_data:
        errors['length'] = 'Field is required'
    elif not validate_length(request_data['length']):
        errors['length'] = 'Must be between 100 and 5000'

    # Validate keywords
    if 'keywords' in request_data and not validate_keywords(request_data['keywords']):
        errors['keywords'] = 'Keywords list must not exceed 10 items and each keyword must be under 50 characters'

    # Validate audience
    if 'audience' not in request_data or not request_data.get('audience'):
        errors['audience'] = 'Audience is required and must be specified from predefined options'

    # Validate tone
    if 'tone' not in request_data or not request_data.get('tone'):
        errors['tone'] = 'Tone is required and must be specified from predefined options'

    # Validate format
    if 'format' not in request_data or not request_data.get('format'):
        errors['format'] = 'Format is required and must be specified from predefined options'

    return errors