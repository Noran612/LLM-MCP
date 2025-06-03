from datetime import datetime,date
from typing import List, Dict
import random

class ImageDBService:
    def __init__(self):
        # Mock database with 1000 images from different times
        self.images = []
        today = date.today()
        for i in range(1000):
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            self.images.append({
                'id': f'img_{i:04d}.jpg',
                 'timestamp': datetime(today.year, today.month, today.day, hour, minute).isoformat()
            })
    def get_images_by_time_range(self, start_time: str, end_time: str) -> List[str]:
        if len(start_time) == 8:  # format: "HH:MM:SS"
            start_time = f"{date.today().isoformat()}T{start_time}"
        if len(end_time) == 8:
            end_time = f"{date.today().isoformat()}T{end_time}"

        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)

        matching_ids = [
            img['id']
            for img in self.images
            if start_dt <= datetime.fromisoformat(img['timestamp']) <= end_dt
        ]
        
        print(f"Found {len(matching_ids)} images in time range {start_time} to {end_time}")
        return matching_ids
