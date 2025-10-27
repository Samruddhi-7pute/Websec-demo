# Cybersecurity Demonstration Project

A small Flask web app demoing:
- SQL Injection (vulnerable login)
- SQL Injection Prevention (secure login with parameterized queries + hashed passwords)
- Steganography (hide/reveal short messages in images)

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
