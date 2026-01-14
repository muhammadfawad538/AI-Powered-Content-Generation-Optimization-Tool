"""
Insights & Recommendations Data Models

This module defines Pydantic models for insights and recommendations functionality,
including content insights, recommendations, trend analysis, and personalized suggestions.
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Dict, Optional, Any, Literal
from enum import Enum
from .content_generation import ContentDraft
from .analytics import ContentPerformance, EngagementMetrics, SEOEffectiveness
from .seo_analysis import SEOAnalysisResponse


class InsightCategoryEnum(str, Enum):
    """Enumeration of insight categories."""
    PERFORMANCE = "performance"
    ENGAGEMENT = "engagement"
    SEO = "seo"
    QUALITY = "quality"
    AUDIENCE = "audience"
    TIMING = "timing"
    COMPARISON = "comparison"


class RecommendationPriorityEnum(str, Enum):
    """Enumeration of recommendation priorities."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class TrendDirectionEnum(str, Enum):
    """Enumeration of trend directions."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


class ContentInsight(BaseModel):
    """Model representing an insight about content performance."""

    insight_id: str = Field(..., description="Unique identifier for this insight")
    content_id: str = Field(..., description="Identifier of the content this insight relates to")
    category: InsightCategoryEnum = Field(..., description="Category of the insight")
    title: str = Field(..., description="Brief title of the insight")
    description: str = Field(..., description="Detailed description of the insight")
    significance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Score indicating the significance of the insight (0-1)")
    supporting_data: Dict[str, Any] = Field(default_factory=dict, description="Supporting data for the insight")
    date_generated: datetime = Field(default_factory=datetime.utcnow, description="When the insight was generated")
    impacted_metrics: List[str] = Field(default_factory=list, description="List of metrics affected by this insight")
    confidence_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence level in the insight (0-1)")
    trend_data: Optional[Dict[str, Any]] = Field(default=None, description="Trend data related to this insight")
    visualization_hint: Optional[str] = Field(default=None, description="Suggested visualization type for this insight")


class Recommendation(BaseModel):
    """Model representing a recommendation for content improvement."""

    recommendation_id: str = Field(..., description="Unique identifier for this recommendation")
    content_id: Optional[str] = Field(default=None, description="Identifier of the specific content this recommendation relates to")
    priority: RecommendationPriorityEnum = Field(..., description="Priority level of the recommendation")
    title: str = Field(..., description="Brief title of the recommendation")
    description: str = Field(..., description="Detailed description of the recommendation")
    action_items: List[str] = Field(default_factory=list, description="Specific action items to implement the recommendation")
    estimated_impact: float = Field(default=0.0, ge=0.0, le=100.0, description="Estimated impact as percentage improvement (0-100)")
    implementation_effort: Literal["low", "medium", "high"] = Field(default="medium", description="Effort required to implement")
    affected_metrics: List[str] = Field(default_factory=list, description="List of metrics that would be affected by this recommendation")
    date_generated: datetime = Field(default_factory=datetime.utcnow, description="When the recommendation was generated")
    category: InsightCategoryEnum = Field(..., description="Category of the recommendation")
    confidence_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence level in the recommendation (0-1)")
    tags: List[str] = Field(default_factory=list, description="Tags for categorizing the recommendation")


class TrendAnalysis(BaseModel):
    """Model representing trend analysis for content or metrics."""

    analysis_id: str = Field(..., description="Unique identifier for this trend analysis")
    content_id: Optional[str] = Field(default=None, description="Identifier of the content being analyzed (if specific)")
    metric_type: str = Field(..., description="Type of metric being analyzed")
    trend_direction: TrendDirectionEnum = Field(..., description="Direction of the trend")
    trend_strength: float = Field(default=0.0, ge=0.0, le=1.0, description="Strength of the trend (0-1)")
    time_period: str = Field(..., description="Time period for the trend analysis")
    start_value: float = Field(..., description="Starting value of the metric")
    end_value: float = Field(..., description="Ending value of the metric")
    percentage_change: float = Field(..., description="Percentage change over the period")
    data_points: List[Dict[str, Any]] = Field(default_factory=list, description="Time series data points")
    seasonality_detected: bool = Field(default=False, description="Whether seasonality patterns were detected")
    anomaly_count: int = Field(default=0, description="Number of anomalies detected in the data")
    forecast_available: bool = Field(default=False, description="Whether a forecast is available")
    forecast_data: Optional[Dict[str, Any]] = Field(default=None, description="Forecasted values and confidence intervals")
    date_generated: datetime = Field(default_factory=datetime.utcnow, description="When the analysis was generated")
    confidence_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence level in the analysis (0-1)")


class PersonalizationProfile(BaseModel):
    """Model representing user preferences for personalized insights and recommendations."""

    profile_id: str = Field(..., description="Unique identifier for the personalization profile")
    user_id: str = Field(..., description="Identifier of the user this profile belongs to")
    preferred_categories: List[InsightCategoryEnum] = Field(default_factory=list, description="Preferred insight categories")
    recommendation_threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum significance score for recommendations to be shown")
    notification_preferences: Dict[str, bool] = Field(default_factory=dict, description="Notification preferences for different insight types")
    content_focus_areas: List[str] = Field(default_factory=list, description="Areas of content the user wants to focus on")
    update_frequency: Literal["realtime", "daily", "weekly", "monthly"] = Field(default="daily", description="How often to receive updates")
    date_created: datetime = Field(default_factory=datetime.utcnow, description="When the profile was created")
    date_modified: datetime = Field(default_factory=datetime.utcnow, description="When the profile was last modified")


class ContentInsightsResponse(BaseModel):
    """Response model for content insights."""

    content_id: str = Field(..., description="Identifier of the content")
    insights: List[ContentInsight] = Field(default_factory=list, description="List of insights for the content")
    recommendations: List[Recommendation] = Field(default_factory=list, description="List of recommendations for the content")
    trend_analysis: Optional[TrendAnalysis] = Field(default=None, description="Trend analysis for the content")
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Overall score for the content (0-100)")
    date_generated: datetime = Field(default_factory=datetime.utcnow, description="When the insights were generated")
    execution_time: float = Field(..., description="Time taken to generate insights in seconds")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used for the insights")


class InsightsQuery(BaseModel):
    """Model for querying insights and recommendations."""

    content_ids: Optional[List[str]] = Field(default=None, description="Filter by specific content IDs")
    categories: Optional[List[InsightCategoryEnum]] = Field(default=None, description="Filter by insight categories")
    date_range_start: Optional[datetime] = Field(default=None, description="Start date for date range filter")
    date_range_end: Optional[datetime] = Field(default=None, description="End date for date range filter")
    min_significance: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum significance score for insights")
    min_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum confidence level for insights/recommendations")
    include_recommendations: bool = Field(default=True, description="Whether to include recommendations in the response")
    include_trends: bool = Field(default=True, description="Whether to include trend analysis in the response")
    limit: int = Field(default=50, ge=1, le=500, description="Maximum number of results to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    sort_by: str = Field(default="significance_score", description="Field to sort by")
    sort_order: Literal["asc", "desc"] = Field(default="desc", description="Sort order (ascending or descending)")


class InsightsValidationRequest(BaseModel):
    """Request to validate insights and recommendations data."""

    insight_data: Dict[str, Any] = Field(..., description="Raw insight data to validate")
    recommendation_data: Optional[Dict[str, Any]] = Field(default=None, description="Raw recommendation data to validate")
    content_id: Optional[str] = Field(default=None, description="Content ID associated with the data")
    user_id: Optional[str] = Field(default=None, description="User ID for personalization validation")


class InsightsValidationResponse(BaseModel):
    """Response for insights and recommendations validation."""

    is_valid: bool = Field(..., description="Whether the insights data is valid")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors")
    warnings: List[str] = Field(default_factory=list, description="List of validation warnings")
    data_quality_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Score representing the quality of the data (0-1)")
    recommended_fixes: List[str] = Field(default_factory=list, description="Recommended fixes for invalid data")
    data_sanitized: bool = Field(default=False, description="Whether data was sanitized during validation")


class ComparativeAnalysis(BaseModel):
    """Model for comparing content performance and generating insights."""

    analysis_id: str = Field(..., description="Unique identifier for this comparative analysis")
    content_ids: List[str] = Field(..., description="IDs of content being compared")
    comparison_basis: str = Field(..., description="Basis for comparison (e.g., engagement, SEO, conversions)")
    winning_content_id: Optional[str] = Field(default=None, description="ID of the content that performed better")
    performance_gaps: Dict[str, float] = Field(default_factory=dict, description="Performance gaps between content items")
    improvement_opportunities: List[str] = Field(default_factory=list, description="Opportunities for improvement based on comparison")
    date_generated: datetime = Field(default_factory=datetime.utcnow, description="When the analysis was generated")


class PredictiveInsight(BaseModel):
    """Model for predictive insights and forecasting."""

    insight_id: str = Field(..., description="Unique identifier for this predictive insight")
    content_id: Optional[str] = Field(default=None, description="Identifier of the content this insight relates to")
    prediction_type: str = Field(..., description="Type of prediction (e.g., performance, trend, outcome)")
    predicted_value: float = Field(..., description="Predicted value")
    confidence_interval: Dict[str, float] = Field(default_factory=dict, description="Confidence interval for the prediction")
    prediction_horizon: str = Field(..., description="Time horizon for the prediction")
    influencing_factors: List[str] = Field(default_factory=list, description="Factors influencing the prediction")
    date_generated: datetime = Field(default_factory=datetime.utcnow, description="When the prediction was generated")