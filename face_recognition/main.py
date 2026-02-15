"""
Face Recognition REST API Server
Receives images from ESP32, performs face recognition, and returns results
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import pickle
import os
from datetime import datetime
import config
from utils.face_detector import detect_faces
from utils.face_matcher import match_face
from utils.image_processor import preprocess_image

app = Flask(__name__)
CORS(app)

# Load known face encodings
encodings_data = None
if os.path.exists(config.ENCODINGS_FILE):
    with open(config.ENCODINGS_FILE, 'rb') as f:
        encodings_data = pickle.load(f)
    print(f"Loaded {len(encodings_data['names'])} known faces")
else:
    print("Warning: No face encodings found. Please run train_faces.py first.")
    encodings_data = {'encodings': [], 'names': []}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'known_faces': len(encodings_data['names'])
    })


@app.route('/recognize', methods=['POST'])
def recognize_face():
    """
    Main face recognition endpoint
    Expects: JSON with base64 encoded image
    Returns: JSON with recognition result
    """
    try:
        # Get image from request
        if 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(request.json['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Detect faces
        face_locations = detect_faces(processed_image)
        
        if len(face_locations) == 0:
            return jsonify({
                'success': False,
                'message': 'No face detected',
                'timestamp': datetime.now().isoformat()
            })
        
        if len(face_locations) > 1:
            return jsonify({
                'success': False,
                'message': 'Multiple faces detected',
                'timestamp': datetime.now().isoformat()
            })
        
        # Match face with known faces
        result = match_face(processed_image, face_locations[0], encodings_data)
        
        return jsonify({
            'success': result['matched'],
            'name': result.get('name', 'Unknown'),
            'confidence': result.get('confidence', 0.0),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/add_face', methods=['POST'])
def add_face():
    """
    Add a new face to the system
    Expects: JSON with base64 encoded image and name
    """
    try:
        if 'image' not in request.json or 'name' not in request.json:
            return jsonify({'error': 'Image and name required'}), 400
        
        # Decode image
        image_data = base64.b64decode(request.json['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        name = request.json['name']
        
        # Save image to known_faces directory
        os.makedirs(config.KNOWN_FACES_DIR, exist_ok=True)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(config.KNOWN_FACES_DIR, filename)
        cv2.imwrite(filepath, image)
        
        return jsonify({
            'success': True,
            'message': f'Face image saved. Please retrain the model.',
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(config.KNOWN_FACES_DIR, exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    print(f"Starting Face Recognition API Server on {config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
