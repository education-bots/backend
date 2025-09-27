from agents import Agent

from app.agents.helpper import coach_agent_instructions

language_agent = Agent(
    name="English",
    instructions=coach_agent_instructions,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches English to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive."
)



