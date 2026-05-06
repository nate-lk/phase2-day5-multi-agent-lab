"""LangGraph workflow skeleton."""

from typing import Any
from langgraph.graph import StateGraph, END

from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.agents.critic import CriticAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.observability.tracing import trace_span


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def __init__(self) -> None:
        self.llm_client = LLMClient()
        self.search_client = SearchClient()
        
        self.supervisor = SupervisorAgent(self.llm_client)
        self.researcher = ResearcherAgent(self.llm_client, self.search_client)
        self.analyst = AnalystAgent(self.llm_client)
        self.writer = WriterAgent(self.llm_client)
        self.critic = CriticAgent(self.llm_client)

    def _run_supervisor(self, state: ResearchState) -> ResearchState:
        with trace_span("supervisor", state=state):
            return self.supervisor.run(state)

    def _run_researcher(self, state: ResearchState) -> ResearchState:
        with trace_span("researcher", state=state):
            return self.researcher.run(state)

    def _run_analyst(self, state: ResearchState) -> ResearchState:
        with trace_span("analyst", state=state):
            return self.analyst.run(state)

    def _run_writer(self, state: ResearchState) -> ResearchState:
        with trace_span("writer", state=state):
            return self.writer.run(state)

    def _run_critic(self, state: ResearchState) -> ResearchState:
        with trace_span("critic", state=state):
            return self.critic.run(state)

    def _get_next_step(self, state: ResearchState) -> str:
        """Helper for conditional routing."""
        if not state.route_history:
            return "supervisor"
        last_route = state.route_history[-1]
        if last_route == "done":
            return END
        return last_route

    def build(self) -> Any:
        """Create a LangGraph graph."""

        workflow = StateGraph(ResearchState)

        # Define nodes
        workflow.add_node("supervisor", self._run_supervisor)
        workflow.add_node("researcher", self._run_researcher)
        workflow.add_node("analyst", self._run_analyst)
        workflow.add_node("writer", self._run_writer)
        workflow.add_node("critic", self._run_critic)

        # Set entry point
        workflow.set_entry_point("supervisor")

        # Define conditional edges from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            lambda x: x.route_history[-1] if x.route_history else "supervisor",
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "critic": "critic",
                "done": END
            }
        )

        # Workers always go back to supervisor
        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("writer", "supervisor")
        workflow.add_edge("critic", "supervisor")

        return workflow.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        app = self.build()
        # LangGraph invoke returns the final state (often as a dict)
        result = app.invoke(state)
        
        if isinstance(result, dict):
            return ResearchState.model_validate(result)
        return result
