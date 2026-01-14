from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum


class AnalysisDepthEnum(str, Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"


class SEOAnalysisRequest(BaseModel):
    """Represents a request for SEO analysis of existing content"""

    content_id: str = Field(
        ...,
        description="Identifier for the content being analyzed"
    )
    content: str = Field(
        ...,
        min_length=100,
        max_length=10000,
        description="The content to analyze for SEO"
    )
    target_keywords: List[str] = Field(
        default=[],
        max_items=20,
        description="Keywords to analyze for optimization"
    )
    competitor_urls: List[str] = Field(
        default=[],
        max_items=5,
        description="URLs of competitor content for comparison (optional)"
    )
    analysis_depth: AnalysisDepthEnum = Field(
        default=AnalysisDepthEnum.DETAILED,
        description="Level of analysis"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of request creation"
    )


class SEOAnalysisResponse(BaseModel):
    """Represents the results of SEO analysis"""

    content_id: str = Field(
        ...,
        description="Identifier matching the original request"
    )
    keyword_density: Dict[str, float] = Field(
        ...,
        description="Density of each target keyword"
    )
    readability_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Overall readability score"
    )
    heading_structure: Dict[str, int] = Field(
        ...,
        description="Count of H1, H2, H3, etc. tags"
    )
    meta_description: str = Field(
        ...,
        description="Suggested meta description"
    )
    title_suggestions: List[str] = Field(
        ...,
        description="Recommended titles"
    )
    recommended_keywords: List[str] = Field(
        ...,
        description="Additional keywords to consider"
    )
    seo_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Overall SEO score"
    )
    improvement_suggestions: List[str] = Field(
        ...,
        description="Specific suggestions for improvement"
    )
    competitor_comparison: Optional[Dict[str, str]] = Field(
        None,
        description="Comparison with competitor content"
    )
    report_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Time of analysis completion"
    )


class SEOSuggestion(BaseModel):
    """Represents a specific SEO suggestion"""

    category: str = Field(
        ...,
        description="Category of the suggestion (e.g., 'keyword', 'structure', 'content')"
    )
    original: str = Field(
        ...,
        description="Original content that needs improvement"
    )
    suggested: str = Field(
        ...,
        description="Suggested improvement"
    )
    reason: str = Field(
        ...,
        description="Reason for the suggestion"
    )
    impact: Literal["low", "medium", "high"] = Field(
        ...,
        description="Expected impact of implementing the suggestion"
    )