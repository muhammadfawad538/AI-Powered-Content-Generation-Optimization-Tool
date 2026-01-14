"""
Workflow Data Models

This module defines Pydantic models for workflow management,
state tracking, and orchestration of content generation and optimization processes.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Any, Literal
from enum import Enum
from .content_generation import ContentDraft


class WorkflowStatusEnum(str, Enum):
    """Enumeration of possible workflow statuses."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class WorkflowStepStatusEnum(str, Enum):
    """Enumeration of possible workflow step statuses."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStep(BaseModel):
    """Represents a single step in a workflow."""

    step_id: str = Field(..., description="Unique identifier for the step")
    step_type: Literal[
        "content_generation",
        "seo_analysis",
        "quality_review",
        "ethics_check",
        "research",
        "export",
        "custom"
    ] = Field(..., description="Type of operation this step performs")
    description: str = Field(..., description="Brief description of the step")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input parameters for the step")
    output_data: Optional[Dict[str, Any]] = Field(default=None, description="Output results from the step")
    status: WorkflowStepStatusEnum = Field(default=WorkflowStepStatusEnum.PENDING, description="Current status of the step")
    error_message: Optional[str] = Field(default=None, description="Error message if step failed")
    start_time: Optional[datetime] = Field(default=None, description="When the step started execution")
    end_time: Optional[datetime] = Field(default=None, description="When the step completed execution")
    duration: Optional[float] = Field(default=None, description="Duration of execution in seconds")


class WorkflowHistoryItem(BaseModel):
    """Represents a historical record of workflow execution."""

    workflow_id: str = Field(..., description="ID of the workflow")
    step_id: str = Field(..., description="ID of the step")
    status: WorkflowStepStatusEnum = Field(..., description="Status of the step")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the status changed")
    message: Optional[str] = Field(default=None, description="Additional information about the status change")


class WorkflowRequest(BaseModel):
    """Request to create and execute a workflow."""

    workflow_name: str = Field(..., description="Name/identifier for the workflow")
    description: Optional[str] = Field(default=None, description="Description of the workflow")
    steps: List[WorkflowStep] = Field(..., description="Ordered list of steps to execute")
    parallel_execution: bool = Field(default=False, description="Whether to allow parallel execution of compatible steps")
    callback_url: Optional[str] = Field(default=None, description="URL to notify when workflow completes")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata for the workflow")


class WorkflowResponse(BaseModel):
    """Response containing workflow execution information."""

    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    workflow_name: str = Field(..., description="Name of the workflow")
    status: WorkflowStatusEnum = Field(..., description="Current status of the workflow")
    current_step: Optional[str] = Field(default=None, description="ID of the currently executing step")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress percentage (0-100)")
    total_steps: int = Field(..., description="Total number of steps in the workflow")
    completed_steps: int = Field(..., description="Number of completed steps")
    steps: List[WorkflowStep] = Field(..., description="Current state of all steps")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Final result of the workflow")
    error_message: Optional[str] = Field(default=None, description="Error message if workflow failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the workflow was created")
    started_at: Optional[datetime] = Field(default=None, description="When the workflow started execution")
    completed_at: Optional[datetime] = Field(default=None, description="When the workflow completed execution")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata for the workflow")


class WorkflowUpdateRequest(BaseModel):
    """Request to update workflow state or configuration."""

    workflow_id: str = Field(..., description="ID of the workflow to update")
    action: Literal["pause", "resume", "cancel", "rerun"] = Field(..., description="Action to perform on the workflow")
    step_id: Optional[str] = Field(default=None, description="Specific step ID if action applies to a particular step")


class WorkflowState(BaseModel):
    """Complete state representation of a workflow for persistence."""

    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    workflow_name: str = Field(..., description="Name of the workflow")
    status: WorkflowStatusEnum = Field(..., description="Current status of the workflow")
    steps: List[WorkflowStep] = Field(..., description="State of all steps")
    current_step_index: Optional[int] = Field(default=None, description="Index of currently executing step")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress percentage (0-100)")
    history: List[WorkflowHistoryItem] = Field(default_factory=list, description="Execution history")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Final result of the workflow")
    error_message: Optional[str] = Field(default=None, description="Error message if workflow failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the workflow was created")
    started_at: Optional[datetime] = Field(default=None, description="When the workflow started execution")
    completed_at: Optional[datetime] = Field(default=None, description="When the workflow completed execution")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata for the workflow")


class WorkflowStatistics(BaseModel):
    """Statistics about workflow execution."""

    total_workflows: int = Field(..., description="Total number of workflows")
    active_workflows: int = Field(..., description="Number of workflows currently running")
    completed_workflows: int = Field(..., description="Number of completed workflows")
    failed_workflows: int = Field(..., description="Number of failed workflows")
    average_duration: Optional[float] = Field(default=None, description="Average duration in seconds")
    success_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Success rate percentage (0-100)")