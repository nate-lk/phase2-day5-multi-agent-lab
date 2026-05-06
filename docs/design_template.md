# Design Template: Multi-Agent Research System

## Problem
The system is designed to handle complex research queries that require multiple steps: searching for information from diverse sources, performing critical analysis to identify key claims and gaps, and synthesizing a polished final report for specific audiences.

## Why multi-agent?
Single-agent systems often struggle with "context drift" and hallucination when tasked with long-form research. They tend to skip deep analysis or fail to verify their own claims. A multi-agent approach provides:
1. **Specialization**: Each agent focuses on one task (e.g., searching vs. analyzing), leading to higher quality.
2. **Error Correction**: Specialized roles like a 'Critic' can catch mistakes made by the 'Writer'.
3. **Structured Handoffs**: By forcing a shared state, we ensure information is explicitly processed at each stage.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Orchestration & Routing | Current state progress | Next agent name | Loop/Stuck |
| Researcher | Info Retrieval & Synthesis | User query | Research notes + Sources | Irrelevant sources |
| Analyst | Critical Evaluation | Research notes | Analysis notes (claims/gaps) | Shallow analysis |
| Writer | Content Generation | Research & Analysis notes | Final answer | Style mismatches |
| Critic | Fact-checking & Review | Notes + Final answer | Approval or Feedback | Overly harsh/lenient |

## Shared state
The `ResearchState` uses the following key fields:
- `request`: Holds the original query and audience parameters.
- `sources`: Maintains a list of all retrieved documents for transparency.
- `research_notes`: Raw synthesis of external data.
- `analysis_notes`: Structured insights and critique of the research.
- `final_answer`: The final deliverable for the user.
- `route_history`: Tracks agent execution to prevent infinite loops and aid debugging.

## Routing policy
The system uses a **Centralized Supervisor** pattern built on LangGraph:
1. Entry -> **Supervisor**.
2. Supervisor -> **Researcher** (if notes missing).
3. Researcher -> **Supervisor**.
4. Supervisor -> **Analyst** (if research done).
5. Analyst -> **Supervisor**.
6. Supervisor -> **Writer** (if analysis done).
7. Writer -> **Supervisor**.
8. Supervisor -> **Critic** (for final check).
9. Critic -> **Supervisor**.
10. Supervisor -> **END** (if approved).

## Guardrails
- **Max iterations**: Limited to 6 steps to prevent runaway costs.
- **Timeout**: Each LLM call is protected by provider-level timeouts.
- **Retry**: Implemented via the `tenacity` library in the LLM client (standard practice).
- **Fallback**: Supervisor defaults to 'done' if the LLM fails to provide a valid next step.
- **Validation**: Pydantic schemas enforce strict input/output formats for all agents.

## Benchmark plan
- **Query**: "Research GraphRAG state-of-the-art and write a short summary"
- **Metrics**: Latency (s), Estimated Cost (USD), Quality Score (0-10).
- **Expected Outcome**: Multi-agent should show ~2x higher latency but ~25% higher quality/depth compared to a single-agent baseline.
