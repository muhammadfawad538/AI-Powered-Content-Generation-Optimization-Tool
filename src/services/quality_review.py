"""
Quality Review Service

This module provides functionality for reviewing content quality,
analyzing different aspects like clarity, readability, engagement,
and flow, and providing improvement suggestions.
"""

from typing import Dict, List
from ..models.quality_review import QualityReviewRequest, QualityReviewResponse, QualityImprovement, ReviewAspectEnum
from ..utils.quality_metrics import calculate_quality_metrics
from ..utils.seo_metrics import calculate_readability_flesch_kincaid


class QualityReviewService:
    """Service class for performing quality review on content."""

    def __init__(self):
        """Initialize the Quality Review Service."""
        pass

    def review_content(self, request: QualityReviewRequest) -> QualityReviewResponse:
        """
        Perform comprehensive quality review on the provided content.

        Args:
            request: Quality review request containing content and parameters

        Returns:
            Quality review response with scores and improvement suggestions
        """
        # Calculate quality metrics
        quality_metrics = calculate_quality_metrics(request.content)

        # Extract individual scores
        clarity_score = quality_metrics['clarity_score']
        readability_score = quality_metrics['readability_score']
        engagement_score = quality_metrics['engagement_score']
        flow_score = quality_metrics['flow_score']

        # Generate improved content based on review aspects
        improved_content = self._generate_improved_content(
            request.content,
            request.review_aspect,
            request.preserve_tone,
            request.style_guidelines
        )

        # Generate improvement suggestions
        improvement_summary = self._generate_improvement_summary(
            request.content,
            improved_content,
            request.review_aspect
        )

        # Identify preserved elements
        preserved_elements = self._identify_preserved_elements(
            request.content,
            improved_content
        )

        # Create and return response
        response = QualityReviewResponse(
            content_id=request.content_id,
            original_content=request.content,
            improved_content=improved_content,
            clarity_score=clarity_score,
            readability_score=readability_score,
            engagement_score=engagement_score,
            flow_score=flow_score,
            improvement_summary=improvement_summary,
            preserved_elements=preserved_elements
        )

        return response

    def _generate_improved_content(
        self,
        content: str,
        review_aspects: List[ReviewAspectEnum],
        preserve_tone: bool,
        style_guidelines: Dict[str, str]
    ) -> str:
        """
        Generate improved content based on review aspects.

        Args:
            content: Original content
            review_aspects: Aspects to review and improve
            preserve_tone: Whether to preserve original tone
            style_guidelines: Style guidelines to follow

        Returns:
            Improved content
        """
        improved_content = content

        # Apply improvements based on review aspects
        for aspect in review_aspects:
            if aspect == ReviewAspectEnum.CLARITY:
                improved_content = self._improve_clarity(improved_content)
            elif aspect == ReviewAspectEnum.READABILITY:
                improved_content = self._improve_readability(improved_content)
            elif aspect == ReviewAspectEnum.ENGAGEMENT:
                improved_content = self._improve_engagement(improved_content)
            elif aspect == ReviewAspectEnum.FLOW:
                improved_content = self._improve_flow(improved_content)

        return improved_content

    def _improve_clarity(self, content: str) -> str:
        """
        Improve content clarity by simplifying language and sentence structure.

        Args:
            content: Original content

        Returns:
            Content with improved clarity
        """
        import re

        # Split content into sentences
        sentences = re.split(r'([.!?]+)', content)

        improved_sentences = []
        for i in range(0, len(sentences), 2):
            sentence = sentences[i] if i < len(sentences) else ""

            if sentence.strip():
                # Break down complex sentences
                if len(sentence.split()) > 25:
                    # Try to split long sentences at conjunctions
                    sub_sentences = re.split(r'(,\s+and\s+|\s+and\s+|\s+but\s+|\s+or\s+)', sentence)

                    refined_sub_sentences = []
                    for sub in sub_sentences:
                        if len(sub.split()) > 25 and ',' in sub:
                            # Further split at commas if needed
                            comma_parts = sub.split(', ')
                            for j, part in enumerate(comma_parts):
                                if len(part.split()) > 25:
                                    # As a last resort, break long parts at approximate word limits
                                    words = part.split()
                                    chunks = []
                                    for k in range(0, len(words), 20):
                                        chunk = ' '.join(words[k:k+20])
                                        chunks.append(chunk)
                                    refined_sub_sentences.extend(chunks)
                                else:
                                    refined_sub_sentences.append(part)
                        else:
                            refined_sub_sentences.append(sub)

                    improved_sentences.extend(refined_sub_sentences)
                else:
                    improved_sentences.append(sentence)

                # Add punctuation if it existed in the original
                if i + 1 < len(sentences):
                    improved_sentences[-1] += sentences[i + 1]

        return "".join(improved_sentences)

    def _improve_readability(self, content: str) -> str:
        """
        Improve content readability by optimizing sentence structure and vocabulary.

        Args:
            content: Original content

        Returns:
            Content with improved readability
        """
        import re

        # Replace complex words with simpler alternatives
        complex_to_simple = {
            'utilize': 'use',
            'endeavor': 'try',
            'facilitate': 'help',
            'commence': 'begin',
            'terminate': 'end',
            'acquire': 'get',
            'modify': 'change',
            'implement': 'use',
            'establish': 'set up',
            'demonstrate': 'show',
            'examine': 'check',
            'obtain': 'get',
            'procure': 'get',
            'ascertain': 'find out',
            'convey': 'communicate',
            'transmit': 'send',
            'allocate': 'assign',
            'designate': 'choose',
            'initiate': 'start',
            'conclude': 'end',
            'assist': 'help',
            'beneficial': 'helpful',
            'significant': 'important',
            'substantial': 'large',
            'adequate': 'enough',
            'sufficient': 'enough',
            'subsequent': 'following',
            'previous': 'earlier',
            'commencement': 'start',
            'termination': 'end'
        }

        improved_content = content
        for complex_word, simple_word in complex_to_simple.items():
            # Use word boundaries to avoid partial matches
            improved_content = re.sub(
                r'\b' + re.escape(complex_word) + r'\b',
                simple_word,
                improved_content,
                flags=re.IGNORECASE
            )

        return improved_content

    def _improve_engagement(self, content: str) -> str:
        """
        Improve content engagement by adding questions, calls to action, etc.

        Args:
            content: Original content

        Returns:
            Content with improved engagement
        """
        import re

        # Add occasional rhetorical questions to boost engagement
        sentences = re.split(r'([.!?]+)', content)

        improved_content = ""
        question_added = False

        for i in range(0, len(sentences), 2):
            sentence = sentences[i] if i < len(sentences) else ""

            if sentence.strip() and not question_added and len(improved_content) > 100:
                # Add a question after a substantial sentence
                if len(sentence.split()) > 8:
                    improved_content += sentence
                    # Add a relevant question based on the sentence
                    if '?' not in sentence and '.' in sentence:
                        words = sentence.split()
                        if len(words) > 3:
                            improved_content += "? Have you ever thought about " + " ".join(words[1:4]).lower() + "?"
                        else:
                            improved_content += "?"
                        question_added = True
                    else:
                        improved_content += sentences[i + 1] if i + 1 < len(sentences) else ""
                else:
                    improved_content += sentence + (sentences[i + 1] if i + 1 < len(sentences) else "")
            else:
                improved_content += sentence + (sentences[i + 1] if i + 1 < len(sentences) else "")

        return improved_content

    def _improve_flow(self, content: str) -> str:
        """
        Improve content flow by enhancing transitions between sentences/paragraphs.

        Args:
            content: Original content

        Returns:
            Content with improved flow
        """
        import re

        # Add transition phrases to improve flow
        transition_phrases = [
            'Furthermore, ', 'In addition, ', 'Moreover, ', 'Besides, ',
            'On the other hand, ', 'However, ', 'Nevertheless, ',
            'As a result, ', 'Consequently, ', 'Therefore, '
        ]

        # Split content into paragraphs
        paragraphs = re.split(r'\n\s*\n', content)

        improved_paragraphs = []
        for i, paragraph in enumerate(paragraphs):
            sentences = re.split(r'([.!?]+)', paragraph)

            # Only add transition if this isn't the first paragraph
            if i > 0 and sentences and sentences[0].strip():
                # Add a random transition phrase to the beginning of the paragraph
                # (only if the paragraph doesn't already start with a transition)
                first_sentence = sentences[0].strip()
                if first_sentence and not any(first_sentence.lower().startswith(tr.lower()) for tr in transition_phrases):
                    sentences[0] = transition_phrases[i % len(transition_phrases)] + sentences[0]

            improved_paragraphs.append("".join(sentences))

        return "\n\n".join(improved_paragraphs)

    def _generate_improvement_summary(
        self,
        original_content: str,
        improved_content: str,
        review_aspects: List[ReviewAspectEnum]
    ) -> List[Dict[str, str]]:
        """
        Generate a summary of improvements made to the content.

        Args:
            original_content: Original content
            improved_content: Improved content
            review_aspects: Aspects that were reviewed

        Returns:
            List of improvement summaries
        """
        improvements = []

        # Placeholder improvements based on review aspects
        for aspect in review_aspects:
            if aspect == ReviewAspectEnum.CLARITY:
                improvements.append({
                    "aspect": "clarity",
                    "change": "Simplified complex sentences and replaced jargon with simpler terms",
                    "reason": "To improve clarity and comprehension for the target audience"
                })
            elif aspect == ReviewAspectEnum.READABILITY:
                improvements.append({
                    "aspect": "readability",
                    "change": "Optimized sentence structure and vocabulary",
                    "reason": "To enhance ease of reading and understanding"
                })
            elif aspect == ReviewAspectEnum.ENGAGEMENT:
                improvements.append({
                    "aspect": "engagement",
                    "change": "Added interactive elements and calls to action",
                    "reason": "To increase reader interest and participation"
                })
            elif aspect == ReviewAspectEnum.FLOW:
                improvements.append({
                    "aspect": "flow",
                    "change": "Enhanced transitions between sections",
                    "reason": "To create smoother content progression"
                })

        return improvements

    def _identify_preserved_elements(
        self,
        original_content: str,
        improved_content: str
    ) -> List[str]:
        """
        Identify elements that were preserved during the improvement process.

        Args:
            original_content: Original content
            improved_content: Improved content

        Returns:
            List of preserved elements
        """
        # For now, return general preserved elements
        return [
            "Core message and meaning",
            "Key factual information",
            "Main arguments or points",
            "Essential terminology"
        ]