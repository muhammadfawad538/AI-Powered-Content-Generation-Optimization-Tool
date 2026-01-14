"""
Analytics API Routes

This module defines the API endpoints for analytics and performance tracking functionality.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ...models.analytics import (
    AnalyticsQuery, AnalyticsResponse, AnalyticsValidationRequest,
    AnalyticsValidationResponse, ContentPerformance, EngagementMetrics,
    SEOEffectiveness, UserInteraction
)
from ...services.analytics_service import AnalyticsService
from ...services.validation import ContentValidationService
from ..middleware.security import validate_api_key
from ...utils.logging_config import api_logger


router = APIRouter()
analytics_service = AnalyticsService()
validation_service = ContentValidationService()


@router.post("/track-performance", response_model=ContentPerformance)
async def track_content_performance(
    content_id: str,
    channel: str,
    views: int = Query(0, ge=0),
    unique_visitors: int = Query(0, ge=0),
    session_duration: float = Query(0.0, ge=0.0),
    bounce_rate: float = Query(0.0, ge=0.0, le=100.0),
    conversions: int = Query(0, ge=0),
    revenue: float = Query(0.0, ge=0.0),
    api_key: str = Depends(validate_api_key)
) -> ContentPerformance:
    """
    Track content performance metrics.

    Args:
        content_id: Identifier of the content
        channel: Channel where content is distributed (website, blog, social_media, etc.)
        views: Number of views
        unique_visitors: Number of unique visitors
        session_duration: Average session duration in seconds
        bounce_rate: Bounce rate as percentage (0-100)
        conversions: Number of conversions
        revenue: Revenue generated
        api_key: Validated API key for authentication

    Returns:
        ContentPerformance model with tracked metrics
    """
    try:
        from ...models.analytics import ContentChannelEnum
        channel_enum = ContentChannelEnum(channel)

        result = await analytics_service.track_content_performance(
            content_id=content_id,
            channel=channel_enum,
            views=views,
            unique_visitors=unique_visitors,
            session_duration=session_duration,
            bounce_rate=bounce_rate,
            conversions=conversions,
            revenue=revenue
        )

        # Log successful tracking
        api_logger.info(f"Content performance tracked for {content_id} on {channel_enum.value}")

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {str(e)}")
    except Exception as e:
        api_logger.error(f"Error tracking content performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error tracking content performance: {str(e)}")


@router.post("/track-engagement", response_model=EngagementMetrics)
async def track_engagement_metrics(
    content_id: str,
    channel: str,
    likes: int = Query(0, ge=0),
    shares: int = Query(0, ge=0),
    comments: int = Query(0, ge=0),
    saves: int = Query(0, ge=0),
    video_views: int = Query(0, ge=0),
    video_completion_rate: float = Query(0.0, ge=0.0, le=100.0),
    time_spent: float = Query(0.0, ge=0.0),
    api_key: str = Depends(validate_api_key)
) -> EngagementMetrics:
    """
    Track engagement metrics for content.

    Args:
        content_id: Identifier of the content
        channel: Channel where engagement occurred
        likes: Number of likes
        shares: Number of shares
        comments: Number of comments
        saves: Number of saves/bookmarks
        video_views: Number of video views
        video_completion_rate: Video completion rate as percentage (0-100)
        time_spent: Total time spent in seconds
        api_key: Validated API key for authentication

    Returns:
        EngagementMetrics model with tracked metrics
    """
    try:
        from ...models.analytics import ContentChannelEnum
        channel_enum = ContentChannelEnum(channel)

        result = await analytics_service.track_engagement_metrics(
            content_id=content_id,
            channel=channel_enum,
            likes=likes,
            shares=shares,
            comments=comments,
            saves=saves,
            video_views=video_views,
            video_completion_rate=video_completion_rate,
            time_spent=time_spent
        )

        # Log successful tracking
        api_logger.info(f"Engagement metrics tracked for {content_id} on {channel_enum.value}")

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {str(e)}")
    except Exception as e:
        api_logger.error(f"Error tracking engagement metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error tracking engagement metrics: {str(e)}")


@router.post("/track-seo", response_model=SEOEffectiveness)
async def track_seo_effectiveness(
    content_id: str,
    channel: str,
    organic_traffic: int = Query(0, ge=0),
    impressions: int = Query(0, ge=0),
    backlinks: int = Query(0, ge=0),
    domain_authority: float = Query(0.0, ge=0.0, le=100.0),
    api_key: str = Depends(validate_api_key)
) -> SEOEffectiveness:
    """
    Track SEO effectiveness metrics for content.

    Args:
        content_id: Identifier of the content
        channel: Channel where content is published
        organic_traffic: Organic traffic to the content
        impressions: Organic impressions
        backlinks: Number of backlinks
        domain_authority: Domain authority score (0-100)
        api_key: Validated API key for authentication

    Returns:
        SEOEffectiveness model with tracked metrics
    """
    try:
        from ...models.analytics import ContentChannelEnum
        channel_enum = ContentChannelEnum(channel)

        result = await analytics_service.track_seo_effectiveness(
            content_id=content_id,
            channel=channel_enum,
            organic_traffic=organic_traffic,
            impressions=impressions,
            backlinks=backlinks,
            domain_authority=domain_authority
        )

        # Log successful tracking
        api_logger.info(f"SEO metrics tracked for {content_id} on {channel_enum.value}")

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {str(e)}")
    except Exception as e:
        api_logger.error(f"Error tracking SEO metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error tracking SEO metrics: {str(e)}")


@router.post("/track-interaction", response_model=UserInteraction)
async def track_user_interaction(
    content_id: str,
    session_id: str,
    interaction_type: str,
    user_id: Optional[str] = None,
    duration: Optional[float] = Query(None, ge=0.0),
    scroll_depth: Optional[float] = Query(None, ge=0.0, le=100.0),
    api_key: str = Depends(validate_api_key)
) -> UserInteraction:
    """
    Track user interaction with content.

    Args:
        content_id: Identifier of the content
        session_id: Session identifier
        interaction_type: Type of interaction (view, click, share, comment, etc.)
        user_id: User identifier (optional)
        duration: Duration of interaction in seconds
        scroll_depth: Scroll depth achieved (0-100%)
        api_key: Validated API key for authentication

    Returns:
        UserInteraction model with tracked interaction
    """
    try:
        result = await analytics_service.track_user_interaction(
            content_id=content_id,
            session_id=session_id,
            interaction_type=interaction_type,
            user_id=user_id,
            duration=duration,
            scroll_depth=scroll_depth
        )

        # Log successful tracking
        api_logger.info(f"User interaction tracked for {content_id}, session {session_id}, type {interaction_type}")

        return result
    except Exception as e:
        api_logger.error(f"Error tracking user interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error tracking user interaction: {str(e)}")


@router.post("/query", response_model=AnalyticsResponse)
async def query_analytics(
    request: AnalyticsQuery,
    api_key: str = Depends(validate_api_key)
) -> AnalyticsResponse:
    """
    Query analytics data based on specified parameters.

    Args:
        request: Analytics query parameters
        api_key: Validated API key for authentication

    Returns:
        AnalyticsResponse with query results
    """
    try:
        result = await analytics_service.query_analytics(request)

        # Log successful query
        api_logger.info(f"Analytics query executed with {len(result.data)} results")

        return result
    except Exception as e:
        api_logger.error(f"Error querying analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying analytics: {str(e)}")


@router.post("/validate-data", response_model=AnalyticsValidationResponse)
async def validate_analytics_data(
    request: AnalyticsValidationRequest,
    api_key: str = Depends(validate_api_key)
) -> AnalyticsValidationResponse:
    """
    Validate analytics data for correctness and privacy compliance.

    Args:
        request: Analytics validation request
        api_key: Validated API key for authentication

    Returns:
        AnalyticsValidationResponse with validation results
    """
    try:
        result = await analytics_service.validate_analytics_data(request)

        # Log validation result
        api_logger.info(f"Analytics data validation for {request.content_id}: {'VALID' if result.is_valid else 'INVALID'}")

        return result
    except Exception as e:
        api_logger.error(f"Error validating analytics data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error validating analytics data: {str(e)}")


@router.get("/performance-trends/{content_id}")
async def get_content_performance_trends(
    content_id: str,
    days_back: int = Query(30, ge=1, le=365),
    api_key: str = Depends(validate_api_key)
) -> Dict[str, Any]:
    """
    Get performance trends for a specific content item.

    Args:
        content_id: Identifier of the content
        days_back: Number of days to look back for trends (default 30, max 365)
        api_key: Validated API key for authentication

    Returns:
        Dictionary with trend analysis results
    """
    try:
        from datetime import datetime
        result = await analytics_service.get_content_performance_trends(content_id, days_back)

        # Log successful request
        api_logger.info(f"Retrieved performance trends for {content_id} over {days_back} days")

        return result
    except Exception as e:
        api_logger.error(f"Error retrieving performance trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving performance trends: {str(e)}")


@router.post("/generate-report")
async def generate_performance_report(
    content_ids: List[str] = Query(..., min_items=1),
    start_date: str = Query(...),
    end_date: str = Query(...),
    api_key: str = Depends(validate_api_key)
) -> Dict[str, Any]:
    """
    Generate a comprehensive performance report for specified content.

    Args:
        content_ids: List of content IDs to include in report
        start_date: Start date for the report period (ISO format)
        end_date: End date for the report period (ISO format)
        api_key: Validated API key for authentication

    Returns:
        Dictionary with comprehensive performance report
    """
    try:
        # Parse date strings to datetime objects
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))

        result = await analytics_service.generate_performance_report(content_ids, start_dt, end_dt)

        # Log successful report generation
        api_logger.info(f"Generated performance report for {len(content_ids)} content items")

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        api_logger.error(f"Error generating performance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating performance report: {str(e)}")


@router.get("/health")
async def analytics_health_check():
    """
    Health check endpoint for analytics service.

    Returns:
        Health status of the analytics service
    """
    return {
        "status": "healthy",
        "service": "analytics-service",
        "message": "Analytics service is operational",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/aggregate-by-timeframe")
async def aggregate_data_by_timeframe(
    data: str,  # In a real implementation, this would be a more structured request
    timeframe: str = Query("daily", regex="^(hourly|daily|weekly|monthly)$"),
    api_key: str = Depends(validate_api_key)
) -> List[Dict[str, Any]]:
    """
    Aggregate analytics data by specified timeframe.

    Args:
        data: JSON string containing analytics data to aggregate
        timeframe: Aggregation timeframe ("hourly", "daily", "weekly", "monthly")
        api_key: Validated API key for authentication

    Returns:
        Aggregated data list
    """
    try:
        import json
        parsed_data = json.loads(data)

        result = await analytics_service.aggregate_data_by_timeframe(parsed_data, timeframe)

        # Log successful aggregation
        api_logger.info(f"Aggregated {len(parsed_data)} records by {timeframe} timeframe")

        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided")
    except Exception as e:
        api_logger.error(f"Error aggregating data by timeframe: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error aggregating data by timeframe: {str(e)}")