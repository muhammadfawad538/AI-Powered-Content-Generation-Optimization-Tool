"""
Export Package Data Models

This module defines Pydantic models for export functionality,
including various export formats and platform integrations.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Any, Literal
from enum import Enum


class ExportFormatEnum(str, Enum):
    """Enumeration of supported export formats."""
    BLOG = "blog"
    SOCIAL_MEDIA = "social_media"
    AD_CAMPAIGN = "ad_campaign"
    EMAIL_NEWSLETTER = "email_newsletter"
    PDF = "pdf"
    MARKDOWN = "markdown"
    PLAIN_TEXT = "plain_text"


class ExportPlatformEnum(str, Enum):
    """Enumeration of supported export platforms."""
    WORDPRESS = "wordpress"
    MEDIUM = "medium"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    GOOGLE_ADS = "google_ads"
    FACEBOOK_ADS = "facebook_ads"
    CUSTOM = "custom"


class ExportStatusEnum(str, Enum):
    """Enumeration of export operation statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PlatformConfig(BaseModel):
    """Configuration for a specific export platform."""

    platform: ExportPlatformEnum = Field(..., description="Target platform for export")
    credentials: Dict[str, str] = Field(default_factory=dict, description="Authentication credentials")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific settings")
    enabled: bool = Field(default=True, description="Whether this platform configuration is enabled")


class ExportRequest(BaseModel):
    """Request to export content to a specific platform/format."""

    content_id: str = Field(..., description="Identifier for the content being exported")
    content: str = Field(..., description="Content to be exported")
    export_format: ExportFormatEnum = Field(..., description="Desired export format")
    target_platform: ExportPlatformEnum = Field(..., description="Target platform for export")
    platform_config: Optional[PlatformConfig] = Field(default=None, description="Platform-specific configuration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for export")
    include_images: bool = Field(default=True, description="Whether to include images in export")
    optimize_for_platform: bool = Field(default=True, description="Whether to optimize content for target platform")


class ExportPackage(BaseModel):
    """Represents a complete export package with all necessary components."""

    export_id: str = Field(..., description="Unique identifier for this export operation")
    content_id: str = Field(..., description="Identifier of the original content")
    export_format: ExportFormatEnum = Field(..., description="Format of the export")
    target_platform: ExportPlatformEnum = Field(..., description="Target platform for export")
    formatted_content: str = Field(..., description="Content formatted for the target platform")
    assets: List[Dict[str, str]] = Field(default_factory=list, description="Associated assets (images, files, etc.)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Export metadata")
    export_status: ExportStatusEnum = Field(default=ExportStatusEnum.PENDING, description="Current status of the export")
    export_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the export was initiated")
    completion_timestamp: Optional[datetime] = Field(default=None, description="When the export was completed")
    platform_response: Optional[Dict[str, Any]] = Field(default=None, description="Response from the target platform")
    error_message: Optional[str] = Field(default=None, description="Error message if export failed")


class ExportResponse(BaseModel):
    """Response containing export operation results."""

    export_id: str = Field(..., description="Identifier for the export operation")
    content_id: str = Field(..., description="Identifier of the original content")
    export_status: ExportStatusEnum = Field(..., description="Status of the export operation")
    export_url: Optional[str] = Field(default=None, description="URL where exported content can be accessed")
    platform_identifier: Optional[str] = Field(default=None, description="Identifier assigned by the target platform")
    message: str = Field(..., description="Status message")
    export_duration: Optional[float] = Field(default=None, description="Time taken to complete export in seconds")
    completion_timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="When the operation completed")


class BatchExportRequest(BaseModel):
    """Request to export multiple pieces of content."""

    export_requests: List[ExportRequest] = Field(..., description="List of individual export requests")
    parallel_processing: bool = Field(default=True, description="Whether to process exports in parallel")
    continue_on_failure: bool = Field(default=True, description="Whether to continue processing other exports if one fails")


class BatchExportResponse(BaseModel):
    """Response containing results for batch export operation."""

    batch_id: str = Field(..., description="Identifier for the batch operation")
    total_exports: int = Field(..., description="Total number of export operations")
    successful_exports: int = Field(..., description="Number of successful exports")
    failed_exports: int = Field(..., description="Number of failed exports")
    results: List[ExportResponse] = Field(..., description="Individual export results")
    batch_status: ExportStatusEnum = Field(..., description="Overall status of the batch operation")
    completion_timestamp: Optional[datetime] = Field(default=None, description="When the batch operation completed")


class ExportTemplate(BaseModel):
    """Template for export formatting."""

    template_id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    description: Optional[str] = Field(default=None, description="Description of the template")
    platform: ExportPlatformEnum = Field(..., description="Platform this template is designed for")
    format_type: ExportFormatEnum = Field(..., description="Format type this template supports")
    template_content: str = Field(..., description="Template content with placeholders")
    placeholders: List[str] = Field(default_factory=list, description="Placeholders available in the template")
    is_default: bool = Field(default=False, description="Whether this is the default template for the platform")


class ExportHistoryItem(BaseModel):
    """Record of a past export operation."""

    export_id: str = Field(..., description="Identifier for the export operation")
    content_id: str = Field(..., description="Identifier of the original content")
    export_format: ExportFormatEnum = Field(..., description="Format used for export")
    target_platform: ExportPlatformEnum = Field(..., description="Target platform for export")
    export_status: ExportStatusEnum = Field(..., description="Status of the export operation")
    export_timestamp: datetime = Field(..., description="When the export was performed")
    export_size: int = Field(..., description="Size of the exported content in bytes")
    user_id: Optional[str] = Field(default=None, description="ID of the user who initiated the export")