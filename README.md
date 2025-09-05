# QR-Code-Attendance-System-
A smart and secure QR Code Attendance system powered by dynamic QR codes. Supports admin dashboard, real-time monitoring, and detailed reports---ideal for classrooms, offices and event check-ins.

## Features
- **Authentication**
  - Admin Login
  - User Access
- **Admin Dashboard**
  - There are three main modules
    1. QR Code Generator
    2. View Attendnace
    3. Generate Reports
- **QR Code Generatorv**
  - QR codes are generated every few seconds
  - Each QR code has a unique token id
  - Prevents proxy attendance
  - QR is displayed on the screen for users to scan directly
- **Attendance Recording**
  - Once scanned, users enter their roll number/ID
  - Submission records timestamp, token ID, and user ID
  - Displays success confirmation to user
  - System blocks duplicate submissions from same device
- **Attendance Logs**
  - Admins can see:
    1. Roll number/Employee ID
    2. Session token
    3. Date & time of entry
- **Report Generation**
  - Automatically calculates:
    - Attendance percentage for each participant
    - Total classes attended vs. missed
    - Status (Present/Absent)
  - Helps admins generate performance insights for individuals and groups.
 
## Tech Stack
- Backend: Python (Flask)
- Database: MySQL
- Frontend: HTML, CSS

## Project Structure
qr-code-attendance/
│── app.py                    # Main Flask application
│── requirements.txt          # Project dependencies
├── templates/                # HTML templates
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── qr_generator.html
│   ├── view_attendance.html
│   ├── generate_reports.html
│   ├── mark_success.html
│   └── mark_duplicate.html
├── static/
│   ├── styles.css
│   └── qrcode.png            # Auto-generated QR image
├── database/                 
└── README.md                 

## Getting Started
### Prerequisites
- Python 3.x
- MySQL Server
- pip

### Installation Steps
```bash
git clone https://github.com/yourusername/qr-code-attendance.git
cd qr-code-attendance
pip install -r requirements.txt
```
1. **Set up database**
   - Create a database and update credentials in `app.py`
3. **Run Flask app**
   `python app.py`
5. **Access the interface**
- Go to http://<YOUR_LOCAL_IP_ADDRESS>:5000 in your browser.
