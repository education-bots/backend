import logging
from typing import AsyncGenerator

from app.agents.router_agent import OrchestratorAgent
from app.schemas.agent_schema import AgentRequest


logger = logging.getLogger(__name__)


class AgentService:
    """Service orchestrator for agent interactions"""
    
    def __init__(self):
        # self.guardrails = Guardrails()
        self.agents = {}  # Cache for agent instances
        self.lesson_agent = None
        self._initialize_agents()
        
    
    def _initialize_agents(self):
        """Initialize available agents"""
        self.lesson_agent = OrchestratorAgent()
        # self.agents["lesson-agent"] = lesson_agent

    async def process_request(self, request: AgentRequest) -> AsyncGenerator[str, None]:
        """Process agent request through the complete pipeline"""

        try:
            # Step 1: Get agent
            if not self.lesson_agent:
                yield "I'm sorry, but I couldn't find the requested learning assistant. Please try again."
                return

            # Step 2: Generate response
            response_chunks = []
            async for chunk in self.lesson_agent.generate_response(
                request.question,
                context=request.user,
                conversation_id=request.conversation_id,
                user_id=request.user_id
            ):
                response_chunks.append(chunk)
                yield chunk
            
    
            # Step 6: Store agent response in memory
        
        except Exception as e:
            logger.error(f"Error processing agent request: {e}")
            yield "I apologize, but I encountered an error while processing your question. Please try again."

        
        









