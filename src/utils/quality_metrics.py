"""
Quality metrics calculation module for content analysis.

This module provides functions to calculate various quality metrics
including clarity, readability, and engagement scores for content.
"""

from typing import Dict, List, Tuple
import re
from collections import Counter


def calculate_clarity_score(content: str) -> float:
    """
    Calculate clarity score based on sentence structure, vocabulary simplicity,
    and logical flow of the content.

    Args:
        content: The content to analyze

    Returns:
        Clarity score from 0 to 100
    """
    if not content.strip():
        return 0.0

    # Remove HTML tags for accurate analysis
    clean_content = re.sub(r'<[^>]+>', ' ', content)

    # Calculate average sentence length (optimal is around 15-20 words)
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean_content) if s.strip()]
    if not sentences:
        return 0.0

    words = re.findall(r'\b\w+\b', clean_content.lower())
    if not words:
        return 0.0

    avg_sentence_length = len(words) / len(sentences)

    # Calculate clarity based on sentence length (penalize very long sentences)
    if avg_sentence_length <= 10:
        clarity_from_length = 90
    elif avg_sentence_length <= 15:
        clarity_from_length = 95
    elif avg_sentence_length <= 20:
        clarity_from_length = 100
    elif avg_sentence_length <= 25:
        clarity_from_length = 90
    elif avg_sentence_length <= 30:
        clarity_from_length = 75
    else:
        clarity_from_length = max(30, 130 - avg_sentence_length)

    # Calculate vocabulary simplicity (favor common words)
    common_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for',
        'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his',
        'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
        'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if',
        'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like',
        'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
        'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look',
        'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two',
        'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because',
        'any', 'these', 'give', 'day', 'most', 'us'
    }

    common_word_count = sum(1 for word in words if word in common_words)
    common_word_ratio = common_word_count / len(words) if words else 0

    # Score based on common word usage (higher ratio is better for clarity)
    clarity_from_vocabulary = min(100, common_word_ratio * 150)

    # Combine scores with weights
    clarity_score = (clarity_from_length * 0.6) + (clarity_from_vocabulary * 0.4)

    # Ensure score is within bounds
    return max(0, min(100, round(clarity_score, 2)))


def calculate_readability_score(content: str) -> float:
    """
    Calculate readability score using multiple established metrics.

    Args:
        content: The content to analyze

    Returns:
        Readability score from 0 to 100
    """
    if not content.strip():
        return 0.0

    # Remove HTML tags for accurate analysis
    clean_content = re.sub(r'<[^>]+>', ' ', content)

    try:
        # Try to import textstat, if not available use fallback
        import textstat

        # Use multiple readability formulas and average them
        flesch_ease = textstat.flesch_reading_ease(clean_content)
        # Convert to 0-100 scale (Flesch Reading Ease ranges from ~-15 to 120)
        flesch_score = max(0, min(100, (flesch_ease + 15) / 1.35))

        flesch_grade = textstat.flesch_kincaid_grade(clean_content)
        # Convert grade level to readability score (lower grade = higher readability)
        grade_score = max(0, min(100, (18 - flesch_grade) * 7.14))  # Scale to 0-100

        ari = textstat.automated_readability_index(clean_content)
        # Convert ARI to readability score (lower grade = higher readability)
        ari_score = max(0, min(100, (16 - ari) * 6.25))  # Scale to 0-100

        # Average all scores
        readability_score = (flesch_score + grade_score + ari_score) / 3

        return round(readability_score, 2)
    except ImportError:
        # Fallback to a simpler calculation if textstat is not available
        sentences = [s.strip() for s in re.split(r'[.!?]+', clean_content) if s.strip()]
        words = re.findall(r'\b\w+\b', clean_content.lower())

        if not sentences or not words:
            return 0.0

        avg_sentence_length = len(words) / len(sentences)

        # Simpler readability calculation based on sentence length
        if avg_sentence_length <= 15:
            return 90.0
        elif avg_sentence_length <= 20:
            return 80.0
        elif avg_sentence_length <= 25:
            return 70.0
        elif avg_sentence_length <= 30:
            return 50.0
        else:
            return max(10.0, 100.0 - (avg_sentence_length * 2))


