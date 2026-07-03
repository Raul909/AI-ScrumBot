"""Central tool registry.

Combines stateless web-research tools with the stateful DevOps tools. The DevOps
client is injected (built and owned by the application container) so tools share
its pooled HTTP connection.
"""
from __future__ import annotations

from typing import List, Optional

from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_core.tools import BaseTool

from scrumbot.custom_backend.client import DevOpsClient
from scrumbot.custom_backend.tools import get_devops_tools


def get_web_tools() -> List[BaseTool]:
    """Stateless research tools: web search, arXiv, Wikipedia."""
    return [
        DuckDuckGoSearchRun(),
        ArxivQueryRun(api_wrapper=ArxivAPIWrapper()),
        WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    ]


def get_all_tools(devops_client: Optional[DevOpsClient] = None) -> List[BaseTool]:
    """Assemble the full tool set for the agent.

    Args:
        devops_client: When provided, DevOps board tools bound to this client
            are included. When ``None`` (e.g. a research-only deployment) only
            the web tools are returned.
    """
    tools: List[BaseTool] = get_web_tools()
    if devops_client is not None:
        tools.extend(get_devops_tools(devops_client))
    return tools
