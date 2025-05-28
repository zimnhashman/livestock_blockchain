from functools import wraps
from flask import request, jsonify
import datetime

# Example access rules (can later come from DB or config)
ACCESS_RULES = {
    "veterinary": {"locations": ["FarmA", "FarmB"], "time_window_hours": 48},
    "regulatory": {"locations": ["*"], "time_window_hours": 72},
}

def abac_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = request.headers.get("X-Role")
            location = request.headers.get("X-Location")
            upload_time_str = request.headers.get("X-Upload-Time")

            if role != required_role:
                return jsonify({"error": "Unauthorized role"}), 403

            rule = ACCESS_RULES.get(role)
            if not rule:
                return jsonify({"error": "No access rule defined for role"}), 403

            # Location check
            allowed_locations = rule["locations"]
            if "*" not in allowed_locations and location not in allowed_locations:
                return jsonify({"error": "Unauthorized location"}), 403

            # Time window check
            try:
                upload_time = datetime.datetime.fromisoformat(upload_time_str)
            except Exception:
                return jsonify({"error": "Invalid upload time format"}), 400

            now = datetime.datetime.utcnow()
            diff = now - upload_time
            if diff.total_seconds() > rule["time_window_hours"] * 3600:
                return jsonify({"error": "Access time expired"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
