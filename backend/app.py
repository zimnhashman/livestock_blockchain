from flask import Flask, request, jsonify
from blockchain.contract import send_sensor_data
from models import SessionLocal, SensorData, init_db
from services.blockchain import send_sensor_data


app = Flask(__name__)
init_db()


@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400

    try:
        temperature = int(data.get('temperature'))
        acceleration = int(data.get('acceleration'))
    except (ValueError, TypeError):
        return jsonify(
            {'status': 'error', 'message': 'Invalid input: temperature and acceleration must be integers'}), 400

    db = SessionLocal()
    try:
        # Send to blockchain smart contract
        tx_hash = send_sensor_data(temperature, acceleration)

        # Save to DB
        sensor_entry = SensorData(
            temperature=temperature,
            acceleration=acceleration,
            tx_hash=tx_hash
        )
        db.add(sensor_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        db.close()

    return jsonify({'status': 'success', 'tx_hash': tx_hash}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
