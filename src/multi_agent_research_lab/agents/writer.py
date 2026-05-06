"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""

        if not state.research_notes or not state.analysis_notes:
            state.errors.append("Writer called without sufficient research or analysis.")
            return state

        system_prompt = (
            f"You are a professional writer. "
            f"Your task is to synthesize a clear, comprehensive response for a {state.request.audience} audience. "
            "Use the provided research and analysis to draft a final answer with proper flow and clarity."
        )
        user_prompt = (
            f"Research Notes:\n{state.research_notes}\n\n"
            f"Analysis Notes:\n{state.analysis_notes}\n\n"
            "Final Answer:"
        )

        response = self.llm_client.complete(system_prompt, user_prompt)

        state.final_answer = response.content
        state.agent_results.append(
            AgentResult(agent=AgentName.WRITER, content=response.content)
        )

        return state
