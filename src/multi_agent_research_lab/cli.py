"""Command-line entrypoint for the lab starter."""

from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging
from multi_agent_research_lab.services.llm_client import LLMClient

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a minimal single-agent baseline implementation."""

    _init()
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    
    llm = LLMClient()
    response = llm.complete(
        system_prompt="You are a helpful research assistant. Provide a comprehensive answer to the research query.",
        user_prompt=query
    )
    
    state.final_answer = response.content
    console.print(Panel.fit(state.final_answer, title="Single-Agent Baseline"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow skeleton."""

    _init()
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    try:
        result = workflow.run(state)
    except StudentTodoError as exc:
        console.print(Panel.fit(str(exc), title="Expected TODO", style="yellow"))
        raise typer.Exit(code=2) from exc
    console.print(result.model_dump_json(indent=2))


@app.command()
def benchmark(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
    output: Annotated[str, typer.Option("--output", "-o", help="Report file")] = "reports/benchmark_report.md",
) -> None:
    """Run both baseline and multi-agent and compare results."""
    _init()
    from multi_agent_research_lab.evaluation.benchmark import run_benchmark
    from multi_agent_research_lab.evaluation.report import render_markdown_report
    
    # 1. Runner for baseline
    def baseline_runner(q: str) -> ResearchState:
        llm = LLMClient()
        state = ResearchState(request=ResearchQuery(query=q))
        resp = llm.complete("You are a helpful research assistant. Provide a comprehensive answer.", q)
        state.final_answer = resp.content
        return state
    
    # 2. Runner for multi-agent
    def multi_agent_runner(q: str) -> ResearchState:
        workflow = MultiAgentWorkflow()
        state = ResearchState(request=ResearchQuery(query=q))
        return workflow.run(state)
    
    console.print("[bold blue]Starting Benchmark...[/bold blue]")
    
    console.print("Running Single-Agent Baseline...")
    _, baseline_metrics = run_benchmark("Baseline (Single-Agent)", query, baseline_runner)
    
    console.print("Running Multi-Agent Workflow...")
    _, multi_agent_metrics = run_benchmark("Multi-Agent Workflow", query, multi_agent_runner)
    
    report_md = render_markdown_report([baseline_metrics, multi_agent_metrics])
    
    import os
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        f.write(report_md)
    
    console.print(Panel.fit(f"Benchmark report saved to [green]{output}[/green]", title="Benchmark Complete"))


if __name__ == "__main__":
    app()
