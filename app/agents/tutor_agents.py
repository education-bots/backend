from agents import Agent

from app.agents.helpper import coach_agent_instructions


english_agent = Agent(
    name="English",
    instructions=coach_agent_instructions,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches English to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive."
)

urdu_agent = Agent(
    name="Urdu",
    instructions=coach_agent_instructions,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches Urdu to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive."
)

maths_agent = Agent(
    name="Maths",
    instructions=coach_agent_instructions,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches Maths to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive."
)


science_agent = Agent(
    name="Science",
    instructions=coach_agent_instructions,
    model="gemini-2.5-flash",
    handoff_description="This agent teaches Science to children (ages 4-12) using simple words, games, questions, and positive feedback to make learning fun and interactive."
)