def calculate_engagement_score(content: str) -> float:
    """
    Calculate engagement score based on content structure, variety,
    use of questions, and other engagement indicators.

    Args:
        content: The content to analyze

    Returns:
        Engagement score from 0 to 100
    """
    if not content.strip():
        return 0.0

    # Calculate various engagement factors
    engagement_factors = []

    # Factor 1: Use of questions (indicates interactivity)
    questions = len(re.findall(r'\?', content))
    question_ratio = min(20, (questions / max(1, len(content.split()))) * 1000)
    engagement_factors.append(question_ratio * 2)  # Weight questions heavily

    # Factor 2: Content variety (use of different sentence starters)
    sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
    if sentences:
        starters = [re.match(r'\s*(\w+)', s) for s in sentences if re.match(r'\s*(\w+)', s)]
        starter_words = [match.group(1).lower() for match in starters if match]
        unique_starters = len(set(starter_words))
        variety_score = (unique_starters / len(sentences)) * 50 if sentences else 0
        engagement_factors.append(variety_score)

    # Factor 3: Use of transition words (indicates good flow)
    transition_words = [
        'however', 'therefore', 'meanwhile', 'furthermore', 'nevertheless',
        'nonetheless', 'consequently', 'accordingly', 'thus', 'hence',
        'besides', 'similarly', 'likewise', 'otherwise', 'instead',
        'alternatively', 'finally', 'subsequently', 'next', 'first',
        'second', 'third', 'lastly', 'ultimately', 'in conclusion'
    ]

    content_lower = content.lower()
    transition_count = sum(1 for word in transition_words if word in content_lower)
    transition_ratio = (transition_count / max(1, len(sentences))) * 25
    engagement_factors.append(min(25, transition_ratio))

    # Factor 4: Active vs passive voice (active is more engaging)
    # Very simplified check - looking for "is/are + past participle"
    words = content.split()
    passive_indicators = 0
    for i, word in enumerate(words):
        if word.lower() in ['is', 'are', 'was', 'were', 'be', 'been', 'being']:
            if i + 1 < len(words):
                next_word = words[i + 1]
                # Check if next word ends with typical past participle endings
                if any(next_word.lower().endswith(end) for end in ['ed', 't', 'n']):
                    passive_indicators += 1

    active_voice_ratio = max(0, 100 - ((passive_indicators / max(1, len(words))) * 200))
    engagement_factors.append(active_voice_ratio)

    # Factor 5: Paragraph structure (good content has varied paragraph lengths)
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    if len(paragraphs) > 1:
        para_lengths = [len(p.split()) for p in paragraphs]
        if len(set(para_lengths)) > 1:  # If paragraph lengths vary
            engagement_factors.append(15)  # Bonus for variety
        else:
            engagement_factors.append(5)  # Penalty for uniform paragraphs
    else:
        engagement_factors.append(0)  # No paragraph structure

    # Factor 6: Use of power words (persuasive language)
    power_words = [
        'new', 'free', 'you', 'discover', 'secret', 'ultimate', 'essential',
        'proven', 'effective', 'results', 'guaranteed', 'breakthrough',
        'exclusive', 'important', 'urgent', 'amazing', 'powerful', 'incredible',
        'best', 'top', 'leading', 'premium', 'advanced', 'innovative'
    ]

    power_word_count = sum(1 for word in power_words if word.lower() in content_lower)
    power_word_ratio = (power_word_count / max(1, len(content.split()))) * 100
    engagement_factors.append(min(20, power_word_ratio))

    # Calculate final engagement score
    if engagement_factors:
        engagement_score = sum(engagement_factors) / len(engagement_factors)
        # Normalize to 0-100 scale
        engagement_score = min(100, engagement_score)
        return round(max(0, engagement_score), 2)
    else:
        return 0.0


