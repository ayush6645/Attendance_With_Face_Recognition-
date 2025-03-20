import os
import cv2
import face_recognition
import numpy as np
import json
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk

# Directory paths
DATA_DIR = "E:/Mini_Project/face-recognition-attendance/data/"
FACES_DIR = os.path.join(DATA_DIR, "temp_faces")
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.json")

# Ensure directories exist
os.makedirs(FACES_DIR, exist_ok=True)

# Function to save face data and user information
def save_face_data(user_data, embeddings):
    """Save the embeddings and user information to a JSON file."""
    face_data = []

    # Load existing embeddings if file exists
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "r") as f:
            try:
                face_data = json.load(f)
            except json.JSONDecodeError:
                print("No existing data found, starting fresh.")

    # Add the new data
    face_data.append({
        "name": user_data["name"],
        "faculty_or_student": user_data["faculty_or_student"],
        "branch": user_data["branch"],
        "year": user_data["year"],
        "roll_no": user_data["roll_no"],
        "mob": user_data["mob"],
        "datetime_added": user_data["datetime_added"],
        "embeddings": embeddings.tolist()
    })

    # Save updated data back to the file
    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump(face_data, f, indent=4)

# Function to extract face embeddings
def compute_embedding(frame):
    """Detect faces and compute their embeddings."""
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) != 1:
        return None, face_locations

    # Compute face encoding
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    if len(face_encodings) == 1:
        return face_encodings[0], face_locations
    return None, face_locations

# GUI Functionality
def add_user_gui():
    root = Tk()
    root.title("Add User - Face Recognition")
    root.geometry("500x600")
    root.configure(bg="#f4f4f4")

    # Style configuration
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 12), background="#2c3e50", foreground="white")
    style.map("TButton", background=[("active", "#3498db")])

    def start_capture():
        user_data = {
            "name": name_entry.get().strip().replace(" ", "_"),
            "faculty_or_student": member_type_var.get(),
            "branch": branch_entry.get().strip(),
            "year": year_entry.get().strip(),
            "roll_no": roll_no_entry.get().strip(),
            "mob": mobile_entry.get().strip(),
            "datetime_added": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        if not all(user_data.values()):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        video_capture = cv2.VideoCapture(0)
        captured_embeddings = []

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Detect faces
            embedding, face_locations = compute_embedding(frame)

            # Draw rectangles around faces
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow("Capture Face - Press 'c' to Capture, 'q' to Quit", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):  # Capture face data
                if embedding is not None and len(face_locations) == 1:
                    captured_embeddings.append(embedding)
                    image_path = os.path.join(FACES_DIR, f"{user_data['name']}_face_{len(captured_embeddings)}.jpg")
                    cv2.imwrite(image_path, frame)
                    messagebox.showinfo("Info", f"Face captured and saved as {image_path}.")
                else:
                    messagebox.showwarning("Warning", "Please ensure only one face is visible.")

            elif key == ord('q'):  # Quit the loop
                video_capture.release()
                cv2.destroyAllWindows()
                if captured_embeddings:
                    avg_embedding = np.mean(captured_embeddings, axis=0)
                    save_face_data(user_data, avg_embedding)
                    messagebox.showinfo("Success", f"Data saved for {user_data['name']}.")
                else:
                    messagebox.showwarning("Warning", "No valid face captured.")
                break

    # GUI Layout
    Label(root, text="Add User Information", font=("Helvetica", 16, "bold"), bg="#f4f4f4", fg="#34495e").pack(pady=10)

    Label(root, text="Name", font=("Arial", 12), bg="#f4f4f4").pack(anchor=W, padx=20, pady=2)
    name_entry = Entry(root, width=30, font=("Arial", 12))
    name_entry.pack(padx=20, pady=5)

    Label(root, text="Member Type", font=("Arial", 12), bg="#f4f4f4").pack(anchor=W, padx=20, pady=2)
    member_type_var = StringVar(value="Student")
    ttk.Combobox(root, textvariable=member_type_var, values=["Faculty", "Student"], state="readonly", font=("Arial", 12)).pack(padx=20, pady=5)

    Label(root, text="Branch", font=("Arial", 12), bg="#f4f4f4").pack(anchor=W, padx=20, pady=2)
    branch_entry = Entry(root, width=30, font=("Arial", 12))
    branch_entry.pack(padx=20, pady=5)

    Label(root, text="Year", font=("Arial", 12), bg="#f4f4f4").pack(anchor=W, padx=20, pady=2)
    year_entry = Entry(root, width=30, font=("Arial", 12))
    year_entry.pack(padx=20, pady=5)

    Label(root, text="Roll No", font=("Arial", 12), bg="#f4f4f4").pack(anchor=W, padx=20, pady=2)
    roll_no_entry = Entry(root, width=30, font=("Arial", 12))
    roll_no_entry.pack(padx=20, pady=5)

    Label(root, text="Mobile Number", font=("Arial", 12), bg="#f4f4f4").pack(anchor=W, padx=20, pady=2)
    mobile_entry = Entry(root, width=30, font=("Arial", 12))
    mobile_entry.pack(padx=20, pady=5)

    ttk.Button(root, text="Capture Face Data", command=start_capture).pack(pady=20)

    footer_label = Label(root, text="Face Recognition Attendance System", font=("Helvetica", 10), bg="#f4f4f4", fg="#7f8c8d")
    footer_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    add_user_gui()
