from typing import List
from langchain_core.tools import BaseTool
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.utilities.arxiv import ArxivAPIWrapper

try:
    from scrumbot.custom_backend.tools import get_devops_tools
except ImportError:
    def get_devops_tools() -> List[BaseTool]:
        return []

def get_all_tools() -> List[BaseTool]:
    """
    Registry that combines duckduckgo, arxiv, wikipedia, and local tools.
    """
    tools: List[BaseTool] = []
    
    # Add external tools
    tools.append(DuckDuckGoSearchRun())
    tools.append(ArxivQueryRun(api_wrapper=ArxivAPIWrapper()))
    tools.append(WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()))
    
    # Add LP Admin tools
    tools.extend(get_devops_tools())
    
    return tools
