from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import random
import smtplib
import base64
import hashlib

app = Flask(__name__)
app.secret_key = 'ama23n21mcha123'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="man0045chau",
    database="face_auth_db"
)
cursor = db.cursor()

# Helper function for sending OTP via email
def send_otp(email, otp):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mannuchaurasiya36@gmail.com"
    sender_password = "huzcpscgkhnlwhvj"

    message = f"Your OTP for registration is {otp}."
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, email, message)
    server.quit()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        role = request.form['role']  # Get role from the form (e.g., 'teacher' or 'student')
        otp = random.randint(1000, 9999)

        # Capture image from hidden form input
        image_data = request.form['captured_image']
        image_data = image_data.replace("data:image/png;base64,", "")
        image_blob = base64.b64decode(image_data)
        
        # Save user info and OTP in the database
        cursor.execute("INSERT INTO users (username, email, password, role, otp, image) VALUES (%s, %s, %s, %s, %s, %s)",
                       (username, email, password, role, otp, image_blob))
        db.commit()
        
        # Send OTP via email
        send_otp(email, otp)
        flash("OTP sent to your email. Verify to complete registration.")
        return redirect(url_for('verify', email=email))
    return render_template('register.html')

# OTP verification route
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    email = request.args.get('email')
    if request.method == 'POST':
        otp_input = request.form['otp']
        cursor.execute("SELECT otp FROM users WHERE email=%s", (email,))
        db_otp = cursor.fetchone()[0]
        if str(db_otp) == otp_input:
            cursor.execute("UPDATE users SET otp=NULL WHERE email=%s", (email,))
            db.commit()
            flash("Registration successful!")
            return redirect(url_for('login'))
        else:
            flash("Invalid OTP. Please try again.")
    return render_template('verify.html')

# Login route with role-based redirection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        # Retrieve user information along with role
        cursor.execute("SELECT password, role FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        if user and user[0] == password:
            role = user[1]
            session['email'] = email
            session['role'] = role
            
            # Redirect based on role
            if role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif role == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid email or password.")
    return render_template('login.html')

# Teacher dashboard route
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('professor_dashboard.html')
    return redirect(url_for('login'))

# Student dashboard route
@app.route('/student_dashboard')
def student_dashboard():
    if 'role' in session and session['role'] == 'student':
        return render_template('student_dashboard.html')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

@app.route('/')
def index():
    return render_template('index.html', title="Home Page")

@app.route('/faq')
def about():
    return render_template('faq.html', title="Mostly Asked question")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact pages")

if __name__ == '__main__':
    app.run(debug=True)
