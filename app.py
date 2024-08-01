from flask import Flask, request, jsonify
from ultralytics import YOLO
from flask_cors import CORS
import base64
import os

app = Flask(__name__)

# Enable CORS for all routes and allow requests from http://localhost:3000
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load the pre-trained YOLO model
model = YOLO("yolov8n.pt")  # Replace 'yolov8n.pt' with the path to your pre-trained model weights

# Endpoint to train the model with your custom dataset
@app.route('/train', methods=['POST'])
def train():
    data = request.json
    config_file = data.get('config_file', 'config.yaml')
    epochs = data.get('epochs', 50)
    try:
        results = model.train(data=config_file, epochs=epochs)
        return jsonify({"message": "Model trained successfully", "results": str(results)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Endpoint to evaluate the model's performance
@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        results = model.val()
        return jsonify({"message": "Model evaluated successfully", "results": str(results)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Endpoint to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_data = data['image']
    location = data['location']  # Retrieve location data from the request
    print(location,"location")
    image_path = "temp_image.png"
    try:
        # Decode the base64 image data
        with open(image_path, "wb") as fh:
            fh.write(base64.b64decode(image_data.split(',')[1]))
        # Perform prediction
        results = model(image_path)
        # Optionally delete the temporary image file
        os.remove(image_path)
        # Extract relevant information from the results
        detections = []
        for result in results.xyxy[0]:
            detection = {
                "class": int(result[5]),  # class index
                "confidence": float(result[4]),  # confidence score
                "box": [float(result[0]), float(result[1]), float(result[2]), float(result[3])]  # bounding box
            }
            detections.append(detection)
        return jsonify({"message": "Prediction successful", "results": detections, "location": location}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
