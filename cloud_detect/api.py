from pathlib import Path
from flask import Flask, request, jsonify

from .io import image_from_json, image_data_to_cv2_image
from .object_detection import load_model, detect_objects

app = Flask(__name__)

YOLO_DIR = Path(__file__).parent.parent / "yolo_tiny_configs"
net, labels = load_model(YOLO_DIR)


@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/cloud-detect', methods=['POST'])
def cloud_detect():
    uuid, img = image_from_json(request.data)
    cv2_img = image_data_to_cv2_image(img)
    objects = detect_objects(cv2_img, net, labels)
    result = {
        "id": str(uuid),
        "objects": objects,
        }
    return jsonify(result), 200