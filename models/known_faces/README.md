# Known Faces Directory

Place training images in this directory to train the face recognition system.

## Image Naming Convention

Name your images using the format: `PersonName_XX.jpg`

Examples:
- `John_01.jpg`
- `John_02.jpg`
- `Sarah_01.jpg`
- `Sarah_02.jpg`
- `Alice_01.jpg`

## Best Practices

### Image Quality
- Use clear, well-lit photos
- Face should be front-facing
- Avoid extreme angles or occlusions
- Resolution: At least 640x480 pixels
- Format: JPG, JPEG, or PNG

### Multiple Images Per Person
- Add 3-5 images per person for better accuracy
- Use different:
  - Lighting conditions
  - Facial expressions
  - Slight angle variations
  - With/without glasses (if applicable)

### Do's and Don'ts

✓ **DO:**
- Use high-quality images
- Ensure good lighting
- Keep faces clearly visible
- Use recent photos
- Include variations (with/without glasses, different expressions)

✗ **DON'T:**
- Use blurry or low-resolution images
- Include multiple people in one training image
- Use images with heavy filters or editing
- Use images where face is partially covered
- Use group photos

## After Adding Images

Once you've added your training images, run:

```bash
python scripts/train_faces.py
```

This will process all images and create the face encodings file needed for recognition.

## Example Directory Structure

```
known_faces/
├── John_01.jpg
├── John_02.jpg
├── John_03.jpg
├── Sarah_01.jpg
├── Sarah_02.jpg
├── Alice_01.jpg
└── Alice_02.jpg
```

## Training Output

After training, you'll see:
- `models/face_encodings.pkl` - The trained model file
- Console output showing how many faces were encoded

## Troubleshooting

**"No face detected" error:**
- Ensure face is clearly visible and well-lit
- Try a different photo with better quality
- Face should be front-facing

**"Multiple faces detected" warning:**
- Each training image should contain only ONE person
- Crop the image to show only the person you want to train

**Low recognition accuracy:**
- Add more training images (3-5 per person minimum)
- Use images with varying conditions
- Ensure training images are high quality
