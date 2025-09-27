from agents import Agent
from app.agents.adaptation_agent import adaptation_agent    
from app.agents.language_agent import language_agent
from app.prompts.assesment_prompt import assessment_agent_prompt
from app.schemas.agents_output.assesment_agent_schema import AssessmentOutputSchema
 

assesment_agent = Agent(
    name="Assessment Agent",
    instructions=assessment_agent_prompt,
    model="gemini-2.5-flash",
    handoff_description="This agent generates short micro-quizzes, evaluates learner responses, "
        "updates mastery estimates, and detects misconceptions. It returns structured "
        "JSON outputs containing quiz items, correctness, mastery updates, and "
        "misconception labels for downstream agents like the Adaptation Agent "
        "and Content Curator.",
    handoffs=[adaptation_agent,language_agent],
    output_type=AssessmentOutputSchema
)


