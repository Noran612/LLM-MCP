from typing import List, Dict
import random

class YOLODetectorService:
    def __init__(self):
        # Mock detection - in reality this would use the actual YOLO model
        self.detection_classes = ['car', 'person', 'bicycle', 'truck', 'dog']
    
    def detect_objects(self, image_ids: List[str]) -> Dict[str, List[str]]:
        results = {}
        for img_id in image_ids:
            # Simulate detection with random results
            num_objects = random.randint(0, 3)
            detected = random.sample(self.detection_classes, num_objects)
            results[img_id] = detected
        #print(f"Detected objects for images {image_ids}: {results}")
        return results