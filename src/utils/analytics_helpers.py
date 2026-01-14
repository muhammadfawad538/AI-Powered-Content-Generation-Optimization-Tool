"""
Analytics Helper Utilities

This module provides utility functions for analytics and data processing,
including statistical calculations, data transformations, and privacy controls.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from ..config.settings import settings


class AnalyticsDataType(str, Enum):
    """Enumeration of analytics data types."""
    CONTENT_PERFORMANCE = "content_performance"
    ENGAGEMENT_METRICS = "engagement_metrics"
    SEO_EFFECTIVENESS = "seo_effectiveness"
    USER_INTERACTION = "user_interaction"
    TREND_ANALYSIS = "trend_analysis"


@dataclass
class AnalyticsQueryParams:
    """Parameters for analytics queries."""
    content_ids: Optional[List[str]] = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    metric_types: Optional[List[str]] = None
    group_by: Optional[str] = None
    limit: int = 100
    offset: int = 0
    order_by: str = "timestamp"
    order_direction: str = "desc"


class AnalyticsHelper:
    """Utility class for analytics operations."""

    @staticmethod
    def calculate_engagement_rate(interactions: int, impressions: int) -> float:
        """
        Calculate engagement rate as a percentage.

        Args:
            interactions: Number of user interactions
            impressions: Number of impressions

        Returns:
            Engagement rate as a percentage (0-100)
        """
        if impressions == 0:
            return 0.0
        return round((interactions / impressions) * 100, 2)

    @staticmethod
    def calculate_conversion_rate(conversions: int, visitors: int) -> float:
        """
        Calculate conversion rate as a percentage.

        Args:
            conversions: Number of conversions
            visitors: Number of visitors

        Returns:
            Conversion rate as a percentage (0-100)
        """
        if visitors == 0:
            return 0.0
        return round((conversions / visitors) * 100, 2)

    @staticmethod
    def calculate_growth_rate(current_value: float, previous_value: float) -> float:
        """
        Calculate growth rate as a percentage.

        Args:
            current_value: Current value
            previous_value: Previous value

        Returns:
            Growth rate as a percentage
        """
        if previous_value == 0:
            return 0.0 if current_value == 0 else float('inf')
        return round(((current_value - previous_value) / previous_value) * 100, 2)

    @staticmethod
    def calculate_average_time_on_page(total_time: float, views: int) -> float:
        """
        Calculate average time spent on page.

        Args:
            total_time: Total time spent in seconds
            views: Number of views

        Returns:
            Average time in seconds
        """
        if views == 0:
            return 0.0
        return round(total_time / views, 2)

    @staticmethod
    def calculate_bounce_rate(bounces: int, entrances: int) -> float:
        """
        Calculate bounce rate as a percentage.

        Args:
            bounces: Number of bounces
            entrances: Number of entrances

        Returns:
            Bounce rate as a percentage (0-100)
        """
        if entrances == 0:
            return 0.0
        return round((bounces / entrances) * 100, 2)

    @staticmethod
    def calculate_click_through_rate(clicks: int, impressions: int) -> float:
        """
        Calculate click-through rate as a percentage.

        Args:
            clicks: Number of clicks
            impressions: Number of impressions

        Returns:
            Click-through rate as a percentage (0-100)
        """
        if impressions == 0:
            return 0.0
        return round((clicks / impressions) * 100, 2)

    @staticmethod
    def calculate_trend_slope(values: List[float], timestamps: List[datetime]) -> float:
        """
        Calculate the slope of a trend using linear regression.

        Args:
            values: List of metric values
            timestamps: List of corresponding timestamps

        Returns:
            Slope of the trend line
        """
        if len(values) < 2 or len(timestamps) < 2:
            return 0.0

        # Convert timestamps to numeric values (seconds since epoch)
        x_values = [(ts - timestamps[0]).total_seconds() for ts in timestamps]

        # Calculate slope using numpy
        coefficients = np.polyfit(x_values, values, 1)
        return float(coefficients[0])

    @staticmethod
    def calculate_correlation(x_values: List[float], y_values: List[float]) -> float:
        """
        Calculate Pearson correlation coefficient between two sets of values.

        Args:
            x_values: First set of values
            y_values: Second set of values

        Returns:
            Correlation coefficient (-1 to 1)
        """
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0

        # Convert to numpy arrays and calculate correlation
        x_array = np.array(x_values)
        y_array = np.array(y_values)

        # Handle case where arrays are constant
        if np.std(x_array) == 0 or np.std(y_array) == 0:
            return 0.0

        correlation_matrix = np.corrcoef(x_array, y_array)
        return float(correlation_matrix[0, 1])

    @staticmethod
    def calculate_percentile(data: List[float], percentile: float) -> float:
        """
        Calculate percentile of a dataset.

        Args:
            data: List of numeric values
            percentile: Percentile to calculate (0-100)

        Returns:
            Calculated percentile value
        """
        if not data:
            return 0.0

        return float(np.percentile(data, percentile))

    @staticmethod
    def anonymize_user_data(user_data: Dict[str, Any], fields_to_anonymize: List[str] = None) -> Dict[str, Any]:
        """
        Anonymize user data for privacy compliance.

        Args:
            user_data: Dictionary containing user data
            fields_to_anonymize: List of field names to anonymize

        Returns:
            Anonymized data dictionary
        """
        if fields_to_anonymize is None:
            fields_to_anonymize = ['email', 'phone', 'address', 'ip_address', 'user_id']

        anonymized_data = user_data.copy()

        for field in fields_to_anonymize:
            if field in anonymized_data:
                if isinstance(anonymized_data[field], str):
                    # Hash the value to anonymize while preserving data type
                    hashed_value = hashlib.sha256(anonymized_data[field].encode()).hexdigest()
                    anonymized_data[field] = hashed_value[:10]  # Truncate for readability
                else:
                    anonymized_data[field] = "ANONYMIZED"

        return anonymized_data

    @staticmethod
    def filter_data_by_privacy_compliance(
        data: List[Dict[str, Any]],
        content_owner_id: str,
        requesting_user_id: str
    ) -> List[Dict[str, Any]]:
        """
        Filter data based on privacy compliance rules.

        Args:
            data: List of data records
            content_owner_id: ID of content owner
            requesting_user_id: ID of user requesting data

        Returns:
            Filtered data list based on privacy rules
        """
        if not settings.privacy_compliance_enabled:
            return data

        # For now, only return data for the requesting user or admin
        # In a real system, this would have more sophisticated access controls
        if requesting_user_id == content_owner_id:
            return data
        else:
            # Return only aggregated/anonymized data for other users
            return [AnalyticsHelper.anonymize_user_data(record) for record in data]

    @staticmethod
    def aggregate_data_by_timeframe(
        data: List[Dict[str, Any]],
        timeframe: str = "daily",
        date_field: str = "timestamp"
    ) -> List[Dict[str, Any]]:
        """
        Aggregate data by specified timeframe.

        Args:
            data: List of data records
            timeframe: Aggregation timeframe ("hourly", "daily", "weekly", "monthly")
            date_field: Name of the date field in records

        Returns:
            Aggregated data list
        """
        if not data:
            return []

        df = pd.DataFrame(data)

        # Convert date field to datetime if it's not already
        df[date_field] = pd.to_datetime(df[date_field])

        # Group by specified timeframe
        if timeframe == "hourly":
            df['group'] = df[date_field].dt.floor('H')
        elif timeframe == "daily":
            df['group'] = df[date_field].dt.date
        elif timeframe == "weekly":
            df['group'] = df[date_field].dt.to_period('W')
        elif timeframe == "monthly":
            df['group'] = df[date_field].dt.to_period('M')
        else:
            # Default to daily
            df['group'] = df[date_field].dt.date

        # Perform aggregation (sum, mean, count, etc.)
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        agg_dict = {col: 'sum' for col in numeric_columns}

        # Add count for all columns
        agg_dict.update({col: 'count' for col in df.columns if col not in ['group', date_field]})

        aggregated_df = df.groupby('group').agg(agg_dict).reset_index()

        # Convert back to list of dictionaries
        result = aggregated_df.to_dict('records')

        return result

    @staticmethod
    def calculate_anomaly_scores(data: List[Dict[str, Any]], metric_field: str) -> List[Dict[str, Any]]:
        """
        Calculate anomaly scores for a specific metric in the data.

        Args:
            data: List of data records
            metric_field: Name of the metric field to analyze

        Returns:
            List of records with anomaly scores added
        """
        if not data:
            return data

        # Extract metric values
        values = [record.get(metric_field, 0) for record in data if metric_field in record]

        if len(values) < 2:
            # Add anomaly score of 0 for all records if insufficient data
            for record in data:
                record['anomaly_score'] = 0.0
            return data

        # Calculate z-scores for anomaly detection
        mean_val = np.mean(values)
        std_val = np.std(values)

        if std_val == 0:
            # If all values are the same, no anomalies
            for record in data:
                record['anomaly_score'] = 0.0
            return data

        # Calculate z-score for each value
        for record in data:
            if metric_field in record:
                value = record[metric_field]
                z_score = abs((value - mean_val) / std_val)
                # Normalize z-score to 0-1 scale for anomaly score
                anomaly_score = min(z_score / 3.0, 1.0)  # Clamp at 1.0
                record['anomaly_score'] = round(anomaly_score, 3)
            else:
                record['anomaly_score'] = 0.0

        return data

    @staticmethod
    def create_data_retention_filter(retention_days: int = None) -> datetime:
        """
        Create a date filter based on data retention policy.

        Args:
            retention_days: Number of days to retain data (uses setting if None)

        Returns:
            Cutoff date for data retention
        """
        if retention_days is None:
            retention_days = settings.analytics_retention_days

        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        return cutoff_date

    @staticmethod
    def validate_analytics_data(data: Dict[str, Any]) -> List[str]:
        """
        Validate analytics data structure and values.

        Args:
            data: Analytics data to validate

        Returns:
            List of validation errors
        """
        errors = []

        # Check required fields based on data type
        if 'data_type' in data:
            required_fields = {
                AnalyticsDataType.CONTENT_PERFORMANCE: ['content_id', 'views', 'engagement_rate'],
                AnalyticsDataType.ENGAGEMENT_METRICS: ['content_id', 'likes', 'shares', 'comments'],
                AnalyticsDataType.SEO_EFFECTIVENESS: ['content_id', 'keyword_rankings', 'traffic'],
                AnalyticsDataType.USER_INTERACTION: ['user_id', 'content_id', 'interaction_type'],
                AnalyticsDataType.TREND_ANALYSIS: ['content_id', 'metric_type', 'timestamp', 'value']
            }

            if data['data_type'] in required_fields:
                for field in required_fields[data['data_type']]:
                    if field not in data:
                        errors.append(f"Missing required field '{field}' for data type {data['data_type']}")

        # Validate numeric fields
        numeric_fields = ['views', 'engagement_rate', 'likes', 'shares', 'comments', 'traffic', 'value']
        for field in numeric_fields:
            if field in data:
                try:
                    val = float(data[field])
                    if val < 0:
                        errors.append(f"Field '{field}' must be non-negative, got {val}")
                except (ValueError, TypeError):
                    errors.append(f"Field '{field}' must be numeric, got {type(data[field])}")

        return errors