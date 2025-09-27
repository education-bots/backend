from typing import Optional
from agents import Agent, GuardrailFunctionOutput, Runner, input_guardrail
from pydantic import BaseModel

from app.prompts.safety_policy_prompt import safety_policy_agent_prompt
from app.schemas.agents_output.guardrails_schema import SafetyPolicyOutput


class InputGuardrailOutputType(BaseModel):
    is_related_to_study: bool
    reasoning: str
    subject: str
    response: Optional[str]
    safety_policy: SafetyPolicyOutput


input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    model="gemini-2.0-flash",
    instructions=safety_policy_agent_prompt,
    output_type=InputGuardrailOutputType
)



@input_guardrail
async def input_guardrails(context, agent, input):

    result = await Runner.run(input_guardrail_agent, input)
    final_output = result.final_output_as(InputGuardrailOutputType)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_related_to_study
    )
    











        