# Smart Lock System with Face Recognition

ESP32-based smart lock system with Python face recognition module.

## Project Structure

```
Smart Lock System/
├── platformio.ini              # PlatformIO configuration
├── src/main.cpp                # ESP32 firmware (camera + lock control)
├── face_recognition/           # Python face recognition module
│   ├── main.py                 # REST API server
│   ├── config.py               # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   └── utils/                  # Utility modules
├── scripts/                    # Utility scripts
│   ├── train_faces.py          # Train face encodings
│   └── test_recognition.py     # Test the system
└── models/                     # Face data and encodings
    └── known_faces/            # Training images
```

## Setup Instructions

### 1. Python Face Recognition Module

```bash
# Navigate to project directory
cd "Smart Lock System"

# Install Python dependencies
pip install -r face_recognition/requirements.txt

# Add training images (name them as: PersonName_01.jpg, etc.)
# Place images in: models/known_faces/

# Train the model
python scripts/train_faces.py

# Start the face recognition server
python face_recognition/main.py
```

### 2. ESP32 Firmware

```bash
# Build and upload firmware
pio run --target upload

# Monitor serial output
pio device monitor
```

## Usage

### Training New Faces

1. Add photos to `models/known_faces/` directory
   - Name format: `PersonName_01.jpg`, `PersonName_02.jpg`
   - Multiple images per person improve accuracy

2. Run training script:
   ```bash
   python scripts/train_faces.py
   ```

3. Restart the server:
   ```bash
   python face_recognition/main.py
   ```

### Testing

Test with an image:
```bash
python scripts/test_recognition.py --image path/to/test.jpg
```

Test with camera:
```bash
python scripts/test_recognition.py --camera
```

### API Endpoints

- `GET /health` - Check server status
- `POST /recognize` - Recognize face from image
  ```json
  {
    "image": "base64_encoded_image"
  }
  ```
- `POST /add_face` - Add new face
  ```json
  {
    "image": "base64_encoded_image",
    "name": "PersonName"
  }
  ```

## ESP32 Integration

The ESP32 should:
1. Capture image with camera module (OV2640/OV5640)
2. Encode image to base64
3. Send HTTP POST to `/recognize` endpoint
4. Parse JSON response
5. Control lock based on recognition result

## Configuration

Edit `face_recognition/config.py` to adjust:
- Face recognition tolerance (accuracy)
- Server host/port
- Image processing settings
- Security settings

## Requirements

### Python
- Python 3.8+
- OpenCV
- face_recognition
- Flask

### ESP32
- ESP32-CAM or ESP32 with camera module
- WiFi connectivity
- Lock mechanism (servo/solenoid)

## Troubleshooting

**No face detected:**
- Ensure good lighting
- Face should be clearly visible and front-facing
- Adjust RESIZE_FACTOR in config.py

**Low accuracy:**
- Add more training images per person
- Adjust TOLERANCE in config.py (0.4-0.6 recommended)
- Ensure training images have good quality

**Server connection issues:**
- Check firewall settings
- Verify ESP32 and server are on same network
- Check server URL in ESP32 code

## License

MIT License
