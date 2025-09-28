from agents import Agent, function_tool
from app.db.connection import get_supabase, get_supabase_embedding_model
from app.agents.adaptation_agent import adaptation_agent
from app.agents.language_agent import language_agent
from app.prompts.content_curator_prompt import content_curator_agent_prompt
from app.schemas.agents_output.content_agent_schema import ContentCuratorOutputSchema
from typing import List, Dict

@function_tool
def retrieve_curriculum_chunks(query: str, match_threshold: float = 0.8, top_k: int = 5) -> List[Dict]:
    """
    Retrieve curriculum-aligned passages from pre-indexed PDFs stored in Supabase.
    Args:
        query: The learner’s request or topic (string).
        match_threshold: Similarity threshold for matches (default 0.8).
        top_k: Max number of passages to return (default 5).
    Returns:
        A list of dicts containing matched passages with their source citations.
    """
    client = get_supabase()
    model = get_supabase_embedding_model()

    # Convert query to embeddings
    embeddings = model.encode(query)

    # Query Supabase RPC
    response = client.rpc("match_book_chunks", {
        "embedding": embeddings.tolist(),
        "match_threshold": match_threshold
    }).select("content, metadata").limit(top_k).execute()

    if response.data:
        return response.data
    else:
        return [{"content": "No curriculum content found", "metadata": {}}]


content_agent = Agent(
    name="Content Agent",
    instructions=content_curator_agent_prompt,
    model="gemini-2.5-flash",
    handoff_description=(
        "This agent retrieves short, curriculum-aligned passages and practice items "
        "from a pre-indexed set of PDFs. It ensures all content is strictly within the "
        "curriculum scope, leveled (easy, medium, hard), and appropriate to the learner’s "
        "grade and reading level. The agent outputs valid JSON containing both passages "
        "and practice items (2–3 questions/exercises), with source citations (PDF name, page). "
        "Downstream agents like the Language Bridge and Adaptation Agent consume this output "
        "to deliver learning content and adjust the learner’s pathway."
    ),
    handoffs=[language_agent, adaptation_agent],
    tools=[retrieve_curriculum_chunks],   # ✅ Added tool here
    output_type=ContentCuratorOutputSchema
)

