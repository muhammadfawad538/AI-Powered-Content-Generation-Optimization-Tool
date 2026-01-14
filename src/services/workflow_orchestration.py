"""
Workflow Orchestration Service

This module provides functionality for managing and orchestrating
complex workflows involving multiple content generation and optimization steps.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..models.workflow import (
    WorkflowRequest, WorkflowResponse, WorkflowUpdateRequest,
    WorkflowState, WorkflowStep, WorkflowStepStatusEnum, WorkflowStatusEnum,
    WorkflowHistoryItem
)
from ..models.content_generation import ContentGenerationRequest, ContentGenerationResponse
from ..models.seo_analysis import SEOAnalysisRequest, SEOAnalysisResponse
from ..models.quality_review import QualityReviewRequest, QualityReviewResponse
from ..models.ethics_report import EthicsCheckRequest, EthicsCheckResponse
from ..models.research_result import ResearchRequest, ResearchResponse
from ..models.export_package import ExportRequest, ExportResponse
from ..services.content_generation import ContentGenerationService
from ..services.seo_analysis import SEOAnalysisService
from ..services.quality_review import QualityReviewService
from ..services.ethics_review import EthicsReviewService
from ..services.research_assistance import ResearchAssistanceService
from ..services.export_management import ExportManagementService
from ..config.settings import settings
from ..utils.workflow_helpers import generate_workflow_id, calculate_workflow_progress, WorkflowCache
from ..utils.logging_config import workflow_logger


class WorkflowOrchestrationService:
    """Service class for orchestrating complex multi-step workflows."""

    def __init__(self):
        """Initialize the Workflow Orchestration Service."""
        self.content_service = ContentGenerationService()
        self.seo_service = SEOAnalysisService()
        self.quality_service = QualityReviewService()
        self.ethics_service = EthicsReviewService()
        self.research_service = ResearchAssistanceService()
        self.export_service = ExportManagementService()
        self.cache = WorkflowCache(ttl_seconds=settings.redis_ttl)
        self.active_workflows: Dict[str, WorkflowState] = {}
        self.logger = workflow_logger

    async def create_workflow(self, request: WorkflowRequest) -> WorkflowResponse:
        """
        Create and initialize a new workflow.

        Args:
            request: Workflow request containing steps to execute

        Returns:
            Workflow response with initial state
        """
        workflow_id = generate_workflow_id()
        self.logger.info(f"Creating workflow '{request.workflow_name}' with ID {workflow_id} containing {len(request.steps)} steps")

        # Create initial workflow state
        initial_state = WorkflowState(
            workflow_id=workflow_id,
            workflow_name=request.workflow_name,
            status=WorkflowStatusEnum.PENDING,
            steps=[],
            current_step_index=None,
            progress=0.0,
            history=[],
            metadata=request.metadata
        )

        # Initialize steps
        for i, step in enumerate(request.steps):
            step_id = step.step_id or f"step_{i+1}"
            initial_state.steps.append(WorkflowStep(
                step_id=step_id,
                step_type=step.step_type,
                description=step.description,
                input_data=step.input_data,
                status=WorkflowStepStatusEnum.PENDING
            ))
            self.logger.debug(f"Added step {step_id} of type {step.step_type}: {step.description}")

        # Store the initial state
        self.active_workflows[workflow_id] = initial_state

        # Create response
        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_name=request.workflow_name,
            status=WorkflowStatusEnum.PENDING,
            total_steps=len(initial_state.steps),
            completed_steps=0,
            steps=initial_state.steps,
            progress=0.0,
            metadata=request.metadata
        )

        # Log workflow creation
        from ..utils.logging_config import log_workflow_event
        log_workflow_event(
            self.logger,
            workflow_id,
            "WORKFLOW_CREATED",
            status="PENDING",
            message=f"Workflow '{request.workflow_name}' created with {len(request.steps)} steps"
        )

        self.logger.info(f"Successfully created workflow '{request.workflow_name}' with ID {workflow_id}")
        return response

    async def execute_workflow(self, workflow_id: str) -> WorkflowResponse:
        """
        Execute a workflow with the given ID.

        Args:
            workflow_id: ID of the workflow to execute

        Returns:
            Workflow response with execution state
        """
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        workflow_state = self.active_workflows[workflow_id]
        workflow_state.status = WorkflowStatusEnum.RUNNING
        workflow_state.started_at = datetime.utcnow()

        # Add history entry
        workflow_state.history.append(WorkflowHistoryItem(
            workflow_id=workflow_id,
            step_id="workflow_start",
            status=WorkflowStepStatusEnum.EXECUTING,
            message="Workflow execution started"
        ))

        completed_steps = 0

        try:
            # Execute steps sequentially or in parallel based on configuration
            if workflow_state.metadata.get('parallel_execution', False):
                # Execute compatible steps in parallel
                await self._execute_parallel_steps(workflow_state)
            else:
                # Execute steps sequentially
                for i, step in enumerate(workflow_state.steps):
                    workflow_state.current_step_index = i
                    await self._execute_single_step(workflow_state, step, i)

                    if step.status == WorkflowStepStatusEnum.COMPLETED:
                        completed_steps += 1
                    else:
                        # If any step fails, stop the workflow
                        break

            # Update final state
            workflow_state.status = WorkflowStatusEnum.COMPLETED if all(
                s.status == WorkflowStepStatusEnum.COMPLETED for s in workflow_state.steps
            ) else WorkflowStatusEnum.FAILED

            workflow_state.completed_at = datetime.utcnow()
            workflow_state.progress = calculate_workflow_progress(
                completed_steps, len(workflow_state.steps)
            )

            # Add completion history entry
            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_id,
                step_id="workflow_end",
                status=WorkflowStepStatusEnum.COMPLETED if workflow_state.status == WorkflowStatusEnum.COMPLETED else WorkflowStepStatusEnum.FAILED,
                message=f"Workflow completed with status: {workflow_state.status}"
            ))

        except Exception as e:
            # Mark workflow as failed
            workflow_state.status = WorkflowStatusEnum.FAILED
            workflow_state.error_message = str(e)
            workflow_state.completed_at = datetime.utcnow()

            # Add error history entry
            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_id,
                step_id="workflow_error",
                status=WorkflowStepStatusEnum.FAILED,
                message=f"Workflow failed with error: {str(e)}"
            ))

        # Create response
        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_name=workflow_state.workflow_name,
            status=workflow_state.status,
            current_step=workflow_state.steps[workflow_state.current_step_index].step_id if workflow_state.current_step_index is not None else None,
            progress=workflow_state.progress,
            total_steps=len(workflow_state.steps),
            completed_steps=completed_steps,
            steps=workflow_state.steps,
            result=self._extract_workflow_result(workflow_state),
            error_message=workflow_state.error_message,
            created_at=workflow_state.created_at,
            started_at=workflow_state.started_at,
            completed_at=workflow_state.completed_at,
            metadata=workflow_state.metadata
        )

        return response

    async def _execute_single_step(self, workflow_state: WorkflowState, step: WorkflowStep, step_index: int):
        """
        Execute a single workflow step.

        Args:
            workflow_state: Current workflow state
            step: Step to execute
            step_index: Index of the step in the workflow
        """
        step.start_time = datetime.utcnow()
        step.status = WorkflowStepStatusEnum.EXECUTING

        # Add history entry
        workflow_state.history.append(WorkflowHistoryItem(
            workflow_id=workflow_state.workflow_id,
            step_id=step.step_id,
            status=WorkflowStepStatusEnum.EXECUTING,
            message=f"Started executing step: {step.description}"
        ))

        try:
            # Execute the step based on its type
            result = await self._execute_step_by_type(step)

            step.output_data = result
            step.status = WorkflowStepStatusEnum.COMPLETED
            step.end_time = datetime.utcnow()
            step.duration = (step.end_time - step.start_time).total_seconds()

            # Add success history entry
            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_state.workflow_id,
                step_id=step.step_id,
                status=WorkflowStepStatusEnum.COMPLETED,
                message=f"Step completed successfully: {step.description}"
            ))

        except Exception as e:
            step.status = WorkflowStepStatusEnum.FAILED
            step.error_message = str(e)
            step.end_time = datetime.utcnow()
            step.duration = (step.end_time - step.start_time).total_seconds()

            # Add failure history entry
            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_state.workflow_id,
                step_id=step.step_id,
                status=WorkflowStepStatusEnum.FAILED,
                message=f"Step failed with error: {str(e)}"
            ))

    async def _execute_parallel_steps(self, workflow_state: WorkflowState):
        """
        Execute compatible workflow steps in parallel.

        Args:
            workflow_state: Current workflow state
        """
        # For now, execute all steps sequentially (parallel execution would require
        # more complex dependency tracking and resource management)
        for i, step in enumerate(workflow_state.steps):
            workflow_state.current_step_index = i
            await self._execute_single_step(workflow_state, step, i)

    async def _execute_step_by_type(self, step: WorkflowStep) -> Dict[str, Any]:
        """
        Execute a step based on its type.

        Args:
            step: Step to execute

        Returns:
            Result of the step execution
        """
        if step.step_type == "content_generation":
            return await self._execute_content_generation_step(step.input_data)
        elif step.step_type == "seo_analysis":
            return await self._execute_seo_analysis_step(step.input_data)
        elif step.step_type == "quality_review":
            return await self._execute_quality_review_step(step.input_data)
        elif step.step_type == "ethics_check":
            return await self._execute_ethics_check_step(step.input_data)
        elif step.step_type == "research":
            return await self._execute_research_step(step.input_data)
        elif step.step_type == "export":
            return await self._execute_export_step(step.input_data)
        elif step.step_type == "custom":
            return await self._execute_custom_step(step.input_data)
        else:
            raise ValueError(f"Unknown step type: {step.step_type}")

    async def _execute_content_generation_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a content generation step."""
        # Create a ContentGenerationRequest from input data
        request = ContentGenerationRequest(**input_data)
        response = await self.content_service.generate_content(request)

        return {
            "content_id": response.id,
            "generated_content": response.content,
            "quality_score": response.quality_score,
            "word_count": response.word_count,
            "generation_time": response.generation_time,
            "status": response.status
        }

    async def _execute_seo_analysis_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an SEO analysis step."""
        # Create an SEOAnalysisRequest from input data
        request = SEOAnalysisRequest(**input_data)
        response = self.seo_service.analyze_content(request)

        return {
            "content_id": response.content_id,
            "keyword_density": response.keyword_density,
            "readability_score": response.readability_score,
            "heading_structure": response.heading_structure,
            "seo_score": response.seo_score,
            "improvement_suggestions": response.improvement_suggestions
        }

    async def _execute_quality_review_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a quality review step."""
        # Create a QualityReviewRequest from input data
        request = QualityReviewRequest(**input_data)
        response = self.quality_service.review_content(request)

        return {
            "content_id": response.content_id,
            "original_content": response.original_content,
            "improved_content": response.improved_content,
            "clarity_score": response.clarity_score,
            "readability_score": response.readability_score,
            "engagement_score": response.engagement_score,
            "flow_score": response.flow_score
        }

    async def _execute_ethics_check_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an ethics check step."""
        # Create an EthicsCheckRequest from input data
        request = EthicsCheckRequest(**input_data)
        response = self.ethics_service.check_content(request)

        return {
            "content_id": response.content_id,
            "plagiarism_detected": response.plagiarism_detected,
            "ethical_risk_level": response.ethical_risk_level,
            "ethical_concerns": response.ethical_concerns,
            "policy_violations": response.policy_violations,
            "confidence_score": response.confidence_score,
            "recommendations": response.recommendations
        }

    async def _execute_research_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a research step."""
        # Create a ResearchRequest from input data
        request = ResearchRequest(**input_data)
        response = await self.research_service.conduct_research(request)

        return {
            "content_id": response.content_id,
            "query_id": response.research_results.query_id,
            "total_results": len(response.research_results.search_results),
            "research_summary": response.research_results.research_summary,
            "key_insights": response.research_results.key_insights
        }

    async def _execute_export_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an export step."""
        # Create an ExportRequest from input data
        request = ExportRequest(**input_data)
        response = await self.export_service.export_content(request)

        return {
            "export_id": response.export_id,
            "content_id": response.content_id,
            "export_status": response.export_status,
            "export_url": response.export_url,
            "platform_identifier": response.platform_identifier
        }

    async def _execute_custom_step(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a custom step."""
        # For now, just return the input data as the result
        # In a real implementation, this would execute custom business logic
        return {
            "custom_step_result": "executed",
            "input_data": input_data,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def get_workflow_status(self, workflow_id: str) -> WorkflowResponse:
        """
        Get the current status of a workflow.

        Args:
            workflow_id: ID of the workflow

        Returns:
            Current workflow status
        """
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        workflow_state = self.active_workflows[workflow_id]

        # Calculate completed steps
        completed_steps = sum(1 for step in workflow_state.steps if step.status == WorkflowStepStatusEnum.COMPLETED)

        # Create response
        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_name=workflow_state.workflow_name,
            status=workflow_state.status,
            current_step=workflow_state.steps[workflow_state.current_step_index].step_id if workflow_state.current_step_index is not None else None,
            progress=calculate_workflow_progress(completed_steps, len(workflow_state.steps)),
            total_steps=len(workflow_state.steps),
            completed_steps=completed_steps,
            steps=workflow_state.steps,
            result=self._extract_workflow_result(workflow_state),
            error_message=workflow_state.error_message,
            created_at=workflow_state.created_at,
            started_at=workflow_state.started_at,
            completed_at=workflow_state.completed_at,
            metadata=workflow_state.metadata
        )

        return response

    def _extract_workflow_result(self, workflow_state: WorkflowState) -> Optional[Dict[str, Any]]:
        """
        Extract the final result from the workflow state.

        Args:
            workflow_state: Current workflow state

        Returns:
            Final workflow result or None if not complete
        """
        if workflow_state.status != WorkflowStatusEnum.COMPLETED:
            return None

        result = {
            "workflow_id": workflow_state.workflow_id,
            "workflow_name": workflow_state.workflow_name,
            "steps_executed": len(workflow_state.steps),
            "steps_successful": sum(1 for step in workflow_state.steps if step.status == WorkflowStepStatusEnum.COMPLETED),
            "execution_history": [
                {
                    "step_id": item.step_id,
                    "status": item.status,
                    "timestamp": item.timestamp.isoformat(),
                    "message": item.message
                } for item in workflow_state.history
            ]
        }

        # Add output data from completed steps
        for step in workflow_state.steps:
            if step.status == WorkflowStepStatusEnum.COMPLETED and step.output_data:
                result[f"step_{step.step_id}_result"] = step.output_data

        return result

    async def update_workflow(self, request: WorkflowUpdateRequest) -> WorkflowResponse:
        """
        Update a workflow's state or configuration.

        Args:
            request: Request to update the workflow

        Returns:
            Updated workflow status
        """
        workflow_id = request.workflow_id

        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        workflow_state = self.active_workflows[workflow_id]

        if request.action == "pause":
            workflow_state.status = WorkflowStatusEnum.PAUSED
            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_id,
                step_id="workflow_pause",
                status=WorkflowStepStatusEnum.PENDING,
                message="Workflow paused by user request"
            ))
        elif request.action == "resume":
            if workflow_state.status == WorkflowStatusEnum.PAUSED:
                workflow_state.status = WorkflowStatusEnum.RUNNING
                workflow_state.history.append(WorkflowHistoryItem(
                    workflow_id=workflow_id,
                    step_id="workflow_resume",
                    status=WorkflowStepStatusEnum.EXECUTING,
                    message="Workflow resumed by user request"
                ))
        elif request.action == "cancel":
            workflow_state.status = WorkflowStatusEnum.CANCELLED
            workflow_state.completed_at = datetime.utcnow()
            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_id,
                step_id="workflow_cancel",
                status=WorkflowStepStatusEnum.SKIPPED,
                message="Workflow cancelled by user request"
            ))
        elif request.action == "rerun":
            # Reset workflow to initial state
            for step in workflow_state.steps:
                step.status = WorkflowStepStatusEnum.PENDING
                step.output_data = None
                step.error_message = None
                step.start_time = None
                step.end_time = None
                step.duration = None

            workflow_state.status = WorkflowStatusEnum.PENDING
            workflow_state.current_step_index = None
            workflow_state.progress = 0.0
            workflow_state.started_at = None
            workflow_state.completed_at = None
            workflow_state.error_message = None

            workflow_state.history.append(WorkflowHistoryItem(
                workflow_id=workflow_id,
                step_id="workflow_rerun",
                status=WorkflowStepStatusEnum.PENDING,
                message="Workflow reset for rerun by user request"
            ))

        # Return updated status
        completed_steps = sum(1 for step in workflow_state.steps if step.status == WorkflowStepStatusEnum.COMPLETED)
        workflow_state.progress = calculate_workflow_progress(completed_steps, len(workflow_state.steps))

        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_name=workflow_state.workflow_name,
            status=workflow_state.status,
            current_step=workflow_state.steps[workflow_state.current_step_index].step_id if workflow_state.current_step_index is not None else None,
            progress=workflow_state.progress,
            total_steps=len(workflow_state.steps),
            completed_steps=completed_steps,
            steps=workflow_state.steps,
            result=self._extract_workflow_result(workflow_state),
            error_message=workflow_state.error_message,
            created_at=workflow_state.created_at,
            started_at=workflow_state.started_at,
            completed_at=workflow_state.completed_at,
            metadata=workflow_state.metadata
        )

        return response

    async def list_workflows(self) -> List[WorkflowResponse]:
        """
        List all active workflows.

        Returns:
            List of workflow responses
        """
        responses = []
        for workflow_id in self.active_workflows:
            try:
                response = await self.get_workflow_status(workflow_id)
                responses.append(response)
            except Exception:
                # Skip workflows that can't be retrieved
                continue

        return responses