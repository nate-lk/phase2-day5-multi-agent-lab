"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.

        Currently implemented as a Mock for the lab.
        """
        return [
            SourceDocument(
                title=f"Insightful Article on {query} - Part {i+1}",
                url=f"https://knowledge-base.org/research/{query.lower().replace(' ', '-')}-{i}",
                snippet=f"This document provides key details regarding {query}. It covers essential aspects and recent developments in the field, specifically focusing on sub-topic {i+1}."
            )
            for i in range(max_results)
        ]
