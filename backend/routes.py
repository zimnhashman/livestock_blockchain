from flask import Blueprint, request, jsonify
from db.models import SessionLocal, SensorData  # Your model file
from blockchain.contract import send_sensor_data
import datetime
import json

bp = Blueprint('api', __name__)

@bp.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    db = SessionLocal()

    try:
        temperature = float(data.get('temperature'))
        acceleration = float(data.get('acceleration'))
        access_control = data.get('access_control', [])  # Expect a list of allowed roles

        # Send data to blockchain
        tx_hash = send_sensor_data(temperature, acceleration)

        # Store to DB
        sensor_entry = SensorData(
            temperature=temperature,
            acceleration=acceleration,
            tx_hash=tx_hash,
            timestamp=datetime.datetime.utcnow(),
            access_control=json.dumps(access_control)  # Store as JSON string
        )
        db.add(sensor_entry)
        db.commit()

        return jsonify({'status': 'success', 'tx_hash': tx_hash}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        db.close()


@bp.route('/sensor-data', methods=['GET'])
def get_all_sensor_data():
    role = request.headers.get('Role')
    encryption_key = request.headers.get('Encryption-Key')
    if not role or not encryption_key:
        return jsonify({'status': 'error', 'message': 'Missing Role or Encryption-Key header'}), 400

    db = SessionLocal()
    try:
        entries = db.query(SensorData).all()
        allowed_entries = []
        for entry in entries:
            allowed_roles = json.loads(entry.access_control)
            if role in allowed_roles:
                allowed_entries.append({
                    'id': entry.id,
                    'temperature': entry.temperature,
                    'acceleration': entry.acceleration,
                    'timestamp': entry.timestamp.isoformat(),
                    'tx_hash': entry.tx_hash
                })
        return jsonify({'status': 'success', 'data': allowed_entries}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        db.close()


@bp.route('/sensor-data/<int:id>', methods=['GET'])
def get_sensor_data(id):
    role = request.headers.get('Role')
    encryption_key = request.headers.get('Encryption-Key')
    if not role or not encryption_key:
        return jsonify({'status': 'error', 'message': 'Missing Role or Encryption-Key header'}), 400

    db = SessionLocal()
    try:
        entry = db.query(SensorData).filter(SensorData.id == id).first()
        if not entry:
            return jsonify({'status': 'error', 'message': 'Entry not found'}), 404

        allowed_roles = json.loads(entry.access_control)
        if role not in allowed_roles:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

        return jsonify({
            'status': 'success',
            'data': {
                'id': entry.id,
                'temperature': entry.temperature,
                'acceleration': entry.acceleration,
                'timestamp': entry.timestamp.isoformat(),
                'tx_hash': entry.tx_hash
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        db.close()
