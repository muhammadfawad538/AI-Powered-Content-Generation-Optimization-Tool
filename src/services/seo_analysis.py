"""
SEO Analysis Service

This module provides functionality for performing comprehensive SEO analysis
on content, including keyword analysis, readability assessment, and optimization suggestions.
"""

from typing import Dict, List
from ..models.seo_analysis import SEOAnalysisRequest, SEOAnalysisResponse, SEOSuggestion
from ..utils.seo_metrics import calculate_keyword_density, analyze_heading_structure, calculate_seo_score, extract_meta_description, extract_title_suggestions
from ..utils.quality_metrics import calculate_quality_metrics


class SEOAnalysisService:
    """Service class for performing SEO analysis on content."""

    def __init__(self):
        """Initialize the SEO Analysis Service."""
        pass

    def analyze_content(self, request: SEOAnalysisRequest) -> SEOAnalysisResponse:
        """
        Perform comprehensive SEO analysis on the provided content.

        Args:
            request: SEO analysis request containing content and parameters

        Returns:
            SEO analysis response with metrics and suggestions
        """
        # Calculate keyword density
        keyword_density = calculate_keyword_density(request.content, request.target_keywords)

        # Analyze heading structure
        heading_structure = analyze_heading_structure(request.content)

        # Calculate readability score using quality metrics
        quality_metrics = calculate_quality_metrics(request.content)
        readability_score = quality_metrics['readability_score']

        # Extract meta description
        meta_description = extract_meta_description(request.content)

        # Generate title suggestions
        title_suggestions = extract_title_suggestions(request.content)

        # Generate recommended keywords (keywords that appear frequently in content but weren't in targets)
        recommended_keywords = self._generate_recommended_keywords(
            request.content,
            request.target_keywords
        )

        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            request.content,
            keyword_density,
            heading_structure,
            readability_score,
            request.target_keywords
        )

        # Calculate overall SEO score
        seo_score = calculate_seo_score(
            keyword_density,
            readability_score,
            heading_structure,
            recommended_keywords,
            improvement_suggestions
        )

        # Create and return response
        response = SEOAnalysisResponse(
            content_id=request.content_id,
            keyword_density=keyword_density,
            readability_score=readability_score,
            heading_structure=heading_structure,
            meta_description=meta_description,
            title_suggestions=title_suggestions,
            recommended_keywords=recommended_keywords,
            seo_score=seo_score,
            improvement_suggestions=improvement_suggestions,
            competitor_comparison=None  # Will be implemented in comprehensive analysis
        )

        return response

    def _generate_recommended_keywords(self, content: str, target_keywords: List[str]) -> List[str]:
        """
        Generate recommended keywords based on content analysis.

        Args:
            content: Content to analyze
            target_keywords: Original target keywords

        Returns:
            List of recommended keywords
        """
        import re
        from collections import Counter

        # Extract all words from content
        words = re.findall(r'\b\w+\b', content.lower())

        # Remove common stop words
        stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it',
            'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this',
            'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or',
            'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could',
            'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come',
            'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how',
            'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because',
            'any', 'these', 'give', 'day', 'most', 'us'
        }

        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]

        # Count frequency of words
        word_freq = Counter(filtered_words)

        # Get top words that aren't in target keywords
        target_keywords_lower = [kw.lower() for kw in target_keywords]
        recommended = []

        for word, freq in word_freq.most_common(20):
            if word not in target_keywords_lower and freq >= 2:
                recommended.append(word)

        return recommended[:10]  # Return top 10 recommended keywords

    def _generate_improvement_suggestions(
        self,
        content: str,
        keyword_density: Dict[str, float],
        heading_structure: Dict[str, int],
        readability_score: float,
        target_keywords: List[str]
    ) -> List[str]:
        """
        Generate improvement suggestions based on SEO analysis.

        Args:
            content: Original content
            keyword_density: Keyword density results
            heading_structure: Heading structure analysis
            readability_score: Readability score
            target_keywords: Target keywords

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Keyword-related suggestions
        for keyword, density in keyword_density.items():
            if density == 0:
                suggestions.append(f"Consider incorporating the target keyword '{keyword}' into the content.")
            elif density > 5.0:
                suggestions.append(f"Reduce the usage of keyword '{keyword}' as it appears too frequently (density: {density}%).")
            elif density < 1.0:
                suggestions.append(f"Increase the usage of keyword '{keyword}' to achieve optimal density (1-3%).")

        # Heading structure suggestions
        h1_count = heading_structure.get('h1', 0)
        h2_count = heading_structure.get('h2', 0)
        h3_count = heading_structure.get('h3', 0)

        if h1_count == 0:
            suggestions.append("Add an H1 heading to structure your content properly.")
        elif h1_count > 1:
            suggestions.append(f"Reduce the number of H1 headings to just one (currently {h1_count}).")

        if h2_count == 0:
            suggestions.append("Consider adding H2 headings to improve content structure and readability.")

        if h3_count == 0 and len(content) > 500:
            suggestions.append("For longer content, consider adding H3 headings to further organize sections.")

        # Readability suggestions
        if readability_score < 50:
            suggestions.append(f"Improve readability (current score: {readability_score}/100). "
                             f"Try using shorter sentences and simpler vocabulary.")

        # Content length suggestions
        word_count = len(content.split())
        if word_count < 300:
            suggestions.append(f"Consider expanding the content (currently {word_count} words). "
                             f"Longer content tends to rank better for SEO.")

        # Meta description suggestions
        if len(content) > 160:
            suggestions.append("Ensure your meta description is compelling and under 160 characters.")

        return suggestions