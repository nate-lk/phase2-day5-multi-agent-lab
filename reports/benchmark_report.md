# Multi-Agent Research Lab: Benchmark Report

This report compares the performance and quality of single-agent vs. multi-agent research workflows.

## Results Table

| Run | Latency (s) | Cost (USD) | Quality (0-10) | Notes |
|---|---:|---:|---:|---|
| Baseline (Single-Agent) | 13.29 | $0.0005 | 6.5 | Total steps: 0. Sources found: 0. |
| Multi-Agent Workflow | 27.57 | $0.0020 | 8.5 | Total steps: 4. Sources found: 5. |

## Key Observations
- **Multi-agent** workflows typically have higher latency due to sequential agent calls.
- **Quality** is generally higher in multi-agent runs as specialized roles (Analyst, Writer) refine the research findings.
- **Cost** increases with more agents, but provides better synthesis and fewer hallucinations.
