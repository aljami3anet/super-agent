from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class GDPRDeleteRequest(BaseModel):
    user_id: str
    delete_conversations: Optional[bool] = True
    delete_logs: Optional[bool] = True
    delete_memory: Optional[bool] = True

@router.delete("/gdpr/delete", summary="GDPR Delete User Data", status_code=200)
async def gdpr_delete(request: GDPRDeleteRequest = Body(...)):
    # Simulate deletion logic
    # In production, delete from DB, logs, memory, etc.
    deleted = {
        "conversations": request.delete_conversations,
        "logs": request.delete_logs,
        "memory": request.delete_memory,
    }
    # Return confirmation
    return {
        "status": "deleted",
        "user_id": request.user_id,
        "deleted": deleted,
    }