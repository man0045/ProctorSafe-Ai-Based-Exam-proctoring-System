from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import random
import smtplib
import cv2
import base64
from io import BytesIO
from PIL import Image
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
        otp = random.randint(1000, 9999)

        # Capture image from hidden form input
        image_data = request.form['captured_image']
        image_data = image_data.replace("data:image/png;base64,", "")
        image_blob = base64.b64decode(image_data)
        
        # Save user info and OTP in the database
        cursor.execute("INSERT INTO users (username, email, password, otp, image) VALUES (%s, %s, %s, %s, %s)",
                       (username, email, password, otp, image_blob))
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

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
        db_password = cursor.fetchone()
        
        if db_password and db_password[0] == password:
            flash("Login successful!")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
