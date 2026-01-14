from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Literal
from enum import Enum


class AudienceEnum(str, Enum):
    GENERAL_PUBLIC = "general_public"
    EXPERTS = "experts"
    STUDENTS = "students"
    BUSINESS_PROFESSIONALS = "business_professionals"
    ENVIRONMENTAL_ADVOCATES = "environmental_advocates"


class ToneEnum(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    INFORMATIVE = "informative"
    PERSUASIVE = "persuasive"
    HUMOROUS = "humorous"


class StyleEnum(str, Enum):
    NARRATIVE = "narrative"
    INFORMATIVE = "informative"
    PERSUASIVE = "persuasive"
    DESCRIPTIVE = "descriptive"
    EDUCATIONAL = "educational"


class FormatEnum(str, Enum):
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    PRODUCT_DESCRIPTION = "product_description"
    ARTICLE = "article"
    SCRIPT = "script"


class ContentGenerationRequest(BaseModel):
    """Represents a user request for content generation with all required parameters"""

    id: Optional[str] = None
    topic: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Main subject or theme for content generation"
    )
    audience: AudienceEnum = Field(
        ...,
        description="Target audience for the content"
    )
    tone: ToneEnum = Field(
        ...,
        description="Desired tone of the content"
    )
    style: StyleEnum = Field(
        ...,
        description="Writing style preferences"
    )
    format: FormatEnum = Field(
        ...,
        description="Content format"
    )
    length: int = Field(
        ...,
        ge=100,
        le=5000,
        description="Target length in words"
    )
    keywords: List[str] = Field(
        default=[],
        max_items=10,
        description="SEO keywords to incorporate naturally"
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None


class ContentGenerationResponse(BaseModel):
    """Represents the result of a content generation request"""

    id: str = Field(..., description="Unique identifier matching the request")
    content: str = Field(..., description="Generated content text")
    word_count: int = Field(..., description="Actual word count of generated content")
    quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Score representing content quality (0.0-1.0)"
    )
    generation_time: float = Field(..., description="Time taken to generate content in seconds")
    status: Literal["success", "error", "partial"] = Field(
        ...,
        description="Status of the generation process"
    )
    feedback: Optional[str] = Field(
        None,
        description="Optional feedback about the generation process"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of response creation")


class UserPreferences(BaseModel):
    """Stores user preferences for content generation"""

    user_id: str = Field(..., description="Unique identifier for the user")
    default_audience: Optional[AudienceEnum] = Field(None, description="Default target audience")
    default_tone: Optional[ToneEnum] = Field(None, description="Default content tone")
    default_format: Optional[FormatEnum] = Field(None, description="Default content format")
    preferred_keywords: List[str] = Field(
        default=[],
        description="Default keywords to include"
    )
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of last preference update")