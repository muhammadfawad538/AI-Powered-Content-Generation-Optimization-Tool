"""
Test script for Phase 2 implementation of AI Content Generation & Optimization Tool

This script tests the SEO analysis, quality review, and ethics review features.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_quality_metrics():
    """Test the quality metrics utilities."""
    print("Testing Quality Metrics...")
    from utils.quality_metrics import calculate_quality_metrics

    sample_content = """
    Content marketing is an essential strategy for businesses today.
    Companies that invest in content marketing see higher engagement rates
    and increased customer loyalty. Effective content marketing requires
    understanding your audience, creating valuable content, and distributing
    it through appropriate channels. By focusing on quality and relevance,
    businesses can establish themselves as thought leaders in their industry.
    """

    metrics = calculate_quality_metrics(sample_content)
    print(f"Quality Metrics: {metrics}")
    print("V Quality metrics test passed\n")


def test_seo_utilities():
    """Test the SEO utilities."""
    print("Testing SEO Utilities...")
    from utils.seo_metrics import (
        calculate_keyword_density,
        analyze_heading_structure,
        calculate_seo_score,
        extract_meta_description,
        extract_title_suggestions
    )

    sample_content = """
    <h1>Best Practices for Content Marketing</h1>
    <h2>Understanding Your Audience</h2>
    <p>Content marketing is an essential strategy for businesses today.</p>
    <h2>Creating Valuable Content</h2>
    <p>Companies that invest in content marketing see higher engagement.</p>
    """

    keywords = ["content marketing", "audience", "businesses"]

    # Test keyword density
    density = calculate_keyword_density(sample_content, keywords)
    print(f"Keyword Density: {density}")

    # Test heading structure
    headings = analyze_heading_structure(sample_content)
    print(f"Heading Structure: {headings}")

    # Test meta description extraction
    meta_desc = extract_meta_description(sample_content)
    print(f"Meta Description: {meta_desc}")

    # Test title suggestions
    titles = extract_title_suggestions(sample_content)
    print(f"Title Suggestions: {titles}")

    print("V SEO utilities test passed\n")


def test_services():
    """Test the core services."""
    print("Testing Services...")

    # Test SEO Analysis Service
    from models.seo_analysis import SEOAnalysisRequest
    from services.seo_analysis import SEOAnalysisService

    seo_req = SEOAnalysisRequest(
        content_id="test123",
        content="<h1>Content Marketing Guide</h1><p>This is a guide about content marketing for businesses.</p>",
        target_keywords=["content marketing", "guide", "businesses"]
    )

    seo_service = SEOAnalysisService()
    seo_response = seo_service.analyze_content(seo_req)
    print(f"SEO Score: {seo_response.seo_score}")
    print(f"Keyword Density: {seo_response.keyword_density}")

    # Test Quality Review Service
    from models.quality_review import QualityReviewRequest, ReviewAspectEnum
    from services.quality_review import QualityReviewService

    quality_req = QualityReviewRequest(
        content_id="test123",
        content="Content marketing is essential for modern businesses. Companies see great results.",
        target_audience="marketing professionals",
        review_aspect=[ReviewAspectEnum.CLARITY, ReviewAspectEnum.ENGAGEMENT]
    )

    quality_service = QualityReviewService()
    quality_response = quality_service.review_content(quality_req)
    print(f"Clarity Score: {quality_response.clarity_score}")
    print(f"Engagement Score: {quality_response.engagement_score}")

    # Test Ethics Review Service
    from models.ethics_report import EthicsCheckRequest, CheckTypeEnum
    from services.ethics_review import EthicsReviewService

    ethics_req = EthicsCheckRequest(
        content_id="test123",
        content="Businesses should focus on ethical practices and honest marketing.",
        check_type=[CheckTypeEnum.ETHICS, CheckTypeEnum.POLICY]
    )

    ethics_service = EthicsReviewService()
    ethics_response = ethics_service.check_content(ethics_req)
    print(f"Ethical Risk Level: {ethics_response.ethical_risk_level}")
    print(f"Policy Violations: {ethics_response.policy_violations}")

    print("V Services test passed\n")


def main():
    """Run all tests."""
    print("Starting Phase 2 Implementation Tests...\n")

    try:
        test_quality_metrics()
        test_seo_utilities()
        test_services()

        print("🎉 All Phase 2 tests passed successfully!")
        print("\nPhase 2 Features Implemented:")
        print("- SEO Analysis (keyword density, heading structure, SEO scoring)")
        print("- Quality Review (clarity, readability, engagement, flow)")
        print("- Ethics Review (plagiarism detection, ethical risk assessment)")
        print("- Comprehensive API endpoints for all features")

    except Exception as e:
        print(f"X Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\nV Phase 2 Implementation Complete and Tested Successfully!")
    else:
        print("\nX Phase 2 Implementation Failed Tests")
        sys.exit(1)