import face_recognition
import cv2
import numpy as np
import os
import time
from colorama import Fore

def authenticate_face():
    try:
        # Load known face
        known_face_path = os.path.join(os.path.dirname(__file__), "known_face.jpg")
        if not os.path.exists(known_face_path):
            print(f"{Fore.RED}❌ No known face image found at {known_face_path}")
            return False

        known_image = face_recognition.load_image_file(known_face_path)
        known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)

        try:
            known_encodings = face_recognition.face_encodings(known_image)
            if not known_encodings:
                print(f"{Fore.RED}❌ No face detected in the reference image.")
                return False
        except Exception as e:
            print(f"{Fore.RED}❌ Exception while encoding known face: {e}")
            return False

        known_encoding = known_encodings[0]

        # Start webcam
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print(f"{Fore.RED}❌ Could not access the webcam.")
            return False

        print(f"{Fore.YELLOW}📷 Scanning... Please look at the camera.")
        time.sleep(1.5)

        result = False
        timeout = time.time() + 10  # 10-second timeout

        while time.time() < timeout:
            ret, frame = video_capture.read()
            if not ret:
                print(f"{Fore.RED}⚠️ Failed to read from camera.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                match = face_recognition.compare_faces([known_encoding], face_encoding)[0]
                if match:
                    result = True
                    break

            if result:
                break

        video_capture.release()
        cv2.destroyAllWindows()

        if result:
            print(f"{Fore.GREEN}✅ Face match successful.")
        else:
            print(f"{Fore.RED}❌ Face not recognized or timeout reached.")

        return result

    except Exception as error:
        print(f"{Fore.RED}❌ Unexpected error during facial authentication: {error}")
        return False




# This function uses the face_recognition library to authenticate a user based on facial recognition.
# It captures frames from the webcam, compares them with a known face image, and grants access if a match is found.
# Ensure you have a 'known_face.jpg' image in the same directory as this script for testing.
# The function initializes the webcam, captures frames, and checks for a match with the known face encoding.
# Make sure to install the required libraries:
# pip install face_recognition opencv-python
# The function will return True if the face is recognized, otherwise it will return False.