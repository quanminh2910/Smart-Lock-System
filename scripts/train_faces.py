"""
Train the face recognition system by encoding known faces
Run this script whenever you add new faces to the models/known_faces directory
"""

import os
import sys
import pickle
import cv2
import face_recognition

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from face_recognition import config


def train_faces():
    """
    Load images from known_faces directory and create encodings
    """
    known_encodings = []
    known_names = []
    
    print(f"Loading images from {config.KNOWN_FACES_DIR}...")
    
    if not os.path.exists(config.KNOWN_FACES_DIR):
        print(f"Error: Directory {config.KNOWN_FACES_DIR} does not exist")
        return
    
    # Iterate through each person's folder or images
    image_files = [f for f in os.listdir(config.KNOWN_FACES_DIR) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if len(image_files) == 0:
        print("No images found in known_faces directory")
        print("Please add images named as: PersonName_01.jpg, PersonName_02.jpg, etc.")
        return
    
    for filename in image_files:
        # Extract name from filename (e.g., "John_01.jpg" -> "John")
        name = os.path.splitext(filename)[0].rsplit('_', 1)[0]
        
        filepath = os.path.join(config.KNOWN_FACES_DIR, filename)
        print(f"Processing {filename} (Name: {name})...")
        
        # Load image
        image = cv2.imread(filepath)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces and get encodings
        face_locations = face_recognition.face_locations(rgb_image, model=config.MODEL)
        
        if len(face_locations) == 0:
            print(f"  Warning: No face detected in {filename}")
            continue
        
        if len(face_locations) > 1:
            print(f"  Warning: Multiple faces in {filename}, using first one")
        
        encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(name)
            print(f"  ✓ Successfully encoded {name}")
    
    # Save encodings to file
    if len(known_encodings) > 0:
        os.makedirs(os.path.dirname(config.ENCODINGS_FILE), exist_ok=True)
        
        data = {
            'encodings': known_encodings,
            'names': known_names
        }
        
        with open(config.ENCODINGS_FILE, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"\n✓ Training complete!")
        print(f"  Total faces encoded: {len(known_encodings)}")
        print(f"  Unique persons: {len(set(known_names))}")
        print(f"  Encodings saved to: {config.ENCODINGS_FILE}")
    else:
        print("\nError: No faces were successfully encoded")


if __name__ == '__main__':
    print("=" * 50)
    print("Face Recognition Training Script")
    print("=" * 50)
    train_faces()
