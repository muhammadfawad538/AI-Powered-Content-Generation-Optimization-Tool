"""
Analytics Data Models

This module defines Pydantic models for analytics and insights functionality,
including content performance tracking, engagement metrics, and SEO effectiveness measurement.
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Literal
from enum import Enum
from .content_generation import ContentDraft


class AnalyticsDataTypeEnum(str, Enum):
    """Enumeration of analytics data types."""
    CONTENT_PERFORMANCE = "content_performance"
    ENGAGEMENT_METRICS = "engagement_metrics"
    SEO_EFFECTIVENESS = "seo_effectiveness"
    USER_INTERACTION = "user_interaction"
    TREND_ANALYSIS = "trend_analysis"


class EngagementMetricEnum(str, Enum):
    """Enumeration of engagement metrics."""
    LIKES = "likes"
    SHARES = "shares"
    COMMENTS = "comments"
    CLICKS = "clicks"
    TIME_ON_PAGE = "time_on_page"
    SCROLL_DEPTH = "scroll_depth"
    VIDEO_COMPLETION = "video_completion"


class ContentChannelEnum(str, Enum):
    """Enumeration of content distribution channels."""
    WEBSITE = "website"
    BLOG = "blog"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    NEWSLETTER = "newsletter"
    MOBILE_APP = "mobile_app"
    RSS_FEED = "rss_feed"


class AnalyticsData(BaseModel):
    """Base model for analytics data."""

    id: str = Field(..., description="Unique identifier for this analytics record")
    content_id: str = Field(..., description="Identifier of the content being tracked")
    data_type: AnalyticsDataTypeEnum = Field(..., description="Type of analytics data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the data was recorded")
    source_channel: ContentChannelEnum = Field(..., description="Channel where the analytics data originated")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the analytics record")
    user_id: Optional[str] = Field(default=None, description="ID of the user associated with the analytics")
    session_id: Optional[str] = Field(default=None, description="Session ID for tracking user session")
    ip_address: Optional[str] = Field(default=None, description="IP address of the user (anonymized if privacy enabled)")
    country: Optional[str] = Field(default=None, description="Country of origin for the analytics data")
    device_type: Optional[str] = Field(default=None, description="Type of device used (mobile, tablet, desktop)")

    class Config:
        use_enum_values = True


class ContentPerformance(BaseModel):
    """Model representing content performance metrics."""

    content_id: str = Field(..., description="Identifier of the content")
    views: int = Field(default=0, ge=0, description="Number of views")
    unique_visitors: int = Field(default=0, ge=0, description="Number of unique visitors")
    page_views: int = Field(default=0, ge=0, description="Number of page views")
    session_duration: float = Field(default=0.0, ge=0.0, description="Average session duration in seconds")
    bounce_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Bounce rate as percentage (0-100)")
    conversion_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Conversion rate as percentage (0-100)")
    conversions: int = Field(default=0, ge=0, description="Number of conversions")
    revenue: float = Field(default=0.0, ge=0.0, description="Revenue generated")
    cost_per_acquisition: float = Field(default=0.0, ge=0.0, description="Cost per acquisition")
    return_on_ad_spend: float = Field(default=0.0, ge=0.0, description="Return on ad spend")
    impressions: int = Field(default=0, ge=0, description="Number of impressions")
    reach: int = Field(default=0, ge=0, description="Number of unique users reached")
    frequency: float = Field(default=0.0, ge=0.0, description="Average frequency of exposure")
    engagement_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Engagement rate as percentage (0-100)")
    share_of_voice: float = Field(default=0.0, ge=0.0, le=100.0, description="Share of voice as percentage (0-100)")
    market_penetration: float = Field(default=0.0, ge=0.0, le=100.0, description="Market penetration as percentage (0-100)")
    brand_awareness_lift: float = Field(default=0.0, ge=0.0, le=100.0, description="Brand awareness lift as percentage (0-100)")
    sentiment_score: float = Field(default=0.0, ge=-1.0, le=1.0, description="Sentiment score from -1 (negative) to 1 (positive)")
    quality_score: float = Field(default=0.0, ge=0.0, le=10.0, description="Quality score from 0-10")
    performance_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Performance score as percentage (0-100)")
    date_recorded: datetime = Field(default_factory=datetime.utcnow, description="Date when the performance was recorded")
    source_channel: ContentChannelEnum = Field(..., description="Channel where the content was distributed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional performance metrics")


class EngagementMetrics(BaseModel):
    """Model representing engagement metrics for content."""

    content_id: str = Field(..., description="Identifier of the content")
    likes: int = Field(default=0, ge=0, description="Number of likes")
    shares: int = Field(default=0, ge=0, description="Number of shares")
    comments: int = Field(default=0, ge=0, description="Number of comments")
    saves: int = Field(default=0, ge=0, description="Number of saves/bookmarks")
    reactions: Dict[str, int] = Field(default_factory=dict, description="Detailed reaction counts (e.g., love, wow, haha)")
    video_views: int = Field(default=0, ge=0, description="Number of video views")
    video_completion_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Video completion rate as percentage (0-100)")
    time_spent: float = Field(default=0.0, ge=0.0, description="Total time spent on content in seconds")
    average_time_spent: float = Field(default=0.0, ge=0.0, description="Average time spent per visitor in seconds")
    scroll_depth: float = Field(default=0.0, ge=0.0, le=100.0, description="Average scroll depth as percentage (0-100)")
    click_through_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Click-through rate as percentage (0-100)")
    engagement_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Overall engagement rate as percentage (0-100)")
    sentiment_positive: int = Field(default=0, ge=0, description="Number of positive sentiment interactions")
    sentiment_negative: int = Field(default=0, ge=0, description="Number of negative sentiment interactions")
    sentiment_neutral: int = Field(default=0, ge=0, description="Number of neutral sentiment interactions")
    sentiment_score: float = Field(default=0.0, ge=-1.0, le=1.0, description="Net sentiment score from -1 to 1")
    viral_coefficient: float = Field(default=0.0, ge=0.0, description="Viral coefficient measuring share of content")
    amplification_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Amplification rate as percentage (0-100)")
    true_engagement_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="True engagement rate excluding bots/invalid traffic")
    date_recorded: datetime = Field(default_factory=datetime.utcnow, description="Date when the engagement was recorded")
    source_channel: ContentChannelEnum = Field(..., description="Channel where the engagement occurred")
    user_engagements: List[Dict[str, Any]] = Field(default_factory=list, description="Detailed user engagement records")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional engagement metrics")


class SEOEffectiveness(BaseModel):
    """Model representing SEO effectiveness metrics for content."""

    content_id: str = Field(..., description="Identifier of the content")
    keyword_rankings: Dict[str, int] = Field(default_factory=dict, description="Keyword rankings (keyword -> position)")
    organic_traffic: int = Field(default=0, ge=0, description="Organic traffic to the content")
    click_through_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Organic CTR as percentage (0-100)")
    impressions: int = Field(default=0, ge=0, description="Organic impressions")
    backlinks: int = Field(default=0, ge=0, description="Number of backlinks")
    referring_domains: int = Field(default=0, ge=0, description="Number of referring domains")
    domain_authority: float = Field(default=0.0, ge=0.0, le=100.0, description="Domain authority score (0-100)")
    page_authority: float = Field(default=0.0, ge=0.0, le=100.0, description="Page authority score (0-100)")
    keyword_density: Dict[str, float] = Field(default_factory=dict, description="Keyword density by keyword")
    readability_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Readability score (0-100)")
    page_load_speed: float = Field(default=0.0, ge=0.0, description="Page load speed in seconds")
    mobile_friendly_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Mobile-friendly score (0-100)")
    accessibility_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Accessibility score (0-100)")
    technical_seo_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Technical SEO score (0-100)")
    content_seo_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Content SEO score (0-100)")
    overall_seo_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Overall SEO score (0-100)")
    crawl_errors: int = Field(default=0, ge=0, description="Number of crawl errors detected")
    broken_links: int = Field(default=0, ge=0, description="Number of broken links")
    canonical_issues: int = Field(default=0, ge=0, description="Number of canonical tag issues")
    meta_optimization_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Meta optimization score (0-100)")
    internal_linking_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Internal linking score (0-100)")
    duplicate_content_issues: int = Field(default=0, ge=0, description="Number of duplicate content issues")
    schema_markup_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Schema markup implementation score (0-100)")
    date_recorded: datetime = Field(default_factory=datetime.utcnow, description="Date when the SEO metrics were recorded")
    source_channel: ContentChannelEnum = Field(..., description="Channel where the content is published")
    competitor_rankings: Dict[str, Dict[str, int]] = Field(default_factory=dict, description="Competitor rankings for same keywords")
    seasonal_trends: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="Seasonal trends for keywords")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional SEO metrics")


class UserInteraction(BaseModel):
    """Model representing user interactions with content."""

    content_id: str = Field(..., description="Identifier of the content")
    user_id: Optional[str] = Field(default=None, description="Identifier of the user")
    session_id: str = Field(..., description="Session identifier for the user session")
    interaction_type: str = Field(..., description="Type of interaction (view, click, share, comment, etc.)")
    interaction_value: Optional[float] = Field(default=None, description="Numeric value of the interaction if applicable")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the interaction occurred")
    duration: Optional[float] = Field(default=None, ge=0.0, description="Duration of interaction in seconds")
    scroll_depth: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Scroll depth achieved (0-100%)")
    elements_clicked: List[str] = Field(default_factory=list, description="List of elements clicked during interaction")
    exit_intent: bool = Field(default=False, description="Whether user showed exit intent")
    page_exit: bool = Field(default=False, description="Whether this was a page exit interaction")
    referral_source: Optional[str] = Field(default=None, description="Source that referred the user")
    utm_parameters: Dict[str, str] = Field(default_factory=dict, description="UTM parameters for tracking")
    device_info: Dict[str, str] = Field(default_factory=dict, description="Device information (browser, OS, etc.)")
    location: Dict[str, str] = Field(default_factory=dict, description="Geographic location information")
    ip_address: Optional[str] = Field(default=None, description="IP address (anonymized if privacy enabled)")
    is_returning_visitor: bool = Field(default=False, description="Whether user is returning visitor")
    user_journey_step: Optional[int] = Field(default=None, description="Step in user journey")
    previous_page: Optional[str] = Field(default=None, description="Previous page in user journey")
    next_page: Optional[str] = Field(default=None, description="Next page in user journey")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional interaction metadata")


class AnalyticsQuery(BaseModel):
    """Model for querying analytics data."""

    content_ids: Optional[List[str]] = Field(default=None, description="Filter by specific content IDs")
    date_range_start: Optional[datetime] = Field(default=None, description="Start date for date range filter")
    date_range_end: Optional[datetime] = Field(default=None, description="End date for date range filter")
    metric_types: Optional[List[AnalyticsDataTypeEnum]] = Field(default=None, description="Filter by specific metric types")
    source_channels: Optional[List[ContentChannelEnum]] = Field(default=None, description="Filter by specific source channels")
    user_ids: Optional[List[str]] = Field(default=None, description="Filter by specific user IDs")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of results to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    sort_by: str = Field(default="timestamp", description="Field to sort by")
    sort_order: Literal["asc", "desc"] = Field(default="desc", description="Sort order (ascending or descending)")
    include_aggregates: bool = Field(default=True, description="Whether to include aggregate metrics")
    group_by: Optional[str] = Field(default=None, description="Group results by specified field")


class AnalyticsResponse(BaseModel):
    """Model for analytics query responses."""

    query_id: str = Field(..., description="Unique identifier for this query")
    data: List[Dict[str, Any]] = Field(..., description="Analytics data results")
    total_records: int = Field(..., description="Total number of records matching the query")
    filtered_records: int = Field(..., description="Number of records after filtering")
    aggregates: Optional[Dict[str, Any]] = Field(default=None, description="Aggregate metrics calculated from the data")
    date_range: Dict[str, datetime] = Field(..., description="Actual date range of the returned data")
    query_params: AnalyticsQuery = Field(..., description="Original query parameters")
    execution_time: float = Field(..., description="Time taken to execute the query in seconds")
    cached: bool = Field(default=False, description="Whether results were served from cache")
    cache_key: Optional[str] = Field(default=None, description="Cache key used for the results")


class AnalyticsValidationRequest(BaseModel):
    """Request to validate analytics data."""

    data_type: AnalyticsDataTypeEnum = Field(..., description="Type of analytics data to validate")
    data_payload: Dict[str, Any] = Field(..., description="Raw analytics data to validate")
    content_id: str = Field(..., description="Content ID associated with the data")
    source_channel: ContentChannelEnum = Field(..., description="Channel where data originated")
    privacy_compliance_required: bool = Field(default=True, description="Whether privacy compliance is required")


class AnalyticsValidationResponse(BaseModel):
    """Response for analytics data validation."""

    is_valid: bool = Field(..., description="Whether the analytics data is valid")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors")
    warnings: List[str] = Field(default_factory=list, description="List of validation warnings")
    privacy_compliance_status: str = Field(..., description="Privacy compliance status")
    recommended_fixes: List[str] = Field(default_factory=list, description="Recommended fixes for invalid data")
    data_sanitized: bool = Field(default=False, description="Whether data was sanitized during validation")