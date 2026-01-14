"""
SEO Analysis API Routes

This module defines the API endpoints for SEO analysis functionality.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
from ..models.seo_analysis import SEOAnalysisRequest, SEOAnalysisResponse
from ..services.seo_analysis import SEOAnalysisService


router = APIRouter()
seo_service = SEOAnalysisService()


@router.post("/analyze", response_model=SEOAnalysisResponse)
async def analyze_content(request: SEOAnalysisRequest) -> SEOAnalysisResponse:
    """
    Perform comprehensive SEO analysis on the provided content.

    Args:
        request: SEO analysis request containing content and parameters

    Returns:
        SEO analysis response with metrics and suggestions
    """
    try:
        response = seo_service.analyze_content(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing SEO analysis: {str(e)}")


@router.post("/keyword-density")
async def calculate_keyword_density(content: str, keywords: list) -> Dict[str, float]:
    """
    Calculate keyword density for specific keywords in content.

    Args:
        content: Content to analyze
        keywords: List of keywords to calculate density for

    Returns:
        Dictionary mapping keywords to their density percentages
    """
    from ..utils.seo_metrics import calculate_keyword_density
    try:
        density_results = calculate_keyword_density(content, keywords)
        return density_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating keyword density: {str(e)}")


@router.post("/analyze-heading-structure")
async def analyze_heading_structure(content: str) -> Dict[str, int]:
    """
    Analyze the heading structure of the content.

    Args:
        content: Content to analyze

    Returns:
        Dictionary mapping heading levels to their count
    """
    from ..utils.seo_metrics import analyze_heading_structure
    try:
        heading_results = analyze_heading_structure(content)
        return heading_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing heading structure: {str(e)}")


@router.post("/calculate-seo-score")
async def calculate_seo_score(
    keyword_density: Dict[str, float],
    readability_score: float,
    heading_structure: Dict[str, int],
    recommended_keywords: list,
    improvement_suggestions: list
) -> float:
    """
    Calculate an overall SEO score based on multiple factors.

    Args:
        keyword_density: Dictionary of keyword densities
        readability_score: Readability score
        heading_structure: Heading structure analysis
        recommended_keywords: List of recommended keywords
        improvement_suggestions: List of improvement suggestions

    Returns:
        SEO score from 0 to 100
    """
    from ..utils.seo_metrics import calculate_seo_score
    try:
        score = calculate_seo_score(
            keyword_density,
            readability_score,
            heading_structure,
            recommended_keywords,
            improvement_suggestions
        )
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating SEO score: {str(e)}")