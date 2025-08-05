"""
Conversations API endpoints for AI Coder Agent.

This module provides API endpoints for:
- Conversation management
- Summary generation
- Memory operations
- Conversation history
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.conversation import ConversationService
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize conversation service
conversation_service = ConversationService()


# Request/Response Models
class ConversationCreateRequest(BaseModel):
    """Request model for creating a conversation."""
    title: str = Field(..., description="Conversation title")
    description: Optional[str] = Field(default=None, description="Conversation description")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Initial context")


class ConversationResponse(BaseModel):
    """Response model for conversation operations."""
    conversation_id: str = Field(..., description="Unique conversation ID")
    title: str = Field(..., description="Conversation title")
    description: Optional[str] = Field(default=None, description="Conversation description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    message_count: int = Field(..., description="Number of messages")
    summary: Optional[str] = Field(default=None, description="Conversation summary")


class MessageRequest(BaseModel):
    """Request model for adding a message."""
    conversation_id: str = Field(..., description="Conversation ID")
    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role (user/assistant)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Message metadata")


class MessageResponse(BaseModel):
    """Response model for message operations."""
    message_id: str = Field(..., description="Unique message ID")
    conversation_id: str = Field(..., description="Conversation ID")
    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role")
    timestamp: datetime = Field(..., description="Message timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Message metadata")


class SummaryRequest(BaseModel):
    """Request model for generating a summary."""
    conversation_id: str = Field(..., description="Conversation ID")
    max_length: Optional[int] = Field(default=None, description="Maximum summary length")
    compression_ratio: Optional[float] = Field(default=None, description="Compression ratio")


class SummaryResponse(BaseModel):
    """Response model for summary operations."""
    conversation_id: str = Field(..., description="Conversation ID")
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(..., description="Original conversation length")
    summary_length: int = Field(..., description="Summary length")
    compression_ratio: float = Field(..., description="Compression ratio")
    generated_at: datetime = Field(..., description="Summary generation timestamp")


# Conversation Management Endpoints
@router.post("/create", response_model=ConversationResponse)
async def create_conversation(request: ConversationCreateRequest):
    """Create a new conversation."""
    try:
        conversation = await conversation_service.create_conversation(
            title=request.title,
            description=request.description,
            context=request.context
        )
        
        return ConversationResponse(
            conversation_id=conversation["conversation_id"],
            title=conversation["title"],
            description=conversation["description"],
            created_at=conversation["created_at"],
            updated_at=conversation["updated_at"],
            message_count=conversation["message_count"],
            summary=conversation.get("summary")
        )
        
    except Exception as e:
        logger.error(f"Failed to create conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=List[ConversationResponse])
async def list_conversations(
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    include_summaries: bool = False
):
    """List all conversations."""
    try:
        conversations = await conversation_service.list_conversations(
            limit=limit,
            offset=offset,
            include_summaries=include_summaries
        )
        
        return [
            ConversationResponse(
                conversation_id=conv["conversation_id"],
                title=conv["title"],
                description=conv["description"],
                created_at=conv["created_at"],
                updated_at=conv["updated_at"],
                message_count=conv["message_count"],
                summary=conv.get("summary")
            )
            for conv in conversations
        ]
        
    except Exception as e:
        logger.error(f"Failed to list conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    """Get a specific conversation."""
    try:
        conversation = await conversation_service.get_conversation(conversation_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return ConversationResponse(
            conversation_id=conversation["conversation_id"],
            title=conversation["title"],
            description=conversation["description"],
            created_at=conversation["created_at"],
            updated_at=conversation["updated_at"],
            message_count=conversation["message_count"],
            summary=conversation.get("summary")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    try:
        success = await conversation_service.delete_conversation(conversation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": f"Conversation {conversation_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Message Management Endpoints
@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def add_message(conversation_id: str, request: MessageRequest):
    """Add a message to a conversation."""
    try:
        message = await conversation_service.add_message(
            conversation_id=conversation_id,
            content=request.content,
            role=request.role,
            metadata=request.metadata
        )
        
        return MessageResponse(
            message_id=message["message_id"],
            conversation_id=message["conversation_id"],
            content=message["content"],
            role=message["role"],
            timestamp=message["timestamp"],
            metadata=message.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Failed to add message to conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: str,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0
):
    """Get messages from a conversation."""
    try:
        messages = await conversation_service.get_messages(
            conversation_id=conversation_id,
            limit=limit,
            offset=offset
        )
        
        return [
            MessageResponse(
                message_id=msg["message_id"],
                conversation_id=msg["conversation_id"],
                content=msg["content"],
                role=msg["role"],
                timestamp=msg["timestamp"],
                metadata=msg.get("metadata")
            )
            for msg in messages
        ]
        
    except Exception as e:
        logger.error(f"Failed to get messages from conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Summary Management Endpoints
@router.post("/{conversation_id}/summary", response_model=SummaryResponse)
async def generate_summary(conversation_id: str, request: SummaryRequest):
    """Generate a summary for a conversation."""
    try:
        summary = await conversation_service.generate_summary(
            conversation_id=conversation_id,
            max_length=request.max_length or settings.SUMMARY_MAX_SIZE,
            compression_ratio=request.compression_ratio or settings.SUMMARY_COMPRESSION_RATIO
        )
        
        return SummaryResponse(
            conversation_id=summary["conversation_id"],
            summary=summary["summary"],
            original_length=summary["original_length"],
            summary_length=summary["summary_length"],
            compression_ratio=summary["compression_ratio"],
            generated_at=summary["generated_at"]
        )
        
    except Exception as e:
        logger.error(f"Failed to generate summary for conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}/summary", response_model=SummaryResponse)
async def get_summary(conversation_id: str):
    """Get the summary for a conversation."""
    try:
        summary = await conversation_service.get_summary(conversation_id)
        
        if not summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        return SummaryResponse(
            conversation_id=summary["conversation_id"],
            summary=summary["summary"],
            original_length=summary["original_length"],
            summary_length=summary["summary_length"],
            compression_ratio=summary["compression_ratio"],
            generated_at=summary["generated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get summary for conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Memory Management Endpoints
@router.get("/memory/status")
async def get_memory_status():
    """Get memory usage status."""
    try:
        status = await conversation_service.get_memory_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get memory status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/cleanup")
async def cleanup_memory():
    """Clean up old conversations and summaries."""
    try:
        result = await conversation_service.cleanup_memory()
        return {
            "message": "Memory cleanup completed",
            "deleted_conversations": result.get("deleted_conversations", 0),
            "deleted_summaries": result.get("deleted_summaries", 0),
            "freed_space": result.get("freed_space", 0)
        }
    except Exception as e:
        logger.error(f"Failed to cleanup memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory/export")
async def export_memory():
    """Export all conversations and summaries."""
    try:
        export_data = await conversation_service.export_memory()
        return {
            "export_timestamp": datetime.utcnow(),
            "conversations_count": len(export_data["conversations"]),
            "summaries_count": len(export_data["summaries"]),
            "data": export_data
        }
    except Exception as e:
        logger.error(f"Failed to export memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/import")
async def import_memory(export_data: Dict[str, Any]):
    """Import conversations and summaries."""
    try:
        result = await conversation_service.import_memory(export_data)
        return {
            "message": "Memory import completed",
            "imported_conversations": result.get("imported_conversations", 0),
            "imported_summaries": result.get("imported_summaries", 0)
        }
    except Exception as e:
        logger.error(f"Failed to import memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))