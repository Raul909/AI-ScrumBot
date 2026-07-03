import os
from typing import Any, Dict

import httpx


class DevOpsClient:
    """Client for interacting with the DevOpsBackend REST API."""
    
    def __init__(self) -> None:
        """Initialize the DevOpsBackend client with URL and API key from environment."""
        self.api_url = os.environ.get("DEVOPS_API_URL", "http://localhost:8000/api")
        self.api_key = os.environ.get("BOT_API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def get_resources(self) -> Dict[str, Any]:
        """
        Fetch bot resources from the DevOpsBackend API.
        
        Returns:
            Dict[str, Any]: The response data containing bot resources.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/bot/resources",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
            
    async def update_node(self, node_type: str, node_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a devops node.
        
        Args:
            node_type (str): The type of the node (e.g., 'epic', 'task').
            node_id (str): The unique identifier of the node.
            fields (Dict[str, Any]): The fields and values to update.
            
        Returns:
            Dict[str, Any]: The response data from the API.
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/devops/nodes/{node_type}/{node_id}",
                headers=self.headers,
                json=fields
            )
            response.raise_for_status()
            return response.json()
