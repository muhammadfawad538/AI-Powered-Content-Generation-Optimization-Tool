import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.content_generation import (
    ContentGenerationRequest,
    AudienceEnum,
    ToneEnum,
    StyleEnum,
    FormatEnum
)


@pytest.fixture
def client():
    """Create a test client for the API"""
    return TestClient(app)


def test_api_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "AI Content Generation API is running" in data["message"]
    assert "status" in data


def test_content_generation_request_model():
    """Test the ContentGenerationRequest model"""
    request_data = ContentGenerationRequest(
        topic="Sample topic for testing",
        audience=AudienceEnum.GENERAL_PUBLIC,
        tone=ToneEnum.INFORMATIVE,
        style=StyleEnum.EDUCATIONAL,
        format=FormatEnum.BLOG_POST,
        length=300,
        keywords=["sample", "test", "content"]
    )

    assert request_data.topic == "Sample topic for testing"
    assert request_data.audience == AudienceEnum.GENERAL_PUBLIC
    assert request_data.tone == ToneEnum.INFORMATIVE
    assert request_data.style == StyleEnum.EDUCATIONAL
    assert request_data.format == FormatEnum.BLOG_POST
    assert request_data.length == 300
    assert "sample" in request_data.keywords
    assert "test" in request_data.keywords
    assert "content" in request_data.keywords


def test_content_generation_response_structure():
    """Test that the response model has the required fields"""
    from src.models.content_generation import ContentGenerationResponse

    # This test verifies the model structure without creating an instance
    # since the actual response comes from the API
    import inspect
    import sys

    response_class = ContentGenerationResponse
    sig = inspect.signature(response_class.__init__)

    expected_fields = [
        'id', 'content', 'word_count', 'quality_score',
        'generation_time', 'status', 'feedback', 'timestamp'
    ]

    for field in expected_fields:
        assert field in sig.parameters, f"Field {field} missing from ContentGenerationResponse"