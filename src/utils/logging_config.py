"""
Logging Configuration Utility

This module provides centralized logging configuration for all services,
including research, export, and workflow orchestration features.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(
    service_name: str = "app",
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up logging for a service with both console and file output options.

    Args:
        service_name: Name of the service for log identification
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )

    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler if path provided
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def log_api_call(
    logger: logging.Logger,
    endpoint: str,
    method: str,
    user_id: Optional[str] = None,
    request_data: Optional[dict] = None,
    response_status: Optional[int] = None,
    duration_ms: Optional[float] = None
):
    """
    Log API call information.

    Args:
        logger: Logger instance
        endpoint: API endpoint
        method: HTTP method
        user_id: User identifier
        request_data: Request payload
        response_status: HTTP response status
        duration_ms: Request duration in milliseconds
    """
    log_msg = f"API Call: {method} {endpoint}"
    if user_id:
        log_msg += f" by user {user_id}"
    if response_status:
        log_msg += f" -> {response_status}"
    if duration_ms:
        log_msg += f" ({duration_ms:.2f}ms)"

    logger.info(log_msg)

    # Log request data if provided and not sensitive
    if request_data:
        safe_data = _sanitize_log_data(request_data)
        logger.debug(f"Request data: {safe_data}")


def log_workflow_event(
    logger: logging.Logger,
    workflow_id: str,
    event_type: str,
    step_id: Optional[str] = None,
    status: Optional[str] = None,
    message: Optional[str] = None
):
    """
    Log workflow-related events.

    Args:
        logger: Logger instance
        workflow_id: Workflow identifier
        event_type: Type of event
        step_id: Step identifier
        status: Event status
        message: Additional message
    """
    log_msg = f"Workflow {workflow_id} - {event_type}"
    if step_id:
        log_msg += f" (Step: {step_id})"
    if status:
        log_msg += f" -> {status}"
    if message:
        log_msg += f": {message}"

    logger.info(log_msg)


def log_export_operation(
    logger: logging.Logger,
    export_id: str,
    content_id: str,
    platform: str,
    format_type: str,
    status: str,
    duration_ms: Optional[float] = None
):
    """
    Log export operation details.

    Args:
        logger: Logger instance
        export_id: Export operation identifier
        content_id: Content identifier
        platform: Target platform
        format_type: Export format
        status: Operation status
        duration_ms: Duration in milliseconds
    """
    log_msg = f"Export {export_id} for content {content_id} to {platform} as {format_type}: {status}"
    if duration_ms:
        log_msg += f" ({duration_ms:.2f}ms)"

    logger.info(log_msg)


def log_research_operation(
    logger: logging.Logger,
    query_id: str,
    query_text: str,
    num_results: int,
    duration_ms: float,
    status: str
):
    """
    Log research operation details.

    Args:
        logger: Logger instance
        query_id: Research query identifier
        query_text: Original query text
        num_results: Number of results returned
        duration_ms: Duration in milliseconds
        status: Operation status
    """
    log_msg = f"Research query '{query_text[:50]}...' ({query_id}) returned {num_results} results in {duration_ms:.2f}ms: {status}"
    logger.info(log_msg)


def _sanitize_log_data(data: dict) -> dict:
    """
    Sanitize sensitive data from logs.

    Args:
        data: Dictionary containing potentially sensitive data

    Returns:
        Sanitized dictionary
    """
    sanitized = {}
    sensitive_keys = {
        'password', 'secret', 'token', 'key', 'auth', 'credential',
        'api_key', 'access_token', 'refresh_token', 'client_secret'
    }

    for key, value in data.items():
        if key.lower() in sensitive_keys:
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = _sanitize_log_data(value)
        else:
            sanitized[key] = value

    return sanitized


# Pre-configured loggers for different services
research_logger = setup_logging("research-service", "INFO", "logs/research.log")
export_logger = setup_logging("export-service", "INFO", "logs/export.log")
workflow_logger = setup_logging("workflow-service", "INFO", "logs/workflow.log")
api_logger = setup_logging("api-service", "INFO", "logs/api.log")