import pytest
from unittest.mock import MagicMock

from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.core.schemas import ResearchQuery, SourceDocument
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient, LLMResponse
from multi_agent_research_lab.services.search_client import SearchClient


@pytest.fixture
def mock_llm():
    client = MagicMock(spec=LLMClient)
    client.complete.return_value = LLMResponse(content="researcher", input_tokens=10, output_tokens=5)
    return client


@pytest.fixture
def mock_search():
    client = MagicMock(spec=SearchClient)
    client.search.return_value = [
        SourceDocument(title="Test", url="http://test.com", snippet="Test snippet")
    ]
    return client


def test_supervisor_routing(mock_llm):
    state = ResearchState(request=ResearchQuery(query="Test query"))
    agent = SupervisorAgent(mock_llm)
    
    # Mock LLM to return 'researcher'
    mock_llm.complete.return_value = LLMResponse(content="researcher")
    
    new_state = agent.run(state)
    assert new_state.route_history == ["researcher"]
    assert new_state.iteration == 1


def test_researcher_run(mock_llm, mock_search):
    state = ResearchState(request=ResearchQuery(query="Test query"))
    agent = ResearcherAgent(mock_llm, mock_search)
    
    mock_llm.complete.return_value = LLMResponse(content="These are research notes.")
    
    new_state = agent.run(state)
    assert len(new_state.sources) == 1
    assert "These are research notes." in new_state.research_notes
    assert len(new_state.agent_results) == 1
