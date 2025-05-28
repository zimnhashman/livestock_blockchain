from flask import Blueprint, request, jsonify
from app.blockchain.contract import w3, contract, FARMER_ADDRESS, FARMER_PRIVATE_KEY
import time

sensor_bp = Blueprint('sensor_bp', __name__)

@sensor_bp.route('/upload-sensor', methods=['POST'])
def upload_sensor_data():
    data = request.get_json()

    try:
        animal_id = data['animal_id']
        temp = float(data['temperature'])
        heart = int(data['heart_rate'])
        ts = int(time.time())

        # Prepare transaction
        nonce = w3.eth.get_transaction_count(FARMER_ADDRESS)
        txn = contract.functions.logSensorData(
            animal_id,
            int(temp * 100),  # store as integer (e.g., 38.5°C → 3850)
            heart,
            ts
        ).build_transaction({
            'chainId': 1337,
            'gas': 200000,
            'gasPrice': w3.to_wei('1', 'gwei'),
            'nonce': nonce
        })

        # Sign and send
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=FARMER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return jsonify({'status': 'success', 'tx_hash': tx_hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
