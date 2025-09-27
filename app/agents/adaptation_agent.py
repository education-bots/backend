from agents import Agent
from app.agents.language_agent import language_agent
from app.agents.content_agent import content_agent
from app.prompts.adaptation_prompt import adaptation_agent_prompt
from app.schemas.agents_output.adaptation_agent_schema import AdaptationOutputSchema

adaptation_agent = Agent(
    name="Adaptation Agent",
    instructions=adaptation_agent_prompt,
    model="gemini-2.5-flash",
    handoff_description="This agent adapts the learner's pathway based on assessment results and mastery profiles, deciding whether to remediate, practice more, or advance.",
    handoffs=[content_agent,language_agent],
    output_type=AdaptationOutputSchema
)



