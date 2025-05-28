from flask import Blueprint, request, jsonify
from app.utils.access_control import check_access

sensor_bp = Blueprint('sensor', __name__)

# Route to upload sensor data without login
@sensor_bp.route('/sensor/upload', methods=['POST'])
def upload_sensor_data():
    data = request.json
    # Simulate saving data...
    print("Sensor data uploaded:", data)
    return jsonify({"message": "Sensor data received"}), 201

# Route to get data with ABAC check
@sensor_bp.route('/sensor/data', methods=['GET'])
def get_sensor_data():
    user_attrs = request.args.to_dict()
    if not check_access(user_attrs):
        return jsonify({"error": "Access denied"}), 403

    # Simulate data access
    return jsonify({"data": "Sensor data visible"}), 200
