"""
Ethics Review API Routes

This module defines the API endpoints for ethics review and plagiarism checking functionality.
"""

from fastapi import APIRouter, HTTPException
from ..models.ethics_report import EthicsCheckRequest, EthicsCheckResponse
from ..services.ethics_review import EthicsReviewService


router = APIRouter()
ethics_service = EthicsReviewService()


@router.post("/check", response_model=EthicsCheckResponse)
async def check_content(request: EthicsCheckRequest) -> EthicsCheckResponse:
    """
    Perform comprehensive ethics and plagiarism check on the provided content.

    Args:
        request: Ethics check request containing content and parameters

    Returns:
        Ethics check response with results and recommendations
    """
    try:
        response = ethics_service.check_content(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing ethics check: {str(e)}")


@router.post("/plagiarism-check")
async def check_plagiarism(content: str, reference_sources: list = []) -> dict:
    """
    Check content for potential plagiarism against reference sources.

    Args:
        content: Content to check for plagiarism
        reference_sources: Known sources to check against

    Returns:
        Dictionary with plagiarism check results
    """
    try:
        result = ethics_service._check_plagiarism(content, reference_sources, False)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking plagiarism: {str(e)}")


@router.post("/ethics-screen")
async def screen_for_ethics_issues(content: str) -> dict:
    """
    Screen content for potential ethical concerns.

    Args:
        content: Content to check

    Returns:
        Dictionary with ethics check results
    """
    try:
        result = ethics_service._check_ethics(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error screening for ethics issues: {str(e)}")


@router.post("/policy-compliance")
async def check_policy_compliance(content: str) -> dict:
    """
    Check content for policy compliance.

    Args:
        content: Content to check

    Returns:
        Dictionary with policy compliance results
    """
    try:
        result = ethics_service._check_policy_compliance(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking policy compliance: {str(e)}")


@router.post("/store-content")
async def store_content_for_checking(content_id: str, content: str, author_id: str = None):
    """
    Store content for future plagiarism checks.

    Args:
        content_id: Identifier for the content
        content: Content to store
        author_id: Optional author identifier
    """
    try:
        ethics_service.store_content_for_future_check(content_id, content, author_id)
        return {"message": "Content stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing content: {str(e)}")