from flask import Blueprint, request, jsonify
import os
import csv
from app.utils.encryption import generate_aes_key, encrypt_data
from app.utils.signature import generate_rsa_keypair, sign_message
import base64

csv_upload_bp = Blueprint('csv_upload', __name__)
UPLOAD_FOLDER = 'uploads'

@csv_upload_bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Parse the CSV
    parsed_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parsed_data.append({
                "animal_id": row.get("animal_id"),
                "temperature": row.get("temperature"),
                "acceleration": row.get("acceleration"),
                "timestamp": row.get("timestamp"),
                "location": row.get("location")
            })

    # Encrypt each parsed row using AES
    aes_key = generate_aes_key()  # Normally created by gateway
    encrypted_data = []
    for row in parsed_data:
        plaintext = f"{row['animal_id']},{row['temperature']},{row['acceleration']},{row['timestamp']},{row['location']}"
        encrypted = encrypt_data(plaintext, aes_key)
        encrypted_data.append({
            "iv": encrypted["iv"],
            "ciphertext": encrypted["ciphertext"]
        })

    return jsonify({
        "message": "CSV uploaded, parsed and encrypted successfully",
        "encrypted_data": encrypted_data
    }), 200
