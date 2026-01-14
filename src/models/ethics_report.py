from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum


class CheckTypeEnum(str, Enum):
    PLAGIARISM = "plagiarism"
    ETHICS = "ethics"
    POLICY = "policy"


class EthicsCheckRequest(BaseModel):
    """Represents a request for plagiarism and ethical review"""

    content_id: str = Field(
        ...,
        description="Identifier for the content being checked"
    )
    content: str = Field(
        ...,
        min_length=50,
        max_length=10000,
        description="The content to check for ethical issues"
    )
    reference_sources: List[str] = Field(
        default=[],
        max_items=20,
        description="Known sources to check against"
    )
    check_type: List[CheckTypeEnum] = Field(
        default=[],
        min_items=1,
        max_items=3,
        description="Types of checks to perform"
    )
    exclude_self_content: bool = Field(
        default=False,
        description="Whether to exclude user's own previous content from checks"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of request creation"
    )


class EthicsCheckResponse(BaseModel):
    """Represents the results of ethical review"""

    content_id: str = Field(
        ...,
        description="Identifier matching the original request"
    )
    original_content: str = Field(
        ...,
        description="The original content submitted for review"
    )
    plagiarism_detected: bool = Field(
        ...,
        description="Whether potential plagiarism was detected"
    )
    similar_content_sources: List[Dict[str, str]] = Field(
        ...,
        description="Sources of similar content"
    )
    ethical_risk_level: Literal["low", "medium", "high"] = Field(
        ...,
        description="Risk level"
    )
    ethical_concerns: List[str] = Field(
        default=[],
        description="Specific ethical concerns identified"
    )
    policy_violations: List[str] = Field(
        default=[],
        description="Policy violations detected"
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the analysis"
    )
    recommendations: List[str] = Field(
        ...,
        description="Recommendations to address issues"
    )
    check_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Time of ethical check completion"
    )


class PlagiarismMatch(BaseModel):
    """Represents a plagiarism match found in content"""

    source_url: str = Field(
        ...,
        description="URL of the source with matching content"
    )
    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Similarity score between content"
    )
    matched_text: str = Field(
        ...,
        description="Text that matches between the documents"
    )
    matched_percent: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage of content that matches"
    )