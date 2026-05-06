"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""

        if not state.research_notes:
            state.errors.append("Analyst called without research notes.")
            return state

        system_prompt = (
            "You are a strategic analyst. "
            "Your task is to take research notes and extract key claims, compare different viewpoints, "
            "and identify any gaps or weak evidence. Provide structured insights."
        )
        user_prompt = f"Research Notes:\n{state.research_notes}\n\nAnalysis:"

        response = self.llm_client.complete(system_prompt, user_prompt)

        state.analysis_notes = response.content
        state.agent_results.append(
            AgentResult(agent=AgentName.ANALYST, content=response.content)
        )

        return state
