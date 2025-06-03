from mcp.service_registry import ServiceRegistry
from mcp.orchestrator import MCPOrchestrator
from Services.image_db import ImageDBService
from Services.yolo_detector import YOLODetectorService
from typing import List, Dict, Any
from openai import OpenAI  # or any other LLM provider
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
class MissionProcessor:
    def __init__(self):
        # Initialize services
        self.image_db = ImageDBService()
        self.yolo_detector = YOLODetectorService()
        
        # Initialize MCP
        self.service_registry = ServiceRegistry()
        self.orchestrator = MCPOrchestrator(self.service_registry)
        
        # Register services
        self.service_registry.register_service(
            "image_db",
            "local/image_db",
            self.image_db.get_images_by_time_range
        )
        
        self.service_registry.register_service(
            "yolo_detector",
            "local/yolo_detector",
            self.yolo_detector.detect_objects
        )
        
        # LLM configuration
        #openai.api_key = os.getenv("OPENAI_API_KEY")

    def parse_mission_with_llm(self, mission_text: str) -> Dict[str, Any]:
        """Use LLM to parse natural language mission into structured service calls"""
        prompt = f"""
        You are a mission parsing assistant. Convert the following mission into structured JSON.

        Mission: "{mission_text}"

        The output format should be:
        {{
            "services": ["service1", "service2"],
            "parameters": {{
                "service1": {{...}},
                "service2": {{...}}
            }},
            "expected_output": "description of expected output"
        }}

        Available services: {list(self.service_registry.list_services().keys())}

        Parameter rules for services:
        - "image_db" requires:
            {{
                "start_time": "<ISO timestamp string>",
                "end_time": "<ISO timestamp string>"
            }}

        - "yolo_detector" requires:
            {{
                "image_ids": "<list of images or reference like $image_db>"
            }}

        If one service needs the output of another, use a dollar sign to reference it, like:
            "image_ids": "$image_db"

        Respond with only the JSON structure and nothing else.
        """
        response = client.responses.create(
            model="gpt-3.5-turbo",
            input=[{"role": "system", "content": prompt}]
        )
        #print("Mission parsed successfully:", response.output_text)
        try:
            return eval(response.output_text)
        except:
            raise ValueError("Failed to parse mission")

    async def execute_mission(self, mission_text: str):
        """Execute a complete mission locally"""
        # Step 1: Parse mission with LLM
        parsed_mission = self.parse_mission_with_llm(mission_text)
        
        # Step 2: Execute services in order via MCP
        intermediate_results = {}
        
        for service in parsed_mission["services"]:
            params = parsed_mission["parameters"].get(service, {})
            
            # If parameters reference previous results, substitute them
            for k, v in params.items():
                if isinstance(v, str) and v.startswith("$"):
                    ref_service = v[1:]
                    params[k] = intermediate_results[ref_service]
            
            result = await self.orchestrator.execute_service(service, params)
            intermediate_results[service] = result
        
        # Special handling for our car detection mission
        if "image_db" in parsed_mission["services"] and "yolo_detector" in parsed_mission["services"]:
            images_in_range = intermediate_results["image_db"]
            image_ids =  images_in_range
            detections = intermediate_results["yolo_detector"]
            
            # Filter images with cars
            images_with_cars = [img_id for img_id, objects in detections.items() 
                               if "car" in objects]
            return images_with_cars
        
        return intermediate_results[parsed_mission["services"][-1]]

async def main():
    processor = MissionProcessor()
    
    # Example mission
    mission = "detect all cars in images between 11:00 and 11:05"
    
    print(f"Executing mission: {mission}")
    result = await processor.execute_mission(mission)
    
    print("\nMission Results:")
    for img_id in result:
        print(f"- Image with cars found: {img_id}")

if __name__ == "__main__":
    asyncio.run(main())