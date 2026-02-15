"""
Face detection utilities
"""

import face_recognition
import config


def detect_faces(image):
    """
    Detect faces in an image
    
    Args:
        image: RGB image array
        
    Returns:
        List of face locations [(top, right, bottom, left), ...]
    """
    face_locations = face_recognition.face_locations(
        image, 
        model=config.MODEL,
        number_of_times_to_upsample=1
    )
    return face_locations


def get_face_encodings(image, face_locations=None):
    """
    Get face encodings from image
    
    Args:
        image: RGB image array
        face_locations: Optional list of face locations
        
    Returns:
        List of 128-dimensional face encodings
    """
    if face_locations is None:
        face_locations = detect_faces(image)
    
    encodings = face_recognition.face_encodings(
        image,
        known_face_locations=face_locations,
        num_jitters=1
    )
    return encodings
