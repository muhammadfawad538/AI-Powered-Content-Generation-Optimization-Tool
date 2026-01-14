"""
Export Management Service

This module provides functionality for exporting content to various platforms
and formats, including blog platforms, social media, and ad campaigns.
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional
from urllib.parse import urlparse
from ..models.export_package import (
    ExportRequest, ExportResponse, ExportPackage, ExportStatusEnum,
    ExportFormatEnum, ExportPlatformEnum, PlatformConfig, BatchExportRequest,
    BatchExportResponse, ExportTemplate
)
from ..config.settings import settings
from ..utils.workflow_helpers import format_export_content, sanitize_content_for_platform, generate_workflow_id
from ..utils.logging_config import export_logger
from datetime import datetime


class ExportManagementService:
    """Service class for managing content export to various platforms."""

    def __init__(self):
        """Initialize the Export Management Service."""
        self.session = None
        self.templates = self._load_default_templates()
        self.logger = export_logger

    async def initialize_session(self):
        """Initialize the HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        """Close the HTTP session."""
        if self.session:
            await self.session.close()

    def _load_default_templates(self) -> Dict[str, ExportTemplate]:
        """Load default export templates."""
        templates = {}

        # Blog template
        blog_template = ExportTemplate(
            template_id="blog_default",
            name="Default Blog Template",
            description="Standard template for blog posts",
            platform=ExportPlatformEnum.WORDPRESS,
            format_type=ExportFormatEnum.BLOG,
            template_content="{{title}}\n\n{{content}}\n\nTags: {{tags}}",
            placeholders=["title", "content", "tags"],
            is_default=True
        )
        templates[f"{ExportPlatformEnum.WORDPRESS.value}_{ExportFormatEnum.BLOG.value}"] = blog_template

        # Social media template
        social_template = ExportTemplate(
            template_id="social_default",
            name="Default Social Media Template",
            description="Template for social media posts",
            platform=ExportPlatformEnum.TWITTER,
            format_type=ExportFormatEnum.SOCIAL_MEDIA,
            template_content="{{content}}\n\n#{{hashtags}}",
            placeholders=["content", "hashtags"],
            is_default=True
        )
        templates[f"{ExportPlatformEnum.TWITTER.value}_{ExportFormatEnum.SOCIAL_MEDIA.value}"] = social_template

        # Ad campaign template
        ad_template = ExportTemplate(
            template_id="ad_default",
            name="Default Ad Campaign Template",
            description="Template for ad campaigns",
            platform=ExportPlatformEnum.GOOGLE_ADS,
            format_type=ExportFormatEnum.AD_CAMPAIGN,
            template_content="Headline: {{headline}}\nDescription: {{description}}",
            placeholders=["headline", "description"],
            is_default=True
        )
        templates[f"{ExportPlatformEnum.GOOGLE_ADS.value}_{ExportFormatEnum.AD_CAMPAIGN.value}"] = ad_template

        return templates

    async def export_content(self, request: ExportRequest) -> ExportResponse:
        """
        Export content to the specified platform and format.

        Args:
            request: Export request containing content and destination details

        Returns:
            Export response with operation results
        """
        await self.initialize_session()

        start_time = asyncio.get_event_loop().time()
        export_id = generate_workflow_id()

        self.logger.info(f"Starting export for content_id: {request.content_id}, platform: {request.target_platform.value}, format: {request.export_format.value}")

        try:
            # Format content for the target platform
            formatted_content = format_export_content(request.content, request.export_format.value)
            self.logger.debug(f"Formatted content for {request.export_format.value}")

            # Sanitize content for the specific platform
            sanitized_content = sanitize_content_for_platform(formatted_content, request.target_platform.value)
            self.logger.debug(f"Sanitized content for {request.target_platform.value}")

            # Create export package
            export_package = ExportPackage(
                export_id=export_id,
                content_id=request.content_id,
                export_format=request.export_format,
                target_platform=request.target_platform,
                formatted_content=sanitized_content,
                metadata=request.metadata
            )

            # Execute the export based on platform
            self.logger.info(f"Executing export to {request.target_platform.value}")
            platform_response = await self._execute_platform_export(export_package, request.platform_config)

            # Calculate duration
            duration = asyncio.get_event_loop().time() - start_time

            # Create success response
            response = ExportResponse(
                export_id=export_id,
                content_id=request.content_id,
                export_status=ExportStatusEnum.SUCCESS,
                export_url=platform_response.get('url') if platform_response else None,
                platform_identifier=platform_response.get('id') if platform_response else None,
                message=f"Successfully exported content to {request.target_platform.value}",
                export_duration=duration,
                completion_timestamp=datetime.utcnow()
            )

            # Log export operation
            from ..utils.logging_config import log_export_operation
            log_export_operation(
                self.logger,
                export_id,
                request.content_id,
                request.target_platform.value,
                request.export_format.value,
                "SUCCESS",
                duration * 1000  # Convert to milliseconds
            )

            self.logger.info(f"Successfully exported content_id: {request.content_id} to {request.target_platform.value} in {duration:.2f}s")
            return response

        except Exception as e:
            # Calculate duration even for failed exports
            duration = asyncio.get_event_loop().time() - start_time

            # Create failure response
            response = ExportResponse(
                export_id=export_id,
                content_id=request.content_id,
                export_status=ExportStatusEnum.FAILED,
                message=f"Failed to export content: {str(e)}",
                export_duration=duration,
                completion_timestamp=datetime.utcnow()
            )

            # Log export failure
            from ..utils.logging_config import log_export_operation
            log_export_operation(
                self.logger,
                export_id,
                request.content_id,
                request.target_platform.value,
                request.export_format.value,
                "FAILED",
                duration * 1000  # Convert to milliseconds
            )

            self.logger.error(f"Export failed for content_id: {request.content_id}, error: {str(e)}")
            return response

    async def _execute_platform_export(self, export_package: ExportPackage, platform_config: Optional[PlatformConfig] = None) -> Optional[Dict[str, Any]]:
        """
        Execute the export operation for the specific platform.

        Args:
            export_package: Package containing content to export
            platform_config: Configuration for the target platform

        Returns:
            Response from the target platform
        """
        platform = export_package.target_platform

        if platform == ExportPlatformEnum.WORDPRESS:
            return await self._export_to_wordpress(export_package, platform_config)
        elif platform == ExportPlatformEnum.MEDIUM:
            return await self._export_to_medium(export_package, platform_config)
        elif platform == ExportPlatformEnum.TWITTER:
            return await self._export_to_twitter(export_package, platform_config)
        elif platform == ExportPlatformEnum.FACEBOOK:
            return await self._export_to_facebook(export_package, platform_config)
        elif platform == ExportPlatformEnum.LINKEDIN:
            return await self._export_to_linkedin(export_package, platform_config)
        elif platform == ExportPlatformEnum.GOOGLE_ADS:
            return await self._export_to_google_ads(export_package, platform_config)
        elif platform == ExportPlatformEnum.FACEBOOK_ADS:
            return await self._export_to_facebook_ads(export_package, platform_config)
        else:
            # For custom or unsupported platforms, return basic success
            return {
                "id": export_package.export_id,
                "status": "success",
                "message": f"Content formatted for {platform.value} (mock export)"
            }

    async def _export_to_wordpress(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to WordPress."""
        try:
            # Mock WordPress export - in a real implementation, this would use the WordPress API
            if not config or not config.credentials.get('username') or not config.credentials.get('password'):
                # Use environment variables if no config provided
                wp_user = settings.wordpress_username
                wp_pass = settings.wordpress_password
                wp_url = settings.wordpress_site_url

                if not all([wp_user, wp_pass, wp_url]):
                    return {
                        "id": export_package.export_id,
                        "status": "error",
                        "message": "WordPress credentials not configured"
                    }

                # Mock successful export
                return {
                    "id": export_package.export_id,
                    "url": f"{wp_url}/posts/{export_package.export_id}",
                    "status": "published",
                    "message": "Content exported to WordPress"
                }
            else:
                # Use provided config
                return {
                    "id": export_package.export_id,
                    "url": f"{config.settings.get('site_url', 'https://example.com')}/posts/{export_package.export_id}",
                    "status": "published",
                    "message": "Content exported to WordPress"
                }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"WordPress export failed: {str(e)}"
            }

    async def _export_to_medium(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to Medium."""
        try:
            # Mock Medium export
            return {
                "id": export_package.export_id,
                "url": f"https://medium.com/@user/{export_package.export_id}",
                "status": "published",
                "message": "Content exported to Medium"
            }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"Medium export failed: {str(e)}"
            }

    async def _export_to_twitter(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to Twitter."""
        try:
            # In a real implementation, this would use the Twitter API
            if not config or not config.credentials.get('api_key') or not config.credentials.get('api_secret'):
                # Use environment variables if no config provided
                tw_api_key = settings.twitter_api_key
                tw_api_secret = settings.twitter_api_secret

                if not all([tw_api_key, tw_api_secret]):
                    return {
                        "id": export_package.export_id,
                        "status": "error",
                        "message": "Twitter API credentials not configured"
                    }

            # Truncate content to Twitter's character limit
            tweet_content = export_package.formatted_content[:280]

            return {
                "id": export_package.export_id,
                "url": f"https://twitter.com/user/status/{export_package.export_id}",
                "status": "posted",
                "message": "Content posted to Twitter"
            }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"Twitter export failed: {str(e)}"
            }

    async def _export_to_facebook(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to Facebook."""
        try:
            # In a real implementation, this would use the Facebook Graph API
            if not config or not config.credentials.get('access_token'):
                fb_token = settings.facebook_access_token
                if not fb_token:
                    return {
                        "id": export_package.export_id,
                        "status": "error",
                        "message": "Facebook access token not configured"
                    }

            return {
                "id": export_package.export_id,
                "url": f"https://facebook.com/{export_package.export_id}",
                "status": "posted",
                "message": "Content posted to Facebook"
            }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"Facebook export failed: {str(e)}"
            }

    async def _export_to_linkedin(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to LinkedIn."""
        try:
            # Mock LinkedIn export
            return {
                "id": export_package.export_id,
                "url": f"https://linkedin.com/posts/{export_package.export_id}",
                "status": "posted",
                "message": "Content posted to LinkedIn"
            }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"LinkedIn export failed: {str(e)}"
            }

    async def _export_to_google_ads(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to Google Ads."""
        try:
            # Mock Google Ads export
            return {
                "id": export_package.export_id,
                "status": "created",
                "message": "Ad created in Google Ads"
            }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"Google Ads export failed: {str(e)}"
            }

    async def _export_to_facebook_ads(self, export_package: ExportPackage, config: Optional[PlatformConfig]) -> Optional[Dict[str, Any]]:
        """Export content to Facebook Ads."""
        try:
            # Mock Facebook Ads export
            return {
                "id": export_package.export_id,
                "status": "created",
                "message": "Ad created in Facebook Ads"
            }
        except Exception as e:
            return {
                "id": export_package.export_id,
                "status": "error",
                "message": f"Facebook Ads export failed: {str(e)}"
            }

    async def batch_export(self, request: BatchExportRequest) -> BatchExportResponse:
        """
        Export multiple pieces of content in batch.

        Args:
            request: Batch export request containing multiple export requests

        Returns:
            Batch export response with results
        """
        batch_id = generate_workflow_id()

        if request.parallel_processing:
            # Process exports in parallel
            tasks = [self.export_content(req) for req in request.export_requests]
            individual_results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Process exports sequentially
            individual_results = []
            for export_request in request.export_requests:
                try:
                    result = await self.export_content(export_request)
                    individual_results.append(result)
                except Exception as e:
                    if request.continue_on_failure:
                        # Create a failure response and continue
                        individual_results.append(ExportResponse(
                            export_id=generate_workflow_id(),
                            content_id=export_request.content_id,
                            export_status=ExportStatusEnum.FAILED,
                            message=f"Failed to export content: {str(e)}",
                            completion_timestamp=datetime.utcnow()
                        ))
                    else:
                        # Stop processing if not continuing on failure
                        raise e

        # Process results
        successful_count = 0
        failed_count = 0
        processed_results = []

        for i, result in enumerate(individual_results):
            if isinstance(result, Exception):
                # Handle exceptions from gather
                processed_results.append(ExportResponse(
                    export_id=generate_workflow_id(),
                    content_id=request.export_requests[i].content_id,
                    export_status=ExportStatusEnum.FAILED,
                    message=f"Export failed with exception: {str(result)}",
                    completion_timestamp=datetime.utcnow()
                ))
                failed_count += 1
            elif result.export_status == ExportStatusEnum.SUCCESS:
                processed_results.append(result)
                successful_count += 1
            else:
                processed_results.append(result)
                failed_count += 1

        # Determine overall batch status
        if failed_count == 0:
            batch_status = ExportStatusEnum.SUCCESS
        elif successful_count == 0:
            batch_status = ExportStatusEnum.FAILED
        else:
            batch_status = ExportStatusEnum.SUCCESS  # Partial success

        batch_response = BatchExportResponse(
            batch_id=batch_id,
            total_exports=len(request.export_requests),
            successful_exports=successful_count,
            failed_exports=failed_count,
            results=processed_results,
            batch_status=batch_status,
            completion_timestamp=datetime.utcnow()
        )

        return batch_response

    async def validate_export_format(self, content: str, export_format: ExportFormatEnum) -> Dict[str, Any]:
        """
        Validate that content is suitable for the specified export format.

        Args:
            content: Content to validate
            export_format: Target export format

        Returns:
            Validation results
        """
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "suggestions": []
        }

        if export_format == ExportFormatEnum.SOCIAL_MEDIA:
            if len(content) > 280:
                validation_result["is_valid"] = False
                validation_result["warnings"].append("Content exceeds social media character limits")
                validation_result["suggestions"].append("Consider shortening content or splitting into multiple posts")

        elif export_format == ExportFormatEnum.EMAIL_NEWSLETTER:
            if len(content) < 100:
                validation_result["warnings"].append("Content might be too short for effective newsletter")
                validation_result["suggestions"].append("Consider adding more substantive content")

        elif export_format == ExportFormatEnum.AD_CAMPAIGN:
            if len(content) > 150:
                validation_result["warnings"].append("Content might be too long for ad campaign")
                validation_result["suggestions"].append("Consider condensing to key selling points")

        return validation_result

    def get_export_template(self, platform: ExportPlatformEnum, format_type: ExportFormatEnum) -> Optional[ExportTemplate]:
        """
        Get an appropriate export template for the specified platform and format.

        Args:
            platform: Target platform
            format_type: Export format

        Returns:
            Appropriate export template or None if not found
        """
        key = f"{platform.value}_{format_type.value}"
        return self.templates.get(key)