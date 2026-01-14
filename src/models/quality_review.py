from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum


class ReviewAspectEnum(str, Enum):
    CLARITY = "clarity"
    READABILITY = "readability"
    ENGAGEMENT = "engagement"
    FLOW = "flow"


class QualityReviewRequest(BaseModel):
    """Represents a request for quality review and improvement"""

    content_id: str = Field(
        ...,
        description="Identifier for the content being reviewed"
    )
    content: str = Field(
        ...,
        min_length=50,
        max_length=10000,
        description="The content to review for quality"
    )
    target_audience: str = Field(
        ...,
        description="Audience for whom the content is intended"
    )
    review_aspect: List[ReviewAspectEnum] = Field(
        default=[],
        min_items=1,
        max_items=4,
        description="Aspects to review"
    )
    preserve_tone: bool = Field(
        default=True,
        description="Whether to maintain the original tone"
    )
    style_guidelines: Optional[Dict[str, str]] = Field(
        None,
        description="Specific style guidelines to follow"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of request creation"
    )


class QualityReviewResponse(BaseModel):
    """Represents the results of quality review with improvement suggestions"""

    content_id: str = Field(
        ...,
        description="Identifier matching the original request"
    )
    original_content: str = Field(
        ...,
        description="The original content submitted for review"
    )
    improved_content: str = Field(
        ...,
        description="Content with quality improvements applied"
    )
    clarity_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Clarity rating"
    )
    readability_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Readability rating"
    )
    engagement_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Engagement potential rating"
    )
    flow_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Content flow rating"
    )
    improvement_summary: List[Dict[str, str]] = Field(
        ...,
        description="Summary of changes made"
    )
    preserved_elements: List[str] = Field(
        ...,
        description="Elements that were preserved"
    )
    review_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Time of review completion"
    )


class QualityImprovement(BaseModel):
    """Represents a specific quality improvement"""

    aspect: ReviewAspectEnum = Field(
        ...,
        description="Aspect being improved"
    )
    before: str = Field(
        ...,
        description="Original text segment"
    )
    after: str = Field(
        ...,
        description="Improved text segment"
    )
    reason: str = Field(
        ...,
        description="Reason for the change"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the improvement"
    )