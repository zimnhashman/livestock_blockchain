from flask import Blueprint, jsonify

status_bp = Blueprint('status', __name__)

@status_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Backend is up and running 🚀"}), 200
