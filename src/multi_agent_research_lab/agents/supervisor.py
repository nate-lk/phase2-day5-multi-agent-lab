"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.config import get_settings


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.settings = get_settings()

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""

        # Guardrail: Max Iterations
        if state.iteration >= self.settings.max_iterations:
            next_step = "done"
            state.errors.append(f"Max iterations ({self.settings.max_iterations}) reached. Forcing stop.")
        else:
            system_prompt = (
            "You are a research supervisor. Your job is to orchestrate a team of agents: "
            "Researcher, Analyst, Writer, and Critic.\n"
            "Decide the next step based on the current state. "
            "Return ONLY the name of the next agent ('researcher', 'analyst', 'writer', 'critic') or 'done' if the task is complete.\n\n"
            "Routing Rules:\n"
            "1. If research_notes are missing or insufficient, call 'researcher'.\n"
            "2. If research_notes exist but analysis_notes are missing, call 'analyst'.\n"
            "3. If analysis_notes exist but final_answer is missing, call 'writer'.\n"
            "4. If final_answer exists but has not been reviewed, call 'critic'.\n"
            "5. If critic has approved or provided final feedback, return 'done'."
        )
        
        user_prompt = (
            f"Query: {state.request.query}\n"
            f"Has Research: {bool(state.research_notes)}\n"
            f"Has Analysis: {bool(state.analysis_notes)}\n"
            f"Has Final Answer: {bool(state.final_answer)}\n"
            f"Has been Reviewed: {any(r.agent == 'critic' for r in state.agent_results)}\n"
            f"Route History: {state.route_history}\n"
            "Next step:"
        )

        response = self.llm_client.complete(system_prompt, user_prompt)
        next_step = response.content.lower().strip().strip("'").strip('"')

        # Fallback and validation
        valid_routes = ["researcher", "analyst", "writer", "critic", "done"]
        if next_step not in valid_routes:
            # Simple heuristic fallback
            if not state.research_notes: next_step = "researcher"
            elif not state.analysis_notes: next_step = "analyst"
            elif not state.final_answer: next_step = "writer"
            elif not any(r.agent == 'critic' for r in state.agent_results): next_step = "critic"
            else: next_step = "done"

        state.record_route(next_step)
        state.agent_results.append(
            AgentResult(
                agent=AgentName.SUPERVISOR, 
                content=f"Routing to: {next_step}",
                metadata={"next_agent": next_step}
            )
        )

        return state
