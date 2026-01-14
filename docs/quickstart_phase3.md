# Quickstart Guide - Phase 3: Research & Export Features

This guide provides a quick overview of how to use the new Research Assistance, Export Management, and Workflow Orchestration features added in Phase 3.

## Prerequisites

Before using the new Phase 3 features, ensure you have:

1. **API Keys**: Set up the required API keys in your `.env` file:
   ```
   # Research Configuration
   SERP_API_KEY=your_serps_api_key

   # Export Configuration
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
   WORDPRESS_SITE_URL=https://your-wordpress-site.com
   WORDPRESS_USERNAME=your_username
   WORDPRESS_PASSWORD=your_password

   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   REDIS_TTL=3600
   ```

2. **Environment Setup**: Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Redis Server**: Ensure Redis is running for caching research results and workflow state.

## Research Assistance Features

### Conducting Research

To perform research on a topic:

```bash
curl -X POST http://localhost:8000/api/v1/research/conduct-research \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "my_content_001",
    "query": {
      "query_text": "AI content generation best practices",
      "target_domains": [],
      "max_results": 5,
      "research_purpose": "Finding best practices for AI-generated content",
      "content_topic": "AI Content Generation"
    },
    "validate_sources": true,
    "include_related_queries": true
  }'
```

### Checking Source Credibility

Validate the credibility of specific URLs:

```bash
curl -X POST http://localhost:8000/api/v1/research/check-credibility \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "urls_to_check": [
      "https://example.com/article",
      "https://another-source.com/resource"
    ],
    "content_context": "AI content generation article"
  }'
```

## Export Management Features

### Exporting Content

Export content to various platforms:

```bash
curl -X POST http://localhost:8000/api/v1/export/export-content \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "my_article_001",
    "content": "This is the content to be exported...",
    "export_format": "blog",
    "target_platform": "medium",
    "metadata": {
      "title": "My Exported Article",
      "tags": ["AI", "content", "export"]
    }
  }'
```

### Batch Export

Export multiple pieces of content at once:

```bash
curl -X POST http://localhost:8000/api/v1/export/batch-export \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "export_requests": [
      {
        "content_id": "article_1",
        "content": "First article content...",
        "export_format": "blog",
        "target_platform": "medium"
      },
      {
        "content_id": "article_2",
        "content": "Second article content...",
        "export_format": "social_media",
        "target_platform": "twitter"
      }
    ],
    "parallel_processing": true,
    "continue_on_failure": true
  }'
```

## Workflow Orchestration Features

### Creating a Workflow

Create a multi-step workflow:

```bash
curl -X POST http://localhost:8000/api/v1/workflow/create-workflow \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "workflow_name": "Content Creation Pipeline",
    "description": "Generate, optimize, and export content",
    "steps": [
      {
        "step_id": "generate_content",
        "step_type": "content_generation",
        "description": "Generate initial content draft",
        "input_data": {
          "topic": "AI in Marketing",
          "audience": "marketing_professionals",
          "tone": "informative",
          "style": "professional",
          "format": "blog_post",
          "length": 600
        }
      },
      {
        "step_id": "analyze_seo",
        "step_type": "seo_analysis",
        "description": "Analyze content for SEO",
        "input_data": {
          "content_id": "dynamic_content_id",
          "target_keywords": ["AI", "marketing", "automation"]
        }
      },
      {
        "step_id": "export_content",
        "step_type": "export",
        "description": "Export to blog platform",
        "input_data": {
          "content_id": "dynamic_content_id",
          "export_format": "blog",
          "target_platform": "wordpress"
        }
      }
    ],
    "metadata": {
      "priority": "high",
      "campaign": "q4_content_push"
    }
  }'
```

### Executing a Workflow

Execute a created workflow by its ID:

```bash
curl -X POST http://localhost:8000/api/v1/workflow/execute-workflow/{workflow_id} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Monitoring Workflow Status

Check the status of a workflow:

```bash
curl -X GET http://localhost:8000/api/v1/workflow/workflow-status/{workflow_id} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Common Use Cases

### 1. Research-Based Content Creation

Combine research and content generation:

1. Conduct research on a topic
2. Use research results to inform content creation
3. Export the generated content to your preferred platform

### 2. Multi-Platform Publishing

Create a workflow that exports content to multiple platforms:

- Generate content once
- Export to blog platforms (WordPress, Medium)
- Adapt for social media (Twitter, LinkedIn)
- Format for ad campaigns (Google Ads)

### 3. Automated Content Pipeline

Set up a complete content pipeline:

- Automatic research gathering
- Content generation based on research
- SEO optimization
- Quality review
- Multi-platform export

## Best Practices

1. **Caching**: Research results are automatically cached to reduce API calls and improve performance.

2. **Validation**: Always validate export formats before bulk operations.

3. **Monitoring**: Monitor workflow status and set up alerts for failures.

4. **Rate Limits**: Be aware of API rate limits for research and export platforms.

5. **Security**: Store API keys securely and rotate them regularly.

6. **Error Handling**: Implement retry logic for failed operations in production environments.

## Troubleshooting

- **API Connection Issues**: Verify that all required API keys are properly configured.
- **Redis Connection**: Ensure Redis server is running for caching functionality.
- **Platform Integration**: Check platform-specific requirements and credentials.
- **Rate Limiting**: Monitor API usage and implement appropriate delays if hitting limits.

## Next Steps

Once you've mastered these Phase 3 features, consider:

1. Creating custom workflows for your specific use cases
2. Integrating with your existing content management systems
3. Setting up automated content pipelines
4. Exploring advanced export formatting options
5. Implementing custom research queries for your domain

For more detailed information, refer to the full API documentation and usage examples.