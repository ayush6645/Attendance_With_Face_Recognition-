import os
import json
from tkinter import *
from tkinter import ttk, messagebox

# Directory and file path
DATA_DIR = "E:/Mini_Project/face-recognition-attendance/data/"
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.json")

def list_registered_users_gui():
    """Display registered users in a GUI table with improved aesthetics."""
    root = Tk()
    root.title("Registered Users")
    root.geometry("900x500")
    root.configure(bg="#f4f4f4")

    # Style configuration
    style = ttk.Style()
    style.theme_use("clam")  # Use a modern theme
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#2c3e50", foreground="white")
    style.map("Treeview", background=[("selected", "#3498db")])

    # Header label
    header_label = Label(root, text="Registered Users", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#34495e")
    header_label.pack(pady=10)

    # Frame for Treeview
    frame = Frame(root, bg="#f4f4f4")
    frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # Create the Treeview widget
    tree = ttk.Treeview(frame, columns=(), show="headings", selectmode="browse")
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for Treeview
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Function to load and display users
    def load_users():
        if os.path.exists(EMBEDDINGS_FILE):
            try:
                with open(EMBEDDINGS_FILE, 'r') as file:
                    face_data = json.load(file)

                    if not face_data:
                        messagebox.showinfo("Info", "No users are registered.")
                        return

                    # Get headers and exclude 'embeddings' and 'attendance'
                    headers = list(face_data[0].keys())
                    headers = [header for header in headers if header not in ['embeddings', 'attendance']]

                    # Set headers in the Treeview
                    tree["columns"] = headers
                    for header in headers:
                        tree.heading(header, text=header.capitalize(), anchor="center")
                        tree.column(header, width=120, anchor="center")

                    # Populate rows
                    for user in face_data:
                        row = [user[header] for header in headers]
                        tree.insert("", "end", values=row)

            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error reading the user data from the file. It may be corrupted.")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}")
        else:
            messagebox.showinfo("Info", "No user data found. No users are registered.")

    # Load data when the GUI starts
    load_users()

    # Footer
    footer_label = Label(root, text="Face Recognition Attendance System", font=("Helvetica", 10), bg="#f4f4f4", fg="#7f8c8d")
    footer_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    list_registered_users_gui()
