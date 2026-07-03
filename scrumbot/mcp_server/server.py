from fastmcp import FastMCP
from scrumbot.agent import ScrumAgent
from langchain_core.messages import HumanMessage

# Initialize FastMCP server
mcp = FastMCP("ScrumBot", description="ScrumBot MCP Server")
agent = ScrumAgent()

@mcp.tool()
async def ask_scrum_bot(query: str) -> str:
    """
    Ask the ScrumBot a question or give it a task.
    """
    messages = [HumanMessage(content=query)]
    response = await agent.invoke(messages)
    # The last message in the state should be the AI's response
    last_message = response["messages"][-1]
    return last_message.content

def run():
    """Run the MCP server."""
    mcp.run(transport="stdio")
