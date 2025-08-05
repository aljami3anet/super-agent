"""
Tools API endpoints for AI Coder Agent.

This module provides API endpoints for:
- File operations
- Git operations
- Code execution
- Package management
- Testing and linting
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

from ..tools.file_operations import FileOperations
from ..tools.git_operations import GitOperations
from ..tools.code_execution import CodeExecution
from ..tools.package_management import PackageManagement
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize tool instances
file_ops = FileOperations()
git_ops = GitOperations()
code_exec = CodeExecution()
pkg_mgr = PackageManagement()


# Request/Response Models
class FileReadRequest(BaseModel):
    """Request model for file read operations."""
    file_path: str = Field(..., description="Path to the file to read")
    encoding: Optional[str] = Field(default="utf-8", description="File encoding")


class FileReadResponse(BaseModel):
    """Response model for file read operations."""
    content: str = Field(..., description="File content")
    file_path: str = Field(..., description="Path of the file")
    size: int = Field(..., description="File size in bytes")
    encoding: str = Field(..., description="File encoding used")


class FileWriteRequest(BaseModel):
    """Request model for file write operations."""
    file_path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write")
    encoding: Optional[str] = Field(default="utf-8", description="File encoding")
    append: bool = Field(default=False, description="Whether to append to existing file")


class FileWriteResponse(BaseModel):
    """Response model for file write operations."""
    file_path: str = Field(..., description="Path of the file")
    bytes_written: int = Field(..., description="Number of bytes written")
    success: bool = Field(..., description="Whether operation was successful")


class DirectoryListRequest(BaseModel):
    """Request model for directory listing."""
    directory_path: str = Field(..., description="Path to the directory")
    recursive: bool = Field(default=False, description="Whether to list recursively")


class DirectoryListResponse(BaseModel):
    """Response model for directory listing."""
    directory_path: str = Field(..., description="Path of the directory")
    items: List[Dict[str, Any]] = Field(..., description="Directory contents")
    total_items: int = Field(..., description="Total number of items")


class GitOperationRequest(BaseModel):
    """Request model for Git operations."""
    operation: str = Field(..., description="Git operation to perform")
    repository_path: str = Field(..., description="Path to the repository")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Operation parameters")


class GitOperationResponse(BaseModel):
    """Response model for Git operations."""
    operation: str = Field(..., description="Git operation performed")
    success: bool = Field(..., description="Whether operation was successful")
    output: str = Field(..., description="Command output")
    error: Optional[str] = Field(default=None, description="Error message if any")


class CodeExecutionRequest(BaseModel):
    """Request model for code execution."""
    command: str = Field(..., description="Command to execute")
    working_directory: Optional[str] = Field(default=None, description="Working directory")
    timeout: Optional[int] = Field(default=30, description="Execution timeout in seconds")


class CodeExecutionResponse(BaseModel):
    """Response model for code execution."""
    command: str = Field(..., description="Command executed")
    success: bool = Field(..., description="Whether execution was successful")
    output: str = Field(..., description="Command output")
    error: Optional[str] = Field(default=None, description="Error output")
    return_code: int = Field(..., description="Return code")
    duration: float = Field(..., description="Execution duration in seconds")


# File Operations Endpoints
@router.post("/file/read", response_model=FileReadResponse)
async def read_file(request: FileReadRequest):
    """Read a file from the filesystem."""
    try:
        result = await file_ops.read_file(
            file_path=request.file_path,
            encoding=request.encoding
        )
        
        return FileReadResponse(
            content=result["content"],
            file_path=request.file_path,
            size=result["size"],
            encoding=request.encoding
        )
        
    except Exception as e:
        logger.error(f"File read failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file/write", response_model=FileWriteResponse)
async def write_file(request: FileWriteRequest):
    """Write content to a file."""
    try:
        result = await file_ops.write_file(
            file_path=request.file_path,
            content=request.content,
            encoding=request.encoding,
            append=request.append
        )
        
        return FileWriteResponse(
            file_path=request.file_path,
            bytes_written=result["bytes_written"],
            success=result["success"]
        )
        
    except Exception as e:
        logger.error(f"File write failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file/upload")
async def upload_file(file: UploadFile = File(...), target_path: Optional[str] = None):
    """Upload a file to the filesystem."""
    try:
        if not target_path:
            target_path = f"uploads/{file.filename}"
        
        content = await file.read()
        result = await file_ops.write_file(
            file_path=target_path,
            content=content.decode("utf-8"),
            encoding="utf-8"
        )
        
        return {
            "filename": file.filename,
            "target_path": target_path,
            "size": len(content),
            "success": result["success"]
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/directory/list", response_model=DirectoryListResponse)
async def list_directory(request: DirectoryListRequest):
    """List contents of a directory."""
    try:
        result = await file_ops.list_directory(
            directory_path=request.directory_path,
            recursive=request.recursive
        )
        
        return DirectoryListResponse(
            directory_path=request.directory_path,
            items=result["items"],
            total_items=len(result["items"])
        )
        
    except Exception as e:
        logger.error(f"Directory listing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/directory/create")
async def create_directory(directory_path: str):
    """Create a directory."""
    try:
        result = await file_ops.create_directory(directory_path)
        return {
            "directory_path": directory_path,
            "success": result["success"],
            "message": result.get("message", "")
        }
        
    except Exception as e:
        logger.error(f"Directory creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/file/delete")
async def delete_file(file_path: str):
    """Delete a file or directory."""
    try:
        result = await file_ops.delete_path(file_path)
        return {
            "file_path": file_path,
            "success": result["success"],
            "message": result.get("message", "")
        }
        
    except Exception as e:
        logger.error(f"File deletion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Git Operations Endpoints
@router.post("/git/operation", response_model=GitOperationResponse)
async def git_operation(request: GitOperationRequest):
    """Perform a Git operation."""
    try:
        result = await git_ops.execute_git_operation(
            operation=request.operation,
            repository_path=request.repository_path,
            parameters=request.parameters
        )
        
        return GitOperationResponse(
            operation=request.operation,
            success=result["success"],
            output=result["output"],
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Git operation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/git/commit")
async def git_commit(repository_path: str, message: str, files: Optional[List[str]] = None):
    """Commit changes to Git repository."""
    try:
        result = await git_ops.commit_changes(
            repository_path=repository_path,
            message=message,
            files=files
        )
        
        return {
            "repository_path": repository_path,
            "commit_hash": result.get("commit_hash"),
            "success": result["success"],
            "message": result.get("message", "")
        }
        
    except Exception as e:
        logger.error(f"Git commit failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/git/branch")
async def git_branch(repository_path: str, branch_name: str, operation: str = "create"):
    """Manage Git branches."""
    try:
        if operation == "create":
            result = await git_ops.create_branch(repository_path, branch_name)
        elif operation == "switch":
            result = await git_ops.switch_branch(repository_path, branch_name)
        elif operation == "delete":
            result = await git_ops.delete_branch(repository_path, branch_name)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {operation}")
        
        return {
            "repository_path": repository_path,
            "branch_name": branch_name,
            "operation": operation,
            "success": result["success"],
            "message": result.get("message", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Git branch operation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Code Execution Endpoints
@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """Execute a command."""
    try:
        result = await code_exec.execute_command(
            command=request.command,
            working_directory=request.working_directory,
            timeout=request.timeout
        )
        
        return CodeExecutionResponse(
            command=request.command,
            success=result["success"],
            output=result["output"],
            error=result.get("error"),
            return_code=result["return_code"],
            duration=result["duration"]
        )
        
    except Exception as e:
        logger.error(f"Code execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute/shell")
async def execute_shell_script(script_content: str, working_directory: Optional[str] = None):
    """Execute a shell script."""
    try:
        result = await code_exec.execute_shell_script(
            script_content=script_content,
            working_directory=working_directory
        )
        
        return {
            "success": result["success"],
            "output": result["output"],
            "error": result.get("error"),
            "return_code": result["return_code"],
            "duration": result["duration"]
        }
        
    except Exception as e:
        logger.error(f"Shell script execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Package Management Endpoints
@router.post("/package/install")
async def install_package(package_name: str, package_manager: str = "pip"):
    """Install a package."""
    try:
        result = await pkg_mgr.install_package(
            package_name=package_name,
            package_manager=package_manager
        )
        
        return {
            "package_name": package_name,
            "package_manager": package_manager,
            "success": result["success"],
            "output": result["output"],
            "error": result.get("error")
        }
        
    except Exception as e:
        logger.error(f"Package installation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/package/uninstall")
async def uninstall_package(package_name: str, package_manager: str = "pip"):
    """Uninstall a package."""
    try:
        result = await pkg_mgr.uninstall_package(
            package_name=package_name,
            package_manager=package_manager
        )
        
        return {
            "package_name": package_name,
            "package_manager": package_manager,
            "success": result["success"],
            "output": result["output"],
            "error": result.get("error")
        }
        
    except Exception as e:
        logger.error(f"Package uninstallation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Testing and Linting Endpoints
@router.post("/test/run")
async def run_tests(test_path: str, test_framework: str = "pytest"):
    """Run tests."""
    try:
        result = await code_exec.run_tests(
            test_path=test_path,
            test_framework=test_framework
        )
        
        return {
            "test_path": test_path,
            "test_framework": test_framework,
            "success": result["success"],
            "output": result["output"],
            "error": result.get("error"),
            "test_results": result.get("test_results", {})
        }
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/lint/run")
async def run_linter(file_path: str, linter: str = "ruff"):
    """Run a linter on a file."""
    try:
        result = await code_exec.run_linter(
            file_path=file_path,
            linter=linter
        )
        
        return {
            "file_path": file_path,
            "linter": linter,
            "success": result["success"],
            "output": result["output"],
            "error": result.get("error"),
            "issues": result.get("issues", [])
        }
        
    except Exception as e:
        logger.error(f"Linting failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools/available")
async def get_available_tools():
    """Get list of available tools."""
    return {
        "file_operations": [
            "read_file",
            "write_file", 
            "upload_file",
            "list_directory",
            "create_directory",
            "delete_file"
        ],
        "git_operations": [
            "git_operation",
            "commit",
            "branch"
        ],
        "code_execution": [
            "execute",
            "execute_shell"
        ],
        "package_management": [
            "install_package",
            "uninstall_package"
        ],
        "testing_linting": [
            "run_tests",
            "run_linter"
        ]
    }