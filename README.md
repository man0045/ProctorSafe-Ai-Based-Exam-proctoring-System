# ProctorSafe:Ai-Based-Exam-proctoring-System
an AI based proctoring system by using AI-based technologies and to normalise and improve the quality of examination

# Running the Application

Follow these steps to set up and run the application using a requirements file.

## Step 1: Install Dependencies

First, make sure you have the necessary packages installed. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt

## Requirements for Login and Signup using MySQL

### Prerequisites
- MySQL Server

### Database Setup
Run the following commands to set up your database and users table:

```sql
CREATE DATABASE face_auth_db;
USE face_auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    otp INT,
    image LONGBLOB
);

ADjust your SMTP server password

Feel free to adjust the headings or content as needed. Just copy and paste this into your README file, and it should be clear and easy to understand!
