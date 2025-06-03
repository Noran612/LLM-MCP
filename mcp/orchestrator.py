from .service_registry import ServiceRegistry
from typing import Dict, Any
import requests

class MCPOrchestrator:
    def __init__(self, service_registry: ServiceRegistry):
        self.registry = service_registry

    async def execute_service(self, service_name: str, params: Dict[str, Any]) -> Any:
        service = self.registry.get_service(service_name)
        
        # For local services
        if callable(service['function']):
            return service['function'](**params)
        
        # For remote services (HTTP endpoints)
        response = requests.post(service['endpoint'], json=params)
        response.raise_for_status()
        return response.json()