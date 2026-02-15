# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- PlatformIO (for ESP32 development)
- ESP32 development board (ESP32-CAM recommended)
- Camera module (if not using ESP32-CAM)

## Installation Steps

### 1. Install Python Dependencies

```bash
cd "Smart Lock System"
pip install -r face_recognition/requirements.txt
```

**Note:** On Windows, you may need to install dlib separately:
```bash
pip install cmake
pip install dlib
```

### 2. Prepare Training Data

1. Create a `models/known_faces` directory (already created)
2. Add photos of authorized persons:
   - Name format: `PersonName_01.jpg`, `PersonName_02.jpg`, etc.
   - Add 3-5 images per person
   - See `models/known_faces/README.md` for guidelines

3. Train the model:
   ```bash
   python scripts/train_faces.py
   ```

### 3. Start the Python Server

```bash
python face_recognition/main.py
```

Server will start on `http://localhost:5000`

To test the server:
```bash
# In another terminal
curl http://localhost:5000/health
```

### 4. Configure ESP32

1. Open `src/main.cpp` and update:
   - WiFi SSID and password
   - Server URL (use your computer's IP address)
   
2. Find your computer's IP:
   ```bash
   # Windows
   ipconfig
   # Look for IPv4 Address
   ```

3. Update the `serverUrl` in `main.cpp`:
   ```cpp
   const char* serverUrl = "http://YOUR_IP_ADDRESS:5000/recognize";
   ```

### 5. Upload to ESP32

```bash
pio run --target upload
pio device monitor
```

## Testing

### Test Python Server with Image

```bash
python scripts/test_recognition.py --image path/to/test.jpg
```

### Test with Camera (if you have a webcam)

```bash
python scripts/test_recognition.py --camera
```

### Test ESP32 Integration

1. Press the button connected to GPIO 13
2. Check serial monitor for output
3. Server will log the recognition request

## Workflow

```
1. ESP32 captures image → 
2. Sends to Python server via HTTP → 
3. Server performs face recognition → 
4. Returns result (success/failure, name, confidence) → 
5. ESP32 unlocks door if recognized
```

## Troubleshooting

### Python Server Issues

**"No module named 'face_recognition'":**
```bash
pip install face_recognition
```

**"No face encodings found":**
- Add training images to `models/known_faces/`
- Run `python scripts/train_faces.py`

### ESP32 Issues

**WiFi won't connect:**
- Check SSID and password in `main.cpp`
- Ensure ESP32 is in range

**"HTTP Error: -1":**
- Verify server is running
- Check server URL in code
- Ensure ESP32 and server are on same network

**Camera not working:**
- Uncomment ESP32-CAM configuration in code
- Add camera initialization code (see examples online)

### Recognition Issues

**Low accuracy:**
- Add more training images per person
- Adjust TOLERANCE in `face_recognition/config.py`
- Use better quality images

**"No face detected":**
- Improve lighting
- Position face directly toward camera
- Adjust RESIZE_FACTOR in config

## Next Steps

1. **Add Camera Support:**
   - If using ESP32-CAM, add camera initialization code
   - See ESP32-CAM examples for setup

2. **Add Lock Mechanism:**
   - Connect servo motor or solenoid lock to GPIO 12
   - Update unlock/lock functions in code

3. **Enhance Security:**
   - Add authentication to HTTP endpoints
   - Implement HTTPS
   - Add logging system
   - Add failed attempt tracking

4. **Add Features:**
   - Web dashboard for managing users
   - Mobile app interface
   - Email/SMS notifications
   - Access log database

## Resources

- [ESP32-CAM Getting Started](https://randomnerdtutorials.com/esp32-cam-video-streaming-face-recognition-arduino-ide/)
- [Face Recognition Library](https://github.com/ageitgey/face_recognition)
- [PlatformIO Documentation](https://docs.platformio.org/)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review configuration in `face_recognition/config.py`
3. Check serial monitor output for ESP32
4. Check server logs for Python application
