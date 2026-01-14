import time
import asyncio
from typing import Optional
from ..models.content_generation import (
    ContentGenerationRequest,
    ContentGenerationResponse,
    AudienceEnum,
    ToneEnum,
    StyleEnum,
    FormatEnum
)
from .llm_integration import get_llm_provider, LLMProvider
from ..utils.validators import validate_content_quality, validate_generation_time
from ..utils.sanitizer import sanitize_content


class ContentGenerationService:
    """Service class for handling content generation operations"""

    def __init__(self):
        self.llm_provider: LLMProvider = get_llm_provider()

    async def generate_content(
        self,
        request: ContentGenerationRequest
    ) -> ContentGenerationResponse:
        """
        Generate content based on the provided request parameters

        Args:
            request: ContentGenerationRequest with topic, audience, tone, etc.

        Returns:
            ContentGenerationResponse with generated content and metadata
        """
        start_time = time.time()

        try:
            # Generate content using the LLM provider
            raw_content = await self.llm_provider.generate_content(request)

            # Sanitize the generated content
            content = sanitize_content(raw_content)

            # Calculate metrics
            word_count = len(content.split())
            generation_time = time.time() - start_time

            # Calculate a basic quality score (could be enhanced with more sophisticated methods)
            quality_score = self._calculate_quality_score(content, request)

            # Validate the content and generation time
            if not validate_content_quality(content, quality_score):
                raise ValueError("Generated content does not meet quality standards")

            if not validate_generation_time(generation_time):
                raise ValueError("Generation time validation failed")

            # Create and return the response
            response = ContentGenerationResponse(
                id=request.id or f"gen_{int(time.time())}",
                content=content,
                word_count=word_count,
                quality_score=quality_score,
                generation_time=round(generation_time, 2),
                status="success",
                feedback=None
            )

            return response

        except Exception as e:
            # Handle any errors during content generation
            generation_time = time.time() - start_time

            error_response = ContentGenerationResponse(
                id=request.id or f"gen_{int(time.time())}",
                content="",
                word_count=0,
                quality_score=0.0,
                generation_time=round(generation_time, 2),
                status="error",
                feedback=f"Error generating content: {str(e)}"
            )

            return error_response

    def _calculate_quality_score(
        self,
        content: str,
        request: ContentGenerationRequest
    ) -> float:
        """
        Calculate a basic quality score for the generated content
        This is a simplified implementation - in a real system this could be more sophisticated
        """
        score = 0.5  # Start with a neutral score

        # Check if content is substantial
        if len(content) > 50:
            score += 0.2

        # Check if content somewhat matches the requested length (within 20%)
        requested_length = request.length
        actual_length = len(content.split())
        length_ratio = actual_length / requested_length if requested_length > 0 else 1
        if 0.8 <= length_ratio <= 1.2:
            score += 0.15

        # Check if keywords were included (if specified)
        if request.keywords:
            content_lower = content.lower()
            included_keywords = sum(1 for kw in request.keywords if kw.lower() in content_lower)
            if included_keywords > 0:
                keyword_score = included_keywords / len(request.keywords) * 0.15
                score += keyword_score

        # Ensure score stays within bounds
        return max(0.0, min(1.0, score))

    async def estimate_generation_time(
        self,
        request: ContentGenerationRequest
    ) -> float:
        """
        Estimate the time it will take to generate content
        This is a placeholder implementation
        """
        # Base time plus time proportional to requested length
        base_time = 1.0  # seconds
        time_per_word = 0.01  # seconds per word
        estimated_time = base_time + (request.length * time_per_word)
        return min(estimated_time, 30.0)  # Cap at 30 seconds