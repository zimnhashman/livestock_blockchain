from flask import Blueprint, request, jsonify
from app.blockchain.contract import w3, contract, FARMER_ADDRESS, FARMER_PRIVATE_KEY
import time

sensor_bp = Blueprint('sensor', __name__, url_prefix='/sensor')

@sensor_bp.route('/upload', methods=['POST'])
def upload_sensor_data():
    data = request.json
    temperature = data.get('temperature')
    acceleration = data.get('acceleration')
    timestamp = data.get('timestamp') or int(time.time())

    if temperature is None or acceleration is None:
        return jsonify({'error': 'Missing temperature or acceleration'}), 400

    nonce = w3.eth.get_transaction_count(FARMER_ADDRESS)

    txn = contract.functions.storeSensorData(
        temperature, acceleration, timestamp
    ).build_transaction({
        'from': FARMER_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'chainId': w3.eth.chain_id
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=FARMER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return jsonify({'tx_hash': tx_hash.hex(), 'status': receipt.status})
