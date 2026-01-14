from typing import Dict, Any, List
from ..models.content_generation import (
    ContentGenerationRequest,
    ContentGenerationResponse,
    AudienceEnum,
    ToneEnum,
    StyleEnum,
    FormatEnum
)
from ..models.research_result import ResearchRequest
from ..utils.validators import validate_content_generation_request
from ..utils.sanitizer import sanitize_dict
import re


class ContentValidationService:
    """Service class for validating content and requests"""

    @staticmethod
    def validate_content_generation_request(request_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate a content generation request and return any validation errors

        Args:
            request_data: Dictionary containing the request parameters

        Returns:
            Dictionary of validation errors, with field names as keys and error messages as values
        """
        # Sanitize the input data first
        sanitized_data = sanitize_dict(request_data)

        # Use the validator utility to perform the actual validation
        validation_errors = validate_content_generation_request(sanitized_data)

        return validation_errors

    @staticmethod
    def validate_generated_content(content: str, request: ContentGenerationRequest) -> List[str]:
        """
        Validate the generated content against the original request parameters

        Args:
            content: The generated content string
            request: The original ContentGenerationRequest

        Returns:
            List of validation issues found
        """
        issues = []

        if not content:
            issues.append("Generated content is empty")
            return issues

        # Check content length against requested length (within tolerance)
        content_words = len(content.split())
        length_tolerance = request.length * 0.2  # 20% tolerance
        if abs(content_words - request.length) > length_tolerance:
            issues.append(f"Content length ({content_words} words) differs significantly from requested length ({request.length} words)")

        # Check if specified keywords are present (if any were requested)
        if request.keywords:
            content_lower = content.lower()
            missing_keywords = [kw for kw in request.keywords if kw.lower() not in content_lower]
            if missing_keywords:
                issues.append(f"Missing requested keywords: {', '.join(missing_keywords)}")

        # Check for basic quality metrics
        if len(content) < 50:
            issues.append("Generated content is too short to be meaningful")

        # Check for repetitive content (simple heuristic)
        words = content.split()
        unique_words = set(words)
        if len(unique_words) / len(words) < 0.5:  # Less than 50% unique words
            issues.append("Content appears to have excessive repetition")

        # Check for common problematic patterns
        if re.search(r'(duplicate|repeated|filler)', content, re.IGNORECASE):
            issues.append("Content contains potential filler or duplicate text")

        return issues

    @staticmethod
    def validate_content_response(response: ContentGenerationResponse) -> List[str]:
        """
        Validate a content generation response

        Args:
            response: ContentGenerationResponse to validate

        Returns:
            List of validation issues found
        """
        issues = []

        if not response.id:
            issues.append("Response ID is missing")

        if response.status == "success" and not response.content:
            issues.append("Successful response has empty content")

        if response.quality_score < 0.0 or response.quality_score > 1.0:
            issues.append(f"Quality score {response.quality_score} is outside valid range [0.0, 1.0]")

        if response.generation_time <= 0:
            issues.append(f"Generation time {response.generation_time} is not positive")

        if response.word_count < 0:
            issues.append(f"Word count {response.word_count} is negative")

        return issues

    @staticmethod
    def assess_content_ethics(content: str) -> Dict[str, Any]:
        """
        Perform basic ethical assessment of content

        Args:
            content: Content to assess

        Returns:
            Dictionary with ethical assessment results
        """
        assessment = {
            "has_potential_issues": False,
            "issues_found": [],
            "confidence": 0.0
        }

        # Look for potential ethical issues
        content_lower = content.lower()

        # Check for hate speech indicators
        hate_indicators = [
            "hate", "attack", "destroy", "kill", "harm", "threaten", "violence"
        ]
        potential_hate = [indicator for indicator in hate_indicators if indicator in content_lower]

        if potential_hate:
            assessment["has_potential_issues"] = True
            assessment["issues_found"].extend([f"Potential hate speech indicator: {indicator}" for indicator in potential_hate])

        # Check for discriminatory language
        discrimination_indicators = [
            "discriminate", "inferior", "superior", "race", "racist", "bigotry", "prejudice"
        ]
        potential_discrimination = [indicator for indicator in discrimination_indicators if indicator in content_lower]

        if potential_discrimination:
            assessment["has_potential_issues"] = True
            assessment["issues_found"].extend([f"Potential discrimination indicator: {indicator}" for indicator in potential_discrimination])

        # Set confidence based on number of issues found
        assessment["confidence"] = min(len(assessment["issues_found"]) * 0.2, 1.0)

        return assessment

    @staticmethod
    def validate_research_request(request: ResearchRequest) -> Dict[str, str]:
        """
        Validate a research request and return any validation errors.

        Args:
            request: ResearchRequest to validate

        Returns:
            Dictionary of validation errors, with field names as keys and error messages as values
        """
        errors = {}

        # Validate content ID
        if not request.content_id or len(request.content_id.strip()) == 0:
            errors["content_id"] = "Content ID is required"

        # Validate query text
        if not request.query.query_text or len(request.query.query_text.strip()) < 3:
            errors["query_text"] = "Query text must be at least 3 characters long"

        if len(request.query.query_text) > 500:
            errors["query_text"] = "Query text is too long (max 500 characters)"

        # Validate max results
        if request.query.max_results < 1 or request.query.max_results > 100:
            errors["max_results"] = "Max results must be between 1 and 100"

        # Validate target domains
        if len(request.query.target_domains) > 20:
            errors["target_domains"] = "Too many target domains (max 20 allowed)"

        # Validate research purpose
        if not request.query.research_purpose or len(request.query.research_purpose.strip()) < 5:
            errors["research_purpose"] = "Research purpose must be at least 5 characters long"

        return errors

    @staticmethod
    def validate_analytics_request(request: AnalyticsQuery) -> Dict[str, str]:
        """
        Validate an analytics query request and return any validation errors.

        Args:
            request: AnalyticsQuery to validate

        Returns:
            Dictionary of validation errors, with field names as keys and error messages as values
        """
        errors = {}

        # Validate date range
        if request.date_range_start and request.date_range_end:
            if request.date_range_start > request.date_range_end:
                errors["date_range"] = "Start date must be before end date"

        # Validate limit
        if request.limit < 1 or request.limit > 1000:
            errors["limit"] = "Limit must be between 1 and 1000"

        # Validate offset
        if request.offset < 0:
            errors["offset"] = "Offset must be non-negative"

        # Validate content IDs if provided
        if request.content_ids and len(request.content_ids) > 100:
            errors["content_ids"] = "Too many content IDs (max 100 allowed)"

        # Validate metric types if provided
        if hasattr(request, 'metric_types') and getattr(request, 'metric_types', None):
            from ..models.analytics import AnalyticsDataTypeEnum
            valid_types = [item.value for item in AnalyticsDataTypeEnum]
            for metric_type in request.metric_types:
                if metric_type not in valid_types:
                    errors["metric_types"] = f"Invalid metric type: {metric_type}"

        # Validate source channels if provided
        if hasattr(request, 'source_channels') and getattr(request, 'source_channels', None):
            from ..models.analytics import ContentChannelEnum
            valid_channels = [item.value for item in ContentChannelEnum]
            for channel in request.source_channels:
                if channel not in valid_channels:
                    errors["source_channels"] = f"Invalid source channel: {channel}"

        return errors

    @staticmethod
    def validate_insights_request(request: InsightsQuery) -> Dict[str, str]:
        """
        Validate an insights query request and return any validation errors.

        Args:
            request: InsightsQuery to validate

        Returns:
            Dictionary of validation errors, with field names as keys and error messages as values
        """
        errors = {}

        # Validate content IDs if provided
        if request.content_ids and len(request.content_ids) > 100:
            errors["content_ids"] = "Too many content IDs (max 100 allowed)"

        # Validate date range
        if request.date_range_start and request.date_range_end:
            if request.date_range_start > request.date_range_end:
                errors["date_range"] = "Start date must be before end date"

        # Validate significance threshold
        if request.min_significance < 0.0 or request.min_significance > 1.0:
            errors["min_significance"] = "Minimum significance must be between 0.0 and 1.0"

        # Validate confidence threshold
        if request.min_confidence < 0.0 or request.min_confidence > 1.0:
            errors["min_confidence"] = "Minimum confidence must be between 0.0 and 1.0"

        # Validate limit
        if request.limit < 1 or request.limit > 500:
            errors["limit"] = "Limit must be between 1 and 500"

        # Validate offset
        if request.offset < 0:
            errors["offset"] = "Offset must be non-negative"

        # Validate categories if provided
        if request.categories:
            from ..models.insights import InsightCategoryEnum
            valid_categories = [item.value for item in InsightCategoryEnum]
            for category in request.categories:
                if category not in valid_categories:
                    errors["categories"] = f"Invalid category: {category}"

        return errors