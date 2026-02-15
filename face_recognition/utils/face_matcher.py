"""
Face matching utilities
"""

import face_recognition
import numpy as np
import config
from .face_detector import get_face_encodings


def match_face(image, face_location, encodings_data):
    """
    Match a face against known faces
    
    Args:
        image: RGB image array
        face_location: Tuple (top, right, bottom, left)
        encodings_data: Dict with 'encodings' and 'names' lists
        
    Returns:
        Dict with 'matched', 'name', and 'confidence'
    """
    if not encodings_data['encodings']:
        return {'matched': False, 'name': 'Unknown', 'confidence': 0.0}
    
    # Get encoding for the detected face
    face_encodings = get_face_encodings(image, [face_location])
    
    if len(face_encodings) == 0:
        return {'matched': False, 'name': 'Unknown', 'confidence': 0.0}
    
    face_encoding = face_encodings[0]
    
    # Compare with known faces
    distances = face_recognition.face_distance(
        encodings_data['encodings'],
        face_encoding
    )
    
    # Get best match
    best_match_index = np.argmin(distances)
    min_distance = distances[best_match_index]
    
    # Check if within tolerance
    if min_distance <= config.TOLERANCE:
        name = encodings_data['names'][best_match_index]
        confidence = 1 - min_distance  # Convert distance to confidence
        return {
            'matched': True,
            'name': name,
            'confidence': round(confidence, 2)
        }
    else:
        return {
            'matched': False,
            'name': 'Unknown',
            'confidence': round(1 - min_distance, 2)
        }
