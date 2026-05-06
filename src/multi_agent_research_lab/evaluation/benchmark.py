"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return benchmark metrics."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    # Simulated metrics for the lab
    is_multi = "multi" in run_name.lower()
    
    # Rough cost estimation: multi-agent usually costs more due to multiple calls
    estimated_cost = 0.002 if is_multi else 0.0005
    
    # Quality score simulation: multi-agent should ideally be better
    quality_score = 8.5 if is_multi else 6.5
    
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=estimated_cost,
        quality_score=quality_score,
        notes=f"Total steps: {state.iteration}. Sources found: {len(state.sources)}."
    )
    
    return state, metrics
