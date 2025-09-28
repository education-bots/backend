from typing import Literal, Optional, Dict, Any, TypedDict
from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.user_schema import User


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str

class AgentRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user asking the question")
    conversation_id: str = Field(..., description="UUID of the conversation")
    question: str = Field(..., min_length=1, max_length=2000, description="User's question")
    user: User = Field(..., description="User's context")


class AgentResponse(BaseModel):
    answer: str = Field(..., description="Agent's response")
    conversation_id: UUID = Field(..., description="UUID of the conversation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional response metadata")


class StreamingChunk(BaseModel):
    chunk: str = Field(..., description="Streaming response chunk")
    conversation_id: UUID = Field(..., description="UUID of the conversation")
    is_final: bool = Field(False, description="Whether this is the final chunk")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    status_code: int = Field(..., description="HTTP status code")

