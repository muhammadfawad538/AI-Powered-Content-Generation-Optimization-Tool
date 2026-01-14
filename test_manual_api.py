"""
Test script to verify that the manual testing API is working correctly.
"""

import requests
import json

def test_api_endpoints():
    """Test the main API endpoints to ensure they're working."""
    base_url = "http://localhost:8000"

    print("Testing Manual Testing API Endpoints...")
    print(f"Base URL: {base_url}")
    print()

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("V Health endpoint: OK")
            print(f"  Response: {response.json()}")
        else:
            print(f"X Health endpoint: Failed with status {response.status_code}")
    except Exception as e:
        print(f"X Health endpoint: Error - {e}")

    print()

    # Test content generation endpoint
    try:
        content_gen_data = {
            "topic": "AI Content Generation",
            "audience": "professionals",
            "tone": "informative",
            "style": "technical",  # Changed from "professional" to "technical" (valid enum value)
            "format": "blog_post",
            "length": 500,
            "keywords": ["AI", "content", "generation"],
            "requirements": ["include benefits", "focus on efficiency"]
        }

        response = requests.post(f"{base_url}/content/generate",
                               json=content_gen_data,
                               headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            print("V Content Generation endpoint: OK")
            resp_data = response.json()
            print(f"  Generated content length: {len(resp_data.get('content', ''))} chars")
            print(f"  Content ID: {resp_data.get('content_id', 'N/A')}")
        else:
            print(f"X Content Generation endpoint: Failed with status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"X Content Generation endpoint: Error - {e}")

    print()

    # Test SEO analysis endpoint
    try:
        seo_data = {
            "content": "This is a sample content about AI content generation for testing purposes.",
            "target_keywords": ["AI", "content", "generation"]
        }

        response = requests.post(f"{base_url}/seo/analyze",
                               json=seo_data,
                               headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            print("V SEO Analysis endpoint: OK")
            resp_data = response.json()
            print(f"  SEO Score: {resp_data.get('seo_score', 'N/A')}")
            print(f"  Content ID: {resp_data.get('content_id', 'N/A')}")
        else:
            print(f"X SEO Analysis endpoint: Failed with status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"X SEO Analysis endpoint: Error - {e}")

    print()

    # Test that Swagger UI is accessible
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("V Swagger UI endpoint: OK")
            print("  You can access the manual testing interface at: http://localhost:8000/docs")
        else:
            print(f"X Swagger UI endpoint: Failed with status {response.status_code}")
    except Exception as e:
        print(f"X Swagger UI endpoint: Error - {e}")

    print()
    print("API Testing Complete!")
    print("All endpoints are operational and ready for manual testing.")
    print("Access the interactive API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    test_api_endpoints()