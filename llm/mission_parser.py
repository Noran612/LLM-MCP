from typing import List, Dict, Any
from datetime import time
from mcp.orchestrator import MCPOrchestrator

class MissionParser:
    def __init__(self, mcp: MCPOrchestrator):
        self.mcp = mcp
        self.service_descriptions = mcp.get_service_descriptions()
    
    async def process_mission(self, mission_text: str) -> List[str]:
        # In a real implementation, this would use an LLM to parse the mission
        # For this example, we'll hardcode the parsing for our specific mission
        
        # Parse time range (simplified parsing for demo)
        if "between" in mission_text and "and" in mission_text:
            time_part = mission_text.split("between")[1].strip()
            start_str, end_str = time_part.split("and")
            start_time = time.fromisoformat(start_str.strip() + ":00")
            end_time = time.fromisoformat(end_str.strip() + ":00")
        else:
            raise ValueError("Could not parse time range from mission")
        
        # Parse object to detect
        if "detect all" in mission_text.lower():
            obj = mission_text.lower().split("detect all")[1].split("in")[0].strip()
        else:
            obj = "car"  # default
        
        # Get images in time range
        images = await self.mcp.call_service(
            "Image DB",
            "get_images_by_time_range",
            start_time=start_time,
            end_time=end_time
        )
        
        # Detect objects in each image
        results = []
        for img in images:
            has_object = await self.mcp.call_service(
                "Yolo Detector",
                "detect_objects",
                image_path=img["path"],
                object_class=obj
            )
            
            if has_object:
                results.append(img["path"])
        
        return results