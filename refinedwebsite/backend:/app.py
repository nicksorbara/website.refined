from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid  # For generating unique file names
from werkzeug.utils import secure_filename  # To handle filenames safely

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload."""
    print("Upload endpoint hit.")
    
    if "file" not in request.files:
        print("No file part in the request.")
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        print("Empty filename.")
        return jsonify({"message": "No file selected"}), 400

    if not allowed_file(file.filename):
        print(f"Invalid file type: {file.filename}")
        return jsonify({"message": "Invalid file type"}), 400

    # Secure and generate a unique filename
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        # Save the file to the server
        file.save(file_path)
        print(f"File saved as: {file_path}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return jsonify({"message": "Failed to save the file."}), 500

    return jsonify({
        "message": f"File uploaded successfully as {unique_filename}",
        "file_url": f"/uploads/{unique_filename}"
    }), 200

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
