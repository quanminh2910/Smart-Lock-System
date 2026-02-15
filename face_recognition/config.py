"""
Configuration for Face Recognition System
"""

# Server Configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Face Recognition Settings
TOLERANCE = 0.6  # Lower is more strict (0.4-0.6 recommended)
MODEL = 'hog'    # 'hog' (faster, CPU) or 'cnn' (accurate, GPU)
RESIZE_FACTOR = 0.25  # Resize images for faster processing

# File Paths
KNOWN_FACES_DIR = 'models/known_faces'
ENCODINGS_FILE = 'models/face_encodings.pkl'

# Image Processing
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Security
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # seconds (5 minutes)
