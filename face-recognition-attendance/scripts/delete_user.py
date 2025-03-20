import os
import json
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# File paths
DATA_DIR = "E:/Mini_Project/face-recognition-attendance/data/"
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.json")
FACES_DIR = os.path.join(DATA_DIR, "temp_faces")

def load_embeddings():
    """Load face embeddings data."""
    try:
        with open(EMBEDDINGS_FILE, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Embeddings file not found. No users to delete.")
        return []
    except json.JSONDecodeError:
        print("Embeddings file is corrupted.")
        return []

def save_embeddings(data):
    """Save updated embeddings data."""
    with open(EMBEDDINGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print("Embeddings updated successfully.")

def delete_user_from_embeddings(name):
    """Delete a user by name from the embeddings."""
    data = load_embeddings()
    if not data:
        print("No user data available.")
        return False

    updated_data = [entry for entry in data if entry['name'] != name]

    if len(updated_data) == len(data):
        print(f"No user found with the name '{name}'.")
        return False

    save_embeddings(updated_data)
    print(f"User '{name}' removed from embeddings.")
    return True

def delete_user_images(name):
    """Delete all images of the user from the temp_faces directory."""
    if not os.path.exists(FACES_DIR):
        print("Faces directory does not exist. Skipping image deletion.")
        return

    deleted = False
    for file in os.listdir(FACES_DIR):
        if file.startswith(f"{name}_"):
            os.remove(os.path.join(FACES_DIR, file))
            deleted = True

    if deleted:
        print(f"Images for user '{name}' deleted successfully.")
    else:
        print(f"No images found for user '{name}'.")

# GUI Functions
def delete_user_gui():
    """GUI for deleting a user."""
    root = Tk()
    root.title("Delete User - Face Recognition")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    def delete_user():
        """Handle the user deletion."""
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a valid name.")
            return

        # Delete user from embeddings
        user_deleted = delete_user_from_embeddings(name)

        if user_deleted:
            # Optionally delete user's images
            delete_user_images(name)
            messagebox.showinfo("Success", f"User '{name}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"User '{name}' not found.")

    # GUI Layout
    Label(root, text="Delete User", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

    Label(root, text="Enter User Name", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor=W, padx=10)
    name_entry = Entry(root, font=("Helvetica", 12), width=30)
    name_entry.pack(padx=10, pady=5)

    Button(root, text="Delete User", command=delete_user, bg="red", fg="white", font=("Helvetica", 12)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    delete_user_gui()
