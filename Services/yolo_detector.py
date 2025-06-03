
from typing import List, Dict
from ultralytics import YOLO
import cv2
import os

class YOLODetectorService:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Initialize with a YOLO model
        :param model_path: Path to YOLO model weights (.pt file)
                          Defaults to yolov8n (nano) model
        """
        self.model = YOLO(model_path)
        self.class_names = self.model.names  # Get class names from model

    def detect_objects(self, image_ids: List[str]) -> Dict[str, List[str]]:
        """
        Detect objects in multiple images
        :param image_paths: List of paths to images
        :return: Dictionary with image paths as keys and detected classes as values
        """
        results = {}
        
        for img_path in image_ids:
            img_path = img_path['path'] 
            if not os.path.exists(img_path):
                print(f"Warning: Image not found - {img_path}")
                continue
                
            # Perform detection
            detections = self.model(img_path)
            
            # Get detected classes (using class names)
            detected_classes = []
            for detection in detections:
                for box in detection.boxes:
                    class_id = int(box.cls)
                    detected_classes.append(self.class_names[class_id])
            
            results[img_path] = detected_classes
        
        return results