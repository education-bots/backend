from agents import Agent

from app.agents.language_agent import language_agent
from app.agents.helpper import coach_agent_instructions
from app.prompts.content_curator_prompt import content_curator_agent_prompt
from app.schemas.agents_output.content_agent_schema import ContentCuratorOutputSchema

content_agent = Agent(
    name="English",
    instructions=content_curator_agent_prompt,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches English to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive.",
    handoffs=[language_agent],
    output_type=ContentCuratorOutputSchema
)



