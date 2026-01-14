import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from src.models.content_generation import (
    ContentGenerationRequest,
    AudienceEnum,
    ToneEnum,
    StyleEnum,
    FormatEnum
)
from src.services.content_generation import ContentGenerationService


@pytest.fixture
def mock_request():
    """Create a mock content generation request for testing"""
    return ContentGenerationRequest(
        topic="Test topic for content generation",
        audience=AudienceEnum.GENERAL_PUBLIC,
        tone=ToneEnum.INFORMATIVE,
        style=StyleEnum.EDUCATIONAL,
        format=FormatEnum.ARTICLE,
        length=500,
        keywords=["test", "content", "generation"]
    )


@pytest.mark.asyncio
async def test_content_generation_service_initialization():
    """Test that the content generation service initializes correctly"""
    service = ContentGenerationService()
    assert service is not None
    assert hasattr(service, 'generate_content')


@pytest.mark.asyncio
async def test_generate_content_method_exists(mock_request):
    """Test that the generate_content method exists and is callable"""
    service = ContentGenerationService()
    assert callable(service.generate_content)


@pytest.mark.asyncio
async def test_calculate_quality_score_basic():
    """Test the basic quality score calculation"""
    service = ContentGenerationService()

    # Test with valid content
    content = "This is a sample content for testing purposes."
    quality_score = service._calculate_quality_score(content, mock_request)

    assert isinstance(quality_score, float)
    assert 0.0 <= quality_score <= 1.0


@pytest.mark.asyncio
async def test_estimate_generation_time():
    """Test the estimate_generation_time method"""
    service = ContentGenerationService()

    mock_request = ContentGenerationRequest(
        topic="Test topic",
        audience=AudienceEnum.GENERAL_PUBLIC,
        tone=ToneEnum.INFORMATIVE,
        style=StyleEnum.EDUCATIONAL,
        format=FormatEnum.ARTICLE,
        length=500,
        keywords=[]
    )

    estimated_time = await service.estimate_generation_time(mock_request)

    assert isinstance(estimated_time, float)
    assert estimated_time > 0