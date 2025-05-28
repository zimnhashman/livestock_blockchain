from flask import Blueprint, jsonify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

key_bp = Blueprint('key_bp', __name__)

@key_bp.route('/get-aes-key/<animal_id>', methods=['GET'])
def share_key(animal_id):
    key = get_random_bytes(16)  # 128-bit AES key
    encoded = base64.b64encode(key).decode()

    # Store or simulate encrypted key delivery in production
    return jsonify({
        'animal_id': animal_id,
        'aes_key': encoded
    })
