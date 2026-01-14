# Manual Testing Guide for AI-Powered Content Generation & Optimization Tool

This guide explains how to use the manual testing API for the AI-Powered Content Generation & Optimization Tool. This API provides endpoints for testing all features including content generation, SEO optimization, quality review, ethics checks, research assistance, export management, and analytics/insights.

## Starting the API Server

1. Navigate to the project directory:
   ```
   cd E:\DEV\SEO_App
   ```

2. Start the API server:
   ```
   uvicorn manual_test_api:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Access the interactive API documentation at: http://localhost:8000/docs

## Available Endpoints

### Content Generation
- **Endpoint**: `POST /content/generate`
- **Description**: Generate content based on topic, audience, tone, style, and format
- **Sample Request**:
  ```json
  {
    "topic": "AI Content Generation",
    "audience": "professionals",
    "tone": "informative",
    "style": "technical",
    "format": "blog_post",
    "length": 500,
    "keywords": ["AI", "content", "generation"],
    "requirements": ["include benefits", "focus on efficiency"]
  }
  ```

### SEO Analysis
- **Endpoint**: `POST /seo/analyze`
- **Description**: Analyze content for SEO elements and provide recommendations
- **Sample Request**:
  ```json
  {
    "content": "This is a sample content about AI content generation for testing purposes.",
    "target_keywords": ["AI", "content", "generation"]
  }
  ```

### Quality Review
- **Endpoint**: `POST /quality/review`
- **Description**: Review content for clarity, readability, engagement, and flow
- **Sample Request**:
  ```json
  {
    "content": "This is sample content to review for quality...",
    "target_audience": "marketing professionals",
    "review_aspects": ["clarity", "readability", "engagement"]
  }
  ```

### Ethics/Plagiarism Check
- **Endpoint**: `POST /ethics/check`
- **Description**: Check content for ethical issues and potential plagiarism
- **Sample Request**:
  ```json
  {
    "content": "This is original content for ethics review.",
    "check_types": ["plagiarism", "ethics"]
  }
  ```

### Research Assistance
- **Endpoint**: `POST /research/conduct`
- **Description**: Conduct research on a topic and gather relevant information
- **Sample Request**:
  ```json
  {
    "query_text": "AI content generation best practices",
    "target_domains": ["example.com"],
    "max_results": 5,
    "research_purpose": "Finding best practices for content",
    "content_topic": "AI Content Generation"
  }
  ```

### Export Management
- **Endpoint**: `POST /export/content`
- **Description**: Export content to various platforms and formats
- **Sample Request**:
  ```json
  {
    "content": "This is content to export.",
    "export_format": "blog",
    "target_platform": "wordpress",
    "metadata": {"title": "Test Export", "category": "technology"}
  }
  ```

### Analytics Query
- **Endpoint**: `POST /analytics/query`
- **Description**: Query analytics data for content performance
- **Sample Request**:
  ```json
  {
    "content_ids": ["test_content_1", "test_content_2"],
    "date_range_start": "2026-01-01T00:00:00Z",
    "date_range_end": "2026-01-31T23:59:59Z",
    "metric_types": ["views", "engagement"]
  }
  ```

### Insights Generation
- **Endpoint**: `POST /insights/generate`
- **Description**: Generate insights and recommendations for content
- **Sample Request**:
  ```json
  {
    "content_ids": ["test_content_1"],
    "insight_categories": ["performance", "engagement"]
  }
  ```

### Workflow Management
- **Endpoint**: `POST /workflow/create`
- **Description**: Create and manage multi-step content workflows
- **Sample Request**:
  ```json
  {
    "workflow_name": "Content Optimization Workflow",
    "description": "A workflow that generates, optimizes, and exports content",
    "steps": [
      {
        "step_id": "step_1",
        "step_type": "content_generation",
        "description": "Generate initial content draft",
        "input_data": {
          "topic": "AI Content Generation",
          "audience": "professionals",
          "tone": "informative",
          "style": "technical",
          "format": "blog_post",
          "length": 500
        }
      }
    ]
  }
  ```

## Testing Best Practices

1. **Start with the health check**: Verify the API is running with `GET /health`

2. **Use the Swagger UI**: The interactive documentation at http://localhost:8000/docs allows you to test endpoints directly in your browser

3. **Test individual features first**: Start with simple requests to individual endpoints before trying complex workflows

4. **Validate responses**: Check that responses contain the expected fields and data types

5. **Test error handling**: Try invalid inputs to ensure proper error responses

## Expected Response Format

All endpoints return structured JSON responses with appropriate fields based on the operation. Sample responses include realistic data that simulates the behavior of the full implementation without the complex backend logic.

## Purpose

This API is specifically designed for manual pre-deployment testing. It returns realistic sample responses without implementing the full complex logic, making it ideal for:

- Verifying API contracts and data structures
- Testing client applications
- Demonstrating system capabilities
- Validating request/response schemas

## Limitations

This is NOT a production-ready API. It contains placeholder implementations that return sample data for testing purposes only. The actual production system would include full implementations of all services.