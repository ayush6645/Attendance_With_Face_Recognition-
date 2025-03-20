import os
import subprocess
from tkinter import *
from tkinter import messagebox

# Directory paths for the scripts
ADD_USER_SCRIPT = "E:/Mini_Project/face-recognition-attendance/scripts/add_user.py"
DELETE_USER_SCRIPT = "E:/Mini_Project/face-recognition-attendance/scripts/delete_user.py"
LIST_USERS_SCRIPT = "E:/Mini_Project/face-recognition-attendance/scripts/list_users.py"  # Assuming this script exists for listing users

def run_script(script_path):
    """Run a Python script."""
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# GUI Functions
def open_add_user():
    """Open the 'Add User' script."""
    run_script(ADD_USER_SCRIPT)

def open_delete_user():
    """Open the 'Delete User' script."""
    run_script(DELETE_USER_SCRIPT)

def open_list_users():
    """Open the 'List Users' script."""
    run_script(LIST_USERS_SCRIPT)

def exit_application():
    """Exit the application."""
    print("Exiting user management system.")
    root.quit()

# GUI Setup
root = Tk()
root.title("User Management - Face Recognition")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Title label
Label(root, text="User Management", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

# Buttons for each function
Button(root, text="Register User", command=open_add_user, bg="green", fg="white", font=("Helvetica", 12), width=20).pack(pady=10)
Button(root, text="Delete User", command=open_delete_user, bg="red", fg="white", font=("Helvetica", 12), width=20).pack(pady=10)
Button(root, text="List Users", command=open_list_users, bg="blue", fg="white", font=("Helvetica", 12), width=20).pack(pady=10)
Button(root, text="Exit", command=exit_application, bg="gray", fg="white", font=("Helvetica", 12), width=20).pack(pady=20)

root.mainloop()
