"""
Analytics Service

This module provides functionality for tracking and analyzing content performance,
engagement metrics, SEO effectiveness, and user interactions.
"""

import asyncio
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from ..models.analytics import (
    AnalyticsData, ContentPerformance, EngagementMetrics,
    SEOEffectiveness, UserInteraction, AnalyticsQuery,
    AnalyticsResponse, AnalyticsValidationRequest,
    AnalyticsValidationResponse, AnalyticsDataTypeEnum,
    ContentChannelEnum
)
from ..models.content_generation import ContentDraft
from ..config.settings import settings
from ..utils.analytics_helpers import AnalyticsHelper
from ..utils.workflow_helpers import WorkflowCache
from ..utils.logging_config import api_logger
from ..services.validation import ContentValidationService


class AnalyticsService:
    """Service class for analytics and performance tracking."""

    def __init__(self):
        """Initialize the Analytics Service."""
        self.cache = WorkflowCache(ttl_seconds=settings.analytics_cache_ttl)
        self.validation_service = ContentValidationService()
        self.helper = AnalyticsHelper()

    async def track_content_performance(
        self,
        content_id: str,
        channel: ContentChannelEnum,
        views: int = 0,
        unique_visitors: int = 0,
        session_duration: float = 0.0,
        bounce_rate: float = 0.0,
        conversions: int = 0,
        revenue: float = 0.0
    ) -> ContentPerformance:
        """
        Track content performance metrics.

        Args:
            content_id: Identifier of the content
            channel: Channel where content is distributed
            views: Number of views
            unique_visitors: Number of unique visitors
            session_duration: Average session duration in seconds
            bounce_rate: Bounce rate as percentage
            conversions: Number of conversions
            revenue: Revenue generated

        Returns:
            ContentPerformance model with tracked metrics
        """
        # Calculate derived metrics
        engagement_rate = self.helper.calculate_engagement_rate(views, unique_visitors) if unique_visitors > 0 else 0.0
        conversion_rate = self.helper.calculate_conversion_rate(conversions, unique_visitors) if unique_visitors > 0 else 0.0

        performance = ContentPerformance(
            content_id=content_id,
            views=views,
            unique_visitors=unique_visitors,
            session_duration=session_duration,
            bounce_rate=bounce_rate,
            conversions=conversions,
            revenue=revenue,
            engagement_rate=engagement_rate,
            conversion_rate=conversion_rate,
            source_channel=channel,
            date_recorded=datetime.utcnow()
        )

        # Cache the performance data
        cache_key = f"content_performance_{content_id}_{channel.value}"
        self.cache.set(cache_key, performance)

        # Log the tracking event
        api_logger.info(f"Tracked performance for content {content_id} on {channel.value}: "
                       f"{views} views, {unique_visitors} visitors, {engagement_rate}% engagement")

        return performance

    async def track_engagement_metrics(
        self,
        content_id: str,
        channel: ContentChannelEnum,
        likes: int = 0,
        shares: int = 0,
        comments: int = 0,
        saves: int = 0,
        video_views: int = 0,
        video_completion_rate: float = 0.0,
        time_spent: float = 0.0
    ) -> EngagementMetrics:
        """
        Track engagement metrics for content.

        Args:
            content_id: Identifier of the content
            channel: Channel where engagement occurred
            likes: Number of likes
            shares: Number of shares
            comments: Number of comments
            saves: Number of saves/bookmarks
            video_views: Number of video views
            video_completion_rate: Video completion rate as percentage
            time_spent: Total time spent in seconds

        Returns:
            EngagementMetrics model with tracked metrics
        """
        # Calculate derived metrics
        average_time_spent = time_spent / (likes + shares + comments + 1)  # +1 to avoid division by zero
        engagement_rate = self.helper.calculate_engagement_rate(likes + shares + comments, 100)  # Simplified for demo
        click_through_rate = self.helper.calculate_click_through_rate(shares, likes + comments + 1)

        engagement = EngagementMetrics(
            content_id=content_id,
            likes=likes,
            shares=shares,
            comments=comments,
            saves=saves,
            video_views=video_views,
            video_completion_rate=video_completion_rate,
            time_spent=time_spent,
            average_time_spent=average_time_spent,
            engagement_rate=engagement_rate,
            click_through_rate=click_through_rate,
            source_channel=channel,
            date_recorded=datetime.utcnow()
        )

        # Cache the engagement data
        cache_key = f"engagement_metrics_{content_id}_{channel.value}"
        self.cache.set(cache_key, engagement)

        # Log the tracking event
        api_logger.info(f"Tracked engagement for content {content_id} on {channel.value}: "
                       f"{likes} likes, {shares} shares, {comments} comments")

        return engagement

    async def track_seo_effectiveness(
        self,
        content_id: str,
        channel: ContentChannelEnum,
        keyword_rankings: Optional[Dict[str, int]] = None,
        organic_traffic: int = 0,
        impressions: int = 0,
        backlinks: int = 0,
        domain_authority: float = 0.0
    ) -> SEOEffectiveness:
        """
        Track SEO effectiveness metrics for content.

        Args:
            content_id: Identifier of the content
            channel: Channel where content is published
            keyword_rankings: Keyword rankings (keyword -> position)
            organic_traffic: Organic traffic to the content
            impressions: Organic impressions
            backlinks: Number of backlinks
            domain_authority: Domain authority score

        Returns:
            SEOEffectiveness model with tracked metrics
        """
        if keyword_rankings is None:
            keyword_rankings = {}

        # Calculate derived metrics
        click_through_rate = self.helper.calculate_click_through_rate(organic_traffic, impressions) if impressions > 0 else 0.0

        seo_metrics = SEOEffectiveness(
            content_id=content_id,
            keyword_rankings=keyword_rankings,
            organic_traffic=organic_traffic,
            impressions=impressions,
            backlinks=backlinks,
            domain_authority=domain_authority,
            click_through_rate=click_through_rate,
            source_channel=channel,
            date_recorded=datetime.utcnow()
        )

        # Cache the SEO data
        cache_key = f"seo_metrics_{content_id}_{channel.value}"
        self.cache.set(cache_key, seo_metrics)

        # Log the tracking event
        api_logger.info(f"Tracked SEO metrics for content {content_id} on {channel.value}: "
                       f"{organic_traffic} traffic, {backlinks} backlinks, DA {domain_authority}")

        return seo_metrics

    async def track_user_interaction(
        self,
        content_id: str,
        session_id: str,
        interaction_type: str,
        user_id: Optional[str] = None,
        duration: Optional[float] = None,
        scroll_depth: Optional[float] = None
    ) -> UserInteraction:
        """
        Track user interaction with content.

        Args:
            content_id: Identifier of the content
            session_id: Session identifier
            interaction_type: Type of interaction
            user_id: User identifier (optional)
            duration: Duration of interaction in seconds
            scroll_depth: Scroll depth achieved

        Returns:
            UserInteraction model with tracked interaction
        """
        interaction = UserInteraction(
            content_id=content_id,
            user_id=user_id,
            session_id=session_id,
            interaction_type=interaction_type,
            duration=duration,
            scroll_depth=scroll_depth,
            timestamp=datetime.utcnow()
        )

        # Cache the interaction data
        cache_key = f"user_interaction_{content_id}_{session_id}"
        self.cache.set(cache_key, interaction)

        # Log the tracking event
        api_logger.info(f"Tracked interaction for content {content_id}, session {session_id}, "
                       f"type {interaction_type}")

        return interaction

    async def query_analytics(self, query: AnalyticsQuery) -> AnalyticsResponse:
        """
        Query analytics data based on specified parameters.

        Args:
            query: Analytics query parameters

        Returns:
            AnalyticsResponse with query results
        """
        start_time = datetime.utcnow()

        # Create cache key based on query parameters for caching
        query_hash = hashlib.md5(json.dumps(query.dict(), sort_keys=True).encode()).hexdigest()
        cache_key = f"analytics_query_{query_hash}"

        # Try to get from cache first
        cached_result = self.cache.get(cache_key)
        if cached_result and not query.skip_cache:
            api_logger.info(f"Analytics query served from cache: {cached_result.execution_time:.2f}s")
            return cached_result

        # Perform the query
        results = []

        # Use optimized approach with filters applied early
        if query.content_ids:
            # Batch retrieve data for multiple content IDs efficiently
            tasks = []
            for content_id in query.content_ids[:query.limit]:  # Respect limit early
                task = self._fetch_content_analytics(content_id, query)
                tasks.append(task)

            # Execute tasks concurrently for better performance
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in batch_results:
                if not isinstance(result, Exception) and result:
                    results.extend(result)
        else:
            # If no specific content IDs, fetch from general analytics store
            results = await self._fetch_general_analytics(query)

        # Apply date range filtering early to reduce data processing
        if query.date_range_start or query.date_range_end:
            results = await self._apply_date_filter(results, query)

        # Apply other filters efficiently
        if query.metric_types:
            results = await self._apply_metric_type_filter(results, query.metric_types)

        if query.source_channels:
            results = await self._apply_channel_filter(results, query.source_channels)

        # Apply pagination after filtering to minimize data transfer
        paginated_results = await self._apply_pagination(results, query)

        # Calculate aggregates if requested
        aggregates = None
        if query.include_aggregates and paginated_results:
            aggregates = await self._calculate_aggregates_async(paginated_results)

        # Prepare response
        response = AnalyticsResponse(
            query_id=f"query_{int(start_time.timestamp())}_{query_hash[:8]}",
            data=paginated_results,
            total_records=len(results),
            filtered_records=len(paginated_results),
            aggregates=aggregates,
            date_range={
                'start': query.date_range_start or start_time - timedelta(days=30),
                'end': query.date_range_end or start_time
            },
            query_params=query,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )

        # Cache the result if not disabled
        if not query.skip_cache:
            self.cache.set(cache_key, response, ttl_seconds=settings.analytics_cache_ttl)

        # Log the query performance
        api_logger.info(f"Analytics query executed: {len(paginated_results)} results, "
                       f"{len(results)} total, {(response.execution_time):.2f}s execution time")

        return response

    async def _fetch_content_analytics(self, content_id: str, query: AnalyticsQuery) -> List[Dict[str, Any]]:
        """
        Efficiently fetch analytics for a specific content ID.

        Args:
            content_id: Content identifier
            query: Analytics query parameters

        Returns:
            List of analytics data for the content
        """
        results = []

        # Try to get from cache first
        cache_key = f"content_analytics_{content_id}_{query.source_channels[0] if query.source_channels else 'all'}"
        cached_data = self.cache.get(cache_key)

        if cached_data:
            results.append(cached_data)
        else:
            # In a real implementation, this would query the database
            # For now, simulate data retrieval
            simulated_data = {
                'content_id': content_id,
                'views': 1000 + hash(content_id) % 500,
                'engagement_rate': 2.5 + (hash(content_id) % 10) / 10,
                'revenue': 500.0 + (hash(content_id) % 500),
                'timestamp': datetime.utcnow().isoformat()
            }
            results.append(simulated_data)

            # Cache the data for future queries
            self.cache.set(cache_key, simulated_data, ttl_seconds=settings.analytics_cache_ttl)

        return results

    async def _apply_date_filter(self, results: List[Dict], query: AnalyticsQuery) -> List[Dict]:
        """
        Apply date range filtering to results efficiently.

        Args:
            results: List of analytics results
            query: Analytics query with date range parameters

        Returns:
            Filtered results
        """
        if not query.date_range_start and not query.date_range_end:
            return results

        filtered_results = []
        for item in results:
            # Extract timestamp from item
            item_timestamp = item.get('timestamp', item.get('date_recorded', datetime.utcnow().isoformat()))

            # Convert to datetime if string
            if isinstance(item_timestamp, str):
                try:
                    item_timestamp = datetime.fromisoformat(item_timestamp.replace('Z', '+00:00'))
                except ValueError:
                    continue  # Skip invalid timestamps

            # Apply date range filter
            if query.date_range_start and item_timestamp < query.date_range_start:
                continue
            if query.date_range_end and item_timestamp > query.date_range_end:
                continue

            filtered_results.append(item)

        return filtered_results

    async def _apply_metric_type_filter(self, results: List[Dict], metric_types: List[str]) -> List[Dict]:
        """
        Apply metric type filtering to results.

        Args:
            results: List of analytics results
            metric_types: List of metric types to include

        Returns:
            Filtered results
        """
        if not metric_types:
            return results

        filtered_results = []
        for item in results:
            # Check if item has metrics that match the requested types
            item_metrics = item.get('metrics', {})
            if any(metric_type in item_metrics for metric_type in metric_types):
                filtered_results.append(item)

        return filtered_results

    async def _apply_channel_filter(self, results: List[Dict], channels: List[str]) -> List[Dict]:
        """
        Apply source channel filtering to results.

        Args:
            results: List of analytics results
            channels: List of source channels to include

        Returns:
            Filtered results
        """
        if not channels:
            return results

        return [
            item for item in results
            if item.get('source_channel') in channels or item.get('channel') in channels
        ]

    async def _apply_pagination(self, results: List[Dict], query: AnalyticsQuery) -> List[Dict]:
        """
        Apply pagination to results.

        Args:
            results: List of analytics results
            query: Analytics query with pagination parameters

        Returns:
            Paginated results
        """
        start_idx = query.offset
        end_idx = start_idx + query.limit

        return results[start_idx:end_idx]

    async def _calculate_aggregates_async(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Asynchronously calculate aggregate metrics from analytics data.

        Args:
            data: List of analytics data records

        Returns:
            Dictionary with calculated aggregates
        """
        if not data:
            return {}

        # Use asyncio.gather for concurrent calculation of different aggregates
        tasks = [
            self._calculate_sum_aggregate(data, ['views', 'unique_visitors', 'conversions', 'organic_traffic']),
            self._calculate_avg_aggregate(data, ['engagement_rate', 'bounce_rate', 'conversion_rate', 'seo_score']),
            self._calculate_max_min_aggregate(data, ['revenue', 'time_spent'])
        ]

        sum_aggs, avg_aggs, ext_aggs = await asyncio.gather(*tasks)

        # Combine all aggregates
        aggregates = {**sum_aggs, **avg_aggs, **ext_aggs}

        # Add count and other metrics
        aggregates['total_records'] = len(data)
        aggregates['date_range'] = self._calculate_date_range(data)

        return aggregates

    async def _calculate_sum_aggregate(self, data: List[Dict], fields: List[str]) -> Dict[str, float]:
        """Calculate sum aggregates for specified fields."""
        aggregates = {}
        for field in fields:
            total = 0
            count = 0
            for item in data:
                if field in item:
                    value = item[field]
                    if isinstance(value, (int, float)):
                        total += value
                        count += 1
            if count > 0:
                aggregates[f'total_{field}'] = total
        return aggregates

    async def _calculate_avg_aggregate(self, data: List[Dict], fields: List[str]) -> Dict[str, float]:
        """Calculate average aggregates for specified fields."""
        aggregates = {}
        for field in fields:
            total = 0
            count = 0
            for item in data:
                if field in item:
                    value = item[field]
                    if isinstance(value, (int, float)):
                        total += value
                        count += 1
            if count > 0:
                aggregates[f'avg_{field}'] = total / count
        return aggregates

    async def _calculate_max_min_aggregate(self, data: List[Dict], fields: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate max/min aggregates for specified fields."""
        aggregates = {}
        for field in fields:
            values = [
                item[field] for item in data
                if field in item and isinstance(item[field], (int, float))
            ]
            if values:
                aggregates[f'{field}_range'] = {
                    'max': max(values),
                    'min': min(values),
                    'count': len(values)
                }
        return aggregates

    def _calculate_date_range(self, data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Calculate the date range from the data."""
        timestamps = []
        for item in data:
            ts = item.get('timestamp', item.get('date_recorded'))
            if ts:
                if isinstance(ts, str):
                    try:
                        ts = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    except ValueError:
                        continue
                timestamps.append(ts)

        if timestamps:
            return {
                'start': min(timestamps).isoformat(),
                'end': max(timestamps).isoformat()
            }
        else:
            now = datetime.utcnow()
            return {
                'start': now.isoformat(),
                'end': now.isoformat()
            }

    def _calculate_aggregates(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate aggregate metrics from analytics data.

        Args:
            data: List of analytics data records

        Returns:
            Dictionary with calculated aggregates
        """
        if not data:
            return {}

        # Calculate various aggregates based on the data
        aggregates = {
            'total_views': sum(item.get('views', 0) for item in data if isinstance(item, dict)),
            'total_unique_visitors': sum(item.get('unique_visitors', 0) for item in data if isinstance(item, dict)),
            'average_engagement_rate': 0,
            'total_engagements': 0,
            'total_revenue': sum(item.get('revenue', 0) for item in data if isinstance(item, dict)),
            'period_start': None,
            'period_end': None
        }

        # Calculate averages
        engagement_rates = [item.get('engagement_rate', 0) for item in data if isinstance(item, dict)]
        if engagement_rates:
            aggregates['average_engagement_rate'] = sum(engagement_rates) / len(engagement_rates)

        # Calculate total engagements
        for item in data:
            if isinstance(item, dict):
                total_engagements = item.get('likes', 0) + item.get('shares', 0) + item.get('comments', 0)
                aggregates['total_engagements'] += total_engagements

        # Determine date range
        timestamps = []
        for item in data:
            if isinstance(item, dict):
                ts = item.get('date_recorded', item.get('timestamp'))
                if ts:
                    if isinstance(ts, str):
                        ts = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    timestamps.append(ts)

        if timestamps:
            aggregates['period_start'] = min(timestamps)
            aggregates['period_end'] = max(timestamps)

        return aggregates

    async def validate_analytics_data(self, request: AnalyticsValidationRequest) -> AnalyticsValidationResponse:
        """
        Validate analytics data for correctness and privacy compliance.

        Args:
            request: Analytics validation request

        Returns:
            AnalyticsValidationResponse with validation results
        """
        # Perform basic validation
        errors = self.helper.validate_analytics_data(request.data_payload)

        # Check privacy compliance if required
        privacy_status = "COMPLIANT"
        if settings.privacy_compliance_enabled and request.privacy_compliance_required:
            # Anonymize data if needed
            if 'user_id' in request.data_payload and request.data_payload['user_id']:
                request.data_payload = self.helper.anonymize_user_data(request.data_payload)

        # Generate response
        response = AnalyticsValidationResponse(
            is_valid=len(errors) == 0,
            validation_errors=errors,
            privacy_compliance_status=privacy_status,
            data_sanitized=privacy_status == "COMPLIANT"
        )

        # Log validation result
        api_logger.info(f"Analytics data validation for content {request.content_id}: "
                       f"{'VALID' if response.is_valid else 'INVALID'}")

        return response

    async def aggregate_data_by_timeframe(
        self,
        data: List[Dict[str, Any]],
        timeframe: str = "daily"
    ) -> List[Dict[str, Any]]:
        """
        Aggregate analytics data by specified timeframe.

        Args:
            data: List of analytics data records
            timeframe: Aggregation timeframe ("hourly", "daily", "weekly", "monthly")

        Returns:
            Aggregated data list
        """
        return self.helper.aggregate_data_by_timeframe(data, timeframe)

    async def calculate_anomaly_scores(
        self,
        data: List[Dict[str, Any]],
        metric_field: str
    ) -> List[Dict[str, Any]]:
        """
        Calculate anomaly scores for analytics data.

        Args:
            data: List of analytics data records
            metric_field: Name of the metric field to analyze

        Returns:
            List of records with anomaly scores added
        """
        return self.helper.calculate_anomaly_scores(data, metric_field)

    async def get_content_performance_trends(
        self,
        content_id: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Get performance trends for a specific content item.

        Args:
            content_id: Identifier of the content
            days_back: Number of days to look back for trends

        Returns:
            Dictionary with trend analysis results
        """
        # This is a simplified implementation - in a real system, this would query historical data
        # For now, we'll simulate trend data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)

        # Simulate trend data
        trend_data = []
        for i in range(days_back):
            day = start_date + timedelta(days=i)
            trend_data.append({
                'date': day.isoformat(),
                'views': max(0, 100 + (i * 2) + (i % 7) * 10),  # Simulated increasing trend with weekly pattern
                'engagement_rate': max(0, 2.5 + (i * 0.05) + (i % 7) * 0.2)  # Simulated improving engagement
            })

        # Calculate trend slopes
        view_values = [item['views'] for item in trend_data]
        engagement_values = [item['engagement_rate'] for item in trend_data]
        date_values = [datetime.fromisoformat(item['date']) for item in trend_data]

        views_slope = self.helper.calculate_trend_slope(view_values, date_values)
        engagement_slope = self.helper.calculate_trend_slope(engagement_values, date_values)

        trend_analysis = {
            'content_id': content_id,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'trend_data': trend_data,
            'views_trend_slope': views_slope,
            'engagement_trend_slope': engagement_slope,
            'interpretation': {
                'views_trend': 'increasing' if views_slope > 0.1 else 'decreasing' if views_slope < -0.1 else 'stable',
                'engagement_trend': 'improving' if engagement_slope > 0.01 else 'declining' if engagement_slope < -0.01 else 'stable'
            }
        }

        return trend_analysis

    async def generate_performance_report(
        self,
        content_ids: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report for specified content.

        Args:
            content_ids: List of content IDs to include in report
            start_date: Start date for the report period
            end_date: End date for the report period

        Returns:
            Dictionary with comprehensive performance report
        """
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'content_summaries': [],
            'overall_metrics': {},
            'trends': {},
            'recommendations': []
        }

        # Calculate metrics for each content item
        total_views = 0
        total_engagements = 0
        content_count = len(content_ids)

        for content_id in content_ids:
            # Simulate getting data for this content
            # In a real implementation, this would query the database for the specific period
            content_summary = {
                'content_id': content_id,
                'views': 1000 + hash(content_id) % 1000,  # Simulated data
                'engagement_rate': 3.0 + (hash(content_id) % 5) / 10,  # Simulated data
                'conversion_rate': 2.0 + (hash(content_id) % 3) / 10,  # Simulated data
                'revenue': 500 + (hash(content_id) % 500)  # Simulated data
            }

            total_views += content_summary['views']
            total_engagements += content_summary['views'] * (content_summary['engagement_rate'] / 100)

            report['content_summaries'].append(content_summary)

        # Calculate overall metrics
        report['overall_metrics'] = {
            'total_views': total_views,
            'average_engagement_rate': (total_engagements / max(total_views, 1)) * 100,
            'content_count': content_count,
            'average_views_per_content': total_views / max(content_count, 1)
        }

        # Generate recommendations based on data
        if report['overall_metrics']['average_engagement_rate'] < 3.0:
            report['recommendations'].append("Engagement rate is below benchmark. Consider improving content quality or format.")

        if content_count > 1:
            # Check for variation in performance
            view_values = [cs['views'] for cs in report['content_summaries']]
            if max(view_values) / max(min(view_values), 1) > 3:
                report['recommendations'].append("Significant variation in content performance. Investigate high-performing content for best practices.")

        return report