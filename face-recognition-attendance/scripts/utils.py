import yaml
import json
import os
from tensorflow.keras.models import load_model

# Load configuration
def load_config(config_path="config.yaml"):
    """Load the YAML configuration file."""
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

# Load a Keras model
def load_keras_model(model_path):
    """Load a Keras model from the specified path."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return load_model(model_path)

# Save embeddings.json to a JSON file
def save_embeddings(embeddings, file_path):
    """Save embeddings.json to a JSON file."""
    try:
        with open(file_path, "w") as file:
            json.dump(embeddings, file, indent=4)
    except Exception as e:
        print(f"Error saving embeddings.json: {e}")

# Load embeddings.json from a JSON file
def load_embeddings(file_path):
    """Load embeddings.json from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r") as file:
            embeddings = json.load(file)
        return embeddings
    except Exception as e:
        print(f"Error loading embeddings.json: {e}")
        return {}

# Log messages (optional logging utility)
def log_message(message, log_path="outputs/logs/system.log"):
    """Log messages to a log file."""
    try:
        with open(log_path, "a") as log_file:
            log_file.write(f"{message}\n")
    except Exception as e:
        print(f"Error writing log: {e}")
