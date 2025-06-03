from typing import Dict, Any, Callable
from fastapi import HTTPException

class ServiceRegistry:
    def __init__(self):
        self.services = {}

    def register_service(self, service_name: str, service_endpoint: str, service_function: Callable):
        self.services[service_name] = {
            'endpoint': service_endpoint,
            'function': service_function
        }

    def get_service(self, service_name: str) -> Dict[str, Any]:
        if service_name not in self.services:
            raise HTTPException(status_code=404, detail="Service not found")
        return self.services[service_name]

    def list_services(self) -> Dict[str, str]:
        return {name: service['endpoint'] for name, service in self.services.items()}