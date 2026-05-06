"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def __init__(self, llm_client: LLMClient, search_client: SearchClient):
        self.llm_client = llm_client
        self.search_client = search_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""

        # 1. Search for information
        results = self.search_client.search(
            state.request.query, max_results=state.request.max_sources
        )
        state.sources.extend(results)

        # 2. Synthesize notes using LLM
        source_text = "\n".join(
            [f"- {r.title} ({r.url}): {r.snippet}" for r in results]
        )
        system_prompt = (
            "You are a professional researcher. "
            "Your task is to synthesize search results into concise, factual research notes. "
            "Focus on answering the user's query and highlighting key information."
        )
        user_prompt = (
            f"Query: {state.request.query}\n\n"
            f"Search Results:\n{source_text}\n\n"
            "Research Notes:"
        )

        response = self.llm_client.complete(system_prompt, user_prompt)
        
        # 3. Update state
        state.research_notes = (state.research_notes or "") + "\n" + response.content
        state.agent_results.append(
            AgentResult(agent=AgentName.RESEARCHER, content=response.content)
        )
        
        return state
