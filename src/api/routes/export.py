"""
Export API Routes

This module defines the API endpoints for export functionality.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from ...models.export_package import (
    ExportRequest, ExportResponse, BatchExportRequest, BatchExportResponse
)
from ...services.export_management import ExportManagementService
from ..middleware.security import validate_api_key


router = APIRouter()
export_service = ExportManagementService()


@router.post("/export-content", response_model=ExportResponse)
async def export_content(
    request: ExportRequest,
    api_key: str = Depends(validate_api_key)
) -> ExportResponse:
    """
    Export content to the specified platform and format.

    Args:
        request: Export request containing content and destination details
        api_key: Validated API key for authentication

    Returns:
        Export response with operation results
    """
    from ..middleware.security import api_logger
    from ..utils.logging_config import log_api_call
    import time

    start_time = time.time()
    try:
        # Validate export format
        validation_result = await export_service.validate_export_format(request.content, request.export_format)
        if not validation_result["is_valid"]:
            warnings = validation_result.get("warnings", [])
            if warnings:
                api_logger.warning(f"Export content validation warnings: {warnings}")

        response = await export_service.export_content(request)

        # Log successful API call
        duration = (time.time() - start_time) * 1000
        log_api_call(
            api_logger,
            "/api/v1/export/export-content",
            "POST",
            request_data={"content_id": request.content_id, "target_platform": request.target_platform.value},
            response_status=200,
            duration_ms=duration
        )

        return response
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        api_logger.error(f"Error exporting content: {str(e)}")
        log_api_call(
            api_logger,
            "/api/v1/export/export-content",
            "POST",
            response_status=500,
            duration_ms=duration
        )
        raise HTTPException(status_code=500, detail=f"Error exporting content: {str(e)}")


@router.post("/batch-export", response_model=BatchExportResponse)
async def batch_export(
    request: BatchExportRequest,
    api_key: str = Depends(validate_api_key)
) -> BatchExportResponse:
    """
    Export multiple pieces of content in batch.

    Args:
        request: Batch export request containing multiple export requests
        api_key: Validated API key for authentication

    Returns:
        Batch export response with results
    """
    try:
        response = await export_service.batch_export(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing batch export: {str(e)}")


@router.get("/health")
async def export_health_check():
    """
    Health check endpoint for export service.

    Returns:
        Health status of the export service
    """
    return {
        "status": "healthy",
        "service": "export-management",
        "message": "Export service is operational"
    }


@router.post("/validate-format")
async def validate_export_format(
    content: str,
    format_type: str,
    api_key: str = Depends(validate_api_key)
) -> Dict[str, any]:
    """
    Validate that content is suitable for the specified export format.

    Args:
        content: Content to validate
        format_type: Target export format
        api_key: Validated API key for authentication

    Returns:
        Validation results
    """
    try:
        from ...models.export_package import ExportFormatEnum
        format_enum = ExportFormatEnum(format_type)

        validation_result = await export_service.validate_export_format(content, format_enum)
        return validation_result
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid format type: {format_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating export format: {str(e)}")


@router.get("/supported-formats")
async def get_supported_formats(api_key: str = Depends(validate_api_key)):
    """
    Get list of supported export formats.

    Args:
        api_key: Validated API key for authentication

    Returns:
        List of supported export formats
    """
    from ...models.export_package import ExportFormatEnum
    return {
        "formats": [fmt.value for fmt in ExportFormatEnum],
        "message": "List of supported export formats"
    }


@router.get("/supported-platforms")
async def get_supported_platforms(api_key: str = Depends(validate_api_key)):
    """
    Get list of supported export platforms.

    Args:
        api_key: Validated API key for authentication

    Returns:
        List of supported export platforms
    """
    from ...models.export_package import ExportPlatformEnum
    return {
        "platforms": [platform.value for platform in ExportPlatformEnum],
        "message": "List of supported export platforms"
    }