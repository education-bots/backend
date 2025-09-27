from agents import Agent
from app.agents.helpper import coach_agent_instructions
from app.prompts.language_bridge_prompt import language_bridge_prompt
from app.schemas.agents_output.language_agent_schema import LanguageBridgeOutputSchema
 
language_agent = Agent(
    name="English",
    instructions=language_bridge_prompt,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches English to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive.",
    output_type=LanguageBridgeOutputSchema
)



