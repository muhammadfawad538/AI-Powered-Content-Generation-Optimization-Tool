# Quickstart Guide: AI-Powered Content Generation Tool - Phase 2

## Overview
Phase 2 adds SEO Optimization, Quality Review, and Ethical Safeguards to the core content generation functionality. This guide covers the new features and how to use them.

## Prerequisites
- Complete Phase 1 setup (core content generation)
- Additional Python packages for NLP and SEO analysis
- (Optional) Redis server for caching analysis results

## Installation of Additional Dependencies
Install Phase 2 specific dependencies:
```bash
pip install textstat spacy transformers sentence-transformers google-search-results
python -m spacy download en_core_web_sm
```

## Configuration Updates
Add these new environment variables to your .env file:
```bash
# SEO Analysis
SERP_API_KEY=your_google_search_api_key  # For SERP analysis
SEO_ANALYSIS_DEPTH=comprehensive  # Options: basic, detailed, comprehensive

# Quality Review
QUALITY_CHECK_ENABLED=true
READABILITY_METRICS=textstat  # Options: textstat, spacy, custom

# Ethics & Plagiarism
PLAGIARISM_CHECK_ENABLED=true
PLAGIARISM_THRESHOLD=0.8  # Similarity threshold (0.0-1.0)
CACHE_TTL=3600  # Cache TTL for analysis results in seconds

# Performance
MAX_CONTENT_SIZE=10000  # Maximum content size for analysis in characters
ASYNC_ANALYSIS=true  # Enable async processing for long-running analyses
```

## New API Endpoints

### SEO Analysis
Send a POST request to `/api/v1/content/analyze-seo`:

```bash
curl -X POST http://localhost:8000/api/v1/content/analyze-seo \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "content_12345",
    "content": "Your content here...",
    "target_keywords": ["keyword1", "keyword2"],
    "analysis_depth": "detailed"
  }'
```

### Quality Review
Send a POST request to `/api/v1/content/review-quality`:

```bash
curl -X POST http://localhost:8000/api/v1/content/review-quality \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "content_12345",
    "content": "Your content here...",
    "target_audience": "general_public",
    "review_aspect": ["clarity", "readability", "engagement"]
  }'
```

### Ethics Check
Send a POST request to `/api/v1/content/check-ethics`:

```bash
curl -X POST http://localhost:8000/api/v1/content/check-ethics \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "content_12345",
    "content": "Your content here...",
    "check_type": ["plagiarism", "ethics"]
  }'
```

## Integration with Phase 1
The new Phase 2 features can be used independently or chained with Phase 1 content generation:

```bash
# 1. Generate content (Phase 1)
# 2. Analyze SEO of generated content (Phase 2)
# 3. Review quality (Phase 2)
# 4. Check ethics (Phase 2)
# 5. Apply suggestions to improve content
```

## Testing Phase 2 Features

### Run Phase 2 Unit Tests
```bash
pytest tests/unit/test_seo_optimization.py
pytest tests/unit/test_quality_review.py
pytest tests/unit/test_ethics_safeguard.py
```

### Run Phase 2 Integration Tests
```bash
pytest tests/integration/test_content_optimization_flow.py
```

### Run Phase 2 Contract Tests
```bash
pytest tests/contract/test_seo_api.py
pytest tests/contract/test_quality_api.py
pytest tests/contract/test_ethics_api.py
```

## Performance Considerations
- SEO and quality analyses may take longer than basic content generation
- Enable async processing for content longer than 1000 words
- Use caching for repeated analyses of the same content
- Monitor API rate limits for external services (Google Search API)

## Troubleshooting
- **Slow analysis**: Enable async processing or reduce analysis depth
- **Memory issues**: Reduce MAX_CONTENT_SIZE or process content in chunks
- **API limits**: Implement proper rate limiting and caching
- **Quality issues**: Adjust model parameters or switch to a different analysis method