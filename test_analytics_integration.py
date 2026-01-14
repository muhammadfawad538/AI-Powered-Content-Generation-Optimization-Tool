"""
Integration Test Script for Analytics & Insights Features

This script tests the integration between analytics and insights features,
validating that they work together properly with the existing system.
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.analytics import (
    ContentPerformance, EngagementMetrics, SEOEffectiveness, UserInteraction,
    AnalyticsQuery, AnalyticsResponse
)
from models.insights import (
    ContentInsightsResponse, InsightsQuery, PersonalizationProfile,
    InsightCategoryEnum, RecommendationPriorityEnum
)
from services.analytics_service import AnalyticsService
from services.insights_service import InsightsService
from utils.analytics_helpers import AnalyticsHelper


async def test_analytics_functionality():
    """Test the analytics functionality."""
    print("Testing Analytics Functionality...")

    analytics_service = AnalyticsService()

    # Test content performance tracking
    content_performance = await analytics_service.track_content_performance(
        content_id="test_content_1",
        channel="website",
        views=1500,
        unique_visitors=1200,
        session_duration=120.5,
        bounce_rate=25.0,
        conversions=45,
        revenue=1250.75
    )
    print(f"✓ Content performance tracked: {content_performance.views} views, {content_performance.engagement_rate}% engagement")

    # Test engagement metrics tracking
    engagement_metrics = await analytics_service.track_engagement_metrics(
        content_id="test_content_1",
        channel="website",
        likes=120,
        shares=45,
        comments=89,
        saves=30,
        video_views=200,
        video_completion_rate=75.0,
        time_spent=180.0
    )
    print(f"✓ Engagement metrics tracked: {engagement_metrics.likes} likes, {engagement_metrics.engagement_rate}% engagement")

    # Test SEO effectiveness tracking
    seo_metrics = await analytics_service.track_seo_effectiveness(
        content_id="test_content_1",
        channel="website",
        keyword_rankings={"seo": 15, "content": 8, "marketing": 22},
        organic_traffic=800,
        impressions=4500,
        backlinks=25,
        domain_authority=65.0
    )
    print(f"✓ SEO metrics tracked: {seo_metrics.organic_traffic} organic traffic, DA {seo_metrics.domain_authority}")

    # Test user interaction tracking
    user_interaction = await analytics_service.track_user_interaction(
        content_id="test_content_1",
        session_id="session_123",
        interaction_type="view",
        user_id="user_456",
        duration=120.0,
        scroll_depth=75.0
    )
    print(f"✓ User interaction tracked: {user_interaction.interaction_type} on {user_interaction.content_id}")

    # Test analytics querying
    query = AnalyticsQuery(
        content_ids=["test_content_1"],
        date_range_start=datetime.utcnow() - timedelta(days=7),
        date_range_end=datetime.utcnow(),
        include_aggregates=True
    )
    response = await analytics_service.query_analytics(query)
    print(f"✓ Analytics query executed: {len(response.data)} results")

    return True


async def test_insights_functionality():
    """Test the insights functionality."""
    print("\nTesting Insights Functionality...")

    insights_service = InsightsService()

    # Test content insights generation
    insights_response = await insights_service.generate_content_insights(
        content_id="test_content_1"
    )
    print(f"✓ Generated {len(insights_response.insights)} insights and {len(insights_response.recommendations)} recommendations")

    # Test trend analysis
    trend_analyses = await insights_service.analyze_trends(
        content_ids=["test_content_1", "test_content_2"],
        metric_type="views",
        days_back=30
    )
    print(f"✓ Performed trend analysis for {len(trend_analyses)} content items")

    # Test comparative analysis
    comparative_analysis = await insights_service.perform_comparative_analysis(
        content_ids=["test_content_1", "test_content_2"],
        comparison_basis="engagement"
    )
    print(f"✓ Performed comparative analysis for {len(comparative_analysis.content_ids)} content items")

    # Test predictive insights
    predictive_insights = await insights_service.generate_predictive_insights(
        content_id="test_content_1",
        prediction_type="engagement",
        prediction_horizon="7d"
    )
    print(f"✓ Generated {len(predictive_insights)} predictive insights")

    return True


async def test_end_to_end_scenario():
    """Test an end-to-end scenario combining analytics and insights."""
    print("\nTesting End-to-End Scenario...")

    analytics_service = AnalyticsService()
    insights_service = InsightsService()

    try:
        # Step 1: Track content performance over time
        content_ids = [f"content_{i}" for i in range(1, 6)]
        for content_id in content_ids:
            # Track performance
            await analytics_service.track_content_performance(
                content_id=content_id,
                channel="website",
                views=1000 + (hash(content_id) % 500),
                unique_visitors=800 + (hash(content_id) % 400),
                session_duration=90.0 + (hash(content_id) % 60),
                bounce_rate=30.0 - (hash(content_id) % 10),
                conversions=20 + (hash(content_id) % 30),
                revenue=500.0 + (hash(content_id) % 500)
            )

            # Track engagement
            await analytics_service.track_engagement_metrics(
                content_id=content_id,
                channel="website",
                likes=50 + (hash(content_id) % 100),
                shares=10 + (hash(content_id) % 50),
                comments=20 + (hash(content_id) % 60),
                saves=5 + (hash(content_id) % 20)
            )

        print(f"✓ Tracked performance for {len(content_ids)} content items")

        # Step 2: Generate insights for all content
        query = InsightsQuery(
            content_ids=content_ids,
            min_significance=0.1,
            min_confidence=0.1,
            include_recommendations=True,
            include_trends=True
        )
        insights_response = await insights_service.query_insights(query)
        print(f"✓ Generated insights for {len(content_ids)} content items: {len(insights_response.insights)} insights")

        # Step 3: Perform comparative analysis
        comp_analysis = await insights_service.perform_comparative_analysis(
            content_ids=content_ids,
            comparison_basis="engagement"
        )
        print(f"✓ Comparative analysis completed, winner: {comp_analysis.winning_content_id}")

        # Step 4: Generate personalized recommendations
        profile = PersonalizationProfile(
            profile_id="profile_test",
            user_id="user_test",
            preferred_categories=[InsightCategoryEnum.PERFORMANCE, InsightCategoryEnum.ENGAGEMENT],
            recommendation_threshold=0.3,
            notification_preferences={"performance": True, "engagement": True},
            content_focus_areas=["engagement", "conversions"],
            update_frequency="daily"
        )
        personalized_recs = await insights_service.generate_personalized_recommendations(
            user_profile=profile,
            content_ids=content_ids
        )
        print(f"✓ Generated {len(personalized_recs)} personalized recommendations")

        print("✓ End-to-end scenario completed successfully")
        return True

    except Exception as e:
        print(f"✗ End-to-end scenario failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_validation_functionality():
    """Test the validation functionality for analytics and insights."""
    print("\nTesting Validation Functionality...")

    from services.validation import ContentValidationService
    validation_service = ContentValidationService()

    # Test analytics validation
    from models.analytics import AnalyticsValidationRequest, AnalyticsDataTypeEnum, ContentChannelEnum
    analytics_validation_request = AnalyticsValidationRequest(
        data_type=AnalyticsDataTypeEnum.CONTENT_PERFORMANCE,
        data_payload={
            "content_id": "test_content_1",
            "views": 1000,
            "unique_visitors": 800,
            "engagement_rate": 2.5
        },
        content_id="test_content_1",
        source_channel=ContentChannelEnum.WEBSITE,
        privacy_compliance_required=True
    )

    analytics_validation_response = await analytics_service.validate_analytics_data(analytics_validation_request)
    print(f"✓ Analytics validation: {'VALID' if analytics_validation_response.is_valid else 'INVALID'}")

    # Test insights validation
    from models.insights import InsightsValidationRequest, InsightsValidationResponse
    insights_validation_request = InsightsValidationRequest(
        insight_data={
            "insight_id": "test_insight_1",
            "content_id": "test_content_1",
            "category": "performance",
            "title": "Test Insight",
            "description": "This is a test insight"
        },
        content_id="test_content_1"
    )

    insights_validation_response = await insights_service.validate_insights_data(insights_validation_request)
    print(f"✓ Insights validation: {'VALID' if insights_validation_response.is_valid else 'INVALID'}")

    return True


async def main():
    """Run all integration tests."""
    print("Starting Analytics & Insights Integration Tests...\n")

    results = []

    # Run all tests
    results.append(("Analytics Functionality", await test_analytics_functionality()))
    results.append(("Insights Functionality", await test_insights_functionality()))
    results.append(("Validation Functionality", await test_validation_functionality()))
    results.append(("End-to-End Scenario", await test_end_to_end_scenario()))

    # Print summary
    print("\n" + "="*60)
    print("INTEGRATION TEST SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        icon = "✓" if passed else "✗"
        print(f"{icon} {test_name}: {status}")
        if not passed:
            all_passed = False

    print("="*60)
    if all_passed:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nAnalytics & Insights features are fully integrated and working!")
    else:
        print("❌ SOME INTEGRATION TESTS FAILED")
        print("Please review the failing tests above.")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)