import face_recognition
import cv2
import os
import numpy as np
from PIL import Image
import time

def authenticate_face():
    print("📷 Starting facial recognition...")

    # Path to the known face image
    known_face_path = os.path.join(os.path.dirname(__file__), "known_face.jpg")
    if not os.path.exists(known_face_path):
        print("❌ known_face.jpg not found in auth folder.")
        return False

    known_image = cv2.imread(known_face_path)
    if known_image is None:
        print("❌ Failed to load known_face.jpg.")
        return False

    # Ensure the image is in 8-bit unsigned integer format
    if known_image.dtype != np.uint8:
        print("❌ Image is not 8-bit per channel.")
        return False

    known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)

    print(f"[DEBUG] Image shape: {known_image.shape}")
    print(f"[DEBUG] Image dtype: {known_image.dtype}")

    # Encode the known face
    try:
        known_encodings = face_recognition.face_encodings(known_image)
    except Exception as e:
        print("🔥 Exception while encoding known face:", e)
        return False

    if not known_encodings:
        print("❌ No face detected in known image.")
        return False

    known_encoding = known_encodings[0]

    # Start webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("❌ Could not open webcam.")
        return False

    print("🕵️ Please look at the camera... scanning for 10 seconds...")

    match_found = False 
    start_time = time.time()
    scan_duration = 10  # seconds

    while time.time() - start_time < scan_duration:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding in face_encodings:
            matches = face_recognition.compare_faces([known_encoding], encoding)
            if matches[0]:
                match_found = True
                break

        if match_found:
            break

    # Release webcam and close windows
    video_capture.release()
    cv2.destroyAllWindows()

    if match_found:
        print("✅ Face recognized! Access granted.")
        return True
    else:
        print("❌ Face not recognized. Access denied.")
        return False


# This function uses the face_recognition library to authenticate a user based on facial recognition.
# It captures frames from the webcam, compares them with a known face image, and grants access if a match is found.
# Ensure you have a 'known_face.jpg' image in the same directory as this script for testing.
# The function initializes the webcam, captures frames, and checks for a match with the known face encoding.
# Make sure to install the required libraries:
# pip install face_recognition opencv-python
# The function will return True if the face is recognized, otherwise it will return False.