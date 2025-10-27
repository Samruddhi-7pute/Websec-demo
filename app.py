import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import database

try:
    from stegano import lsb
    from PIL import Image
    STEGANO_AVAILABLE = True
except ImportError:
    print("Warning: stegano or Pillow library not found. Installing required packages...")
    import subprocess
    subprocess.check_call(["pip", "install", "stegano", "Pillow"])
    from stegano import lsb
    from PIL import Image
    STEGANO_AVAILABLE = True

ALLOWED_EXT = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB

app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret_for_demo"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
database.init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vulnerable_login", methods=["GET", "POST"])
def vulnerable_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if database.vulnerable_auth_raw(username, password):
            flash("Login successful (vulnerable endpoint).", "success")
            return redirect(url_for("index"))
        else:
            flash("Login failed (vulnerable). Try payload: ' OR '1'='1", "danger")
    return render_template("vulnerable_login.html")

@app.route("/secure_login", methods=["GET", "POST"])
def secure_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if database.verify_user_safe(username, password):
            flash("Login successful (secure). This prevents SQLi and uses password hashing.", "success")
            return redirect(url_for("index"))
        else:
            flash("Login failed (secure).", "danger")
    return render_template("secure_login.html")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/hide", methods=["GET", "POST"])
def hide():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            flash("No selected file", "danger")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Only PNG/JPG/JPEG allowed (PNG recommended).", "danger")
            return redirect(request.url)
        message = request.form.get("message", "").strip()
        if message == "":
            flash("Please provide a message to hide.", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], f"input_{filename}")
        file.save(input_path)

        # Convert to PNG if needed
        if not filename.lower().endswith('.png'):
            img = Image.open(input_path)
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], f"input_{filename.rsplit('.',1)[0]}.png")
            img.save(input_path, 'PNG')

        out_filename = f"stego_{filename.rsplit('.',1)[0]}.png"
        out_path = os.path.join(app.config["UPLOAD_FOLDER"], out_filename)
        
        try:
            # Ensure the image is in the correct format
            if not STEGANO_AVAILABLE:
                raise ImportError("Steganography library not available")
            
            # Hide the message
            secret_image = lsb.hide(input_path, message)
            if secret_image is None:
                raise ValueError("Failed to process image")
                
            secret_image.save(out_path, 'PNG')
        except Exception as e:
            flash(f"Error while hiding message: {str(e)}", "danger")
            return redirect(request.url)

        flash("Message hidden successfully. Download your stego image.", "success")
        return render_template("hide_result.html", stego_filename=out_filename)

    return render_template("hide.html")

@app.route("/reveal", methods=["GET", "POST"])
def reveal():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            flash("No selected file", "danger")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Only PNG/JPG/JPEG allowed.", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], f"reveal_{filename}")
        file.save(path)
        try:
            message = lsb.reveal(path)
        except Exception as e:
            message = None

        if message is None:
            flash("No hidden message found (or unsupported format).", "warning")
            return redirect(request.url)
        return render_template("reveal_result.html", message=message)

    return render_template("reveal.html")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)