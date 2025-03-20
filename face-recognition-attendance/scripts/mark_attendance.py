import os
import cv2
import face_recognition
import dlib
import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
import subprocess
import re
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Directory paths
DATA_DIR = "E:/Mini_Project/face-recognition-attendance/data/"
FACES_DIR = os.path.join(DATA_DIR, "temp_faces")
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")

# Define the expected network SSID (for testing, set as "Ayush")
EXPECTED_SSID = "Ayush"

# Function to get the SSID of the currently connected Wi-Fi network
def get_connected_ssid():
    """Get the SSID of the currently connected Wi-Fi network."""
    try:
        # For Windows, use `netsh wlan show interfaces`
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode(errors="ignore")
        ssid_match = re.search(r"SSID\s*:\s*(.+)", result)
        if ssid_match:
            return ssid_match.group(1).strip()
    except Exception as e:
        print(f"Error fetching Wi-Fi SSID: {e}")
    return None

# Function to validate the network connection
def validate_network():
    """Check if the device is connected to the expected network."""
    connected_ssid = get_connected_ssid()
    if connected_ssid:
        if connected_ssid == EXPECTED_SSID:
            print(f"Network validation successful! Connected to '{connected_ssid}'.")
            return True
        else:
            print(f"Connected to '{connected_ssid}', but expected '{EXPECTED_SSID}'.")
    else:
        print("Not connected to any Wi-Fi network.")
    return False

# Load existing face embeddings data
def load_face_data():
    """Load the face embeddings and names from the embeddings file."""
    try:
        with open(EMBEDDINGS_FILE, 'r') as f:
            face_data = json.load(f)
        return face_data
    except (FileNotFoundError, json.JSONDecodeError):
        print("No existing face data found.")
        return []


# Initialize attendance file if it doesn't exist or is empty
def initialize_attendance_file():
    """Ensure the attendance file has proper headers."""
    if not os.path.exists(ATTENDANCE_FILE) or os.path.getsize(ATTENDANCE_FILE) == 0:
        df = pd.DataFrame(columns=["Name", "Time"])
        df.to_csv(ATTENDANCE_FILE, index=False)
        print("Initialized attendance file with headers.")


# Mark attendance by storing the name and time of detection
def mark_attendance(name):
    """Mark the attendance in the CSV file."""
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if attendance file exists, if not create it
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=["Name", "Time"])

    # Check if the person has already marked attendance within the last 1 hour
    last_attendance = df[df["Name"] == name]["Time"]
    if not last_attendance.empty:
        last_time = datetime.strptime(last_attendance.iloc[0], '%Y-%m-%d %H:%M:%S')
        if datetime.now() - last_time < timedelta(hours=1):
            print(f"{name} has already marked attendance within the last hour.")
            return  # Skip marking attendance

    # Mark attendance in the DataFrame
    df = pd.concat([df, pd.DataFrame([{"Name": name, "Time": time_now}])], ignore_index=True)

    # Save the DataFrame to CSV
    df.to_csv(ATTENDANCE_FILE, index=False)
    print(f"Attendance marked for {name} at {time_now}.")


def recognize_face(frame, face_locations, face_encodings, face_data):
    """Recognize the face in the frame and return the matching name."""
    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        distances = []
        # Compare the current face encoding with stored face embeddings
        for data in face_data:
            stored_embeddings = np.array(data['embeddings'])
            distance = np.linalg.norm(stored_embeddings - encoding)
            distances.append(distance)

        # Find the minimum distance and check if it's a match
        min_distance = min(distances)

        # Define a dynamic or stricter threshold for recognizing faces
        threshold = 0.55  # Lowering this threshold for stricter matching
        if min_distance < threshold:  # Threshold for matching faces
            matched_name = face_data[distances.index(min_distance)]["name"]
            return matched_name
        else:
            print(f"Face distance too high ({min_distance:.2f}) - not recognized as a match.")
            return None

    return None


# Detect blinking for liveness verification
def detect_blinking(landmarks):
    """Detect blinking based on eye landmarks."""
    def eye_aspect_ratio(eye):
        # Calculate the EAR (Eye Aspect Ratio)
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        return (A + B) / (2.0 * C)

    left_eye = landmarks[36:42]  # Left eye indices
    right_eye = landmarks[42:48]  # Right eye indices

    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)

    return (left_ear + right_ear) / 2.0  # Average EAR


# GUI for displaying network status and attendance
def gui_main():
    root = Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("500x400")

    status_label = Label(root, text="Waiting for connection to Wi-Fi", font=("Helvetica", 14))
    status_label.pack(pady=20)

    def check_network_status():
        if validate_network():
            status_label.config(text="Network Validation: Successful!", fg="green")
        else:
            status_label.config(text="Network Validation Failed", fg="red")

    def start_attendance_process():
        # Start the main face recognition and attendance process
        status_label.config(text="Checking Wi-Fi Connection...", fg="orange")
        root.after(1000, check_network_status)  # Wait 1 second and check network again

        video_capture = cv2.VideoCapture(0)

        # Load dlib's pre-trained face landmarks detector
        predictor_path = "E:\\Mini_Project\\face-recognition-attendance\\data\\shape_predictor_68_face_landmarks.dat\\shape_predictor_68_face_landmarks.dat"  # Ensure this file is downloaded
        face_detector = dlib.get_frontal_face_detector()
        landmark_predictor = dlib.shape_predictor(predictor_path)

        # Load face data (embeddings and names)
        face_data = load_face_data()

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab frame.")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces using dlib
            faces = face_detector(gray_frame)

            if len(faces) == 0:
                print("No face detected.")
            elif len(faces) > 1:
                print("Multiple faces detected! Ensure only one person is in the frame.")
                cv2.putText(frame, "Multiple faces detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                face = faces[0]
                landmarks = landmark_predictor(gray_frame, face)
                face_landmarks = np.array([[p.x, p.y] for p in landmarks.parts()])

                # Detect blinking to confirm liveness
                ear = detect_blinking(face_landmarks)
                if ear < 0.25:  # Blinking threshold
                    print("Blink detected. Liveness confirmed.")

                    # Recognize face and mark attendance
                    face_encodings = face_recognition.face_encodings(frame, [(face.top(), face.right(), face.bottom(), face.left())])
                    if face_encodings:
                        name = recognize_face(frame, [(face.top(), face.right(), face.bottom(), face.left())], face_encodings, face_data)
                        if name:
                            mark_attendance(name)
                        else:
                            print("Face not recognized!")
                else:
                    print("No blink detected. Liveness failed.")

            # Display the resulting image
            cv2.imshow('Attendance System', frame)

            # Press 'q' to quit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    Button(root, text="Start Attendance Process", command=start_attendance_process, bg="blue", fg="white", font=("Helvetica", 14)).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    gui_main()
