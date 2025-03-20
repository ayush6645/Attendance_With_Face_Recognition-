import tkinter as tk
from tkinter import messagebox
import requests


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")

        # Add user button
        self.add_user_btn = tk.Button(root, text="Add User", command=self.add_user)
        self.add_user_btn.pack(pady=10)

        # Delete user button
        self.delete_user_btn = tk.Button(root, text="Delete User", command=self.delete_user)
        self.delete_user_btn.pack(pady=10)

        # List users button
        self.list_users_btn = tk.Button(root, text="List Users", command=self.list_users)
        self.list_users_btn.pack(pady=10)

    def add_user(self):
        # Add user functionality (invoke API)
        user_data = {
            'name': 'John Doe',
            'branch': 'Computer Science',
            'roll_number': 'CS12345',
            'email': 'johndoe@example.com',
            'phone': '1234567890'
        }
        response = requests.post("http://localhost:5000/api/users", json=user_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "User added successfully")
        else:
            messagebox.showerror("Error", "Failed to add user")

    def delete_user(self):
        # Delete user functionality (invoke API)
        user_id = 'CS12345'  # Example, ideally would be inputted
        response = requests.delete(f"http://localhost:5000/api/users/{user_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "User deleted successfully")
        else:
            messagebox.showerror("Error", "Failed to delete user")

    def list_users(self):
        # List all users functionality (invoke API)
        response = requests.get("http://localhost:5000/api/users")
        if response.status_code == 200:
            users = response.json()
            users_list = "\n".join([f"{user['name']} - {user['roll_number']}" for user in users])
            messagebox.showinfo("Users List", users_list)
        else:
            messagebox.showerror("Error", "Failed to fetch users")


# Create and start the GUI application
root = tk.Tk()
admin_panel = AdminPanel(root)
root.mainloop()
