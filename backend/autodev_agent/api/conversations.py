"""
Conversations API endpoints.

This module provides API endpoints for managing conversations
with the AI agents.
"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..services.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class Conversation(BaseModel):
    """Conversation model."""
    id: str
    user_id: str
    title: str
    messages: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    summary: Optional[str] = None


class ConversationListResponse(BaseModel):
    """Response model for listing conversations."""
    conversations: List[Conversation]
    total: int
    page: int
    page_size: int


class ConversationCreateRequest(BaseModel):
    """Request model for creating a conversation."""
    user_id: str
    title: str


class ConversationUpdateRequest(BaseModel):
    """Request model for updating a conversation."""
    title: Optional[str] = None
    summary: Optional[str] = None


class Message(BaseModel):
    """Message model."""
    role: str
    content: str
    timestamp: str


class MessageAddRequest(BaseModel):
    """Request model for adding a message to a conversation."""
    message: Message


# In-memory storage for conversations (in a real app, this would be a database)
conversations_db = {}
conversation_counter = 0


@router.get("/", response_model=ConversationListResponse)
async def list_conversations(
    user_id: str,
    page: int = 1,
    page_size: int = 10,
):
    """List conversations for a user."""
    # Filter conversations by user_id
    user_conversations = [
        conv for conv in conversations_db.values() if conv.user_id == user_id
    ]
    
    # Sort by updated_at (newest first)
    user_conversations.sort(key=lambda x: x.updated_at, reverse=True)
    
    # Paginate
    start = (page - 1) * page_size
    end = start + page_size
    paginated_conversations = user_conversations[start:end]
    
    return {
        "conversations": paginated_conversations,
        "total": len(user_conversations),
        "page": page,
        "page_size": page_size,
    }


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation."""
    if conversation_id not in conversations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation '{conversation_id}' not found",
        )
    
    return conversations_db[conversation_id]


@router.post("/", response_model=Conversation)
async def create_conversation(request: ConversationCreateRequest):
    """Create a new conversation."""
    global conversation_counter
    conversation_counter += 1
    
    conversation_id = str(conversation_counter)
    
    conversation = Conversation(
        id=conversation_id,
        user_id=request.user_id,
        title=request.title,
        messages=[],
        created_at="2023-01-01T00:00:00Z",  # In a real app, use current time
        updated_at="2023-01-01T00:00:00Z",  # In a real app, use current time
    )
    
    conversations_db[conversation_id] = conversation
    
    logger.info(f"Created conversation {conversation_id} for user {request.user_id}")
    
    return conversation


@router.put("/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str,
    request: ConversationUpdateRequest,
):
    """Update a conversation."""
    if conversation_id not in conversations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation '{conversation_id}' not found",
        )
    
    conversation = conversations_db[conversation_id]
    
    if request.title is not None:
        conversation.title = request.title
    
    if request.summary is not None:
        conversation.summary = request.summary
    
    # In a real app, update the updated_at timestamp
    conversation.updated_at = "2023-01-01T00:00:00Z"
    
    logger.info(f"Updated conversation {conversation_id}")
    
    return conversation


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if conversation_id not in conversations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation '{conversation_id}' not found",
        )
    
    del conversations_db[conversation_id]
    
    logger.info(f"Deleted conversation {conversation_id}")
    
    return {"status": "deleted"}


@router.post("/{conversation_id}/messages", response_model=Conversation)
async def add_message(
    conversation_id: str,
    request: MessageAddRequest,
):
    """Add a message to a conversation."""
    if conversation_id not in conversations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation '{conversation_id}' not found",
        )
    
    conversation = conversations_db[conversation_id]
    conversation.messages.append(request.message.dict())
    
    # In a real app, update the updated_at timestamp
    conversation.updated_at = "2023-01-01T00:00:00Z"
    
    logger.info(f"Added message to conversation {conversation_id}")
    
    return conversation