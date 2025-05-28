# app.py
from flask import Flask, request, jsonify
from services.blockchain import blockchain
import hashlib

app = Flask(__name__)


@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json
    data_id = hashlib.sha256(data['content'].encode()).hexdigest()

    tx = blockchain.submitData(
        data_id,
        hashlib.sha256(data['content'].encode()).hexdigest(),
        data['geo_hash']
    )

    return jsonify({
        "data_id": data_id,
        "tx_hash": tx.transactionHash
    })


if __name__ == '__main__':
    app.run(port=5000)