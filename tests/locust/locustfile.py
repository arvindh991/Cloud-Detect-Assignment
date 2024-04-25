import time
from pathlib import Path
from locust import HttpUser, task, between
import cloud_detect.io

image_dir = Path("../data/images")
images = list(image_dir.glob("*.jpg"))

class ObjectDetector(HttpUser):
    host = "http://168.138.31.171:30005/"
    wait_time = between(1, 5)

    @task
    def detect_objects(self):
        for img_path in images:
            json_data = cloud_detect.io.image_file_to_json(img_path)
            self.client.post("/cloud-detect", json=json_data)
            time.sleep(1)