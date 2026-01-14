"""
Data Visualization Utilities

This module provides functions for creating visualizations of analytics data
using matplotlib and plotly for dashboards and reports.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from io import BytesIO
import base64
from enum import Enum
import seaborn as sns
from ..utils.analytics_helpers import AnalyticsHelper


class ChartType(str, Enum):
    """Enumeration of chart types."""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    AREA = "area"
    COMBO = "combo"


class VisualizationHelper:
    """Utility class for creating data visualizations."""

    @staticmethod
    def create_line_chart(
        data: List[Dict[str, Any]],
        x_field: str,
        y_field: str,
        title: str = "Line Chart",
        x_label: str = "",
        y_label: str = "",
        color: str = "#1f77b4"
    ) -> str:
        """
        Create a line chart and return as base64-encoded image.

        Args:
            data: List of data records
            x_field: Field name for x-axis
            y_field: Field name for y-axis
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            color: Line color

        Returns:
            Base64-encoded image string
        """
        if not data:
            return ""

        df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df[x_field], df[y_field], marker='o', color=color, linewidth=2, markersize=6)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True, linestyle='--', alpha=0.7)

        # Rotate x-axis labels if they're dates
        if pd.api.types.is_datetime64_any_dtype(df[x_field]):
            ax.tick_params(axis='x', rotation=45)

        # Save to bytes
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)

        return img_str

    @staticmethod
    def create_bar_chart(
        data: List[Dict[str, Any]],
        x_field: str,
        y_field: str,
        title: str = "Bar Chart",
        x_label: str = "",
        y_label: str = "",
        color: str = "#1f77b4"
    ) -> str:
        """
        Create a bar chart and return as base64-encoded image.

        Args:
            data: List of data records
            x_field: Field name for x-axis
            y_field: Field name for y-axis
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            color: Bar color

        Returns:
            Base64-encoded image string
        """
        if not data:
            return ""

        df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df[x_field], df[y_field], color=color, edgecolor='black', linewidth=0.5)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True, linestyle='--', alpha=0.7, axis='y')

        # Rotate x-axis labels if they're long
        ax.tick_params(axis='x', rotation=45)

        # Save to bytes
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)

        return img_str

    @staticmethod
    def create_interactive_line_plotly(
        data: List[Dict[str, Any]],
        x_field: str,
        y_field: str,
        title: str = "Interactive Line Chart",
        color: str = "#1f77b4"
    ) -> str:
        """
        Create an interactive line chart using Plotly.

        Args:
            data: List of data records
            x_field: Field name for x-axis
            y_field: Field name for y-axis
            title: Chart title
            color: Line color

        Returns:
            HTML string for the interactive chart
        """
        if not data:
            return ""

        df = pd.DataFrame(data)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x_field],
            y=df[y_field],
            mode='lines+markers',
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>' +
                         f'{y_field}: '+'%{y}<br>' +
                         '<extra></extra>'
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_field,
            yaxis_title=y_field,
            hovermode='x unified',
            template='plotly_white',
            height=500
        )

        return fig.to_html(include_plotlyjs=True, div_id="interactive-chart")

    @staticmethod
    def create_interactive_bar_plotly(
        data: List[Dict[str, Any]],
        x_field: str,
        y_field: str,
        title: str = "Interactive Bar Chart",
        color: str = "#1f77b4"
    ) -> str:
        """
        Create an interactive bar chart using Plotly.

        Args:
            data: List of data records
            x_field: Field name for x-axis
            y_field: Field name for y-axis
            title: Chart title
            color: Bar color

        Returns:
            HTML string for the interactive chart
        """
        if not data:
            return ""

        df = pd.DataFrame(data)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df[x_field],
            y=df[y_field],
            marker_color=color,
            hovertemplate='<b>%{x}</b><br>' +
                         f'{y_field}: '+'%{y}<br>' +
                         '<extra></extra>'
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_field,
            yaxis_title=y_field,
            hovermode='x unified',
            template='plotly_white',
            height=500
        )

        return fig.to_html(include_plotlyjs=True, div_id="interactive-bar-chart")

    @staticmethod
    def create_pie_chart(
        data: List[Dict[str, Any]],
        labels_field: str,
        values_field: str,
        title: str = "Pie Chart"
    ) -> str:
        """
        Create a pie chart and return as base64-encoded image.

        Args:
            data: List of data records
            labels_field: Field name for labels
            values_field: Field name for values
            title: Chart title

        Returns:
            Base64-encoded image string
        """
        if not data:
            return ""

        df = pd.DataFrame(data)

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            df[values_field],
            labels=df[labels_field],
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3.colors
        )

        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title(title, fontsize=14, fontweight='bold')

        # Save to bytes
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)

        return img_str

    @staticmethod
    def create_heatmap(
        data: List[Dict[str, Any]],
        row_field: str,
        col_field: str,
        value_field: str,
        title: str = "Heatmap"
    ) -> str:
        """
        Create a heatmap and return as base64-encoded image.

        Args:
            data: List of data records
            row_field: Field name for rows
            col_field: Field name for columns
            value_field: Field name for values
            title: Chart title

        Returns:
            Base64-encoded image string
        """
        if not data:
            return ""

        df = pd.DataFrame(data)

        # Pivot the data to create a matrix
        pivot_df = df.pivot_table(
            index=row_field,
            columns=col_field,
            values=value_field,
            fill_value=0
        )

        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(pivot_df.values, cmap='viridis', aspect='auto')

        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Values", rotation=-90, va="bottom")

        # Set ticks and labels
        ax.set_xticks(np.arange(len(pivot_df.columns)))
        ax.set_yticks(np.arange(len(pivot_df.index)))
        ax.set_xticklabels(pivot_df.columns)
        ax.set_yticklabels(pivot_df.index)

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha="right")

        # Add text annotations in each cell
        for i in range(len(pivot_df.index)):
            for j in range(len(pivot_df.columns)):
                text = ax.text(j, i, f"{pivot_df.iloc[i, j]:.1f}",
                              ha="center", va="center", color="white", fontsize=8)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(col_field)
        ax.set_ylabel(row_field)

        # Save to bytes
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)

        return img_str

    @staticmethod
    def create_content_performance_dashboard(
        content_data: List[Dict[str, Any]],
        engagement_data: List[Dict[str, Any]],
        seo_data: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Create a comprehensive content performance dashboard.

        Args:
            content_data: Content performance data
            engagement_data: Engagement metrics data
            seo_data: SEO effectiveness data

        Returns:
            Dictionary of chart images keyed by chart type
        """
        charts = {}

        # Content performance over time
        if content_data:
            charts['content_performance'] = VisualizationHelper.create_line_chart(
                content_data,
                'timestamp',
                'views',
                'Content Views Over Time',
                'Date',
                'Views',
                '#2ca02c'
            )

        # Engagement metrics
        if engagement_data:
            charts['engagement_metrics'] = VisualizationHelper.create_bar_chart(
                engagement_data,
                'content_id',
                'engagement_rate',
                'Engagement Rates by Content',
                'Content ID',
                'Engagement Rate (%)',
                '#ff7f0e'
            )

        # SEO effectiveness
        if seo_data:
            charts['seo_effectiveness'] = VisualizationHelper.create_line_chart(
                seo_data,
                'keyword',
                'ranking_position',
                'Keyword Rankings',
                'Keyword',
                'Ranking Position',
                '#d62728'
            )

        return charts

    @staticmethod
    def create_trend_analysis_charts(
        trend_data: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Create trend analysis charts.

        Args:
            trend_data: Trend analysis data

        Returns:
            Dictionary of trend charts
        """
        charts = {}

        if not trend_data:
            return charts

        # Convert to DataFrame
        df = pd.DataFrame(trend_data)

        # Group by metric type if available
        if 'metric_type' in df.columns:
            for metric_type in df['metric_type'].unique():
                metric_data = df[df['metric_type'] == metric_type].to_dict('records')

                charts[f'trend_{metric_type}'] = VisualizationHelper.create_line_chart(
                    metric_data,
                    'timestamp',
                    'value',
                    f'Trend Analysis - {metric_type}',
                    'Date',
                    'Value',
                    '#9467bd'
                )
        else:
            # Create a single chart if no metric type is specified
            charts['trend_overall'] = VisualizationHelper.create_line_chart(
                trend_data,
                'timestamp',
                'value',
                'Trend Analysis',
                'Date',
                'Value',
                '#9467bd'
            )

        return charts

    @staticmethod
    def create_insight_visualization(
        insight_data: List[Dict[str, Any]],
        insight_type: str
    ) -> str:
        """
        Create a visualization for specific insights.

        Args:
            insight_data: Insight data
            insight_type: Type of insight

        Returns:
            Base64-encoded image string
        """
        if not insight_data:
            return ""

        df = pd.DataFrame(insight_data)

        if insight_type == "correlation":
            # Create a scatter plot for correlation insights
            if 'x_value' in df.columns and 'y_value' in df.columns:
                return VisualizationHelper.create_scatter_plot(
                    insight_data,
                    'x_value',
                    'y_value',
                    f'Correlation Analysis: {insight_type}'
                )
        elif insight_type == "comparison":
            # Create a bar chart for comparison insights
            if 'category' in df.columns and 'value' in df.columns:
                return VisualizationHelper.create_bar_chart(
                    insight_data,
                    'category',
                    'value',
                    f'Comparison Analysis: {insight_type}',
                    'Category',
                    'Value'
                )

        # Default to line chart
        if 'timestamp' in df.columns and 'value' in df.columns:
            return VisualizationHelper.create_line_chart(
                insight_data,
                'timestamp',
                'value',
                f'Insight Analysis: {insight_type}',
                'Date',
                'Value'
            )

        return ""

    @staticmethod
    def create_scatter_plot(
        data: List[Dict[str, Any]],
        x_field: str,
        y_field: str,
        title: str = "Scatter Plot",
        color: str = "#1f77b4"
    ) -> str:
        """
        Create a scatter plot and return as base64-encoded image.

        Args:
            data: List of data records
            x_field: Field name for x-axis
            y_field: Field name for y-axis
            title: Chart title
            color: Point color

        Returns:
            Base64-encoded image string
        """
        if not data:
            return ""

        df = pd.DataFrame(data)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df[x_field], df[y_field], c=color, alpha=0.6, s=50)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_field)
        ax.set_ylabel(y_field)
        ax.grid(True, linestyle='--', alpha=0.7)

        # Add trend line if there are enough data points
        if len(df) > 2:
            z = np.polyfit(df[x_field], df[y_field], 1)
            p = np.poly1d(z)
            ax.plot(df[x_field], p(df[x_field]), color="red", linestyle="--", alpha=0.8)

        # Save to bytes
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)

        return img_str

    @staticmethod
    def generate_analytics_report(
        content_data: List[Dict[str, Any]],
        engagement_data: List[Dict[str, Any]],
        seo_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive analytics report with visualizations.

        Args:
            content_data: Content performance data
            engagement_data: Engagement metrics data
            seo_data: SEO effectiveness data

        Returns:
            Dictionary containing report data and visualizations
        """
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'summary': {},
            'charts': {},
            'insights': []
        }

        # Calculate summary statistics
        if content_data:
            views_list = [item.get('views', 0) for item in content_data]
            report['summary']['total_views'] = sum(views_list)
            report['summary']['average_views'] = sum(views_list) / len(views_list) if views_list else 0
            report['summary']['content_count'] = len(content_data)

        if engagement_data:
            engagement_rates = [item.get('engagement_rate', 0) for item in engagement_data]
            report['summary']['average_engagement_rate'] = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0

        if seo_data:
            rankings = [item.get('ranking_position', 100) for item in seo_data]
            report['summary']['average_ranking'] = sum(rankings) / len(rankings) if rankings else 100

        # Generate charts
        report['charts'] = VisualizationHelper.create_content_performance_dashboard(
            content_data, engagement_data, seo_data
        )

        # Generate insights
        if content_data and engagement_data:
            # Check for correlation between views and engagement
            helper = AnalyticsHelper()
            view_values = [item.get('views', 0) for item in content_data]
            engagement_values = [item.get('engagement_rate', 0) for item in engagement_data]

            if len(view_values) > 1 and len(engagement_values) > 1:
                correlation = helper.calculate_correlation(view_values, engagement_values)
                if abs(correlation) > 0.5:
                    insight_direction = "positive" if correlation > 0 else "negative"
                    report['insights'].append({
                        'type': 'correlation',
                        'description': f'Strong {insight_direction} correlation ({correlation:.2f}) between content views and engagement rates',
                        'significance': 'high'
                    })

        return report