"""
Quality Review API Routes

This module defines the API endpoints for quality review functionality.
"""

from fastapi import APIRouter, HTTPException
from ..models.quality_review import QualityReviewRequest, QualityReviewResponse
from ..services.quality_review import QualityReviewService


router = APIRouter()
quality_service = QualityReviewService()


@router.post("/review", response_model=QualityReviewResponse)
async def review_content(request: QualityReviewRequest) -> QualityReviewResponse:
    """
    Perform comprehensive quality review on the provided content.

    Args:
        request: Quality review request containing content and parameters

    Returns:
        Quality review response with scores and improvement suggestions
    """
    try:
        response = quality_service.review_content(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing quality review: {str(e)}")


@router.post("/calculate-metrics")
async def calculate_quality_metrics(content: str) -> dict:
    """
    Calculate all quality metrics for the given content.

    Args:
        content: Content to analyze

    Returns:
        Dictionary containing all quality metrics
    """
    from ..utils.quality_metrics import calculate_quality_metrics
    try:
        metrics = calculate_quality_metrics(content)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating quality metrics: {str(e)}")


@router.post("/clarity-score")
async def get_clarity_score(content: str) -> float:
    """
    Calculate clarity score for the content.

    Args:
        content: Content to analyze

    Returns:
        Clarity score from 0 to 100
    """
    from ..utils.quality_metrics import calculate_clarity_score
    try:
        score = calculate_clarity_score(content)
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating clarity score: {str(e)}")


@router.post("/readability-score")
async def get_readability_score(content: str) -> float:
    """
    Calculate readability score for the content.

    Args:
        content: Content to analyze

    Returns:
        Readability score from 0 to 100
    """
    from ..utils.quality_metrics import calculate_readability_score
    try:
        score = calculate_readability_score(content)
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating readability score: {str(e)}")


@router.post("/engagement-score")
async def get_engagement_score(content: str) -> float:
    """
    Calculate engagement score for the content.

    Args:
        content: Content to analyze

    Returns:
        Engagement score from 0 to 100
    """
    from ..utils.quality_metrics import calculate_engagement_score
    try:
        score = calculate_engagement_score(content)
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating engagement score: {str(e)}")


@router.post("/flow-score")
async def get_flow_score(content: str) -> float:
    """
    Calculate flow score for the content.

    Args:
        content: Content to analyze

    Returns:
        Flow score from 0 to 100
    """
    from ..utils.quality_metrics import calculate_flow_score
    try:
        score = calculate_flow_score(content)
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating flow score: {str(e)}")