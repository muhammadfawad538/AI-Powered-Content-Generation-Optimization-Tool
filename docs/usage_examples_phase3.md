# Usage Examples - Phase 3: Research & Export Features

This document provides practical usage examples for the new Research Assistance, Export Management, and Workflow Orchestration features added in Phase 3.

## Research Assistance Examples

### Basic Research Query

Conduct research on a specific topic:

```bash
curl -X POST http://localhost:8000/api/v1/research/conduct-research \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "blog_post_001",
    "query": {
      "query_text": "best practices for AI content generation",
      "target_domains": [],
      "max_results": 5,
      "research_purpose": "Finding best practices for AI-generated content",
      "content_topic": "AI Content Generation"
    },
    "validate_sources": true,
    "include_related_queries": true
  }'
```

### Research with Target Domains

Focus research on specific domains:

```bash
curl -X POST http://localhost:8000/api/v1/research/conduct-research \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "article_002",
    "query": {
      "query_text": "machine learning in content creation",
      "target_domains": ["medium.com", "towardsdatascience.com"],
      "max_results": 3,
      "research_purpose": "Research ML applications in content creation",
      "content_topic": "ML Content Creation"
    },
    "validate_sources": true,
    "include_related_queries": false
  }'
```

### Source Credibility Check

Validate the credibility of specific sources:

```bash
curl -X POST http://localhost:8000/api/v1/research/check-credibility \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "urls_to_check": [
      "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "https://www.example-blog.com/ai-content",
      "https://suspicious-source.org/unverified-claims"
    ],
    "content_context": "AI content generation article"
  }'
```

## Export Management Examples

### Export to WordPress

Export content to WordPress in blog format:

```bash
curl -X POST http://localhost:8000/api/v1/export/export-content \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "draft_001",
    "content": "This is a sample blog post about AI content generation. It includes multiple paragraphs and covers the basics of the topic...",
    "export_format": "blog",
    "target_platform": "wordpress",
    "platform_config": {
      "platform": "wordpress",
      "credentials": {
        "username": "your_username",
        "password": "your_password"
      },
      "settings": {
        "site_url": "https://your-site.com",
        "category": "Technology",
        "tags": ["AI", "Content", "Automation"]
      }
    },
    "metadata": {
      "title": "The Future of AI Content Generation",
      "author": "Content Creator"
    },
    "include_images": true,
    "optimize_for_platform": true
  }'
```

### Export to Social Media

Export content for Twitter with platform-specific optimization:

```bash
curl -X POST http://localhost:8000/api/v1/export/export-content \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "social_001",
    "content": "AI is revolutionizing content creation. Modern tools can generate high-quality, relevant content in seconds. The future of digital marketing is here!",
    "export_format": "social_media",
    "target_platform": "twitter",
    "platform_config": {
      "platform": "twitter",
      "credentials": {
        "api_key": "your_api_key",
        "api_secret": "your_api_secret"
      }
    },
    "metadata": {
      "hashtags": ["AI", "ContentMarketing", "Innovation"]
    },
    "include_images": false,
    "optimize_for_platform": true
  }'
```

### Batch Export

Export multiple pieces of content in a single request:

```bash
curl -X POST http://localhost:8000/api/v1/export/batch-export \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "export_requests": [
      {
        "content_id": "post_001",
        "content": "First blog post content...",
        "export_format": "blog",
        "target_platform": "medium",
        "metadata": {"title": "First Post"}
      },
      {
        "content_id": "post_002",
        "content": "Second blog post content...",
        "export_format": "blog",
        "target_platform": "wordpress",
        "metadata": {"title": "Second Post"}
      }
    ],
    "parallel_processing": true,
    "continue_on_failure": true
  }'
```

## Workflow Orchestration Examples

### Create Content Creation Workflow

Create a workflow that generates content, analyzes SEO, and exports to a platform:

