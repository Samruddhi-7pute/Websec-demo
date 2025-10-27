# Webapp Security Demonstration Project

A small Flask web app demoing:
- SQL Injection (vulnerable login)
- SQL Injection Prevention (secure login with parameterized queries + hashed passwords)
- Steganography (hide/reveal short messages in images)

## Project Description

This compact Flask web application is designed for hands-on learning. It demonstrates SQL Injection via an intentionally vulnerable login, how to prevent it using secure coding practices (parameterized queries and hashed passwords), and simple image steganography techniques for hiding and revealing short messages. The project allows learners to see insecure and secure implementations side-by-side.  

## 🔹 Features
1. **SQL Injection (Vulnerable Login)**  
   - Shows how attackers exploit unsafe SQL queries.

2. **SQL Injection Prevention (Secure Login)**  
   - Uses parameterized queries + hashed passwords.

3. **Steganography**  
   - Users can upload an image and hide/reveal secret messages.

## ⚙️ Setup (local)
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt

# initialize demo DB (creates example users)
python init_db.py

# run app
python app.py
# or
# set FLASK_APP=app.py
# flask run
