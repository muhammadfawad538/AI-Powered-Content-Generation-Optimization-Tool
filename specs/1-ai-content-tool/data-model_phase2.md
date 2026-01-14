# Data Model for AI-Powered Content Generation Tool - Phase 2

## Core Entities

### SEOAnalysisRequest
**Description**: Represents a request for SEO analysis of existing content

**Fields**:
- `content_id` (str): Identifier for the content being analyzed
- `content` (str): The content to analyze for SEO
- `target_keywords` (List[str]): Keywords to analyze for optimization
- `competitor_urls` (List[str]): URLs of competitor content for comparison (optional)
- `analysis_depth` (str): Level of analysis (basic, detailed, comprehensive)
- `created_at` (datetime): Timestamp of request creation

**Validation rules**:
- Content is required and must be between 100-10000 characters
- Target keywords list must not exceed 20 items
- Competitor URLs must be valid URLs if provided
- Analysis depth must be one of: 'basic', 'detailed', 'comprehensive'

### SEOAnalysisResponse
**Description**: Represents the results of SEO analysis

**Fields**:
- `content_id` (str): Identifier matching the original request
- `keyword_density` (Dict[str, float]): Density of each target keyword
- `readability_score` (float): Overall readability score (0.0-100.0)
- `heading_structure` (Dict[str, int]): Count of H1, H2, H3, etc. tags
- `meta_description` (str): Suggested meta description
- `title_suggestions` (List[str]): Recommended titles
- `recommended_keywords` (List[str]): Additional keywords to consider
- `seo_score` (float): Overall SEO score (0.0-100.0)
- `improvement_suggestions` (List[str]): Specific suggestions for improvement
- `competitor_comparison` (Dict[str, Any]): Comparison with competitor content
- `report_timestamp` (datetime): Time of analysis completion

**Validation rules**:
- All numeric scores must be within valid ranges
- Improvement suggestions must not be empty when SEO score is below threshold

### QualityReviewRequest
**Description**: Represents a request for quality review and improvement

**Fields**:
- `content_id` (str): Identifier for the content being reviewed
- `content` (str): The content to review for quality
- `target_audience` (str): Audience for whom the content is intended
- `review_aspect` (List[str]): Aspects to review (clarity, readability, engagement, flow)
- `preserve_tone` (bool): Whether to maintain the original tone
- `style_guidelines` (Dict[str, str]): Specific style guidelines to follow
- `created_at` (datetime): Timestamp of request creation

**Validation rules**:
- Content is required and must be between 50-10000 characters
- Review aspects must be from predefined options
- Style guidelines must follow key-value format if provided

### QualityReviewResponse
**Description**: Represents the results of quality review with improvement suggestions

**Fields**:
- `content_id` (str): Identifier matching the original request
- `original_content` (str): The original content submitted for review
- `improved_content` (str): Content with quality improvements applied
- `clarity_score` (float): Clarity rating (0.0-100.0)
- `readability_score` (float): Readability rating (0.0-100.0)
- `engagement_score` (float): Engagement potential rating (0.0-100.0)
- `flow_score` (float): Content flow rating (0.0-100.0)
- `improvement_summary` (List[Dict[str, str]]): Summary of changes made
- `preserved_elements` (List[str]): Elements that were preserved (e.g., tone, style)
- `review_timestamp` (datetime): Time of review completion

**Validation rules**:
- All quality scores must be between 0.0 and 100.0
- Improved content must differ from original content if scores are low
- Improvement summary must align with the actual changes made

### EthicsCheckRequest
**Description**: Represents a request for plagiarism and ethical review

**Fields**:
- `content_id` (str): Identifier for the content being checked
- `content` (str): The content to check for ethical issues
- `reference_sources` (List[str]): Known sources to check against
- `check_type` (List[str]): Types of checks to perform (plagiarism, ethics, policy)
- `exclude_self_content` (bool): Whether to exclude user's own previous content from checks
- `created_at` (datetime): Timestamp of request creation

**Validation rules**:
- Content is required and must be between 50-10000 characters
- Check types must be from predefined options
- Reference sources must be valid URLs or text snippets if provided

### EthicsCheckResponse
**Description**: Represents the results of ethical review

**Fields**:
- `content_id` (str): Identifier matching the original request
- `original_content` (str): The original content submitted for review
- `plagiarism_detected` (bool): Whether potential plagiarism was detected
- `similar_content_sources` (List[Dict[str, str]]): Sources of similar content
- `ethical_risk_level` (str): Risk level (low, medium, high)
- `ethical_concerns` (List[str]): Specific ethical concerns identified
- `policy_violations` (List[str]): Policy violations detected
- `confidence_score` (float): Confidence in the analysis (0.0-1.0)
- `recommendations` (List[str]): Recommendations to address issues
- `check_timestamp` (datetime): Time of ethical check completion

**Validation rules**:
- Confidence score must be between 0.0 and 1.0
- Similar content sources must include URLs when plagiarism is detected
- Risk level must be one of: 'low', 'medium', 'high'

## Relationships
- One `ContentGenerationResponse` can be associated with multiple analysis requests (SEO, Quality, Ethics)
- Each analysis request has exactly one corresponding analysis response
- Multiple analysis responses can be combined to form a comprehensive optimization report

## State Transitions
- `SEOAnalysisRequest` transitions from 'submitted' → 'analyzing' → 'completed'/'failed'
- `QualityReviewRequest` transitions from 'submitted' → 'reviewing' → 'completed'/'failed'
- `EthicsCheckRequest` transitions from 'submitted' → 'checking' → 'completed'/'failed'