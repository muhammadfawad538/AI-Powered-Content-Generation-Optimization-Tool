"""
Workflow API Routes

This module defines the API endpoints for workflow orchestration functionality.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ...models.workflow import (
    WorkflowRequest, WorkflowResponse, WorkflowUpdateRequest
)
from ...services.workflow_orchestration import WorkflowOrchestrationService
from ..middleware.security import validate_api_key


router = APIRouter()
workflow_service = WorkflowOrchestrationService()


@router.post("/create-workflow", response_model=WorkflowResponse)
async def create_workflow(
    request: WorkflowRequest,
    api_key: str = Depends(validate_api_key)
) -> WorkflowResponse:
    """
    Create a new workflow with the specified steps.

    Args:
        request: Workflow request containing steps to execute
        api_key: Validated API key for authentication

    Returns:
        Workflow response with initial state
    """
    from ..middleware.security import api_logger
    from ..utils.logging_config import log_api_call
    import time

    start_time = time.time()
    try:
        response = await workflow_service.create_workflow(request)

        # Log successful API call
        duration = (time.time() - start_time) * 1000
        log_api_call(
            api_logger,
            "/api/v1/workflow/create-workflow",
            "POST",
            request_data={"workflow_name": request.workflow_name, "total_steps": len(request.steps)},
            response_status=200,
            duration_ms=duration
        )

        return response
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        api_logger.error(f"Error creating workflow: {str(e)}")
        log_api_call(
            api_logger,
            "/api/v1/workflow/create-workflow",
            "POST",
            response_status=500,
            duration_ms=duration
        )
        raise HTTPException(status_code=500, detail=f"Error creating workflow: {str(e)}")


@router.post("/execute-workflow/{workflow_id}", response_model=WorkflowResponse)
async def execute_workflow(
    workflow_id: str,
    api_key: str = Depends(validate_api_key)
) -> WorkflowResponse:
    """
    Execute a workflow with the given ID.

    Args:
        workflow_id: ID of the workflow to execute
        api_key: Validated API key for authentication

    Returns:
        Workflow response with execution state
    """
    try:
        response = await workflow_service.execute_workflow(workflow_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing workflow: {str(e)}")


@router.get("/workflow-status/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(
    workflow_id: str,
    api_key: str = Depends(validate_api_key)
) -> WorkflowResponse:
    """
    Get the current status of a workflow.

    Args:
        workflow_id: ID of the workflow to check
        api_key: Validated API key for authentication

    Returns:
        Current workflow status
    """
    try:
        response = await workflow_service.get_workflow_status(workflow_id)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting workflow status: {str(e)}")


@router.post("/update-workflow", response_model=WorkflowResponse)
async def update_workflow(
    request: WorkflowUpdateRequest,
    api_key: str = Depends(validate_api_key)
) -> WorkflowResponse:
    """
    Update a workflow's state or configuration.

    Args:
        request: Request to update the workflow
        api_key: Validated API key for authentication

    Returns:
        Updated workflow status
    """
    try:
        response = await workflow_service.update_workflow(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating workflow: {str(e)}")


@router.get("/list-workflows", response_model=List[WorkflowResponse])
async def list_workflows(
    api_key: str = Depends(validate_api_key)
) -> List[WorkflowResponse]:
    """
    List all active workflows.

    Args:
        api_key: Validated API key for authentication

    Returns:
        List of workflow responses
    """
    try:
        responses = await workflow_service.list_workflows()
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing workflows: {str(e)}")


@router.get("/health")
async def workflow_health_check():
    """
    Health check endpoint for workflow service.

    Returns:
        Health status of the workflow service
    """
    return {
        "status": "healthy",
        "service": "workflow-orchestration",
        "message": "Workflow orchestration service is operational"
    }


@router.delete("/cleanup-workflow/{workflow_id}")
async def cleanup_workflow(
    workflow_id: str,
    api_key: str = Depends(validate_api_key)
):
    """
    Remove a completed workflow from active workflows.

    Args:
        workflow_id: ID of the workflow to clean up
        api_key: Validated API key for authentication

    Returns:
        Success message
    """
    try:
        if workflow_id in workflow_service.active_workflows:
            del workflow_service.active_workflows[workflow_id]
            return {
                "message": f"Workflow {workflow_id} cleaned up successfully",
                "workflow_id": workflow_id
            }
        else:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cleaning up workflow: {str(e)}")