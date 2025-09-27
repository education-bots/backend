from agents import Agent

from app.agents.language_agent import language_agent
from app.agents.helpper import coach_agent_instructions


assesment_agent = Agent(
    name="English",
    instructions=coach_agent_instructions,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches English to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive.",
    handoffs=[language_agent]
)


