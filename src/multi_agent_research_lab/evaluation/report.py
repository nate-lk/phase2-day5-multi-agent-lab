"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown."""

    lines = [
        "# Multi-Agent Research Lab: Benchmark Report",
        "",
        "This report compares the performance and quality of single-agent vs. multi-agent research workflows.",
        "",
        "## Results Table",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality (0-10) | Notes |",
        "|---|---:|---:|---:|---|",
    ]
    for item in metrics:
        cost = "N/A" if item.estimated_cost_usd is None else f"${item.estimated_cost_usd:.4f}"
        quality = "N/A" if item.quality_score is None else f"{item.quality_score:.1f}"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |")
    
    lines.extend([
        "",
        "## Failure Modes & Potential Fixes",
        "",
        "### 1. Infinite Routing Loops",
        "- **Failure**: The Supervisor keeps toggling between two agents (e.g., Researcher and Analyst) without making progress.",
        "- **Fix**: Implemented a `max_iterations` guardrail in the Supervisor to force a 'done' state after a threshold.",
        "",
        "### 2. Context Drift & Hallucinations",
        "- **Failure**: The Writer starts generating facts not present in the research notes.",
        "- **Fix**: Integrated a 'Critic' agent that performs a dedicated fact-check and provides corrective feedback before finalization.",
        "",
        "### 3. API Transient Failures",
        "- **Failure**: LLM or Search API calls fail due to rate limits or network issues.",
        "- **Fix**: Added exponential backoff retry logic using the `tenacity` library in the `LLMClient`.",
        "",
        "### 4. Search Irrelevance",
        "- **Failure**: The Researcher gathers snippets that don't answer the core query.",
        "- **Fix**: Researcher uses an LLM-driven synthesis step to filter and summarize only the relevant parts of the search results.",
    ])
    
    return "\n".join(lines) + "\n"
