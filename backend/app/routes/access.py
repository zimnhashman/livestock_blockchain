from flask import Blueprint, jsonify
from app.utils.abac import abac_required

access_bp = Blueprint('access', __name__)

@access_bp.route("/access-data", methods=["GET"])
@abac_required("veterinary")  # Can be "regulatory", "analytics", etc.
def access_data():
    # Logic to fetch and return data from storage
    dummy_data = {
        "temperature": "36.7°C",
        "acceleration": "0.02g",
        "timestamp": "2025-05-27T12:00:00Z"
    }
    return jsonify(dummy_data)
