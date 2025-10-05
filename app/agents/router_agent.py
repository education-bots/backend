import logging
from typing import AsyncGenerator, Dict, List
from uuid import UUID
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, InputGuardrailTripwireTriggered, Runner, TResponseInputItem
from app.agents.adaptation_agent import adaptation_agent
from app.agents.assessment_agent import assesment_agent
from app.agents.content_agent import content_agent
from app.agents.guardrails import input_guardrails
from app.agents.helpper import generate_instructions
from app.agents.memory import Memory
from app.schemas.agent_schema import Message
from app.schemas.user_schema import User

logger = logging.getLogger(__name__)

class OrchestratorAgent():
    """AI tutor agent specialized in lesson delivery and educational content"""

    def __init__(self):
        self.agent = Agent(
            name="Learning Assistant",
            model="gemini-2.5-flash",
            instructions=generate_instructions,
            input_guardrails=[input_guardrails],
            handoffs=[assesment_agent, adaptation_agent, content_agent],
        )
        self.memory = Memory()


    async def generate_response(
        self,
        question: str,
        context: User,
        conversation_id: UUID,
        user_id: UUID
    ) -> AsyncGenerator[str, None]:
        """Generate educational response with context from lessons and books"""
        
        # Get last conversation history
        history = await self.memory.get_last_messages(conversation_id, limit=10)
        
        await self.memory.add_message(
            conversation_id,
            user_id, 
            message={"role": "user", "content": question}
        )
        
        # Build context-aware prompt
        prompt = self._build_educational_prompt(
            question, 
            history=history,
            relevant_books=[],
            relevant_lessons=[]
        )
        
        result = ''
        # Generate streaming response
        async for chunk in self._stream_response(prompt, context):
            result += chunk
            yield chunk
        
        await self.memory.add_message(
            conversation_id,
            user_id, 
            message={"role": "assistant", "content": result}
        )
        
        
    def _build_educational_prompt(
        self,
        question: str, *,
        history: List[Message],
        relevant_lessons: List[Dict],
        relevant_books: List[Dict]
    ) -> List[TResponseInputItem]:
        """Build context-aware educational prompt"""
        
        current_prompt = str(history)
        
        # Add relevant lessons context
        if relevant_lessons:
            current_prompt += f"\n\nRelevant Lessons:\n"
            for lesson in relevant_lessons:
                current_prompt += f"- {lesson.get('title', 'Untitled')}: {lesson.get('content', {}).get('summary', 'No summary available')}\n"
        
        # Add relevant books context
        if relevant_books:
            current_prompt += f"\n\nRelevant Book Content:\n"
            for book in relevant_books:
                current_prompt += f"- From '{book.get('title', 'Untitled')}': {book.get('relevant_text', '')}\n"
        
        # Add the question
        current_prompt += f"\n\nStudent Question: {question}\n\n"
        current_prompt += "Please provide a helpful, educational response that:\n"
        current_prompt += "1. Directly answers the question\n"
        current_prompt += "2. Uses the provided lesson and book context when relevant\n"
        current_prompt += "3. Explains concepts in simple, age-appropriate language\n"
        current_prompt += "4. Encourages further learning\n"
        current_prompt += "5. Uses the student's preferred language when helpful\n\n"
        current_prompt += "Response:"
        
        agent_input: List[TResponseInputItem] = history + [{"role": 'user', "content": current_prompt}]
        return agent_input

    async def _stream_response(self, prompt: List[TResponseInputItem], context: User) -> AsyncGenerator[str, None]:
        """Stream response from Gemini model"""

        try:
            result = Runner.run_streamed(
                starting_agent=self.agent,
                input=prompt,
                context=context
            )
            
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    text = event.data.delta
                    print(text)
                    yield text
        
        except InputGuardrailTripwireTriggered as e:
            logger.error(f"Input guardrail tripwire triggered: {e.guardrail_result.output.output_info.reasoning}")
            yield f"I apologize, but I could not proccess you request.\n{e.guardrail_result.output.output_info.response}."

        except Exception as e:
            logger.error(f"Error generating response: {e}\nError class name: {e.__class__.__name__}")
            yield f"I apologize, but I encountered an error while processing your question. Please try again."
        

