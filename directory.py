import os

# Define the directory structure
structure = {
    "data": ["embeddings.json"],
    "models": [],
    "scripts": ["add_user.py", "delete_user.py", "mark_attendance.py", "liveness_detection.py", "utils.py"],
    "attendance": ["attendance_log.csv"],
    "app/gui": ["admin_panel.py", "attendance_panel.py", "__init__.py"],
    "app/api": ["attendance_api.py", "user_api.py"],
    "notebooks": ["explore_data.ipynb", "model_training.ipynb"],
    "outputs/logs": [],
}

# Create directories and files
base_path = "face-recognition-attendance"
for folder, files in structure.items():
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    for file in files:
        open(os.path.join(folder_path, file), "w").close()  # Create empty files

# Create root-level files
root_files = ["config.yaml", "README.md", "requirements.txt", ".gitignore", "main_gui.py"]
for file in root_files:
    open(os.path.join(base_path, file), "w").close()

print(f"Project structure created at {os.path.abspath(base_path)}")
