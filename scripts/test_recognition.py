"""
Test the face recognition system with a local image or camera
"""

import os
import sys
import cv2
import base64
import requests
import argparse

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from face_recognition import config


def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')


def test_with_image(image_path, server_url='http://localhost:5000'):
    """Test face recognition with an image file"""
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return
    
    print(f"Testing with image: {image_path}")
    
    # Encode image
    encoded_image = encode_image(image_path)
    
    # Send request to server
    response = requests.post(
        f"{server_url}/recognize",
        json={'image': encoded_image}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 50)
        print("Recognition Result:")
        print("=" * 50)
        print(f"Success: {result['success']}")
        print(f"Name: {result.get('name', 'Unknown')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Timestamp: {result.get('timestamp', 'N/A')}")
        print("=" * 50)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def test_with_camera(server_url='http://localhost:5000'):
    """Test face recognition with live camera feed"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Press SPACE to capture and test, ESC to exit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Camera - Press SPACE to test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            # Encode frame
            _, buffer = cv2.imencode('.jpg', frame)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            
            # Send to server
            print("\nSending image to server...")
            response = requests.post(
                f"{server_url}/recognize",
                json={'image': encoded_image}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Result: {result.get('name', 'Unknown')} "
                      f"(Confidence: {result.get('confidence', 0):.2%})")
            else:
                print(f"Error: {response.status_code}")
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test face recognition system')
    parser.add_argument('-i', '--image', help='Path to test image')
    parser.add_argument('-c', '--camera', action='store_true', help='Use camera')
    parser.add_argument('-s', '--server', default='http://localhost:5000', 
                       help='Server URL (default: http://localhost:5000)')
    
    args = parser.parse_args()
    
    # Check if server is running
    try:
        response = requests.get(f"{args.server}/health")
        print(f"Server status: {response.json()}")
    except:
        print(f"Error: Could not connect to server at {args.server}")
        print("Make sure the server is running (python face_recognition/main.py)")
        sys.exit(1)
    
    if args.image:
        test_with_image(args.image, args.server)
    elif args.camera:
        test_with_camera(args.server)
    else:
        print("Please specify either --image or --camera")
        parser.print_help()
