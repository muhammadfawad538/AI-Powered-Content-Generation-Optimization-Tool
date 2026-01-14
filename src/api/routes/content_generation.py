from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import time
import asyncio
from ...models.content_generation import (
    ContentGenerationRequest,
    ContentGenerationResponse
)
from ...services.content_generation import ContentGenerationService
from ...services.validation import ContentValidationService
from ..middleware.security import validate_api_key
from ...config.settings import settings


router = APIRouter(prefix="/api/v1", tags=["content-generation"])


@router.post("/content/generate", response_model=ContentGenerationResponse)
async def generate_content_route(
    request: ContentGenerationRequest,
    api_key: str = Depends(validate_api_key)
) -> ContentGenerationResponse:
    """
    Generate content based on user-provided parameters including topic, audience, tone, style, format, and length.

    Args:
        request: ContentGenerationRequest with all required parameters
        api_key: Validated API key for authentication

    Returns:
        ContentGenerationResponse with generated content and metadata
    """
    start_time = time.time()

    try:
        # Validate the request using our validation service
        validation_service = ContentValidationService()
        validation_errors = validation_service.validate_content_generation_request(request.dict())

        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid input parameters",
                    "details": validation_errors
                }
            )

        # Create the content generation service
        content_service = ContentGenerationService()

        # Generate the content
        response = await content_service.generate_content(request)

        # Validate the response
        response_issues = validation_service.validate_content_response(response)
        if response_issues:
            # Log the issues but still return the response
            print(f"Response validation issues: {response_issues}")

        # Add generation time to the response if not already set
        if response.generation_time <= 0:
            response.generation_time = round(time.time() - start_time, 2)

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Handle any unexpected errors
        error_time = time.time() - start_time
        error_response = ContentGenerationResponse(
            id=request.id or f"err_{int(time.time())}",
            content="",
            word_count=0,
            quality_score=0.0,
            generation_time=round(error_time, 2),
            status="error",
            feedback=f"Unexpected error: {str(e)}"
        )
        return error_response


@router.post("/content/validate")
async def validate_content_route(
    request: ContentGenerationRequest,
    api_key: str = Depends(validate_api_key)
) -> Dict[str, Any]:
    """
    Validate content generation request without generating content.

    Args:
        request: ContentGenerationRequest to validate
        api_key: Validated API key for authentication

    Returns:
        Dictionary with validation results
    """
    validation_service = ContentValidationService()
    validation_errors = validation_service.validate_content_generation_request(request.dict())

    return {
        "valid": len(validation_errors) == 0,
        "errors": validation_errors
    }


@router.get("/content/providers")
async def get_available_providers(
    api_key: str = Depends(validate_api_key)
) -> Dict[str, Any]:
    """
    Get available LLM providers and their capabilities.

    Args:
        api_key: Validated API key for authentication

    Returns:
        Dictionary with available providers and their details
    """
    providers_info = {
        "providers": [],
        "active_provider": settings.llm_provider
    }

    # Add OpenAI if configured
    if settings.openai_api_key:
        providers_info["providers"].append({
            "name": "openai",
            "configured": True,
            "models": ["gpt-3.5-turbo", "gpt-4"]
        })

    # Add Anthropic if configured
    if settings.anthropic_api_key:
        providers_info["providers"].append({
            "name": "anthropic",
            "configured": True,
            "models": ["claude-3-haiku", "claude-3-sonnet"]
        })

    return providers_info