import logging
from typing import Any, AsyncGenerator, Dict, List
from uuid import UUID

from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

from app.agents.helpper import generate_instructions
from app.agents.memory import Memory
from app.schemas.user_schema import User


logger = logging.getLogger(__name__)

class LessonAgent():
    """AI tutor agent specialized in lesson delivery and educational content"""

    def __init__(self):
        self.agent = Agent(
            name="Learning Assistant",
            model="gemini-2.5-flash",
            instructions=generate_instructions,
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
        history = await self.memory.get_last_messages(conversation_id, limit=5)
        
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
            message={"role": "agent", "content": result}
        )
        
        
    
    def _build_educational_prompt(
        self,
        question: str, *,
        history: List[Dict[str, Any]],
        relevant_lessons: List[Dict],
        relevant_books: List[Dict]
    ) -> str:
        """Build context-aware educational prompt"""
        
        prompt = str(history)
        
        # Add relevant lessons context
        if relevant_lessons:
            prompt += f"\n\nRelevant Lessons:\n"
            for lesson in relevant_lessons:
                prompt += f"- {lesson.get('title', 'Untitled')}: {lesson.get('content', {}).get('summary', 'No summary available')}\n"
        
        # Add relevant books context
        if relevant_books:
            prompt += f"\n\nRelevant Book Content:\n"
            for book in relevant_books:
                prompt += f"- From '{book.get('title', 'Untitled')}': {book.get('relevant_text', '')}\n"
        
        # Add the question
        prompt += f"\n\nStudent Question: {question}\n\n"
        prompt += "Please provide a helpful, educational response that:\n"
        prompt += "1. Directly answers the question\n"
        prompt += "2. Uses the provided lesson and book context when relevant\n"
        prompt += "3. Explains concepts in simple, age-appropriate language\n"
        prompt += "4. Encourages further learning\n"
        prompt += "5. Uses the student's preferred language when helpful\n\n"
        prompt += "Response:"
        
        return prompt



    async def _stream_response(self, prompt: str, context: User) -> AsyncGenerator[str, None]:
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

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield f"I apologize, but I encountered an error while processing your question. Please try again."
        

