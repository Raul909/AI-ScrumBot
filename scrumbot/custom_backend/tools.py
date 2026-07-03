from typing import Any, Dict, List, Optional

from langchain_core.tools import BaseTool, tool

from .client import DevOpsClient

client = DevOpsClient()

@tool
async def devops_list_epics() -> Dict[str, Any]:
    """List all epics from DevOpsBackend."""
    # Using get_resources to fetch epics based on the provided API capabilities
    res = await client.get_resources()
    return {"epics": res.get("epics", [])}

@tool
async def devops_list_tasks() -> Dict[str, Any]:
    """List all tasks from DevOpsBackend."""
    # Using get_resources to fetch tasks
    res = await client.get_resources()
    return {"tasks": res.get("tasks", [])}

@tool
async def devops_update_task_status(task_id: str, status: str) -> Dict[str, Any]:
    """
    Update the status of a specific task in DevOpsBackend.
    
    Args:
        task_id (str): The unique identifier of the task.
        status (str): The new status to apply to the task.
    """
    return await client.update_node("task", task_id, {"status": status})

@tool
async def devops_get_board_overview() -> Dict[str, Any]:
    """Get an overview of the Scrum board."""
    return await client.get_resources()

@tool
async def devops_create_task(title: str, description: str, epic_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task in DevOpsBackend.
    
    Args:
        title (str): Title of the new task.
        description (str): Description of the new task.
        epic_id (str, optional): The ID of the epic this task belongs to.
    """
    # This is a placeholder since POST /bot/tasks or similar wasn't fully defined.
    # We will just return a mock success response for now.
    return {
        "status": "success", 
        "message": "Task created (placeholder)", 
        "task": {
            "title": title, 
            "description": description,
            "epic_id": epic_id
        }
    }

def get_devops_tools() -> List[BaseTool]:
    """
    Get a list of all available DevOpsBackend LangChain tools.
    
    Returns:
        List[BaseTool]: A list of tools for the agent to use.
    """
    return [
        devops_list_epics,
        devops_list_tasks,
        devops_update_task_status,
        devops_get_board_overview,
        devops_create_task
    ]
