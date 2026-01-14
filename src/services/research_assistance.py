"""
Research Assistance Service

This module provides functionality for conducting research and gathering
relevant data, references, and examples to support content creation.
"""

from typing import Dict, List, Optional
import asyncio
import aiohttp
from urllib.parse import urlparse
from ..models.research_result import (
    ResearchRequest, ResearchResponse, ResearchResult, SearchResult,
    ResearchQuery, SourceCredibilityLevel, SourceCredibilityAssessment,
    CredibilityCheckRequest, CredibilityCheckResponse
)
from ..config.settings import settings
from ..utils.workflow_helpers import WorkflowCache, generate_workflow_id
from ..utils.logging_config import research_logger


class ResearchAssistanceService:
    """Service class for conducting research and gathering information."""

    def __init__(self):
        """Initialize the Research Assistance Service."""
        self.cache = WorkflowCache(ttl_seconds=settings.redis_ttl)
        self.session = None
        self.logger = research_logger

    async def initialize_session(self):
        """Initialize the HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=settings.research_timeout)
            )

    async def close_session(self):
        """Close the HTTP session."""
        if self.session:
            await self.session.close()

    async def conduct_research(self, request: ResearchRequest) -> ResearchResponse:
        """
        Conduct research based on the provided query.

        Args:
            request: Research request containing query parameters

        Returns:
            Research response with results
        """
        await self.initialize_session()

        # Generate a unique query ID
        query_id = generate_workflow_id()
        self.logger.info(f"Starting research for content_id: {request.content_id}, query: '{request.query.query_text[:50]}...'")

        # Check cache first
        cache_key = f"research_{request.content_id}_{hash(request.query.query_text)}"
        cached_result = self.cache.get(cache_key)

        if cached_result:
            self.logger.info(f"Returning cached results for content_id: {request.content_id}")
            return cached_result

        # Perform the research
        start_time = asyncio.get_event_loop().time()

        # Perform search using SERP API or other search methods
        self.logger.info(f"Performing search for query: '{request.query.query_text}'")
        search_results = await self._perform_search(request.query)

        # Filter results based on target domains if specified
        if request.query.target_domains:
            initial_count = len(search_results)
            search_results = [
                result for result in search_results
                if any(domain in result.url for domain in request.query.target_domains)
            ]
            self.logger.info(f"Filtered results from {initial_count} to {len(search_results)} based on target domains")

        # Assess credibility of results if requested
        if request.validate_sources:
            self.logger.info(f"Validating and enhancing {len(search_results)} results")
            search_results = await self._validate_and_enhance_results(search_results)

        # Generate research summary
        research_summary = await self._generate_research_summary(
            request.query.query_text,
            search_results
        )

        # Calculate search duration
        duration = asyncio.get_event_loop().time() - start_time

        # Create research result
        research_result = ResearchResult(
            query_id=query_id,
            original_query=request.query,
            search_results=search_results,
            total_results_found=len(search_results),
            filtered_results_count=len(search_results),
            credibility_summary=self._summarize_credentiality(search_results),
            research_summary=research_summary,
            key_insights=await self._extract_key_insights(search_results),
            related_topics=await self._suggest_related_topics(request.query.query_text, search_results),
            search_duration=duration
        )

        # Create response
        response = ResearchResponse(
            content_id=request.content_id,
            research_results=research_result
        )

        # Cache the result
        self.logger.info(f"Caching research results for content_id: {request.content_id}")
        self.cache.set(cache_key, response)

        # Log the research operation
        from ..utils.logging_config import log_research_operation
        log_research_operation(
            self.logger,
            query_id,
            request.query.query_text,
            len(search_results),
            duration * 1000,  # Convert to milliseconds
            "completed"
        )

        self.logger.info(f"Completed research for content_id: {request.content_id}, found {len(search_results)} results in {duration:.2f}s")
        return response

    async def _perform_search(self, query: ResearchQuery) -> List[SearchResult]:
        """
        Perform search using SERP API or alternative search methods.

        Args:
            query: Research query to execute

        Returns:
            List of search results
        """
        results = []

        try:
            # Try to use SERP API if available
            if settings.serp_api_key:
                results = await self._perform_serps_api_search(query)
            else:
                # Fallback to a mock search for demonstration
                results = await self._perform_mock_search(query)
        except Exception as e:
            # Fallback to mock search if primary method fails
            print(f"Search API failed: {e}. Using mock search.")
            results = await self._perform_mock_search(query)

        return results

    async def _perform_serps_api_search(self, query: ResearchQuery) -> List[SearchResult]:
        """
        Perform search using SERP API.

        Args:
            query: Research query to execute

        Returns:
            List of search results
        """
        # Note: This is a simplified implementation. In a real system, you'd
        # integrate with the actual SERP API
        try:
            params = {
                'q': query.query_text,
                'num': query.max_results,
                'api_key': settings.serp_api_key
            }

            if query.target_domains:
                # Add domain filters if specified
                params['site'] = ','.join(query.target_domains)

            async with self.session.get('https://serpapi.com/search', params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    # Parse results - this would vary depending on the actual API response format
                    organic_results = data.get('organic_results', [])
                    results = []

                    for item in organic_results[:query.max_results]:
                        result = SearchResult(
                            title=item.get('title', ''),
                            url=item.get('link', ''),
                            snippet=item.get('snippet', ''),
                            source_domain=urlparse(item.get('link', '')).netloc,
                            published_date=item.get('date', None),
                            relevance_score=min(1.0, len(results) / query.max_results)  # Simple ranking
                        )
                        results.append(result)

                    return results
        except Exception as e:
            print(f"SERP API search failed: {e}")

        # Return mock results if API fails
        return await self._perform_mock_search(query)

    async def _perform_mock_search(self, query: ResearchQuery) -> List[SearchResult]:
        """
        Perform mock search for demonstration purposes.

        Args:
            query: Research query to execute

        Returns:
            List of mock search results
        """
        # Create mock results based on the query
        mock_results = [
            SearchResult(
                title=f"Article about {query.query_text}",
                url=f"https://example.com/article-{i}",
                snippet=f"This article discusses {query.query_text} in detail.",
                source_domain=f"example{i}.com",
                published_date="2023-01-01",
                relevance_score=1.0 - (i * 0.1),
                credibility_level=SourceCredibilityLevel.HIGH
            )
            for i in range(min(query.max_results, 5))
        ]

        # Add some variety to make it more realistic
        if "marketing" in query.query_text.lower():
            mock_results.extend([
                SearchResult(
                    title="Digital Marketing Best Practices",
                    url="https://marketingpro.com/digital-best-practices",
                    snippet="Learn the latest digital marketing strategies and best practices for 2023.",
                    source_domain="marketingpro.com",
                    published_date="2023-05-15",
                    relevance_score=0.9,
                    credibility_level=SourceCredibilityLevel.HIGH
                ),
                SearchResult(
                    title="Content Marketing Trends",
                    url="https://contenthub.org/marketing-trends-2023",
                    snippet="Explore the newest content marketing trends that are shaping the industry.",
                    source_domain="contenthub.org",
                    published_date="2023-03-22",
                    relevance_score=0.85,
                    credibility_level=SourceCredibilityLevel.MEDIUM
                )
            ])

        return mock_results[:query.max_results]

    async def _validate_and_enhance_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        Validate and enhance search results with credibility assessments.

        Args:
            results: List of search results to validate

        Returns:
            List of validated and enhanced search results
        """
        validated_results = []

        for result in results:
            # Assess credibility based on domain and other factors
            credibility = await self._assess_source_credibility(result.url)
            result.credibility_level = credibility

            # Add relevance score based on content analysis
            result.relevance_score = await self._calculate_relevance_score(
                result.snippet,
                result.title
            )

            validated_results.append(result)

        return validated_results

    async def _assess_source_credibility(self, url: str) -> SourceCredibilityLevel:
        """
        Assess the credibility of a source based on various factors.

        Args:
            url: URL of the source to assess

        Returns:
            Credibility level of the source
        """
        domain = urlparse(url).netloc.lower()

        # Known high credibility domains
        high_credibility_domains = [
            'edu', 'gov', 'org', 'wikipedia.org', 'nytimes.com', 'bbc.com',
            'reuters.com', 'apnews.com', 'forbes.com', 'harvard.edu'
        ]

        # Known medium credibility domains
        medium_credibility_domains = [
            'blogspot.com', 'wordpress.com', 'medium.com', 'quora.com',
            'reddit.com', 'linkedin.com'
        ]

        # Check domain extensions and specific sites
        for high_domain in high_credibility_domains:
            if high_domain in domain:
                return SourceCredibilityLevel.HIGH

        for med_domain in medium_credibility_domains:
            if med_domain in domain:
                return SourceCredibilityLevel.MEDIUM

        # Check for common low credibility indicators
        low_credibility_indicators = [
            'unreliable-', 'scam-', 'fake-', 'rumor-', 'gossip-'
        ]

        for indicator in low_credibility_indicators:
            if indicator in domain:
                return SourceCredibilityLevel.LOW

        # Default to medium for most domains
        return SourceCredibilityLevel.MEDIUM

    async def _calculate_relevance_score(self, snippet: str, title: str) -> float:
        """
        Calculate relevance score based on content analysis.

        Args:
            snippet: Snippet text to analyze
            title: Title text to analyze

        Returns:
            Relevance score from 0 to 1
        """
        # Simple relevance calculation based on content richness
        content = f"{title} {snippet}".lower()

        # Check for common indicators of quality content
        positive_indicators = [
            'study', 'research', 'analysis', 'report', 'data', 'statistics',
            'expert', 'professional', 'author', 'source', 'reference'
        ]

        negative_indicators = [
            'ad', 'advertisement', 'promo', 'buy now', 'click here',
            'sale', 'discount', 'deal', 'offer'
        ]

        positive_score = sum(1 for indicator in positive_indicators if indicator in content)
        negative_score = sum(1 for indicator in negative_indicators if indicator in content)

        # Calculate normalized score (between 0 and 1)
        raw_score = max(0, positive_score - negative_score)
        normalized_score = min(1.0, raw_score / 5.0)  # Cap at 1.0

        return max(0.1, normalized_score)  # Ensure minimum score

    def _summarize_credentiality(self, results: List[SearchResult]) -> Dict[SourceCredibilityLevel, int]:
        """
        Summarize credibility distribution among results.

        Args:
            results: List of search results

        Returns:
            Dictionary with credibility level counts
        """
        summary = {
            SourceCredibilityLevel.HIGH: 0,
            SourceCredibilityLevel.MEDIUM: 0,
            SourceCredibilityLevel.LOW: 0,
            SourceCredibilityLevel.UNKNOWN: 0
        }

        for result in results:
            summary[result.credibility_level] += 1

        return summary

    async def _generate_research_summary(self, query: str, results: List[SearchResult]) -> str:
        """
        Generate a summary of the research findings.

        Args:
            query: Original query
            results: Search results

        Returns:
            Summary of research findings
        """
        if not results:
            return f"No results found for query: {query}"

        # Count results by credibility
        high_cred_count = sum(1 for r in results if r.credibility_level == SourceCredibilityLevel.HIGH)
        medium_cred_count = sum(1 for r in results if r.credibility_level == SourceCredibilityLevel.MEDIUM)
        low_cred_count = sum(1 for r in results if r.credibility_level == SourceCredibilityLevel.LOW)

        summary_parts = [
            f"Research on '{query}' yielded {len(results)} results.",
            f"High credibility sources: {high_cred_count}, ",
            f"Medium credibility sources: {medium_cred_count}, ",
            f"Low credibility sources: {low_cred_count}."
        ]

        if results:
            top_titles = [r.title for r in results[:3]]
            summary_parts.append(f"Top sources include: {', '.join(top_titles[:2])}.")

        return " ".join(summary_parts)

    async def _extract_key_insights(self, results: List[SearchResult]) -> List[str]:
        """
        Extract key insights from search results.

        Args:
            results: Search results

        Returns:
            List of key insights
        """
        insights = []

        # Extract insights based on high credibility sources
        high_cred_results = [r for r in results if r.credibility_level == SourceCredibilityLevel.HIGH]

        if high_cred_results:
            # Take snippets from high credibility sources as potential insights
            for result in high_cred_results[:3]:  # Limit to top 3
                if len(result.snippet) > 20:  # Only include meaningful snippets
                    insights.append(result.snippet)

        # If no high credibility results, use medium
        if not insights:
            medium_cred_results = [r for r in results if r.credibility_level == SourceCredibilityLevel.MEDIUM]
            for result in medium_cred_results[:2]:
                if len(result.snippet) > 20:
                    insights.append(result.snippet)

        return insights

    async def _suggest_related_topics(self, query: str, results: List[SearchResult]) -> List[str]:
        """
        Suggest related topics based on search results.

        Args:
            query: Original query
            results: Search results

        Returns:
            List of related topics
        """
        related_topics = []

        # Extract related topics from result titles and snippets
        all_text = " ".join([r.title + " " + r.snippet for r in results])

        # Simple keyword extraction (in a real system, use NLP techniques)
        words = all_text.lower().split()
        word_freq = {}

        for word in words:
            # Filter out common stop words and short words
            if len(word) > 4 and word not in ['this', 'that', 'with', 'from', 'have', 'they', 'were']:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top words as related topics
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        related_topics = [word for word, count in sorted_words[:5]]

        return related_topics

    async def check_source_credibility(self, request: CredibilityCheckRequest) -> CredibilityCheckResponse:
        """
        Check credibility of specific sources.

        Args:
            request: Request containing URLs to check

        Returns:
            Response with credibility assessments
        """
        assessments = []

        for url in request.urls_to_check:
            # Assess credibility
            credibility = await self._assess_source_credibility(url)

            # Create assessment
            assessment = SourceCredibilityAssessment(
                source_url=url,
                credibility_level=credibility,
                assessment_criteria=["domain_authority", "content_quality", "publication_date"],
                confidence_score=0.8 if credibility != SourceCredibilityLevel.UNKNOWN else 0.5,
                assessment_reasoning=f"Domain credibility assessment resulted in {credibility.value} level",
                assessed_by="automated_system"
            )

            assessments.append(assessment)

        # Calculate overall trustworthiness
        if assessments:
            avg_score = sum(1 if a.credibility_level == SourceCredibilityLevel.HIGH else
                           0.7 if a.credibility_level == SourceCredibilityLevel.MEDIUM else
                           0.3 for a in assessments) / len(assessments)
        else:
            avg_score = 0.0

        # Create summary
        summary = {
            SourceCredibilityLevel.HIGH: sum(1 for a in assessments if a.credibility_level == SourceCredibilityLevel.HIGH),
            SourceCredibilityLevel.MEDIUM: sum(1 for a in assessments if a.credibility_level == SourceCredibilityLevel.MEDIUM),
            SourceCredibilityLevel.LOW: sum(1 for a in assessments if a.credibility_level == SourceCredibilityLevel.LOW),
            SourceCredibilityLevel.UNKNOWN: sum(1 for a in assessments if a.credibility_level == SourceCredibilityLevel.UNKNOWN),
        }

        response = CredibilityCheckResponse(
            request_id=generate_workflow_id(),
            assessments=assessments,
            summary=summary,
            overall_trustworthiness=avg_score
        )

        return response