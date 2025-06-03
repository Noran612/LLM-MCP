from typing import List, Dict
from datetime import datetime,date
import os
from PIL import Image
import hashlib

class ImageDBService:
    def __init__(self, storage_dir: str = 'image_storage'):
        """
        Initialize with a storage directory
        :param storage_dir: Path to directory where images are stored
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Create in-memory index (in a real system, use a database)
        self.image_index = []

    def store_image(self, image_path: str) -> str:
        with Image.open(image_path) as img:
            timestamp = datetime.now().isoformat()  # valid ISO format
            safe_timestamp = timestamp.replace(":", "-")  # safe for filename

            with open(image_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()

            img_id = f"{content_hash}_{safe_timestamp}"
            dest_path = os.path.join(self.storage_dir, f"{img_id}.jpg")
            img.save(dest_path)

            # Use the original ISO timestamp in metadata
            self.image_index.append({
                'id': img_id,
                'path': dest_path,
                'timestamp': timestamp
            })

            return img_id


    def get_images_by_time_range(self, start_time: str, end_time: str) -> List[Dict]:
        """
        Get images within a time range
        :param start_time: ISO format datetime string
        :param end_time: ISO format datetime string
        :return: List of image metadata dictionaries
        """
        if len(start_time) == 8:  # format: "HH:MM:SS"
            start_time = f"{date.today().isoformat()}T{start_time}"
        if len(end_time) == 8:
            end_time = f"{date.today().isoformat()}T{end_time}"

        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        return [img for img in self.image_index 
                if start_dt <= datetime.fromisoformat(img['timestamp']) <= end_dt]