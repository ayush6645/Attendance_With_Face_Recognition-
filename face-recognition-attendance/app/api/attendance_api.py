from flask import Flask, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Sample attendance data (in practice, you might use a database)
ATTENDANCE_FILE = "E:/Mini_Project/face-recognition-attendance/data/attendance.csv"


@app.route('/api/attendance/<string:name>', methods=['POST'])
def mark_attendance(name):
    """Mark attendance for the given user."""
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Append the attendance data to the CSV file
    with open(ATTENDANCE_FILE, 'a') as file:
        file.write(f"{name},{time_now}\n")

    return jsonify({"message": f"Attendance marked for {name}"}), 200


if __name__ == "__main__":
    app.run(debug=True)
