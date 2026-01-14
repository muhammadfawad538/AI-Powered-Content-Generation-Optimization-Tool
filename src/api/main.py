from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import time
import asyncio
from ..models.content_generation import (
    ContentGenerationRequest,
    ContentGenerationResponse
)
from ..services.content_generation import ContentGenerationService
from ..services.validation import ContentValidationService
from .middleware.security import validate_api_key, bearer_scheme
from ..config.settings import settings


# Initialize FastAPI app
app = FastAPI(
    title="AI Content Generation API",
    description="API for generating high-quality, SEO-optimized content using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Content Generation API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "config": {
            "debug": settings.debug,
            "llm_provider": settings.llm_provider,
            "rate_limit_requests": settings.rate_limit_requests,
            "content_length_limit": settings.content_length_limit
        }
    }


@app.post("/api/v1/content/generate", response_model=ContentGenerationResponse)
async def generate_content(
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

        # Add generation time to the response
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


@app.post("/api/v1/content/validate")
async def validate_content(
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


# Initialize services when the app starts up
@app.on_event("startup")
async def startup_event():
    print("Starting up AI Content Generation API...")
    if settings.debug:
        print(f"Debug mode enabled, using LLM provider: {settings.llm_provider}")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down AI Content Generation API...")


# Include routes
from .routes import content_generation, seo_analysis, quality_review, ethics_review, research, export, workflow, analytics, insights
app.include_router(content_generation.router, prefix="/api/v1/content", tags=["content-generation"])
app.include_router(seo_analysis.router, prefix="/api/v1/seo", tags=["seo-analysis"])
app.include_router(quality_review.router, prefix="/api/v1/quality", tags=["quality-review"])
app.include_router(ethics_review.router, prefix="/api/v1/ethics", tags=["ethics-review"])
app.include_router(research.router, prefix="/api/v1/research", tags=["research-assistance"])
app.include_router(export.router, prefix="/api/v1/export", tags=["export-management"])
app.include_router(workflow.router, prefix="/api/v1/workflow", tags=["workflow-orchestration"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics-insights"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights-recommendations"])