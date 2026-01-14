"""
Research API Routes

This module defines the API endpoints for research assistance functionality.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from ...models.research_result import (
    ResearchRequest, ResearchResponse,
    CredibilityCheckRequest, CredibilityCheckResponse
)
from ...services.research_assistance import ResearchAssistanceService
from ..middleware.security import validate_api_key


router = APIRouter()
research_service = ResearchAssistanceService()


@router.post("/conduct-research", response_model=ResearchResponse)
async def conduct_research(
    request: ResearchRequest,
    api_key: str = Depends(validate_api_key)
) -> ResearchResponse:
    """
    Conduct research based on the provided query.

    Args:
        request: Research request containing query parameters
        api_key: Validated API key for authentication

    Returns:
        Research response with results
    """
    from ..middleware.security import api_logger
    from ..utils.logging_config import log_api_call
    import time

    start_time = time.time()
    try:
        # Validate request
        from ...services.validation import ContentValidationService
        validation_service = ContentValidationService()
        validation_errors = validation_service.validate_research_request(request)

        if validation_errors:
            api_logger.warning(f"Research request validation failed: {validation_errors}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid input parameters",
                    "details": validation_errors
                }
            )

        response = await research_service.conduct_research(request)

        # Log successful API call
        duration = (time.time() - start_time) * 1000
        log_api_call(
            api_logger,
            "/api/v1/research/conduct-research",
            "POST",
            request_data={"content_id": request.content_id, "query_text": request.query.query_text},
            response_status=200,
            duration_ms=duration
        )

        return response
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        api_logger.error(f"Error conducting research: {str(e)}")
        log_api_call(
            api_logger,
            "/api/v1/research/conduct-research",
            "POST",
            response_status=500,
            duration_ms=duration
        )
        raise HTTPException(status_code=500, detail=f"Error conducting research: {str(e)}")


@router.post("/check-credibility", response_model=CredibilityCheckResponse)
async def check_source_credibility(
    request: CredibilityCheckRequest,
    api_key: str = Depends(validate_api_key)
) -> CredibilityCheckResponse:
    """
    Check credibility of specific sources.

    Args:
        request: Request containing URLs to check
        api_key: Validated API key for authentication

    Returns:
        Response with credibility assessments
    """
    try:
        response = await research_service.check_source_credibility(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking credibility: {str(e)}")


@router.get("/health")
async def research_health_check():
    """
    Health check endpoint for research service.

    Returns:
        Health status of the research service
    """
    return {
        "status": "healthy",
        "service": "research-assistance",
        "message": "Research service is operational"
    }


@router.post("/validate-query")
async def validate_research_query(
    query_text: str,
    target_domains: list = [],
    api_key: str = Depends(validate_api_key)
) -> Dict[str, bool]:
    """
    Validate a research query before execution.

    Args:
        query_text: Query text to validate
        target_domains: Target domains for validation
        api_key: Validated API key for authentication

    Returns:
        Validation result
    """
    try:
        # Basic validation
        if not query_text or len(query_text.strip()) < 3:
            return {"valid": False, "error": "Query must be at least 3 characters long"}

        if len(target_domains) > 10:
            return {"valid": False, "error": "Too many target domains (max 10)"}

        # Additional validation could go here
        return {"valid": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating query: {str(e)}")