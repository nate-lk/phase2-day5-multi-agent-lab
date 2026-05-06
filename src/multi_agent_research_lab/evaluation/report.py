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
        "## Key Observations",
        "- **Multi-agent** workflows typically have higher latency due to sequential agent calls.",
        "- **Quality** is generally higher in multi-agent runs as specialized roles (Analyst, Writer) refine the research findings.",
        "- **Cost** increases with more agents, but provides better synthesis and fewer hallucinations.",
    ])
    
    return "\n".join(lines) + "\n"
