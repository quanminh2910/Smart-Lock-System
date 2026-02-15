"""
Image preprocessing utilities
"""

import cv2
import numpy as np
import config


def preprocess_image(image):
    """
    Preprocess image for face recognition
    
    Args:
        image: BGR image from OpenCV
        
    Returns:
        RGB image array, optionally resized
    """
    # Convert BGR to RGB (face_recognition uses RGB)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Optionally resize for faster processing
    if config.RESIZE_FACTOR < 1.0:
        height, width = rgb_image.shape[:2]
        new_width = int(width * config.RESIZE_FACTOR)
        new_height = int(height * config.RESIZE_FACTOR)
        rgb_image = cv2.resize(rgb_image, (new_width, new_height))
    
    return rgb_image


def enhance_image(image):
    """
    Enhance image quality (optional preprocessing)
    
    Args:
        image: Input image
        
    Returns:
        Enhanced image
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge and convert back
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    return enhanced
