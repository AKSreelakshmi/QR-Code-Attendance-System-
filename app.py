from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import pymysql
import qrcode
import os
import time

app = Flask(__name__)

# Admin credentials
admin_username = "admin"
admin_password = "admin123"

# MySQL credentials
host = "localhost"
user = "root"
password = "@Jeme5ovien5#"
database = "college_db"

LOCAL_IP = "192.168.50.132"

if not os.path.exists("static"):
    os.makedirs("static")

def get_mysql_conn():
    return pymysql.connect(host=host, user=user, password=password, db=database)

def init_mysql_tables():
    conn = pymysql.connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    cursor.execute(f"USE {database}")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(100),
            qr_code VARCHAR(255),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

init_mysql_tables()

last_generated_time = 0
QR_CODE_INTERVAL = 24 * 60 * 60  # 24 hours
active_tokens = {}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    passwd = request.form['password']

    if username == admin_username and passwd == admin_password:
        return redirect(url_for('admin_dashboard'))

    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, passwd))
    user = cursor.fetchone()
    conn.close()

    if user:
        return redirect(url_for('user_dashboard'))
    else:
        return "Invalid credentials", 401

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/user')
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route('/admin/qrcode')
def qr_page():
    return render_template("qr_page.html")

@app.route('/qrcode')
def generate_qr():
    global last_generated_time
    current_time = time.time()

    if current_time - last_generated_time < QR_CODE_INTERVAL:
        return send_file("static/qrcode.png", mimetype="image/png")

    last_generated_time = current_time

    # Generate daily QR token based on date
    date_token = time.strftime("%Y%m%d")
    token = f"token_{date_token}"
    qr_url = f"http://{LOCAL_IP}:5000/scan?token={token}"

    active_tokens[token] = current_time

    qr = qrcode.make(qr_url)
    qr.save("static/qrcode.png")

    return send_file("static/qrcode.png", mimetype="image/png")

@app.route('/scan', methods=['GET', 'POST'])
def scan_qr():
    if request.method == 'GET':
        token = request.args.get("token")
        token_time = active_tokens.get(token)

        if not token_time or time.time() - token_time > QR_CODE_INTERVAL:
            return "QR Code expired or invalid.", 403

        return render_template("scan_qr.html", qr_code=token)

    student_id = request.form['student_id']
    qr_code = request.form['qr_code']

    if not qr_code or not student_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_mysql_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM attendance WHERE student_id = %s AND qr_code = %s", (student_id, qr_code))
    existing = c.fetchone()

    if existing:
        conn.close()
        return render_template("already_marked.html", student_id=student_id)

    c.execute("INSERT INTO attendance (student_id, qr_code) VALUES (%s, %s)", (student_id, qr_code))
    conn.commit()
    conn.close()

    return render_template("success.html", student_id=student_id)

@app.route('/admin/attendance')
def view_attendance():
    conn = get_mysql_conn()
    c = conn.cursor()
    c.execute("SELECT student_id, qr_code, timestamp FROM attendance ORDER BY timestamp DESC")
    records = c.fetchall()
    conn.close()
    return render_template("attendance.html", records=records)

@app.route('/admin/report')
def attendance_report():
    conn = get_mysql_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(DISTINCT qr_code) FROM attendance")
    total_classes = c.fetchone()[0] or 0

    c.execute("SELECT student_id, COUNT(*) FROM attendance GROUP BY student_id")
    attendance_counts = c.fetchall()
    conn.close()

    report_data = []
    for student_id, attended in attendance_counts:
        missed = total_classes - attended
        percentage = (attended / total_classes) * 100 if total_classes > 0 else 0
        status = "OK" if percentage >= 75 else "Below 75%"
        report_data.append({
            "student_id": student_id,
            "attended": attended,
            "missed": missed,
            "total": total_classes,
            "percentage": round(percentage, 2),
            "status": status
        })

    return render_template("attendance_report.html", reports=report_data, total_classes=total_classes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
