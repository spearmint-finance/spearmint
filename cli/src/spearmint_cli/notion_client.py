"""Notion API client for work history tracking."""
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests
from rich.console import Console

console = Console()


class NotionClient:
    """Client for interacting with Notion API."""
    
    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def create_work_entry(
        self,
        title: str,
        description: str,
        date: Optional[str] = None,
        duration: Optional[float] = None,
        tags: Optional[List[str]] = None,
        status: str = "Completed"
    ) -> Dict:
        """Create a new work history entry in Notion database."""
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID not set")
        
        # Format database ID (add hyphens if needed)
        db_id = self.database_id.replace("-", "")
        if len(db_id) == 32:
            # Format as: 8-4-4-4-12
            db_id = f"{db_id[:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:]}"
        
        date = date or datetime.now().strftime("%Y-%m-%d")
        tags = tags or []
        
        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "Title": {
                    "title": [{"text": {"content": title}}]
                },
                "Date": {
                    "date": {"start": date}
                },
                "Description": {
                    "rich_text": [{"text": {"content": description}}]
                },
                "Status": {
                    "select": {"name": status}
                }
            }
        }
        
        if duration:
            payload["properties"]["Duration"] = {"number": duration}
        
        if tags:
            payload["properties"]["Tags"] = {
                "multi_select": [{"name": tag} for tag in tags]
            }
        
        response = requests.post(
            f"{self.base_url}/pages",
            headers=self.headers,
            json=payload
        )
        
        if not response.ok:
            console.print(f"[red]Notion API Error: {response.status_code}[/red]")
            console.print(f"Response: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    def query_entries(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Query work history entries with filters."""
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID not set")
        
        filters = []
        
        if start_date:
            filters.append({
                "property": "Date",
                "date": {"on_or_after": start_date}
            })
        
        if end_date:
            filters.append({
                "property": "Date",
                "date": {"on_or_before": end_date}
            })
        
        if tags:
            for tag in tags:
                filters.append({
                    "property": "Tags",
                    "multi_select": {"contains": tag}
                })
        
        payload = {
            "page_size": limit,
            "sorts": [{"property": "Date", "direction": "descending"}]
        }
        
        if filters:
            payload["filter"] = {
                "and": filters
            } if len(filters) > 1 else filters[0]
        
        response = requests.post(
            f"{self.base_url}/databases/{self.database_id}/query",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json().get("results", [])
    
    def update_entry(self, page_id: str, **properties) -> Dict:
        """Update an existing work entry."""
        payload = {"properties": {}}
        
        if "title" in properties:
            payload["properties"]["Title"] = {
                "title": [{"text": {"content": properties["title"]}}]
            }
        
        if "description" in properties:
            payload["properties"]["Description"] = {
                "rich_text": [{"text": {"content": properties["description"]}}]
            }
        
        if "status" in properties:
            payload["properties"]["Status"] = {
                "select": {"name": properties["status"]}
            }
        
        if "duration" in properties:
            payload["properties"]["Duration"] = {
                "number": properties["duration"]
            }
        
        response = requests.patch(
            f"{self.base_url}/pages/{page_id}",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def search_database(self, query: str = "") -> List[Dict]:
        """Search for databases in Notion workspace."""
        payload = {
            "filter": {"property": "object", "value": "database"}
        }
        
        if query:
            payload["query"] = query
        
        response = requests.post(
            f"{self.base_url}/search",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json().get("results", [])
