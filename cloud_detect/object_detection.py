"""Object detection using YOLOv3"""

from loguru import logger
from pathlib import Path
import time
import numpy as np
import cv2

from typing import List

CONFIDENCE = 0.5
THRESHOLD = 0.3


def load_model(model_path: Path) -> tuple[cv2.dnn_Net, List[str]]:
    """Load YOLOv3 model parameters and labels from disk."""
    labelsPath = model_path / "coco.names"
    labels = open(labelsPath).read().strip().split("\n")
    logger.info(f"Read YOLOv3 labels from {labelsPath}.")

    weightsPath = model_path / "yolov3-tiny.weights"
    configPath = model_path / "yolov3-tiny.cfg"
    logger.info("Loading YOLOv3 from disk...")
    net = cv2.dnn.readNetFromDarknet(str(configPath), str(weightsPath))
    logger.info("Loaded YOLOv3 from disk.")
    return net, labels


def detect_objects(image: np.ndarray, net: cv2.dnn_Net, labels: List[str]) -> List:
    """Use the YOLOv3 model to detect objects in an image."""
    (H, W) = image.shape[:2]
    ln = net.getUnconnectedOutLayersNames()
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()
    logger.info(f"YOLO took {end - start:.6f} seconds")

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
         for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > CONFIDENCE:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # non-maxima suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)

    objects = []
    if len(idxs) > 0:
        #TODO: what happens if no boxes are found?
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            objects.append({
                "label": labels[classIDs[i]],
                "accuracy": confidences[i],
                "rectangle": {
                    "height": h,
                    "width": w,
                    "left": x,
                    "top": y,
                }
            })
    logger.info(f"YOLO found {len(objects)} objects.")
    return objects
