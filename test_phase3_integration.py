"""
Integration Test Script for Phase 3: Research & Export Features

This script tests the integration between research, export, and workflow orchestration features.
"""

import asyncio
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.research_result import ResearchRequest, ResearchQuery
from models.export_package import ExportRequest, ExportFormatEnum, ExportPlatformEnum
from models.workflow import WorkflowRequest, WorkflowStep
from services.research_assistance import ResearchAssistanceService
from services.export_management import ExportManagementService
from services.workflow_orchestration import WorkflowOrchestrationService


async def test_research_functionality():
    """Test the research functionality."""
    print("Testing Research Functionality...")

    research_service = ResearchAssistanceService()

    # Create a research request
    research_request = ResearchRequest(
        content_id="test_content_1",
        query=ResearchQuery(
            query_text="AI content generation best practices",
            target_domains=["example.com"],
            max_results=5,
            research_purpose="Finding best practices for AI-generated content",
            content_topic="AI Content Generation"
        ),
        validate_sources=True,
        include_related_queries=True
    )

    try:
        result = await research_service.conduct_research(research_request)
        print(f"✓ Research completed successfully. Found {len(result.research_results.search_results)} results.")
        print(f"  Research summary: {result.research_results.research_summary[:100]}...")

        # Test credibility check
        from models.research_result import CredibilityCheckRequest
        credibility_request = CredibilityCheckRequest(
            urls_to_check=[result.research_results.search_results[0].url if result.research_results.search_results else "https://example.com"]
        )
        credibility_result = await research_service.check_source_credibility(credibility_request)
        print(f"✓ Credibility check completed. Overall trustworthiness: {credibility_result.overall_trustworthiness:.2f}")

        return True
    except Exception as e:
        print(f"✗ Research functionality failed: {e}")
        return False


async def test_export_functionality():
    """Test the export functionality."""
    print("\nTesting Export Functionality...")

    export_service = ExportManagementService()

    # Create an export request
    export_request = ExportRequest(
        content_id="test_content_1",
        content="This is a sample content for export testing. It includes multiple sentences and covers the basics of the topic.",
        export_format=ExportFormatEnum.BLOG,
        target_platform=ExportPlatformEnum.WORDPRESS,
        metadata={"category": "testing", "tags": ["ai", "content", "test"]}
    )

    try:
        result = await export_service.export_content(export_request)
        print(f"✓ Export completed with status: {result.export_status}")
        print(f"  Message: {result.message}")

        # Test batch export
        batch_request = export_request.copy()
        batch_request.content = "This is the second piece of content for batch testing."
        batch_request.content_id = "test_content_2"

        from models.export_package import BatchExportRequest
        batch_export_request = BatchExportRequest(
            export_requests=[export_request, batch_request],
            parallel_processing=True,
            continue_on_failure=True
        )

        batch_result = await export_service.batch_export(batch_export_request)
        print(f"✓ Batch export completed. Successful: {batch_result.successful_exports}, Failed: {batch_result.failed_exports}")

        return True
    except Exception as e:
        print(f"✗ Export functionality failed: {e}")
        return False


