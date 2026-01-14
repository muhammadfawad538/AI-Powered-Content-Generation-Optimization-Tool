# Return Mechanisms for AI Content Generation & Optimization Tool Subagents

## Overview
This document outlines how each subagent communicates its results back to the main Claude Code instance, ensuring proper data flow, user control, and system integration while maintaining the project's principles of transparency and user decision-making authority.

## Communication Protocols

### Standard Response Format
All subagents must return results in the following standardized JSON format:

```json
{
  "subagent_id": "unique_subagent_identifier",
  "timestamp": "ISO_8601_timestamp",
  "status": "success|error|partial",
  "results": {},
  "metadata": {
    "execution_time": "milliseconds",
    "version": "subagent_version",
    "user_controlled": true
  },
  "quality_metrics": {},
  "next_steps": []
}
```

## Content Generation Subagent Return Mechanism

### Return Interface
- **Method**: Asynchronous callback to main Claude Code
- **Channel**: Named pipe or message queue
- **Format**: Standard response format with generated content in `results.content`

### Result Structure
```json
{
  "subagent_id": "content-generation-v1",
  "timestamp": "2026-01-13T10:30:00Z",
  "status": "success",
  "results": {
    "content": "Generated text content...",
    "word_count": 500,
    "quality_score": 0.92,
    "seo_analysis": {
      "score": 0.85,
      "keyword_density": 0.02
    },
    "originality_check": {
      "similarity_score": 0.05,
      "sources_verified": true
    }
  },
  "metadata": {
    "execution_time": 2450,
    "version": "1.0.0",
    "user_controlled": true
  },
  "quality_metrics": {
    "relevance": 0.95,
    "coherence": 0.90,
    "readability": 0.88
  },
  "next_steps": [
    "optimize_content",
    "validate_seo",
    "request_user_approval"
  ]
}
```

### User Interaction Points
- Provides content for user review and approval
- Offers alternative versions if requested
- Supports iterative refinement based on user feedback

## Content Optimization Subagent Return Mechanism

### Return Interface
- **Method**: Asynchronous callback to main Claude Code
- **Channel**: Named pipe or message queue
- **Format**: Standard response format with optimization results in `results.optimization`

### Result Structure
```json
{
  "subagent_id": "content-optimization-v1",
  "timestamp": "2026-01-13T10:32:00Z",
  "status": "success",
  "results": {
    "optimized_content": "Improved content text...",
    "original_content": "Original content text...",
    "improvements_made": [
      "enhanced_readability",
      "improved_keyword_placement",
      "better_structure"
    ],
    "seo_improvements": {
      "before_score": 0.70,
      "after_score": 0.88
    },
    "readability_metrics": {
      "before_grade": 12,
      "after_grade": 8
    },
    "compliance_check": {
      "ethical_compliant": true,
      "policy_adherent": true
    }
  },
  "metadata": {
    "execution_time": 3120,
    "version": "1.0.0",
    "user_controlled": true
  },
  "quality_metrics": {
    "readability_improvement": 0.35,
    "seo_improvement": 0.18,
    "engagement_potential": 0.82
  },
  "next_steps": [
    "validate_quality",
    "request_user_approval",
    "generate_comparison_report"
  ]
}
```

### User Interaction Points
- Presents before/after comparison
- Highlights specific improvements made
- Requests user approval for changes

## Research Subagent Return Mechanism

### Return Interface
- **Method**: Asynchronous callback to main Claude Code
- **Channel**: Named pipe or message queue
- **Format**: Standard response format with research results in `results.research`

### Result Structure
```json
{
  "subagent_id": "research-v1",
  "timestamp": "2026-01-13T10:35:00Z",
  "status": "success",
  "results": {
    "findings": [
      {
        "topic": "Main finding",
        "summary": "Brief summary of the finding",
        "confidence": 0.92,
        "source_url": "https://example.com/source"
      }
    ],
    "source_list": [
      {
        "url": "https://example.com/source1",
        "credibility_score": 0.95,
        "relevance_score": 0.88
      }
    ],
    "data_summary": {
      "key_points": ["point1", "point2"],
      "statistics": {},
      "trends_identified": []
    },
    "credibility_assessment": {
      "overall_credibility": 0.89,
      "potential_biases": [],
      "verification_status": "verified"
    },
    "ethical_review": {
      "ethics_check_passed": true,
      "concerns_flagged": []
    }
  },
  "metadata": {
    "execution_time": 4200,
    "version": "1.0.0",
    "user_controlled": true
  },
  "quality_metrics": {
    "source_credentiality": 0.92,
    "information_relevance": 0.88,
    "completeness_score": 0.85
  },
  "next_steps": [
    "integrate_findings",
    "validate_sources",
    "request_user_confirmation"
  ]
}
```

### User Interaction Points
- Lists all sources with credibility scores
- Flags any ethical concerns
- Requests user confirmation to proceed

## Workflow Orchestrator Subagent Return Mechanism

### Return Interface
- **Method**: Asynchronous callback to main Claude Code
- **Channel**: Named pipe or message queue
- **Format**: Standard response format with workflow results in `results.workflow`

### Result Structure
```json
{
  "subagent_id": "workflow-orchestrator-v1",
  "timestamp": "2026-01-13T10:40:00Z",
  "status": "success",
  "results": {
    "workflow_id": "wf-abc123",
    "final_output": {},
    "subagent_executions": [
      {
        "subagent": "research-v1",
        "status": "completed",
        "duration": 4200,
        "output_keys": ["findings", "sources"]
      }
    ],
    "dependencies_resolved": true,
    "errors_encountered": [],
    "quality_gate_passed": true
  },
  "metadata": {
    "execution_time": 12500,
    "version": "1.0.0",
    "user_controlled": true
  },
  "quality_metrics": {
    "workflow_efficiency": 0.85,
    "resource_utilization": 0.72,
    "error_rate": 0.0
  },
  "next_steps": [
    "present_final_output",
    "request_user_feedback",
    "archive_workflow_results"
  ]
}
```

### User Interaction Points
- Provides summary of all subagent activities
- Offers option to rerun specific subagents
- Requests user feedback on overall workflow

## Error Handling and Recovery

### Error Return Format
When subagents encounter errors, they return:

```json
{
  "subagent_id": "subagent-identifier",
  "timestamp": "ISO_8601_timestamp",
  "status": "error",
  "results": {},
  "metadata": {
    "execution_time": "milliseconds",
    "version": "subagent_version",
    "user_controlled": true
  },
  "error_details": {
    "type": "error_type",
    "message": "descriptive_error_message",
    "recovery_suggestion": "suggested_recovery_action"
  },
  "quality_metrics": {},
  "next_steps": ["retry", "skip", "manual_intervention"]
}
```

## Quality Assurance Checks

Each subagent performs internal quality checks before returning results:
- Validates output format and completeness
- Verifies adherence to ethical guidelines
- Confirms user control mechanisms are intact
- Ensures data integrity and authenticity