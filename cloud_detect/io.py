"""Utilities to convert between data formats."""
import uuid
import json
import base64
from pathlib import Path

import cv2
import numpy as np 

def image_file_to_json(img_path: Path):
    img_id = uuid.uuid5(uuid.NAMESPACE_URL, img_path.stem)
    with open(img_path, "rb") as f:
        img_bytes = f.read()
        encoded_img = base64.b64encode(img_bytes).decode("utf-8")
    
    return {
        "id": str(img_id),
        "image": encoded_img
    }


def image_file_to_cv2_image(img_path: Path) -> np.ndarray:
    cv2_img = cv2.imread(str(img_path))
    return cv2_img

def image_from_json(json_data: str) -> tuple[uuid.UUID, bytes]:
    data = json.loads(json_data)
    img_id = data["id"]
    img_bytes = base64.b64decode(data["image"])
    return img_id, img_bytes

def image_data_to_cv2_image(data: bytes) -> np.ndarray:
    cv2_img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
    return cv2_img

def cv2_image_to_plt_image(cv2_img: np.ndarray) -> np.ndarray:
    plt_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return plt_img
