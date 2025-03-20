import tkinter as tk
import cv2
from tkinter import messagebox
import requests


class AttendancePanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Panel")

        # Start webcam button
        self.start_btn = tk.Button(root, text="Start Webcam", command=self.start_webcam)
        self.start_btn.pack(pady=10)

    def start_webcam(self):
        # Start real-time webcam feed for face recognition
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                messagebox.showerror("Error", "Failed to grab frame")
                break

            # Process the frame (face recognition code goes here)
            # If face is recognized:
            recognized_name = "John Doe"  # Example name after recognition

            # Mark attendance using backend API
            if recognized_name:
                response = requests.post(f"http://localhost:5000/api/attendance/{recognized_name}")
                if response.status_code == 200:
                    messagebox.showinfo("Success", f"Attendance marked for {recognized_name}")
                else:
                    messagebox.showerror("Error", "Failed to mark attendance")

            cv2.imshow("Attendance Panel", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()


# Create and start the GUI application
root = tk.Tk()
attendance_panel = AttendancePanel(root)
root.mainloop()
