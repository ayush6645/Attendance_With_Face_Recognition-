import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import json
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import matplotlib.pyplot as plt

# Paths
DATA_DIR = "E:/Mini_Project/face-recognition-attendance/data/"
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")
ADD_USER_SCRIPT = "E:/Mini_Project/face-recognition-attendance/scripts/add_user.py"
DELETE_USER_SCRIPT = "E:/Mini_Project/face-recognition-attendance/scripts/delete_user.py"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"


def authenticate_student(name):
    """Authenticate student by name and face."""
    # Mock-up for face recognition validation
    # Replace this with your face recognition code
    face_recognized = messagebox.askyesno("Face Recognition", f"Is {name}'s face recognized?")
    if face_recognized:
        return True
    else:
        messagebox.showerror("Error", "Face not recognized!")
        return False


def mark_attendance(name):
    """Mark attendance for the student."""
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=["Name", "Time"])

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.concat([df, pd.DataFrame([{"Name": name, "Time": time_now}])], ignore_index=True)
    df.to_csv(ATTENDANCE_FILE, index=False)
    messagebox.showinfo("Attendance", f"Attendance marked for {name} at {time_now}")


def show_visualizations():
    """Display attendance visualizations."""
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        if df.empty:
            messagebox.showinfo("Visualization", "No attendance data to display.")
            return

        attendance_counts = df["Name"].value_counts()
        attendance_counts.plot(kind="bar", title="Attendance Records")
        plt.ylabel("Number of Attendances")
        plt.xlabel("Student Name")
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Error", "Attendance file not found.")


def student_interface():
    """Student functionalities."""
    student_window = tk.Toplevel(root)
    student_window.title("Student Interface")
    student_window.geometry("400x300")
    student_window.configure(bg="#f0f0f0")

    tk.Label(student_window, text="Student Dashboard", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)
    tk.Button(student_window, text="Proceed as Student", command=proceed_as_student, bg="blue", fg="white", width=20,
              height=2).pack(pady=10)


def proceed_as_student():
    """Handle student attendance flow."""
    name = simpledialog.askstring("Student Login", "Enter your name:")
    if name:
        if authenticate_student(name):
            action = messagebox.askyesno("Action", "Do you want to mark attendance?")
            if action:
                mark_attendance(name)
            show_visualizations()


def admin_interface():
    """Admin functionalities."""
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Interface")
    admin_window.geometry("400x300")
    admin_window.configure(bg="#f0f0f0")

    tk.Label(admin_window, text="Admin Dashboard", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)
    tk.Button(admin_window, text="Add User", command=add_user, bg="green", fg="white", width=20, height=2).pack(pady=10)
    tk.Button(admin_window, text="Delete User", command=delete_user, bg="red", fg="white", width=20, height=2).pack(pady=10)
    tk.Button(admin_window, text="List All Users", command=list_users, bg="blue", fg="white", width=20, height=2).pack(pady=10)
    tk.Button(admin_window, text="Find User", command=find_user, bg="orange", fg="white", width=20, height=2).pack(pady=10)



def add_user():
    """Run add_user script."""
    subprocess.run(["python", ADD_USER_SCRIPT])


def delete_user():
    """Run delete_user script."""
    subprocess.run(["python", DELETE_USER_SCRIPT])


def list_users():
    """Run the list_users script to display registered users."""
    LIST_USERS_SCRIPT = "E:/Mini_Project/face-recognition-attendance/scripts/list_users.py"
    try:
        subprocess.run(["python", LIST_USERS_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the script:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")



def find_user():
    """Find a specific user by name."""
    name = simpledialog.askstring("Find User", "Enter the name of the user:")
    if name:
        try:
            with open(EMBEDDINGS_FILE, 'r') as file:
                face_data = json.load(file)
                user = next((user for user in face_data if user["name"] == name), None)
                if user:
                    user_info = {key: value for key, value in user.items() if key not in ["embeddings", "attendance"]}
                    messagebox.showinfo("User Found", f"Details:\n{json.dumps(user_info, indent=4)}")
                else:
                    messagebox.showerror("Error", f"No user found with the name {name}.")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "No user data available.")


def admin_login():
    """Authenticate admin credentials."""
    username = simpledialog.askstring("Admin Login", "Enter username:")
    password = simpledialog.askstring("Admin Login", "Enter password:", show="*")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        admin_interface()
    else:
        messagebox.showerror("Error", "Invalid credentials!")


# Main window
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Welcome to Attendance System", font=("Helvetica", 18), bg="#f0f0f0").pack(pady=20)
tk.Button(root, text="Student", command=student_interface, bg="blue", fg="white", width=20, height=2).pack(pady=10)
tk.Button(root, text="Admin", command=admin_login, bg="green", fg="white", width=20, height=2).pack(pady=10)

root.mainloop()