```bash
curl -X POST http://localhost:8000/api/v1/workflow/create-workflow \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "workflow_name": "Complete Content Creation Pipeline",
    "description": "Full pipeline: generate, optimize, and publish content",
    "steps": [
      {
        "step_id": "gen_step_1",
        "step_type": "content_generation",
        "description": "Generate initial content draft",
        "input_data": {
          "id": "workflow_content_001",
          "topic": "Benefits of AI in Digital Marketing",
          "audience": "marketing_professionals",
          "tone": "informative",
          "style": "professional",
          "format": "blog_post",
          "length": 800,
          "keywords": ["AI", "digital marketing", "automation"],
          "requirements": ["include statistics", "focus on ROI"]
        }
      },
      {
        "step_id": "seo_step_1",
        "step_type": "seo_analysis",
        "description": "Analyze content for SEO optimization",
        "input_data": {
          "content_id": "workflow_content_001",
          "content": "{{gen_step_1.generated_content}}",
          "target_keywords": ["AI", "digital marketing", "automation"]
        }
      },
      {
        "step_id": "export_step_1",
        "step_type": "export",
        "description": "Export to WordPress blog",
        "input_data": {
          "content_id": "workflow_content_001",
          "content": "{{gen_step_1.improved_content}}",
          "export_format": "blog",
          "target_platform": "wordpress"
        }
      }
    ],
    "parallel_execution": false,
    "metadata": {
      "priority": "high",
      "campaign": "Q4_marketing"
    }
  }'
```

### Execute a Workflow

Execute a previously created workflow:

```bash
curl -X POST http://localhost:8000/api/v1/workflow/execute-workflow/workflow_abc123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Check Workflow Status

Monitor the progress of a workflow:

```bash
curl -X GET http://localhost:8000/api/v1/workflow/workflow-status/workflow_abc123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Update Workflow

Pause, resume, or cancel a workflow:

```bash
curl -X POST http://localhost:8000/api/v1/workflow/update-workflow \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "workflow_id": "workflow_abc123",
    "action": "pause"
  }'
```

## Combined Examples

### Research-Based Content Creation

Combine research and content generation:

1. First, conduct research:
```bash
curl -X POST http://localhost:8000/api/v1/research/conduct-research \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "research_content_001",
    "query": {
      "query_text": "latest trends in content marketing automation",
      "max_results": 5,
      "research_purpose": "Content creation research",
      "content_topic": "Marketing Automation"
    },
    "validate_sources": true
  }'
```

2. Use research results to generate content:
```bash
curl -X POST http://localhost:8000/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "id": "generated_content_001",
    "topic": "Content Marketing Automation Trends",
    "audience": "marketing_managers",
    "tone": "informative",
    "style": "professional",
    "format": "blog_post",
    "length": 600,
    "keywords": ["automation", "content marketing", "AI"],
    "requirements": ["include research findings", "mention top tools"]
  }'
```

3. Export the generated content:
```bash
curl -X POST http://localhost:8000/api/v1/export/export-content \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "content_id": "generated_content_001",
    "content": "Based on recent research, here are the top trends in content marketing automation...",
    "export_format": "blog",
    "target_platform": "medium",
    "metadata": {"title": "Top Content Marketing Automation Trends for 2024"}
  }'
```

## Environment Variables

Make sure to set the following environment variables for platform integrations:

```
# Research Configuration
SERP_API_KEY=your_serps_api_key
RESEARCH_TIMEOUT=10

# Export Configuration
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
WORDPRESS_SITE_URL=https://your-site.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_TTL=3600
```

## Best Practices

1. **Caching**: Research results are automatically cached to improve performance and reduce API calls.

2. **Validation**: Always validate export formats before sending large amounts of content.

3. **Error Handling**: Implement retry logic for failed exports and monitor workflow status.

4. **Rate Limiting**: Be mindful of API rate limits for research and export platforms.

5. **Security**: Never expose API keys in client-side code or public repositories.