async def test_workflow_functionality():
    """Test the workflow functionality."""
    print("\nTesting Workflow Functionality...")

    workflow_service = WorkflowOrchestrationService()

    # Create a simple workflow with multiple steps
    workflow_request = WorkflowRequest(
        workflow_name="Test Content Creation Workflow",
        description="A test workflow that creates content, analyzes it, and exports it",
        steps=[
            WorkflowStep(
                step_id="step_1",
                step_type="content_generation",
                description="Generate initial content draft",
                input_data={
                    "id": "workflow_test_1",
                    "topic": "AI Content Generation",
                    "audience": "developers",
                    "tone": "informative",
                    "style": "professional",
                    "format": "blog_post",
                    "length": 200,
                    "keywords": ["AI", "content", "generation"],
                    "requirements": ["include best practices", "focus on benefits"]
                }
            ),
            WorkflowStep(
                step_id="step_2",
                step_type="seo_analysis",
                description="Analyze content for SEO optimization",
                input_data={
                    "content_id": "workflow_test_1",
                    "content": "Sample content for SEO analysis...",
                    "target_keywords": ["AI", "content", "generation"]
                }
            ),
            WorkflowStep(
                step_id="step_3",
                step_type="quality_review",
                description="Review content quality",
                input_data={
                    "content_id": "workflow_test_1",
                    "content": "Sample content for quality review...",
                    "target_audience": "developers",
                    "review_aspect": ["clarity", "readability", "engagement"]
                }
            )
        ],
        parallel_execution=False,
        metadata={"priority": "high", "origin": "integration_test"}
    )

    try:
        # Create the workflow
        workflow_response = await workflow_service.create_workflow(workflow_request)
        print(f"✓ Workflow created with ID: {workflow_response.workflow_id}")
        print(f"  Workflow name: {workflow_response.workflow_name}")
        print(f"  Total steps: {workflow_response.total_steps}")

        # Execute the workflow
        execution_response = await workflow_service.execute_workflow(workflow_response.workflow_id)
        print(f"✓ Workflow execution completed with status: {execution_response.status}")
        print(f"  Progress: {execution_response.progress}%")
        print(f"  Completed steps: {execution_response.completed_steps}/{execution_response.total_steps}")

        return True
    except Exception as e:
        print(f"✗ Workflow functionality failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_end_to_end_scenario():
    """Test an end-to-end scenario combining all features."""
    print("\nTesting End-to-End Scenario...")

    try:
        # Step 1: Conduct research
        research_service = ResearchAssistanceService()
        research_request = ResearchRequest(
            content_id="e2e_content_1",
            query=ResearchQuery(
                query_text="machine learning applications in content creation",
                target_domains=[],
                max_results=3,
                research_purpose="Research for content creation",
                content_topic="ML Content Creation"
            ),
            validate_sources=True
        )

        research_result = await research_service.conduct_research(research_request)
        print(f"✓ Research completed: {len(research_result.research_results.search_results)} sources found")

        # Step 2: Generate content based on research
        content_draft = f"Based on research, here are key findings about machine learning in content creation:\n"
        for i, result in enumerate(research_result.research_results.search_results[:2]):
            content_draft += f"\n{i+1}. {result.title}: {result.snippet[:100]}..."

        # Step 3: Export the content
        export_service = ExportManagementService()
        export_request = ExportRequest(
            content_id="e2e_content_1",
            content=content_draft,
            export_format=ExportFormatEnum.BLOG,
            target_platform=ExportPlatformEnum.MEDIUM,
            metadata={"topic": "ML Content Creation", "research_based": True}
        )

        export_result = await export_service.export_content(export_request)
        print(f"✓ Content exported with status: {export_result.export_status}")

        # Step 4: Create and execute a workflow for the content
        workflow_service = WorkflowOrchestrationService()
        workflow_request = WorkflowRequest(
            workflow_name="E2E Content Workflow",
            steps=[
                WorkflowStep(
                    step_id="e2e_step_1",
                    step_type="seo_analysis",
                    description="Analyze SEO for research-based content",
                    input_data={
                        "content_id": "e2e_content_1",
                        "content": content_draft,
                        "target_keywords": ["machine learning", "content creation", "AI"]
                    }
                )
            ]
        )

        workflow_response = await workflow_service.create_workflow(workflow_request)
        execution_response = await workflow_service.execute_workflow(workflow_response.workflow_id)
        print(f"✓ E2E workflow completed with status: {execution_response.status}")

        print("✓ End-to-end scenario completed successfully")
        return True

    except Exception as e:
        print(f"✗ End-to-end scenario failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all integration tests."""
    print("Starting Phase 3 Integration Tests...\n")

    results = []

    # Run all tests
    results.append(("Research Functionality", await test_research_functionality()))
    results.append(("Export Functionality", await test_export_functionality()))
    results.append(("Workflow Functionality", await test_workflow_functionality()))
    results.append(("End-to-End Scenario", await test_end_to_end_scenario()))

    # Print summary
    print("\n" + "="*60)
    print("INTEGRATION TEST SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        icon = "✓" if passed else "✗"
        print(f"{icon} {test_name}: {status}")
        if not passed:
            all_passed = False

    print("="*60)
    if all_passed:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nPhase 3 features (Research, Export, Workflow) are fully integrated and working!")
    else:
        print("❌ SOME INTEGRATION TESTS FAILED")
        print("Please review the failing tests above.")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)