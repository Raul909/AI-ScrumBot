from typing import Any, Dict, List
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import create_react_agent
from scrumbot.llm import get_llm
from scrumbot.tools import get_all_tools

class ScrumAgent:
    """
    Core Agent for ScrumBot using LangGraph's create_react_agent.
    """
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        """
        Initializes the ScrumAgent.
        
        Args:
            model_name: The name of the LLM to use.
        """
        self.llm = get_llm(model_name)
        self.tools = get_all_tools()
        self.agent = create_react_agent(self.llm, self.tools)
        
    async def invoke(self, messages: List[BaseMessage], **kwargs: Any) -> Dict[str, Any]:
        """
        Invokes the agent with a list of messages.
        
        Args:
            messages: List of messages (HumanMessage, AIMessage, etc.).
            
        Returns:
            The state dictionary from the agent execution.
        """
        state = {"messages": messages}
        return await self.agent.ainvoke(state, **kwargs)
