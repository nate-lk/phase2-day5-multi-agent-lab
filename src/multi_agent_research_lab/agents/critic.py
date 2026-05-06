"""Optional critic agent skeleton for bonus work."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings."""

        if not state.final_answer:
            state.errors.append("Critic called without a final answer to review.")
            return state

        system_prompt = (
            "You are a meticulous fact-checker and editor. "
            "Your task is to review the final answer against the research notes. "
            "Check for hallucinations, citation accuracy, and clarity. "
            "If the answer is high quality, start your response with 'Approved'. "
            "Otherwise, provide specific points for improvement."
        )
        user_prompt = (
            f"Research Notes:\n{state.research_notes}\n\n"
            f"Final Answer:\n{state.final_answer}\n\n"
            "Review:"
        )

        response = self.llm_client.complete(system_prompt, user_prompt)

        state.agent_results.append(
            AgentResult(agent=AgentName.CRITIC, content=response.content)
        )
        
        # Add feedback to errors if not approved
        if "approved" not in response.content.lower()[:20]:
            state.errors.append(f"Critic feedback: {response.content}")

        return state
