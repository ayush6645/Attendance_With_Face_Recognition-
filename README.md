# **Face Recognition Attendance System**

A robust and intuitive system for managing attendance using face recognition technology. Designed for both students and administrators, this application leverages modern Python libraries and machine learning techniques to ensure a seamless experience.

---

## **Features**

### 🎓 **Student Dashboard**
- Authenticate using face recognition.
- Mark attendance securely with a timestamp.
- Visualize attendance records with clear and interactive charts.

### 🛠️ **Admin Dashboard**
- **Add User:** Register new users into the system.
- **Delete User:** Remove users from the system along with their data.
- **List All Users:** View a complete list of registered users.
- **Find User:** Retrieve details of a specific user by name.
- Manage attendance records efficiently.

---

## **Getting Started**

### **Prerequisites**
Ensure you have the following installed:
- Python 3.8 or higher
- `pip` (Python package manager)

### **Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/face-recognition-attendance.git
   cd face-recognition-attendance

### **Install the required dependencies:**
   ```bash
python -m pip install -r requirements.txt
```

### **Run the application:**
   ```bash
python main.py
   ```
## How It Works

### Student Workflow
- **Log in:** Enter your name for identification.
- **Face Recognition:** The system verifies your face.
- **Attendance:** If verified, your attendance is marked with the current date and time.

### Admin Workflow
- **Log in:** Authenticate with the admin username and password.
- **Manage Users:** Add, delete, or list registered users.
- **Attendance Records:** Access attendance visualizations and manage attendance files.

## **Folder Structure**
# Directory Structure

```html
face-recognition-attendance/
│
├── data/  
│   ├── embeddings.json       # Stores face embeddings and user data  
│   ├── attendance.csv        # Records attendance data  
│
├── scripts/  
│   ├── add_user.py           # Script to add a user  
│   ├── delete_user.py        # Script to delete a user  
│   ├── list_users.py         # Script to list all users  
│
├── main.py                   # Main application file  
├── requirements.txt          # Project dependencies  
└── README.md                 # Project documentation
```
# Usage

## Admin Login
- **Username**: admin
- **Password**: password

## Visualizations
- **Bar Charts**: Display the number of attendances for each user.
- **Tabulated Records**: View attendance in a tabular format.

# Dependencies

The project uses the following Python libraries:

- **Face Recognition**: OpenCV and scikit-learn
- **Data Handling**: pandas and numpy
- **Visualization**: matplotlib and tabulate
- **GUI Development**: tkinter
- **Image Processing**: Pillow


# Contributing

We welcome contributions to improve the system!  
To contribute:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add a descriptive message"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

# License

This project is licensed under the MIT License.

# Acknowledgments

- Built with ❤️ using Python and cutting-edge libraries.
- Inspired by real-world challenges in attendance management.

# Contact

For any inquiries or support, reach out to:  
📧 gyangupta6645@gmail.com
