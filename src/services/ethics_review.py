"""
Ethics Review Service

This module provides functionality for checking content for ethical issues,
plagiarism, and policy compliance to ensure responsible content generation.
"""

from typing import Dict, List
from ..models.ethics_report import EthicsCheckRequest, EthicsCheckResponse, PlagiarismMatch, CheckTypeEnum
import hashlib
import re
from difflib import SequenceMatcher


class EthicsReviewService:
    """Service class for performing ethics and plagiarism checks on content."""

    def __init__(self):
        """Initialize the Ethics Review Service."""
        # In a real implementation, this would connect to databases, APIs, etc.
        # For now, we'll use in-memory storage for demonstration
        self.content_database = {}  # Would normally be persistent storage
        self.policy_rules = [
            "Do not generate content that promotes hate speech",
            "Avoid creating content that could be harmful",
            "Respect copyright and intellectual property",
            "Maintain honesty and transparency",
            "Follow advertising standards and regulations"
        ]

    def check_content(self, request: EthicsCheckRequest) -> EthicsCheckResponse:
        """
        Perform comprehensive ethics and plagiarism check on the provided content.

        Args:
            request: Ethics check request containing content and parameters

        Returns:
            Ethics check response with results and recommendations
        """
        # Initialize response attributes
        plagiarism_detected = False
        similar_content_sources = []
        ethical_risk_level = "low"
        ethical_concerns = []
        policy_violations = []
        confidence_score = 0.95  # High confidence in our automated checks
        recommendations = []

        # Perform plagiarism check if requested
        if CheckTypeEnum.PLAGIARISM in request.check_type:
            plagiarism_result = self._check_plagiarism(
                request.content,
                request.reference_sources,
                request.exclude_self_content
            )
            plagiarism_detected = plagiarism_result['detected']
            similar_content_sources = plagiarism_result['matches']

        # Perform ethics check if requested
        if CheckTypeEnum.ETHICS in request.check_type:
            ethics_result = self._check_ethics(request.content)
            ethical_risk_level = ethics_result['risk_level']
            ethical_concerns = ethics_result['concerns']

        # Perform policy compliance check if requested
        if CheckTypeEnum.POLICY in request.check_type:
            policy_result = self._check_policy_compliance(request.content)
            policy_violations = policy_result['violations']
            recommendations.extend(policy_result['recommendations'])

        # Determine overall risk level based on all checks
        if policy_violations or ethical_concerns or plagiarism_detected:
            if len(policy_violations) > 3 or ethical_concerns or plagiarism_detected:
                ethical_risk_level = "high"
            elif len(policy_violations) > 1 or len(ethical_concerns) > 1:
                ethical_risk_level = "medium"

        # Generate recommendations based on findings
        if plagiarism_detected:
            recommendations.append("Revise content to ensure originality and proper attribution")
        if ethical_concerns:
            recommendations.extend([
                "Review content for ethical concerns",
                "Consider alternative phrasing that addresses ethical issues"
            ])
        if policy_violations:
            recommendations.append("Modify content to comply with content policies")

        if not recommendations:
            recommendations = ["Content passes all ethics and compliance checks"]

        # Create and return response
        response = EthicsCheckResponse(
            content_id=request.content_id,
            original_content=request.content,
            plagiarism_detected=plagiarism_detected,
            similar_content_sources=similar_content_sources,
            ethical_risk_level=ethical_risk_level,
            ethical_concerns=ethical_concerns,
            policy_violations=policy_violations,
            confidence_score=confidence_score,
            recommendations=recommendations
        )

        return response

    def _check_plagiarism(self, content: str, reference_sources: List[str], exclude_self_content: bool) -> Dict:
        """
        Check content for potential plagiarism against reference sources.

        Args:
            content: Content to check for plagiarism
            reference_sources: Known sources to check against
            exclude_self_content: Whether to exclude user's own previous content

        Returns:
            Dictionary with plagiarism check results
        """
        detected = False
        matches = []

        # Check against provided reference sources
        for source in reference_sources:
            similarity_ratio = self._calculate_similarity(content, source)

            if similarity_ratio > 0.7:  # Threshold for potential plagiarism
                detected = True

                # Extract the matching portion
                match_text = self._extract_matching_text(content, source)

                plagiarism_match = PlagiarismMatch(
                    source_url="reference_source",  # In a real system, this would be the actual URL
                    similarity_score=similarity_ratio,
                    matched_text=match_text[:200] + "..." if len(match_text) > 200 else match_text,
                    matched_percent=similarity_ratio * 100
                )

                matches.append({
                    'source_url': plagiarism_match.source_url,
                    'similarity_score': plagiarism_match.similarity_score,
                    'matched_text': plagiarism_match.matched_text,
                    'matched_percent': plagiarism_match.matched_percent
                })

        # If no reference sources provided, we could check against a broader database
        # For this implementation, we'll just return the results from reference sources
        return {
            'detected': detected,
            'matches': matches
        }

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity ratio between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity ratio from 0 to 1
        """
        # Remove HTML tags and normalize whitespace
        clean_text1 = re.sub(r'<[^>]+>', ' ', text1).strip()
        clean_text2 = re.sub(r'<[^>]+>', ' ', text2).strip()

        # Calculate similarity using SequenceMatcher
        return SequenceMatcher(None, clean_text1.lower(), clean_text2.lower()).ratio()

    def _extract_matching_text(self, content: str, source: str) -> str:
        """
        Extract the matching text between content and source.

        Args:
            content: Content being checked
            source: Source to compare against

        Returns:
            Matching text
        """
        # This is a simplified version - in a real system, this would be more sophisticated
        matcher = SequenceMatcher(None, content.lower(), source.lower())

        matching_blocks = matcher.get_matching_blocks()

        # Get the largest matching block
        if matching_blocks:
            largest_block = max(matching_blocks, key=lambda x: x.size)
            if largest_block.size > 0:
                return content[largest_block.a:largest_block.a + largest_block.size]

        return ""

    def _check_ethics(self, content: str) -> Dict:
        """
        Check content for potential ethical concerns.

        Args:
            content: Content to check

        Returns:
            Dictionary with ethics check results
        """
        concerns = []

        # Check for potentially problematic content patterns
        harmful_patterns = [
            r'\b(?:kill|murder|assassinate)\b',
            r'\b(?:hate|bigotry|prejudice)\s+(?:speech|groups?)\b',
            r'\b(?:discriminat|oppress|persecut)\w*\b',
            r'\b(?:steal|rob|burglar)\w*\b',
            r'\b(?:violat|abus)\w*\b'
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                concern = f"Potential harmful content detected matching pattern: {pattern}"
                concerns.append(concern)

        # Check for potentially manipulative language
        manipulative_patterns = [
            r'\b(?:guarantee|promised?)\s+(?:results|money back)\b',
            r'\b(?:miracle|revolutionary|breakthrough)\s+\w+',
            r'(?:fake\s+)?\b(?:reviews?|testimonials?)\s+(?:verified|real)'
        ]

        for pattern in manipulative_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                concern = f"Potentially manipulative language detected: {pattern}"
                concerns.append(concern)

        # Determine risk level based on number of concerns
        if len(concerns) >= 3:
            risk_level = "high"
        elif len(concerns) >= 1:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            'risk_level': risk_level,
            'concerns': concerns
        }

    def _check_policy_compliance(self, content: str) -> Dict:
        """
        Check content for policy compliance.

        Args:
            content: Content to check

        Returns:
            Dictionary with policy compliance results
        """
        violations = []
        recommendations = []

        # Check against policy rules
        for rule in self.policy_rules:
            # This is a simplified check - in reality, this would be more nuanced
            if "hate speech" in rule and re.search(r'\bhate\b.*\bspeech\b|\bspeech\b.*\bhate\b', content, re.IGNORECASE):
                violations.append(rule)
                recommendations.append(f"Avoid language that could be considered {rule.split('promotes')[1].strip()}")

            if "harmful" in rule and re.search(r'\bdangerous\b|\bharmful\b|\bunsafe\b|\brisky\b', content, re.IGNORECASE):
                violations.append(rule)
                recommendations.append(f"Ensure content does not {rule.split('creating')[1].strip()}")

            if "copyright" in rule or "intellectual property" in rule:
                # Check for potential copyright issues
                copyright_patterns = [
                    r'\b(?:copyrighted|trademarked|patented)\s+\w+\b',
                    r'\b(?:owned by|property of)\s+\w+',
                    r'\b(?:all rights reserved|©)\b'
                ]

                for pattern in copyright_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        violations.append(rule)
                        recommendations.append("Ensure proper attribution and permissions for copyrighted material")

        return {
            'violations': violations,
            'recommendations': recommendations
        }

    def store_content_for_future_check(self, content_id: str, content: str, author_id: str = None):
        """
        Store content for future plagiarism checks.

        Args:
            content_id: Identifier for the content
            content: Content to store
            author_id: Optional author identifier
        """
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        self.content_database[content_hash] = {
            'content_id': content_id,
            'content': content,
            'author_id': author_id,
            'timestamp': str(__import__('datetime').datetime.now())
        }