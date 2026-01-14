# Analytics & Insights API Documentation

This document provides comprehensive information about the Analytics & Insights API endpoints added in Phase 4 and Phase 5 of the AI-Powered Content Generation & Optimization Tool.

## Base URL
```
http://your-domain.com/api/v1/
```

## Authentication
All endpoints require a valid API key in the request headers:
```
Authorization: Bearer YOUR_API_KEY
```
or
```
X-API-Key: YOUR_API_KEY
```

## Analytics Endpoints

### POST `/analytics/track-performance`
Track content performance metrics.

#### Parameters:
- `content_id`: String (required) - Identifier of the content
- `channel`: String (required) - Channel where content is distributed (website, blog, social_media, etc.)
- `views`: Integer (optional, default: 0) - Number of views
- `unique_visitors`: Integer (optional, default: 0) - Number of unique visitors
- `session_duration`: Float (optional, default: 0.0) - Average session duration in seconds
- `bounce_rate`: Float (optional, default: 0.0) - Bounce rate as percentage (0-100)
- `conversions`: Integer (optional, default: 0) - Number of conversions
- `revenue`: Float (optional, default: 0.0) - Revenue generated

#### Response:
Returns a `ContentPerformance` object with the tracked metrics.

#### Example:
````
curl -X POST "http://your-domain.com/api/v1/analytics/track-performance?content_id=content_123&channel=website&views=1500&revenue=1250.75" \
  -H "Authorization: Bearer YOUR_API_KEY"
````

### POST `/analytics/track-engagement`
Track engagement metrics for content.

#### Parameters:
- `content_id`: String (required) - Identifier of the content
- `channel`: String (required) - Channel where engagement occurred
- `likes`: Integer (optional, default: 0) - Number of likes
- `shares`: Integer (optional, default: 0) - Number of shares
- `comments`: Integer (optional, default: 0) - Number of comments
- `saves`: Integer (optional, default: 0) - Number of saves/bookmarks
- `video_views`: Integer (optional, default: 0) - Number of video views
- `video_completion_rate`: Float (optional, default: 0.0) - Video completion rate as percentage (0-100)
- `time_spent`: Float (optional, default: 0.0) - Total time spent in seconds

#### Response:
Returns an `EngagementMetrics` object with the tracked metrics.

### POST `/analytics/track-seo`
Track SEO effectiveness metrics for content.

#### Parameters:
- `content_id`: String (required) - Identifier of the content
- `channel`: String (required) - Channel where content is published
- `organic_traffic`: Integer (optional, default: 0) - Organic traffic to the content
- `impressions`: Integer (optional, default: 0) - Organic impressions
- `backlinks`: Integer (optional, default: 0) - Number of backlinks
- `domain_authority`: Float (optional, default: 0.0) - Domain authority score (0-100)

#### Response:
Returns a `SEOEffectiveness` object with the tracked metrics.

### POST `/analytics/track-interaction`
Track user interaction with content.

#### Parameters:
- `content_id`: String (required) - Identifier of the content
- `session_id`: String (required) - Session identifier
- `interaction_type`: String (required) - Type of interaction (view, click, share, comment, etc.)
- `user_id`: String (optional) - User identifier
- `duration`: Float (optional) - Duration of interaction in seconds
- `scroll_depth`: Float (optional) - Scroll depth achieved (0-100%)

#### Response:
Returns a `UserInteraction` object with the tracked interaction.

### POST `/analytics/query`
Query analytics data based on specified parameters.

#### Request Body:
````
{
  "content_ids": ["content_1", "content_2"],
  "date_range_start": "2023-01-01T00:00:00Z",
  "date_range_end": "2023-01-31T23:59:59Z",
  "metric_types": ["content_performance", "engagement_metrics"],
  "source_channels": ["website", "blog"],
  "user_ids": ["user_1", "user_2"],
  "limit": 100,
  "offset": 0,
  "sort_by": "timestamp",
  "sort_order": "desc",
  "include_aggregates": true,
  "group_by": "day"
}
````

#### Response:
Returns an `AnalyticsResponse` object with query results.

### POST `/analytics/validate-data`
Validate analytics data for correctness and privacy compliance.

#### Request Body:
````
{
  "data_type": "content_performance",
  "data_payload": {
    "content_id": "content_123",
    "views": 1000,
    "unique_visitors": 800,
    "engagement_rate": 2.5
  },
  "content_id": "content_123",
  "source_channel": "website",
  "privacy_compliance_required": true
}
````

#### Response:
Returns an `AnalyticsValidationResponse` object with validation results.

### GET `/analytics/performance-trends/{content_id}`
Get performance trends for a specific content item.

#### Parameters:
- `content_id`: String (required) - Identifier of the content
- `days_back`: Integer (optional, default: 30, max: 365) - Number of days to look back for trends

