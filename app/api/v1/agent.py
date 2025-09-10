import logging
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.security import verify_auth_header
from app.schemas.agent_schema import AgentRequest, StreamingChunk
from app.services.agent_service import AgentService


logger = logging.getLogger(__name__)
router = APIRouter()



@router.post("/ask", response_class=StreamingResponse)
async def ask_agent(
    request: AgentRequest, 
    _: str = Depends(verify_auth_header)
) -> StreamingResponse:
    """Ask a question to an AI agent and stream the response."""
    
    try:
        agent_service = AgentService()
        
        # Stream the agent response
        async def generate_response() -> AsyncGenerator[str, None]:
            try:
                async for chunk in agent_service.process_request(request):
                    chunk_data = StreamingChunk(
                        chunk=chunk,
                        conversation_id=request.conversation_id,
                        is_final=False
                    )
                    yield chunk_data.model_dump_json()

                # Send final chunk
                final_chunk = StreamingChunk(
                    chunk="",
                    conversation_id=request.conversation_id,
                    is_final=True
                )
                yield final_chunk.model_dump_json()

            except Exception as e:
                logger.error(f"Error in streaming response: {e}")
                error_chunk = StreamingChunk(
                    chunk=f"Error: {str(e)}",
                    conversation_id=request.conversation_id,
                    is_final=True
                )
                yield error_chunk.model_dump_json()

        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error processing agent request: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing request"
        )


@router.get("/all")
async def list_agents(_: str = Depends(verify_auth_header)):
    """List available agents"""
    try:
        agent_service = AgentService()
        # agents = await agent_service.list_agents()
        return {"agents": ["lesson_agent"]}
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving agents"
        )
                

