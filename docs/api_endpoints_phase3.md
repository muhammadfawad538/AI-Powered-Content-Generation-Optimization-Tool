# API Endpoints - Phase 3: Research & Export Features

This document describes the new API endpoints added in Phase 3, which include Research Assistance, Export Management, and Workflow Orchestration features.

## Research Assistance Endpoints

Base URL: `/api/v1/research`

### POST `/conduct-research`
Conduct research based on the provided query.

**Request Body:**
```json
{
  "content_id": "string",
  "query": {
    "query_text": "AI content generation best practices",
    "target_domains": ["example.com"],
    "max_results": 10,
    "research_purpose": "Finding best practices for AI-generated content",
    "content_topic": "AI Content Generation"
  },
  "validate_sources": true,
  "include_related_queries": true
}
```

**Response:**
```json
{
  "content_id": "string",
  "research_results": {
    "query_id": "string",
    "original_query": {},
    "search_results": [
      {
        "title": "string",
        "url": "string",
        "snippet": "string",
        "source_domain": "string",
        "published_date": "string",
        "relevance_score": 0.0,
        "credibility_level": "high|medium|low|unknown"
      }
    ],
    "total_results_found": 0,
    "filtered_results_count": 0,
    "credibility_summary": {},
    "research_summary": "string",
    "key_insights": ["string"],
    "related_topics": ["string"],
    "search_duration": 0.0
  },
  "status": "completed",
  "completion_timestamp": "2023-01-01T00:00:00Z"
}
```

### POST `/check-credibility`
Check credibility of specific sources.

**Request Body:**
```json
{
  "urls_to_check": ["https://example.com"],
  "content_context": "string"
}
```

**Response:**
```json
{
  "request_id": "string",
  "assessments": [
    {
      "source_url": "string",
      "credibility_level": "high|medium|low|unknown",
      "assessment_criteria": ["string"],
      "confidence_score": 0.0,
      "assessment_reasoning": "string",
      "assessed_by": "string",
      "assessment_timestamp": "2023-01-01T00:00:00Z"
    }
  ],
  "summary": {},
  "overall_trustworthiness": 0.0
}
```

### GET `/health`
Health check for research service.

---

## Export Management Endpoints

Base URL: `/api/v1/export`

### POST `/export-content`
Export content to the specified platform and format.

**Request Body:**
```json
{
  "content_id": "string",
  "content": "string",
  "export_format": "blog|social_media|ad_campaign|email_newsletter|pdf|markdown|plain_text",
  "target_platform": "wordpress|medium|twitter|facebook|linkedin|google_ads|facebook_ads|custom",
  "platform_config": {
    "platform": "string",
    "credentials": {},
    "settings": {},
    "enabled": true
  },
  "metadata": {},
  "include_images": true,
  "optimize_for_platform": true
}
```

**Response:**
```json
{
  "export_id": "string",
  "content_id": "string",
  "export_status": "pending|processing|success|failed|cancelled",
  "export_url": "string",
  "platform_identifier": "string",
  "message": "string",
  "export_duration": 0.0,
  "completion_timestamp": "2023-01-01T00:00:00Z"
}
```

### POST `/batch-export`
Export multiple pieces of content in batch.

**Request Body:**
```json
{
  "export_requests": [
    {
      "content_id": "string",
      "content": "string",
      "export_format": "string",
      "target_platform": "string"
    }
  ],
  "parallel_processing": true,
  "continue_on_failure": true
}
```

**Response:**
```json
{
  "batch_id": "string",
  "total_exports": 0,
  "successful_exports": 0,
  "failed_exports": 0,
  "results": [],
  "batch_status": "pending|processing|success|failed|cancelled",
  "completion_timestamp": "2023-01-01T00:00:00Z"
}
```

### GET `/supported-formats`
Get list of supported export formats.

### GET `/supported-platforms`
Get list of supported export platforms.

---

## Workflow Orchestration Endpoints

Base URL: `/api/v1/workflow`

### POST `/create-workflow`
Create a new workflow with the specified steps.

**Request Body:**
```json
{
  "workflow_name": "string",
  "description": "string",
  "steps": [
    {
      "step_id": "string",
      "step_type": "content_generation|seo_analysis|quality_review|ethics_check|research|export|custom",
      "description": "string",
      "input_data": {},
      "status": "pending|executing|completed|failed|skipped"
    }
  ],
  "parallel_execution": false,
  "callback_url": "string",
  "metadata": {}
}
```

**Response:**
```json
{
  "workflow_id": "string",
  "workflow_name": "string",
  "status": "pending|running|completed|failed|cancelled|paused",
  "current_step": "string",
  "progress": 0.0,
  "total_steps": 0,
  "completed_steps": 0,
  "steps": [],
  "result": {},
  "error_message": "string",
  "created_at": "2023-01-01T00:00:00Z",
  "started_at": "2023-01-01T00:00:00Z",
  "completed_at": "2023-01-01T00:00:00Z",
  "metadata": {}
}
```

### POST `/execute-workflow/{workflow_id}`
Execute a workflow with the given ID.

### GET `/workflow-status/{workflow_id}`
Get the current status of a workflow.

### POST `/update-workflow`
Update a workflow's state or configuration.

**Request Body:**
```json
{
  "workflow_id": "string",
  "action": "pause|resume|cancel|rerun",
  "step_id": "string"
}
```

### GET `/list-workflows`
List all active workflows.

### DELETE `/cleanup-workflow/{workflow_id}`
Remove a completed workflow from active workflows.

### GET `/health`
Health check for workflow service.

---

## Authentication

All endpoints require a valid API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```
or
```
X-API-Key: YOUR_API_KEY
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages in the following format:
```json
{
  "detail": "Error message"
}
```

Common error codes:
- 400: Bad Request - Invalid input parameters
- 401: Unauthorized - Invalid or missing API key
- 404: Not Found - Requested resource not found
- 500: Internal Server Error - Server-side error occurred