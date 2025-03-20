from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Sample user data (in practice, you might use a database)
USER_DATA_FILE = "E:/Mini_Project/face-recognition-attendance/data/embeddings.json"


@app.route('/api/users', methods=['GET'])
def get_users():
    """Fetch all users."""
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
        return jsonify(users), 200
    except FileNotFoundError:
        return jsonify({"error": "No users found"}), 404


@app.route('/api/users', methods=['POST'])
def add_user():
    """Add a new user."""
    user_data = request.get_json()
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    users.append(user_data)

    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

    return jsonify({"message": "User added successfully"}), 201


@app.route('/api/users/<string:roll_number>', methods=['DELETE'])
def delete_user(roll_number):
    """Delete a user by roll number."""
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "No users found"}), 404

    users = [user for user in users if user['roll_number'] != roll_number]

    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
