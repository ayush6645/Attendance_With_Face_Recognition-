import os
import subprocess
import sys

def install_requirements():
    """Automatically install required libraries."""
    try:
        print("Checking and installing required libraries...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All required libraries are installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing libraries: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

# Run this at the beginning of your script
install_requirements()