def calculate_flow_score(content: str) -> float:
    """
    Calculate content flow score based on structural elements,
    coherence, and logical progression.

    Args:
        content: The content to analyze

    Returns:
        Flow score from 0 to 100
    """
    if not content.strip():
        return 0.0

    # Remove HTML tags for accurate analysis
    clean_content = re.sub(r'<[^>]+>', ' ', content)

    flow_factors = []

    # Factor 1: Logical structure (presence of introduction, body, conclusion)
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean_content) if s.strip()]
    if len(sentences) >= 3:
        # Check for introductory, middle, and concluding indicators
        intro_indicators = ['introduction', 'first', 'initially', 'to begin', 'start']
        conclusion_indicators = ['conclusion', 'finally', 'in conclusion', 'to conclude', 'ultimately', 'lastly']

        first_third = sentences[:max(1, len(sentences)//3)]
        last_third = sentences[-max(1, len(sentences)//3):]

        first_text = ' '.join(first_third).lower()
        last_text = ' '.join(last_third).lower()

        has_intro = any(indicator in first_text for indicator in intro_indicators)
        has_conclusion = any(indicator in last_text for indicator in conclusion_indicators)

        structure_score = 25 if (has_intro and has_conclusion) else (15 if (has_intro or has_conclusion) else 5)
        flow_factors.append(structure_score)
    else:
        flow_factors.append(0)

    # Factor 2: Consistency of topic focus
    words = re.findall(r'\b\w+\b', clean_content.lower())
    if len(words) >= 10:
        # Get most common words (excluding common stop words)
        stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it',
            'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this',
            'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or'
        }
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

        if filtered_words:
            word_freq = Counter(filtered_words)
            top_words = [word for word, _ in word_freq.most_common(5)]

            # Calculate how consistently top words appear throughout the text
            total_top_word_occurrences = sum(word_freq[word] for word in top_words)
            consistency_ratio = total_top_word_occurrences / len(filtered_words)
            topic_focus_score = min(30, consistency_ratio * 50)
            flow_factors.append(topic_focus_score)
        else:
            flow_factors.append(0)
    else:
        flow_factors.append(0)

    # Factor 3: Smooth transitions between sentences
    transition_phrases = [
        'in addition', 'on the other hand', 'furthermore', 'however', 'therefore',
        'meanwhile', 'nevertheless', 'consequently', 'similarly', 'likewise',
        'in contrast', 'as a result', 'for example', 'specifically', 'namely',
        'indeed', 'certainly', 'obviously', 'generally', 'particularly'
    ]

    transition_count = sum(1 for phrase in transition_phrases if phrase.lower() in clean_content.lower())
    transition_score = min(25, (transition_count / max(1, len(sentences))) * 100)
    flow_factors.append(transition_score)

    # Factor 4: Sentence variety
    sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
    if len(sentence_lengths) > 1:
        # Calculate variance in sentence length (variety is good for flow)
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        if avg_length > 0:
            variance = sum((length - avg_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
            # Normalize variance to a 0-20 scale
            variety_score = min(20, (variance / avg_length) * 10 if avg_length > 0 else 0)
            variety_score = min(20, variety_score)  # Cap at 20
            flow_factors.append(variety_score)
        else:
            flow_factors.append(0)
    else:
        flow_factors.append(0)

    # Calculate final flow score
    if flow_factors:
        flow_score = sum(flow_factors) / len(flow_factors)
        return round(max(0, min(100, flow_score)), 2)
    else:
        return 0.0


def calculate_quality_metrics(content: str) -> Dict[str, float]:
    """
    Calculate all quality metrics for the given content.

    Args:
        content: The content to analyze

    Returns:
        Dictionary containing all quality metrics
    """
    return {
        'clarity_score': calculate_clarity_score(content),
        'readability_score': calculate_readability_score(content),
        'engagement_score': calculate_engagement_score(content),
        'flow_score': calculate_flow_score(content)
    }