#### Response:
Returns a dictionary with trend analysis results.

### POST `/analytics/generate-report`
Generate a comprehensive performance report for specified content.

#### Parameters (Query):
- `content_ids`: Array of strings (required) - List of content IDs to include in report
- `start_date`: String (required) - Start date for the report period (ISO format)
- `end_date`: String (required) - End date for the report period (ISO format)

#### Response:
Returns a dictionary with comprehensive performance report.

## Insights Endpoints

### POST `/insights/generate-insights`
Generate insights for a specific content item based on its performance data.

#### Parameters:
- `content_id`: String (required) - Identifier of the content to analyze
- `include_performance`: Boolean (optional, default: true) - Whether to include performance data analysis
- `include_engagement`: Boolean (optional, default: true) - Whether to include engagement data analysis
- `include_seo`: Boolean (optional, default: true) - Whether to include SEO data analysis

#### Response:
Returns a `ContentInsightsResponse` object with insights and recommendations.

### POST `/insights/query-insights`
Query insights and recommendations based on specified parameters.

#### Request Body:
````
{
  "content_ids": ["content_1", "content_2"],
  "categories": ["performance", "engagement"],
  "date_range_start": "2023-01-01T00:00:00Z",
  "date_range_end": "2023-01-31T23:59:59Z",
  "min_significance": 0.3,
  "min_confidence": 0.5,
  "include_recommendations": true,
  "include_trends": true,
  "limit": 50,
  "offset": 0,
  "sort_by": "significance_score",
  "sort_order": "desc"
}
````

#### Response:
Returns a `ContentInsightsResponse` object with query results.

### POST `/insights/trend-analysis`
Analyze trends for content performance metrics.

#### Parameters (Query):
- `content_ids`: Array of strings (required) - List of content IDs to analyze
- `metric_type`: String (optional, default: "views") - Type of metric to analyze (views, engagement_rate, organic_traffic, revenue, conversions)
- `days_back`: Integer (optional, default: 30, max: 365) - Number of days to look back for trend analysis

#### Response:
Returns an array of `TrendAnalysis` objects with trend analysis results.

### POST `/insights/personalized-recommendations`
Generate personalized recommendations based on user preferences.

#### Request Body:
````
{
  "profile_id": "profile_123",
  "user_id": "user_123",
  "preferred_categories": ["performance", "engagement"],
  "recommendation_threshold": 0.3,
  "notification_preferences": {"performance": true, "engagement": true},
  "content_focus_areas": ["engagement", "conversions"],
  "update_frequency": "daily"
}
````

#### Parameters (Query):
- `content_ids`: Array of strings (required) - List of content IDs to generate recommendations for

#### Response:
Returns an array of recommendation objects with personalized recommendations.

### POST `/insights/comparative-analysis`
Perform comparative analysis between multiple content pieces.

#### Parameters (Query):
- `content_ids`: Array of strings (required, min: 2, max: 10) - List of content IDs to compare
- `comparison_basis`: String (optional, default: "engagement") - Basis for comparison (engagement, views, seo, performance, revenue)

#### Response:
Returns a `ComparativeAnalysis` object with comparison results.

### POST `/insights/predictive-insights`
Generate predictive insights for future content performance.

#### Parameters:
- `content_id`: String (required) - Content ID to predict for
- `prediction_type`: String (optional, default: "engagement") - Type of prediction (engagement, traffic, revenue, performance)
- `prediction_horizon`: String (optional, default: "7d") - Time horizon for prediction (7d, 14d, 30d, 60d)

#### Response:
Returns an array of `PredictiveInsight` objects with predictions.

### GET `/insights/insight-categories`
Get list of available insight categories.

#### Response:
Returns an array of available insight category strings.

### GET `/insights/recommendation-priorities`
Get list of available recommendation priorities.

#### Response:
Returns an array of available recommendation priority strings.

### GET `/insights/trend-directions`
Get list of available trend directions.

#### Response:
Returns an array of available trend direction strings.

## Common Responses

### Success Response
Most successful API calls return a 200 OK status with the requested data in the response body.

### Error Response
When an error occurs, the API returns an appropriate HTTP status code and an error message:

````
{
  "detail": "Error description"
}
````

## Error Codes
- 400: Bad Request - Invalid input parameters
- 401: Unauthorized - Invalid or missing API key
- 404: Not Found - Requested resource not found
- 422: Unprocessable Entity - Validation error
- 500: Internal Server Error - Server-side error occurred

## Rate Limiting
The API implements rate limiting to prevent abuse. Exceeding the rate limit will result in a 429 status code. The rate limits are configurable and typically allow 100 requests per minute per API key.

## Data Privacy
All analytics and insights endpoints respect user privacy and comply with GDPR regulations. Personal data is anonymized when privacy compliance is required.