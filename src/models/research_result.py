"""
Research Result Data Models

This module defines Pydantic models for research assistance functionality,
including search queries, results, and credibility assessments.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum


class SourceCredibilityLevel(str, Enum):
    """Enumeration of source credibility levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class SearchResult(BaseModel):
    """Represents a single search result from a research query."""

    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    snippet: str = Field(..., description="Brief description/snippet of the result")
    source_domain: str = Field(..., description="Domain of the source website")
    published_date: Optional[str] = Field(default=None, description="Publication date if available")
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Relevance score (0-1)")
    credibility_level: SourceCredibilityLevel = Field(default=SourceCredibilityLevel.UNKNOWN, description="Credibility assessment of the source")


class ResearchQuery(BaseModel):
    """Represents a research query request."""

    query_text: str = Field(..., description="The search query text")
    target_domains: List[str] = Field(default_factory=list, description="Specific domains to search within")
    max_results: int = Field(default=10, ge=1, le=100, description="Maximum number of results to return")
    research_purpose: str = Field(..., description="Purpose/context for the research")
    content_topic: Optional[str] = Field(default=None, description="Topic of content being researched")


class ResearchResult(BaseModel):
    """Represents the complete research results for a query."""

    query_id: str = Field(..., description="Unique identifier for this research query")
    original_query: ResearchQuery = Field(..., description="The original research query")
    search_results: List[SearchResult] = Field(..., description="List of search results")
    total_results_found: int = Field(..., description="Total number of results found")
    filtered_results_count: int = Field(..., description="Number of results after filtering")
    credibility_summary: Dict[SourceCredibilityLevel, int] = Field(
        default_factory=dict,
        description="Summary of credibility distribution among results"
    )
    research_summary: str = Field(..., description="Summary of the research findings")
    key_insights: List[str] = Field(default_factory=list, description="Key insights from the research")
    related_topics: List[str] = Field(default_factory=list, description="Related topics discovered during research")
    search_duration: float = Field(..., description="Time taken to perform the research in seconds")
    search_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the research was performed")


class ResearchRequest(BaseModel):
    """Request to perform research assistance."""

    content_id: str = Field(..., description="Identifier for the content being researched")
    query: ResearchQuery = Field(..., description="The research query to execute")
    validate_sources: bool = Field(default=True, description="Whether to validate source credibility")
    include_related_queries: bool = Field(default=True, description="Whether to include related search suggestions")


class ResearchResponse(BaseModel):
    """Response containing research results."""

    content_id: str = Field(..., description="Identifier matching the original request")
    research_results: ResearchResult = Field(..., description="The complete research results")
    status: str = Field(default="completed", description="Status of the research operation")
    completion_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the research completed")


class SourceCredibilityAssessment(BaseModel):
    """Assessment of source credibility."""

    source_url: str = Field(..., description="URL of the source being assessed")
    credibility_level: SourceCredibilityLevel = Field(..., description="Credibility level assigned")
    assessment_criteria: List[str] = Field(..., description="Criteria used for assessment")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the credibility assessment")
    assessment_reasoning: str = Field(..., description="Explanation for the credibility assessment")
    assessed_by: str = Field(default="automated", description="Method used for assessment")
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the assessment was made")


class CredibilityCheckRequest(BaseModel):
    """Request to check credibility of specific sources."""

    urls_to_check: List[str] = Field(..., description="List of URLs to assess for credibility")
    content_context: Optional[str] = Field(default=None, description="Context of content where sources will be used")


class CredibilityCheckResponse(BaseModel):
    """Response containing credibility assessments for sources."""

    request_id: str = Field(..., description="Identifier for the request")
    assessments: List[SourceCredibilityAssessment] = Field(..., description="Credibility assessments for each source")
    summary: Dict[SourceCredibilityLevel, int] = Field(
        default_factory=dict,
        description="Summary of credibility distribution"
    )
    overall_trustworthiness: float = Field(ge=0.0, le=1.0, description="Overall trustworthiness score (0-1)")