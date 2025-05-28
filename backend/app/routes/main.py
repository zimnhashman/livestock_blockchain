from flask import Blueprint, jsonify
from app.utils.access_control import access_required

main_bp = Blueprint("main", __name__)

@main_bp.route("/status")
@access_required("/status")
def status():
    return jsonify({"message": "API is live"})

@main_bp.route("/upload")
@access_required("/upload")
def upload():
    return jsonify({"message": "Upload successful"})
