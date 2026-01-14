"""
Insights API Routes

This module defines the API endpoints for insights and recommendations functionality.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ...models.insights import (
    ContentInsightsResponse, InsightsQuery, InsightsValidationRequest,
    InsightsValidationResponse, PersonalizationProfile, TrendAnalysis,
    ComparativeAnalysis, PredictiveInsight, InsightCategoryEnum,
    RecommendationPriorityEnum, TrendDirectionEnum
)
from ...models.analytics import ContentPerformance, EngagementMetrics, SEOEffectiveness
from ...services.insights_service import InsightsService
from ...services.validation import ContentValidationService
from ..middleware.security import validate_api_key
from ...utils.logging_config import api_logger


router = APIRouter()
insights_service = InsightsService()
validation_service = ContentValidationService()


@router.post("/generate-insights", response_model=ContentInsightsResponse)
async def generate_content_insights(
    content_id: str,
    include_performance: bool = Query(True),
    include_engagement: bool = Query(True),
    include_seo: bool = Query(True),
    api_key: str = Depends(validate_api_key)
) -> ContentInsightsResponse:
    """
    Generate insights for a specific content item based on its performance data.

    Args:
        content_id: Identifier of the content to analyze
        include_performance: Whether to include performance data analysis
        include_engagement: Whether to include engagement data analysis
        include_seo: Whether to include SEO data analysis
        api_key: Validated API key for authentication

    Returns:
        ContentInsightsResponse with insights and recommendations
    """
    try:
        # In a real implementation, we would fetch the actual performance data
        # For now, we'll pass None to generate insights with simulated data
        performance_data = None
        engagement_data = None
        seo_data = None

        if include_performance:
            # Simulate performance data
            performance_data = ContentPerformance(
                content_id=content_id,
                views=1000 + hash(content_id) % 500,
                unique_visitors=800 + hash(content_id) % 400,
                engagement_rate=2.5 + (hash(content_id) % 10) / 10,
                conversion_rate=1.8 + (hash(content_id) % 5) / 10,
                revenue=500.0 + (hash(content_id) % 500),
                source_channel="website",
                date_recorded=datetime.utcnow()
            )

        if include_engagement:
            # Simulate engagement data
            engagement_data = EngagementMetrics(
                content_id=content_id,
                likes=50 + hash(content_id) % 100,
                shares=10 + hash(content_id) % 50,
                comments=20 + hash(content_id) % 60,
                saves=5 + hash(content_id) % 20,
                engagement_rate=3.0 + (hash(content_id) % 15) / 10,
                source_channel="website",
                date_recorded=datetime.utcnow()
            )

        if include_seo:
            # Simulate SEO data
            seo_data = SEOEffectiveness(
                content_id=content_id,
                keyword_rankings={"seo": 15, "content": 8, "marketing": 22},
                organic_traffic=300 + hash(content_id) % 700,
                impressions=2000 + hash(content_id) % 3000,
                backlinks=15 + hash(content_id) % 35,
                overall_seo_score=75.0 + (hash(content_id) % 25),
                source_channel="website",
                date_recorded=datetime.utcnow()
            )

        result = await insights_service.generate_content_insights(
            content_id=content_id,
            performance_data=performance_data,
            engagement_data=engagement_data,
            seo_data=seo_data
        )

        # Log successful insight generation
        api_logger.info(f"Generated {len(result.insights)} insights and {len(result.recommendations)} recommendations for content {content_id}")

        return result
    except Exception as e:
        api_logger.error(f"Error generating content insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating content insights: {str(e)}")


@router.post("/query-insights", response_model=ContentInsightsResponse)
async def query_insights(
    request: InsightsQuery,
    api_key: str = Depends(validate_api_key)
) -> ContentInsightsResponse:
    """
    Query insights and recommendations based on specified parameters.

    Args:
        request: Insights query parameters
        api_key: Validated API key for authentication

    Returns:
        ContentInsightsResponse with query results
    """
    try:
        # Validate the query request
        validation_errors = validation_service.validate_analytics_request(request)
        if validation_errors:
            raise HTTPException(status_code=400, detail=validation_errors)

        result = await insights_service.query_insights(request)

        # Log successful query
        api_logger.info(f"Insights query executed: {len(result.insights)} insights, {len(result.recommendations)} recommendations")

        return result
    except Exception as e:
        api_logger.error(f"Error querying insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying insights: {str(e)}")


@router.post("/trend-analysis", response_model=List[TrendAnalysis])
async def analyze_trends(
    content_ids: List[str] = Query(..., min_items=1),
    metric_type: str = Query("views", regex="^(views|engagement_rate|organic_traffic|revenue|conversions)$"),
    days_back: int = Query(30, ge=1, le=365),
    api_key: str = Depends(validate_api_key)
) -> List[TrendAnalysis]:
    """
    Analyze trends for content performance metrics.

    Args:
        content_ids: List of content IDs to analyze
        metric_type: Type of metric to analyze
        days_back: Number of days to look back for trend analysis (default 30, max 365)
        api_key: Validated API key for authentication

    Returns:
        List of trend analysis results
    """
    try:
        result = await insights_service.analyze_trends(
            content_ids=content_ids,
            metric_type=metric_type,
            days_back=days_back
        )

        # Log successful analysis
        api_logger.info(f"Trend analysis completed for {len(content_ids)} content items, metric: {metric_type}")

        return result
    except Exception as e:
        api_logger.error(f"Error analyzing trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing trends: {str(e)}")


@router.post("/personalized-recommendations")
async def generate_personalized_recommendations(
    user_profile: PersonalizationProfile,
    content_ids: List[str] = Query(..., min_items=1),
    api_key: str = Depends(validate_api_key)
) -> List[Dict[str, Any]]:
    """
    Generate personalized recommendations based on user preferences.

    Args:
        user_profile: User's personalization profile
        content_ids: List of content IDs to generate recommendations for
        api_key: Validated API key for authentication

    Returns:
        List of personalized recommendations
    """
    try:
        result = await insights_service.generate_personalized_recommendations(
            user_profile=user_profile,
            content_ids=content_ids
        )

        # Log successful generation
        api_logger.info(f"Generated {len(result)} personalized recommendations for user {user_profile.user_id}")

        return [rec.dict() for rec in result]
    except Exception as e:
        api_logger.error(f"Error generating personalized recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating personalized recommendations: {str(e)}")


@router.post("/validate-insights", response_model=InsightsValidationResponse)
async def validate_insights_data(
    request: InsightsValidationRequest,
    api_key: str = Depends(validate_api_key)
) -> InsightsValidationResponse:
    """
    Validate insights and recommendations data.

    Args:
        request: Insights validation request
        api_key: Validated API key for authentication

    Returns:
        InsightsValidationResponse with validation results
    """
    try:
        result = await insights_service.validate_insights_data(request)

        # Log validation result
        api_logger.info(f"Insights data validation for {request.content_id}: {'VALID' if result.is_valid else 'INVALID'}")

        return result
    except Exception as e:
        api_logger.error(f"Error validating insights data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error validating insights data: {str(e)}")


@router.post("/comparative-analysis", response_model=ComparativeAnalysis)
async def perform_comparative_analysis(
    content_ids: List[str] = Query(..., min_items=2, max_items=10),
    comparison_basis: str = Query("engagement", regex="^(engagement|views|seo|performance|revenue)$"),
    api_key: str = Depends(validate_api_key)
) -> ComparativeAnalysis:
    """
    Perform comparative analysis between multiple content pieces.

    Args:
        content_ids: List of content IDs to compare (min 2, max 10)
        comparison_basis: Basis for comparison (engagement, views, SEO, etc.)
        api_key: Validated API key for authentication

    Returns:
        ComparativeAnalysis with comparison results
    """
    try:
        result = await insights_service.perform_comparative_analysis(
            content_ids=content_ids,
            comparison_basis=comparison_basis
        )

        # Log successful analysis
        api_logger.info(f"Comparative analysis completed for {len(content_ids)} content items, basis: {comparison_basis}")

        return result
    except Exception as e:
        api_logger.error(f"Error performing comparative analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error performing comparative analysis: {str(e)}")


@router.post("/predictive-insights")
async def generate_predictive_insights(
    content_id: str,
    prediction_type: str = Query("engagement", regex="^(engagement|traffic|revenue|performance)$"),
    prediction_horizon: str = Query("7d", regex="^(7d|14d|30d|60d)$"),
    api_key: str = Depends(validate_api_key)
) -> List[Dict[str, Any]]:
    """
    Generate predictive insights for future content performance.

    Args:
        content_id: Content ID to predict for
        prediction_type: Type of prediction (engagement, traffic, revenue, performance)
        prediction_horizon: Time horizon for prediction (7d, 14d, 30d, 60d)
        api_key: Validated API key for authentication

    Returns:
        List of predictive insights
    """
    try:
        result = await insights_service.generate_predictive_insights(
            content_id=content_id,
            prediction_type=prediction_type,
            prediction_horizon=prediction_horizon
        )

        # Log successful prediction
        api_logger.info(f"Generated {len(result)} predictive insights for content {content_id}, type: {prediction_type}")

        return [insight.dict() for insight in result]
    except Exception as e:
        api_logger.error(f"Error generating predictive insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating predictive insights: {str(e)}")


@router.get("/insight-categories")
async def get_insight_categories(
    api_key: str = Depends(validate_api_key)
) -> List[str]:
    """
    Get list of available insight categories.

    Args:
        api_key: Validated API key for authentication

    Returns:
        List of available insight categories
    """
    return [cat.value for cat in InsightCategoryEnum]


@router.get("/recommendation-priorities")
async def get_recommendation_priorities(
    api_key: str = Depends(validate_api_key)
) -> List[str]:
    """
    Get list of available recommendation priorities.

    Args:
        api_key: Validated API key for authentication

    Returns:
        List of available recommendation priorities
    """
    return [priority.value for priority in RecommendationPriorityEnum]


@router.get("/trend-directions")
async def get_trend_directions(
    api_key: str = Depends(validate_api_key)
) -> List[str]:
    """
    Get list of available trend directions.

    Args:
        api_key: Validated API key for authentication

    Returns:
        List of available trend directions
    """
    return [direction.value for direction in TrendDirectionEnum]


@router.get("/health")
async def insights_health_check():
    """
    Health check endpoint for insights service.

    Returns:
        Health status of the insights service
    """
    return {
        "status": "healthy",
        "service": "insights-service",
        "message": "Insights service is operational",
        "timestamp": datetime.utcnow().isoformat()
    }