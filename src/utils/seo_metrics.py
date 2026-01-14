from typing import Dict, List, Tuple
import re
from collections import Counter


def calculate_keyword_density(content: str, keywords: List[str]) -> Dict[str, float]:
    """
    Calculate the density of each keyword in the content.

    Args:
        content: The content to analyze
        keywords: List of keywords to calculate density for

    Returns:
        Dictionary mapping keywords to their density percentages
    """
    if not content or not keywords:
        return {}

    content_lower = content.lower()
    total_words = len(re.findall(r'\b\w+\b', content_lower))

    if total_words == 0:
        return {keyword: 0.0 for keyword in keywords}

    keyword_density = {}
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Count exact word matches
        matches = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', content_lower))
        density = (matches / total_words) * 100
        keyword_density[keyword] = round(density, 3)

    return keyword_density


def analyze_heading_structure(content: str) -> Dict[str, int]:
    """
    Analyze the heading structure of the content.

    Args:
        content: The content to analyze

    Returns:
        Dictionary mapping heading levels to their count
    """
    heading_pattern = r'<h([1-6])[^>]*>.*?</h\1>'
    matches = re.findall(heading_pattern, content, re.IGNORECASE)

    heading_counts = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0}

    for level in matches:
        heading_counts[f'h{level}'] += 1

    return heading_counts


def calculate_seo_score(
    keyword_density: Dict[str, float],
    readability_score: float,
    heading_structure: Dict[str, int],
    recommended_keywords: List[str],
    improvement_suggestions: List[str]
) -> float:
    """
    Calculate an overall SEO score based on multiple factors.

    Args:
        keyword_density: Dictionary of keyword densities
        readability_score: Readability score
        heading_structure: Heading structure analysis
        recommended_keywords: List of recommended keywords
        improvement_suggestions: List of improvement suggestions

    Returns:
        SEO score from 0 to 100
    """
    score = 50  # Base score

    # Adjust for keyword density (optimal range is 1-3%)
    for density in keyword_density.values():
        if 1.0 <= density <= 3.0:
            score += 10  # Good keyword density
        elif 0.5 <= density <= 5.0:
            score += 5   # Acceptable keyword density
        elif density == 0:
            score -= 10  # Missing keywords
        else:
            score -= 5   # Too much keyword density

    # Adjust for readability
    if 60 <= readability_score <= 100:
        score += 15  # Good readability
    elif 40 <= readability_score < 60:
        score += 5   # Acceptable readability
    else:
        score -= 10  # Poor readability

    # Adjust for heading structure (good structure has 1 H1, some H2/H3)
    h1_count = heading_structure.get('h1', 0)
    h2_count = heading_structure.get('h2', 0)
    h3_count = heading_structure.get('h3', 0)

    if h1_count == 1:
        score += 10  # Proper H1 count
    elif h1_count == 0:
        score -= 15  # Missing H1
    elif h1_count > 1:
        score -= 10  # Too many H1s

    if h2_count > 0:
        score += 5  # Has H2s
    if h3_count > 0:
        score += 5  # Has H3s

    # Adjust for improvement suggestions
    if len(improvement_suggestions) == 0:
        score += 10  # No suggestions needed
    elif len(improvement_suggestions) <= 2:
        score += 5   # Few suggestions
    elif len(improvement_suggestions) > 5:
        score -= 10  # Many suggestions needed

    # Ensure score stays within bounds
    return max(0, min(100, score))


def extract_meta_description(content: str, max_length: int = 160) -> str:
    """
    Extract or generate a meta description from content.

    Args:
        content: The content to extract from
        max_length: Maximum length for the meta description

    Returns:
        Meta description string
    """
    # First, try to find an existing meta description in HTML
    meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if meta_match:
        return meta_match.group(1)[:max_length]

    # If not found, generate one from the first part of content
    sentences = re.split(r'[.!?]+', content.strip())
    if sentences:
        first_sentence = sentences[0].strip()
        if len(first_sentence) > max_length:
            # Find the best cut point (try to end at a word boundary)
            best_cut = max_length
            for i in range(max_length, max_length-30, -1):
                if i < len(first_sentence) and first_sentence[i].isspace():
                    best_cut = i
                    break
            first_sentence = first_sentence[:best_cut].strip()

        return first_sentence

    return ""


def extract_title_suggestions(content: str) -> List[str]:
    """
    Extract or generate title suggestions from content.

    Args:
        content: The content to extract titles from

    Returns:
        List of suggested titles
    """
    suggestions = []

    # Look for existing titles in HTML
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
    if title_match:
        suggestions.append(title_match.group(1).strip())

    # Look for H1 tags
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
    for match in h1_matches:
        suggestions.append(re.sub(r'<[^>]+>', '', match).strip())

    # If no titles found, generate from content
    if not suggestions:
        # Take the first sentence as a potential title
        sentences = re.split(r'[.!?]+', content.strip())
        if sentences and sentences[0].strip():
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 60:  # Truncate if too long
                first_sentence = first_sentence[:60].strip() + "..."
            suggestions.append(first_sentence)

    # Add variations by taking first 5-10 words from content
    words = content.split()[:10]
    if len(words) >= 5:
        suggestions.append(" ".join(words))

    return list(set(suggestions))  # Remove duplicates


def calculate_readability_flesch_kincaid(content: str) -> float:
    """
    Calculate readability using a simplified Flesch-Kincaid approach.
    Returns a score from 0-100 (higher is more readable).

    Args:
        content: The content to analyze

    Returns:
        Readability score from 0-100
    """
    # Remove HTML tags for accurate counting
    clean_content = re.sub(r'<[^>]+>', ' ', content)

    # Count sentences, words, and syllables
    sentences = len(re.findall(r'[.!?]+', clean_content)) or 1
    words = len(re.findall(r'\b\w+\b', clean_content))

    if words == 0:
        return 0.0

    # Simplified syllable counting (count vowels in each word)
    vowel_pattern = r'[aeiouAEIOU]+'
    syllables = sum(len(re.findall(vowel_pattern, word)) for word in re.findall(r'\b\w+\b', clean_content))
    syllables = max(1, syllables)  # Avoid division by zero

    # Calculate Flesch Reading Ease score
    # Formula: 206.835 - (1.015 × ASL) - (84.6 × ASW)
    # ASL = Average Sentence Length (words / sentences)
    # ASW = Average Syllables per Word (syllables / words)
    avg_sentence_length = words / sentences
    avg_syllables_per_word = syllables / words

    fre_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)

    # Convert to 0-100 scale
    # FRE ranges from 0-100 naturally, but let's bound it
    return max(0, min(100, fre_score))